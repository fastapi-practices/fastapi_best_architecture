-- PostgreSQL数据库初始化脚本(自增ID)

-- API项目表
CREATE TABLE IF NOT EXISTS api_project (
  id SERIAL PRIMARY KEY COMMENT '主键ID',
  name VARCHAR(64) NOT NULL COMMENT '项目名称',
  description TEXT COMMENT '项目描述',
  base_url VARCHAR(255) NOT NULL COMMENT '基础URL',
  headers JSONB DEFAULT NULL COMMENT '全局请求头',
  variables JSONB DEFAULT NULL COMMENT '全局变量',
  status SMALLINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT uk_api_project_name UNIQUE (name)
);

-- 触发器函数
CREATE OR REPLACE FUNCTION update_api_project_update_time()
RETURNS TRIGGER AS $$
BEGIN
   NEW.update_time = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_api_project_update_time
BEFORE UPDATE ON api_project
FOR EACH ROW
EXECUTE FUNCTION update_api_project_update_time();

-- API测试用例表
CREATE TABLE IF NOT EXISTS api_test_case (
  id SERIAL PRIMARY KEY COMMENT '主键ID',
  name VARCHAR(64) NOT NULL COMMENT '用例名称',
  project_id INTEGER NOT NULL COMMENT '所属项目ID',
  description TEXT COMMENT '用例描述',
  pre_script TEXT COMMENT '前置脚本',
  post_script TEXT COMMENT '后置脚本',
  status SMALLINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_api_test_case_project_id FOREIGN KEY (project_id) REFERENCES api_project(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_api_test_case_project_id ON api_test_case(project_id);

-- 创建触发器
CREATE TRIGGER update_api_test_case_update_time
BEFORE UPDATE ON api_test_case
FOR EACH ROW
EXECUTE FUNCTION update_api_project_update_time();

-- API测试步骤表
CREATE TABLE IF NOT EXISTS api_test_step (
  id SERIAL PRIMARY KEY COMMENT '主键ID',
  name VARCHAR(64) NOT NULL COMMENT '步骤名称',
  test_case_id INTEGER NOT NULL COMMENT '所属用例ID',
  url VARCHAR(255) NOT NULL COMMENT '请求URL',
  method VARCHAR(16) NOT NULL COMMENT '请求方法',
  headers JSONB DEFAULT NULL COMMENT '请求头',
  params JSONB DEFAULT NULL COMMENT '查询参数',
  body JSONB DEFAULT NULL COMMENT '请求体',
  files JSONB DEFAULT NULL COMMENT '上传文件',
  auth JSONB DEFAULT NULL COMMENT '认证信息',
  extract JSONB DEFAULT NULL COMMENT '提取变量',
  validate JSONB DEFAULT NULL COMMENT '断言列表',
  sql_queries JSONB DEFAULT NULL COMMENT 'SQL查询列表',
  timeout INTEGER NOT NULL DEFAULT 30 COMMENT '超时时间(秒)',
  retry INTEGER NOT NULL DEFAULT 0 COMMENT '重试次数',
  retry_interval INTEGER NOT NULL DEFAULT 1 COMMENT '重试间隔(秒)',
  "order" INTEGER NOT NULL COMMENT '步骤顺序',
  status SMALLINT NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_api_test_step_test_case_id FOREIGN KEY (test_case_id) REFERENCES api_test_case(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_api_test_step_test_case_id ON api_test_step(test_case_id);
CREATE INDEX idx_api_test_step_order ON api_test_step(test_case_id, "order");

-- 创建触发器
CREATE TRIGGER update_api_test_step_update_time
BEFORE UPDATE ON api_test_step
FOR EACH ROW
EXECUTE FUNCTION update_api_project_update_time();

-- API测试报告表
CREATE TABLE IF NOT EXISTS api_test_report (
  id SERIAL PRIMARY KEY COMMENT '主键ID',
  test_case_id INTEGER NOT NULL COMMENT '所属用例ID',
  name VARCHAR(64) NOT NULL COMMENT '报告名称',
  success BOOLEAN NOT NULL COMMENT '是否成功',
  total_steps INTEGER NOT NULL COMMENT '总步骤数',
  success_steps INTEGER NOT NULL COMMENT '成功步骤数',
  fail_steps INTEGER NOT NULL COMMENT '失败步骤数',
  start_time TIMESTAMP NOT NULL COMMENT '开始时间',
  end_time TIMESTAMP NOT NULL COMMENT '结束时间',
  duration INTEGER NOT NULL COMMENT '执行时长(毫秒)',
  details JSONB NOT NULL COMMENT '报告详情',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  CONSTRAINT fk_api_test_report_test_case_id FOREIGN KEY (test_case_id) REFERENCES api_test_case(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_api_test_report_test_case_id ON api_test_report(test_case_id);