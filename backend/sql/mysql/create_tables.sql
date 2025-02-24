create table sys_api
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(50)  not null comment 'api名称',
    method       varchar(16)  not null comment '请求方法',
    path         varchar(500) not null comment 'api路径',
    remark       longtext     null comment '备注',
    created_time datetime     not null comment '创建时间',
    updated_time datetime     null comment '更新时间',
    constraint name
        unique (name)
);

create index ix_sys_api_id
    on sys_api (id);

create table sys_casbin_rule
(
    id    int auto_increment comment '主键id'
        primary key,
    ptype varchar(255) not null comment '策略类型: p / g',
    v0    varchar(255) not null comment '角色ID / 用户uuid',
    v1    longtext     not null comment 'api路径 / 角色名称',
    v2    varchar(255) null comment '请求方法',
    v3    varchar(255) null,
    v4    varchar(255) null,
    v5    varchar(255) null
);

create index ix_sys_casbin_rule_id
    on sys_casbin_rule (id);

create table sys_config
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(20) not null comment '名称',
    type         varchar(20) null comment '类型',
    `key`        varchar(50) not null comment '键名',
    value        longtext    not null comment '键值',
    is_frontend  tinyint(1)  not null comment '是否前端',
    remark       longtext    null comment '备注',
    created_time datetime    not null comment '创建时间',
    updated_time datetime    null comment '更新时间',
    constraint `key`
        unique (`key`)
);

create index ix_sys_config_id
    on sys_config (id);

create table sys_data_rule
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(255) not null comment '规则名称',
    model        varchar(50)  not null comment 'SQLA 模型类',
    `column`     varchar(20)  not null comment '数据库字段',
    operator     int          not null comment '运算符（0：and、1：or）',
    expression   int          not null comment '表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）',
    value        varchar(255) not null comment '规则值',
    created_time datetime     not null comment '创建时间',
    updated_time datetime     null comment '更新时间',
    constraint name
        unique (name)
);

create index ix_sys_data_rule_id
    on sys_data_rule (id);

create table sys_dept
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(50) not null comment '部门名称',
    sort         int         not null comment '排序',
    leader       varchar(20) null comment '负责人',
    phone        varchar(11) null comment '手机',
    email        varchar(50) null comment '邮箱',
    status       int         not null comment '部门状态(0停用 1正常)',
    del_flag     tinyint(1)  not null comment '删除标志（0删除 1存在）',
    parent_id    int         null comment '父部门ID',
    created_time datetime    not null comment '创建时间',
    updated_time datetime    null comment '更新时间',
    constraint sys_dept_ibfk_1
        foreign key (parent_id) references sys_dept (id)
            on delete set null
);

create index ix_sys_dept_id
    on sys_dept (id);

create index ix_sys_dept_parent_id
    on sys_dept (parent_id);

create table sys_dict_type
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(32) not null comment '字典类型名称',
    code         varchar(32) not null comment '字典类型编码',
    status       int         not null comment '状态（0停用 1正常）',
    remark       longtext    null comment '备注',
    created_time datetime    not null comment '创建时间',
    updated_time datetime    null comment '更新时间',
    constraint code
        unique (code),
    constraint name
        unique (name)
);

create table sys_dict_data
(
    id           int auto_increment comment '主键id'
        primary key,
    label        varchar(32) not null comment '字典标签',
    value        varchar(32) not null comment '字典值',
    sort         int         not null comment '排序',
    status       int         not null comment '状态（0停用 1正常）',
    remark       longtext    null comment '备注',
    type_id      int         not null comment '字典类型关联ID',
    created_time datetime    not null comment '创建时间',
    updated_time datetime    null comment '更新时间',
    constraint label
        unique (label),
    constraint value
        unique (value),
    constraint sys_dict_data_ibfk_1
        foreign key (type_id) references sys_dict_type (id)
            on delete cascade
);

create index ix_sys_dict_data_id
    on sys_dict_data (id);

create index type_id
    on sys_dict_data (type_id);

create index ix_sys_dict_type_id
    on sys_dict_type (id);

