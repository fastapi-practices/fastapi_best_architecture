CREATE TABLE alembic_version
(
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

CREATE TABLE sys_api
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    name         VARCHAR(50)  NOT NULL COMMENT 'api名称',
    method       VARCHAR(16)  NOT NULL COMMENT '请求方法',
    path         VARCHAR(500) NOT NULL COMMENT 'api路径',
    remark       LONGTEXT COMMENT '备注',
    created_time DATETIME     NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE INDEX ix_sys_api_id ON sys_api (id);

CREATE TABLE sys_casbin_rule
(
    id    INTEGER      NOT NULL COMMENT '主键id' AUTO_INCREMENT,
    ptype VARCHAR(255) NOT NULL COMMENT '策略类型: p 或者 g',
    v0    VARCHAR(255) NOT NULL COMMENT '角色 / 用户uuid',
    v1    LONGTEXT     NOT NULL COMMENT 'api路径 / 角色名称',
    v2    VARCHAR(255) COMMENT '请求方法',
    v3    VARCHAR(255),
    v4    VARCHAR(255),
    v5    VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_casbin_rule_id ON sys_casbin_rule (id);

CREATE TABLE sys_dept
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(50) NOT NULL COMMENT '部门名称',
    level        INTEGER     NOT NULL COMMENT '部门层级',
    sort         INTEGER     NOT NULL COMMENT '排序',
    leader       VARCHAR(20) COMMENT '负责人',
    phone        VARCHAR(11) COMMENT '手机',
    email        VARCHAR(50) COMMENT '邮箱',
    status       INTEGER     NOT NULL COMMENT '部门状态(0停用 1正常)',
    del_flag     BOOL        NOT NULL COMMENT '删除标志（0删除 1存在）',
    parent_id    INTEGER COMMENT '父部门ID',
    created_time DATETIME    NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES sys_dept (id) ON DELETE SET NULL
);

CREATE INDEX ix_sys_dept_id ON sys_dept (id);

CREATE INDEX ix_sys_dept_parent_id ON sys_dept (parent_id);

CREATE TABLE sys_dict_type
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(32) NOT NULL COMMENT '字典类型名称',
    code         VARCHAR(32) NOT NULL COMMENT '字典类型编码',
    status       INTEGER     NOT NULL COMMENT '状态（0停用 1正常）',
    remark       LONGTEXT COMMENT '备注',
    created_time DATETIME    NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE (code),
    UNIQUE (name)
);

CREATE INDEX ix_sys_dict_type_id ON sys_dict_type (id);

CREATE TABLE sys_login_log
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    user_uuid    VARCHAR(50)  NOT NULL COMMENT '用户UUID',
    username     VARCHAR(20)  NOT NULL COMMENT '用户名',
    status       INTEGER      NOT NULL COMMENT '登录状态(0失败 1成功)',
    ip           VARCHAR(50)  NOT NULL COMMENT '登录IP地址',
    country      VARCHAR(50) COMMENT '国家',
    region       VARCHAR(50) COMMENT '地区',
    city         VARCHAR(50) COMMENT '城市',
    user_agent   VARCHAR(255) NOT NULL COMMENT '请求头',
    os           VARCHAR(50) COMMENT '操作系统',
    browser      VARCHAR(50) COMMENT '浏览器',
    device       VARCHAR(50) COMMENT '设备',
    msg          LONGTEXT     NOT NULL COMMENT '提示消息',
    login_time   DATETIME     NOT NULL COMMENT '登录时间',
    created_time DATETIME     NOT NULL COMMENT '创建时间',
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_login_log_id ON sys_login_log (id);

CREATE TABLE sys_menu
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    title        VARCHAR(50) NOT NULL COMMENT '菜单标题',
    name         VARCHAR(50) NOT NULL COMMENT '菜单名称',
    level        INTEGER     NOT NULL COMMENT '菜单层级',
    sort         INTEGER     NOT NULL COMMENT '排序',
    icon         VARCHAR(100) COMMENT '菜单图标',
    path         VARCHAR(200) COMMENT '路由地址',
    menu_type    INTEGER     NOT NULL COMMENT '菜单类型（0目录 1菜单 2按钮）',
    component    VARCHAR(255) COMMENT '组件路径',
    perms        VARCHAR(100) COMMENT '权限标识',
    status       INTEGER     NOT NULL COMMENT '菜单状态（0停用 1正常）',
    `show`       INTEGER     NOT NULL COMMENT '是否显示（0否 1是）',
    cache        INTEGER     NOT NULL COMMENT '是否缓存（0否 1是）',
    remark       LONGTEXT COMMENT '备注',
    parent_id    INTEGER COMMENT '父菜单ID',
    created_time DATETIME    NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES sys_menu (id) ON DELETE SET NULL
);

CREATE INDEX ix_sys_menu_id ON sys_menu (id);

CREATE INDEX ix_sys_menu_parent_id ON sys_menu (parent_id);

