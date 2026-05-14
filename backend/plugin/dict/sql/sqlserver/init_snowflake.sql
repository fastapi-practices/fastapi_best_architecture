INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES (2049629108253622287, 'dict.menu', 'PluginDict', '/plugins/dict', 8, 'fluent-mdl2:dictionary', 1, '/plugins/dict/views/index', NULL, 1, 1, 1, '', NULL, 2049629108245233667, GETDATE(), NULL);

INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(2049629108253622288, N'新增类型', 'AddDictType', NULL, 0, NULL, 2, NULL, 'dict:type:add', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL),
(2049629108253622289, N'修改类型', 'EditDictType', NULL, 0, NULL, 2, NULL, 'dict:type:edit', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL),
(2049629108253622290, N'删除类型', 'DeleteDictType', NULL, 0, NULL, 2, NULL, 'dict:type:del', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL),
(2049629108253622291, N'新增数据', 'AddDictData', NULL, 0, NULL, 2, NULL, 'dict:data:add', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL),
(2049629108253622292, N'修改数据', 'EditDictData', NULL, 0, NULL, 2, NULL, 'dict:data:edit', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL),
(2049629108253622293, N'删除数据', 'DeleteDictData', NULL, 0, NULL, 2, NULL, 'dict:data:del', 1, 0, 1, '', NULL, 2049629108253622287, GETDATE(), NULL);

INSERT INTO sys_dict_type (id, name, code, remark, created_time, updated_time)
VALUES
(2048602512340156416, N'通用状态', 'sys_status', N'系统通用状态：1/0', GETDATE(), NULL),
(2048602512369516544, N'通用开关', 'sys_choose', N'系统通用开关：true/false', GETDATE(), NULL),
(2048602512432431104, N'菜单类型', 'sys_menu_type', N'系统菜单类型', GETDATE(), NULL),
(2048602512495345664, N'登录状态', 'sys_login_status', N'用户登录状态', GETDATE(), NULL),
(2048602512549871616, N'数据规则运算符', 'sys_data_rule_operator', N'数据权限规则运算符', GETDATE(), NULL),
(2048602512616980480, N'数据规则表达式', 'sys_data_rule_expression', N'数据权限规则表达式', GETDATE(), NULL),
(2048602512692477952, N'前端参数配置', 'sys_frontend_config', N'前端参数配置类型', GETDATE(), NULL),
(2048602512755392512, N'任务策略类型', 'task_strategy_type', N'定时任务策略类型', GETDATE(), NULL),
(2048602512818307072, N'任务周期类型', 'task_period_type', N'定时任务周期类型', GETDATE(), NULL),
(2048602512881221632, N'通知公告', 'notice', N'通知类型', GETDATE(), NULL),
(2048602512948330496, N'在线状态', 'user_online_status', N'用户在线状态', GETDATE(), NULL),
(2048602513015439360, N'插件类型', 'sys_plugin_type', N'插件类型', GETDATE(), NULL);

