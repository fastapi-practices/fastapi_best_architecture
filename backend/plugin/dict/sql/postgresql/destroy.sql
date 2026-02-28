delete from sys_menu where name in ('AddDictType', 'EditDictType', 'DeleteDictType', 'AddDictData', 'EditDictData', 'DeleteDictData');

delete from sys_menu where name = 'PluginDict';

drop table if exists sys_dict_data;
drop table if exists sys_dict_type;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
