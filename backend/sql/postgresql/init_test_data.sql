insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values  (1, 'test', 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

insert into sys_api (id, name, method, path, remark, created_time, updated_time)
values  (1, '创建API', 'POST', '/api/v1/apis', null, '2024-02-02 11:29:47', null),
        (2, '删除API', 'DELETE', '/api/v1/apis', null, '2024-02-02 11:31:32', null),
        (3, '编辑API', 'PUT', '/api/v1/apis/{pk}', null, '2024-02-02 11:32:22', null);

insert into sys_menu (id, title, name, sort, icon, path, menu_type, component, perms, status, display, cache, remark, parent_id, created_time, updated_time)
values  (1, '测试', 'test', 0, '', null, 0, null, null, 0, 0, 1, null, null, '2023-07-27 19:14:10', null),
        (2, '仪表盘', 'dashboard', 0, 'IconDashboard', 'dashboard', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:15:45', null),
        (3, '工作台', 'Workplace', 0, null, 'workplace', 1, '/dashboard/workplace/index.vue', null, 1, 1, 1, null, 2, '2023-07-27 19:17:59', null),
        (4, '系统管理', 'admin', 0, 'IconSettings', 'admin', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:23:00', null),
        (5, '部门管理', 'SysDept', 0, null, 'sys-dept', 1, '/admin/dept/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:23:42', null),
        (6, '用户管理', 'SysUser', 0, null, 'sys-user', 1, '/admin/user/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:25:13', null),
        (7, '角色管理', 'SysRole', 0, null, 'sys-role', 1, '/admin/role/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:25:45', null),
        (8, '菜单管理', 'SysMenu', 0, null, 'sys-menu', 1, '/admin/menu/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:45:29', null),
        (9, 'API 管理', 'SysApi', 0, null, 'sys-api', 1, '/admin/api/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:24:12', null),
        (10, '数据规则管理', 'SysDataRule', 0, null, 'sys-data-rule', 1, '/admin/data-rule/index.vue', null, 1, 1, 1, null, 4, '2023-07-27 19:24:12', null),
        (11, '系统自动化', 'automation', 0, 'IconCodeSquare', 'automation', 0, null, null, 1, 1, 1, null, null, '2024-07-27 02:06:20', '2024-07-27 02:18:52'),
        (12, '代码生成', 'CodeGenerator', 0, null, 'code-generator', 1, '/automation/generator/index.vue', null, 1, 1, 1, null, 11, '2024-07-27 12:24:54', null),
        (13, '系统监控', 'monitor', 0, 'IconComputer', 'monitor', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:27:08', null),
        (14, 'Redis 监控', 'Redis', 0, null, 'redis', 1, '/monitor/redis/index.vue', 'sys:monitor:redis', 1, 1, 1, null, 13, '2023-07-27 19:28:03', null),
        (15, '服务器监控', 'Server', 0, null, 'server', 1, '/monitor/server/index.vue', 'sys:monitor:server', 1, 1, 1, null, 13, '2023-07-27 19:28:29', null),
        (16, '日志', 'log', 0, 'IconBug', 'log', 0, null, null, 1, 1, 1, null, null, '2023-07-27 19:19:59', null),
        (17, '登录日志', 'Login', 0, null, 'login', 1, '/log/login/index.vue', null, 1, 1, 1, null, 16, '2023-07-27 19:20:56', null),
        (18, '操作日志', 'Opera', 0, null, 'opera', 1, '/log/opera/index.vue', null, 1, 1, 1, null, 16, '2023-07-27 19:21:28', null),
        (19, '官网', 'site', 998, 'IconComputer', 'https://fastapi-practices.github.io/fastapi_best_architecture_docs/', 1, null, null, 1, 1, 1, null, null, '2023-07-27 19:22:24', null),
        (20, '赞助', 'sponsor', 999, 'IconFire', 'https://wu-clan.github.io/sponsor/', 1, null, null, 1, 1, 1, null, null, '2024-07-27 12:39:57', null);

insert into sys_role (id, name, status, remark, created_time, updated_time)
values  (1, 'test', 1, null, '2023-06-26 17:13:45', null);

insert into sys_role_menu (id, role_id, menu_id)
values  (1, 1, 1);

insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values  (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', '0x24326224313224387932654E7563583139566A6D5A33745968424C634F', 'admin@example.com', 1, 1, 1, 0, null, null, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 1, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

insert into sys_user_role (id, user_id, role_id)
values  (1, 1, 1);
