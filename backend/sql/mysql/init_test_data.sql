insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values  (1, 'test', 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

insert into fba.sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values  (1, 'Test', 'Test', 'test', 0, null, 0, null, null, 0, 0, 1, null, null, null, '2023-07-27 19:14:10', null),
        (2, 'dashboard', 'Dashboard', 'dashboard', 0, 'material-symbols:dashboard', 0, null, null, 1, 1, 1, null, null, null, '2023-07-27 19:15:45', null),
        (3, 'Workstation', 'Workspace', 'workspace', 0, null, 1, '/dashboard/workspace/index.vue', null, 1, 1, 1, null, null, 2, '2023-07-27 19:17:59', null),
        (4, 'Data analysis', 'Analytics', 'analytics', 0, null, 1, '/dashboard/analytics/index.vue', null, 1, 1, 1, null, null, 2, '2023-07-27 19:17:59', null),
        (5, 'System management', 'Admin', 'admin', 0, 'eos-icons:admin', 0, null, null, 1, 1, 1, null, null, null, '2023-07-27 19:23:00', null),
        (6, 'Sector management', 'SysDept', 'sys-dept', 0, null, 1, '/admin/dept/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:23:42', null),
        (7, 'User Management', 'SysUser', 'sys-user', 0, null, 1, '/admin/user/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:25:13', null),
        (8, 'Role management', 'SysRole', 'sys-role', 0, null, 1, '/admin/role/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:25:45', null),
        (9, 'Menu Management', 'SysMenu', 'sys-menu', 0, null, 1, '/admin/menu/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:45:29', null),
        (10, 'API MANAGEMENT', 'SysApi', 'sys-api', 0, null, 1, '/admin/api/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:24:12', null),
        (11, 'Data rule management', 'SysDataRule', 'sys-data-rule', 0, null, 1, '/admin/data-rule/index.vue', null, 1, 1, 1, null, null, 5, '2023-07-27 19:24:12', null),
        (12, 'System automation', 'Automation', 'automation', 0, 'material-symbols:automation', 0, null, null, 1, 1, 1, null, null, null, '2024-07-27 02:06:20', null),
        (13, 'Code Generation', 'CodeGenerator', 'code-generator', 0, null, 1, '/automation/code-generator/index.vue', null, 1, 1, 1, null, null, 12, '2024-07-27 12:24:54', null),
        (14, 'System monitoring', 'Monitor', 'monitor', 0, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, null, null, null, '2023-07-27 19:27:08', null),
        (15, 'Redis Monitor', 'Redis', 'redis', 0, null, 1, '/monitor/redis/index.vue', null, 1, 1, 1, null, null, 14, '2023-07-27 19:28:03', null),
        (16, 'Server Monitor', 'Server', 'server', 0, null, 1, '/monitor/server/index.vue', null, 1, 1, 1, null, null, 14, '2023-07-27 19:28:29', null),
        (17, 'Log', 'Log', 'log', 0, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, null, null, null, '2023-07-27 19:19:59', null),
        (18, 'Login Log', 'Login', 'login', 0, null, 1, '/log/login/index.vue', null, 1, 1, 1, null, null, 17, '2023-07-27 19:20:56', null),
        (19, 'Operation Log', 'Opera', 'opera', 0, null, 1, '/log/opera/index.vue', null, 1, 1, 1, null, null, 17, '2023-07-27 19:21:28', null),
        (20, 'Network of officials', 'Site', '', 998, 'dashicons:admin-site', 1, null, null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs/', null, null, '2023-07-27 19:22:24', null),
        (21, 'Sponsorship', 'Sponsor', '', 999, 'material-icon-theme:github-sponsors', 1, null, null, 1, 1, 1, 'https://wu-clan.github.io/sponsor/', null, null, '2024-07-27 12:39:57', null);

insert into sys_role (id, name, status, remark, created_time, updated_time)
values  (1, 'test', 1, null, '2023-06-26 17:13:45', null);

insert into sys_role_menu (id, role_id, menu_id)
values  (1, 1, 1);

insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values  (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', 'User88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', 0x24326224313224387932654E7563583139566A6D5A33745968424C634F, 'admin@example.com', 1, 1, 1, 0, null, null, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 1, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

insert into sys_user_role (id, user_id, role_id)
values  (1, 1, 1);
