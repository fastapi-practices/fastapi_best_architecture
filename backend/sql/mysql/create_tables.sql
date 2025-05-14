create table gen_business
(
    id                      int auto_increment comment 'PRIMARY ID'
        primary key,
    app_name                varchar(50)  not null comment 'Application name (English)',
    table_name              varchar(255) not null comment 'Table name (English)',
    doc_comment             varchar(255) not null comment 'Document Comment (for function/parameter documents)',
    table_comment           varchar(255) null comment 'Table Description',
    class_name              varchar(50)  null comment 'Base class name (defaultly English Table name)',
    schema_name             varchar(50)  null comment 'Schema Name (Default is Table Name)',
    filename                varchar(50)  null comment 'Base File Name (default is the English Table Name)',
    default_datetime_column tinyint(1)   not null comment 'Existence of default timebar',
    api_version             varchar(20)  not null comment 'code generation api version, default v1',
    gen_path                varchar(255) null comment 'code generation path (default app root path)',
    remark                  longtext     null comment 'Remarks',
    created_time            datetime     not null comment 'Created',
    updated_time            datetime     null comment 'Update Time',
    constraint table_name
        unique (table_name)
)
    comment 'Code Generation Business Sheet';

create index ix_gen_business_id
    on gen_business (id);

create table gen_column
(
    id              int auto_increment comment 'PRIMARY ID'
        primary key,
    name            varchar(50)  not null comment 'Column Name',
    comment         varchar(255) null comment 'Column Description',
    type            varchar(20)  not null comment 'SQLA MODEL COLUMN TYPE',
    pd_type         varchar(20)  not null comment 'pydantic type for column type',
    `default`       longtext     null comment 'Column Default',
    sort            int          null comment 'Column Sort',
    length          int          not null comment 'Column Length',
    is_pk           tinyint(1)   not null comment 'Whether the primary key',
    is_nullable     tinyint(1)   not null comment 'Could it be empty',
    gen_business_id int          not null comment 'CODE GENERATION BUSINESS ID',
    constraint gen_column_ibfk_1
        foreign key (gen_business_id) references gen_business (id)
            on delete cascade
)
    comment 'Code Generation Model List';

create index gen_business_id
    on gen_column (gen_business_id);

create index ix_gen_column_id
    on gen_column (id);

create table sys_config
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(20) not null comment 'Name',
    type         varchar(20) null comment 'Type',
    `key`        varchar(50) not null comment 'Keyname',
    value        longtext    not null comment 'Key Value',
    is_frontend  tinyint(1)  not null comment 'Whether to frontend',
    remark       longtext    null comment 'Remarks',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint `key`
        unique (`key`)
)
    comment 'Parameter Configuration Table';

create index ix_sys_config_id
    on sys_config (id);

create table sys_data_scope
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(50) not null comment 'Name',
    status       int         not null comment 'Status (0 disabled 1)',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint name
        unique (name)
)
    comment 'Data Range Table';

create table sys_data_rule
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(500) not null comment 'Name',
    model        varchar(50)  not null comment 'SQLA MODEL NAME, CORRESPONDING TO DATA_PERMISSION_MODES',
    `column`     varchar(20)  not null comment 'Model field name',
    operator     int          not null comment 'operators (0:and, 1:or)',
    expression   int          not null comment 'expressions (0: =, 1:! =, 2:>, 3:>, 4:<, 5:: < , 6:in, 7:not_in)',
    value        varchar(255) not null comment 'Rule value',
    scope_id     int          null comment 'DATA RANGE CORRELATION ID',
    created_time datetime     not null comment 'Created',
    updated_time datetime     null comment 'Update Time',
    constraint name
        unique (name),
    constraint sys_data_rule_ibfk_1
        foreign key (scope_id) references sys_data_scope (id)
            on delete set null
)
    comment 'Data rule sheet';

create index ix_sys_data_rule_id
    on sys_data_rule (id);

create index scope_id
    on sys_data_rule (scope_id);

create index ix_sys_data_scope_id
    on sys_data_scope (id);

create table sys_dept
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(50) not null comment 'Department name',
    sort         int         not null comment 'Sort',
    leader       varchar(20) null comment 'Head',
    phone        varchar(11) null comment 'Cell phone',
    email        varchar(50) null comment 'Mailbox',
    status       int         not null comment 'Sector status (0 disabled 1)',
    del_flag     tinyint(1)  not null comment 'Delete sign (0 delete 1 exists)',
    parent_id    int         null comment 'PARENT ID',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint sys_dept_ibfk_1
        foreign key (parent_id) references sys_dept (id)
            on delete set null
)
    comment 'Sectoral table';

create index ix_sys_dept_id
    on sys_dept (id);

create index ix_sys_dept_parent_id
    on sys_dept (parent_id);