INSERT INTO sys_dict_data (id, type_code, label, value, color, sort, status, remark, type_id, created_time, updated_time)
VALUES
(2048602513078353920, 'sys_status', N'停用', '0', 'red', 1, 1, N'停用状态', 2048602512340156416, GETDATE(), NULL),
(2048602513128685568, 'sys_status', N'正常', '1', 'green', 2, 1, N'正常状态', 2048602512340156416, GETDATE(), NULL),
(2048602513174822912, 'sys_choose', N'关闭', 'false', 'error', 1, 1, N'关闭状态', 2048602512369516544, GETDATE(), NULL),
(2048602513241931776, 'sys_choose', N'开启', 'true', 'success', 2, 1, N'开启状态', 2048602512369516544, GETDATE(), NULL),
(2048602513292263424, 'sys_menu_type', N'目录', '0', 'orange', 1, 1, N'菜单目录', 2048602512432431104, GETDATE(), NULL),
(2048602513359372288, 'sys_menu_type', N'菜单', '1', 'default', 2, 1, N'普通菜单', 2048602512432431104, GETDATE(), NULL),
(2048602513422286848, 'sys_menu_type', N'按钮', '2', 'processing', 3, 1, N'菜单按钮', 2048602512432431104, GETDATE(), NULL),
(2048602513476812800, 'sys_menu_type', N'内嵌', '3', 'cyan', 4, 1, N'内嵌页面', 2048602512432431104, GETDATE(), NULL),
(2048602513543921664, 'sys_menu_type', N'外链', '4', 'purple', 5, 1, N'外部链接', 2048602512432431104, GETDATE(), NULL),
(2048602513590059008, 'sys_login_status', N'失败', '0', 'error', 1, 1, N'登录失败状态', 2048602512495345664, GETDATE(), NULL),
(2048602513657167872, 'sys_login_status', N'成功', '1', 'success', 2, 1, N'登录成功状态', 2048602512495345664, GETDATE(), NULL),
(2048602513720082432, 'sys_data_rule_operator', 'AND', '0', 'green', 1, 1, N'逻辑 AND 运算符', 2048602512549871616, GETDATE(), NULL),
(2048602513782996992, 'sys_data_rule_operator', 'OR', '1', 'gold', 2, 1, N'逻辑 OR 运算符', 2048602512549871616, GETDATE(), NULL),
(2048602513850105856, 'sys_data_rule_expression', N'等于(==)', '0', 'success', 1, 1, N'等于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602513917214720, 'sys_data_rule_expression', N'不等于(!=)', '1', 'error', 2, 1, N'不等于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602513984323584, 'sys_data_rule_expression', N'大于(>)', '2', 'magenta', 3, 1, N'大于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514051432448, 'sys_data_rule_expression', N'大于等于(>=)', '3', 'volcano', 4, 1, N'大于等于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514118541312, 'sys_data_rule_expression', N'小于(<)', '4', 'gold', 5, 1, N'小于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514168872960, 'sys_data_rule_expression', N'小于等于(<=)', '5', 'orange', 6, 1, N'小于等于比较表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514231787520, 'sys_data_rule_expression', N'包含(in)', '6', 'purple', 7, 1, N'包含表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514303090688, 'sys_data_rule_expression', N'不包含(not in)', '7', 'error', 8, 1, N'不包含表达式', 2048602512616980480, GETDATE(), NULL),
(2048602514366005248, 'sys_frontend_config', N'否', '0', 'red', 1, 1, N'不是前端参数配置', 2048602512692477952, GETDATE(), NULL),
(2048602514433114112, 'sys_frontend_config', N'是', '1', 'green', 2, 1, N'是前端参数配置', 2048602512692477952, GETDATE(), NULL),
(2048602514500222976, 'task_strategy_type', N'Interval（间隔）', '0', 'cyan', 1, 1, N'时间间隔策略', 2048602512755392512, GETDATE(), NULL),
(2048602514567331840, 'task_strategy_type', N'Crontab（计划）', '1', 'purple', 2, 1, N'时间表达式策略', 2048602512755392512, GETDATE(), NULL),
(2048602514634440704, 'task_period_type', N'天', 'days', 'processing', 1, 1, N'定时任务周期类型-天', 2048602512818307072, GETDATE(), NULL),
(2048602514701549568, 'task_period_type', N'小时', 'hours', 'magenta', 2, 1, N'定时任务周期类型-小时', 2048602512818307072, GETDATE(), NULL),
(2048602514768658432, 'task_period_type', N'分钟', 'minutes', 'volcano', 3, 1, N'定时任务周期类型-分钟', 2048602512818307072, GETDATE(), NULL),
(2048602514835767296, 'task_period_type', N'秒', 'seconds', 'gold', 4, 1, N'定时任务周期类型-秒', 2048602512818307072, GETDATE(), NULL),
(2048602514902876160, 'task_period_type', N'微妙', 'microseconds', 'warning', 5, 1, N'定时任务周期类型-微妙', 2048602512818307072, GETDATE(), NULL),
(2048602514969985024, 'notice', N'通知', '0', 'magenta', 1, 1, N'通知类型', 2048602512881221632, GETDATE(), NULL),
(2048602515037093888, 'notice', N'公告', '1', 'purple', 2, 1, N'公告类型', 2048602512881221632, GETDATE(), NULL),
(2048602515104202752, 'user_online_status', N'离线', '0', 'warning', 1, 1, N'用户离线状态', 2048602512948330496, GETDATE(), NULL),
(2048602515171311616, 'user_online_status', N'在线', '1', 'success', 2, 1, N'用户在线状态', 2048602512948330496, GETDATE(), NULL),
(2048602515238420480, 'sys_plugin_type', N'压缩包', '0', 'gold', 1, 1, N'插件类型-压缩包', 2048602513015439360, GETDATE(), NULL),
(2048602515305529344, 'sys_plugin_type', 'GIT', '1', 'processing', 2, 1, N'插件类型-GIT', 2048602513015439360, GETDATE(), NULL);
