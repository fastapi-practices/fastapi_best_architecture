insert into sys_config (id, name, type, `key`, value, is_frontend, remark, created_time, updated_time)
values
(1, '状态', 'EMAIL', 'EMAIL_STATUS', '1', 0, null, now(), null),
(2, '服务器地址', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', 0, null, now(), null),
(3, '服务器端口', 'EMAIL', 'EMAIL_PORT', '465', 0, null, now(), null),
(4, '邮箱账号', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', 0, null, now(), null),
(5, '邮箱密码', 'EMAIL', 'EMAIL_PASSWORD', '', 0, null, now(), null),
(6, 'SSL 加密', 'EMAIL', 'EMAIL_SSL', '1', 0, null, now(), null),