create table sys_dict_type
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(32) not null comment 'Dictionary Type Name',
    code         varchar(32) not null comment 'Dictionary type encoding',
    status       int         not null comment 'Status (0 disabled 1)',
    remark       longtext    null comment 'Remarks',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint code
        unique (code)
)
    comment 'Dictionary Type Table';

create table sys_dict_data
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    label        varchar(32) not null comment 'Dictionary Label',
    value        varchar(32) not null comment 'Dictionary values',
    sort         int         not null comment 'Sort',
    status       int         not null comment 'Status (0 disabled 1)',
    remark       longtext    null comment 'Remarks',
    type_id      int         not null comment 'DICTIONARY TYPE ASSOCIATION ID',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint label
        unique (label),
    constraint sys_dict_data_ibfk_1
        foreign key (type_id) references sys_dict_type (id)
            on delete cascade
)
    comment 'Dictionary Data Sheet';

create index ix_sys_dict_data_id
    on sys_dict_data (id);

create index type_id
    on sys_dict_data (type_id);

create index ix_sys_dict_type_id
    on sys_dict_type (id);

create table sys_login_log
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    user_uuid    varchar(50)  not null comment 'USERUID',
    username     varchar(20)  not null comment 'Username',
    status       int          not null comment 'Login status (0 failed)',
    ip           varchar(50)  not null comment 'LOGIN IP ADDRESS',
    country      varchar(50)  null comment 'Country',
    region       varchar(50)  null comment 'Region',
    city         varchar(50)  null comment 'Urban',
    user_agent   varchar(255) not null comment 'Request Header',
    os           varchar(50)  null comment 'Operating systems',
    browser      varchar(50)  null comment 'Browser',
    device       varchar(50)  null comment 'Equipment',
    msg          longtext     not null comment 'Message',
    login_time   datetime     not null comment 'Login Time',
    created_time datetime     not null comment 'Created'
)
    comment 'Login Login Table';

create index ix_sys_login_log_id
    on sys_login_log (id);

create table sys_menu
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    title        varchar(50)  not null comment 'Menu Title',
    name         varchar(50)  not null comment 'Menu Name',
    path         varchar(200) not null comment 'Route Address',
    sort         int          not null comment 'Sort',
    icon         varchar(100) null comment 'Menu Icon',
    type         int          not null comment 'Menu type (0 directory 1 menu 2 button)',
    component    varchar(255) null comment 'Component Path',
    perms        varchar(100) null comment 'Permission Identification',
    status       int          not null comment 'Menu status (0 disabled 1 normal)',
    display      int          not null comment 'Whether to show (0 no 1)',
    cache        int          not null comment 'Cache (0 No 1)',
    link         longtext     null comment 'Outlink Address',
    remark       longtext     null comment 'Remarks',
    parent_id    int          null comment 'PARENT MENU ID',
    created_time datetime     not null comment 'Created',
    updated_time datetime     null comment 'Update Time',
    constraint sys_menu_ibfk_1
        foreign key (parent_id) references sys_menu (id)
            on delete set null
)
    comment 'Menu Table';

create index ix_sys_menu_id
    on sys_menu (id);

create index ix_sys_menu_parent_id
    on sys_menu (parent_id);

create table sys_notice
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    title        varchar(50) not null comment 'Title',
    type         int         not null comment 'Type (0: circular, 1: bulletin)',
    author       varchar(16) not null comment 'Author',
    source       varchar(50) not null comment 'Sources of information',
    status       int         not null comment 'Status (0: hidden, 1: displayed)',
    content      longtext    not null comment 'Contents',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time'
)
    comment 'System notice bulletin form';

create index ix_sys_notice_id
    on sys_notice (id);

create table sys_opera_log
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    trace_id     varchar(32)  not null comment 'REQUEST TRACKING ID',
    username     varchar(20)  null comment 'Username',
    method       varchar(20)  not null comment 'Type of request',
    title        varchar(255) not null comment 'Operation module',
    path         varchar(500) not null comment 'Request Path',
    ip           varchar(50)  not null comment 'IP ADDRESS',
    country      varchar(50)  null comment 'Country',
    region       varchar(50)  null comment 'Region',
    city         varchar(50)  null comment 'Urban',
    user_agent   varchar(255) not null comment 'Request Header',
    os           varchar(50)  null comment 'Operating systems',
    browser      varchar(50)  null comment 'Browser',
    device       varchar(50)  null comment 'Equipment',
    args         json         null comment 'Request parameters',
    status       int          not null comment 'Operational status (0 anomaly 1)',
    code         varchar(20)  not null comment 'Operational status code',
    msg          longtext     null comment 'Message',
    cost_time    float        not null comment 'request time-consuming (ms)',
    opera_time   datetime     not null comment 'Operation Time',
    created_time datetime     not null comment 'Created'
)
    comment 'Operations Log Table';

create index ix_sys_opera_log_id
    on sys_opera_log (id);

