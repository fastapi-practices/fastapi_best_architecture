insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2047437120000000100, '测试', 0, null, null, null, 1, 0, null, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
-- 顶级菜单
(2047437120000000101, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000102, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000103, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000104, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000105, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000106, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437120000000107, '个人中心', 'Profile', 'profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, now(), null),
-- 一级子菜单
(2047437120000000108, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2047437120000000101, now(), null),
(2047437120000000109, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2047437120000000101, now(), null),
(2047437120000000110, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000111, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000112, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000113, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000114, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000115, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000116, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000117, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000118, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2047437120000000102, now(), null),
(2047437120000000119, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 2047437120000000103, now(), null),
(2047437120000000120, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 2047437120000000103, now(), null),
(2047437120000000121, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2047437120000000104, now(), null),
(2047437120000000122, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2047437120000000104, now(), null),
(2047437120000000123, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2047437120000000105, now(), null),
(2047437120000000124, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2047437120000000105, now(), null),
(2047437120000000125, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2047437120000000105, now(), null),
(2047437120000000126, '文档', 'Document', 'document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2047437120000000106, now(), null),
(2047437120000000127, 'Github', 'Github', 'github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2047437120000000106, now(), null),
(2047437120000000128, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2047437120000000106, now(), null),
-- 二级子菜单
(2047437120000000129, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2047437120000000114, now(), null),
(2047437120000000130, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2047437120000000114, now(), null),
-- 按钮权限
(2047437120000000201, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2047437120000000110, now(), null),
(2047437120000000202, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2047437120000000110, now(), null),
(2047437120000000203, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2047437120000000110, now(), null),
(2047437120000000204, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2047437120000000111, now(), null),
(2047437120000000205, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2047437120000000112, now(), null),
(2047437120000000206, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2047437120000000112, now(), null),
(2047437120000000207, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2047437120000000112, now(), null),
(2047437120000000208, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2047437120000000113, now(), null),
(2047437120000000209, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2047437120000000113, now(), null),
(2047437120000000210, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2047437120000000113, now(), null),
(2047437120000000211, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2047437120000000129, now(), null),
(2047437120000000212, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2047437120000000129, now(), null),
(2047437120000000213, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2047437120000000129, now(), null),
(2047437120000000214, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2047437120000000129, now(), null),
(2047437120000000215, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2047437120000000130, now(), null),
(2047437120000000216, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2047437120000000130, now(), null),
(2047437120000000217, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2047437120000000130, now(), null),
(2047437120000000218, '安装插件', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2047437120000000115, now(), null),
(2047437120000000219, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2047437120000000115, now(), null),
(2047437120000000220, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2047437120000000115, now(), null),
(2047437120000000221, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2047437120000000116, now(), null),
(2047437120000000222, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2047437120000000116, now(), null),
(2047437120000000223, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2047437120000000116, now(), null),
(2047437120000000224, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000225, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000226, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000227, '新增', 'AddSysDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000228, '修改', 'EditSysDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000229, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2047437120000000117, now(), null),
(2047437120000000230, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2047437120000000118, now(), null),
(2047437120000000231, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2047437120000000118, now(), null),
(2047437120000000232, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2047437120000000118, now(), null),
(2047437120000000233, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000234, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000235, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000236, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000237, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000238, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000239, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000240, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2047437120000000119, now(), null),
(2047437120000000241, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2047437120000000121, now(), null),
(2047437120000000242, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2047437120000000121, now(), null),
(2047437120000000243, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2047437120000000122, now(), null),
(2047437120000000244, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2047437120000000122, now(), null),
(2047437120000000245, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:session:delete', 1, 0, 1, '', null, 2047437120000000123, now(), null);

insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2047437120000000300, '测试', 1, 1, null, now(), null);

insert into sys_role_menu (id, role_id, menu_id)
values
(2047437120000000301, 2047437120000000300, 2047437120000000101),
(2047437120000000302, 2047437120000000300, 2047437120000000102),
(2047437120000000303, 2047437120000000300, 2047437120000000103),
(2047437120000000304, 2047437120000000300, 2047437120000000104);

insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values (2047437120000000400, gen_random_uuid(), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', decode('24326224313224387932654E7563583139566A6D5A33745968424C634F', 'hex'), 'admin@example.com', 1, 1, 1, 1, null, null, now(), now(), 2047437120000000100, now(), null);

insert into sys_user_role (id, user_id, role_id)
values (2047437120000000401, 2047437120000000400, 2047437120000000300);

insert into sys_data_scope (id, name, status, created_time, updated_time)
values
(2047437120000000500, '测试部门数据权限', 1, now(), null),
(2047437120000000501, '测试部门及以下数据权限', 1, now(), null);

insert into sys_data_rule (id, name, model, "column", operator, expression, "value", created_time, updated_time)
values
(2047437120000000600, '部门名称等于测试', '部门', 'name', 1, 0, '测试', now(), null),
(2047437120000000601, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', now(), null);

insert into sys_data_scope_rule (id, data_scope_id, data_rule_id)
values
(2047437120000000700, 2047437120000000500, 2047437120000000600),
(2047437120000000701, 2047437120000000501, 2047437120000000600),
(2047437120000000702, 2047437120000000501, 2047437120000000601);