CREATE TABLE sys_opera_log
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    username     VARCHAR(20) COMMENT '用户名',
    method       VARCHAR(20)  NOT NULL COMMENT '请求类型',
    title        VARCHAR(255) NOT NULL COMMENT '操作模块',
    path         VARCHAR(500) NOT NULL COMMENT '请求路径',
    ip           VARCHAR(50)  NOT NULL COMMENT 'IP地址',
    country      VARCHAR(50) COMMENT '国家',
    region       VARCHAR(50) COMMENT '地区',
    city         VARCHAR(50) COMMENT '城市',
    user_agent   VARCHAR(255) NOT NULL COMMENT '请求头',
    os           VARCHAR(50) COMMENT '操作系统',
    browser      VARCHAR(50) COMMENT '浏览器',
    device       VARCHAR(50) COMMENT '设备',
    args         JSON COMMENT '请求参数',
    status       INTEGER      NOT NULL COMMENT '操作状态（0异常 1正常）',
    code         VARCHAR(20)  NOT NULL COMMENT '操作状态码',
    msg          LONGTEXT COMMENT '提示消息',
    cost_time    FLOAT        NOT NULL COMMENT '请求耗时ms',
    opera_time   DATETIME     NOT NULL COMMENT '操作时间',
    created_time DATETIME     NOT NULL COMMENT '创建时间',
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_opera_log_id ON sys_opera_log (id);

CREATE TABLE sys_role
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(20) NOT NULL COMMENT '角色名称',
    data_scope   INTEGER COMMENT '权限范围（1：全部数据权限 2：自定义数据权限）',
    status       INTEGER     NOT NULL COMMENT '角色状态（0停用 1正常）',
    remark       LONGTEXT COMMENT '备注',
    created_time DATETIME    NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE INDEX ix_sys_role_id ON sys_role (id);

CREATE TABLE sys_dict_data
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    label        VARCHAR(32) NOT NULL COMMENT '字典标签',
    value        VARCHAR(32) NOT NULL COMMENT '字典值',
    sort         INTEGER     NOT NULL COMMENT '排序',
    status       INTEGER     NOT NULL COMMENT '状态（0停用 1正常）',
    remark       LONGTEXT COMMENT '备注',
    type_id      INTEGER     NOT NULL COMMENT '字典类型关联ID',
    created_time DATETIME    NOT NULL COMMENT '创建时间',
    updated_time DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (type_id) REFERENCES sys_dict_type (id),
    UNIQUE (label),
    UNIQUE (value)
);

CREATE INDEX ix_sys_dict_data_id ON sys_dict_data (id);

CREATE TABLE sys_role_menu
(
    id      INTEGER NOT NULL COMMENT '主键ID' AUTO_INCREMENT,
    role_id INTEGER NOT NULL COMMENT '角色ID',
    menu_id INTEGER NOT NULL COMMENT '菜单ID',
    PRIMARY KEY (id, role_id, menu_id),
    FOREIGN KEY (menu_id) REFERENCES sys_menu (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES sys_role (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_sys_role_menu_id ON sys_role_menu (id);

CREATE TABLE sys_user
(
    id              INTEGER      NOT NULL AUTO_INCREMENT,
    uuid            VARCHAR(50)  NOT NULL,
    username        VARCHAR(20)  NOT NULL COMMENT '用户名',
    nickname        VARCHAR(20)  NOT NULL COMMENT '昵称',
    password        VARCHAR(255) NOT NULL COMMENT '密码',
    salt            VARCHAR(5)   NOT NULL COMMENT '加密盐',
    email           VARCHAR(50)  NOT NULL COMMENT '邮箱',
    is_superuser    BOOL         NOT NULL COMMENT '超级权限(0否 1是)',
    is_staff        BOOL         NOT NULL COMMENT '后台管理登陆(0否 1是)',
    status          INTEGER      NOT NULL COMMENT '用户账号状态(0停用 1正常)',
    is_multi_login  BOOL         NOT NULL COMMENT '是否重复登陆(0否 1是)',
    avatar          VARCHAR(255) COMMENT '头像',
    phone           VARCHAR(11) COMMENT '手机号',
    join_time       DATETIME     NOT NULL COMMENT '注册时间',
    last_login_time DATETIME COMMENT '上次登录',
    dept_id         INTEGER COMMENT '部门关联ID',
    created_time    DATETIME     NOT NULL COMMENT '创建时间',
    updated_time    DATETIME COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (dept_id) REFERENCES sys_dept (id) ON DELETE SET NULL,
    UNIQUE (nickname),
    UNIQUE (uuid)
);

CREATE UNIQUE INDEX ix_sys_user_email ON sys_user (email);

CREATE INDEX ix_sys_user_id ON sys_user (id);

CREATE UNIQUE INDEX ix_sys_user_username ON sys_user (username);

CREATE TABLE sys_user_role
(
    id      INTEGER NOT NULL COMMENT '主键ID' AUTO_INCREMENT,
    user_id INTEGER NOT NULL COMMENT '用户ID',
    role_id INTEGER NOT NULL COMMENT '角色ID',
    PRIMARY KEY (id, user_id, role_id),
    FOREIGN KEY (role_id) REFERENCES sys_role (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sys_user (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_sys_user_role_id ON sys_user_role (id);
