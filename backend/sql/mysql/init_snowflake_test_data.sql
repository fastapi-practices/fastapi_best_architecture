insert into sys_dept  (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2047437108473364480, '测试', 0, null, null, null, 1, 0, null, '2025-05-26 17:13:45', null);

insert into sys_menu  (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (2047437108502724608, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:26:18', null),
        (2047437108569833472, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:30:01', null),
        (2047437108632748032, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:31:41', null),
        (2047437108699856896, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:32:34', null),
        (2047437108766965760, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:33:29', null),
        (2047437108834074624, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, '2025-06-09 17:35:41', null),
        (2047437108901183488, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2047437108502724608, '2025-06-09 17:54:29', null),
        (2047437108968292352, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2047437108502724608, '2025-06-09 17:57:09', null),
        (2047437109035401216, '文档', 'Document', 'document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2047437108834074624, '2025-06-09 17:59:44', null),
        (2047437109102510080, 'Github', 'Github', 'github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2047437108834074624, '2025-06-09 18:00:50', null),
        (2047437109169618944, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2047437108834074624, '2025-06-09 18:01:39', null),
        (2047437109236727808, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:03:17', null),
        (2047437109303836672, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:03:54', null),
        (2047437109366751232, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:04:47', null),
        (2047437109429665792, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:05:31', null),
        (2047437109496774656, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:07:04', null),
        (2047437109563883520, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2047437109496774656, '2025-06-09 18:07:46', null),
        (2047437109630992384, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2047437109496774656, '2025-06-09 18:08:22', null),
        (2047437109698101248, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:09:12', null),
        (2047437109761015808, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:10:20', null),
        (2047437109828124672, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:11:10', null),
        (2047437109891039232, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2047437108569833472, '2025-06-09 18:11:38', null),
        (2047437109958148096, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 2047437108632748032, '2025-06-09 18:12:38', null),
        (2047437110025256960, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 2047437108632748032, '2025-06-09 18:13:19', null),
        (2047437110092365824, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2047437108699856896, '2025-06-09 18:14:35', null),
        (2047437110159474688, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2047437108699856896, '2025-06-09 18:15:26', null),
        (2047437110226583552, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2047437108766965760, '2025-06-09 18:17:12', null),
        (2047437110293692416, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2047437108766965760, '2025-06-09 18:17:42', null),
        (2047437110360801280, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2047437108766965760, '2025-06-09 18:18:12', null),
        (2047437110427910144, '个人中心', 'Profile', 'profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, '2025-06-09 18:18:12', null),
        (2047437110495019008, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2047437109236727808, '2025-06-09 18:21:17', null),
        (2047437110562127872, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2047437109236727808, '2025-06-09 18:22:01', null),
        (2047437110629236736, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2047437109236727808, '2025-06-09 18:22:39', null),
        (2047437110696345600, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2047437109303836672, '2025-06-09 18:24:09', null),
        (2047437110759260160, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2047437109366751232, '2025-06-09 18:25:08', null),
        (2047437110822174720, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2047437109366751232, '2025-06-09 18:26:30', null),
        (2047437110889283584, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 2047437109366751232, '2025-06-09 18:27:24', null),
        (2047437110956392448, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 2047437109366751232, '2025-06-09 18:28:25', null),
        (2047437111023501312, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2047437109366751232, '2025-06-09 18:28:55', null),
        (2047437111090610176, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2047437109429665792, '2025-06-09 18:29:51', null),
        (2047437111157719040, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2047437109429665792, '2025-06-09 18:30:13', null),
        (2047437111220633600, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2047437109429665792, '2025-06-09 18:30:37', null),
        (2047437111287742464, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2047437109563883520, '2025-06-09 18:31:11', null),
        (2047437111350657024, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2047437109563883520, '2025-06-09 18:31:42', null),
        (2047437111417765888, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2047437109563883520, '2025-06-09 18:32:36', null),
        (2047437111484874752, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2047437109563883520, '2025-06-09 18:33:09', null),
        (2047437111551983616, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2047437109630992384, '2025-06-09 18:35:54', null),
        (2047437111614898176, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2047437109630992384, '2025-06-09 18:36:19', null),
        (2047437111682007040, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2047437109630992384, '2025-06-09 18:36:44', null),
        (2047437111749115904, '安装插件', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2047437109698101248, '2025-06-09 18:38:14', null),
        (2047437111816224768, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2047437109698101248, '2025-06-09 18:39:08', null),
        (2047437111883333632, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2047437109698101248, '2025-06-09 18:39:47', null),
        (2047437111950442496, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2047437109761015808, '2025-06-09 18:45:52', null),
        (2047437112017551360, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2047437109761015808, '2025-06-09 18:46:13', null),
        (2047437112084660224, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2047437109761015808, '2025-06-09 18:46:36', null),
        (2047437112151769088, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:48:17', null),
        (2047437112218877952, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:48:49', null),
        (2047437112285986816, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:49:23', null),
        (2047437112353095680, '新增', 'AddSysDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:50:01', null),
        (2047437112416010240, '修改', 'EditSysDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:50:26', null),
        (2047437112483119104, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2047437109828124672, '2025-06-09 18:50:48', null),
        (2047437112550227968, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2047437109891039232, '2025-06-09 18:51:22', null),
        (2047437112617336832, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2047437109891039232, '2025-06-09 18:51:45', null),
        (2047437112684445696, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2047437109891039232, '2025-06-09 18:52:10', null),
        (2047437112751554560, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:53:07', null),
        (2047437112822857728, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:53:45', null),
        (2047437112889966592, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:54:11', null),
        (2047437112957075456, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:54:45', null),
        (2047437113024184320, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:55:08', null),
        (2047437113091293184, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:55:35', null),
        (2047437113154207744, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 18:58:16', null),
        (2047437113221316608, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2047437109958148096, '2025-06-09 19:01:22', null),
        (2047437113284231168, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2047437110092365824, '2025-06-09 19:02:21', null),
        (2047437113351340032, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2047437110092365824, '2025-06-09 19:02:50', null),
        (2047437113418448896, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2047437110159474688, '2025-06-09 19:03:13', null),
        (2047437113485557760, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2047437110159474688, '2025-06-09 19:03:40', null),
        (2047437113552666624, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:session:delete', 1, 0, 1, '', null, 2047437110226583552, '2025-06-09 19:04:52', null);

insert into sys_role  (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2047437113619775488, '测试', 1, 1, null, '2025-05-26 17:13:45', null);

insert into sys_role_menu  (id, role_id, menu_id)
values (2047437113686884352, 2047437113619775488, 2047437108502724608),
        (2047437113753993216, 2047437113619775488, 2047437108569833472),
        (2047437113821102080, 2047437113619775488, 2047437108632748032),
        (2047437113888210944, 2047437113619775488, 2047437108699856896);

insert into sys_user  (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values (2047437113955319808, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', 0x24326224313224387932654E7563583139566A6D5A33745968424C634F, 'admin@example.com', 1, 1, 1, 1, null, null, '2023-06-26 17:13:45', '2024-11-18 13:53:57', 2047437108473364480, '2023-06-26 17:13:45', '2024-11-18 13:53:57');

insert into sys_user_role  (id, user_id, role_id)
values (2047437114022428672, 2047437113955319808, 2047437113619775488);

insert into sys_data_scope  (id, name, status, created_time, updated_time)
values (2047437114085343232, '测试部门数据权限', 1, '2025-06-09 16:53:29', null),
        (2047437114152452096, '测试部门及以下数据权限', 1, '2025-06-09 16:53:40', null);

insert into sys_data_rule  (id, name, model, `column`, operator, expression, `value`, created_time, updated_time)
values (2047437114219560960, '部门名称等于测试', '部门', 'name', 1, 0, '测试', '2025-06-09 16:56:06', null),
        (2047437114286669824, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', '2025-06-09 17:16:14', null);

insert into sys_data_scope_rule  (id, data_scope_id, data_rule_id)
values (2047437114353778688, 2047437114085343232, 2047437114219560960),
        (2047437114420887552, 2047437114152452096, 2047437114219560960),
        (2047437114487996416, 2047437114152452096, 2047437114286669824);
