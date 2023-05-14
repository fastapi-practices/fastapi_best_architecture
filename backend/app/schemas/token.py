#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel

from backend.app.schemas.user import GetUserInfoNoRelation


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelation
