import pytest


def test_user_model_has_auth_provider_column():
    """sys_user table should include auth_provider column."""
    from backend.app.admin.model.user import User

    assert hasattr(User, 'auth_provider')
    assert hasattr(User, 'external_id')


def test_sys_user_role_has_source_column():
    """sys_user_role table should include source column."""
    from backend.app.admin.model.m2m import user_role

    assert 'source' in [c.name for c in user_role.columns]
