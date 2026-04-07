import json
from collections import deque

from sqlalchemy import func, select

from backend.app.admin.model import Dept, User, user_role
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.workflow.crud.crud_definition import workflow_definition_dao
from backend.plugin.workflow.crud.crud_instance import workflow_instance_dao
from backend.plugin.workflow.crud.crud_message import workflow_message_dao
from backend.plugin.workflow.crud.crud_task import workflow_task_dao
from backend.plugin.workflow.engine.instance_no_gen import instance_no_generator
from backend.plugin.workflow.model import WorkflowInstance, WorkflowMessage, WorkflowTask
from backend.plugin.workflow.schema.instance import StartWorkflowInstanceParam
from backend.plugin.workflow.service.message_service import workflow_message_service
from backend.utils.timezone import timezone


async def _todo_count(db, user_id: int) -> int:
    stmt = select(func.count(WorkflowTask.id)).where(
        WorkflowTask.assignee_id == user_id,
        WorkflowTask.status == 'PENDING',
    )
    return int((await db.execute(stmt)).scalar() or 0)


async def _has_user_pending_task_for_instance(db, instance_id: int, user_id: int) -> bool:
    stmt = select(func.count(WorkflowTask.id)).where(
        WorkflowTask.instance_id == instance_id,
        WorkflowTask.assignee_id == user_id,
        WorkflowTask.status == 'PENDING',
    )
    return int((await db.execute(stmt)).scalar() or 0) > 0


async def _get_pending_tasks_for_instance(db, instance_id: int) -> list[WorkflowTask]:
    stmt = (
        select(WorkflowTask)
        .where(
            WorkflowTask.instance_id == instance_id,
            WorkflowTask.status == 'PENDING',
        )
        .order_by(WorkflowTask.id.asc())
    )
    return list((await db.execute(stmt)).scalars().all())


async def _get_task_for_instance_node(db, instance_id: int, node_key: str) -> WorkflowTask | None:
    stmt = (
        select(WorkflowTask)
        .where(
            WorkflowTask.instance_id == instance_id,
            WorkflowTask.node_key == node_key,
        )
        .order_by(WorkflowTask.id.asc())
    )
    return (await db.execute(stmt)).scalars().first()


async def _sync_instance_runtime_state(db, instance_id: int, *, reached_end: bool) -> list[WorkflowTask]:
    pending_tasks = await _get_pending_tasks_for_instance(db, instance_id)
    if pending_tasks:
        await workflow_instance_dao.update_model(
            db,
            instance_id,
            {'current_task_id': pending_tasks[0].id, 'status': 'RUNNING'},
        )
        return pending_tasks
    if reached_end:
        await workflow_instance_dao.update_model(
            db,
            instance_id,
            {'status': 'APPROVED', 'current_task_id': None},
        )
        return []
    await workflow_instance_dao.update_model(
        db,
        instance_id,
        {'status': 'RUNNING', 'current_task_id': None},
    )
    return []


def _serialize_instance_detail(instance: WorkflowInstance | dict, *, todo_count: int | None = None) -> dict:
    if isinstance(instance, dict):
        data = dict(instance)
        if todo_count is not None:
            data['todo_count'] = todo_count
        return data

    data = {
        'id': instance.id,
        'instance_no': instance.instance_no,
        'definition_id': instance.definition_id,
        'title': instance.title,
        'initiator_id': instance.initiator_id,
        'status': instance.status,
        'current_task_id': instance.current_task_id,
        'form_data': instance.form_data,
        'remark': instance.remark,
        'created_time': instance.created_time,
        'updated_time': instance.updated_time,
    }
    if todo_count is not None:
        data['todo_count'] = todo_count
    return data



def _serialize_page_items(page_data, *, todo_count: int | None = None):
    page_data['items'] = [
        _serialize_instance_detail(item, todo_count=todo_count)
        for item in page_data['items']
    ]
    return page_data



def _serialize_single_instance(instance: WorkflowInstance, *, todo_count: int | None = None):
    return _serialize_instance_detail(instance, todo_count=todo_count)



def _parse_json_text(value: str | None):
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {'raw': value}



