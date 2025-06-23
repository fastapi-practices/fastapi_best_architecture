-- ----------------------------
-- 初始化部门数据
-- ----------------------------
insert into sys_dept (id, name, sort, leader, phone, email, status, del_flag, parent_id, created_time, updated_time)
values (2047437108473364480, '测试', 0, null, null, null, 1, 0, null, now(), null);

-- ----------------------------
-- 初始化菜单数据
-- ----------------------------
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
-- 顶级菜单
(2047437108502724608, '概览', 'Dashboard', 'dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437108569833472, '系统管理', 'System', 'system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437108632748032, '系统自动化', 'Automation', 'automation', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437108699856896, '日志管理', 'Log', 'log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437108766965760, '系统监控', 'Monitor', 'monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437108834074624, '项目', 'Project', 'fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, now(), null),
(2047437110427910144, '个人中心', 'Profile', 'profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, now(), null),
-- 一级子菜单
(2047437108901183488, '分析页', 'Analytics', 'analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 2047437108502724608, now(), null),
(2047437108968292352, '工作台', 'Workspace', 'workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 2047437108502724608, now(), null),
(2047437109236727808, '部门管理', 'SysDept', 'sys-dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109303836672, '用户管理', 'SysUser', 'sys-user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109366751232, '角色管理', 'SysRole', 'sys-role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109429665792, '菜单管理', 'SysMenu', 'sys-menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109496774656, '数据权限', 'SysDataPermission', 'sys-data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109698101248, '插件管理', 'SysPlugin', 'sys-plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109761015808, '参数管理', 'SysConfig', 'sys-config', 9, 'codicon:symbol-parameter', 1, '/system/config/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109828124672, '字典管理', 'SysDict', 'sys-dict', 10, 'fluent-mdl2:dictionary', 1, '/system/dict/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109891039232, '通知公告', 'SysNotice', 'sys-notice', 11, 'fe:notice-push', 1, '/system/notice/index', null, 1, 1, 1, '', null, 2047437108569833472, now(), null),
(2047437109958148096, '代码生成', 'CodeGenerator', 'code-generator', 1, 'tabler:code', 1, '/automation/code-generator/index', null, 1, 1, 1, '', null, 2047437108632748032, now(), null),
(2047437110025256960, '任务调度', 'Scheduler', 'scheduler', 2, 'ix:scheduler', 1, '/automation/scheduler/index', null, 1, 1, 1, '', null, 2047437108632748032, now(), null),
(2047437110092365824, '登录日志', 'LoginLog', 'login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 2047437108699856896, now(), null),
(2047437110159474688, '操作日志', 'OperaLog', 'opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 2047437108699856896, now(), null),
(2047437110226583552, '在线用户', 'Online', 'online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 2047437108766965760, now(), null),
(2047437110293692416, 'Redis', 'Redis', 'redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 2047437108766965760, now(), null),
(2047437110360801280, 'Server', 'Server', 'server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 2047437108766965760, now(), null),
(2047437109035401216, '文档', 'Document', 'document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 2047437108834074624, now(), null),
(2047437109102510080, 'Github', 'Github', 'github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi_best_architecture', null, 2047437108834074624, now(), null),
(2047437109169618944, 'Apifox', 'Apifox', 'apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 2047437108834074624, now(), null),
-- 二级子菜单
(2047437109563883520, '数据范围', 'SysDataScope', 'sys-data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 2047437109496774656, now(), null),
(2047437109630992384, '数据规则', 'SysDataRule', 'sys-data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 2047437109496774656, now(), null),
-- 按钮权限
(2047437110494801920, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 2047437109236727808, now(), null),
(2047437110561910784, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 2047437109236727808, now(), null),
(2047437110629019648, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 2047437109236727808, now(), null),
(2047437110696128512, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 2047437109303836672, now(), null),
(2047437110763237376, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 2047437109366751232, now(), null),
(2047437110830346240, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 2047437109366751232, now(), null),
(2047437110897455104, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 2047437109366751232, now(), null),
(2047437110964563968, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 2047437109366751232, now(), null),
(2047437111031672832, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 2047437109366751232, now(), null),
(2047437111098781696, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 2047437109429665792, now(), null),
(2047437111165890560, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 2047437109429665792, now(), null),
(2047437111232999424, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 2047437109429665792, now(), null),
(2047437111300108288, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 2047437109563883520, now(), null),
(2047437111367217152, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 2047437109563883520, now(), null),
(2047437111434326016, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 2047437109563883520, now(), null),
(2047437111501434880, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 2047437109563883520, now(), null),
(2047437111568543744, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 2047437109630992384, now(), null),
(2047437111635652608, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 2047437109630992384, now(), null),
(2047437111702761472, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 2047437109630992384, now(), null),
(2047437111769870336, '安装插件', 'InstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:install', 1, 0, 1, '', null, 2047437109698101248, now(), null),
(2047437111836979200, '卸载', 'UninstallSysPlugin', null, 0, null, 2, null, 'sys:plugin:uninstall', 1, 0, 1, '', null, 2047437109698101248, now(), null),
(2047437111904088064, '修改', 'EditSysPlugin', null, 0, null, 2, null, 'sys:plugin:edit', 1, 0, 1, '', null, 2047437109698101248, now(), null),
(2047437111971196928, '新增', 'AddSysConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2047437109761015808, now(), null),
(2047437112038305792, '修改', 'EditSysConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2047437109761015808, now(), null),
(2047437112105414656, '删除', 'DeleteSysConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2047437109761015808, now(), null),
(2047437112172523520, '新增类型', 'AddSysDictType', null, 0, null, 2, null, 'dict:type:add', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112239632384, '修改类型', 'EditSysDictType', null, 0, null, 2, null, 'dict:type:edit', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112306741248, '删除类型', 'DeleteSysDictType', null, 0, null, 2, null, 'dict:type:del', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112373850112, '新增', 'AddSysDictData', null, 0, null, 2, null, 'dict:data:add', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112440958976, '修改', 'EditSysDictData', null, 0, null, 2, null, 'dict:data:edit', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112508067840, '删除', 'DeleteSysDictData', null, 0, null, 2, null, 'dict:data:del', 1, 0, 1, '', null, 2047437109828124672, now(), null),
(2047437112575176704, '新增', 'AddSysNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, 2047437109891039232, now(), null),
(2047437112642285568, '修改', 'EditSysNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, 2047437109891039232, now(), null),
(2047437112709394432, '删除', 'DeleteSysNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, 2047437109891039232, now(), null),
(2047437112776503296, '新增业务', 'AddSysGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437112843612160, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437112910721024, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437112977829888, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437113044938752, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437113112047616, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437113179156480, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437113246265344, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2047437109958148096, now(), null),
(2047437113313374208, '删除', 'DeleteSysLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 2047437110092365824, now(), null),
(2047437113380483072, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 2047437110092365824, now(), null),
(2047437113447591936, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 2047437110159474688, now(), null),
(2047437113514700800, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 2047437110159474688, now(), null),
(2047437113581809664, '下线', 'KickSysToken', null, 0, null, 2, null, 'sys:session:delete', 1, 0, 1, '', null, 2047437110226583552, now(), null);

-- ----------------------------
-- 初始化角色数据
-- ----------------------------
insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (2047437113648918528, '测试', 1, 1, null, now(), null);

-- ----------------------------
-- 初始化角色菜单关系数据
-- ----------------------------
insert into sys_role_menu (id, role_id, menu_id)
values
(2047437113716027392, 2047437113648918528, 2047437108502724608),
(2047437113783136256, 2047437113648918528, 2047437108569833472),
(2047437113850245120, 2047437113648918528, 2047437108632748032),
(2047437113917353984, 2047437113648918528, 2047437108699856896);

-- ----------------------------
-- 初始化用户数据
-- ----------------------------
insert into sys_user (id, uuid, username, nickname, password, salt, email, is_superuser, is_staff, status, is_multi_login, avatar, phone, join_time, last_login_time, dept_id, created_time, updated_time)
values (2047437113984462848, uuid(), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', unhex('24326224313224387932654E7563583139566A6D5A33745968424C634F'), 'admin@example.com', 1, 1, 1, 1, null, null, now(), now(), 2047437108473364480, now(), null);

-- ----------------------------
-- 初始化用户角色关系数据
-- ----------------------------
insert into sys_user_role (id, user_id, role_id)
values (2047437114051571712, 2047437113984462848, 2047437113648918528);

-- ----------------------------
-- 初始化数据范围数据
-- ----------------------------
insert into sys_data_scope (id, name, status, created_time, updated_time)
values
(2047437114118680576, '测试部门数据权限', 1, now(), null),
(2047437114185789440, '测试部门及以下数据权限', 1, now(), null);

-- ----------------------------
-- 初始化数据规则数据
-- ----------------------------
insert into sys_data_rule (id, name, model, `column`, operator, expression, `value`, created_time, updated_time)
values
(2047437114252898304, '部门名称等于测试', '部门', 'name', 1, 0, '测试', now(), null),
(2047437114320007168, '父部门 ID 等于 1', '部门', 'parent_id', 0, 0, '1', now(), null);

-- ----------------------------
-- 初始化数据范围规则关系数据
-- ----------------------------
insert into sys_data_scope_rule (id, data_scope_id, data_rule_id)
values
(2047437114387116032, 2047437114118680576, 2047437114252898304),
(2047437114454224896, 2047437114185789440, 2047437114252898304),
(2047437114521333760, 2047437114185789440, 2047437114320007168);

-- ----------------------------
-- 初始化数据字典类型
-- ----------------------------
insert into sys_dict_type (id, name, code, status, remark, created_time, updated_time)
values
(2047437114588442624, '通用状态', 'sys_status', 1, '系统通用状态：启用/停用', now(), null),
(2047437114655551488, '菜单类型', 'sys_menu_type', 1, '系统菜单类型', now(), null),
(2047437114722660352, '登录日志状态', 'sys_login_status', 1, '用户登录日志状态', now(), null),
(2047437114789769216, '数据规则运算符', 'sys_data_rule_operator', 1, '数据权限规则运算符', now(), null),
(2047437114856878080, '数据规则表达式', 'sys_data_rule_expression', 1, '数据权限规则表达式', now(), null),
(2047437114923986944, '前端参数配置', 'sys_frontend_config', 1, '前端参数配置类型', now(), null),
(2047437114991095808, '过滤数据权限', 'sys_data_permission', 1, '数据权限过滤类型', now(), null),
(2047437115058204672, '菜单显示', 'sys_menu_display', 1, '菜单是否显示', now(), null),
(2047437115125313536, '菜单缓存', 'sys_menu_cache', 1, '菜单是否缓存', now(), null);

-- ----------------------------
-- 初始化数据字典数据
-- ----------------------------
insert into sys_dict_data (id, label, value, sort, status, remark, type_id, created_time, updated_time)
values
(2047437115192422400, '停用', '0', 1, 1, '系统停用状态', 2047437114588442624, now(), null),
(2047437115259531264, '正常', '1', 2, 1, '系统正常状态', 2047437114588442624, now(), null),
(2047437115326640128, '目录', '0', 1, 1, '菜单目录类型', 2047437114655551488, now(), null),
(2047437115393748992, '菜单', '1', 2, 1, '普通菜单类型', 2047437114655551488, now(), null),
(2047437115460857856, '按钮', '2', 3, 1, '按钮权限类型', 2047437114655551488, now(), null),
(2047437115527966720, '内嵌', '3', 4, 1, '内嵌页面类型', 2047437114655551488, now(), null),
(2047437115595075584, '外链', '4', 5, 1, '外部链接类型', 2047437114655551488, now(), null),
(2047437115662184448, '失败', '0', 1, 1, '登录失败状态', 2047437114722660352, now(), null),
(2047437115729293312, '成功', '1', 2, 1, '登录成功状态', 2047437114722660352, now(), null),
(2047437115796402176, 'AND', '0', 1, 1, '逻辑与运算符', 2047437114789769216, now(), null),
(2047437115863511040, 'OR', '1', 2, 1, '逻辑或运算符', 2047437114789769216, now(), null),
(2047437115930619904, '等于(==)', '0', 1, 1, '等于比较表达式', 2047437114856878080, now(), null),
(2047437115997728768, '不等于(!=)', '1', 2, 1, '不等于比较表达式', 2047437114856878080, now(), null),
(2047437116064837632, '大于(>)', '2', 3, 1, '大于比较表达式', 2047437114856878080, now(), null),
(2047437116131946496, '大于等于(>=)', '3', 4, 1, '大于等于比较表达式', 2047437114856878080, now(), null),
(2047437116199055360, '小于(<)', '4', 5, 1, '小于比较表达式', 2047437114856878080, now(), null),
(2047437116266164224, '小于等于(<=)', '5', 6, 1, '小于等于比较表达式', 2047437114856878080, now(), null),
(2047437116333273088, '包含(in)', '6', 7, 1, '包含表达式', 2047437114856878080, now(), null),
(2047437116400381952, '不包含(not in)', '7', 8, 1, '不包含表达式', 2047437114856878080, now(), null),
(2047437116467490816, '否', '0', 1, 1, '不是前端参数配置', 2047437114923986944, now(), null),
(2047437116534599680, '是', '1', 2, 1, '是前端参数配置', 2047437114923986944, now(), null),
(2047437116601708544, '否', '0', 1, 1, '不进行数据权限过滤', 2047437114991095808, now(), null),
(2047437116668817408, '是', '1', 2, 1, '进行数据权限过滤', 2047437114991095808, now(), null),
(2047437116735926272, '隐藏', '0', 1, 1, '菜单隐藏', 2047437115058204672, now(), null),
(2047437116803035136, '显示', '1', 2, 1, '菜单显示', 2047437115058204672, now(), null),
(2047437116870144000, '不缓存', '0', 1, 1, '菜单不缓存', 2047437115125313536, now(), null),
(2047437116937252864, '缓存', '1', 2, 1, '菜单缓存', 2047437115125313536, now(), null);