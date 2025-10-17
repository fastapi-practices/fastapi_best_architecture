from backend.common.socketio.server import sio


async def task_notification(msg: str) -> None:
    """
    任务通知

    :param msg: 通知信息
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})
