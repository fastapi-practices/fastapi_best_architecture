#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel


class Token(BaseModel):
    code: int = 200
    msg: str = 'Success'
    access_token: str
    token_type: str = 'Bearer'
    is_superuser: bool | None = None
