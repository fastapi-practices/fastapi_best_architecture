insert into sys_config (id, name, type, "key", value, is_frontend, remark, created_time, updated_time)
values
(2069061886627938304, '状态', 'EMAIL', 'EMAIL_STATUS', '1', false, null, now(), null),
(2069061886627938305, '服务器地址', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', false, null, now(), null),
(2069061886627938306, '服务器端口', 'EMAIL', 'EMAIL_PORT', '465', false, null, now(), null),
(2069061886627938307, '邮箱账号', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', false, null, now(), null),
(2069061886627938308, '邮箱密码', 'EMAIL', 'EMAIL_PASSWORD', '', false, null, now(), null),
(2069061886627938309, 'SSL 加密', 'EMAIL', 'EMAIL_SSL', '1', false, null, now(), null);
