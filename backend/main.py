#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import uvicorn

from backend.core.registrar import register_app

app = register_app()


if __name__ == '__main__':
    # 如果你喜欢在 IDE 中进行 DEBUG，main 启动方法会很有帮助
    # 如果你喜欢通过日志方式进行调试，建议使用 fastapi cli 方式启动服务
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', reload=True)
    except Exception as e:
        raise e
