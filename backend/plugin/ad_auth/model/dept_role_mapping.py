from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalStr, id_key


class DeptRoleMapping(Base):
    """部门角色映射表"""

    __tablename__ = 'sys_dept_role_mapping'

    id: Mapped[id_key] = mapped_column(init=False)
    dept_pattern: Mapped[str] = mapped_column(UniversalStr(256), comment='部门名正则表达式')
    role_name: Mapped[str] = mapped_column(UniversalStr(64), comment='对应角色名称')
    priority: Mapped[int] = mapped_column(default=100, comment='优先级(数字越小优先级越高)')
    is_active: Mapped[bool] = mapped_column(default=True, comment='是否启用')
