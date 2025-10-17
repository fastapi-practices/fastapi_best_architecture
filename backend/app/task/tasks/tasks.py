from time import sleep

from anyio import sleep as asleep

from backend.app.task.celery import celery_app


@celery_app.task(name='task_demo')
def task_demo() -> str:
    """示例任务，模拟耗时操作"""
    sleep(30)
    return 'test async'


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    """异步示例任务，模拟耗时操作"""
    await asleep(30)
    return 'test async'


@celery_app.task(name='task_demo_params')
async def task_demo_params(hello: str, world: str | None = None) -> str:
    """参数示例任务，模拟传参操作"""
    await asleep(1)
    return hello + world
