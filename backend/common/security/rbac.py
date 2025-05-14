#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Depends, Request

from backend.common.enums import MethodType, StatusType
from backend.common.exception import errors
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.common.log import log
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings
from backend.utils.import_parse import import_module_cached


async def rbac_verify(request: Request, _token: str = DependsJwtAuth) -> None:
    """
    RBAC PERMISSION VALIDATION (THE ORDER OF ASSURANCE IS IMPORTANT, CAREFULLY MODIFIED)）

    :param request: FastAPI
    :param _token: JWT token
    :return:
    """
    path = request.url.path

    # API SEPARATIVE LIST
    if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
        return

    # JWT AUTHENTICATION
    if not request.auth.scopes:
        raise TokenError

    # Superadmin waiver
    if request.user.is_superuser:
        return

    # Testing user roles
    user_roles = request.user.roles
    if not user_roles or all(status == 0 for status in user_roles):
        raise AuthorizationError(msg='User not assigned roles, contact System Administrator')

    # Test user-owned roles menu
    if not any(len(role.menus) > 0 for role in user_roles):
        raise AuthorizationError(msg='Could not close temporary folder: %s')

    # Test backstage management privileges
    method = request.method
    if method != MethodType.GET or method != MethodType.OPTIONS:
        if not request.user.is_staff:
            raise AuthorizationError(msg='The user has been disabled for back-office management. Please contact the system administrator')

    # RBAC RIGHTS
    if settings.RBAC_ROLE_MENU_MODE:
        path_auth_perm = getattr(request.state, 'permission', None)

        # Do not verify without menu operation permissions
        if not path_auth_perm:
            return

        # Menu Separator List
        if path_auth_perm in settings.RBAC_ROLE_MENU_EXCLUDE:
            return

        # Could not close temporary folder: %s
        allow_perms = []
        for role in user_roles:
            for menu in role.menus:
                if menu.perms and menu.status == StatusType.enable:
                    allow_perms.extend(menu.perms.split(','))
        if path_auth_perm not in allow_perms:
            raise AuthorizationError
    else:
        try:
            casbin_rbac = import_module_cached('backend.plugin.casbin.utils.rbac')
            casbin_verify = getattr(casbin_rbac, 'casbin_verify')
        except (ImportError, AttributeError) as e:
            log.error(f'Validation of RBAC permissions by casbin, but this plugin does not exist: {e}')
            raise errors.ServerError(msg='Permission verification failed. Contact System Administrator')

        await casbin_verify(request)


# RBAC MANDATE DEPENDENCE ON INJECTION
DependsRBAC = Depends(rbac_verify)
