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

comment on table sys_data_scope is '数据范围表';

comment on column sys_data_scope.id is '主键 ID';

comment on column sys_data_scope.name is '名称';

comment on column sys_data_scope.status is '状态（0停用 1正常）';

comment on column sys_data_scope.created_time is '创建时间';

comment on column sys_data_scope.updated_time is '更新时间';

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

comment on table sys_dept is '部门表';

comment on column sys_dept.id is '主键 ID';

comment on column sys_dept.name is '部门名称';

comment on column sys_dept.sort is '排序';

comment on column sys_dept.leader is '负责人';

comment on column sys_dept.phone is '手机';

comment on column sys_dept.email is '邮箱';

comment on column sys_dept.status is '部门状态(0停用 1正常)';

comment on column sys_dept.del_flag is '删除标志（0删除 1存在）';

comment on column sys_dept.parent_id is '父部门ID';

comment on column sys_dept.created_time is '创建时间';

comment on column sys_dept.updated_time is '更新时间';

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

comment on table sys_login_log is '登录日志表';

comment on column sys_login_log.id is '主键 ID';

comment on column sys_login_log.user_uuid is '用户UUID';

comment on column sys_login_log.username is '用户名';

comment on column sys_login_log.status is '登录状态(0失败 1成功)';

comment on column sys_login_log.ip is '登录IP地址';

comment on column sys_login_log.country is '国家';

comment on column sys_login_log.region is '地区';

comment on column sys_login_log.city is '城市';

comment on column sys_login_log.user_agent is '请求头';

comment on column sys_login_log.os is '操作系统';

comment on column sys_login_log.browser is '浏览器';

comment on column sys_login_log.device is '设备';

comment on column sys_login_log.msg is '提示消息';

comment on column sys_login_log.login_time is '登录时间';

comment on column sys_login_log.created_time is '创建时间';

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

comment on table sys_menu is '菜单表';

comment on column sys_menu.id is '主键 ID';

comment on column sys_menu.title is '菜单标题';

comment on column sys_menu.name is '菜单名称';

comment on column sys_menu.path is '路由地址';

comment on column sys_menu.sort is '排序';

comment on column sys_menu.icon is '菜单图标';

comment on column sys_menu.type is '菜单类型（0目录 1菜单 2按钮）';

comment on column sys_menu.component is '组件路径';

comment on column sys_menu.perms is '权限标识';

comment on column sys_menu.status is '菜单状态（0停用 1正常）';

comment on column sys_menu.display is '是否显示（0否 1是）';

comment on column sys_menu.cache is '是否缓存（0否 1是）';

comment on column sys_menu.link is '外链地址';

comment on column sys_menu.remark is '备注';

comment on column sys_menu.parent_id is '父菜单ID';

comment on column sys_menu.created_time is '创建时间';

comment on column sys_menu.updated_time is '更新时间';

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

comment on table sys_opera_log is '操作日志表';

comment on column sys_opera_log.id is '主键 ID';

comment on column sys_opera_log.trace_id is '请求跟踪 ID';

comment on column sys_opera_log.username is '用户名';

comment on column sys_opera_log.method is '请求类型';

comment on column sys_opera_log.title is '操作模块';

comment on column sys_opera_log.path is '请求路径';

comment on column sys_opera_log.ip is 'IP地址';

comment on column sys_opera_log.country is '国家';

comment on column sys_opera_log.region is '地区';

comment on column sys_opera_log.city is '城市';

comment on column sys_opera_log.user_agent is '请求头';

comment on column sys_opera_log.os is '操作系统';

comment on column sys_opera_log.browser is '浏览器';

comment on column sys_opera_log.device is '设备';

comment on column sys_opera_log.args is '请求参数';

comment on column sys_opera_log.status is '操作状态（0异常 1正常）';

comment on column sys_opera_log.code is '操作状态码';

comment on column sys_opera_log.msg is '提示消息';

comment on column sys_opera_log.cost_time is '请求耗时（ms）';

