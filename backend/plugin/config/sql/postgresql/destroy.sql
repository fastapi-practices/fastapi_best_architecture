delete from sys_menu where name in ('AddConfig', 'EditConfig', 'DeleteConfig');

delete from sys_menu where name = 'PluginConfig';

drop table if exists sys_config;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
