#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.routing import APIRoute


def simplify_operation_ids(app: FastAPI) -> None:
    """
    SIMPLIFY THE OPERATION ID SO THAT THE GENERATED CLIENT HAS A SIMPLER API FUNCTION NAME

    :param app: FastAPI application instance
    :return:
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
