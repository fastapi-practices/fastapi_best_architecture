INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES (2049629108253622283, 'config.menu', 'PluginConfig', '/plugins/config', 7, 'codicon:symbol-parameter', 1, '/plugins/config/views/index', NULL, 1, 1, 1, '', NULL, 2049629108245233667, GETDATE(), NULL);

INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(2049629108253622284, N'新增', 'AddConfig', NULL, 0, NULL, 2, NULL, 'sys:config:add', 1, 0, 1, '', NULL, 2049629108253622283, GETDATE(), NULL),
(2049629108253622285, N'修改', 'EditConfig', NULL, 0, NULL, 2, NULL, 'sys:config:edit', 1, 0, 1, '', NULL, 2049629108253622283, GETDATE(), NULL),
(2049629108253622286, N'删除', 'DeleteConfig', NULL, 0, NULL, 2, NULL, 'sys:config:del', 1, 0, 1, '', NULL, 2049629108253622283, GETDATE(), NULL);

INSERT INTO sys_config (id, name, type, [key], value, is_frontend, remark, created_time, updated_time)
VALUES
(2069061886627938304, N'状态', 'EMAIL', 'EMAIL_CONFIG_STATUS', '1', 0, NULL, GETDATE(), NULL),
(2069061886627938305, N'服务器地址', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', 0, NULL, GETDATE(), NULL),
(2069061886627938306, N'服务器端口', 'EMAIL', 'EMAIL_PORT', '465', 0, NULL, GETDATE(), NULL),
(2069061886627938307, N'邮箱账号', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', 0, NULL, GETDATE(), NULL),
(2069061886627938308, N'邮箱密码', 'EMAIL', 'EMAIL_PASSWORD', '', 0, NULL, GETDATE(), NULL),
(2069061886627938309, N'SSL 加密', 'EMAIL', 'EMAIL_SSL', 'true', 0, NULL, GETDATE(), NULL),
(2069061886627938310, N'状态', 'USER_SECURITY', 'USER_SECURITY_CONFIG_STATUS', '1', 0, NULL, GETDATE(), NULL),
(2069061886627938311, N'密码错误锁定阈值', 'USER_SECURITY', 'USER_LOCK_THRESHOLD', '5', 0, N'0 表示禁用锁定', GETDATE(), NULL),
(2069061886627938312, N'密码错误锁定时长（秒）', 'USER_SECURITY', 'USER_LOCK_SECONDS', '300', 0, NULL, GETDATE(), NULL),
(2069061886627938313, N'密码有效期（天）', 'USER_SECURITY', 'USER_PASSWORD_EXPIRY_DAYS', '365', 0, N'0 表示永不过期', GETDATE(), NULL),
(2069061886627938314, N'密码到期提醒（天）', 'USER_SECURITY', 'USER_PASSWORD_REMINDER_DAYS', '7', 0, N'0 表示不提醒', GETDATE(), NULL),
(2069061886627938315, N'密码历史检查次数', 'USER_SECURITY', 'USER_PASSWORD_HISTORY_CHECK_COUNT', '3', 0, NULL, GETDATE(), NULL),
(2069061886627938316, N'密码最小长度', 'USER_SECURITY', 'USER_PASSWORD_MIN_LENGTH', '6', 0, NULL, GETDATE(), NULL),
(2069061886627938317, N'密码最大长度', 'USER_SECURITY', 'USER_PASSWORD_MAX_LENGTH', '32', 0, NULL, GETDATE(), NULL),
(2069061886627938318, N'密码必须包含特殊字符', 'USER_SECURITY', 'USER_PASSWORD_REQUIRE_SPECIAL_CHAR', 'false', 0, NULL, GETDATE(), NULL),
(2069061886627938319, N'状态', 'LOGIN', 'LOGIN_CONFIG_STATUS', '1', 0, NULL, GETDATE(), NULL),
(2069061886627938320, N'验证码开关', 'LOGIN', 'LOGIN_CAPTCHA_ENABLED', 'true', 0, NULL, GETDATE(), NULL);
