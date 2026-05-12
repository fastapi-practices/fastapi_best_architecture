import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from backend.plugin.ad_auth.provider.base import ExternalIdentity


class TestAdAuthService:
    """Test AD auth service orchestration."""

    def test_new_user_created_with_role(self):
        """New AD user should be created and assigned department-mapped role."""
        from backend.plugin.ad_auth.service.ad_auth_service import AdAuthService

        identity = ExternalIdentity(
            email="test@avc.com",
            external_id="S-1-5-21-12345",
            display_name="Test User",
            department="信息部",
            auth_provider="ad",
        )

        mock_provider = MagicMock()
        mock_provider.authenticate.return_value = identity
        mock_role_svc = MagicMock()
        mock_role_svc.resolve_role = AsyncMock(return_value="admin")

        mock_db = AsyncMock()
        mock_db.add = MagicMock()  # sync in SQLAlchemy

        def _refresh_side_effect(user):
            user.id = 1
            user.uuid = "uuid-1"

        mock_db.refresh = AsyncMock(side_effect=_refresh_side_effect)

        with patch(
            "backend.plugin.ad_auth.service.ad_auth_service.user_dao"
        ) as mock_dao, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.create_access_token"
        ) as mock_jwt, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.create_refresh_token"
        ) as mock_refresh, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.timezone"
        ) as mock_tz:
            mock_dao.check_email = AsyncMock(return_value=None)
            mock_dao.get_by_username = AsyncMock(return_value=None)

            mock_role = MagicMock()
            mock_role.name = "admin"
            mock_role.id = 3
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none = MagicMock(return_value=mock_role)
            mock_db.execute = AsyncMock(return_value=mock_role_result)

            mock_access = MagicMock()
            mock_access.access_token = "access-token"
            mock_access.access_token_expire_time = datetime(2025, 1, 1)
            mock_access.session_uuid = "sess-1"
            mock_jwt.return_value = mock_access

            mock_refresh_data = MagicMock()
            mock_refresh_data.refresh_token = "refresh-token"
            mock_refresh_data.refresh_token_expire_time = datetime(2025, 1, 8)
            mock_refresh.return_value = mock_refresh_data

            mock_tz.now.return_value = datetime(2025, 1, 1)
            mock_tz.to_str.return_value = "2025-01-01T00:00:00"

            async def run_login():
                svc = AdAuthService(provider=mock_provider, role_mapping_svc=mock_role_svc)
                return await svc.login(mock_db, "test@avc.com", "password")

            result = asyncio.run(run_login())
            assert result.access_token == "access-token"
            assert result.user.email == "test@avc.com"

    def test_existing_user_updated_on_login(self):
        """Existing AD user should have profile updated on subsequent login."""
        from backend.plugin.ad_auth.service.ad_auth_service import AdAuthService

        identity = ExternalIdentity(
            email="test@avc.com",
            external_id="S-1-5-21-12345",
            display_name="Test User",
            department="信息部",
            auth_provider="ad",
        )

        mock_provider = MagicMock()
        mock_provider.authenticate.return_value = identity
        mock_role_svc = MagicMock()
        mock_role_svc.resolve_role = AsyncMock(return_value="admin")

        existing_user = MagicMock()
        existing_user.id = 42
        existing_user.uuid = "uuid-42"
        existing_user.username = "testuser"
        existing_user.nickname = "Old Name"
        existing_user.email = "test@avc.com"
        existing_user.auth_provider = "ad"
        existing_user.external_id = "S-1-5-21-old"
        existing_user.is_multi_login = False
        existing_user.last_login_time = datetime(2024, 1, 1)
        existing_user.roles = []

        mock_db = AsyncMock()

        with patch(
            "backend.plugin.ad_auth.service.ad_auth_service.user_dao"
        ) as mock_dao, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.create_access_token"
        ) as mock_jwt, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.create_refresh_token"
        ) as mock_refresh, patch(
            "backend.plugin.ad_auth.service.ad_auth_service.timezone"
        ) as mock_tz:
            mock_dao.check_email = AsyncMock(return_value=existing_user)

            mock_role = MagicMock()
            mock_role.name = "admin"
            mock_role.id = 3
            mock_role_result = MagicMock()
            mock_role_result.scalar_one_or_none = MagicMock(return_value=mock_role)
            mock_db.execute = AsyncMock(return_value=mock_role_result)

            mock_access = MagicMock()
            mock_access.access_token = "access-token-2"
            mock_access.access_token_expire_time = datetime(2025, 1, 2)
            mock_access.session_uuid = "sess-2"
            mock_jwt.return_value = mock_access

            mock_refresh_data = MagicMock()
            mock_refresh_data.refresh_token = "refresh-token-2"
            mock_refresh_data.refresh_token_expire_time = datetime(2025, 1, 9)
            mock_refresh.return_value = mock_refresh_data

            mock_tz.now.return_value = datetime(2025, 1, 2)
            mock_tz.to_str.return_value = "2025-01-02T00:00:00"

            async def run_login():
                svc = AdAuthService(provider=mock_provider, role_mapping_svc=mock_role_svc)
                return await svc.login(mock_db, "test@avc.com", "password")

            result = asyncio.run(run_login())
            assert existing_user.nickname == "Test User"
            assert result.access_token == "access-token-2"