comment on column sys_opera_log.opera_time is '操作时间';

comment on column sys_opera_log.created_time is '创建时间';

create index ix_sys_opera_log_id
    on sys_opera_log (id);

create table sys_role
(
    id               serial
        primary key,
    name             varchar(20)              not null
        unique,
    status           integer                  not null,
    is_filter_scopes integer                  not null,
    remark           text,
    created_time     timestamp with time zone not null,
    updated_time     timestamp with time zone
);

comment on table sys_role is '角色表';

comment on column sys_role.id is '主键 ID';

comment on column sys_role.name is '角色名称';

comment on column sys_role.status is '角色状态（0停用 1正常）';

comment on column sys_role.is_filter_scopes is '过滤数据权限(0否 1是)';

comment on column sys_role.remark is '备注';

comment on column sys_role.created_time is '创建时间';

comment on column sys_role.updated_time is '更新时间';

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

comment on table sys_config is '参数配置表';

comment on column sys_config.id is '主键 ID';

comment on column sys_config.name is '名称';

comment on column sys_config.type is '类型';

comment on column sys_config.key is '键名';

comment on column sys_config.value is '键值';

comment on column sys_config.is_frontend is '是否前端';

comment on column sys_config.remark is '备注';

comment on column sys_config.created_time is '创建时间';

comment on column sys_config.updated_time is '更新时间';

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

comment on table sys_dict_type is '字典类型表';

comment on column sys_dict_type.id is '主键 ID';

comment on column sys_dict_type.name is '字典类型名称';

comment on column sys_dict_type.code is '字典类型编码';

comment on column sys_dict_type.status is '状态（0停用 1正常）';

comment on column sys_dict_type.remark is '备注';

comment on column sys_dict_type.created_time is '创建时间';

comment on column sys_dict_type.updated_time is '更新时间';

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

comment on table sys_notice is '系统通知公告表';

comment on column sys_notice.id is '主键 ID';

comment on column sys_notice.title is '标题';

comment on column sys_notice.type is '类型（0：通知、1：公告）';

comment on column sys_notice.author is '作者';

comment on column sys_notice.source is '信息来源';

comment on column sys_notice.status is '状态（0：隐藏、1：显示）';

comment on column sys_notice.content is '内容';

comment on column sys_notice.created_time is '创建时间';

comment on column sys_notice.updated_time is '更新时间';

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

comment on table gen_business is '代码生成业务表';

comment on column gen_business.id is '主键 ID';

comment on column gen_business.app_name is '应用名称（英文）';

comment on column gen_business.table_name is '表名称（英文）';

comment on column gen_business.doc_comment is '文档注释（用于函数/参数文档）';

comment on column gen_business.table_comment is '表描述';

comment on column gen_business.class_name is '基础类名（默认为英文表名称）';

comment on column gen_business.schema_name is 'Schema 名称 (默认为英文表名称)';

comment on column gen_business.filename is '基础文件名（默认为英文表名称）';

comment on column gen_business.default_datetime_column is '是否存在默认时间列';

comment on column gen_business.api_version is '代码生成 api 版本，默认为 v1';

comment on column gen_business.gen_path is '代码生成路径（默认为 app 根路径）';

comment on column gen_business.remark is '备注';

comment on column gen_business.created_time is '创建时间';

comment on column gen_business.updated_time is '更新时间';

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

comment on table sys_data_rule is '数据规则表';

comment on column sys_data_rule.id is '主键 ID';

comment on column sys_data_rule.name is '名称';

comment on column sys_data_rule.model is 'SQLA 模型名，对应 DATA_PERMISSION_MODELS 键名';

comment on column sys_data_rule."column" is '模型字段名';

comment on column sys_data_rule.operator is '运算符（0：and、1：or）';

comment on column sys_data_rule.expression is '表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）';

comment on column sys_data_rule.value is '规则值';

comment on column sys_data_rule.scope_id is '数据范围关联 ID';

comment on column sys_data_rule.created_time is '创建时间';

