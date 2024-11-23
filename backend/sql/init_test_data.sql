INSERT INTO `fba`.`sys_dept` (`id`, `name`, `level`, `sort`, `leader`, `phone`, `email`, `status`, `del_flag`, `parent_id`, `created_time`, `updated_time`)
VALUES (1, 'test', 0, 0, NULL, NULL, NULL, 1, 0, NULL, '2023-06-26 17:13:45', NULL);

INSERT INTO `fba`.`sys_api` (`id`, `name`, `method`, `path`, `remark`, `created_time`, `updated_time`)
VALUES (1, '创建API', 'POST', '/api/v1/apis', NULL, '2024-02-02 11:29:47', NULL),
       (2, '删除API', 'DELETE', '/api/v1/apis', NULL, '2024-02-02 11:31:32', NULL),
       (3, '编辑API', 'PUT', '/api/v1/apis/{pk}', NULL, '2024-02-02 11:32:22', NULL);

INSERT INTO `fba`.`sys_menu` (`id`, `title`, `name`, `level`, `sort`, `icon`, `path`, `menu_type`, `component`, `perms`, `status`, `show`, `cache`, `remark`, `parent_id`, `created_time`, `updated_time`)
VALUES (1, '测试', 'test', 0, 0, '', NULL, 0, NULL, NULL, 0, 0, 1, NULL, NULL, '2023-07-27 19:14:10', NULL),
       (2, '仪表盘', 'dashboard', 0, 0, 'IconDashboard', 'dashboard', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:15:45', NULL),
       (3, '工作台', 'Workplace', 0, 0, NULL, 'workplace', 1, '/dashboard/workplace/index.vue', NULL, 1, 1, 1, NULL, 2, '2023-07-27 19:17:59', NULL),
       (4, '日志', 'log', 0, 66, 'IconBug', 'log', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:19:59', NULL),
       (5, '登录日志', 'Login', 0, 0, NULL, 'login', 1, '/log/login/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:20:56', NULL),
       (6, '操作日志', 'Opera', 0, 0, NULL, 'opera', 1, '/log/opera/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:21:28', NULL),
       (7, '系统管理', 'admin', 0, 6, 'IconSettings', 'admin', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:23:00', NULL),
       (8, '部门管理', 'SysDept', 0, 0, NULL, 'sys-dept', 1, '/admin/dept/index.vue', NULL, 1, 1, 1, NULL, 7, '2023-07-27 19:23:42', NULL),
       (9, '新增', '', 0, 0, NULL, NULL, 2, NULL, 'sys:dept:add', 1, 1, 1, NULL, 8, '2024-01-07 11:37:00', NULL),
       (10, '编辑', '', 0, 0, NULL, NULL, 2, NULL, 'sys:dept:edit', 1, 1, 1, NULL, 8, '2024-01-07 11:37:29', NULL),
       (11, '删除', '', 0, 0, NULL, NULL, 2, NULL, 'sys:dept:del', 1, 1, 1, NULL, 8, '2024-01-07 11:37:44', NULL),
       (12, 'API管理', 'SysApi', 0, 1, NULL, 'sys-api', 1, '/admin/api/index.vue', NULL, 1, 1, 1, NULL, 7, '2023-07-27 19:24:12', NULL),
       (13, '新增', '', 0, 0, NULL, NULL, 2, NULL, 'sys:api:add', 1, 1, 1, NULL, 12, '2024-01-07 11:57:09', NULL),
       (14, '编辑', '', 0, 0, NULL, NULL, 2, NULL, 'sys:api:edit', 1, 1, 1, NULL, 12, '2024-01-07 11:57:44', NULL),
       (15, '删除', '', 0, 0, NULL, NULL, 2, NULL, 'sys:api:del', 1, 1, 1, NULL, 12, '2024-01-07 11:57:56', NULL),
       (16, '用户管理', 'SysUser', 0, 0, NULL, 'sys-user', 1, '/admin/user/index.vue', NULL, 1, 1, 1, NULL, 7, '2023-07-27 19:25:13', NULL),
       (17, '编辑用户角色', '', 0, 0, NULL, NULL, 2, NULL, 'sys:user:role:edit', 1, 1, 1, NULL, 16, '2024-01-07 12:04:20', NULL),
       (18, '注销', '', 0, 0, NULL, NULL, 2, NULL, 'sys:user:del', 1, 1, 1, '用户注销 != 用户登出，注销之后用户将从数据库删除', 16, '2024-01-07 02:28:09', NULL),
       (19, '角色管理', 'SysRole', 0, 2, NULL, 'sys-role', 1, '/admin/role/index.vue', NULL, 1, 1, 1, NULL, 7, '2023-07-27 19:25:45', NULL),
       (20, '新增', '', 0, 0, NULL, NULL, 2, NULL, 'sys:role:add', 1, 1, 1, NULL, 19, '2024-01-07 11:58:37', NULL),
       (21, '编辑', '', 0, 0, NULL, NULL, 2, NULL, 'sys:role:edit', 1, 1, 1, NULL, 19, '2024-01-07 11:58:52', NULL),
       (22, '删除', '', 0, 0, NULL, NULL, 2, NULL, 'sys:role:del', 1, 1, 1, NULL, 19, '2024-01-07 11:59:07', NULL),
       (23, '编辑角色菜单', '', 0, 0, NULL, NULL, 2, NULL, 'sys:role:menu:edit', 1, 1, 1, NULL, 19, '2024-01-07 01:59:39', NULL),
       (24, '编辑角色部门', '', 0, 0, NULL, NULL, 2, NULL, 'sys:role:dept:edit', 1, 1, 1, NULL, 19, '2024-01-07 01:59:39', NULL),
       (25, '菜单管理', 'SysMenu', 0, 2, NULL, 'sys-menu', 1, '/admin/menu/index.vue', NULL, 1, 1, 1, NULL, 7, '2023-07-27 19:45:29', NULL),
       (26, '新增', '', 0, 0, NULL, NULL, 2, NULL, 'sys:menu:add', 1, 1, 1, NULL, 25, '2024-01-07 12:01:24', NULL),
       (27, '编辑', '', 0, 0, NULL, NULL, 2, NULL, 'sys:menu:edit', 1, 1, 1, NULL, 25, '2024-01-07 12:01:34', NULL),
       (28, '删除', '', 0, 0, NULL, NULL, 2, NULL, 'sys:menu:del', 1, 1, 1, NULL, 25, '2024-01-07 12:01:48', NULL),
       (29, '系统监控', 'monitor', 0, 88, 'IconComputer', 'monitor', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:27:08', NULL),
       (30, 'Redis监控', 'Redis', 0, 0, NULL, 'redis', 1, '/monitor/redis/index.vue', 'sys:monitor:redis', 1, 1, 1, NULL, 29, '2023-07-27 19:28:03', NULL),
       (31, '服务器监控', 'Server', 0, 0, NULL, 'server', 1, '/monitor/server/index.vue', 'sys:monitor:server', 1, 1, 1, NULL, 29, '2023-07-27 19:28:29', NULL),
       (32, '系统自动化', 'automation', 0, 777, 'IconCodeSquare', 'automation', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2024-07-27 02:06:20', '2024-07-27 02:18:52'),
       (33, '代码生成', 'CodeGenerator', 0, 0, NULL, 'code-generator', 1, '/automation/generator/index.vue', NULL, 1, 1, 1, NULL, 32, '2024-07-27 12:24:54', NULL),
       (34, '导入', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:import', 1, 1, 1, NULL, 32, '2024-08-04 12:49:58', NULL),
       (35, '新增业务', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:business:add', 1, 1, 1, NULL, 32, '2024-08-04 12:51:29', NULL),
       (36, '编辑业务', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:business:edit', 1, 1, 1, NULL, 32, '2024-08-04 12:51:45', NULL),
       (37, '删除业务', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:business:del', 1, 1, 1, NULL, 32, '2024-08-04 12:52:05', NULL),
       (38, '新增模型', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:model:add', 1, 1, 1, NULL, 32, '2024-08-04 12:52:28', NULL),
       (39, '编辑模型', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:model:edit', 1, 1, 1, NULL, 32, '2024-08-04 12:52:45', NULL),
       (40, '删除模型', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:model:del', 1, 1, 1, NULL, 32, '2024-08-04 12:52:59', NULL),
       (41, '生成', '', 0, 0, NULL, NULL, 2, NULL, 'gen:code:generate', 1, 1, 1, NULL, 32, '2024-08-04 12:55:03', NULL),
       (42, '官网', 'site', 0, 999, 'IconComputer', 'https://fastapi-practices.github.io/fastapi_best_architecture_docs/', 1, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:22:24', NULL),
       (43, '赞助', 'sponsor', 0, 9999, 'IconFire', 'https://wu-clan.github.io/sponsor/', 1, NULL, NULL, 1, 1, 1, NULL, NULL, '2024-07-27 12:39:57', NULL);

INSERT INTO `fba`.`sys_role` (`id`, `name`, `data_scope`, `status`, `remark`, `created_time`, `updated_time`) VALUES (1, 'test', 2, 1, NULL, '2023-06-26 17:13:45', NULL);

INSERT INTO `fba`.`sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (1, 1, 1);

-- 密码明文：123456
INSERT INTO `fba`.`sys_user` (`id`, `uuid`, `username`, `nickname`, `password`, `salt`, `email`, `is_superuser`, `is_staff`, `status`, `is_multi_login`, `avatar`, `phone`, `join_time`, `last_login_time`, `dept_id`, `created_time`, `updated_time`)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', 0x24326224313224387932654E7563583139566A6D5A33745968424C634F, 'admin@example.com', 1, 1, 1, 0, NULL, NULL, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 1, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

INSERT INTO `fba`.`sys_user_role` (`id`, `user_id`, `role_id`) VALUES (1, 1, 1);
