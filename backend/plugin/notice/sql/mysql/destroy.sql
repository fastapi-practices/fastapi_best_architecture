delete from sys_menu where name in ('AddNotice', 'EditNotice', 'DeleteNotice');

delete from sys_menu where name = 'PluginNotice';

drop table if exists sys_notice;
