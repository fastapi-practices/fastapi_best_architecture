insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (2049629108253622283, 'config.menu', 'PluginConfig', '/plugins/config', 7, 'codicon:symbol-parameter', 1, '/plugins/config/views/index', null, 1, 1, 1, '', null, 2049629108245233667, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
(2049629108253622284, '新增', 'AddConfig', null, 0, null, 2, null, 'sys:config:add', 1, 0, 1, '', null, 2049629108253622283, now(), null),
(2049629108253622285, '修改', 'EditConfig', null, 0, null, 2, null, 'sys:config:edit', 1, 0, 1, '', null, 2049629108253622283, now(), null),
(2049629108253622286, '删除', 'DeleteConfig', null, 0, null, 2, null, 'sys:config:del', 1, 0, 1, '', null, 2049629108253622283, now(), null);

insert into sys_config (id, name, type, "key", value, is_frontend, remark, created_time, updated_time)
values
(2069061886627938304, '状态', 'EMAIL', 'EMAIL_CONFIG_STATUS', '1', false, null, now(), null),
(2069061886627938305, '服务器地址', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', false, null, now(), null),
(2069061886627938306, '服务器端口', 'EMAIL', 'EMAIL_PORT', '465', false, null, now(), null),
(2069061886627938307, '邮箱账号', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', false, null, now(), null),
(2069061886627938308, '邮箱密码', 'EMAIL', 'EMAIL_PASSWORD', '', false, null, now(), null),
(2069061886627938309, 'SSL 加密', 'EMAIL', 'EMAIL_SSL', 'true', false, null, now(), null),
(2069061886627938310, '状态', 'USER_SECURITY', 'USER_SECURITY_CONFIG_STATUS', '1', false, null, now(), null),
(2069061886627938311, '密码错误锁定阈值', 'USER_SECURITY', 'USER_LOCK_THRESHOLD', '5', false, '0 表示禁用锁定', now(), null),
(2069061886627938312, '密码错误锁定时长（秒）', 'USER_SECURITY', 'USER_LOCK_SECONDS', '300', false, null, now(), null),
(2069061886627938313, '密码有效期（天）', 'USER_SECURITY', 'USER_PASSWORD_EXPIRY_DAYS', '365', false, '0 表示永不过期', now(), null),
(2069061886627938314, '密码到期提醒（天）', 'USER_SECURITY', 'USER_PASSWORD_REMINDER_DAYS', '7', false, '0 表示不提醒', now(), null),
(2069061886627938315, '密码历史检查次数', 'USER_SECURITY', 'USER_PASSWORD_HISTORY_CHECK_COUNT', '3', false, null, now(), null),
(2069061886627938316, '密码最小长度', 'USER_SECURITY', 'USER_PASSWORD_MIN_LENGTH', '6', false, null, now(), null),
(2069061886627938317, '密码最大长度', 'USER_SECURITY', 'USER_PASSWORD_MAX_LENGTH', '32', false, null, now(), null),
(2069061886627938318, '密码必须包含特殊字符', 'USER_SECURITY', 'USER_PASSWORD_REQUIRE_SPECIAL_CHAR', 'false', false, null, now(), null),
(2069061886627938319, '状态', 'LOGIN', 'LOGIN_CONFIG_STATUS', '1', false, null, now(), null),
(2069061886627938320, '验证码开关', 'LOGIN', 'LOGIN_CAPTCHA_ENABLED', 'true', false, null, now(), null);
