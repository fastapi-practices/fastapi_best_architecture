from collections import defaultdict, namedtuple
from collections.abc import Sequence
from decimal import Decimal
from typing import Any, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

RowData = Row[Any] | RowMapping | Any

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
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        result = {}
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

    def get_relation_key(model_name: str, rel_type: str, custom_field: str | None = None) -> str:
        """获取关系键名"""
        return custom_field or (model_name if rel_type in ('o2o', 'm2o') else f'{model_name}s')

    def parse_relationships(relationship_list: list[str]) -> tuple[dict, dict, dict]:
        """解析关系定义"""
        if not relationship_list:
            return {}, {}, {}

        parsed_relation_graph = defaultdict(dict)
        parsed_reverse_relation = {}
        parsed_custom_names = {}

        for rel_str in relationship_list:
            parts = rel_str.split(':', 1)
            rel_part = parts[0].strip()
            field_custom_name = parts[1].strip() if len(parts) > 1 else None

            rel_info = rel_part.split('-')
            if len(rel_info) != 3:
                continue

            source_model, rel_type, target_model = (info.lower() for info in rel_info)
            if rel_type not in ('o2m', 'm2o', 'o2o', 'm2m'):
                continue

            parsed_relation_graph[source_model][target_model] = rel_type
            parsed_reverse_relation[target_model] = source_model
            if field_custom_name:
                parsed_custom_names[source_model, target_model] = field_custom_name

        return parsed_relation_graph, parsed_reverse_relation, parsed_custom_names

    def get_model_columns(model_obj: Any) -> list[str]:
        """获取模型列名"""
        mapper = class_mapper(type(model_obj))
        return [
            prop.key
            for prop in mapper.iterate_properties
            if isinstance(prop, (ColumnProperty, SynonymProperty)) and hasattr(model_obj, prop.key)
        ]

    def get_unique_objects(objs: list[Any], key_attr: str = 'id') -> list[Any]:
        """根据键属性去重对象列表"""
        seen = set()
        unique = []
        for item in objs:
            item_id = getattr(item, key_attr, None)
            if item_id is not None and item_id not in seen:
                seen.add(item_id)
                unique.append(item)
        return unique

    if not row:
        return None

    rows_list = [row] if not isinstance(row, list) else row
    if not rows_list:
        return None

    # 获取主对象信息
    first_row = rows_list[0]
    main_obj = first_row[0] if hasattr(first_row, '__getitem__') and first_row else first_row
    if main_obj is None:
        return None

    main_obj_name = type(main_obj).__name__.lower()
    main_columns = get_model_columns(main_obj)

    # 解析关系
    relation_graph, reverse_relation, custom_names = parse_relationships(relationships or [])
    has_relationships = bool(relation_graph)

    # 预处理所有模型类型和列信息
    model_info = {}
    cls_idxs = {}

    for preprocess_row in rows_list:
        preprocess_row_items = preprocess_row if hasattr(preprocess_row, '__getitem__') else (preprocess_row,)
        for idx, row_obj in enumerate(preprocess_row_items):
            if row_obj is None:
                continue
            obj_class_name = type(row_obj).__name__.lower()
            if obj_class_name not in model_info:
                model_info[obj_class_name] = get_model_columns(row_obj)
            if obj_class_name not in cls_idxs:
                cls_idxs[obj_class_name] = idx

    # 数据收集和分组
    main_data = {}
    grouped_data = defaultdict(lambda: defaultdict(list))

    for data_row in rows_list:
        data_row_items = data_row if hasattr(data_row, '__getitem__') else (data_row,)
        if not data_row_items or data_row_items[0] is None:
            continue

        main_obj = data_row_items[0]
        main_id = getattr(main_obj, 'id', None) or id(main_obj)

        if main_id not in main_data:
            main_data[main_id] = main_obj

        # 收集子对象
        for child_obj in data_row_items[1:]:
            if child_obj is None:
                continue
            child_class_name = type(child_obj).__name__.lower()
            grouped_data[main_id][child_class_name].append(child_obj)

    if not main_data:
        return None

    # 预生成 namedtuple 类型
    namedtuple_cache = {}
    if not return_as_dict:
        for cls_name, columns in model_info.items():
            if columns:
                # 为嵌套关系预计算完整字段列表
                full_columns = columns.copy()
                if has_relationships:
                    for target_class, relation_type in relation_graph.get(cls_name, {}).items():
                        field_name = custom_names.get((cls_name, target_class))
                        rel_key = get_relation_key(target_class, relation_type, field_name)
                        full_columns.append(rel_key)
                    full_columns = sorted(set(full_columns))  # 去重并排序

                namedtuple_cache[cls_name] = namedtuple(cls_name.capitalize(), full_columns or columns)  # noqa: PYI024

    def build_flat_result(build_main_id: int, build_main_obj: Any) -> dict[str, Any]:  # noqa: C901
        """构建扁平化结果"""
        flat_result = {col: getattr(build_main_obj, col, None) for col in main_columns}

        for class_name in sorted(grouped_data[build_main_id]):
            if class_name == main_obj_name:
                continue

            flat_objs = get_unique_objects(grouped_data[build_main_id][class_name])
            cls_columns = model_info.get(class_name, [])

            if not flat_objs:
                flat_result[class_name] = []
            elif len(flat_objs) == 1:
                obj_data = {col: getattr(flat_objs[0], col, None) for col in cls_columns}
                # 确保 namedtuple 所需的所有字段都存在
                if not return_as_dict and class_name in namedtuple_cache:
                    nt_fields = getattr(namedtuple_cache[class_name], '_fields', [])
                    for field in nt_fields:
                        if field not in obj_data:
                            obj_data[field] = None
                flat_result[class_name] = obj_data if return_as_dict else namedtuple_cache[class_name](**obj_data)
            else:
                if return_as_dict:
                    flat_result[class_name] = [
                        {col: getattr(flat_obj, col, None) for col in cls_columns} for flat_obj in flat_objs
                    ]
                else:
                    nested_result_list = []
                    for nested_obj in flat_objs:
                        obj_data = {col: getattr(nested_obj, col, None) for col in cls_columns}
                        # 确保 namedtuple 所需的所有字段都存在
                        if class_name in namedtuple_cache:
                            nt_fields = getattr(namedtuple_cache[class_name], '_fields', [])
                            for field in nt_fields:
                                if field not in obj_data:
                                    obj_data[field] = None
                        nested_result_list.append(namedtuple_cache[class_name](**obj_data))
                    flat_result[class_name] = nested_result_list

        return flat_result

    def build_nested_result(nested_main_id: int, nested_main_obj: Any) -> dict[str, Any]:  # noqa: C901
        """构建嵌套化结果"""
        nested_result = {col: getattr(nested_main_obj, col, None) for col in main_columns}

        # 构建关系层级数据结构
        hierarchy = defaultdict(lambda: defaultdict(list))
        for iter_row in rows_list:
            iter_row_items = iter_row if hasattr(iter_row, '__getitem__') else (iter_row,)
            if not iter_row_items or iter_row_items[0] is None:
                continue

            iter_main_id = getattr(iter_row_items[0], 'id', None) or id(iter_row_items[0])
            if iter_main_id != nested_main_id:
                continue

            for _i, related_obj in enumerate(iter_row_items[1:], 1):
                if related_obj is None:
                    continue
                related_class_name = type(related_obj).__name__.lower()

                if related_class_name in reverse_relation:
                    parent_cls = reverse_relation[related_class_name]
                    parent_idx = cls_idxs.get(parent_cls, 0)
                    if parent_idx < len(iter_row_items):
                        parent_obj = iter_row_items[parent_idx]
                        if parent_obj is not None:
                            parent_obj_id = getattr(parent_obj, 'id', None)
                            if parent_obj_id is not None:
                                hierarchy[related_class_name][parent_obj_id].append(related_obj)

        def build_recursive(current_cls_name: str, current_parent_id: int) -> list:
            """递归构建嵌套数据"""
            recursive_objs = get_unique_objects(hierarchy[current_cls_name].get(current_parent_id, []))
            if not recursive_objs:
                return []

            recursive_result = []
            for nested_obj in recursive_objs:
                # 基础数据
                obj_data = {col: getattr(nested_obj, col, None) for col in model_info[current_cls_name]}

                # 处理子关系
                for child_cls, child_rel_type in relation_graph.get(current_cls_name, {}).items():
                    child_parent_id = getattr(nested_obj, 'id', None)
                    if child_parent_id is None:
                        continue

                    child_list = build_recursive(child_cls, child_parent_id)
                    child_key = get_relation_key(
                        child_cls, child_rel_type, custom_names.get((current_cls_name, child_cls))
                    )

                    if child_rel_type in ('m2o', 'o2o'):
                        obj_data[child_key] = child_list[0] if child_list else None
                    else:
                        obj_data[child_key] = child_list

                if not return_as_dict and current_cls_name in namedtuple_cache:
                    nt_fields = getattr(namedtuple_cache[current_cls_name], '_fields', [])
                    for field in nt_fields:
                        if field not in obj_data:
                            obj_data[field] = None

                recursive_result.append(obj_data if return_as_dict else namedtuple_cache[current_cls_name](**obj_data))

            return recursive_result

        # 构建顶级关系
        for top_cls_name, top_rel_type in relation_graph.get(main_obj_name, {}).items():
            instances = build_recursive(top_cls_name, nested_main_id)
            key = get_relation_key(top_cls_name, top_rel_type, custom_names.get((main_obj_name, top_cls_name)))

            if top_rel_type in ('m2o', 'o2o'):
                nested_result[key] = instances[0] if instances else None
            else:
                nested_result[key] = instances

        return nested_result

    # 构建最终结果
    final_result_list = []
    for current_main_id in sorted(main_data.keys()):
        current_main_obj = main_data[current_main_id]

        if has_relationships:
            final_result_data = build_nested_result(current_main_id, current_main_obj)
        else:
            final_result_data = build_flat_result(current_main_id, current_main_obj)

        if not return_as_dict:
            all_fields = list(final_result_data.keys())
            result_type = namedtuple('Result', all_fields)  # noqa: PYI024
            final_result_list.append(result_type(**final_result_data))
        else:
            final_result_list.append(final_result_data)

    return final_result_list[0] if len(final_result_list) == 1 else final_result_list
