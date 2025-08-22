-- MySQL数据库初始化脚本(雪花ID)

-- API项目表
CREATE TABLE IF NOT EXISTS `api_project` (
  `id` bigint(20) NOT NULL COMMENT '主键ID',
  `name` varchar(64) NOT NULL COMMENT '项目名称',
  `description` text COMMENT '项目描述',
  `base_url` varchar(255) NOT NULL COMMENT '基础URL',
  `headers` json DEFAULT NULL COMMENT '全局请求头',
  `variables` json DEFAULT NULL COMMENT '全局变量',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1启用 0禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API项目表';

-- API测试用例表
CREATE TABLE IF NOT EXISTS `api_test_case` (
  `id` bigint(20) NOT NULL COMMENT '主键ID',
  `name` varchar(64) NOT NULL COMMENT '用例名称',
  `project_id` bigint(20) NOT NULL COMMENT '所属项目ID',
  `description` text COMMENT '用例描述',
  `pre_script` text COMMENT '前置脚本',
  `post_script` text COMMENT '后置脚本',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1启用 0禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_project_id` (`project_id`),
  CONSTRAINT `fk_api_test_case_project_id` FOREIGN KEY (`project_id`) REFERENCES `api_project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API测试用例表';

-- API测试步骤表
CREATE TABLE IF NOT EXISTS `api_test_step` (
  `id` bigint(20) NOT NULL COMMENT '主键ID',
  `name` varchar(64) NOT NULL COMMENT '步骤名称',
  `test_case_id` bigint(20) NOT NULL COMMENT '所属用例ID',
  `url` varchar(255) NOT NULL COMMENT '请求URL',
  `method` varchar(16) NOT NULL COMMENT '请求方法',
  `headers` json DEFAULT NULL COMMENT '请求头',
  `params` json DEFAULT NULL COMMENT '查询参数',
  `body` json DEFAULT NULL COMMENT '请求体',
  `files` json DEFAULT NULL COMMENT '上传文件',
  `auth` json DEFAULT NULL COMMENT '认证信息',
  `extract` json DEFAULT NULL COMMENT '提取变量',
  `validate` json DEFAULT NULL COMMENT '断言列表',
  `sql_queries` json DEFAULT NULL COMMENT 'SQL查询列表',
  `timeout` int(11) NOT NULL DEFAULT '30' COMMENT '超时时间(秒)',
  `retry` int(11) NOT NULL DEFAULT '0' COMMENT '重试次数',
  `retry_interval` int(11) NOT NULL DEFAULT '1' COMMENT '重试间隔(秒)',
  `order` int(11) NOT NULL COMMENT '步骤顺序',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1启用 0禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_test_case_id` (`test_case_id`),
  KEY `idx_order` (`test_case_id`, `order`),
  CONSTRAINT `fk_api_test_step_test_case_id` FOREIGN KEY (`test_case_id`) REFERENCES `api_test_case` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API测试步骤表';

-- API测试报告表
CREATE TABLE IF NOT EXISTS `api_test_report` (
  `id` bigint(20) NOT NULL COMMENT '主键ID',
  `test_case_id` bigint(20) NOT NULL COMMENT '所属用例ID',
  `name` varchar(64) NOT NULL COMMENT '报告名称',
  `success` tinyint(1) NOT NULL COMMENT '是否成功',
  `total_steps` int(11) NOT NULL COMMENT '总步骤数',
  `success_steps` int(11) NOT NULL COMMENT '成功步骤数',
  `fail_steps` int(11) NOT NULL COMMENT '失败步骤数',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `duration` int(11) NOT NULL COMMENT '执行时长(毫秒)',
  `details` json NOT NULL COMMENT '报告详情',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_test_case_id` (`test_case_id`),
  CONSTRAINT `fk_api_test_report_test_case_id` FOREIGN KEY (`test_case_id`) REFERENCES `api_test_case` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API测试报告表';