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


def test_dept_role_mapping_model_has_expected_columns():
    """sys_dept_role_mapping table should have all designed columns."""
    from backend.plugin.ad_auth.model.dept_role_mapping import DeptRoleMapping

    assert hasattr(DeptRoleMapping, 'dept_pattern')
    assert hasattr(DeptRoleMapping, 'role_name')
    assert hasattr(DeptRoleMapping, 'priority')
    assert hasattr(DeptRoleMapping, 'is_active')
    assert DeptRoleMapping.__tablename__ == 'sys_dept_role_mapping'
