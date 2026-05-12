from typing import Any

from ldap3 import ALL, Connection, Server

from backend.plugin.ad_auth.provider.base import (
    ExternalIdentity,
    InvalidCredentialsError,
    ProviderUnavailableError,
)


def get_plugin_settings() -> dict[str, Any]:
    """Get plugin settings from FBA Settings."""
    from backend.core.conf import settings

    return {
        "AD_AUTH_LDAP_URL": getattr(settings, "AD_AUTH_LDAP_URL", "ldap://localhost:389"),
        "AD_AUTH_BIND_DN": getattr(settings, "AD_AUTH_BIND_DN", ""),
        "AD_AUTH_BIND_PASSWORD": getattr(settings, "AD_AUTH_BIND_PASSWORD", ""),
        "AD_AUTH_BASE_DN": getattr(settings, "AD_AUTH_BASE_DN", ""),
        "AD_AUTH_USER_SEARCH_FILTER": getattr(settings, "AD_AUTH_USER_SEARCH_FILTER", "(mail={username})"),
        "AD_AUTH_EMAIL_ATTR": getattr(settings, "AD_AUTH_EMAIL_ATTR", "mail"),
        "AD_AUTH_DISPLAY_NAME_ATTR": getattr(settings, "AD_AUTH_DISPLAY_NAME_ATTR", "cn"),
        "AD_AUTH_DEPARTMENT_ATTR": getattr(settings, "AD_AUTH_DEPARTMENT_ATTR", "department"),
        "AD_AUTH_EXTERNAL_ID_ATTR": getattr(settings, "AD_AUTH_EXTERNAL_ID_ATTR", "objectSid"),
    }


class LdapAuthProvider:
    """Authenticate users against LDAP."""

    auth_provider = "ad"

    def authenticate(self, username: str, password: str) -> ExternalIdentity:
        """Authenticate with service-account search followed by user bind."""
        s = get_plugin_settings()
        try:
            server = Server(s["AD_AUTH_LDAP_URL"], get_info=ALL)
            service_conn = Connection(
                server,
                user=s["AD_AUTH_BIND_DN"],
                password=s["AD_AUTH_BIND_PASSWORD"],
                auto_bind=True,
            )
            search_filter = s["AD_AUTH_USER_SEARCH_FILTER"].format(username=username)
            service_conn.search(
                search_base=s["AD_AUTH_BASE_DN"],
                search_filter=search_filter,
                attributes=[
                    s["AD_AUTH_EMAIL_ATTR"],
                    s["AD_AUTH_DISPLAY_NAME_ATTR"],
                    s["AD_AUTH_DEPARTMENT_ATTR"],
                    s["AD_AUTH_EXTERNAL_ID_ATTR"],
                ],
            )
            if not service_conn.entries:
                raise InvalidCredentialsError("AD 域：用户名或密码错误")

            entry = service_conn.entries[0]
            user_dn = entry.entry_dn
            user_conn = Connection(server, user=user_dn, password=password)
            if not user_conn.bind():
                raise InvalidCredentialsError("AD 域：用户名或密码错误")

            return ExternalIdentity(
                email=str(entry[s["AD_AUTH_EMAIL_ATTR"]].value),
                display_name=_optional_attr(entry, s["AD_AUTH_DISPLAY_NAME_ATTR"]),
                department=_optional_attr(entry, s["AD_AUTH_DEPARTMENT_ATTR"]),
                external_id=str(entry[s["AD_AUTH_EXTERNAL_ID_ATTR"]].value),
                auth_provider=self.auth_provider,
            )
        except InvalidCredentialsError:
            raise
        except Exception as e:
            raise ProviderUnavailableError(f"AD 域服务不可用: {e}")


def _optional_attr(entry, attr_name: str) -> str | None:
    """Read an optional LDAP attribute value."""
    try:
        value = entry[attr_name].value
    except Exception:
        return None
    return str(value) if value is not None else None
