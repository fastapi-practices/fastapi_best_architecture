import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock


class TestDeptRoleMappingService:
    """Test department-to-role regex mapping."""

    def test_resolve_admin_by_it_department(self):
        """IT department should match admin role."""
        from backend.plugin.ad_auth.service.dept_role_mapping import DeptRoleMappingService

        svc = DeptRoleMappingService()

        mapping1 = MagicMock()
        mapping1.dept_pattern = r".*(IT|信息|系统管理).*"
        mapping1.role_name = "admin"
        mapping1.priority = 10
        mapping1.is_active = True

        mapping2 = MagicMock()
        mapping2.dept_pattern = r".*"
        mapping2.role_name = "user"
        mapping2.priority = 1000
        mapping2.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mapping1, mapping2]
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(return_value=mock_result)

        async def run():
            return await svc.resolve_role(mock_db, "信息部")

        result = asyncio.run(run())
        assert result == "admin"

    def test_resolve_fallback_when_no_match(self):
        """Unknown department should fall back to default role."""
        from backend.plugin.ad_auth.service.dept_role_mapping import DeptRoleMappingService

        svc = DeptRoleMappingService()

        mapping = MagicMock()
        mapping.dept_pattern = r".*(IT|信息).*"
        mapping.role_name = "admin"
        mapping.priority = 10
        mapping.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mapping]
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(return_value=mock_result)

        async def run():
            return await svc.resolve_role(mock_db, "生产部")

        result = asyncio.run(run())
        assert result == "user"

    def test_invalid_regex_skipped(self):
        """Invalid regex pattern should be skipped."""
        from backend.plugin.ad_auth.service.dept_role_mapping import DeptRoleMappingService

        svc = DeptRoleMappingService()

        bad_mapping = MagicMock()
        bad_mapping.dept_pattern = r"[invalid"
        bad_mapping.role_name = "admin"
        bad_mapping.priority = 10
        bad_mapping.is_active = True

        fallback = MagicMock()
        fallback.dept_pattern = r".*"
        fallback.role_name = "user"
        fallback.priority = 1000
        fallback.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [bad_mapping, fallback]
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(return_value=mock_result)

        async def run():
            return await svc.resolve_role(mock_db, "IT")

        result = asyncio.run(run())
        assert result == "user"
