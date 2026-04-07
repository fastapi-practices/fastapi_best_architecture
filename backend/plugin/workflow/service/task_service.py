from backend.common.exception import errors
from backend.plugin.workflow.crud.crud_definition import workflow_definition_dao
from backend.plugin.workflow.crud.crud_instance import workflow_instance_dao
from backend.plugin.workflow.crud.crud_task import workflow_task_dao
from backend.plugin.workflow.model import WorkflowMessage
from backend.plugin.workflow.schema.task import ApproveWorkflowTaskParam, RejectWorkflowTaskParam
from backend.plugin.workflow.service.instance_service import advance_workflow_runtime
from backend.plugin.workflow.service.message_service import workflow_message_service
from backend.utils.timezone import timezone


class WorkflowTaskService:
    @staticmethod
    async def approve(*, db, pk: int, user_id: int, obj: ApproveWorkflowTaskParam):
        task = await workflow_task_dao.get(db, pk)
        if not task:
            raise errors.NotFoundError(msg='任务不存在')
        if task.assignee_id != user_id:
            raise errors.ForbiddenError(msg='无权审批该任务')
        if task.status != 'PENDING':
            raise errors.RequestError(msg='任务已处理')

        await workflow_task_dao.update_model(
            db,
            pk,
            {'status': 'APPROVED', 'comment': obj.comment, 'completed_time': timezone.now().isoformat()},
        )
        task = await workflow_task_dao.get(db, pk)
        instance = await workflow_instance_dao.get(db, task.instance_id)
        if instance:
            definition = await workflow_definition_dao.get(db, task.definition_id)
            next_task = None
            if definition:
                next_task = await advance_workflow_runtime(db=db, instance=instance, definition=definition, from_task=task)
                instance = await workflow_instance_dao.get(db, task.instance_id) or instance
            if next_task is None and instance.status == 'APPROVED':
                message = WorkflowMessage(
                    receiver_id=instance.initiator_id,
                    instance_id=instance.id,
                    task_id=task.id,
                    message_type='APPROVED',
                    title='您的审批已通过',
                    content=f'流程《{instance.title}》已审批通过',
                    is_read=False,
                )
                db.add(message)
                await db.flush()
                await workflow_message_service.push_message(db=db, message=message)
        return await workflow_task_dao.get(db, pk)

    @staticmethod
    async def reject(*, db, pk: int, user_id: int, obj: RejectWorkflowTaskParam):
        task = await workflow_task_dao.get(db, pk)
        if not task:
            raise errors.NotFoundError(msg='任务不存在')
        if task.assignee_id != user_id:
            raise errors.ForbiddenError(msg='无权审批该任务')
        if task.status != 'PENDING':
            raise errors.RequestError(msg='任务已处理')

        await workflow_task_dao.update_model(
            db,
            pk,
            {'status': 'REJECTED', 'comment': obj.comment, 'completed_time': timezone.now().isoformat()},
        )
        instance = await workflow_instance_dao.get(db, task.instance_id)
        if instance:
            await workflow_instance_dao.update_model(db, instance.id, {'status': 'REJECTED', 'current_task_id': None})
            message = WorkflowMessage(
                receiver_id=instance.initiator_id,
                instance_id=instance.id,
                task_id=task.id,
                message_type='REJECTED',
                title='您的审批被拒绝',
                content=f'流程《{instance.title}》被拒绝',
                is_read=False,
            )
            db.add(message)
            await db.flush()
            await workflow_message_service.push_message(db=db, message=message)
        return await workflow_task_dao.get(db, pk)

    @staticmethod
    async def get(*, db, pk: int, user_id: int):
        task = await workflow_task_dao.get(db, pk)
        if not task:
            raise errors.NotFoundError(msg='任务不存在')
        if task.assignee_id != user_id:
            raise errors.ForbiddenError(msg='无权查看该任务')
        return task


workflow_task_service = WorkflowTaskService()