def _build_instance_detail_payload(
    instance: WorkflowInstance,
    *,
    todo_count: int | None = None,
    messages: list[WorkflowMessage] | None = None,
    definition=None,
) -> dict:
    data = _serialize_instance_detail(instance, todo_count=todo_count)
    data['form_data'] = _parse_json_text(instance.form_data)
    data['messages'] = messages or []
    data['allow_withdraw'] = getattr(definition, 'allow_withdraw', None) if definition else None
    data['allow_urge'] = getattr(definition, 'allow_urge', None) if definition else None
    return data



def _parse_flow_runtime(
    flow_config_text: str | None,
) -> tuple[dict[str, dict], dict[str, list[str]], dict[str, list[str]]]:
    if not flow_config_text:
        return {}, {}, {}
    try:
        flow_config = json.loads(flow_config_text)
    except json.JSONDecodeError:
        return {}, {}, {}
    if not isinstance(flow_config, dict):
        return {}, {}, {}

    nodes = flow_config.get('nodes') or []
    edges = flow_config.get('edges') or []
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return {}, {}, {}

    node_map = {
        node.get('id'): node
        for node in nodes
        if isinstance(node, dict) and node.get('id')
    }
    edge_map: dict[str, list[str]] = {}
    reverse_edge_map: dict[str, list[str]] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source = edge.get('source')
        target = edge.get('target')
        if source and target:
            edge_map.setdefault(source, []).append(target)
            reverse_edge_map.setdefault(target, []).append(source)
    return node_map, edge_map, reverse_edge_map


async def _get_user_name(db, user_id: int) -> str | None:
    user = await db.get(User, user_id)
    if not user:
        return None
    return user.nickname or user.username


async def _get_user_dept_id(db, user_id: int) -> int | None:
    user = await db.get(User, user_id)
    if not user or not user.dept_id:
        return None
    return int(user.dept_id)


async def _resolve_role_user(db, role_ids: list[int]) -> tuple[int | None, str | None]:
    normalized_role_ids = [int(role_id) for role_id in role_ids if isinstance(role_id, int) or str(role_id).isdigit()]
    if not normalized_role_ids:
        return None, None
    stmt = (
        select(User)
        .join(user_role, user_role.c.user_id == User.id)
        .where(user_role.c.role_id.in_(normalized_role_ids), User.status == 1)
        .order_by(User.id.asc())
    )
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        return None, None
    return int(user.id), user.nickname or user.username


async def _resolve_dept_leader_user(db, dept_id: int | None) -> tuple[int | None, str | None]:
    if not dept_id:
        return None, None
    dept = await db.get(Dept, dept_id)
    if not dept or not dept.leader:
        return None, None
    leader_name = str(dept.leader).strip()
    if not leader_name:
        return None, None
    stmt = select(User).where(User.status == 1, ((User.username == leader_name) | (User.nickname == leader_name))).order_by(User.id.asc())
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        return None, None
    return int(user.id), user.nickname or user.username


async def _resolve_dept_leader_up_user(db, dept_id: int | None, level: int) -> tuple[int | None, str | None]:
    current_dept_id = dept_id
    remaining = max(level, 1)
    while current_dept_id and remaining > 0:
        dept = await db.get(Dept, current_dept_id)
        if not dept:
            return None, None
        current_dept_id = int(dept.parent_id) if dept.parent_id else None
        remaining -= 1
    return await _resolve_dept_leader_user(db, current_dept_id)


async def _resolve_self_select_user(db, node: dict, form_data: dict) -> tuple[int | None, str | None]:
    node_id = str(node.get('id') or '')
    self_select_assignees = form_data.get('__self_select_assignees__') or {}
    selected_user_id = self_select_assignees.get(node_id) if isinstance(self_select_assignees, dict) else None
    if selected_user_id is not None and str(selected_user_id).isdigit():
        resolved_id = int(selected_user_id)
        return resolved_id, await _get_user_name(db, resolved_id)
    return None, None


