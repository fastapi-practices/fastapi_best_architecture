INSERT INTO fba.sys_dept (id, name, level, sort, leader, phone, email, status, del_flag, parent_id, created_time,
                          updated_time)
VALUES (1, 'test', 0, 0, null, null, null, 1, 0, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_menu (id, name, level, sort, icon, path, menu_type, component, perms, status, remark, parent_id,
                          created_time, updated_time)
VALUES (1, 'test', 0, 0, null, null, 0, null, null, 1, null, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_role (id, name, data_scope, status, remark, created_time, updated_time)
VALUES (1, 'test', 2, 1, null, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_role_menu (id, role_id, menu_id)
VALUES (1, 1, 1);

INSERT INTO fba.sys_user (id, uuid, username, nickname, password, email, is_superuser, status, is_multi_login, avatar,
                          phone, join_time, last_login_time, dept_id, created_time, updated_time)
VALUES (1, 'af4c804f-3966-4949-ace2-3bb7416ea926', 'test', 'test',
        '$2b$12$TpdL7kKriqhpJHSBMT.Fr.hJNBx5SdUybi.NT1DV5MojYpV9PpRre', 'test@gmail.com', 1, 1, 0, null, null,
        '2023-06-26 17:13:45', null, 1, '2023-06-26 17:13:45', null);

INSERT INTO fba.sys_user_role (id, user_id, role_id)
VALUES (1, 1, 1);
