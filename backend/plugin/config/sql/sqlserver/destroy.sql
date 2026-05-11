DELETE FROM sys_menu WHERE name IN ('AddConfig', 'EditConfig', 'DeleteConfig');

DELETE FROM sys_menu WHERE name = 'PluginConfig';

DROP TABLE IF EXISTS sys_config;
