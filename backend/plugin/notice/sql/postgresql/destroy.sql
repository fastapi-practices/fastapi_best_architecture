delete from sys_menu where name in ('AddNotice', 'EditNotice', 'DeleteNotice');

delete from sys_menu where name = 'PluginNotice';

drop table if exists sys_notice;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
