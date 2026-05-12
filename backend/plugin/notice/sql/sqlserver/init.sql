INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES ('notice.menu', 'PluginNotice', '/plugins/notice', 9, 'fe:notice-push', 1, '/plugins/notice/views/index', NULL, 1, 1, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'System'), GETDATE(), NULL);

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(N'新增', 'AddNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:add', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginNotice'), GETDATE(), NULL),
(N'修改', 'EditNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:edit', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginNotice'), GETDATE(), NULL),
(N'删除', 'DeleteNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:del', 1, 0, 1, '', NULL, (SELECT id FROM sys_menu WHERE name = 'PluginNotice'), GETDATE(), NULL);

SET IDENTITY_INSERT sys_notice ON;
INSERT INTO sys_notice (id, title, type, status, content, created_time, updated_time)
VALUES (1, 'hahahahahaahahaha', 0, 1, N'你好😄

```
print(''fba yyds'')
```

⚡⚡⚡

| col1 | col2 | col3 |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |

* 1
* 2
* 3
', '2025-12-15 15:33:16', NULL);
SET IDENTITY_INSERT sys_notice OFF;

DBCC CHECKIDENT ('sys_notice', RESEED, 1);
