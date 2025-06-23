insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2048601258595581952, '测试', 0, null, null, null, 1, 0, null, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
-- 顶级菜单
(2048601258599776256, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258666885120, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258729799680, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258796908544, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258864017408, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258931126272, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2048601258998235136, '个人中心', 'Profile', 'profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, now(), null),
-- 一级子菜单
(2048601259061149696, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2048601258599776256, now(), null),
(2048601259128258560, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2048601258599776256, now(), null),
(2048601259191173120, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259258281984, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259325390848, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259388305408, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259451219968, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259518328832, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259585437696, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259652546560, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259715461120, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2048601258666885120, now(), null),
(2048601259778375680, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 2048601258729799680, now(), null),
(2048601259845484544, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 2048601258729799680, now(), null),
(2048601259908399104, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2048601258796908544, now(), null),
(2048601259975507968, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2048601258796908544, now(), null),
(2048601260042616832, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2048601258864017408, now(), null),
(2048601260109725696, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2048601258864017408, now(), null),
(2048601260176834560, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2048601258864017408, now(), null),
(2048601260239749120, '文档', 'Document', 'document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2048601258931126272, now(), null),
(2048601260302663680, 'Github', 'Github', 'github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2048601258931126272, now(), null),
(2048601260369772544, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2048601258931126272, now(), null),
-- 二级子菜单
(2048601260436881408, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2048601259451219968, now(), null),
(2048601260503990272, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2048601259451219968, now(), null),
-- 按钮权限
(2048601260571099136, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2048601259191173120, now(), null),
(2048601260638208000, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2048601259191173120, now(), null),
(2048601260705316864, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2048601259191173120, now(), null),
(2048601260772425728, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2048601259258281984, now(), null),
(2048601260839534592, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2048601259325390848, now(), null),
(2048601260906643456, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2048601259325390848, now(), null),
(2048601260969558016, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2048601259325390848, now(), null),
(2048601261032472576, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2048601259388305408, now(), null),
(2048601261095387136, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2048601259388305408, now(), null),
(2048601261162496000, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2048601259388305408, now(), null),
(2048601261229604864, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2048601260436881408, now(), null),
(2048601261296713728, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2048601260436881408, now(), null),
(2048601261359628288, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2048601260436881408, now(), null),
(2048601261426737152, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2048601260436881408, now(), null),
(2048601261489651712, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2048601260503990272, now(), null),
(2048601261552566272, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2048601260503990272, now(), null),
(2048601261619675136, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2048601260503990272, now(), null),
(2048601261686784000, '安装插件', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2048601259518328832, now(), null),
(2048601261753892864, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2048601259518328832, now(), null),
(2048601261816807424, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2048601259518328832, now(), null),
(2048601261883916288, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2048601259585437696, now(), null),
(2048601261946830848, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2048601259585437696, now(), null),
(2048601262013939712, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2048601259585437696, now(), null),
(2048601262076854272, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262143963136, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262211072000, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262273986560, '新增', 'AddSysDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262341095424, '修改', 'EditSysDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262404009984, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2048601259652546560, now(), null),
(2048601262471118848, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2048601259715461120, now(), null),
(2048601262538227712, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2048601259715461120, now(), null),
(2048601262601142272, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2048601259715461120, now(), null),
(2048601262664056832, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601262731165696, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601262798274560, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601262861189120, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601262924103680, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601262991212544, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601263058321408, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601263121235968, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2048601259778375680, now(), null),
(2048601263184150528, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2048601259908399104, now(), null),
(2048601263251259392, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2048601259908399104, now(), null),
(2048601263314173952, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2048601259975507968, now(), null),
(2048601263381282816, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2048601259975507968, now(), null),
(2048601263448391680, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:session:delete', 1, 0, 1, '', null, 2048601260042616832, now(), null);

insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2048601263515500544, '测试', 1, 1, null, now(), null);

insert into sys_role_menu (id, role_id, menu_id)
values
(2048601263578415104, 2048601263515500544, 2048601258599776256),
(2048601263641329664, 2048601263515500544, 2048601258666885120),
(2048601263708438528, 2048601263515500544, 2048601258729799680),
(2048601263775547392, 2048601263515500544, 2048601258796908544);

insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values (2048601263834267648, uuid(), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', unhex('24326224313224387932654E7563583139566A6D5A33745968424C634F'), 'admin@example.com', 1, 1, 1, 1, null, null, now(), now(), 2048601258595581952, now(), null);

insert into sys_user_role (id, user_id, role_id)
values (2048601263838461952, 2048601263834267648, 2048601263515500544);

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
