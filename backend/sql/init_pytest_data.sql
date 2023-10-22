INSERT INTO fba_test.sys_dept (id, name, level, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
VALUES (1, 'test', 0, 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

INSERT INTO fba_test.sys_menu (id, title, name, level, sort, icon, path, menu_type, component, perms, status, `show`, cache, remark, parent_id, created_time, updated_time)
VALUES  (1, '测试', 'test', 0, 0, '', null, 0, null, null, 0, 0, 1, null, null, '2023-07-27 19:14:10', '2023-07-27 19:14:52'),
        (2, '仪表盘', 'dashboard', 0, 0, 'IconDashboard', 'dashboard', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:15:45', null),
        (3, '工作台', 'Workplace', 0, 0, null, 'workplace', 1, '/dashboard/workplace/index.vue', null, 1, 1, 1, null, 2, '2023-07-27 19:17:59', null),
        (4, 'arco官网', 'arcoWebsite', 0, 888, 'IconLink', 'https://arco.design', 1, null, null, 1, 1, 1, null, null, '2023-07-27 19:19:23', null),
        (5, '日志', 'log', 0, 66, 'IconBug', 'log', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:19:59', null),
        (6, '登录日志', 'Login', 0, 0, null, 'login', 1, '/log/login/index.vue', null, 1, 1, 1, null, 5, '2023-07-27 19:20:56', null),
        (7, '操作日志', 'Opera', 0, 0, null, 'opera', 1, '/log/opera/index.vue', null, 1, 1, 1, null, 5, '2023-07-27 19:21:28', null),
        (8, '常见问题', 'faq', 0, 999, 'IconQuestion', 'https://arco.design/vue/docs/pro/faq', 1, null, null, 1, 1, 1, null, null, '2023-07-27 19:22:24', null),
        (9, '系统管理', 'admin', 0, 6, 'IconSettings', 'admin', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:23:00', null),
        (10, '部门管理', 'SysDept', 0, 0, null, 'sys-dept', 1, '/admin/dept/index.vue', null, 1, 1, 1, null, 9, '2023-07-27 19:23:42', null),
        (11, 'API管理', 'SysApi', 0, 1, null, 'sys-api', 1, '/admin/api/index.vue', null, 1, 1, 1, null, 9, '2023-07-27 19:24:12', null),
        (12, '用户管理', 'SysUser', 0, 0, null, 'sys-user', 1, '/admin/user/index.vue', null, 1, 1, 1, null, 9, '2023-07-27 19:25:13', null),
        (13, '角色管理', 'SysRole', 0, 2, null, 'sys-role', 1, '/admin/role/index.vue', null, 1, 1, 1, null, 9, '2023-07-27 19:25:45', null),
        (14, '菜单管理', 'SysMenu', 0, 2, null, 'sys-menu', 1, '/admin/menu/index.vue', null, 1, 1, 1, null, 9, '2023-07-27 19:45:29', null),
        (15, '系统监控', 'monitor', 0, 88, 'IconComputer', 'monitor', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:27:08', null),
        (16, 'Redis监控', 'Redis', 0, 0, null, 'redis', 1, '/monitor/redis/index.vue', null, 1, 1, 1, null, 15, '2023-07-27 19:28:03', null),
        (17, '服务器监控', 'Server', 0, 0, null, 'server', 1, '/monitor/server/index.vue', null, 1, 1, 1, null, 15, '2023-07-27 19:28:29', null);

INSERT INTO fba_test.sys_role (id, name, data_scope, status, remark, created_time, updated_time)
VALUES (1, 'test', 2, 1, null, '2023-06-26 17:13:45', null);

INSERT INTO fba_test.sys_role_menu (id, role_id, menu_id)
VALUES (1, 1, 1);

-- 密码明文：123456
INSERT INTO fba_test.sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$RJXAtJodRw37ZQGxTPlu0OH.aN5lNXG6yvC4Tp9GIQEBmMY/YCc.m', 'bcNjV', 'admin@example.com', 1, 1, 1, 0, null, null, '2023-06-26 17:13:45', null, 1, '2023-06-26 17:13:45', null);

INSERT INTO fba_test.sys_user_role (id, user_id, role_id)
VALUES (1, 1, 1);
