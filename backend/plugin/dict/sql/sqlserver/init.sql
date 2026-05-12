INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES ('dict.menu', 'PluginDict', '/plugins/dict', 8, 'fluent-mdl2:dictionary', 1, '/plugins/dict/views/index', NULL, 1, 1, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'System'), GETDATE(), NULL);

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(N'新增类型', 'AddDictType', NULL, 0, NULL, 2, NULL, 'dict:type:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
(N'修改类型', 'EditDictType', NULL, 0, NULL, 2, NULL, 'dict:type:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
(N'删除类型', 'DeleteDictType', NULL, 0, NULL, 2, NULL, 'dict:type:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
(N'新增数据', 'AddDictData', NULL, 0, NULL, 2, NULL, 'dict:data:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
(N'修改数据', 'EditDictData', NULL, 0, NULL, 2, NULL, 'dict:data:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL),
(N'删除数据', 'DeleteDictData', NULL, 0, NULL, 2, NULL, 'dict:data:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginDict'), GETDATE(), NULL);

SET IDENTITY_INSERT sys_dict_type ON;
INSERT INTO sys_dict_type (id, name, code, remark, created_time, updated_time)
VALUES
(1, N'通用状态', 'sys_status', N'系统通用状态：1/0', GETDATE(), NULL),
(2, N'通用开关', 'sys_choose', N'系统通用开关：true/false', GETDATE(), NULL),
(3, N'菜单类型', 'sys_menu_type', N'系统菜单类型', GETDATE(), NULL),
(4, N'登录状态', 'sys_login_status', N'用户登录状态', GETDATE(), NULL),
(5, N'数据规则运算符', 'sys_data_rule_operator', N'数据权限规则运算符', GETDATE(), NULL),
(6, N'数据规则表达式', 'sys_data_rule_expression', N'数据权限规则表达式', GETDATE(), NULL),
(7, N'前端参数配置', 'sys_frontend_config', N'前端参数配置类型', GETDATE(), NULL),
(8, N'任务策略类型', 'task_strategy_type', N'定时任务策略类型', GETDATE(), NULL),
(9, N'任务周期类型', 'task_period_type', N'定时任务周期类型', GETDATE(), NULL),
(10, N'通知公告', 'notice', N'通知类型', GETDATE(), NULL),
(11, N'在线状态', 'user_online_status', N'用户在线状态', GETDATE(), NULL),
(12, N'插件类型', 'sys_plugin_type', N'插件类型', GETDATE(), NULL);
SET IDENTITY_INSERT sys_dict_type OFF;

SET IDENTITY_INSERT sys_dict_data ON;
INSERT INTO sys_dict_data (id, type_code, label, value, color, sort, status, remark, type_id, created_time, updated_time)
VALUES
(1, 'sys_status', N'停用', '0', 'red', 1, 1, N'停用状态', 1, GETDATE(), NULL),
(2, 'sys_status', N'正常', '1', 'green', 2, 1, N'正常状态', 1, GETDATE(), NULL),
(3, 'sys_choose', N'关闭', 'false', 'error', 1, 1, N'关闭状态', 2, GETDATE(), NULL),
(4, 'sys_choose', N'开启', 'true', 'success', 2, 1, N'开启状态', 2, GETDATE(), NULL),
(5, 'sys_menu_type', N'目录', '0', 'orange', 1, 1, N'菜单目录', 3, GETDATE(), NULL),
(6, 'sys_menu_type', N'菜单', '1', 'default', 2, 1, N'普通菜单', 3, GETDATE(), NULL),
(7, 'sys_menu_type', N'按钮', '2', 'processing', 3, 1, N'菜单按钮', 3, GETDATE(), NULL),
(8, 'sys_menu_type', N'内嵌', '3', 'cyan', 4, 1, N'内嵌页面', 3, GETDATE(), NULL),
(9, 'sys_menu_type', N'外链', '4', 'purple', 5, 1, N'外部链接', 3, GETDATE(), NULL),
(10, 'sys_login_status', N'失败', '0', 'error', 1, 1, N'登录失败状态', 4, GETDATE(), NULL),
(11, 'sys_login_status', N'成功', '1', 'success', 2, 1, N'登录成功状态', 4, GETDATE(), NULL),
(12, 'sys_data_rule_operator', 'AND', '0', 'green', 1, 1, N'逻辑 AND 运算符', 5, GETDATE(), NULL),
(13, 'sys_data_rule_operator', 'OR', '1', 'gold', 2, 1, N'逻辑 OR 运算符', 5, GETDATE(), NULL),
(14, 'sys_data_rule_expression', N'等于(==)', '0', 'success', 1, 1, N'等于比较表达式', 6, GETDATE(), NULL),
(15, 'sys_data_rule_expression', N'不等于(!=)', '1', 'error', 2, 1, N'不等于比较表达式', 6, GETDATE(), NULL),
(16, 'sys_data_rule_expression', N'大于(>)', '2', 'magenta', 3, 1, N'大于比较表达式', 6, GETDATE(), NULL),
(17, 'sys_data_rule_expression', N'大于等于(>=)', '3', 'volcano', 4, 1, N'大于等于比较表达式', 6, GETDATE(), NULL),
(18, 'sys_data_rule_expression', N'小于(<)', '4', 'gold', 5, 1, N'小于比较表达式', 6, GETDATE(), NULL),
(19, 'sys_data_rule_expression', N'小于等于(<=)', '5', 'orange', 6, 1, N'小于等于比较表达式', 6, GETDATE(), NULL),
(20, 'sys_data_rule_expression', N'包含(in)', '6', 'purple', 7, 1, N'包含表达式', 6, GETDATE(), NULL),
(21, 'sys_data_rule_expression', N'不包含(not in)', '7', 'error', 8, 1, N'不包含表达式', 6, GETDATE(), NULL),
(22, 'sys_frontend_config', N'否', '0', 'red', 1, 1, N'不是前端参数配置', 7, GETDATE(), NULL),
(23, 'sys_frontend_config', N'是', '1', 'green', 2, 1, N'是前端参数配置', 7, GETDATE(), NULL),
(24, 'task_strategy_type', N'Interval（间隔）', '0', 'cyan', 1, 1, N'时间间隔策略', 8, GETDATE(), NULL),
(25, 'task_strategy_type', N'Crontab（计划）', '1', 'purple', 2, 1, N'时间表达式策略', 8, GETDATE(), NULL),
(26, 'task_period_type', N'天', 'days', 'processing', 1, 1, N'定时任务周期类型-天', 9, GETDATE(), NULL),
(27, 'task_period_type', N'小时', 'hours', 'magenta', 2, 1, N'定时任务周期类型-小时', 9, GETDATE(), NULL),
(28, 'task_period_type', N'分钟', 'minutes', 'volcano', 3, 1, N'定时任务周期类型-分钟', 9, GETDATE(), NULL),
(29, 'task_period_type', N'秒', 'seconds', 'gold', 4, 1, N'定时任务周期类型-秒', 9, GETDATE(), NULL),
(30, 'task_period_type', N'微妙', 'microseconds', 'warning', 5, 1, N'定时任务周期类型-微妙', 9, GETDATE(), NULL),
(31, 'notice', N'通知', '0', 'magenta', 1, 1, N'通知类型', 10, GETDATE(), NULL),
(32, 'notice', N'公告', '1', 'purple', 2, 1, N'公告类型', 10, GETDATE(), NULL),
(33, 'user_online_status', N'离线', '0', 'warning', 1, 1, N'用户离线状态', 11, GETDATE(), NULL),
(34, 'user_online_status', N'在线', '1', 'success', 2, 1, N'用户在线状态', 11, GETDATE(), NULL),
(35, 'sys_plugin_type', N'压缩包', '0', 'gold', 1, 1, N'插件类型-压缩包', 12, GETDATE(), NULL),
(36, 'sys_plugin_type', 'GIT', '1', 'processing', 2, 1, N'插件类型-GIT', 12, GETDATE(), NULL);
SET IDENTITY_INSERT sys_dict_data OFF;

DBCC CHECKIDENT ('sys_dict_type', RESEED, 12);
DBCC CHECKIDENT ('sys_dict_data', RESEED, 36);
