import operator

from collections import defaultdict, namedtuple
from collections.abc import Sequence
from decimal import Decimal
from functools import lru_cache
from typing import Any, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


class MsgSpecJSONResponse(JSONResponse):
    """
    使用高性能的 msgspec 库将数据序列化为 JSON 的响应类
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)


def select_columns_serialize(row: R) -> dict[str, Any]:
    """
    序列化 SQLAlchemy 查询表的列，不包含关联列

    :param row: SQLAlchemy 查询结果行
    :return:
    """
    result = {}

    if not row:
        return result

    for column in row.__table__.columns.keys():
        value = getattr(row, column)
        if isinstance(value, Decimal):
            value = decimal_encoder(value)
        result[column] = value

    return result


def select_list_serialize(row: Sequence[R]) -> list[dict[str, Any]]:
    """
    序列化 SQLAlchemy 查询列表

    :param row: SQLAlchemy 查询结果列表
    :return:
    """
    return [select_columns_serialize(item) for item in row]


def select_as_dict(row: R, *, use_alias: bool = False) -> dict[str, Any]:
    """
    将 SQLAlchemy 查询结果转换为字典，可以包含关联数据

    :param row: SQLAlchemy 查询结果行
    :param use_alias: 是否使用别名作为列名
    :return:
    """
    result = {}

    if not row:
        return result

    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        mapper = class_mapper(row.__class__)  # type: ignore
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)

    return result


def select_join_serialize(  # noqa: C901
    row: R | Sequence[R],
    relationships: list[str] | None = None,
    *,
    return_as_dict: bool = False,
) -> dict[str, Any] | list[dict[str, Any]] | tuple[Any, ...] | list[tuple[Any, ...]] | None:
    """
    将 SQLAlchemy 连接查询结果序列化为字典或支持属性访问的 namedtuple

    扁平序列化：``relationships=None``
        | 将所有查询结果平铺到同一层级，不进行嵌套处理
        输出：Result(name='Alice', dept=Dept(...))

    嵌套序列化：``relationships=['User-m2o-Dept', 'User-m2m-Role:permissions', 'Role-m2m-Menu']``
        | 根据指定的关系类型将数据嵌套组织，支持层级结构
        | row = select(User, Dept, Role).join(...).all()
        输出：Result(name='Alice', dept=Dept(...), permissions=[Role(..., menus=[Menu(...)])])

    :param row: SQLAlchemy 查询结果
    :param relationships: 表之间的虚拟关系

         source_model_class-type-target_model_class[:custom_name], type: o2m/m2o/o2o/m2m

        - o2m (一对多): 目标模型类名会自动添加's'变为复数形式 (如: dept->depts)
        - m2o (多对一): 目标模型类名保持单数形式 (如: user->user)
        - o2o (一对一): 目标模型类名保持单数形式 (如: profile->profile)
        - m2m (多对多): 目标模型类名会自动添加's'变为复数形式 (如: role->roles)
        - 自定义名称: 可以通过在关系字符串末尾添加 ':custom_name' 来指定自定义的目标字段名
          例如: 'User-m2m-Role:permissions' 会将角色数据放在 'permissions' 字段而不是默认的 'roles'

    :param return_as_dict: False 返回 namedtuple，True 返回 dict
    :return:
    """

    def get_relation_key(target_: str, rel_type_: str, custom_name_: str | None = None) -> str:
        if custom_name_:
            return custom_name_
        return target_ if rel_type_ in ['o2o', 'm2o'] else target_ + 's'

    if not row:
        return None

    is_single = not isinstance(row, list)
    rows_list = [row] if is_single else row

    if not rows_list:
        return None

    # 获取主结构，取第一行第一列，类似于 scalar()
    first_row = rows_list[0]
    main_obj = first_row[0] if hasattr(first_row, '__getitem__') and len(first_row) > 0 else first_row

    if main_obj is None:
        return None

    main_cls = type(main_obj)
    main_obj_name = main_cls.__name__.lower()
    main_mapper = class_mapper(main_cls)
    main_columns = [
        prop.key
        for prop in main_mapper.iterate_properties
        if isinstance(prop, (ColumnProperty, SynonymProperty)) and hasattr(main_obj, prop.key)
    ]

    # 单一遍历收集所有必要信息
    sub_objs = {}
    cls_idxs = {}
    main_ids = set()
    flat_grouped = defaultdict(lambda: defaultdict(list))
    all_layer_instances = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    sub_obj_names = set()
    has_relationships = bool(relationships)

    if has_relationships:
        relation_graph = defaultdict(dict)
        reverse_relation = {}
        custom_names = {}
        for rel_str in relationships:
            if ':' in rel_str:
                rel_part, custom_name = rel_str.split(':', 1)
                custom_name = custom_name.strip()
            else:
                rel_part = rel_str
                custom_name = None

            parts = rel_part.split('-')
            if len(parts) != 3:
                continue
            source, rel_type, target = (
                parts[0].lower(),
                parts[1].lower(),
                parts[2].lower(),
            )
            if rel_type not in ['o2m', 'm2o', 'o2o', 'm2m']:
                continue
            relation_graph[source][target] = rel_type
            reverse_relation[target] = source
            if custom_name:
                custom_names[source, target] = custom_name

    for i, row in enumerate(rows_list):
        if hasattr(row, '__getitem__'):
            row_items = row
        else:
            row_items = (row,)
            if row is None:
                continue

        main = row_items[0]
        if main is None:
            continue

        main_id = getattr(main, 'id', None) or id(main)
        main_ids.add(main_id)
        flat_grouped[main_id]['main'] = main  # 只在第一次设置 main
        if i == 0:
            cls_idxs[main_obj_name] = 0

        for j, obj in enumerate(row_items[1:], 1):
            if obj is None:
                continue
            cls_name = type(obj).__name__.lower()
            if cls_name not in sub_obj_names:
                sub_obj_names.add(cls_name)
                sub_mapper = class_mapper(type(obj))
                sub_objs[cls_name] = [
                    prop.key
                    for prop in sub_mapper.iterate_properties
                    if isinstance(prop, (ColumnProperty, SynonymProperty))
                ]
            if i == 0:
                cls_idxs[cls_name] = j
            flat_grouped[main_id][cls_name].append(obj)

            if has_relationships and cls_name in reverse_relation:
                parent_layer = reverse_relation[cls_name]
                parent_idx = cls_idxs.get(parent_layer, 0)
                parent_obj = row_items[parent_idx]
                if parent_obj is None:
                    continue
                parent_id = getattr(parent_obj, 'id', None)
                if parent_id is None:
                    continue
                all_layer_instances[main_id][cls_name][parent_id].append(obj)

    if not main_ids:
        return None

    group_keys = dict.fromkeys(sub_obj_names, 'id')

    # 子类型预计算
    sub_types = {}
    sub_full_fields = {}
    for sub_obj_name, sub_columns in sub_objs.items():
        child_rel_keys = []
        if has_relationships:
            for target, rel_type in relation_graph[sub_obj_name].items():
                custom_name = custom_names.get((sub_obj_name, target))
                child_rel_keys.append(get_relation_key(target, rel_type, custom_name))
            child_rel_keys = sorted(child_rel_keys)
        full_columns = sub_columns + child_rel_keys
        sub_full_fields[sub_obj_name] = full_columns
        if not return_as_dict and full_columns:
            if child_rel_keys:
                sub_types[sub_obj_name] = namedtuple(sub_obj_name.capitalize(), full_columns)  # noqa: PYI024
            else:
                sub_types[sub_obj_name] = namedtuple(sub_obj_name.capitalize(), sub_columns)  # noqa: PYI024

    if has_relationships:
        # 顶级收集
        top_level_subs = sorted(relation_graph[main_obj_name].keys())
        for main_id in main_ids:
            for layer in top_level_subs:
                if layer in cls_idxs:
                    for obj in flat_grouped[main_id].get(layer, []):
                        all_layer_instances[main_id][layer][main_id].append(obj)

        # 预计算主结果字段
        result_fields = main_columns.copy()
        if not return_as_dict:
            top_keys = []
            for top_layer in top_level_subs:
                rel_type = relation_graph[main_obj_name][top_layer]
                custom_name = custom_names.get((main_obj_name, top_layer))
                top_keys.append(get_relation_key(top_layer, rel_type, custom_name))
            result_fields.extend(top_keys)
            result_type = namedtuple('Result', result_fields) if result_fields else None  # noqa: PYI024

        # 递归构建
        @lru_cache(maxsize=128)
        def build_nested(layer_name: str, parent_id_: int, main_id_: int) -> list:
            objs_list = all_layer_instances[main_id_][layer_name].get(parent_id_, [])
            layer_key = group_keys.get(layer_name, 'id')

            node_map_ = {}
            for obj_ in objs_list:
                layer_id = getattr(obj_, layer_key, None)
                if layer_id is not None and layer_id not in node_map_:
                    node_map_[layer_id] = obj_

            instances = []
            sub_columns_ = sub_objs.get(layer_name, [])
            child_rels = sorted(relation_graph[layer_name].items(), key=operator.itemgetter(0))
            sub_full_fields.get(layer_name, [])

            nt_type = sub_types.get(layer_name) if not return_as_dict else None

            for obj_ in node_map_.values():
                nest_dict = {col: getattr(obj_, col, None) for col in sub_columns_}

                for child_name_, rel_type_ in child_rels:
                    child_parent_id = getattr(obj_, group_keys.get(layer_name, 'id'), None)
                    if child_parent_id is None:
                        continue
                    child_instances = build_nested(child_name_, child_parent_id, main_id_)
                    custom_name_ = custom_names.get((layer_name, child_name_))
                    child_key = get_relation_key(child_name_, rel_type_, custom_name_)
                    if rel_type_ in ['m2o', 'o2o']:
                        nest_dict[child_key] = child_instances[0] if child_instances else None
                    else:
                        nest_dict[child_key] = child_instances

                if return_as_dict:
                    instances.append(nest_dict)
                else:
                    instances.append(nt_type(**nest_dict))
            return instances

    # 构建结果 list
    result_list = []
    sorted_main_ids = sorted(main_ids)  # 排序以保持确定性
    for main_id in sorted_main_ids:
        main = flat_grouped[main_id]['main']
        nest_data = {col: getattr(main, col, None) for col in main_columns}
        if has_relationships:
            for top_layer in top_level_subs:
                rel_type = relation_graph[main_obj_name][top_layer]
                custom_name = custom_names.get((main_obj_name, top_layer))
                top_key = get_relation_key(top_layer, rel_type, custom_name)
                top_instances = build_nested(top_layer, main_id, main_id)
                if rel_type in ['m2o', 'o2o']:
                    nest_data[top_key] = top_instances[0] if top_instances else None
                else:
                    nest_data[top_key] = top_instances
        else:
            for sub_obj in sorted(sub_obj_names):
                subs = flat_grouped[main_id].get(sub_obj, [])
                sub_columns = sub_objs.get(sub_obj, [])
                group_key = group_keys.get(sub_obj, 'id')
                node_map = {}
                for obj in subs:
                    obj_id = getattr(obj, group_key, None)
                    if obj_id is not None and obj_id not in node_map:
                        node_map[obj_id] = obj
                unique_objs = list(node_map.values())
                if not unique_objs:
                    nest_data[sub_obj] = []
                elif len(unique_objs) == 1:
                    if return_as_dict:
                        nest_data[sub_obj] = {col: getattr(unique_objs[0], col, None) for col in sub_columns}
                    else:
                        nt_type = sub_types.get(sub_obj)
                        nest_data[sub_obj] = nt_type(**{col: getattr(unique_objs[0], col, None) for col in sub_columns})
                else:
                    if return_as_dict:
                        nest_data[sub_obj] = [
                            {col: getattr(obj, col, None) for col in sub_columns} for obj in unique_objs
                        ]
                    else:
                        nt_type = sub_types.get(sub_obj)
                        nest_data[sub_obj] = [
                            nt_type(**{col: getattr(obj, col, None) for col in sub_columns}) for obj in unique_objs
                        ]

        if not return_as_dict:
            if has_relationships:
                result_list.append(result_type(**nest_data))
            else:
                result_fields = main_columns + sorted(sub_obj_names)
                result_type = namedtuple('Result', result_fields)  # noqa: PYI024
                result_list.append(result_type(**nest_data))
        else:
            result_list.append(nest_data)

    return result_list[0] if len(result_list) == 1 else result_list
