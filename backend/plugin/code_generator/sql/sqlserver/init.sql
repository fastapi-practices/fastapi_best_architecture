INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES ('code_generator.menu', 'PluginCodeGenerator', '/plugins/code-generator', 10, 'tabler:code', 1, '/plugins/code_generator/views/index', NULL, 1, 1, 1, '', NULL, NULL, GETDATE(), NULL);

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(N'新增业务', 'AddGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'修改业务', 'EditGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'删除业务', 'DeleteGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'新增模型', 'AddGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'修改模型', 'EditGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'删除模型', 'DeleteGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'导入', 'ImportGenCode', NULL, 0, NULL, 2, NULL, 'codegen:table:import', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL),
(N'写入', 'WriteGenCode', NULL, 0, NULL, 2, NULL, 'codegen:local:write', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginCodeGenerator'), GETDATE(), NULL);

SET IDENTITY_INSERT gen_business ON;
INSERT INTO gen_business (id, app_name, table_name, doc_comment, table_comment, class_name, schema_name, filename, datetime_mixin, api_version, gen_path, remark, created_time, updated_time)
VALUES (1, 'test', 'sys_opera_log', N'操作日志表', N'操作日志表', 'SysOperaLog', 'SysOperaLog', 'sys_opera_log', 1, 'v1', NULL, NULL, '2025-12-15 15:30:33', NULL);
SET IDENTITY_INSERT gen_business OFF;

SET IDENTITY_INSERT gen_column ON;
INSERT INTO gen_column (id, name, comment, type, pd_type, [default], sort, [length], is_pk, is_nullable, gen_business_id)
VALUES
(1, 'trace_id', N'请求跟踪 ID', 'String', 'str', NULL, 2, 32, 0, 0, 1),
(2, 'username', N'用户名', 'String', 'str', NULL, 3, 64, 0, 1, 1),
(3, 'method', N'请求类型', 'String', 'str', NULL, 4, 32, 0, 0, 1),
(4, 'title', N'操作模块', 'String', 'str', NULL, 5, 256, 0, 0, 1),
(5, 'path', N'请求路径', 'String', 'str', NULL, 6, 512, 0, 0, 1),
(6, 'ip', N'IP地址', 'String', 'str', NULL, 7, 64, 0, 0, 1),
(7, 'country', N'国家', 'String', 'str', NULL, 8, 64, 0, 1, 1),
(8, 'region', N'地区', 'String', 'str', NULL, 9, 64, 0, 1, 1),
(9, 'city', N'城市', 'String', 'str', NULL, 10, 64, 0, 1, 1),
(10, 'user_agent', N'请求头', 'String', 'str', NULL, 11, 512, 0, 0, 1),
(11, 'os', N'操作系统', 'String', 'str', NULL, 12, 64, 0, 1, 1),
(12, 'browser', N'浏览器', 'String', 'str', NULL, 13, 64, 0, 1, 1),
(13, 'device', N'设备', 'String', 'str', NULL, 14, 64, 0, 1, 1),
(14, 'args', N'请求参数', 'JSON', 'dict', NULL, 15, 0, 0, 1, 1),
(15, 'status', N'操作状态（0异常 1正常）', 'INTEGER', 'int', NULL, 16, 0, 0, 0, 1),
(16, 'code', N'操作状态码', 'String', 'str', NULL, 17, 32, 0, 0, 1),
(17, 'msg', N'提示消息', 'TEXT', 'str', NULL, 18, 0, 0, 1, 1),
(18, 'cost_time', N'请求耗时（ms）', 'String', 'str', NULL, 19, 0, 0, 0, 1),
(19, 'opera_time', N'操作时间', 'String', 'str', NULL, 20, 0, 0, 0, 1);
SET IDENTITY_INSERT gen_column OFF;

DBCC CHECKIDENT ('gen_business', RESEED, 1);
DBCC CHECKIDENT ('gen_column', RESEED, 19);
