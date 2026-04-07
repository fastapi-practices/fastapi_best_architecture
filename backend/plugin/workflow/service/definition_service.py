import json
from collections import deque

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.workflow.crud.crud_definition import workflow_definition_dao
from backend.plugin.workflow.schema.definition import CreateWorkflowDefinitionParam, UpdateWorkflowDefinitionParam
from backend.plugin.workflow.service.instance_service import _get_user_dept_id, _get_user_name, _resolve_node_assignee_runtime


class WorkflowDefinitionService:
    @staticmethod
    def _serialize_config(value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False)

    @staticmethod
    def _parse_config(value):
        if not value:
            return {}
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}

    @classmethod
    def _validate_flow_config(cls, flow_config) -> None:
        parsed = cls._parse_config(flow_config)
        nodes = parsed.get('nodes') if isinstance(parsed, dict) else None
        edges = parsed.get('edges') if isinstance(parsed, dict) else None
        if not isinstance(nodes, list) or not isinstance(edges, list):
            raise errors.RequestError(msg='流程配置格式不正确')

        node_map = {
            node.get('id'): node
            for node in nodes
            if isinstance(node, dict) and node.get('id')
        }
        node_ids = set(node_map.keys())
        start_nodes = [node for node in nodes if isinstance(node, dict) and node.get('type') == 'START']
        end_nodes = [node for node in nodes if isinstance(node, dict) and node.get('type') == 'END']
        approver_nodes = [node for node in nodes if isinstance(node, dict) and node.get('type') == 'APPROVER']
        if not start_nodes:
            raise errors.RequestError(msg='流程缺少开始节点')
        if len(start_nodes) != 1:
            raise errors.RequestError(msg='当前仅支持一个开始节点')
        if not end_nodes:
            raise errors.RequestError(msg='流程缺少结束节点')
        if len(end_nodes) != 1:
            raise errors.RequestError(msg='当前仅支持一个结束节点')
        if not approver_nodes:
            raise errors.RequestError(msg='流程至少需要一个审批节点')

        edge_map: dict[str, list[str]] = {}
        reverse_edge_map: dict[str, list[str]] = {}
        for edge in edges:
            if not isinstance(edge, dict):
                raise errors.RequestError(msg='流程连线格式不正确')
            source = edge.get('source')
            target = edge.get('target')
            if source not in node_ids or target not in node_ids:
                raise errors.RequestError(msg='流程连线包含无效节点')
            edge_map.setdefault(source, []).append(target)
            reverse_edge_map.setdefault(target, []).append(source)

        start_id = start_nodes[0].get('id')
        next_edges = edge_map.get(start_id, [])
        if len(next_edges) != 1:
            raise errors.RequestError(msg='开始节点必须且只能连接一个下游节点')

        visited: set[str] = set()
        queue = deque([start_id])
        while queue:
            node_id = queue.popleft()
            if node_id in visited:
                continue
            visited.add(node_id)
            node = node_map.get(node_id)
            if not isinstance(node, dict):
                continue
            node_type = node.get('type')
            outgoing = edge_map.get(node_id, [])
            incoming = reverse_edge_map.get(node_id, [])
            if node_type == 'END':
                if outgoing:
                    raise errors.RequestError(msg='结束节点不能连接下游节点')
                continue
            if node_type == 'START':
                if incoming:
                    raise errors.RequestError(msg='开始节点不能有上游节点')

            if node_type == 'PARALLEL':
                if len(outgoing) < 2:
                    raise errors.RequestError(msg='并行节点至少需要两个下游分支')
            elif node_type != 'CONDITION' and len(outgoing) > 1:
                raise errors.RequestError(msg='当前运行时仅条件节点和并行节点支持多个下游节点')
            if not outgoing:
                raise errors.RequestError(msg=f"节点“{node.get('data', {}).get('label') or node_id}”缺少下游节点")

            if node_type == 'APPROVER':
                data = node.get('data') or {}
                approver_type = data.get('approverType') or data.get('approver_type') or 'DESIGNATED_USER'
                approver_id = data.get('approver_id') or data.get('approverId')
                approver_ids = data.get('approver_ids') or data.get('approverIds') or []
                role_ids = data.get('roleIds') or data.get('role_ids') or []
                form_field_key = data.get('formFieldKey') or data.get('form_field_key')
                dept_level = data.get('deptLevel') or data.get('dept_level')
                self_select_options = data.get('selfSelectOptions') or data.get('self_select_options') or []
                if approver_type == 'DESIGNATED_ROLE':
                    if not isinstance(role_ids, list) or not role_ids:
                        raise errors.RequestError(msg=f"审批节点“{data.get('label') or node.get('id')}”未配置角色")
                elif approver_type == 'FORM_FIELD_USER':
                    if not form_field_key:
                        raise errors.RequestError(msg=f"审批节点“{data.get('label') or node.get('id')}”未配置表单用户字段")
                elif approver_type == 'DEPT_LEADER_UP':
                    if not dept_level:
                        raise errors.RequestError(msg=f"审批节点“{data.get('label') or node.get('id')}”未配置上级层级")
                elif approver_type == 'SELF_SELECT':
                    if not isinstance(self_select_options, list) or not self_select_options:
                        raise errors.RequestError(msg=f"审批节点“{data.get('label') or node.get('id')}”未配置自选范围")
                elif approver_type in {'INITIATOR', 'DEPT_LEADER', 'INITIATOR_LEADER'}:
                    pass
                elif not approver_id and not (isinstance(approver_ids, list) and approver_ids):
                    raise errors.RequestError(msg=f"审批节点“{data.get('label') or node.get('id')}”未配置审批人")
            elif node_type == 'CONDITION':
                data = node.get('data') or {}
                if len(outgoing) < 2:
                    raise errors.RequestError(msg='条件节点至少需要两个下游分支')
                condition_group = data.get('conditionGroup')
                if isinstance(condition_group, dict):
                    conditions = condition_group.get('conditions') or []
                    if condition_group.get('operator') not in {'AND', 'OR'}:
                        raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置条件关系")
                    if not isinstance(conditions, list) or not conditions:
                        raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置条件规则")
                    for condition in conditions:
                        if not isinstance(condition, dict) or not condition.get('field'):
                            raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置条件字段")
                        if not condition.get('operator'):
                            raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置比较方式")
                else:
                    if not data.get('conditionField'):
                        raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置条件字段")
                    if not data.get('conditionOperator'):
                        raise errors.RequestError(msg=f"条件节点“{data.get('label') or node.get('id')}”未配置比较方式")
            elif node_type == 'CC':
                data = node.get('data') or {}
                if len(outgoing) != 1:
                    raise errors.RequestError(msg='抄送节点必须且只能连接一个下游节点')
                cc_user_ids = data.get('ccUserIds') or []
                if not isinstance(cc_user_ids, list) or not cc_user_ids:
                    raise errors.RequestError(msg=f"抄送节点“{data.get('label') or node.get('id')}”未配置抄送人")
            elif node_type == 'TRIGGER':
                if len(outgoing) != 1:
                    raise errors.RequestError(msg='触发器节点必须且只能连接一个下游节点')
            elif node_type not in {'START', 'END', 'PARALLEL'}:
                raise errors.RequestError(msg=f'暂不支持节点类型：{node_type}')

            for next_node_id in outgoing:
                queue.append(next_node_id)

        end_id = end_nodes[0].get('id')
        if end_id not in visited:
            raise errors.RequestError(msg='流程未形成到结束节点的有效路径')

    @classmethod
    def _normalize_definition_payload(cls, obj):
        flow_config = obj.get('flow_config') if isinstance(obj, dict) else obj.flow_config
        form_config = obj.get('form_config') if isinstance(obj, dict) else obj.form_config
        cls._validate_flow_config(flow_config)
        payload = obj.model_dump() if hasattr(obj, 'model_dump') else dict(obj)
        payload['flow_config'] = cls._serialize_config(flow_config)
        payload['form_config'] = cls._serialize_config(form_config)
        return payload

    @staticmethod
    async def get_list(*, db):
        return await paging_data(db, await workflow_definition_dao.get_select())

    @staticmethod
    async def get_available_list(*, db):
        return await paging_data(db, await workflow_definition_dao.get_available_select())

    @staticmethod
    async def get(*, db, pk: int):
        model = await workflow_definition_dao.get(db, pk)
        if not model:
            raise errors.NotFoundError(msg='流程定义不存在')
        return model

    @staticmethod
    async def get_available(*, db, pk: int):
        model = await workflow_definition_dao.get_available(db, pk)
        if not model:
            raise errors.NotFoundError(msg='流程定义不存在或未发布')
        return model

    @classmethod
    async def create(cls, *, db, obj: CreateWorkflowDefinitionParam) -> None:
        if await workflow_definition_dao.get_by_code(db, obj.code):
            raise errors.ConflictError(msg='流程编码已存在')
        await workflow_definition_dao.create(db, cls._normalize_definition_payload(obj))

    @classmethod
    async def preview_flow(cls, *, db, definition, user_id: int, form_data: dict | None = None) -> dict:
        parsed = cls._parse_config(definition.flow_config)
        if not isinstance(parsed, dict):
            return {'items': []}
        nodes = parsed.get('nodes') or []
        edges = parsed.get('edges') or []
        if not isinstance(nodes, list) or not isinstance(edges, list):
            return {'items': []}

        node_map = {
            node.get('id'): node
            for node in nodes
            if isinstance(node, dict) and node.get('id')
        }
        start_nodes = [
            str(node.get('id'))
            for node in nodes
            if isinstance(node, dict) and node.get('type') == 'START' and node.get('id')
        ]
        edge_map: dict[str, list[str]] = {}
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            source = edge.get('source')
            target = edge.get('target')
            if source and target:
                edge_map.setdefault(source, []).append(target)

        runtime_form_data = form_data or {}
        initiator_dept_id = await _get_user_dept_id(db, user_id)
        preview_items: list[dict] = []
        visited: set[str] = set()

        async def append_node(node: dict, *, assignee_id: int | None = None, assignee_name: str | None = None):
            data = node.get('data') or {}
            self_select_options = data.get('selfSelectOptions') or data.get('self_select_options') or []
            normalized_options = [int(item) for item in self_select_options if str(item).isdigit()]
            self_select_option_labels = {
                option_id: (await _get_user_name(db, option_id)) or f'用户#{option_id}'
                for option_id in normalized_options
            }
            preview_items.append({
                'node_id': str(node.get('id') or ''),
                'node_type': str(node.get('type') or ''),
                'label': str((node.get('data') or {}).get('label') or node.get('id') or ''),
                'assignee_id': assignee_id,
                'assignee_name': assignee_name,
                'self_select_options': normalized_options,
                'self_select_option_labels': self_select_option_labels,
            })

        def evaluate_rule(rule: dict) -> bool:
            field = rule.get('field')
            operator = rule.get('operator') or 'EQ'
            expected_value = rule.get('value')
            if not field:
                return False
            current_value = runtime_form_data.get(field)
            if operator == 'EQ':
                return str(current_value) == str(expected_value)
            if operator == 'NEQ':
                return str(current_value) != str(expected_value)
            if operator == 'CONTAINS':
                return str(expected_value or '') in str(current_value or '')
            try:
                current_number = float(current_value)
                expected_number = float(expected_value)
            except (TypeError, ValueError):
                return False
            if operator == 'GT':
                return current_number > expected_number
            if operator == 'GTE':
                return current_number >= expected_number
            if operator == 'LT':
                return current_number < expected_number
            if operator == 'LTE':
                return current_number <= expected_number
            return False

        def condition_targets(node: dict) -> list[str]:
            node_id = node.get('id')
            if not node_id:
                return []
            targets = edge_map.get(node_id, [])
            if not targets:
                return []
            data = node.get('data') or {}
            condition_group = data.get('conditionGroup') or {
                'operator': 'AND',
                'conditions': [
                    {
                        'field': data.get('conditionField') or '',
                        'operator': data.get('conditionOperator') or 'EQ',
                        'value': data.get('conditionValue'),
                    }
                ],
            }
            conditions = condition_group.get('conditions') or []
            results = [evaluate_rule(condition) for condition in conditions if isinstance(condition, dict)]
            matched = any(results) if condition_group.get('operator') == 'OR' else all(results)
            if matched:
                return targets[:1]
            return targets[1:2] if len(targets) > 1 else targets[:1]

        async def walk(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)
            node = node_map.get(node_id)
            if not isinstance(node, dict):
                return
            node_type = node.get('type')
            if node_type == 'APPROVER':
                assignee_id, assignee_name = await _resolve_node_assignee_runtime(
                    db=db,
                    node=node,
                    initiator_id=user_id,
                    initiator_dept_id=initiator_dept_id,
                    form_data=runtime_form_data,
                )
                await append_node(node, assignee_id=assignee_id, assignee_name=assignee_name)
                return
            await append_node(node)
            if node_type == 'CONDITION':
                for next_node_id in condition_targets(node):
                    await walk(next_node_id)
                return
            if node_type == 'PARALLEL':
                for next_node_id in edge_map.get(node_id, []):
                    await walk(next_node_id)
                return
            for next_node_id in edge_map.get(node_id, [])[:1]:
                await walk(next_node_id)

        for start_node_id in start_nodes[:1]:
            await walk(start_node_id)
        return {'items': preview_items}

    @classmethod
    async def update(cls, *, db, pk: int, obj: UpdateWorkflowDefinitionParam) -> int:
        model = await workflow_definition_dao.get(db, pk)
        if not model:
            raise errors.NotFoundError(msg='流程定义不存在')
        if model.code != obj.code and await workflow_definition_dao.get_by_code(db, obj.code):
            raise errors.ConflictError(msg='流程编码已存在')
        return await workflow_definition_dao.update(db, pk, cls._normalize_definition_payload(obj))


workflow_definition_service = WorkflowDefinitionService()
