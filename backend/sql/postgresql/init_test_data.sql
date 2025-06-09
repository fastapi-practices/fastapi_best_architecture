insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values  (1, '测试', 0, null, null, null, 1, 0, null, '2025-05-26 17:13:45', null);

insert into fba.sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values  (1, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:26:18', null),
        (2, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:30:01', null),
        (3, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:31:41', null),
        (4, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:32:34', null),
        (5, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:33:29', null),
        (6, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:35:41', null),
        (7, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 1, '2025-06-09 17:54:29', null),
        (8, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 1, '2025-06-09 17:57:09', null),
        (9, '文档', 'Document', null, 1, 'lucide:book-open-text', 4, null, null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 6, '2025-06-09 17:59:44', null),
        (10, 'Github', 'Github', null, 2, 'ant-design:github-filled', 4, null, null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 6, '2025-06-09 18:00:50', null),
        (11, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, null, null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 6, '2025-06-09 18:01:39', null),
        (12, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:03:17', null),
        (13, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:03:54', null),
        (14, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:04:47', null),
        (15, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:05:31', null),
        (16, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2, '2025-06-09 18:07:04', null),
        (17, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 16, '2025-06-09 18:07:46', null),
        (18, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 16, '2025-06-09 18:08:22', null),
        (19, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:09:12', null),
        (20, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:10:20', null),
        (21, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:11:10', null),
        (22, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2, '2025-06-09 18:11:38', null),
        (23, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 3, '2025-06-09 18:12:38', null),
        (24, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 3, '2025-06-09 18:13:19', null),
        (25, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 4, '2025-06-09 18:14:35', null),
        (26, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 4, '2025-06-09 18:15:26', null),
        (27, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 5, '2025-06-09 18:17:12', null),
        (28, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 5, '2025-06-09 18:17:42', null),
        (29, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 5, '2025-06-09 18:18:12', null),
        (30, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 12, '2025-06-09 18:21:17', null),
        (31, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 12, '2025-06-09 18:22:01', null),
        (32, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 12, '2025-06-09 18:22:39', null),
        (33, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 13, '2025-06-09 18:24:09', null),
        (34, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 14, '2025-06-09 18:25:08', null),
        (35, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 14, '2025-06-09 18:26:30', null),
        (36, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 14, '2025-06-09 18:27:24', null),
        (37, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 14, '2025-06-09 18:28:25', null),
        (38, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 14, '2025-06-09 18:28:55', null),
        (39, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 15, '2025-06-09 18:29:51', null),
        (40, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 15, '2025-06-09 18:30:13', null),
        (41, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 15, '2025-06-09 18:30:37', null),
        (42, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 17, '2025-06-09 18:31:11', null),
        (43, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 17, '2025-06-09 18:31:42', null),
        (44, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 17, '2025-06-09 18:32:36', null),
        (45, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 17, '2025-06-09 18:33:09', null),
        (46, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 18, '2025-06-09 18:35:54', null),
        (47, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 18, '2025-06-09 18:36:19', null),
        (48, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 18, '2025-06-09 18:36:44', null),
        (49, '安装zip插件', 'InstallZipSysPlugin', null, 0, null, 2, null, 'sys:plugin:zip', 1, 0, 1, '', null, 19, '2025-06-09 18:38:14', null),
        (50, '安装git插件', 'InstallGitSysPlugin', null, 0, null, 2, null, 'sys:plugin:git', 1, 0, 1, '', null, 19, '2025-06-09 18:38:43', null),
        (51, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:del', 1, 0, 1, '', null, 19, '2025-06-09 18:39:08', null),
        (52, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:status', 1, 0, 1, '', null, 19, '2025-06-09 18:39:47', null),
        (53, '新增网站参数', 'AddWebsiteSysConfig', null, 0, null, 2, null, 'sys:config:website:add', 1, 0, 1, '', null, 20, '2025-06-09 18:43:30', null),
        (54, '新增用户协议', 'AddProtocolSysConfig', null, 0, null, 2, null, 'sys:config:protocol:add', 1, 0, 1, '', null, 20, '2025-06-09 18:44:13', null),
        (55, '新增用户政策', 'AddPolicySysConfig', null, 0, null, 2, null, 'sys:config:policy:add', 1, 0, 1, '', null, 20, '2025-06-09 18:45:28', null),
        (56, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 20, '2025-06-09 18:45:52', null),
        (57, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 20, '2025-06-09 18:46:13', null),
        (58, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 20, '2025-06-09 18:46:36', null),
        (59, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'sys:dict:type:add', 1, 0, 1, '', null, 21, '2025-06-09 18:48:17', null),
        (60, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'sys:dict:type:edit', 1, 0, 1, '', null, 21, '2025-06-09 18:48:49', null),
        (61, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'sys:dict:type:del', 1, 0, 1, '', null, 21, '2025-06-09 18:49:23', null),
        (62, '新增', 'AddSysDictData', null, 0, null, 2, null, 'sys:dict:data:add', 1, 0, 1, '', null, 21, '2025-06-09 18:50:01', null),
        (63, '修改', 'EditSysDictData', null, 0, null, 2, null, 'sys:dict:data:edit', 1, 0, 1, '', null, 21, '2025-06-09 18:50:26', null),
        (64, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'sys:dict:data:del', 1, 0, 1, '', null, 21, '2025-06-09 18:50:48', null),
        (65, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 22, '2025-06-09 18:51:22', null),
        (66, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 22, '2025-06-09 18:51:45', null),
        (67, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 22, '2025-06-09 18:52:10', null),
        (68, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'gen:code:business:add', 1, 0, 1, '', null, 23, '2025-06-09 18:53:07', null),
        (69, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'gen:code:business:edit', 1, 0, 1, '', null, 23, '2025-06-09 18:53:45', null),
        (70, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'gen:code:business:del', 1, 0, 1, '', null, 23, '2025-06-09 18:54:11', null),
        (71, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'gen:code:model:add', 1, 0, 1, '', null, 23, '2025-06-09 18:54:45', null),
        (72, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'gen:code:model:edit', 1, 0, 1, '', null, 23, '2025-06-09 18:55:08', null),
        (73, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'gen:code:model:del', 1, 0, 1, '', null, 23, '2025-06-09 18:55:35', null),
        (74, '导入', 'ImportGenCode', null, 0, null, 2, null, 'gen:code:import', 1, 0, 1, '', null, 23, '2025-06-09 18:58:16', null),
        (75, '写入', 'WriteGenCode', null, 0, null, 2, null, 'gen:code:write', 1, 0, 1, '', null, 23, '2025-06-09 19:01:22', null),
        (76, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 25, '2025-06-09 19:02:21', null),
        (77, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:empty', 1, 0, 1, '', null, 25, '2025-06-09 19:02:50', null),
        (78, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 26, '2025-06-09 19:03:13', null),
        (79, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:empty', 1, 0, 1, '', null, 26, '2025-06-09 19:03:40', null),
        (80, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:token:kick', 1, 0, 1, '', null, 27, '2025-06-09 19:04:52', null);

insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values  (1, '测试', 1, 1, null, '2025-05-26 17:13:45', null);

insert into sys_role_menu (id, role_id, menu_id)
values  (1, 1, 1),
        (2, 1, 2),
        (3, 1, 3),
        (4, 1, 4);

insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values  (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', '0x24326224313224387932654E7563583139566A6D5A33745968424C634F', 'admin@example.com', 1, 1, 1, 1, null, null, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 1, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

insert into sys_user_role (id, user_id, role_id)
values  (1, 1, 1);

insert into sys_data_scope (id, name, status, created_time, updated_time)
values  (1, '测试部门数据权限', 1, '2025-06-09 16:53:29', null),
        (2, '测试部门及以下数据权限', 1, '2025-06-09 16:53:40', null);

insert into sys_data_rule (id, name, model, `column`, operator, expression, `value`, created_time, updated_time)
values  (1, '部门名称等于测试', '部门', 'name', 1, 0, '测试', '2025-06-09 16:56:06', null),
        (2, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', '2025-06-09 17:16:14', null);

insert into sys_data_scope_rule (id, data_scope_id, data_rule_id)
values  (1, 1, 1),
        (2, 2, 1),
        (3, 2, 2);

-- Reset auto-increment values for each table based on max id
SELECT setval(pg_get_serial_sequence('sys_dept', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_dept;
SELECT setval(pg_get_serial_sequence('sys_menu', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_menu;
SELECT setval(pg_get_serial_sequence('sys_role', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_role;
SELECT setval(pg_get_serial_sequence('sys_role_menu', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_role_menu;
SELECT setval(pg_get_serial_sequence('sys_user', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_user;
SELECT setval(pg_get_serial_sequence('sys_user_role', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_user_role;
SELECT setval(pg_get_serial_sequence('sys_data_scope', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_data_scope;
SELECT setval(pg_get_serial_sequence('sys_data_rule', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_data_rule;
SELECT setval(pg_get_serial_sequence('sys_data_scope_rule', 'id'),COALESCE(MAX(id), 0) + 1, true) FROM sys_data_scope_rule;
