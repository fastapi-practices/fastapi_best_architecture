import time

from asyncio import Queue
from typing import Any

from asgiref.sync import sync_to_async
from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.context import ctx
from backend.common.enums import OperaLogCipherType, StatusType
from backend.common.log import log
from backend.common.queue import batch_dequeue
from backend.common.response.response_code import StandardResponseCode
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.utils.encrypt import AESCipher, ItsDCipher, Md5Cipher
from backend.utils.trace_id import get_request_trace_id


class OperaLogMiddleware(BaseHTTPMiddleware):
    """操作日志中间件"""

    opera_log_queue: Queue = Queue(maxsize=100000)

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """
        处理请求并记录操作日志

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        response = None
        path = request.url.path

        if path in settings.OPERA_LOG_PATH_EXCLUDE or not path.startswith(f'{settings.FASTAPI_API_V1_PATH}'):
            response = await call_next(request)
        else:
            method = request.method
            args = await self.get_request_args(request)

            # 执行请求
            code = 200
            msg = 'Success'
            status = StatusType.enable
            error = None
            try:
                response = await call_next(request)
                elapsed = (time.perf_counter() - ctx.perf_time) * 1000
                for e in [
                    '__request_http_exception__',
                    '__request_validation_exception__',
                    '__request_assertion_error__',
                    '__request_custom_exception__',
                ]:
                    exception = ctx.get(e)
                    if exception:
                        code = exception.get('code')
                        msg = exception.get('msg')
                        log.error(f'请求异常: {msg}')
                        break
            except Exception as e:
                elapsed = (time.perf_counter() - ctx.perf_time) * 1000
                code = getattr(e, 'code', StandardResponseCode.HTTP_500)  # 兼容 SQLAlchemy 异常用法
                msg = getattr(e, 'msg', str(e))  # 不建议使用 traceback 模块获取错误信息，会暴漏代码信息
                status = StatusType.disable
                error = e
                log.error(f'请求异常: {e!s}')

            # 此信息只能在请求后获取
            route = request.scope.get('route')
            summary = route.summary or '' if route else ''

            try:
                # 此信息来源于 JWT 认证中间件
                username = request.user.username
            except AttributeError:
                username = None

            # 日志记录
            log.debug(f'接口摘要：[{summary}]')
            log.debug(f'请求地址：[{ctx.ip}]')
            log.debug(f'请求参数：{args}')

            # 日志创建
            opera_log_in = CreateOperaLogParam(
                trace_id=get_request_trace_id(),
                username=username,
                method=method,
                title=summary,
                path=path,
                ip=ctx.ip,
                country=ctx.country,
                region=ctx.region,
                city=ctx.city,
                user_agent=ctx.user_agent,
                os=ctx.os,
                browser=ctx.browser,
                device=ctx.device,
                args=args,
                status=status,
                code=str(code),
                msg=msg,
                cost_time=elapsed,  # 可能和日志存在微小差异（可忽略）
                opera_time=ctx.start_time,
            )
            await self.opera_log_queue.put(opera_log_in)

            # 错误抛出
            if error:
                raise error from None

        return response

    async def get_request_args(self, request: Request) -> dict[str, Any] | None:
        """
        获取请求参数

        :param request: FastAPI 请求对象
        :return:
        """
        args = {}

        # 查询参数
        query_params = dict(request.query_params)
        if query_params:
            args['query_params'] = await self.desensitization(query_params)

        # 路径参数
        path_params = request.path_params
        if path_params:
            args['path_params'] = await self.desensitization(path_params)

        # Tip: .body() 必须在 .form() 之前获取
        # https://github.com/encode/starlette/discussions/1933
        content_type = request.headers.get('Content-Type', '').split(';')

        # 请求体
        body_data = await request.body()
        if body_data:
            # 注意：非 json 数据默认使用 data 作为键
            if 'application/json' not in content_type:
                args['data'] = str(body_data)
            else:
                json_data = await request.json()
                if isinstance(json_data, dict):
                    args['json'] = await self.desensitization(json_data)
                else:
                    args['data'] = str(body_data)

        # 表单参数
        form_data = await request.form()
        if len(form_data) > 0:
            for k, v in form_data.items():
                form_data = {k: v.filename} if isinstance(v, UploadFile) else {k: v}
            if 'multipart/form-data' not in content_type:
                args['x-www-form-urlencoded'] = await self.desensitization(form_data)
            else:
                args['form-data'] = await self.desensitization(form_data)

        return args or None

    @staticmethod
    @sync_to_async
    def desensitization(args: dict[str, Any]) -> dict[str, Any]:
        """
        脱敏处理

        :param args: 需要脱敏的参数字典
        :return:
        """
        for key, value in args.items():
            if key in settings.OPERA_LOG_ENCRYPT_KEY_INCLUDE:
                match settings.OPERA_LOG_ENCRYPT_TYPE:
                    case OperaLogCipherType.aes:
                        args[key] = (AESCipher(settings.OPERA_LOG_ENCRYPT_SECRET_KEY).encrypt(value)).hex()
                    case OperaLogCipherType.md5:
                        args[key] = Md5Cipher.encrypt(value)
                    case OperaLogCipherType.itsdangerous:
                        args[key] = ItsDCipher(settings.OPERA_LOG_ENCRYPT_SECRET_KEY).encrypt(value)
                    case OperaLogCipherType.plan:
                        pass
                    case _:
                        args[key] = '******'

        return args

    @classmethod
    async def consumer(cls) -> None:
        """操作日志消费者"""
        while True:
            logs = await batch_dequeue(
                cls.opera_log_queue,
                max_items=settings.OPERA_LOG_QUEUE_BATCH_CONSUME_SIZE,
                timeout=settings.OPERA_LOG_QUEUE_TIMEOUT,
            )
            if logs:
                try:
                    if settings.DATABASE_ECHO:
                        log.info('自动执行【操作日志批量创建】任务...')
                    async with async_db_session.begin() as db:
                        await opera_log_service.bulk_create(db=db, objs=logs)
                finally:
                    if not cls.opera_log_queue.empty():
                        cls.opera_log_queue.task_done()
