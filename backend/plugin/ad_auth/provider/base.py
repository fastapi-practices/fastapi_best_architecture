from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalIdentity:
    """Normalized identity returned by an external auth provider."""

    email: str
    external_id: str
    display_name: str | None
    department: str | None
    auth_provider: str


class AuthProviderError(Exception):
    """Base authentication provider error."""


class InvalidCredentialsError(AuthProviderError):
    """Credentials are invalid."""


class ProviderUnavailableError(AuthProviderError):
    """External identity provider is unavailable."""
