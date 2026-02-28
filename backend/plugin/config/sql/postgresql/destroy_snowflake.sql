delete from sys_menu where name in ('AddConfig', 'EditConfig', 'DeleteConfig');

delete from sys_menu where name = 'PluginConfig';

drop table if exists sys_config;
