INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES (2049629108257816576, 'notice.menu', 'PluginNotice', '/plugins/notice', 9, 'fe:notice-push', 1, '/plugins/notice/views/index', NULL, 1, 1, 1, '', NULL, 2049629108245233667, GETDATE(), NULL);

INSERT INTO sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
(2049629108257816577, N'新增', 'AddNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:add', 1, 0, 1, '', NULL, 2049629108257816576, GETDATE(), NULL),
(2049629108257816578, N'修改', 'EditNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:edit', 1, 0, 1, '', NULL, 2049629108257816576, GETDATE(), NULL),
(2049629108257816579, N'删除', 'DeleteNotice', NULL, 0, NULL, 2, NULL, 'sys:notice:del', 1, 0, 1, '', NULL, 2049629108257816576, GETDATE(), NULL);

INSERT INTO sys_notice (id, title, type, status, content, created_time, updated_time)
VALUES (2112248797756129280, 'hahahahahaahahaha', 0, 1, N'你好😄

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