comment on column sys_data_rule.updated_time is '更新时间';

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

comment on column sys_role_menu.id is '主键ID';

comment on column sys_role_menu.role_id is '角色ID';

comment on column sys_role_menu.menu_id is '菜单ID';

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

comment on column sys_role_data_scope.id is '主键 ID';

comment on column sys_role_data_scope.role_id is '角色 ID';

comment on column sys_role_data_scope.data_scope_id is '数据范围 ID';

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

comment on table sys_user is '用户表';

comment on column sys_user.id is '主键 ID';

comment on column sys_user.username is '用户名';

comment on column sys_user.nickname is '昵称';

comment on column sys_user.password is '密码';

comment on column sys_user.salt is '加密盐';

comment on column sys_user.email is '邮箱';

comment on column sys_user.is_superuser is '超级权限(0否 1是)';

comment on column sys_user.is_staff is '后台管理登陆(0否 1是)';

comment on column sys_user.status is '用户账号状态(0停用 1正常)';

comment on column sys_user.is_multi_login is '是否重复登陆(0否 1是)';

comment on column sys_user.avatar is '头像';

comment on column sys_user.phone is '手机号';

comment on column sys_user.join_time is '注册时间';

comment on column sys_user.last_login_time is '上次登录';

comment on column sys_user.dept_id is '部门关联ID';

comment on column sys_user.created_time is '创建时间';

comment on column sys_user.updated_time is '更新时间';

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

comment on table sys_dict_data is '字典数据表';

comment on column sys_dict_data.id is '主键 ID';

comment on column sys_dict_data.label is '字典标签';

comment on column sys_dict_data.value is '字典值';

comment on column sys_dict_data.sort is '排序';

comment on column sys_dict_data.status is '状态（0停用 1正常）';

comment on column sys_dict_data.remark is '备注';

comment on column sys_dict_data.type_id is '字典类型关联ID';

comment on column sys_dict_data.created_time is '创建时间';

comment on column sys_dict_data.updated_time is '更新时间';

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

comment on table gen_column is '代码生成模型列表';

comment on column gen_column.id is '主键 ID';

comment on column gen_column.name is '列名称';

comment on column gen_column.comment is '列描述';

comment on column gen_column.type is 'SQLA 模型列类型';

comment on column gen_column.pd_type is '列类型对应的 pydantic 类型';

comment on column gen_column."default" is '列默认值';

comment on column gen_column.sort is '列排序';

comment on column gen_column.length is '列长度';

comment on column gen_column.is_pk is '是否主键';

comment on column gen_column.is_nullable is '是否可为空';

comment on column gen_column.gen_business_id is '代码生成业务ID';

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

comment on column sys_user_role.id is '主键ID';

comment on column sys_user_role.user_id is '用户ID';

comment on column sys_user_role.role_id is '角色ID';

create unique index ix_sys_user_role_id
    on sys_user_role (id);

create table sys_user_social
(
    id           serial
        primary key,
    source       varchar(20)              not null,
    open_id      varchar(20),
    sid          varchar(20),
    union_id     varchar(20),
    scope        varchar(120),
    code         varchar(50),
    user_id      integer
                                          references sys_user
                                              on delete set null,
    created_time timestamp with time zone not null,
    updated_time timestamp with time zone
);

comment on table sys_user_social is '用户社交表（OAuth2）';

comment on column sys_user_social.id is '主键 ID';

comment on column sys_user_social.source is '第三方用户来源';

comment on column sys_user_social.open_id is '第三方用户 open id';

comment on column sys_user_social.uid is '第三方用户 ID';

comment on column sys_user_social.union_id is '第三方用户 union id';

comment on column sys_user_social.scope is '第三方用户授予的权限';

comment on column sys_user_social.code is '用户的授权 code';

comment on column sys_user_social.user_id is '用户关联ID';

comment on column sys_user_social.created_time is '创建时间';

comment on column sys_user_social.updated_time is '更新时间';

create index ix_sys_user_social_id
    on sys_user_social (id);