create table sys_gen_business
(
    id                      int auto_increment comment '主键id'
        primary key,
    app_name                varchar(50)  not null comment '应用名称（英文）',
    table_name_en           varchar(255) not null comment '表名称（英文）',
    table_name_zh           varchar(255) not null comment '表名称（中文）',
    table_simple_name_zh    varchar(255) not null comment '表名称（中文简称）',
    table_comment           varchar(255) null comment '表描述',
    schema_name             varchar(255) null comment 'Schema 名称 (默认为英文表名称)',
    default_datetime_column tinyint(1)   not null comment '是否存在默认时间列',
    api_version             varchar(20)  not null comment '代码生成 api 版本，默认为 v1',
    gen_path                varchar(255) null comment '代码生成路径（默认为 app 根路径）',
    remark                  longtext     null comment '备注',
    created_time            datetime     not null comment '创建时间',
    updated_time            datetime     null comment '更新时间',
    constraint table_name_en
        unique (table_name_en)
);

create index ix_sys_gen_business_id
    on sys_gen_business (id);

create table sys_gen_model
(
    id              int auto_increment comment '主键id'
        primary key,
    name            varchar(50)  not null comment '列名称',
    comment         varchar(255) null comment '列描述',
    type            varchar(20)  not null comment 'SQLA 模型列类型',
    pd_type         varchar(20)  not null comment '列类型对应的 pydantic 类型',
    `default`       longtext     null comment '列默认值',
    sort            int          null comment '列排序',
    length          int          not null comment '列长度',
    is_pk           tinyint(1)   not null comment '是否主键',
    is_nullable     tinyint(1)   not null comment '是否可为空',
    gen_business_id int          not null comment '代码生成业务ID',
    constraint sys_gen_model_ibfk_1
        foreign key (gen_business_id) references sys_gen_business (id)
            on delete cascade
);

create index gen_business_id
    on sys_gen_model (gen_business_id);

create index ix_sys_gen_model_id
    on sys_gen_model (id);

create table sys_login_log
(
    id           int auto_increment comment '主键id'
        primary key,
    user_uuid    varchar(50)  not null comment '用户UUID',
    username     varchar(20)  not null comment '用户名',
    status       int          not null comment '登录状态(0失败 1成功)',
    ip           varchar(50)  not null comment '登录IP地址',
    country      varchar(50)  null comment '国家',
    region       varchar(50)  null comment '地区',
    city         varchar(50)  null comment '城市',
    user_agent   varchar(255) not null comment '请求头',
    os           varchar(50)  null comment '操作系统',
    browser      varchar(50)  null comment '浏览器',
    device       varchar(50)  null comment '设备',
    msg          longtext     not null comment '提示消息',
    login_time   datetime     not null comment '登录时间',
    created_time datetime     not null comment '创建时间'
);

create index ix_sys_login_log_id
    on sys_login_log (id);

create table sys_menu
(
    id           int auto_increment comment '主键id'
        primary key,
    title        varchar(50)  not null comment '菜单标题',
    name         varchar(50)  not null comment '菜单名称',
    sort         int          not null comment '排序',
    icon         varchar(100) null comment '菜单图标',
    path         varchar(200) null comment '路由地址',
    menu_type    int          not null comment '菜单类型（0目录 1菜单 2按钮）',
    component    varchar(255) null comment '组件路径',
    perms        varchar(100) null comment '权限标识',
    status       int          not null comment '菜单状态（0停用 1正常）',
    display      int          not null comment '是否显示（0否 1是）',
    cache        int          not null comment '是否缓存（0否 1是）',
    remark       longtext     null comment '备注',
    parent_id    int          null comment '父菜单ID',
    created_time datetime     not null comment '创建时间',
    updated_time datetime     null comment '更新时间',
    constraint sys_menu_ibfk_1
        foreign key (parent_id) references sys_menu (id)
            on delete set null
);

create index ix_sys_menu_id
    on sys_menu (id);

create index ix_sys_menu_parent_id
    on sys_menu (parent_id);

