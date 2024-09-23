INSERT INTO fba.sys_dept (id, name, level, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
VALUES (1, 'test', 0, 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_menu (id, title, name, level, sort, icon, path, menu_type, component, perms, status, `show`, cache, remark, parent_id, created_time, updated_time)
VALUES  (1, '测试', 'test', 0, 0, '', null, 0, null, null, 0, 0, 1, null, null, '2023-07-27 19:14:10', null),
        (2, '仪表盘', 'dashboard', 0, 0, 'IconDashboard', 'dashboard', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:15:45', null),
        (3, '工作台', 'Workplace', 0, 0, null, 'workplace', 1, '/dashboard/workplace/index.vue', null, 1, 1, 1, null, 2, '2023-07-27 19:17:59', null),
        (4, '日志', 'log', 0, 66, 'IconBug', 'log', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:19:59', null),
        (5, '登录日志', 'Login', 0, 0, null, 'login', 1, '/log/login/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:20:56', null),
        (6, '操作日志', 'Opera', 0, 0, null, 'opera', 1, '/log/opera/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:21:28', null),
        (7, '系统管理', 'admin', 0, 6, 'IconSettings', 'admin', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:23:00', null),
        (8, '部门管理', 'SysDept', 0, 0, null, 'sys-dept', 1, '/admin/dept/index.vue', null, 1, 1, 1, null, 7, '2023-07-27 19:23:42', null),
        (9, '新增', '', 0, 0, null, null, 2, null, 'sys:dept:add', 1, 1, 1, null, 8, '2024-01-07 11:37:00', null),
        (10, '编辑', '', 0, 0, null, null, 2, null, 'sys:dept:edit', 1, 1, 1, null, 8, '2024-01-07 11:37:29', null),
        (11, '删除', '', 0, 0, null, null, 2, null, 'sys:dept:del', 1, 1, 1, null, 8, '2024-01-07 11:37:44', null),
        (12, 'API管理', 'SysApi', 0, 1, null, 'sys-api', 1, '/admin/api/index.vue', null, 1, 1, 1, null, 7, '2023-07-27 19:24:12', null),
        (13, '新增', '', 0, 0, null, null, 2, null, 'sys:api:add', 1, 1, 1, null, 12, '2024-01-07 11:57:09', null),
        (14, '编辑', '', 0, 0, null, null, 2, null, 'sys:api:edit', 1, 1, 1, null, 12, '2024-01-07 11:57:44', null),
        (15, '删除', '', 0, 0, null, null, 2, null, 'sys:api:del', 1, 1, 1, null, 12, '2024-01-07 11:57:56', null),
        (16, '用户管理', 'SysUser', 0, 0, null, 'sys-user', 1, '/admin/user/index.vue', null, 1, 1, 1, null, 7, '2023-07-27 19:25:13', null),
        (17, '编辑用户角色', '', 0, 0, null, null, 2, null, 'sys:user:role:edit', 1, 1, 1, null, 16, '2024-01-07 12:04:20', null),
        (18, '注销', '', 0, 0, null, null, 2, null, 'sys:user:del', 1, 1, 1, '用户注销 != 用户登出，注销之后用户将从数据库删除', 16, '2024-01-07 02:28:09', null),
        (19, '角色管理', 'SysRole', 0, 2, null, 'sys-role', 1, '/admin/role/index.vue', null, 1, 1, 1, null, 7, '2023-07-27 19:25:45', null),
        (20, '新增', '', 0, 0, null, null, 2, null, 'sys:role:add', 1, 1, 1, null, 19, '2024-01-07 11:58:37', null),
        (21, '编辑', '', 0, 0, null, null, 2, null, 'sys:role:edit', 1, 1, 1, null, 19, '2024-01-07 11:58:52', null),
        (22, '删除', '', 0, 0, null, null, 2, null, 'sys:role:del', 1, 1, 1, null, 19, '2024-01-07 11:59:07', null),
        (23, '编辑角色菜单', '', 0, 0, null, null, 2, null, 'sys:role:menu:edit', 1, 1, 1, null, 19, '2024-01-07 01:59:39', null),
        (24, '菜单管理', 'SysMenu', 0, 2, null, 'sys-menu', 1, '/admin/menu/index.vue', null, 1, 1, 1, null, 7, '2023-07-27 19:45:29', null),
        (25, '新增', '', 0, 0, null, null, 2, null, 'sys:menu:add', 1, 1, 1, null, 24, '2024-01-07 12:01:24', null),
        (26, '编辑', '', 0, 0, null, null, 2, null, 'sys:menu:edit', 1, 1, 1, null, 24, '2024-01-07 12:01:34', null),
        (27, '删除', '', 0, 0, null, null, 2, null, 'sys:menu:del', 1, 1, 1, null, 24, '2024-01-07 12:01:48', null),
        (28, '系统监控', 'monitor', 0, 88, 'IconComputer', 'monitor', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:27:08', null),
        (29, 'Redis监控', 'Redis', 0, 0, null, 'redis', 1, '/monitor/redis/index.vue', 'sys:monitor:redis', 1, 1, 1, null, 28, '2023-07-27 19:28:03', null),
        (30, '服务器监控', 'Server', 0, 0, null, 'server', 1, '/monitor/server/index.vue', 'sys:monitor:server', 1, 1, 1, null, 28, '2023-07-27 19:28:29', null),
        (31, '系统自动化', 'automation', 0, 777, 'IconCodeSquare', 'automation', 0, null, null, 1, 1, 1, null, null, '2024-07-27 02:06:20', '2024-07-27 02:18:52'),
        (32, '代码生成', 'CodeGenerator', 0, 0, null, 'code-generator', 1, '/automation/generator/index.vue', null, 1, 1, 1, null, 31, '2024-07-27 12:24:54', null),
        (33, '导入', '', 0, 0, null, null, 2, null, 'gen:code:import', 1, 1, 1, null, 31, '2024-08-04 12:49:58', null),
        (34, '新增业务', '', 0, 0, null, null, 2, null, 'gen:code:business:add', 1, 1, 1, null, 31, '2024-08-04 12:51:29', null),
        (35, '编辑业务', '', 0, 0, null, null, 2, null, 'gen:code:business:edit', 1, 1, 1, null, 31, '2024-08-04 12:51:45', null),
        (36, '删除业务', '', 0, 0, null, null, 2, null, 'gen:code:business:del', 1, 1, 1, null, 31, '2024-08-04 12:52:05', null),
        (37, '新增模型', '', 0, 0, null, null, 2, null, 'gen:code:model:add', 1, 1, 1, null, 31, '2024-08-04 12:52:28', null),
        (38, '编辑模型', '', 0, 0, null, null, 2, null, 'gen:code:model:edit', 1, 1, 1, null, 31, '2024-08-04 12:52:45', null),
        (39, '删除模型', '', 0, 0, null, null, 2, null, 'gen:code:model:del', 1, 1, 1, null, 31, '2024-08-04 12:52:59', null),
        (40, '生成', '', 0, 0, null, null, 2, null, 'gen:code:generate', 1, 1, 1, null, 31, '2024-08-04 12:55:03', null),
        (41, 'GitHub', 'github', 0, 8888, 'IconGithub', 'https://github.com/wu-clan', 0, null, null, 1, 1, 1, null, null, '2024-07-27 12:32:46', null),
        (42, '赞助', 'sponsor', 0, 9999, 'IconFire', 'https://wu-clan.github.io/sponsor/', 0, null, null, 1, 1, 1, null, null, '2024-07-27 12:39:57', null);

INSERT INTO fba.sys_role (id, name, data_scope, status, remark, created_time, updated_time)
VALUES (1, 'test', 2, 1, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_role_menu (id, role_id, menu_id)
VALUES (1, 1, 1);

-- 密码明文：123456
INSERT INTO fba.sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$RJXAtJodRw37ZQGxTPlu0OH.aN5lNXG6yvC4Tp9GIQEBmMY/YCc.m', 'bcNjV', 'admin@example.com', 1, 1, 1, 0, null, null, '2023-06-26 17:13:45', null, 1, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_user_role (id, user_id, role_id)
VALUES (1, 1, 1);
