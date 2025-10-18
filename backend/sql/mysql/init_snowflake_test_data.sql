insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2048601258595581952, '测试', 0, null, null, null, 1, false, null, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
(2049629108245233664, 'page.dashboard.title', 'Dashboard', '/dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108245233665, 'page.dashboard.analytics', 'Analytics', '/analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2049629108245233664, '2025-06-26 20:29:06', null),
(2049629108245233666, 'page.dashboard.workspace', 'Workspace', '/workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2049629108245233664, '2025-06-26 20:29:06', null),
(2049629108245233667, 'page.menu.system', 'System', '/system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108245233668, 'page.menu.sysDept', 'SysDept', '/system/dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108245233669, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2049629108245233668, '2025-06-26 20:29:06', null),
(2049629108245233670, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2049629108245233668, '2025-06-26 20:29:06', null),
(2049629108245233671, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2049629108245233668, '2025-06-26 20:29:06', null),
(2049629108245233672, 'page.menu.sysUser', 'SysUser', '/system/user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108245233673, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2049629108245233672, '2025-06-26 20:29:06', null),
(2049629108245233674, 'page.menu.sysRole', 'SysRole', '/system/role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108245233675, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2049629108245233674, '2025-06-26 20:29:06', null),
(2049629108245233676, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2049629108245233674, '2025-06-26 20:29:06', null),
(2049629108245233677, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 2049629108245233674, '2025-06-26 20:29:06', null),
(2049629108245233678, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 2049629108245233674, '2025-06-26 20:29:06', null),
(2049629108245233679, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2049629108245233674, '2025-06-26 20:29:06', null),
(2049629108245233680, 'page.menu.sysMenu', 'SysMenu', '/system/menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108245233681, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2049629108245233680, '2025-06-26 20:29:06', null),
(2049629108245233682, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2049629108245233680, '2025-06-26 20:29:06', null),
(2049629108249427968, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2049629108245233680, '2025-06-26 20:29:06', null),
(2049629108249427969, 'page.menu.sysDataPermission', 'SysDataPermission', '/system/data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108249427970, 'page.menu.sysDataScope', 'SysDataScope', '/system/data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2049629108249427969, '2025-06-26 20:29:06', '2025-06-26 20:37:26'),
(2049629108249427971, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2049629108249427970, '2025-06-26 20:29:06', null),
(2049629108249427972, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2049629108249427970, '2025-06-26 20:29:06', null),
(2049629108249427973, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2049629108249427970, '2025-06-26 20:29:06', null),
(2049629108249427974, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2049629108249427970, '2025-06-26 20:29:06', null),
(2049629108249427975, 'page.menu.sysDataRule', 'SysDataRule', '/system/data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2049629108249427969, '2025-06-26 20:29:06', '2025-06-26 20:37:40'),
(2049629108249427976, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2049629108249427975, '2025-06-26 20:29:06', null),
(2049629108249427977, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2049629108249427975, '2025-06-26 20:29:06', null),
(2049629108249427978, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2049629108249427975, '2025-06-26 20:29:06', null),
(2049629108249427979, 'page.menu.sysPlugin', 'SysPlugin', '/system/plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', null),
(2049629108249427980, '安装', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2049629108249427979, '2025-06-26 20:29:06', null),
(2049629108249427981, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2049629108249427979, '2025-06-26 20:29:06', null),
(2049629108249427982, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2049629108249427979, '2025-06-26 20:29:06', null),
(2049629108249427983, 'page.menu.scheduler', 'Scheduler', '/scheduler', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108249427984, 'page.menu.schedulerManage', 'SchedulerManage', '/scheduler/manage', 1, 'ix:scheduler', 1, '/scheduler/manage/index', null, 1, 1, 1, '', null, 2049629108249427983, '2025-06-26 20:29:06', null),
(2049629108249427985, 'page.menu.schedulerRecord', 'SchedulerRecord', '/scheduler/record', 2, 'ix:scheduler', 1, '/scheduler/record/index', null, 1, 1, 1, '', null, 2049629108249427983, '2025-06-26 20:29:06', null),
(2049629108249427986, 'page.menu.log', 'Log', '/log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108249427987, 'page.menu.login', 'LoginLog', '/log/login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2049629108249427986, '2025-06-26 20:29:06', null),
(2049629108249427988, '删除', 'DeleteLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2049629108249427987, '2025-06-26 20:29:06', null),
(2049629108249427989, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2049629108249427987, '2025-06-26 20:29:06', null),
(2049629108249427990, 'page.menu.opera', 'OperaLog', '/log/opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2049629108249427986, '2025-06-26 20:29:06', null),
(2049629108249427991, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2049629108249427990, '2025-06-26 20:29:06', null),
(2049629108253622272, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2049629108249427990, '2025-06-26 20:29:06', null),
(2049629108253622273, 'page.menu.monitor', 'Monitor', '/monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108253622274, 'page.menu.online', 'Online', '/log/online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2049629108253622273, '2025-06-26 20:29:06', null),
(2049629108253622276, 'page.menu.redis', 'Redis', '/monitor/redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2049629108253622273, '2025-06-26 20:29:06', null),
(2049629108253622277, 'page.menu.server', 'Server', '/monitor/server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2049629108253622273, '2025-06-26 20:29:06', null),
(2049629108253622278, '项目', 'Project', '/fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108253622279, '文档', 'Document', '/fba/document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2049629108253622278, '2025-06-26 20:29:06', null),
(2049629108253622280, 'Github', 'Github', '/fba/github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2049629108253622278, '2025-06-26 20:29:06', null),
(2049629108253622281, 'Apifox', 'Apifox', '/fba/apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2049629108253622278, '2025-06-26 20:29:06', null),
(2049629108253622282, 'page.menu.profile', 'Profile', '/profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, '2025-06-26 20:29:06', null),
(2049629108253622283, 'config.menu', 'PluginConfig', '/plugins/config', 7, 'codicon:symbol-parameter', 1, '/plugins/config/views/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', '2025-06-26 20:34:51'),
(2049629108253622284, '新增', 'AddConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2049629108253622283, '2025-06-26 20:29:06', null),
(2049629108253622285, '修改', 'EditConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2049629108253622283, '2025-06-26 20:29:06', null),
(2049629108253622286, '删除', 'DeleteConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2049629108253622283, '2025-06-26 20:29:06', null),
(2049629108253622287, 'dict.menu', 'PluginDict', '/plugins/dict', 8, 'fluent-mdl2:dictionary', 1, '/plugins/dict/views/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', '2025-06-26 20:35:07'),
(2049629108253622288, '新增类型', 'AddDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108253622289, '修改类型', 'EditDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108253622290, '删除类型', 'DeleteDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108253622291, '新增数据', 'AddDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108253622292, '修改数据', 'EditDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108253622293, '删除数据', 'DeleteDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2049629108253622287, '2025-06-26 20:29:06', null),
(2049629108257816576, 'notice.menu', 'PluginNotice', '/plugins/notice', 9, 'fe:notice-push', 1, '/plugins/notice/views/index', null, 1, 1, 1, '', null, 2049629108245233667, '2025-06-26 20:29:06', '2025-06-26 20:35:14'),
(2049629108257816577, '新增', 'AddNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2049629108257816576, '2025-06-26 20:29:06', null),
(2049629108257816578, '修改', 'EditNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2049629108257816576, '2025-06-26 20:29:06', null),
(2049629108257816579, '删除', 'DeleteNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2049629108257816576, '2025-06-26 20:29:06', null),
(2049629108257816580, 'code_generator.menu', 'PluginCodeGenerator', '/plugins/code-generator', 10, 'tabler:code', 1, '/plugins/code_generator/views/index', null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', '2025-06-26 20:35:25'),
(2049629108257816581, '新增业务', 'AddGenCodeBusiness', '', 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', '2025-06-26 20:45:16'),
(2049629108257816582, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816583, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816584, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816585, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816586, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816587, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null),
(2049629108257816588, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2049629108257816580, '2025-06-26 20:29:06', null);

insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2048601263515500544, '测试', 1, true, null, now(), null);

insert into sys_role_menu (id, role_id, menu_id)
values
(2048601263578415104, 2048601263515500544, 2049629108245233664),
(2048601263641329664, 2048601263515500544, 2049629108245233665),
(2048601263708438528, 2048601263515500544, 2049629108245233666),
(2048601263775547392, 2048601263515500544, 2049629108253622282);

insert into sys_user (id, uuid, username, nickname, password, salt, email, status, is_superuser, is_staff, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values
(2048601263834267648, uuid(), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', unhex('24326224313224387932654E7563583139566A6D5A33745968424C634F'), 'admin@example.com', 1, true, true, true, null, null, now(), now(), 2048601258595581952, now(), null),
(2049946297615646720, uuid(), 'test', '用户66666', '$2b$12$BMiXsNQAgTx7aNc7kVgnwedXGyUxPEHRnJMFbiikbqHgVoT3y14Za', unhex('24326224313224424D6958734E514167547837614E63376B56676E7765'), 'test@example.com', 1, false, false, false, null, null, now(), now(), 2048601258595581952, now(), null);

insert into sys_user_role (id, user_id, role_id)
values
(2048601263838461952, 2048601263834267648, 2048601263515500544),
(2049946493732913152, 2049946297615646720, 2048601263515500544);

insert into sys_data_scope (id, name, status, created_time, updated_time)
values
(2048601263901376512, '测试部门数据权限', 1, now(), null),
(2048601263968485376, '测试部门及以下数据权限', 1, now(), null);

insert into sys_data_rule (id, name, model, `column`, operator, expression, `value`, created_time, updated_time)
values
(2048601264035594240, '部门名称等于测试', '部门', 'name', 1, 0, '测试', now(), null),
(2048601264102703104, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', now(), null);

insert into sys_data_scope_rule (id, data_scope_id, data_rule_id)
values
(2048601264169811968, 2048601263901376512, 2048601264035594240),
(2048601264236920832, 2048601263968485376, 2048601264035594240),
(2048601264299835392, 2048601263968485376, 2048601264102703104);
