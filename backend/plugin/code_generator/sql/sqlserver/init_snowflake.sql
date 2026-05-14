INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES (2049629108257816580, 'code_generator.menu', 'PluginCodeGenerator', '/plugins/code-generator', 10, 'tabler:code', 1, '/plugins/code_generator/views/index', NULL, 1, 1, 1, '', NULL, NULL, GETDATE(), NULL);

INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(2049629108257816581, N'新增业务', 'AddGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:add', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816582, N'修改业务', 'EditGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:edit', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816583, N'删除业务', 'DeleteGenCodeBusiness', NULL, 0, NULL, 2, NULL, 'codegen:business:del', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816584, N'新增模型', 'AddGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:add', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816585, N'修改模型', 'EditGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:edit', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816586, N'删除模型', 'DeleteGenCodeModel', NULL, 0, NULL, 2, NULL, 'codegen:model:del', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816587, N'导入', 'ImportGenCode', NULL, 0, NULL, 2, NULL, 'codegen:table:import', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL),
(2049629108257816588, N'写入', 'WriteGenCode', NULL, 0, NULL, 2, NULL, 'codegen:local:write', 1, 0, 1, '', NULL, 2049629108257816580, GETDATE(), NULL);

INSERT INTO gen_business (id, app_name, table_name, doc_comment, table_comment, class_name, schema_name, filename, datetime_mixin, api_version, gen_path, remark, created_time, updated_time)
VALUES (2112248797819043840, 'test', 'sys_opera_log', N'操作日志表', N'操作日志表', 'SysOperaLog', 'SysOperaLog', 'sys_opera_log', 1, 'v1', NULL, NULL, '2025-12-15 15:30:33', NULL);

INSERT INTO gen_column (id, name, comment, type, pd_type, [default], sort, [length], is_pk, is_nullable, gen_business_id)
VALUES
(2112248797881958400, 'trace_id', N'请求跟踪 ID', 'String', 'str', NULL, 2, 32, 0, 0, 2112248797819043840),
(2112248797944872960, 'username', N'用户名', 'String', 'str', NULL, 3, 64, 0, 1, 2112248797819043840),
(2112248798007787520, 'method', N'请求类型', 'String', 'str', NULL, 4, 32, 0, 0, 2112248797819043840),
(2112248798070702080, 'title', N'操作模块', 'String', 'str', NULL, 5, 256, 0, 0, 2112248797819043840),
(2112248798133616640, 'path', N'请求路径', 'String', 'str', NULL, 6, 512, 0, 0, 2112248797819043840),
(2112248798196531200, 'ip', N'IP地址', 'String', 'str', NULL, 7, 64, 0, 0, 2112248797819043840),
(2112248798259445760, 'country', N'国家', 'String', 'str', NULL, 8, 64, 0, 1, 2112248797819043840),
(2112248798322360320, 'region', N'地区', 'String', 'str', NULL, 9, 64, 0, 1, 2112248797819043840),
(2112248798385274880, 'city', N'城市', 'String', 'str', NULL, 10, 64, 0, 1, 2112248797819043840),
(2112248798448189440, 'user_agent', N'请求头', 'String', 'str', NULL, 11, 512, 0, 0, 2112248797819043840),
(2112248798511104000, 'os', N'操作系统', 'String', 'str', NULL, 12, 64, 0, 1, 2112248797819043840),
(2112248798574018560, 'browser', N'浏览器', 'String', 'str', NULL, 13, 64, 0, 1, 2112248797819043840),
(2112248798636933120, 'device', N'设备', 'String', 'str', NULL, 14, 64, 0, 1, 2112248797819043840),
(2112248798699847680, 'args', N'请求参数', 'JSON', 'dict', NULL, 15, 0, 0, 1, 2112248797819043840),
(2112248798762762240, 'status', N'操作状态（0异常 1正常）', 'INTEGER', 'int', NULL, 16, 0, 0, 0, 2112248797819043840),
(2112248798825676800, 'code', N'操作状态码', 'String', 'str', NULL, 17, 32, 0, 0, 2112248797819043840),
(2112248798888591360, 'msg', N'提示消息', 'TEXT', 'str', NULL, 18, 0, 0, 1, 2112248797819043840),
(2112248798951505920, 'cost_time', N'请求耗时（ms）', 'String', 'str', NULL, 19, 0, 0, 0, 2112248797819043840),
(2112248799014420480, 'opera_time', N'操作时间', 'String', 'str', NULL, 20, 0, 0, 0, 2112248797819043840);
