#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.responses import RedirectResponse

from app.common.response.response_code import StandardResponseCode


class GithubService:
    @staticmethod
    def add_with_login(user: dict):
        email = user['email']
        if email:
            return RedirectResponse(url='/', status_code=StandardResponseCode.HTTP_302)
        # TODO


github_service: GithubService = GithubService()