create table sys_opera_log
(
    id           int auto_increment comment '主键id'
        primary key,
    trace_id     varchar(32)  not null comment '请求跟踪 ID',
    username     varchar(20)  null comment '用户名',
    method       varchar(20)  not null comment '请求类型',
    title        varchar(255) not null comment '操作模块',
    path         varchar(500) not null comment '请求路径',
    ip           varchar(50)  not null comment 'IP地址',
    country      varchar(50)  null comment '国家',
    region       varchar(50)  null comment '地区',
    city         varchar(50)  null comment '城市',
    user_agent   varchar(255) not null comment '请求头',
    os           varchar(50)  null comment '操作系统',
    browser      varchar(50)  null comment '浏览器',
    device       varchar(50)  null comment '设备',
    args         json         null comment '请求参数',
    status       int          not null comment '操作状态（0异常 1正常）',
    code         varchar(20)  not null comment '操作状态码',
    msg          longtext     null comment '提示消息',
    cost_time    float        not null comment '请求耗时（ms）',
    opera_time   datetime     not null comment '操作时间',
    created_time datetime     not null comment '创建时间'
);

create index ix_sys_opera_log_id
    on sys_opera_log (id);

create table sys_role
(
    id           int auto_increment comment '主键id'
        primary key,
    name         varchar(20) not null comment '角色名称',
    status       int         not null comment '角色状态（0停用 1正常）',
    remark       longtext    null comment '备注',
    created_time datetime    not null comment '创建时间',
    updated_time datetime    null comment '更新时间',
    constraint name
        unique (name)
);

create index ix_sys_role_id
    on sys_role (id);

create table sys_role_data_rule
(
    id           int auto_increment comment '主键ID',
    role_id      int not null comment '角色ID',
    data_rule_id int not null comment '数据权限规则ID',
    primary key (id, role_id, data_rule_id),
    constraint ix_sys_role_data_rule_id
        unique (id),
    constraint sys_role_data_rule_ibfk_1
        foreign key (role_id) references sys_role (id)
            on delete cascade,
    constraint sys_role_data_rule_ibfk_2
        foreign key (data_rule_id) references sys_data_rule (id)
            on delete cascade
);

create index data_rule_id
    on sys_role_data_rule (data_rule_id);

create index role_id
    on sys_role_data_rule (role_id);

create table sys_role_menu
(
    id      int auto_increment comment '主键ID',
    role_id int not null comment '角色ID',
    menu_id int not null comment '菜单ID',
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
    id              int auto_increment comment '主键id'
        primary key,
    uuid            varchar(50)    not null,
    username        varchar(20)    not null comment '用户名',
    nickname        varchar(20)    not null comment '昵称',
    password        varchar(255)   null comment '密码',
    salt            varbinary(255) null comment '加密盐',
    email           varchar(50)    not null comment '邮箱',
    is_superuser    tinyint(1)     not null comment '超级权限(0否 1是)',
    is_staff        tinyint(1)     not null comment '后台管理登陆(0否 1是)',
    status          int            not null comment '用户账号状态(0停用 1正常)',
    is_multi_login  tinyint(1)     not null comment '是否重复登陆(0否 1是)',
    avatar          varchar(255)   null comment '头像',
    phone           varchar(11)    null comment '手机号',
    join_time       datetime       not null comment '注册时间',
    last_login_time datetime       null comment '上次登录',
    dept_id         int            null comment '部门关联ID',
    created_time    datetime       not null comment '创建时间',
    updated_time    datetime       null comment '更新时间',
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
);

create index dept_id
    on sys_user (dept_id);

create index ix_sys_user_id
    on sys_user (id);

create table sys_user_role
(
    id      int auto_increment comment '主键ID',
    user_id int not null comment '用户ID',
    role_id int not null comment '角色ID',
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
    id           int auto_increment comment '主键id'
        primary key,
    source       varchar(20)  not null comment '第三方用户来源',
    open_id      varchar(20)  null comment '第三方用户的 open id',
    uid          varchar(20)  null comment '第三方用户的 ID',
    union_id     varchar(20)  null comment '第三方用户的 union id',
    scope        varchar(120) null comment '第三方用户授予的权限',
    code         varchar(50)  null comment '用户的授权 code',
    user_id      int          null comment '用户关联ID',
    created_time datetime     not null comment '创建时间',
    updated_time datetime     null comment '更新时间',
    constraint sys_user_social_ibfk_1
        foreign key (user_id) references sys_user (id)
            on delete set null
);

create index ix_sys_user_social_id
    on sys_user_social (id);

create index user_id
    on sys_user_social (user_id);