async def _resolve_node_assignee_runtime(*, db, node: dict, initiator_id: int, initiator_dept_id: int | None, form_data: dict) -> tuple[int | None, str]:
    data = node.get('data') or {}
    approver_type = data.get('approverType') or data.get('approver_type') or 'DESIGNATED_USER'

    if approver_type == 'INITIATOR':
        return initiator_id, (await _get_user_name(db, initiator_id)) or data.get('label') or '审批'

    if approver_type in {'DEPT_LEADER', 'INITIATOR_LEADER'}:
        assignee_id, assignee_name = await _resolve_dept_leader_user(db, initiator_dept_id)
        return assignee_id, assignee_name or data.get('label') or '审批'

    if approver_type == 'DEPT_LEADER_UP':
        dept_level = data.get('deptLevel') or data.get('dept_level') or 1
        try:
            normalized_level = int(dept_level)
        except (TypeError, ValueError):
            normalized_level = 1
        assignee_id, assignee_name = await _resolve_dept_leader_up_user(db, initiator_dept_id, normalized_level)
        return assignee_id, assignee_name or data.get('label') or '审批'

    if approver_type == 'SELF_SELECT':
        assignee_id, assignee_name = await _resolve_self_select_user(db, node, form_data)
        return assignee_id, assignee_name or data.get('label') or '审批'

    if approver_type == 'FORM_FIELD_USER':
        form_field_key = data.get('formFieldKey') or data.get('form_field_key')
        form_user_id = form_data.get(form_field_key) if form_field_key else None
        if form_user_id is not None and str(form_user_id).isdigit():
            resolved_id = int(form_user_id)
            return resolved_id, (await _get_user_name(db, resolved_id)) or data.get('label') or '审批'
        return None, data.get('label') or '审批'

    if approver_type == 'DESIGNATED_ROLE':
        role_ids = data.get('roleIds') or data.get('role_ids') or []
        assignee_id, assignee_name = await _resolve_role_user(db, role_ids if isinstance(role_ids, list) else [])
        return assignee_id, assignee_name or data.get('label') or '审批'

    approver_id = data.get('approver_id') or data.get('approverId')
    approver_ids = data.get('approver_ids') or data.get('approverIds') or []
    resolved_assignee = approver_id
    if not resolved_assignee and isinstance(approver_ids, list) and approver_ids:
        resolved_assignee = approver_ids[0]
    if resolved_assignee and str(resolved_assignee).isdigit():
        resolved_id = int(resolved_assignee)
        return resolved_id, (await _get_user_name(db, resolved_id)) or data.get('label') or '审批'
    return None, data.get('label') or '审批'



def _evaluate_condition_rule(rule: dict, form_data: dict) -> bool:
    field = rule.get('field')
    operator = rule.get('operator') or 'EQ'
    expected_value = rule.get('value')
    if not field:
        return False
    current_value = form_data.get(field)
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



def _normalize_condition_group(data: dict) -> dict:
    condition_group = data.get('conditionGroup')
    if isinstance(condition_group, dict):
        operator = condition_group.get('operator') or 'AND'
        conditions = condition_group.get('conditions') or []
        if isinstance(conditions, list) and conditions:
            normalized_conditions = [
                condition
                for condition in conditions
                if isinstance(condition, dict)
            ]
            if normalized_conditions:
                return {'operator': operator, 'conditions': normalized_conditions}
    return {
        'operator': 'AND',
        'conditions': [
            {
                'field': data.get('conditionField') or '',
                'operator': data.get('conditionOperator') or 'EQ',
                'value': data.get('conditionValue'),
            }
        ],
    }



def _evaluate_condition(node: dict, form_data: dict) -> bool:
    data = node.get('data') or {}
    condition_group = _normalize_condition_group(data)
    conditions = condition_group.get('conditions') or []
    if not conditions:
        return False
    results = [_evaluate_condition_rule(condition, form_data) for condition in conditions]
    if condition_group.get('operator') == 'OR':
        return any(results)
    return all(results)



def _resolve_condition_targets(node: dict, edge_map: dict[str, list[str]], form_data: dict) -> list[str]:
    node_id = node.get('id')
    if not node_id:
        return []
    targets = edge_map.get(node_id, [])
    if not targets:
        return []
    if _evaluate_condition(node, form_data):
        return targets[:1]
    return targets[1:2] if len(targets) > 1 else targets[:1]


async def _is_node_completed_for_join(
    *,
    db,
    instance_id: int,
    node_id: str,
    node_map: dict[str, dict],
    reverse_edge_map: dict[str, list[str]],
    cache: dict[str, bool],
    path: set[str],
) -> bool:
    if node_id in cache:
        return cache[node_id]
    if node_id in path:
        return False
    node = node_map.get(node_id)
    if not isinstance(node, dict):
        return False

    node_type = node.get('type')
    if node_type == 'START':
        cache[node_id] = True
        return True

    if node_type == 'APPROVER':
        task = await _get_task_for_instance_node(db, instance_id, node_id)
        completed = bool(task and task.status != 'PENDING')
        cache[node_id] = completed
        return completed

    upstream_ids = reverse_edge_map.get(node_id, [])
    if not upstream_ids:
        cache[node_id] = False
        return False

    path.add(node_id)
    completed = True
    for upstream_id in upstream_ids:
        if not await _is_node_completed_for_join(
            db=db,
            instance_id=instance_id,
            node_id=upstream_id,
            node_map=node_map,
            reverse_edge_map=reverse_edge_map,
            cache=cache,
            path=path,
        ):
            completed = False
            break
    path.remove(node_id)
    cache[node_id] = completed
    return completed


