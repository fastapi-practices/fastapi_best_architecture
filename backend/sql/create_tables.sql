-- sys_api: table
CREATE TABLE `sys_api`
(
    `id`           int          NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `name`         varchar(50)  NOT NULL COMMENT 'api名称',
    `method`       varchar(16)  NOT NULL COMMENT '请求方法',
    `path`         varchar(500) NOT NULL COMMENT 'api路径',
    `remark`       longtext COMMENT '备注',
    `created_time` datetime     NOT NULL COMMENT '创建时间',
    `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `ix_sys_api_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_casbin_rule: table
CREATE TABLE `sys_casbin_rule`
(
    `id`    int          NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `ptype` varchar(255) NOT NULL COMMENT '策略类型: p / g',
    `v0`    varchar(255) NOT NULL COMMENT '角色ID / 用户uuid',
    `v1`    longtext     NOT NULL COMMENT 'api路径 / 角色名称',
    `v2`    varchar(255) DEFAULT NULL COMMENT '请求方法',
    `v3`    varchar(255) DEFAULT NULL,
    `v4`    varchar(255) DEFAULT NULL,
    `v5`    varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `ix_sys_casbin_rule_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_dept: table
CREATE TABLE `sys_dept`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `name`         varchar(50) NOT NULL COMMENT '部门名称',
    `level`        int         NOT NULL COMMENT '部门层级',
    `sort`         int         NOT NULL COMMENT '排序',
    `leader`       varchar(20) DEFAULT NULL COMMENT '负责人',
    `phone`        varchar(11) DEFAULT NULL COMMENT '手机',
    `email`        varchar(50) DEFAULT NULL COMMENT '邮箱',
    `status`       int         NOT NULL COMMENT '部门状态(0停用 1正常)',
    `del_flag`     tinyint(1)  NOT NULL COMMENT '删除标志（0删除 1存在）',
    `parent_id`    int         DEFAULT NULL COMMENT '父部门ID',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime    DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `ix_sys_dept_parent_id` (`parent_id`),
    KEY `ix_sys_dept_id` (`id`),
    CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_dict_type: table
CREATE TABLE `sys_dict_type`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `name`         varchar(32) NOT NULL COMMENT '字典类型名称',
    `code`         varchar(32) NOT NULL COMMENT '字典类型编码',
    `status`       int         NOT NULL COMMENT '状态（0停用 1正常）',
    `remark`       longtext COMMENT '备注',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    UNIQUE KEY `code` (`code`),
    KEY `ix_sys_dict_type_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_dict_data: table
CREATE TABLE `sys_dict_data`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `label`        varchar(32) NOT NULL COMMENT '字典标签',
    `value`        varchar(32) NOT NULL COMMENT '字典值',
    `sort`         int         NOT NULL COMMENT '排序',
    `status`       int         NOT NULL COMMENT '状态（0停用 1正常）',
    `remark`       longtext COMMENT '备注',
    `type_id`      int         NOT NULL COMMENT '字典类型关联ID',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `label` (`label`),
    UNIQUE KEY `value` (`value`),
    KEY `type_id` (`type_id`),
    KEY `ix_sys_dict_data_id` (`id`),
    CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `sys_dict_type` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_login_log: table
CREATE TABLE `sys_login_log`
(
    `id`           int          NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `user_uuid`    varchar(50)  NOT NULL COMMENT '用户UUID',
    `username`     varchar(20)  NOT NULL COMMENT '用户名',
    `status`       int          NOT NULL COMMENT '登录状态(0失败 1成功)',
    `ip`           varchar(50)  NOT NULL COMMENT '登录IP地址',
    `country`      varchar(50) DEFAULT NULL COMMENT '国家',
    `region`       varchar(50) DEFAULT NULL COMMENT '地区',
    `city`         varchar(50) DEFAULT NULL COMMENT '城市',
    `user_agent`   varchar(255) NOT NULL COMMENT '请求头',
    `os`           varchar(50) DEFAULT NULL COMMENT '操作系统',
    `browser`      varchar(50) DEFAULT NULL COMMENT '浏览器',
    `device`       varchar(50) DEFAULT NULL COMMENT '设备',
    `msg`          longtext     NOT NULL COMMENT '提示消息',
    `login_time`   datetime     NOT NULL COMMENT '登录时间',
    `created_time` datetime     NOT NULL COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `ix_sys_login_log_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_menu: table
CREATE TABLE `sys_menu`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `title`        varchar(50) NOT NULL COMMENT '菜单标题',
    `name`         varchar(50) NOT NULL COMMENT '菜单名称',
    `level`        int         NOT NULL COMMENT '菜单层级',
    `sort`         int         NOT NULL COMMENT '排序',
    `icon`         varchar(100) DEFAULT NULL COMMENT '菜单图标',
    `path`         varchar(200) DEFAULT NULL COMMENT '路由地址',
    `menu_type`    int         NOT NULL COMMENT '菜单类型（0目录 1菜单 2按钮）',
    `component`    varchar(255) DEFAULT NULL COMMENT '组件路径',
    `perms`        varchar(100) DEFAULT NULL COMMENT '权限标识',
    `status`       int         NOT NULL COMMENT '菜单状态（0停用 1正常）',
    `show`         int         NOT NULL COMMENT '是否显示（0否 1是）',
    `cache`        int         NOT NULL COMMENT '是否缓存（0否 1是）',
    `remark`       longtext COMMENT '备注',
    `parent_id`    int          DEFAULT NULL COMMENT '父菜单ID',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime     DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `ix_sys_menu_id` (`id`),
    KEY `ix_sys_menu_parent_id` (`parent_id`),
    CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_opera_log: table
CREATE TABLE `sys_opera_log`
(
    `id`           int          NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `username`     varchar(20) DEFAULT NULL COMMENT '用户名',
    `method`       varchar(20)  NOT NULL COMMENT '请求类型',
    `title`        varchar(255) NOT NULL COMMENT '操作模块',
    `path`         varchar(500) NOT NULL COMMENT '请求路径',
    `ip`           varchar(50)  NOT NULL COMMENT 'IP地址',
    `country`      varchar(50) DEFAULT NULL COMMENT '国家',
    `region`       varchar(50) DEFAULT NULL COMMENT '地区',
    `city`         varchar(50) DEFAULT NULL COMMENT '城市',
    `user_agent`   varchar(255) NOT NULL COMMENT '请求头',
    `os`           varchar(50) DEFAULT NULL COMMENT '操作系统',
    `browser`      varchar(50) DEFAULT NULL COMMENT '浏览器',
    `device`       varchar(50) DEFAULT NULL COMMENT '设备',
    `args`         json        DEFAULT NULL COMMENT '请求参数',
    `status`       int          NOT NULL COMMENT '操作状态（0异常 1正常）',
    `code`         varchar(20)  NOT NULL COMMENT '操作状态码',
    `msg`          longtext COMMENT '提示消息',
    `cost_time`    float        NOT NULL COMMENT '请求耗时ms',
    `opera_time`   datetime     NOT NULL COMMENT '操作时间',
    `created_time` datetime     NOT NULL COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `ix_sys_opera_log_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_role: table
CREATE TABLE `sys_role`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `name`         varchar(20) NOT NULL COMMENT '角色名称',
    `data_scope`   int      DEFAULT NULL COMMENT '权限范围（1：全部数据权限 2：自定义数据权限）',
    `status`       int         NOT NULL COMMENT '角色状态（0停用 1正常）',
    `remark`       longtext COMMENT '备注',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `ix_sys_role_id` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_role_menu: table
CREATE TABLE `sys_role_menu`
(
    `id`      int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `role_id` int NOT NULL COMMENT '角色ID',
    `menu_id` int NOT NULL COMMENT '菜单ID',
    PRIMARY KEY (`id`, `role_id`, `menu_id`),
    UNIQUE KEY `ix_sys_role_menu_id` (`id`),
    KEY `role_id` (`role_id`),
    KEY `menu_id` (`menu_id`),
    CONSTRAINT `sys_role_menu_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE,
    CONSTRAINT `sys_role_menu_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_user: table
CREATE TABLE `sys_user`
(
    `id`              int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `uuid`            varchar(50) NOT NULL,
    `username`        varchar(20) NOT NULL COMMENT '用户名',
    `nickname`        varchar(20) NOT NULL COMMENT '昵称',
    `password`        varchar(255) DEFAULT NULL COMMENT '密码',
    `salt`            varchar(5)   DEFAULT NULL COMMENT '加密盐',
    `email`           varchar(50) NOT NULL COMMENT '邮箱',
    `is_superuser`    tinyint(1)  NOT NULL COMMENT '超级权限(0否 1是)',
    `is_staff`        tinyint(1)  NOT NULL COMMENT '后台管理登陆(0否 1是)',
    `status`          int         NOT NULL COMMENT '用户账号状态(0停用 1正常)',
    `is_multi_login`  tinyint(1)  NOT NULL COMMENT '是否重复登陆(0否 1是)',
    `avatar`          varchar(255) DEFAULT NULL COMMENT '头像',
    `phone`           varchar(11)  DEFAULT NULL COMMENT '手机号',
    `join_time`       datetime    NOT NULL COMMENT '注册时间',
    `last_login_time` datetime     DEFAULT NULL COMMENT '上次登录',
    `dept_id`         int          DEFAULT NULL COMMENT '部门关联ID',
    `created_time`    datetime    NOT NULL COMMENT '创建时间',
    `updated_time`    datetime     DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uuid` (`uuid`),
    UNIQUE KEY `nickname` (`nickname`),
    UNIQUE KEY `ix_sys_user_username` (`username`),
    UNIQUE KEY `ix_sys_user_email` (`email`),
    KEY `dept_id` (`dept_id`),
    KEY `ix_sys_user_id` (`id`),
    CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_user_role: table
CREATE TABLE `sys_user_role`
(
    `id`      int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `user_id` int NOT NULL COMMENT '用户ID',
    `role_id` int NOT NULL COMMENT '角色ID',
    PRIMARY KEY (`id`, `user_id`, `role_id`),
    UNIQUE KEY `ix_sys_user_role_id` (`id`),
    KEY `user_id` (`user_id`),
    KEY `role_id` (`role_id`),
    CONSTRAINT `sys_user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `sys_user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

-- sys_user_social: table
CREATE TABLE `sys_user_social`
(
    `id`           int         NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `source`       varchar(20) NOT NULL COMMENT '第三方用户来源',
    `open_id`      varchar(20)  DEFAULT NULL COMMENT '第三方用户的 open id',
    `uid`          varchar(20)  DEFAULT NULL COMMENT '第三方用户的 ID',
    `union_id`     varchar(20)  DEFAULT NULL COMMENT '第三方用户的 union id',
    `scope`        varchar(120) DEFAULT NULL COMMENT '第三方用户授予的权限',
    `code`         varchar(50)  DEFAULT NULL COMMENT '用户的授权 code',
    `user_id`      int          DEFAULT NULL COMMENT '用户关联ID',
    `created_time` datetime    NOT NULL COMMENT '创建时间',
    `updated_time` datetime     DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    KEY `ix_sys_user_social_id` (`id`),
    CONSTRAINT `sys_user_social_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;
