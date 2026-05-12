import logging
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.plugin.ad_auth.model.dept_role_mapping import DeptRoleMapping

logger = logging.getLogger(__name__)


class DeptRoleMappingService:
    """Resolve a system role from a department name using regex patterns."""

    async def resolve_role(self, db: AsyncSession, department: str | None) -> str:
        """Return the first active role mapping that matches the department."""
        normalized_department = department or ""

        result = await db.execute(
            select(DeptRoleMapping)
            .where(DeptRoleMapping.is_active.is_(True))
            .order_by(DeptRoleMapping.priority.asc())
        )
        mappings = result.scalars().all()

        for mapping in mappings:
            try:
                if re.search(mapping.dept_pattern, normalized_department, re.IGNORECASE):
                    return mapping.role_name
            except re.error:
                logger.warning(
                    "Invalid department role mapping regex ignored: %s", mapping.dept_pattern
                )

        from backend.core.conf import settings

        return getattr(settings, "AD_AUTH_DEFAULT_ROLE", "user")


dept_role_mapping_service = DeptRoleMappingService()
