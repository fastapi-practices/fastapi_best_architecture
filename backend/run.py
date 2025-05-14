#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn

if __name__ == '__main__':
    # Why this independent startup file：https://stackoverflow.com/questions/64003384
    # IF YOU LIKE TO DO DEBUG IN IDE, YOU CAN START THIS FILE DIRECTLY RIGHT IN IDE
    # if you like debugging by print, use fastapi cli to start the service
    try:
        config = uvicorn.Config(app='backend.main:app', reload=True)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
