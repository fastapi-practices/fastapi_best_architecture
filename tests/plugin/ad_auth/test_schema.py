import pytest
from pydantic import ValidationError


def test_login_request_validates_required_fields():
    """LoginRequest should require both username and password."""
    from backend.plugin.ad_auth.schema.auth import LoginRequest

    with pytest.raises(ValidationError):
        LoginRequest(username="testuser")

    req = LoginRequest(username="testuser", password="secret")
    assert req.username == "testuser"
    assert req.password == "secret"


def test_login_response_default_token_type():
    """LoginResponse token_type should default to 'bearer'."""
    from backend.plugin.ad_auth.schema.auth import LoginResponse, UserInfo

    user = UserInfo(
        id=1, uuid="abc", username="testuser", nickname="Test", email="test@avc.com"
    )
    resp = LoginResponse(
        access_token="token123",
        access_token_expire_time="2025-01-01T00:00:00",
        session_uuid="sess-1",
        user=user,
    )
    assert resp.token_type == "bearer"
    assert resp.access_token == "token123"
    assert resp.user.email == "test@avc.com"