async def _are_all_upstream_nodes_completed(
    *,
    db,
    instance_id: int,
    node_id: str,
    node_map: dict[str, dict],
    reverse_edge_map: dict[str, list[str]],
) -> bool:
    upstream_ids = reverse_edge_map.get(node_id, [])
    if len(upstream_ids) <= 1:
        return True
    cache: dict[str, bool] = {}
    for upstream_id in upstream_ids:
        if not await _is_node_completed_for_join(
            db=db,
            instance_id=instance_id,
            node_id=upstream_id,
            node_map=node_map,
            reverse_edge_map=reverse_edge_map,
            cache=cache,
            path=set(),
        ):
            return False
    return True



async def _notify_task_assignees(
    *,
    db,
    instance: WorkflowInstance,
    tasks: list[WorkflowTask],
    message_type: str,
    title: str,
    content: str,
):
    notified_user_ids: set[int] = set()
    for task in tasks:
        assignee_id = int(task.assignee_id)
        if assignee_id in notified_user_ids:
            continue
        notified_user_ids.add(assignee_id)
        notify_message = WorkflowMessage(
            receiver_id=assignee_id,
            instance_id=instance.id,
            task_id=task.id,
            message_type=message_type,
            title=title,
            content=content,
            is_read=False,
        )
        db.add(notify_message)
        await db.flush()
        await workflow_message_service.push_message(db=db, message=notify_message)


async def _push_pending_task_message(*, db, instance: WorkflowInstance, task: WorkflowTask):
    await _notify_task_assignees(
        db=db,
        instance=instance,
        tasks=[task],
        message_type='PENDING_APPROVAL',
        title='您有新的待审批任务',
        content=f'流程《{instance.title}》待您审批',
    )


async def _expand_runtime_from_nodes(
    *,
    db,
    instance: WorkflowInstance,
    definition,
    node_map: dict[str, dict],
    edge_map: dict[str, list[str]],
    reverse_edge_map: dict[str, list[str]],
    start_node_ids: list[str],
    initiator_dept_id: int | None,
    form_data: dict,
    base_sort: int,
) -> tuple[list[WorkflowTask], bool]:
    queue = deque(start_node_ids)
    processed: set[str] = set()
    created_tasks: list[WorkflowTask] = []
    reached_end = False

    while queue:
        node_id = queue.popleft()
        if node_id in processed:
            continue
        node = node_map.get(node_id)
        if not isinstance(node, dict):
            continue
        if not await _are_all_upstream_nodes_completed(
            db=db,
            instance_id=instance.id,
            node_id=node_id,
            node_map=node_map,
            reverse_edge_map=reverse_edge_map,
        ):
            continue
        processed.add(node_id)
        node_type = node.get('type')

        if node_type == 'APPROVER':
            if await _get_task_for_instance_node(db, instance.id, str(node_id)):
                continue
            assignee_id, task_name = await _resolve_node_assignee_runtime(
                db=db,
                node=node,
                initiator_id=instance.initiator_id,
                initiator_dept_id=initiator_dept_id,
                form_data=form_data,
            )
            if not assignee_id:
                node_label = str((node.get('data') or {}).get('label') or node_id)
                raise errors.RequestError(msg=f'审批节点“{node_label}”未匹配到审批人，请检查审批人配置或部门负责人数据')
            task = WorkflowTask(
                instance_id=instance.id,
                definition_id=definition.id,
                task_name=task_name,
                assignee_id=int(assignee_id),
                node_key=str(node.get('id') or ''),
                status='PENDING',
                comment=None,
                sort=base_sort + 1,
                completed_time=None,
            )
            db.add(task)
            await db.flush()
            created_tasks.append(task)
            continue

        if node_type == 'CC':
            data = node.get('data') or {}
            cc_user_ids = data.get('ccUserIds') or []
            if isinstance(cc_user_ids, list):
                for cc_user_id in cc_user_ids:
                    if not str(cc_user_id).isdigit():
                        continue
                    message = WorkflowMessage(
                        receiver_id=int(cc_user_id),
                        instance_id=instance.id,
                        task_id=instance.current_task_id,
                        message_type='CC_NOTIFY',
                        title='您收到新的流程抄送',
                        content=f'流程《{instance.title}》抄送给您',
                        is_read=False,
                    )
                    db.add(message)
                    await db.flush()
                    await workflow_message_service.push_message(db=db, message=message)
            queue.extend(edge_map.get(node_id, []))
            continue

        if node_type == 'TRIGGER':
            queue.extend(edge_map.get(node_id, []))
            continue

        if node_type == 'CONDITION':
            queue.extend(_resolve_condition_targets(node, edge_map, form_data))
            continue

        if node_type == 'PARALLEL':
            queue.extend(edge_map.get(node_id, []))
            continue

        if node_type == 'END':
            reached_end = True

    return created_tasks, reached_end


