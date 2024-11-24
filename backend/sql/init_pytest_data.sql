INSERT INTO `fba_test`.`sys_dept` (`id`, `name`, `level`, `sort`, `leader`, `phone`, `email`, `status`, `del_flag`, `parent_id`, `created_time`, `updated_time`)
VALUES (1, 'test', 0, 0, NULL, NULL, NULL, 1, 0, NULL, '2023-06-26 17:13:45', NULL);

INSERT INTO `fba_test`.`sys_api` (`id`, `name`, `method`, `path`, `remark`, `created_time`, `updated_time`)
VALUES (1, '创建API', 'POST', '/api/v1/apis', NULL, '2024-02-02 11:29:47', NULL),
       (2, '删除API', 'DELETE', '/api/v1/apis', NULL, '2024-02-02 11:31:32', NULL),
       (3, '编辑API', 'PUT', '/api/v1/apis/{pk}', NULL, '2024-02-02 11:32:22', NULL);

INSERT INTO `fba_test`.`sys_menu` (`id`, `title`, `name`, `level`, `sort`, `icon`, `path`, `menu_type`, `component`, `perms`, `status`, `show`, `cache`, `remark`, `parent_id`, `created_time`, `updated_time`)
VALUES (1, '测试', 'test', 0, 0, '', NULL, 0, NULL, NULL, 0, 0, 1, NULL, NULL, '2023-07-27 19:14:10', NULL),
       (2, '仪表盘', 'dashboard', 0, 0, 'IconDashboard', 'dashboard', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:15:45', NULL),
       (3, '工作台', 'Workplace', 0, 0, NULL, 'workplace', 1, '/dashboard/workplace/index.vue', NULL, 1, 1, 1, NULL, 2, '2023-07-27 19:17:59', NULL),
       (4, '系统管理', 'admin', 0, 0, 'IconSettings', 'admin', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:23:00', NULL),
       (5, '部门管理', 'SysDept', 0, 0, NULL, 'sys-dept', 1, '/admin/dept/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:23:42', NULL),
       (6, '用户管理', 'SysUser', 0, 0, NULL, 'sys-user', 1, '/admin/user/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:25:13', NULL),
       (7, '角色管理', 'SysRole', 0, 0, NULL, 'sys-role', 1, '/admin/role/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:25:45', NULL),
       (8, '菜单管理', 'SysMenu', 0, 0, NULL, 'sys-menu', 1, '/admin/menu/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:45:29', NULL),
       (9, 'API 管理', 'SysApi', 0, 0, NULL, 'sys-api', 1, '/admin/api/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:24:12', NULL),
       (10, '数据规则管理', 'SysDataRule', 0, 0, NULL, 'sys-data-rule', 1, '/admin/data-rule/index.vue', NULL, 1, 1, 1, NULL, 4, '2023-07-27 19:24:12', NULL),
       (11, '系统自动化', 'automation', 0, 0, 'IconCodeSquare', 'automation', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2024-07-27 02:06:20', '2024-07-27 02:18:52'),
       (12, '代码生成', 'CodeGenerator', 0, 0, NULL, 'code-generator', 1, '/automation/generator/index.vue', NULL, 1, 1, 1, NULL, 11, '2024-07-27 12:24:54', NULL),
       (13, '系统监控', 'monitor', 0, 0, 'IconComputer', 'monitor', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:27:08', NULL),
       (14, 'Redis 监控', 'Redis', 0, 0, NULL, 'redis', 1, '/monitor/redis/index.vue', 'sys:monitor:redis', 1, 1, 1, NULL, 13, '2023-07-27 19:28:03', NULL),
       (15, '服务器监控', 'Server', 0, 0, NULL, 'server', 1, '/monitor/server/index.vue', 'sys:monitor:server', 1, 1, 1, NULL, 13, '2023-07-27 19:28:29', NULL),
       (16, '日志', 'log', 0, 0, 'IconBug', 'log', 0, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:19:59', NULL),
       (17, '登录日志', 'Login', 0, 0, NULL, 'login', 1, '/log/login/index.vue', NULL, 1, 1, 1, NULL, 16, '2023-07-27 19:20:56', NULL),
       (18, '操作日志', 'Opera', 0, 0, NULL, 'opera', 1, '/log/opera/index.vue', NULL, 1, 1, 1, NULL, 16, '2023-07-27 19:21:28', NULL),
       (19, '官网', 'site', 0, 998, 'IconComputer', 'https://fastapi-practices.github.io/fastapi_best_architecture_docs/', 1, NULL, NULL, 1, 1, 1, NULL, NULL, '2023-07-27 19:22:24', NULL),
       (20, '赞助', 'sponsor', 0, 999, 'IconFire', 'https://wu-clan.github.io/sponsor/', 1, NULL, NULL, 1, 1, 1, NULL, NULL, '2024-07-27 12:39:57', NULL);

INSERT INTO `fba_test`.`sys_role` (`id`, `name`, `data_scope`, `status`, `remark`, `created_time`, `updated_time`) VALUES (1, 'test', 2, 1, NULL, '2023-06-26 17:13:45', NULL);

INSERT INTO `fba_test`.`sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (1, 1, 1);

-- 密码明文：123456
INSERT INTO `fba_test`.`sys_user` (`id`, `uuid`, `username`, `nickname`, `password`, `salt`, `email`, `is_superuser`, `is_staff`, `status`, `is_multi_login`, `avatar`, `phone`, `join_time`, `last_login_time`, `dept_id`, `created_time`, `updated_time`)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', 0x24326224313224387932654E7563583139566A6D5A33745968424C634F, 'admin@example.com', 1, 1, 1, 0, NULL, NULL, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 1, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

INSERT INTO `fba_test`.`sys_user_role` (`id`, `user_id`, `role_id`) VALUES (1, 1, 1);
