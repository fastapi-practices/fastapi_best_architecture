from backend.common.socketio.server import sio


async def task_notification(msg: str) -> None:
    """
    任务通知

    :param msg: 通知信息
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})


async def workflow_message_notification(user_id: int, data: dict) -> None:
    """审批流消息通知"""
    await sio.emit('workflow_message', data, room=f'user:{user_id}', namespace='/ws')