class WorkflowInstanceService:
    @staticmethod
    async def start(*, db, obj: StartWorkflowInstanceParam, user_id: int) -> dict:
        definition = await workflow_definition_dao.get(db, obj.definition_id)
        if not definition:
            raise errors.NotFoundError(msg='流程定义不存在')
        if definition.status == 2:
            raise errors.RequestError(msg='流程定义已停用，无法发起申请')

        runtime_form_data = obj.form_data if isinstance(obj.form_data, dict) else {}
        runtime_form_data['__self_select_assignees__'] = obj.self_select_assignees if isinstance(obj.self_select_assignees, dict) else {}
        initiator_dept_id = await _get_user_dept_id(db, user_id)

        instance = WorkflowInstance(
            instance_no=instance_no_generator.generate(),
            definition_id=definition.id,
            title=obj.title,
            initiator_id=user_id,
            status='RUNNING',
            current_task_id=None,
            form_data=json.dumps(dict(runtime_form_data), ensure_ascii=False),
            remark=obj.remark,
        )
        db.add(instance)
        await db.flush()

        node_map, edge_map, reverse_edge_map = _parse_flow_runtime(definition.flow_config)
        if not node_map:
            raise errors.RequestError(msg='流程配置无效')

        start_node_ids: list[str] = []
        for node_id, node in node_map.items():
            if node.get('type') == 'START':
                start_node_ids.extend(edge_map.get(node_id, []))

        created_tasks, reached_end = await _expand_runtime_from_nodes(
            db=db,
            instance=instance,
            definition=definition,
            node_map=node_map,
            edge_map=edge_map,
            reverse_edge_map=reverse_edge_map,
            start_node_ids=start_node_ids,
            initiator_dept_id=initiator_dept_id,
            form_data=runtime_form_data,
            base_sort=0,
        )
        if not created_tasks and not reached_end:
            raise errors.RequestError(msg='流程未配置首个审批人')

        for task in created_tasks:
            await _push_pending_task_message(db=db, instance=instance, task=task)
        pending_tasks = await _sync_instance_runtime_state(db, instance.id, reached_end=reached_end)
        instance = await workflow_instance_dao.get(db, instance.id) or instance
        todo_count = await _todo_count(db, int(pending_tasks[0].assignee_id)) if pending_tasks else None
        return _serialize_single_instance(instance, todo_count=todo_count)

    @staticmethod
    async def get_my_apply(*, db, user_id: int):
        return _serialize_page_items(
            await paging_data(db, await workflow_instance_dao.get_select_by_initiator(user_id)),
        )

    @staticmethod
    async def get_my_todo(*, db, user_id: int):
        todo_count = await _todo_count(db, user_id)
        return _serialize_page_items(
            await paging_data(db, await workflow_instance_dao.get_select_todo(user_id)),
            todo_count=todo_count,
        )

    @staticmethod
    async def get_todo_count(*, db, user_id: int) -> int:
        return await _todo_count(db, user_id)


    @staticmethod
    async def get_detail(*, db, pk: int, user_id: int):
        instance = await workflow_instance_dao.get(db, pk)
        if not instance:
            raise errors.NotFoundError(msg='流程实例不存在')
        if instance.initiator_id != user_id and not await _has_user_pending_task_for_instance(db, instance.id, user_id):
            raise errors.ForbiddenError(msg='无权查看该流程实例')

        definition = await workflow_definition_dao.get(db, instance.definition_id)
        todo_count = await _todo_count(db, user_id)
        message_stmt = await workflow_message_dao.get_select_by_instance(instance.id)
        messages = list((await db.execute(message_stmt)).scalars().all())
        return _build_instance_detail_payload(
            instance,
            todo_count=todo_count,
            messages=messages,
            definition=definition,
        )

    @staticmethod
    async def withdraw(*, db, pk: int, user_id: int):
        instance = await workflow_instance_dao.get(db, pk)
        if not instance:
            raise errors.NotFoundError(msg='流程实例不存在')
        if instance.initiator_id != user_id:
            raise errors.ForbiddenError(msg='仅发起人可撤回该流程')
        if instance.status != 'RUNNING':
            raise errors.RequestError(msg='当前流程状态不允许撤回')

        definition = await workflow_definition_dao.get(db, instance.definition_id)
        if not definition or not definition.allow_withdraw:
            raise errors.RequestError(msg='当前流程未开启撤回')

        pending_tasks = await _get_pending_tasks_for_instance(db, instance.id)
        completed_time = timezone.now().isoformat()
        for task in pending_tasks:
            await workflow_task_dao.update_model(
                db,
                task.id,
                {'status': 'CANCELLED', 'comment': '发起人撤回', 'completed_time': completed_time},
            )

        await workflow_instance_dao.update_model(
            db,
            instance.id,
            {'status': 'WITHDRAWN', 'current_task_id': None},
        )

        if pending_tasks:
            await _notify_task_assignees(
                db=db,
                instance=instance,
                tasks=pending_tasks,
                message_type='WITHDRAWN',
                title='流程已撤回',
                content=f'流程《{instance.title}》已被发起人撤回',
            )

        latest_instance = await workflow_instance_dao.get(db, instance.id) or instance
        message_stmt = await workflow_message_dao.get_select_by_instance(latest_instance.id)
        messages = list((await db.execute(message_stmt)).scalars().all())
        return _build_instance_detail_payload(
            latest_instance,
            todo_count=await _todo_count(db, user_id),
            messages=messages,
            definition=definition,
        )

    @staticmethod
    async def urge(*, db, pk: int, user_id: int) -> None:
        instance = await workflow_instance_dao.get(db, pk)
        if not instance:
            raise errors.NotFoundError(msg='流程实例不存在')
        if instance.initiator_id != user_id:
            raise errors.ForbiddenError(msg='仅发起人可催办该流程')
        if instance.status != 'RUNNING':
            raise errors.RequestError(msg='当前流程状态不允许催办')

        definition = await workflow_definition_dao.get(db, instance.definition_id)
        if not definition or not definition.allow_urge:
            raise errors.RequestError(msg='当前流程未开启催办')

        pending_tasks = await _get_pending_tasks_for_instance(db, instance.id)
        if not pending_tasks:
            raise errors.RequestError(msg='当前没有可催办的待办任务')

        await _notify_task_assignees(
            db=db,
            instance=instance,
            tasks=pending_tasks,
            message_type='URGE_NOTIFY',
            title='流程催办提醒',
            content=f'流程《{instance.title}》请尽快处理',
        )


async def advance_workflow_runtime(*, db, instance: WorkflowInstance, definition, from_task: WorkflowTask):
    node_map, edge_map, reverse_edge_map = _parse_flow_runtime(definition.flow_config)
    if not node_map or not from_task.node_key:
        await _sync_instance_runtime_state(db, instance.id, reached_end=True)
        return None

    runtime_form_data = _parse_json_text(instance.form_data)
    initiator_dept_id = await _get_user_dept_id(db, instance.initiator_id)
    created_tasks, reached_end = await _expand_runtime_from_nodes(
        db=db,
        instance=instance,
        definition=definition,
        node_map=node_map,
        edge_map=edge_map,
        reverse_edge_map=reverse_edge_map,
        start_node_ids=edge_map.get(from_task.node_key, []),
        initiator_dept_id=initiator_dept_id,
        form_data=runtime_form_data,
        base_sort=from_task.sort or 0,
    )
    for task in created_tasks:
        await _push_pending_task_message(db=db, instance=instance, task=task)
    await _sync_instance_runtime_state(db, instance.id, reached_end=reached_end)
    return created_tasks[0] if created_tasks else None


workflow_instance_service = WorkflowInstanceService()
