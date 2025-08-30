-- API测试插件数据表创建脚本 (MySQL)
-- 创建时间: 2024-08-29

-- API项目表
CREATE TABLE IF NOT EXISTS `api_project` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(64) NOT NULL COMMENT '项目名称',
    `description` TEXT COMMENT '项目描述',
    `base_url` VARCHAR(255) NOT NULL COMMENT '基础URL',
    `headers` JSON COMMENT '全局请求头',
    `variables` JSON COMMENT '全局变量',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_name` (`name`),
    INDEX `idx_status` (`status`),
    INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='API项目表';

-- API测试用例表
CREATE TABLE IF NOT EXISTS `api_test_case` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(64) NOT NULL COMMENT '用例名称',
    `project_id` INT NOT NULL COMMENT '所属项目ID',
    `description` TEXT COMMENT '用例描述',
    `pre_script` TEXT COMMENT '前置脚本',
    `post_script` TEXT COMMENT '后置脚本',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (`project_id`) REFERENCES `api_project`(`id`) ON DELETE CASCADE,
    INDEX `idx_project_id` (`project_id`),
    INDEX `idx_name` (`name`),
    INDEX `idx_status` (`status`),
    INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='API测试用例表';

-- API测试步骤表
CREATE TABLE IF NOT EXISTS `api_test_step` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(64) NOT NULL COMMENT '步骤名称',
    `test_case_id` INT NOT NULL COMMENT '所属用例ID',
    `url` VARCHAR(255) NOT NULL COMMENT '请求URL',
    `method` VARCHAR(16) NOT NULL COMMENT '请求方法',
    `headers` JSON COMMENT '请求头',
    `params` JSON COMMENT '查询参数',
    `body` JSON COMMENT '请求体',
    `files` JSON COMMENT '上传文件',
    `auth` JSON COMMENT '认证信息',
    `extract` JSON COMMENT '提取变量',
    `validate` JSON COMMENT '断言列表',
    `sql_queries` JSON COMMENT 'SQL查询列表',
    `timeout` INT NOT NULL DEFAULT 30 COMMENT '超时时间(秒)',
    `retry` INT NOT NULL DEFAULT 0 COMMENT '重试次数',
    `retry_interval` INT NOT NULL DEFAULT 1 COMMENT '重试间隔(秒)',
    `order` INT NOT NULL COMMENT '步骤顺序',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (`test_case_id`) REFERENCES `api_test_case`(`id`) ON DELETE CASCADE,
    INDEX `idx_test_case_id` (`test_case_id`),
    INDEX `idx_order` (`order`),
    INDEX `idx_method` (`method`),
    INDEX `idx_status` (`status`),
    INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='API测试步骤表';

-- API测试报告表
CREATE TABLE IF NOT EXISTS `api_test_report` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `test_case_id` INT NOT NULL COMMENT '所属用例ID',
    `name` VARCHAR(64) NOT NULL COMMENT '报告名称',
    `success` BOOLEAN NOT NULL COMMENT '是否成功',
    `total_steps` INT NOT NULL COMMENT '总步骤数',
    `success_steps` INT NOT NULL COMMENT '成功步骤数',
    `fail_steps` INT NOT NULL COMMENT '失败步骤数',
    `start_time` DATETIME NOT NULL COMMENT '开始时间',
    `end_time` DATETIME NOT NULL COMMENT '结束时间',
    `duration` INT NOT NULL COMMENT '执行时长(毫秒)',
    `details` JSON NOT NULL COMMENT '报告详情',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (`test_case_id`) REFERENCES `api_test_case`(`id`) ON DELETE CASCADE,
    INDEX `idx_test_case_id` (`test_case_id`),
    INDEX `idx_success` (`success`),
    INDEX `idx_start_time` (`start_time`),
    INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='API测试报告表';

-- 插入示例数据
INSERT INTO `api_project` (`name`, `description`, `base_url`, `headers`, `variables`) VALUES
('示例API项目', '这是一个示例API测试项目', 'https://jsonplaceholder.typicode.com', 
 '{"Content-Type": "application/json", "Accept": "application/json"}', 
 '{"timeout": 30, "retry": 3}');

INSERT INTO `api_test_case` (`name`, `project_id`, `description`, `pre_script`, `post_script`) VALUES
('获取用户信息测试', 1, '测试获取用户信息接口', 
 'console.log("开始执行测试用例");', 
 'console.log("测试用例执行完成");');

INSERT INTO `api_test_step` (`name`, `test_case_id`, `url`, `method`, `headers`, `params`, `validate`, `order`) VALUES
('获取用户1信息', 1, '/users/1', 'GET', 
 '{"Accept": "application/json"}', 
 '{}', 
 '[{"source": "json", "type": "equals", "path": "$.id", "expected": 1, "message": "用户ID验证"}]', 
 1);
