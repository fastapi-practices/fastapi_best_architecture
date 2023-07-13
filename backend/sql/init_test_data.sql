INSERT INTO fba.sys_dept (id, name, level, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
VALUES (1, 'test', 0, 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_menu (id, name, level, sort, icon, path, menu_type, component, perms, status, remark, parent_id, created_time, updated_time, show, cache, title)
values  (1, 'test', 0, 0, null, null, 0, null, null, 1, null, null, '2023-06-26 17:13:45', null, 0, 1, '测试'),
        (2, 'dashboard', 0, 0, 'icon-dashboard', '/dashboard', 0, '/dashboard/workplace/index.vue', null, 1, null, null, '2023-06-30 10:10:34', null, 1, 1, '仪表盘'),
        (3, 'Workplace', 0, 0, null, '/workplace', 1, null, null, 1, null, 2, '2023-06-30 10:11:40', null, 1, 1, '工作台'),
        (4, 'arcoWebsite', 0, 888, 'icon-link', 'https://arco.design', 0, null, null, 1, null, null, '2023-06-30 10:13:04', '2023-07-07 20:05:20', 1, 1, 'arco官网'),
        (5, 'log', 0, 66, 'icon-bug', '/log', 0, null, null, 1, '这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；这是系统日志记录；', null, '2023-06-30 10:13:54', '2023-07-07 20:04:42', 1, 1, '日志'),
        (6, 'Login', 0, 0, null, '/login', 1, '/log/login/index.vue', null, 1, null, 5, '2023-06-30 10:14:23', null, 1, 1, '登录日志'),
        (7, 'faq', 0, 999, 'icon-question-circle', 'https://arco.design/vue/docs/pro/faq', 0, null, null, 1, null, null, '2023-06-30 10:14:56', '2023-07-07 20:05:10', 1, 1, '常见问题'),
        (8, 'admin', 0, 6, 'icon-settings', '/admin', 0, '', null, 1, null, null, '2023-07-04 10:52:48', '2023-07-07 20:06:02', 1, 1, '系统管理'),
        (9, 'SysMenu', 0, 2, '', '/sys-menu', 1, '/admin/menu/index.vue', null, 1, '系统后台菜单管理，玛卡巴卡?', 8, '2023-07-04 10:55:02', '2023-07-08 22:43:53', 1, 1, '菜单管理'),
        (10, 'test', 0, 100, null, null, 0, null, null, 1, null, null, '2023-07-07 20:23:57', '2023-07-07 20:04:53', 0, 1, '测试2'),
        (11, 'test', 0, 0, null, null, 1, null, null, 1, null, 10, '2023-07-07 20:20:55', null, 1, 1, '测试3'),
        (12, '', 0, 0, null, null, 2, null, null, 1, null, 11, '2023-07-07 20:42:31', null 1, 1, '测试4'),
        (13, '', 0, 0, null, null, 2, null, null, 1, null, 11, '2023-07-07 20:42:52', null 1, 1, '测试5'),
        (14, '', 0, 0, null, null, 2, null, null, 1, null, 11, '2023-07-07 20:16:27', null, 1, 1, '测试6'),
        (15, 'Opera', 0, 0, null, '/opera', 1, '/log/opera/index.vue', null, 1, null, 5, '2023-07-07 20:28:21', null, 1, 1, '操作日志'),
        (16, 'SysDept', 0, 0, null, 'sys-dept', 1, '/admin/dept/index.vue', null, 1, null, 8, '2023-07-08 22:43:20', null, 1, 1, '部门管理');
        (17, 'SysApi', 0, 1, null, 'sys-api', 1, '/admin/api/index.vue', null, 1, null, 8, '2023-07-10 13:10:16', null, 1, 1, 'API管理');
        (18, 'monitor', 0, 88, 'icon-computer', null, 0, null, null, 1, null, null, '2023-07-11 20:20:20', null, 1, 1, '系统监控'),
        (19, 'Redis', 0, 0, null, null, 1, '/monitor/redis/index.vue', null, 1, null, 18, '2023-07-11 20:21:28', null, 1, 1, 'Redis监控'),
        (20, 'Server', 0, 0, null, 'server', 1, '/monitor/server/index.vue', null, 1, null, 18, '2023-07-11 20:23:43', null, 1, 1, '服务器监控');
        (21, 'SysUser', 0, 0, null, 'sys-user', 1, '/admin/user/index.vue', null, 1, null, 8, '2023-07-13 03:32:47', null, 1, 1, '用户管理');

INSERT INTO fba.sys_role (id, name, data_scope, status, remark, created_time, updated_time)
VALUES (1, 'test', 2, 1, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_role_menu (id, role_id, menu_id)
VALUES (1, 1, 1);

INSERT INTO fba.sys_user (id, uuid, username, nickname, password, email, is_superuser, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'test', 'test', '$2b$12$TpdL7kKriqhpJHSBMT.Fr.hJNBx5SdUybi.NT1DV5MojYpV9PpRre', 'test@gmail.com', 1, 1, 0, null, null, '2023-06-26 17:13:45', null, 1, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_user_role (id, user_id, role_id)
VALUES (1, 1, 1);
