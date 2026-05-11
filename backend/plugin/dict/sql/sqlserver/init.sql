INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES ('dict.menu', 'PluginDict', '/plugins/dict', 8, 'fluent-mdl2:dictionary', 1, '/plugins/dict/views/index', NULL, 1, 1, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'System'), GETDATE(), NULL);

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('新增类型', 'AddDictType', NULL, 0, NULL, 2, NULL, 'dict:type:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
('修改类型', 'EditDictType', NULL, 0, NULL, 2, NULL, 'dict:type:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
('删除类型', 'DeleteDictType', NULL, 0, NULL, 2, NULL, 'dict:type:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
('新增数据', 'AddDictData', NULL, 0, NULL, 2, NULL, 'dict:data:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
('修改数据', 'EditDictData', NULL, 0, NULL, 2, NULL, 'dict:data:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
('删除数据', 'DeleteDictData', NULL, 0, NULL, 2, NULL, 'dict:data:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL);

SET IDENTITY_INSERT sys_dict_type ON;
INSERT INTO sys_dict_type (id, name, code, remark, created_time, updated_time)
VALUES
(1, '通用状态', 'sys_status', '系统通用状态：1/0', GETDATE(), NULL),
(2, '通用开关', 'sys_choose', '系统通用开关：true/false', GETDATE(), NULL),
(3, '菜单类型', 'sys_menu_type', '系统菜单类型', GETDATE(), NULL),
(4, '登录状态', 'sys_login_status', '用户登录状态', GETDATE(), NULL),
(5, '数据规则运算符', 'sys_data_rule_operator', '数据权限规则运算符', GETDATE(), NULL),
(6, '数据规则表达式', 'sys_data_rule_expression', '数据权限规则表达式', GETDATE(), NULL),
(7, '前端参数配置', 'sys_frontend_config', '前端参数配置类型', GETDATE(), NULL),
(8, '任务策略类型', 'task_strategy_type', '定时任务策略类型', GETDATE(), NULL),
(9, '任务周期类型', 'task_period_type', '定时任务周期类型', GETDATE(), NULL),
(10, '通知公告', 'notice', '通知类型', GETDATE(), NULL),
(11, '在线状态', 'user_online_status', '用户在线状态', GETDATE(), NULL),
(12, '插件类型', 'sys_plugin_type', '插件类型', GETDATE(), NULL);
SET IDENTITY_INSERT sys_dict_type OFF;

SET IDENTITY_INSERT sys_dict_data ON;
INSERT INTO sys_dict_data (id, type_code, label, value, color, sort, status, remark, type_id, created_time, updated_time)
VALUES
(1, 'sys_status', '停用', '0', 'red', 1, 1, '停用状态', 1, GETDATE(), NULL),
(2, 'sys_status', '正常', '1', 'green', 2, 1, '正常状态', 1, GETDATE(), NULL),
(3, 'sys_choose', '关闭', 'false', 'error', 1, 1, '关闭状态', 2, GETDATE(), NULL),
(4, 'sys_choose', '开启', 'true', 'success', 2, 1, '开启状态', 2, GETDATE(), NULL),
(5, 'sys_menu_type', '目录', '0', 'orange', 1, 1, '菜单目录', 3, GETDATE(), NULL),
(6, 'sys_menu_type', '菜单', '1', 'default', 2, 1, '普通菜单', 3, GETDATE(), NULL),
(7, 'sys_menu_type', '按钮', '2', 'processing', 3, 1, '菜单按钮', 3, GETDATE(), NULL),
(8, 'sys_menu_type', '内嵌', '3', 'cyan', 4, 1, '内嵌页面', 3, GETDATE(), NULL),
(9, 'sys_menu_type', '外链', '4', 'purple', 5, 1, '外部链接', 3, GETDATE(), NULL),
(10, 'sys_login_status', '失败', '0', 'error', 1, 1, '登录失败状态', 4, GETDATE(), NULL),
(11, 'sys_login_status', '成功', '1', 'success', 2, 1, '登录成功状态', 4, GETDATE(), NULL),
(12, 'sys_data_rule_operator', 'AND', '0', 'green', 1, 1, '逻辑 AND 运算符', 5, GETDATE(), NULL),
(13, 'sys_data_rule_operator', 'OR', '1', 'gold', 2, 1, '逻辑 OR 运算符', 5, GETDATE(), NULL),
(14, 'sys_data_rule_expression', '等于(==)', '0', 'success', 1, 1, '等于比较表达式', 6, GETDATE(), NULL),
(15, 'sys_data_rule_expression', '不等于(!=)', '1', 'error', 2, 1, '不等于比较表达式', 6, GETDATE(), NULL),
(16, 'sys_data_rule_expression', '大于(>)', '2', 'magenta', 3, 1, '大于比较表达式', 6, GETDATE(), NULL),
(17, 'sys_data_rule_expression', '大于等于(>=)', '3', 'volcano', 4, 1, '大于等于比较表达式', 6, GETDATE(), NULL),
(18, 'sys_data_rule_expression', '小于(<)', '4', 'gold', 5, 1, '小于比较表达式', 6, GETDATE(), NULL),
(19, 'sys_data_rule_expression', '小于等于(<=)', '5', 'orange', 6, 1, '小于等于比较表达式', 6, GETDATE(), NULL),
(20, 'sys_data_rule_expression', '包含(in)', '6', 'purple', 7, 1, '包含表达式', 6, GETDATE(), NULL),
(21, 'sys_data_rule_expression', '不包含(not in)', '7', 'error', 8, 1, '不包含表达式', 6, GETDATE(), NULL),
(22, 'sys_frontend_config', '否', '0', 'red', 1, 1, '不是前端参数配置', 7, GETDATE(), NULL),
(23, 'sys_frontend_config', '是', '1', 'green', 2, 1, '是前端参数配置', 7, GETDATE(), NULL),
(24, 'task_strategy_type', 'Interval（间隔）', '0', 'cyan', 1, 1, '时间间隔策略', 8, GETDATE(), NULL),
(25, 'task_strategy_type', 'Crontab（计划）', '1', 'purple', 2, 1, '时间表达式策略', 8, GETDATE(), NULL),
(26, 'task_period_type', '天', 'days', 'processing', 1, 1, '定时任务周期类型-天', 9, GETDATE(), NULL),
(27, 'task_period_type', '小时', 'hours', 'magenta', 2, 1, '定时任务周期类型-小时', 9, GETDATE(), NULL),
(28, 'task_period_type', '分钟', 'minutes', 'volcano', 3, 1, '定时任务周期类型-分钟', 9, GETDATE(), NULL),
(29, 'task_period_type', '秒', 'seconds', 'gold', 4, 1, '定时任务周期类型-秒', 9, GETDATE(), NULL),
(30, 'task_period_type', '微妙', 'microseconds', 'warning', 5, 1, '定时任务周期类型-微妙', 9, GETDATE(), NULL),
(31, 'notice', '通知', '0', 'magenta', 1, 1, '通知类型', 10, GETDATE(), NULL),
(32, 'notice', '公告', '1', 'purple', 2, 1, '公告类型', 10, GETDATE(), NULL),
(33, 'user_online_status', '离线', '0', 'warning', 1, 1, '用户离线状态', 11, GETDATE(), NULL),
(34, 'user_online_status', '在线', '1', 'success', 2, 1, '用户在线状态', 11, GETDATE(), NULL),
(35, 'sys_plugin_type', '压缩包', '0', 'gold', 1, 1, '插件类型-压缩包', 12, GETDATE(), NULL),
(36, 'sys_plugin_type', 'GIT', '1', 'processing', 2, 1, '插件类型-GIT', 12, GETDATE(), NULL);
SET IDENTITY_INSERT sys_dict_data OFF;

DBCC CHECKIDENT ('sys_dict_type', RESEED, 12);
DBCC CHECKIDENT ('sys_dict_data', RESEED, 36);
