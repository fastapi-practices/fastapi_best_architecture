SET IDENTITY_INSERT sys_dept ON;
INSERT INTO sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
VALUES (1, '测试', 0, NULL, NULL, NULL, 1, 0, NULL, GETDATE(), NULL);
SET IDENTITY_INSERT sys_dept OFF;

SET IDENTITY_INSERT sys_menu ON;
INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(1, 'page.dashboard.title', 'Dashboard', '/dashboard', 0, 'ant-design:dashboard-outlined', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(2, 'page.dashboard.analytics', 'Analytics', '/analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', NULL, 1, 1, 1, '', NULL, 1, '2025-06-26 20:29:06', NULL),
(3, 'page.dashboard.workspace', 'Workspace', '/workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', NULL, 1, 1, 1, '', NULL, 1, '2025-06-26 20:29:06', NULL),
(4, 'page.menu.system', 'System', '/system', 1, 'eos-icons:admin', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(5, 'page.menu.sysDept', 'SysDept', '/system/dept', 1, 'mingcute:department-line', 1, '/system/dept/index', NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(6, '新增', 'AddSysDept', NULL, 0, NULL, 2, NULL, 'sys:dept:add', 1, 0, 1, '', NULL, 5, '2025-06-26 20:29:06', NULL),
(7, '修改', 'EditSysDept', NULL, 0, NULL, 2, NULL, 'sys:dept:edit', 1, 0, 1, '', NULL, 5, '2025-06-26 20:29:06', NULL),
(8, '删除', 'DeleteSysDept', NULL, 0, NULL, 2, NULL, 'sys:dept:del', 1, 0, 1, '', NULL, 5, '2025-06-26 20:29:06', NULL),
(9, 'page.menu.sysUser', 'SysUser', '/system/user', 2, 'ant-design:user-outlined', 1, '/system/user/index', NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(10, '删除', 'DeleteSysUser', NULL, 0, NULL, 2, NULL, 'sys:user:del', 1, 0, 1, '', NULL, 9, '2025-06-26 20:29:06', NULL),
(11, 'page.menu.sysRole', 'SysRole', '/system/role', 3, 'carbon:user-role', 1, '/system/role/index', NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(12, '新增', 'AddSysRole', NULL, 0, NULL, 2, NULL, 'sys:role:add', 1, 0, 1, '', NULL, 11, '2025-06-26 20:29:06', NULL),
(13, '修改', 'EditSysRole', NULL, 0, NULL, 2, NULL, 'sys:role:edit', 1, 0, 1, '', NULL, 11, '2025-06-26 20:29:06', NULL),
(14, '修改角色菜单', 'EditSysRoleMenu', NULL, 0, NULL, 2, NULL, 'sys:role:menu:edit', 1, 0, 1, '', NULL, 11, '2025-06-26 20:29:06', NULL),
(15, '修改角色数据范围', 'EditSysRoleScope', NULL, 0, NULL, 2, NULL, 'sys:role:scope:edit', 1, 0, 1, '', NULL, 11, '2025-06-26 20:29:06', NULL),
(16, '删除', 'DeleteSysRole', NULL, 0, NULL, 2, NULL, 'sys:role:del', 1, 0, 1, '', NULL, 11, '2025-06-26 20:29:06', NULL),
(17, 'page.menu.sysMenu', 'SysMenu', '/system/menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(18, '新增', 'AddSysMenu', NULL, 0, NULL, 2, NULL, 'sys:menu:add', 1, 0, 1, '', NULL, 17, '2025-06-26 20:29:06', NULL),
(19, '修改', 'EditSysMenu', NULL, 0, NULL, 2, NULL, 'sys:menu:edit', 1, 0, 1, '', NULL, 17, '2025-06-26 20:29:06', NULL),
(20, '删除', 'DeleteSysMenu', NULL, 0, NULL, 2, NULL, 'sys:menu:del', 1, 0, 1, '', NULL, 17, '2025-06-26 20:29:06', NULL),
(21, 'page.menu.sysDataPermission', 'SysDataPermission', '/system/data-permission', 5, 'icon-park-outline:permissions', 0, NULL, NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(22, 'page.menu.sysDataScope', 'SysDataScope', '/system/data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', NULL, 1, 1, 1, '', NULL, 21, '2025-06-26 20:29:06', '2025-06-26 20:37:26'),
(23, '新增', 'AddSysDataScope', NULL, 0, NULL, 2, NULL, 'data:scope:add', 1, 0, 1, '', NULL, 22, '2025-06-26 20:29:06', NULL),
(24, '修改', 'EditSysDataScope', NULL, 0, NULL, 2, NULL, 'data:scope:edit', 1, 0, 1, '', NULL, 22, '2025-06-26 20:29:06', NULL),
(25, '修改数据范围规则', 'EditDataScopeRule', NULL, 0, NULL, 2, NULL, 'data:scope:rule:edit', 1, 0, 1, '', NULL, 22, '2025-06-26 20:29:06', NULL),
(26, '删除', 'DeleteSysDataScope', NULL, 0, NULL, 2, NULL, 'data:scope:del', 1, 0, 1, '', NULL, 22, '2025-06-26 20:29:06', NULL),
(27, 'page.menu.sysDataRule', 'SysDataRule', '/system/data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', NULL, 1, 1, 1, '', NULL, 21, '2025-06-26 20:29:06', '2025-06-26 20:37:40'),
(28, '新增', 'AddSysDataRule', NULL, 0, NULL, 2, NULL, 'data:rule:add', 1, 0, 1, '', NULL, 27, '2025-06-26 20:29:06', NULL),
(29, '修改', 'EditSysDataRule', NULL, 0, NULL, 2, NULL, 'data:rule:edit', 1, 0, 1, '', NULL, 27, '2025-06-26 20:29:06', NULL),
(30, '删除', 'DeleteSysDataRule', NULL, 0, NULL, 2, NULL, 'data:rule:del', 1, 0, 1, '', NULL, 27, '2025-06-26 20:29:06', NULL),
(31, 'page.menu.sysPlugin', 'SysPlugin', '/system/plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', NULL, 1, 1, 1, '', NULL, 4, '2025-06-26 20:29:06', NULL),
(32, 'page.menu.scheduler', 'Scheduler', '/scheduler', 2, 'material-symbols:automation', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(33, 'page.menu.schedulerManage', 'SchedulerManage', '/scheduler/manage', 1, 'ix:scheduler', 1, '/scheduler/manage/index', NULL, 1, 1, 1, '', NULL, 32, '2025-06-26 20:29:06', NULL),
(34, 'page.menu.schedulerRecord', 'SchedulerRecord', '/scheduler/record', 2, 'ix:scheduler', 1, '/scheduler/record/index', NULL, 1, 1, 1, '', NULL, 32, '2025-06-26 20:29:06', NULL),
(35, 'page.menu.log', 'Log', '/log', 3, 'carbon:cloud-logging', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(36, 'page.menu.login', 'LoginLog', '/log/login', 1, 'mdi:login', 1, '/log/login/index', NULL, 1, 1, 1, '', NULL, 35, '2025-06-26 20:29:06', NULL),
(37, '删除', 'DeleteLoginLog', NULL, 0, NULL, 2, NULL, 'log:login:del', 1, 0, 1, '', NULL, 36, '2025-06-26 20:29:06', NULL),
(38, '清空', 'EmptyLoginLog', NULL, 0, NULL, 2, NULL, 'log:login:clear', 1, 0, 1, '', NULL, 36, '2025-06-26 20:29:06', NULL),
(39, 'page.menu.opera', 'OperaLog', '/log/opera', 2, 'carbon:operations-record', 1, '/log/opera/index', NULL, 1, 1, 1, '', NULL, 35, '2025-06-26 20:29:06', NULL),
(40, '删除', 'DeleteOperaLog', NULL, 0, NULL, 2, NULL, 'log:opera:del', 1, 0, 1, '', NULL, 39, '2025-06-26 20:29:06', NULL),
(41, '清空', 'EmptyOperaLog', NULL, 0, NULL, 2, NULL, 'log:opera:clear', 1, 0, 1, '', NULL, 39, '2025-06-26 20:29:06', NULL),
(42, 'page.menu.monitor', 'Monitor', '/monitor', 4, 'mdi:monitor-eye', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(43, 'page.menu.online', 'Online', '/log/online', 1, 'wpf:online', 1, '/monitor/online/index', NULL, 1, 1, 1, '', NULL, 42, '2025-06-26 20:29:06', NULL),
(44, 'page.menu.redis', 'Redis', '/monitor/redis', 2, 'devicon:redis', 1, '/monitor/redis/index', NULL, 1, 1, 1, '', NULL, 42, '2025-06-26 20:29:06', NULL),
(45, 'page.menu.server', 'Server', '/monitor/server', 3, 'mdi:server-outline', 1, '/monitor/server/index', NULL, 1, 1, 1, '', NULL, 42, '2025-06-26 20:29:06', NULL),
(46, '项目', 'Project', '/fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, NULL, NULL, 1, 1, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL),
(47, '文档', 'Document', '/fba/document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', NULL, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', NULL, 46, '2025-06-26 20:29:06', NULL),
(48, 'Github', 'Github', '/fba/github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', NULL, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi-best-architecture', NULL, 46, '2025-06-26 20:29:06', NULL),
(49, 'Apifox', 'Apifox', '/fba/apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', NULL, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', NULL, 46, '2025-06-26 20:29:06', NULL),
(50, 'page.menu.profile', 'Profile', '/profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', NULL, 1, 0, 1, '', NULL, NULL, '2025-06-26 20:29:06', NULL);
SET IDENTITY_INSERT sys_menu OFF;

SET IDENTITY_INSERT sys_role ON;
INSERT INTO sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
VALUES (1, '测试', 1, 1, NULL, GETDATE(), NULL);
SET IDENTITY_INSERT sys_role OFF;

SET IDENTITY_INSERT sys_role_menu ON;
INSERT INTO sys_role_menu (id, role_id, menu_id)
VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 50);
SET IDENTITY_INSERT sys_role_menu OFF;

SET IDENTITY_INSERT sys_user ON;
INSERT INTO sys_user (id, uuid, username, nickname, password, salt, email, status, is_superuser, is_staff, is_multi_login, avatar, phone, join_time, last_login_time, last_password_changed_time, dept_id, created_time, updated_time)
VALUES
(1, CONVERT(varchar(36), NEWID()), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', 0x24326224313224387932654E7563583139566A6D5A33745968424C634F, 'admin@example.com', 1, 1, 1, 1, NULL, NULL, GETDATE(), GETDATE(), GETDATE(), 1, GETDATE(), NULL),
(2, CONVERT(varchar(36), NEWID()), 'test', '用户66666', '$2b$12$BMiXsNQAgTx7aNc7kVgnwedXGyUxPEHRnJMFbiikbqHgVoT3y14Za', 0x24326224313224424D6958734E514167547837614E63376B56676E7765, 'test@example.com', 1, 0, 0, 0, NULL, NULL, GETDATE(), GETDATE(), GETDATE(), 1, GETDATE(), NULL);
SET IDENTITY_INSERT sys_user OFF;

SET IDENTITY_INSERT sys_user_role ON;
INSERT INTO sys_user_role (id, user_id, role_id)
VALUES
(1, 1, 1),
(2, 2, 1);
SET IDENTITY_INSERT sys_user_role OFF;

SET IDENTITY_INSERT sys_data_scope ON;
INSERT INTO sys_data_scope (id, name, status, created_time, updated_time)
VALUES
(1, '本部门数据权限', 1, GETDATE(), NULL),
(2, '部门及以下数据权限', 1, GETDATE(), NULL),
(3, '仅本人数据权限', 1, GETDATE(), NULL),
(4, '全模型本部门数据权限', 1, GETDATE(), NULL),
(5, '排除超级管理员数据权限', 1, GETDATE(), NULL);
SET IDENTITY_INSERT sys_data_scope OFF;

SET IDENTITY_INSERT sys_data_rule ON;
INSERT INTO sys_data_rule (id, name, model, [column], operator, expression, [value], created_time, updated_time)
VALUES
(1, '部门 ID 等于当前用户部门', 'Dept', '__dept_id__', 0, 0, '${dept_id}', GETDATE(), NULL),
(2, '部门名称等于测试', 'Dept', 'name', 1, 0, '测试', GETDATE(), NULL),
(3, '父部门 ID 等于测试部门 ID', 'Dept', 'parent_id', 0, 0, '1', GETDATE(), NULL),
(4, '创建者等于当前用户', '__ALL__', '__created_by__', 0, 0, '${user_id}', GETDATE(), NULL),
(5, '全模型部门 ID 等于当前用户部门', '__ALL__', '__dept_id__', 0, 0, '${dept_id}', GETDATE(), NULL),
(6, '用户非超级管理员', 'User', 'is_superuser', 0, 1, '1', GETDATE(), NULL);
SET IDENTITY_INSERT sys_data_rule OFF;

SET IDENTITY_INSERT sys_role_data_scope ON;
INSERT INTO sys_role_data_scope (id, role_id, data_scope_id)
VALUES
(1, 1, 1),
(2, 1, 2);
SET IDENTITY_INSERT sys_role_data_scope OFF;

SET IDENTITY_INSERT sys_data_scope_rule ON;
INSERT INTO sys_data_scope_rule (id, data_scope_id, data_rule_id)
VALUES
(1, 1, 1),
(2, 2, 2),
(3, 2, 3),
(4, 3, 4),
(5, 4, 5),
(6, 5, 6);
SET IDENTITY_INSERT sys_data_scope_rule OFF;

DBCC CHECKIDENT ('sys_dept', RESEED, 1);
DBCC CHECKIDENT ('sys_menu', RESEED, 50);
DBCC CHECKIDENT ('sys_role', RESEED, 1);
DBCC CHECKIDENT ('sys_role_menu', RESEED, 4);
DBCC CHECKIDENT ('sys_user', RESEED, 2);
DBCC CHECKIDENT ('sys_user_role', RESEED, 2);
DBCC CHECKIDENT ('sys_data_scope', RESEED, 5);
DBCC CHECKIDENT ('sys_data_rule', RESEED, 6);
DBCC CHECKIDENT ('sys_role_data_scope', RESEED, 2);
DBCC CHECKIDENT ('sys_data_scope_rule', RESEED, 6);
