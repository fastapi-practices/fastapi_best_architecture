INSERT INTO sys_dept_role_mapping (dept_pattern, role_name, priority, is_active) VALUES (N'.*(IT|信息|系统管理).*', N'admin', 10, 1);
INSERT INTO sys_dept_role_mapping (dept_pattern, role_name, priority, is_active) VALUES (N'.*(采购|供应链|Purchasing).*', N'purchaser', 20, 1);
INSERT INTO sys_dept_role_mapping (dept_pattern, role_name, priority, is_active) VALUES (N'.*', N'user', 1000, 1);
