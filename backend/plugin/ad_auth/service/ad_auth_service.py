from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import User, user_role
from backend.app.admin.model.role import Role
from backend.common.exception import errors
from backend.common.security.jwt import create_access_token, create_refresh_token
from backend.core.conf import settings
from backend.plugin.ad_auth.provider.base import (
    ExternalIdentity,
    InvalidCredentialsError,
    ProviderUnavailableError,
)
from backend.plugin.ad_auth.provider.ldap_provider import LdapAuthProvider
from backend.plugin.ad_auth.schema.auth import LoginResponse, UserInfo
from backend.plugin.ad_auth.service.dept_role_mapping import (
    DeptRoleMappingService,
    dept_role_mapping_service,
)
from backend.utils.timezone import timezone


class AdAuthService:
    """Coordinate AD authentication, user sync, role mapping, and JWT issuance."""

    def __init__(
        self,
        provider: LdapAuthProvider | None = None,
        role_mapping_svc: DeptRoleMappingService = dept_role_mapping_service,
    ):
        self.provider = provider or LdapAuthProvider()
        self.role_mapping_svc = role_mapping_svc

    async def login(self, db: AsyncSession, username: str, password: str) -> LoginResponse:
        """Authenticate an AD user and return a LoginResponse."""
        try:
            identity = self.provider.authenticate(username, password)
        except InvalidCredentialsError as e:
            raise errors.AuthorizationError(msg=str(e)) from e
        except ProviderUnavailableError as e:
            raise errors.ServerError(msg=str(e)) from e

        user = await self._sync_user(db, identity)
        role_name = await self.role_mapping_svc.resolve_role(db, identity.department)
        await self._sync_department_roles(db, user, role_name)

        access_token_data = await create_access_token(
            user.id,
            multi_login=user.is_multi_login,
            username=user.username,
            nickname=user.nickname,
            last_login_time=timezone.to_str(user.last_login_time),
        )
        refresh_token_data = await create_refresh_token(
            access_token_data.session_uuid,
            user.id,
            multi_login=user.is_multi_login,
        )

        user_info = UserInfo.model_validate(user)

        return LoginResponse(
            access_token=access_token_data.access_token,
            access_token_expire_time=access_token_data.access_token_expire_time,
            session_uuid=access_token_data.session_uuid,
            user=user_info,
        )

    async def _sync_user(self, db: AsyncSession, identity: ExternalIdentity) -> User:
        """Find or create a local user for the AD identity."""
        user = await user_dao.check_email(db, identity.email)
        now = timezone.now()

        if user is None:
            base_username = identity.email.split("@")[0] if "@" in identity.email else identity.email
            username = base_username
            counter = 1
            while await user_dao.get_by_username(db, username):
                username = f"{base_username}{counter}"
                counter += 1

            user = User(
                username=username,
                nickname=identity.display_name or username,
                email=identity.email,
                password=None,
                salt=None,
                auth_provider=identity.auth_provider,
                external_id=identity.external_id,
                is_staff=True,
            )
            db.add(user)
            await db.flush()
            await db.refresh(user)
        else:
            user.nickname = identity.display_name or user.nickname
            user.external_id = identity.external_id
            user.auth_provider = identity.auth_provider
            user.last_login_time = now

        return user

    async def _sync_department_roles(self, db: AsyncSession, user: User, role_name: str) -> None:
        """Replace department-mapped roles for the user."""
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if role is None:
            result = await db.execute(
                select(Role).where(Role.name == getattr(settings, "AD_AUTH_DEFAULT_ROLE", "user"))
            )
            role = result.scalar_one_or_none()
        if role is None:
            return

        await db.execute(
            delete(user_role).where(
                user_role.c.user_id == user.id,
                user_role.c.source == "department_mapping",
            )
        )

        await db.execute(
            insert(user_role).values(
                user_id=user.id,
                role_id=role.id,
                source="department_mapping",
            )
        )


ad_auth_service = AdAuthService()
