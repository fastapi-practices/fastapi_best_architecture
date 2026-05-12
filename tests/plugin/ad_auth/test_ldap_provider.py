import pytest
from unittest.mock import MagicMock, patch

from backend.plugin.ad_auth.provider.base import (
    AuthProviderError,
    ExternalIdentity,
    InvalidCredentialsError,
    ProviderUnavailableError,
)


class TestLdapAuthProvider:
    """Test LdapAuthProvider authentication flow."""

    def test_authenticate_success_returns_identity(self):
        """Successful authentication should return ExternalIdentity."""
        from backend.plugin.ad_auth.provider.ldap_provider import LdapAuthProvider

        mock_server = MagicMock()
        mock_service_conn = MagicMock()
        mock_service_conn.entries = [MagicMock()]
        mock_service_conn.entries[0].entry_dn = "cn=test,ou=users,dc=avc,dc=local"

        def side_effect(k):
            if k == "mail":
                return MagicMock(value="test@avc.com")
            if k == "cn":
                return MagicMock(value="Test User")
            if k == "department":
                return MagicMock(value="IT")
            return MagicMock(value="12345")

        mock_service_conn.entries[0].__getitem__.side_effect = side_effect
        mock_user_conn = MagicMock()
        mock_user_conn.bind.return_value = True

        with patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Server", return_value=mock_server
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Connection",
            side_effect=[mock_service_conn, mock_user_conn],
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.get_plugin_settings",
            return_value={
                "AD_AUTH_LDAP_URL": "ldap://localhost:389",
                "AD_AUTH_BIND_DN": "cn=admin,dc=avc,dc=local",
                "AD_AUTH_BIND_PASSWORD": "adminpass",
                "AD_AUTH_BASE_DN": "dc=avc,dc=local",
                "AD_AUTH_USER_SEARCH_FILTER": "(mail={username})",
                "AD_AUTH_EMAIL_ATTR": "mail",
                "AD_AUTH_DISPLAY_NAME_ATTR": "cn",
                "AD_AUTH_DEPARTMENT_ATTR": "department",
                "AD_AUTH_EXTERNAL_ID_ATTR": "objectSid",
            },
        ):
            provider = LdapAuthProvider()
            identity = provider.authenticate("test@avc.com", "password")

            assert identity.email == "test@avc.com"
            assert identity.auth_provider == "ad"

    def test_authenticate_user_not_found_raises_invalid_credentials(self):
        """Unknown user should raise InvalidCredentialsError."""
        from backend.plugin.ad_auth.provider.ldap_provider import LdapAuthProvider

        mock_server = MagicMock()
        mock_service_conn = MagicMock()
        mock_service_conn.entries = []

        with patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Server", return_value=mock_server
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Connection",
            return_value=mock_service_conn,
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.get_plugin_settings",
            return_value={
                "AD_AUTH_LDAP_URL": "ldap://localhost:389",
                "AD_AUTH_BIND_DN": "cn=admin,dc=avc,dc=local",
                "AD_AUTH_BIND_PASSWORD": "adminpass",
                "AD_AUTH_BASE_DN": "dc=avc,dc=local",
                "AD_AUTH_USER_SEARCH_FILTER": "(mail={username})",
                "AD_AUTH_EMAIL_ATTR": "mail",
                "AD_AUTH_DISPLAY_NAME_ATTR": "cn",
                "AD_AUTH_DEPARTMENT_ATTR": "department",
                "AD_AUTH_EXTERNAL_ID_ATTR": "objectSid",
            },
        ):
            provider = LdapAuthProvider()
            with pytest.raises(InvalidCredentialsError, match="用户名或密码错误"):
                provider.authenticate("unknown@avc.com", "password")

    def test_authenticate_wrong_password_raises_invalid_credentials(self):
        """Wrong password should raise InvalidCredentialsError."""
        from backend.plugin.ad_auth.provider.ldap_provider import LdapAuthProvider

        mock_server = MagicMock()
        mock_service_conn = MagicMock()
        mock_service_conn.entries = [MagicMock()]
        mock_service_conn.entries[0].entry_dn = "cn=test,ou=users,dc=avc,dc=local"
        mock_user_conn = MagicMock()
        mock_user_conn.bind.return_value = False

        with patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Server", return_value=mock_server
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Connection",
            side_effect=[mock_service_conn, mock_user_conn],
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.get_plugin_settings",
            return_value={
                "AD_AUTH_LDAP_URL": "ldap://localhost:389",
                "AD_AUTH_BIND_DN": "cn=admin,dc=avc,dc=local",
                "AD_AUTH_BIND_PASSWORD": "adminpass",
                "AD_AUTH_BASE_DN": "dc=avc,dc=local",
                "AD_AUTH_USER_SEARCH_FILTER": "(mail={username})",
                "AD_AUTH_EMAIL_ATTR": "mail",
                "AD_AUTH_DISPLAY_NAME_ATTR": "cn",
                "AD_AUTH_DEPARTMENT_ATTR": "department",
                "AD_AUTH_EXTERNAL_ID_ATTR": "objectSid",
            },
        ):
            provider = LdapAuthProvider()
            with pytest.raises(InvalidCredentialsError, match="用户名或密码错误"):
                provider.authenticate("test@avc.com", "wrongpass")

    def test_authenticate_provider_unavailable_raises_error(self):
        """Server down should raise ProviderUnavailableError."""
        from backend.plugin.ad_auth.provider.ldap_provider import LdapAuthProvider

        with patch(
            "backend.plugin.ad_auth.provider.ldap_provider.Server",
            side_effect=Exception("Connection refused"),
        ), patch(
            "backend.plugin.ad_auth.provider.ldap_provider.get_plugin_settings",
            return_value={
                "AD_AUTH_LDAP_URL": "ldap://localhost:389",
                "AD_AUTH_BIND_DN": "cn=admin,dc=avc,dc=local",
                "AD_AUTH_BIND_PASSWORD": "adminpass",
                "AD_AUTH_BASE_DN": "dc=avc,dc=local",
                "AD_AUTH_USER_SEARCH_FILTER": "(mail={username})",
                "AD_AUTH_EMAIL_ATTR": "mail",
                "AD_AUTH_DISPLAY_NAME_ATTR": "cn",
                "AD_AUTH_DEPARTMENT_ATTR": "department",
                "AD_AUTH_EXTERNAL_ID_ATTR": "objectSid",
            },
        ):
            provider = LdapAuthProvider()
            with pytest.raises(ProviderUnavailableError, match="AD 域服务不可用"):
                provider.authenticate("test@avc.com", "password")


class TestBaseProvider:
    """Test provider base classes."""

    def test_external_identity_is_frozen_dataclass(self):
        """ExternalIdentity should be a frozen dataclass."""
        identity = ExternalIdentity(
            email="test@avc.com",
            external_id="12345",
            display_name="Test User",
            department="IT",
            auth_provider="ldap",
        )
        assert identity.email == "test@avc.com"
        with pytest.raises(Exception):
            identity.email = "other@avc.com"

    def test_error_hierarchy(self):
        """AuthProviderError hierarchy should be correct."""
        assert issubclass(InvalidCredentialsError, AuthProviderError)
        assert issubclass(ProviderUnavailableError, AuthProviderError)