create table sys_role
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    name         varchar(20) not null comment 'Role Name',
    status       int         not null comment 'Role state (0 disabled 1)',
    remark       longtext    null comment 'Remarks',
    created_time datetime    not null comment 'Created',
    updated_time datetime    null comment 'Update Time',
    constraint name
        unique (name)
)
    comment 'Rolesheet';

create index ix_sys_role_id
    on sys_role (id);

create table sys_role_data_scope
(
    id            int auto_increment comment 'PRIMARY ID',
    role_id       int not null comment 'ROLE ID',
    data_scope_id int not null comment 'DATA RANGE ID',
    primary key (id, role_id, data_scope_id),
    constraint ix_sys_role_data_scope_id
        unique (id),
    constraint sys_role_data_scope_ibfk_1
        foreign key (role_id) references sys_role (id)
            on delete cascade,
    constraint sys_role_data_scope_ibfk_2
        foreign key (data_scope_id) references sys_data_scope (id)
            on delete cascade
);

create index data_scope_id
    on sys_role_data_scope (data_scope_id);

create index role_id
    on sys_role_data_scope (role_id);

create table sys_role_menu
(
    id      int auto_increment comment 'PRIMARY KEY ID',
    role_id int not null comment 'ROLE ID',
    menu_id int not null comment 'MENU ID',
    primary key (id, role_id, menu_id),
    constraint ix_sys_role_menu_id
        unique (id),
    constraint sys_role_menu_ibfk_1
        foreign key (role_id) references sys_role (id)
            on delete cascade,
    constraint sys_role_menu_ibfk_2
        foreign key (menu_id) references sys_menu (id)
            on delete cascade
);

create index menu_id
    on sys_role_menu (menu_id);

create index role_id
    on sys_role_menu (role_id);

create table sys_user
(
    id              int auto_increment comment 'PRIMARY ID'
        primary key,
    uuid            varchar(50)    not null,
    username        varchar(20)    not null comment 'Username',
    nickname        varchar(20)    not null comment 'Nickname',
    password        varchar(255)   null comment 'Password',
    salt            varbinary(255) null comment 'Encrypted Salt',
    email           varchar(50)    not null comment 'Mailbox',
    is_superuser    tinyint(1)     not null comment 'Super permission (0 No 1)',
    is_staff        tinyint(1)     not null comment 'Backstage management landing (0 no 1)',
    status          int            not null comment 'User account status (0 disabled 1)',
    is_multi_login  tinyint(1)     not null comment 'Repeated landing (0 No 1)',
    avatar          varchar(255)   null comment 'Heads',
    phone           varchar(11)    null comment 'Cell phone number',
    join_time       datetime       not null comment 'Date of registration',
    last_login_time datetime       null comment 'Last Login',
    dept_id         int            null comment 'SECTOR-RELATED ID',
    created_time    datetime       not null comment 'Created',
    updated_time    datetime       null comment 'Update Time',
    constraint ix_sys_user_email
        unique (email),
    constraint ix_sys_user_username
        unique (username),
    constraint nickname
        unique (nickname),
    constraint uuid
        unique (uuid),
    constraint sys_user_ibfk_1
        foreign key (dept_id) references sys_dept (id)
            on delete set null
)
    comment 'User Table';

create index dept_id
    on sys_user (dept_id);

create index ix_sys_user_id
    on sys_user (id);

create index ix_sys_user_status
    on sys_user (status);

create table sys_user_role
(
    id      int auto_increment comment 'PRIMARY KEY ID',
    user_id int not null comment 'USER ID',
    role_id int not null comment 'ROLE ID',
    primary key (id, user_id, role_id),
    constraint ix_sys_user_role_id
        unique (id),
    constraint sys_user_role_ibfk_1
        foreign key (user_id) references sys_user (id)
            on delete cascade,
    constraint sys_user_role_ibfk_2
        foreign key (role_id) references sys_role (id)
            on delete cascade
);

create index role_id
    on sys_user_role (role_id);

create index user_id
    on sys_user_role (user_id);

create table sys_user_social
(
    id           int auto_increment comment 'PRIMARY ID'
        primary key,
    source       varchar(20)  not null comment 'Third-party user sources',
    open_id      varchar(20)  null comment 'open id',
    uid          varchar(20)  null comment 'ID OF THIRD-PARTY USER',
    union_id     varchar(20)  null comment 'union id of third-party users',
    scope        varchar(120) null comment 'Authority granted by third-party users',
    code         varchar(50)  null comment 'user\'s authorization code',
    user_id      int          null comment 'USER LINK ID',
    created_time datetime     not null comment 'Created',
    updated_time datetime     null comment 'Update Time',
    constraint sys_user_social_ibfk_1
        foreign key (user_id) references sys_user (id)
            on delete set null
)
    comment 'User Social Table (OAuth2)';

create index ix_sys_user_social_id
    on sys_user_social (id);

create index user_id
    on sys_user_social (user_id);
