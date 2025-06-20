insert into sys_dept  (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2047437114580271104, '测试', 0, null, null, null, 1, 0, null, '2025-05-26 17:13:45', null);

insert into sys_menu  (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (2047437114622214144, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:26:18', null),
        (2047437114689323008, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:30:01', null),
        (2047437114756431872, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:31:41', null),
        (2047437114819346432, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:32:34', null),
        (2047437114886455296, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:33:29', null),
        (2047437114949369856, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:35:41', null),
        (2047437115016478720, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2047437114622214144, '2025-06-09 17:54:29', null),
        (2047437115083587584, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2047437114622214144, '2025-06-09 17:57:09', null),
        (2047437115150696448, '文档', 'Document', 'document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2047437114949369856, '2025-06-09 17:59:44', null),
        (2047437115217805312, 'Github', 'Github', 'github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2047437114949369856, '2025-06-09 18:00:50', null),
        (2047437115284914176, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2047437114949369856, '2025-06-09 18:01:39', null),
        (2047437115352023040, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:03:17', null),
        (2047437115414937600, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:03:54', null),
        (2047437115477852160, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:04:47', null),
        (2047437115540766720, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:05:31', null),
        (2047437115607875584, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:07:04', null),
        (2047437115674984448, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2047437115607875584, '2025-06-09 18:07:46', null),
        (2047437115742093312, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2047437115607875584, '2025-06-09 18:08:22', null),
        (2047437115809202176, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:09:12', null),
        (2047437115876311040, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:10:20', null),
        (2047437115943419904, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:11:10', null),
        (2047437116010528768, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2047437114689323008, '2025-06-09 18:11:38', null),
        (2047437116077637632, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 2047437114756431872, '2025-06-09 18:12:38', null),
        (2047437116144746496, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 2047437114756431872, '2025-06-09 18:13:19', null),
        (2047437116211855360, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2047437114819346432, '2025-06-09 18:14:35', null),
        (2047437116274769920, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2047437114819346432, '2025-06-09 18:15:26', null),
        (2047437116341878784, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2047437114886455296, '2025-06-09 18:17:12', null),
        (2047437116408987648, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2047437114886455296, '2025-06-09 18:17:42', null),
        (2047437116476096512, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2047437114886455296, '2025-06-09 18:18:12', null),
        (2047437116543205376, '个人中心', 'Profile', 'profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, '2025-06-09 18:18:12', null),
        (2047437116610314240, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2047437115352023040, '2025-06-09 18:21:17', null),
        (2047437116677423104, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2047437115352023040, '2025-06-09 18:22:01', null),
        (2047437116744531968, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2047437115352023040, '2025-06-09 18:22:39', null),
        (2047437116807446528, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2047437115414937600, '2025-06-09 18:24:09', null),
        (2047437116870361088, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2047437115477852160, '2025-06-09 18:25:08', null),
        (2047437116937469952, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2047437115477852160, '2025-06-09 18:26:30', null),
        (2047437117004578816, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 2047437115477852160, '2025-06-09 18:27:24', null),
        (2047437117067493376, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 2047437115477852160, '2025-06-09 18:28:25', null),
        (2047437117134602240, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2047437115477852160, '2025-06-09 18:28:55', null),
        (2047437117201711104, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2047437115540766720, '2025-06-09 18:29:51', null),
        (2047437117268819968, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2047437115540766720, '2025-06-09 18:30:13', null),
        (2047437117335928832, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2047437115540766720, '2025-06-09 18:30:37', null),
        (2047437117403037696, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2047437115674984448, '2025-06-09 18:31:11', null),
        (2047437117470146560, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2047437115674984448, '2025-06-09 18:31:42', null),
        (2047437117537255424, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2047437115674984448, '2025-06-09 18:32:36', null),
        (2047437117600169984, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2047437115674984448, '2025-06-09 18:33:09', null),
        (2047437117663084544, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2047437115742093312, '2025-06-09 18:35:54', null),
        (2047437117730193408, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2047437115742093312, '2025-06-09 18:36:19', null),
        (2047437117793107968, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2047437115742093312, '2025-06-09 18:36:44', null),
        (2047437117860216832, '安装插件', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2047437115809202176, '2025-06-09 18:38:14', null),
        (2047437117927325696, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2047437115809202176, '2025-06-09 18:39:08', null),
        (2047437117994434560, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2047437115809202176, '2025-06-09 18:39:47', null),
        (2047437118061543424, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2047437115876311040, '2025-06-09 18:45:52', null),
        (2047437118128652288, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2047437115876311040, '2025-06-09 18:46:13', null),
        (2047437118195761152, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2047437115876311040, '2025-06-09 18:46:36', null),
        (2047437118262870016, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:48:17', null),
        (2047437118325784576, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:48:49', null),
        (2047437118392893440, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:49:23', null),
        (2047437118460002304, '新增', 'AddSysDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:50:01', null),
        (2047437118527111168, '修改', 'EditSysDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:50:26', null),
        (2047437118594220032, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2047437115943419904, '2025-06-09 18:50:48', null),
        (2047437118661328896, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2047437116010528768, '2025-06-09 18:51:22', null),
        (2047437118728437760, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2047437116010528768, '2025-06-09 18:51:45', null),
        (2047437118791352320, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2047437116010528768, '2025-06-09 18:52:10', null),
        (2047437118858461184, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:53:07', null),
        (2047437118921375744, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:53:45', null),
        (2047437118988484608, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:54:11', null),
        (2047437119055593472, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:54:45', null),
        (2047437119118508032, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:55:08', null),
        (2047437119185616896, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:55:35', null),
        (2047437119252725760, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 18:58:16', null),
        (2047437119319834624, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2047437116077637632, '2025-06-09 19:01:22', null),
        (2047437119386943488, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2047437116211855360, '2025-06-09 19:02:21', null),
        (2047437119454052352, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2047437116211855360, '2025-06-09 19:02:50', null),
        (2047437119521161216, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2047437116274769920, '2025-06-09 19:03:13', null),
        (2047437119584075776, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2047437116274769920, '2025-06-09 19:03:40', null),
        (2047437119651184640, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:session:delete', 1, 0, 1, '', null, 2047437116341878784, '2025-06-09 19:04:52', null);

insert into sys_role  (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2047437119714099200, '测试', 1, 1, null, '2025-05-26 17:13:45', null);

insert into sys_role_menu  (id, role_id, menu_id)
values (2047437119781208064, 2047437119714099200, 2047437114622214144),
        (2047437119844122624, 2047437119714099200, 2047437114689323008),
        (2047437119911231488, 2047437119714099200, 2047437114756431872),
        (2047437119974146048, 2047437119714099200, 2047437114819346432);

insert into sys_user  (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values (2047437120041254912, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', '0x24326224313224387932654E7563583139566A6D5A33745968424C634F', 'admin@example.com', 1, 1, 1, 1, null, null, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 2047437114580271104, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

insert into sys_user_role  (id, user_id, role_id)
values (2047437120108363776, 2047437120041254912, 2047437119714099200);

insert into sys_data_scope  (id, name, status, created_time, updated_time)
values (2047437120175472640, '测试部门数据权限', 1, '2025-06-09 16:53:29', null),
        (2047437120242581504, '测试部门及以下数据权限', 1, '2025-06-09 16:53:40', null);

insert into sys_data_rule  (id, name, model, "column", operator, expression, "value", created_time, updated_time)
values (2047437120309690368, '部门名称等于测试', '部门', 'name', 1, 0, '测试', '2025-06-09 16:56:06', null),
        (2047437120376799232, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', '2025-06-09 17:16:14', null);

insert into sys_data_scope_rule  (id, data_scope_id, data_rule_id)
values (2047437120443908096, 2047437120175472640, 2047437120309690368),
        (2047437120511016960, 2047437120242581504, 2047437120309690368),
        (2047437120578125824, 2047437120242581504, 2047437120376799232);
