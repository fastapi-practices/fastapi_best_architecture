#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    code: int = 200
    msg: str = 'Success'
    access_token: str
    token_type: str = 'Bearer'
    is_superuser: Optional[bool] = None
