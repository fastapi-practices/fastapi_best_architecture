create table sys_data_scope
(
    id           serial
        primary key,
    name         varchar(50)              not null
        unique,
    status       integer                  not null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_data_scope is 'Data Range Table';

comment on column sys_data_scope.id is 'PRIMARY ID';

comment on column sys_data_scope.name is 'Name';

comment on column sys_data_scope.status is 'Status (0 disabled 1)';

comment on column sys_data_scope.created_time is 'Created';

comment on column sys_data_scope.updated_time is 'Update Time';

create index ix_sys_data_scope_id
    on sys_data_scope (id);

create table sys_dept
(
    id           serial
        primary key,
    name         varchar(50)              not null,
    sort         integer                  not null,
    leader       varchar(20),
    phone        varchar(11),
    email        varchar(50),
    status       integer                  not null,
    del_flag     integer                  not null,
    parent_id    integer
                                          references sys_dept
                                              on delete set null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_dept is 'Sectoral table';

comment on column sys_dept.id is 'PRIMARY ID';

comment on column sys_dept.name is 'Department name';

comment on column sys_dept.sort is 'Sort';

comment on column sys_dept.leader is 'Head';

comment on column sys_dept.phone is 'Cell phone';

comment on column sys_dept.email is 'Mailbox';

comment on column sys_dept.status is 'Sector status (0 disabled 1)';

comment on column sys_dept.del_flag is 'Delete sign (0 delete 1 exists)';

comment on column sys_dept.parent_id is 'PARENT ID';

comment on column sys_dept.created_time is 'Created';

comment on column sys_dept.updated_time is 'Update Time';

create index ix_sys_dept_id
    on sys_dept (id);

create index ix_sys_dept_parent_id
    on sys_dept (parent_id);

create table sys_login_log
(
    id           serial
        primary key,
    user_uuid    varchar(50)              not null,
    username     varchar(20)              not null,
    status       integer                  not null,
    ip           varchar(50)              not null,
    country      varchar(50),
    region       varchar(50),
    city         varchar(50),
    user_agent   varchar(255)             not null,
    os           varchar(50),
    browser      varchar(50),
    device       varchar(50),
    msg          text                     not null,
    login_time   timestamp with time zone not null,
    created_time timestamp with time zone not null
);

comment on table sys_login_log is 'Login Login Table';

comment on column sys_login_log.id is 'PRIMARY ID';

comment on column sys_login_log.user_uuid is 'USERUID';

comment on column sys_login_log.username is 'Username';

comment on column sys_login_log.status is 'Login status (0 failed)';

comment on column sys_login_log.ip is 'LOGIN IP ADDRESS';

comment on column sys_login_log.country is 'Country';

comment on column sys_login_log.region is 'Region';

comment on column sys_login_log.city is 'Urban';

comment on column sys_login_log.user_agent is 'Request Header';

comment on column sys_login_log.os is 'Operating systems';

comment on column sys_login_log.browser is 'Browser';

comment on column sys_login_log.device is 'Equipment';

comment on column sys_login_log.msg is 'Message';

comment on column sys_login_log.login_time is 'Login Time';

comment on column sys_login_log.created_time is 'Created';

create index ix_sys_login_log_id
    on sys_login_log (id);

create table sys_menu
(
    id           serial
        primary key,
    title        varchar(50)              not null,
    name         varchar(50)              not null,
    path         varchar(200)             not null,
    sort         integer                  not null,
    icon         varchar(100),
    type         integer                  not null,
    component    varchar(255),
    perms        varchar(100),
    status       integer                  not null,
    display      integer                  not null,
    cache        integer                  not null,
    link         text,
    remark       text,
    parent_id    integer
                                          references sys_menu
                                              on delete set null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_menu is 'Menu Table';

comment on column sys_menu.id is 'PRIMARY ID';

comment on column sys_menu.title is 'Menu Title';

comment on column sys_menu.name is 'Menu Name';

comment on column sys_menu.path is 'Route Address';

comment on column sys_menu.sort is 'Sort';

comment on column sys_menu.icon is 'Menu Icon';

comment on column sys_menu.type is 'Menu type (0 directory 1 menu 2 button)';

comment on column sys_menu.component is 'Component Path';

comment on column sys_menu.perms is 'Permission Identification';

comment on column sys_menu.status is 'Menu status (0 disabled 1 normal)';

comment on column sys_menu.display is 'Whether to show (0 no 1)';

comment on column sys_menu.cache is 'Cache (0 No 1)';

comment on column sys_menu.link is 'Outlink Address';

comment on column sys_menu.remark is 'Remarks';

comment on column sys_menu.parent_id is 'PARENT MENU ID';

comment on column sys_menu.created_time is 'Created';

comment on column sys_menu.updated_time is 'Update Time';

create index ix_sys_menu_id
    on sys_menu (id);

create index ix_sys_menu_parent_id
    on sys_menu (parent_id);

create table sys_opera_log
(
    id           serial
        primary key,
    trace_id     varchar(32)              not null,
    username     varchar(20),
    method       varchar(20)              not null,
    title        varchar(255)             not null,
    path         varchar(500)             not null,
    ip           varchar(50)              not null,
    country      varchar(50),
    region       varchar(50),
    city         varchar(50),
    user_agent   varchar(255)             not null,
    os           varchar(50),
    browser      varchar(50),
    device       varchar(50),
    args         json,
    status       integer                  not null,
    code         varchar(20)              not null,
    msg          text,
    cost_time    double precision         not null,
    opera_time   timestamp with time zone not null,
    created_time timestamp with time zone not null
);

comment on table sys_opera_log is 'Operations Log Table';

comment on column sys_opera_log.id is 'PRIMARY ID';

comment on column sys_opera_log.trace_id is 'REQUEST TRACKING ID';

comment on column sys_opera_log.username is 'Username';

comment on column sys_opera_log.method is 'Type of request';

comment on column sys_opera_log.title is 'Operation module';

comment on column sys_opera_log.path is 'Request Path';

comment on column sys_opera_log.ip is 'IP ADDRESS';

comment on column sys_opera_log.country is 'Country';

comment on column sys_opera_log.region is 'Region';

comment on column sys_opera_log.city is 'Urban';

comment on column sys_opera_log.user_agent is 'Request Header';

comment on column sys_opera_log.os is 'Operating systems';

comment on column sys_opera_log.browser is 'Browser';

comment on column sys_opera_log.device is 'Equipment';

comment on column sys_opera_log.args is 'Request parameters';

comment on column sys_opera_log.status is 'Operational status (0 anomaly 1)';

comment on column sys_opera_log.code is 'Operational status code';

comment on column sys_opera_log.msg is 'Message';

comment on column sys_opera_log.cost_time is 'request time-consuming (ms)';

comment on column sys_opera_log.opera_time is 'Operation Time';

comment on column sys_opera_log.created_time is 'Created';

create index ix_sys_opera_log_id
    on sys_opera_log (id);

create table sys_role
(
    id           serial
        primary key,
    name         varchar(20)              not null
        unique,
    status       integer                  not null,
    remark       text,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_role is 'Rolesheet';

comment on column sys_role.id is 'PRIMARY ID';

comment on column sys_role.name is 'Role Name';

comment on column sys_role.status is 'Role state (0 disabled 1)';

comment on column sys_role.remark is 'Remarks';

comment on column sys_role.created_time is 'Created';

comment on column sys_role.updated_time is 'Update Time';

create index ix_sys_role_id
    on sys_role (id);

create table sys_config
(
    id           serial
        primary key,
    name         varchar(20)              not null,
    type         varchar(20),
    key          varchar(50)              not null
        unique,
    value        text                     not null,
    is_frontend  integer                  not null,
    remark       text,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_config is 'Parameter Configuration Table';

comment on column sys_config.id is 'PRIMARY ID';

comment on column sys_config.name is 'Name';

comment on column sys_config.type is 'Type';

comment on column sys_config.key is 'Keyname';

comment on column sys_config.value is 'Key Value';

comment on column sys_config.is_frontend is 'Whether to frontend';

comment on column sys_config.remark is 'Remarks';

comment on column sys_config.created_time is 'Created';

comment on column sys_config.updated_time is 'Update Time';

create index ix_sys_config_id
    on sys_config (id);

create table sys_dict_type
(
    id           serial
        primary key,
    name         varchar(32)              not null,
    code         varchar(32)              not null
        unique,
    status       integer                  not null,
    remark       text,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_dict_type is 'Dictionary Type Table';

comment on column sys_dict_type.id is 'PRIMARY ID';

comment on column sys_dict_type.name is 'Dictionary Type Name';

comment on column sys_dict_type.code is 'Dictionary type encoding';

comment on column sys_dict_type.status is 'Status (0 disabled 1)';

comment on column sys_dict_type.remark is 'Remarks';

comment on column sys_dict_type.created_time is 'Created';

comment on column sys_dict_type.updated_time is 'Update Time';

create index ix_sys_dict_type_id
    on sys_dict_type (id);

create table sys_notice
(
    id           serial
        primary key,
    title        varchar(50)              not null,
    type         integer                  not null,
    author       varchar(16)              not null,
    source       varchar(50)              not null,
    status       integer                  not null,
    content      text                     not null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_notice is 'System notice bulletin form';

comment on column sys_notice.id is 'PRIMARY ID';

comment on column sys_notice.title is 'Title';

comment on column sys_notice.type is 'Type (0: circular, 1: bulletin)';

comment on column sys_notice.author is 'Author';

comment on column sys_notice.source is 'Sources of information';

comment on column sys_notice.status is 'Status (0: hidden, 1: displayed)';

comment on column sys_notice.content is 'Contents';

comment on column sys_notice.created_time is 'Created';

comment on column sys_notice.updated_time is 'Update Time';

create index ix_sys_notice_id
    on sys_notice (id);

create table gen_business
(
    id                      serial
        primary key,
    app_name                varchar(50)              not null,
    table_name              varchar(255)             not null
        unique,
    doc_comment             varchar(255)             not null,
    table_comment           varchar(255),
    class_name              varchar(50),
    schema_name             varchar(50),
    filename                varchar(50),
    default_datetime_column boolean                  not null,
    api_version             varchar(20)              not null,
    gen_path                varchar(255),
    remark                  text,
    created_time            timestamp with time zone not null,
    updated_time            timestamp with time zone
);

comment on table gen_business is 'Code Generation Business Sheet';

comment on column gen_business.id is 'PRIMARY ID';

comment on column gen_business.app_name is 'Application name (English)';

comment on column gen_business.table_name is 'Table name (English)';

comment on column gen_business.doc_comment is 'Document Comment (for function/parameter documents)';

comment on column gen_business.table_comment is 'Table Description';

comment on column gen_business.class_name is 'Base class name (defaultly English Table name)';

comment on column gen_business.schema_name is 'Schema Name (Default is Table Name)';

comment on column gen_business.filename is 'Base File Name (default is the English Table Name)';

comment on column gen_business.default_datetime_column is 'Existence of default timebar';

comment on column gen_business.api_version is 'code generation api version, default v1';

comment on column gen_business.gen_path is 'code generation path (default app root path)';

comment on column gen_business.remark is 'Remarks';

comment on column gen_business.created_time is 'Created';

comment on column gen_business.updated_time is 'Update Time';

create index ix_gen_business_id
    on gen_business (id);

create table sys_data_rule
(
    id           serial
        primary key,
    name         varchar(500)             not null
        unique,
    model        varchar(50)              not null,
    "column"     varchar(20)              not null,
    operator     integer                  not null,
    expression   integer                  not null,
    value        varchar(255)             not null,
    scope_id     integer
                                          references sys_data_scope
                                              on delete set null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_data_rule is 'Data rule sheet';

comment on column sys_data_rule.id is 'PRIMARY ID';

comment on column sys_data_rule.name is 'Name';

comment on column sys_data_rule.model is 'SQLA MODEL NAME, CORRESPONDING TO DATA_PERMISSION_MODES';

comment on column sys_data_rule."column" is 'Model field name';

comment on column sys_data_rule.operator is 'operators (0:and, 1:or)';

comment on column sys_data_rule.expression is 'expressions (0: =, 1:! =, 2:>, 3:>, 4:<, 5:: < , 6:in, 7:not_in)';

comment on column sys_data_rule.value is 'Rule value';

comment on column sys_data_rule.scope_id is 'DATA RANGE CORRELATION ID';

comment on column sys_data_rule.created_time is 'Created';

comment on column sys_data_rule.updated_time is 'Update Time';

create index ix_sys_data_rule_id
    on sys_data_rule (id);

create table sys_role_menu
(
    id      serial,
    role_id integer not null
        references sys_role
            on delete cascade,
    menu_id integer not null
        references sys_menu
            on delete cascade,
    primary key (id, role_id, menu_id)
);

comment on column sys_role_menu.id is 'PRIMARY KEY ID';

comment on column sys_role_menu.role_id is 'ROLE ID';

comment on column sys_role_menu.menu_id is 'MENU ID';

create unique index ix_sys_role_menu_id
    on sys_role_menu (id);

create table sys_role_data_scope
(
    id            serial,
    role_id       integer not null
        references sys_role
            on delete cascade,
    data_scope_id integer not null
        references sys_data_scope
            on delete cascade,
    primary key (id, role_id, data_scope_id)
);

comment on column sys_role_data_scope.id is 'PRIMARY ID';

comment on column sys_role_data_scope.role_id is 'ROLE ID';

comment on column sys_role_data_scope.data_scope_id is 'DATA RANGE ID';

create unique index ix_sys_role_data_scope_id
    on sys_role_data_scope (id);

create table sys_user
(
    id              serial
        primary key,
    uuid            varchar(50)              not null
        unique,
    username        varchar(20)              not null,
    nickname        varchar(20)              not null
        unique,
    password        varchar(255),
    salt            bytea,
    email           varchar(50)              not null,
    is_superuser    integer                  not null,
    is_staff        integer                  not null,
    status          integer                  not null,
    is_multi_login  integer                  not null,
    avatar          varchar(255),
    phone           varchar(11),
    join_time       timestamp with time zone not null,
    last_login_time timestamp with time zone,
    dept_id         integer
                                             references sys_dept
                                                 on delete set null,
    created_time    timestamp with time zone not null,
    updated_time    timestamp with time zone
);

comment on table sys_user is 'User Table';

comment on column sys_user.id is 'PRIMARY ID';

comment on column sys_user.username is 'Username';

comment on column sys_user.nickname is 'Nickname';

comment on column sys_user.password is 'Password';

comment on column sys_user.salt is 'Encrypted Salt';

comment on column sys_user.email is 'Mailbox';

comment on column sys_user.is_superuser is 'Super permission (0 No 1)';

comment on column sys_user.is_staff is 'Backstage management landing (0 no 1)';

comment on column sys_user.status is 'User account status (0 disabled 1)';

comment on column sys_user.is_multi_login is 'Repeated landing (0 No 1)';

comment on column sys_user.avatar is 'Heads';

comment on column sys_user.phone is 'Cell phone number';

comment on column sys_user.join_time is 'Date of registration';

comment on column sys_user.last_login_time is 'Last Login';

comment on column sys_user.dept_id is 'SECTOR-RELATED ID';

comment on column sys_user.created_time is 'Created';

comment on column sys_user.updated_time is 'Update Time';

create unique index ix_sys_user_email
    on sys_user (email);

create index ix_sys_user_id
    on sys_user (id);

create unique index ix_sys_user_username
    on sys_user (username);

create index ix_sys_user_status
    on sys_user (status);

create table sys_dict_data
(
    id           serial
        primary key,
    label        varchar(32)              not null
        unique,
    value        varchar(32)              not null,
    sort         integer                  not null,
    status       integer                  not null,
    remark       text,
    type_id      integer                  not null
        references sys_dict_type
            on delete cascade,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_dict_data is 'Dictionary Data Sheet';

comment on column sys_dict_data.id is 'PRIMARY ID';

comment on column sys_dict_data.label is 'Dictionary Label';

comment on column sys_dict_data.value is 'Dictionary values';

comment on column sys_dict_data.sort is 'Sort';

comment on column sys_dict_data.status is 'Status (0 disabled 1)';

comment on column sys_dict_data.remark is 'Remarks';

comment on column sys_dict_data.type_id is 'DICTIONARY TYPE ASSOCIATION ID';

comment on column sys_dict_data.created_time is 'Created';

comment on column sys_dict_data.updated_time is 'Update Time';

create index ix_sys_dict_data_id
    on sys_dict_data (id);

create table gen_column
(
    id              serial
        primary key,
    name            varchar(50) not null,
    comment         varchar(255),
    type            varchar(20) not null,
    pd_type         varchar(20) not null,
    "default"       text,
    sort            integer,
    length          integer     not null,
    is_pk           boolean     not null,
    is_nullable     boolean     not null,
    gen_business_id integer     not null
        references gen_business
            on delete cascade
);

comment on table gen_column is 'Code Generation Model List';

comment on column gen_column.id is 'PRIMARY ID';

comment on column gen_column.name is 'Column Name';

comment on column gen_column.comment is 'Column Description';

comment on column gen_column.type is 'SQLA MODEL COLUMN TYPE';

comment on column gen_column.pd_type is 'pydantic type for column type';

comment on column gen_column."default" is 'Column Default';

comment on column gen_column.sort is 'Column Sort';

comment on column gen_column.length is 'Column Length';

comment on column gen_column.is_pk is 'Whether the primary key';

comment on column gen_column.is_nullable is 'Could it be empty';

comment on column gen_column.gen_business_id is 'CODE GENERATION BUSINESS ID';

create index ix_gen_column_id
    on gen_column (id);

create table sys_user_role
(
    id      serial,
    user_id integer not null
        references sys_user
            on delete cascade,
    role_id integer not null
        references sys_role
            on delete cascade,
    primary key (id, user_id, role_id)
);

comment on column sys_user_role.id is 'PRIMARY KEY ID';

comment on column sys_user_role.user_id is 'USER ID';

comment on column sys_user_role.role_id is 'ROLE ID';

create unique index ix_sys_user_role_id
    on sys_user_role (id);

create table sys_user_social
(
    id           serial
        primary key,
    source       varchar(20)              not null,
    open_id      varchar(20),
    uid          varchar(20),
    union_id     varchar(20),
    scope        varchar(120),
    code         varchar(50),
    user_id      integer
                                          references sys_user
                                              on delete set null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_user_social is 'User Social Table (OAuth2)';

comment on column sys_user_social.id is 'PRIMARY ID';

comment on column sys_user_social.source is 'Third-party user sources';

comment on column sys_user_social.open_id is 'open id';

comment on column sys_user_social.uid is 'ID OF THIRD-PARTY USER';

comment on column sys_user_social.union_id is 'union id of third-party users';

comment on column sys_user_social.scope is 'Authority granted by third-party users';

comment on column sys_user_social.code is 'user\'s authorization code';

comment on column sys_user_social.user_id is 'USER LINK ID';

comment on column sys_user_social.created_time is 'Created';

comment on column sys_user_social.updated_time is 'Update Time';

create index ix_sys_user_social_id
    on sys_user_social (id);
