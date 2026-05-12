DELETE FROM sys_menu WHERE name IN ('AddNotice', 'EditNotice', 'DeleteNotice');

DELETE FROM sys_menu WHERE name = 'PluginNotice';

DROP TABLE IF EXISTS sys_notice;
