-- API测试插件数据表创建脚本 (PostgreSQL)
-- 创建时间: 2024-08-29

-- API项目表
CREATE TABLE IF NOT EXISTS api_project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    base_url VARCHAR(255) NOT NULL,
    headers JSONB,
    variables JSONB,
    status SMALLINT NOT NULL DEFAULT 1,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_api_project_name ON api_project(name);
CREATE INDEX IF NOT EXISTS idx_api_project_status ON api_project(status);
CREATE INDEX IF NOT EXISTS idx_api_project_create_time ON api_project(create_time);

-- 添加注释
COMMENT ON TABLE api_project IS 'API项目表';
COMMENT ON COLUMN api_project.id IS '主键ID';
COMMENT ON COLUMN api_project.name IS '项目名称';
COMMENT ON COLUMN api_project.description IS '项目描述';
COMMENT ON COLUMN api_project.base_url IS '基础URL';
COMMENT ON COLUMN api_project.headers IS '全局请求头';
COMMENT ON COLUMN api_project.variables IS '全局变量';
COMMENT ON COLUMN api_project.status IS '状态 1启用 0禁用';
COMMENT ON COLUMN api_project.create_time IS '创建时间';
COMMENT ON COLUMN api_project.update_time IS '更新时间';

-- API测试用例表
CREATE TABLE IF NOT EXISTS api_test_case (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    project_id INTEGER NOT NULL,
    description TEXT,
    pre_script TEXT,
    post_script TEXT,
    status SMALLINT NOT NULL DEFAULT 1,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES api_project(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_api_test_case_project_id ON api_test_case(project_id);
CREATE INDEX IF NOT EXISTS idx_api_test_case_name ON api_test_case(name);
CREATE INDEX IF NOT EXISTS idx_api_test_case_status ON api_test_case(status);
CREATE INDEX IF NOT EXISTS idx_api_test_case_create_time ON api_test_case(create_time);

-- 添加注释
COMMENT ON TABLE api_test_case IS 'API测试用例表';
COMMENT ON COLUMN api_test_case.id IS '主键ID';
COMMENT ON COLUMN api_test_case.name IS '用例名称';
COMMENT ON COLUMN api_test_case.project_id IS '所属项目ID';
COMMENT ON COLUMN api_test_case.description IS '用例描述';
COMMENT ON COLUMN api_test_case.pre_script IS '前置脚本';
COMMENT ON COLUMN api_test_case.post_script IS '后置脚本';
COMMENT ON COLUMN api_test_case.status IS '状态 1启用 0禁用';
COMMENT ON COLUMN api_test_case.create_time IS '创建时间';
COMMENT ON COLUMN api_test_case.update_time IS '更新时间';

-- API测试步骤表
CREATE TABLE IF NOT EXISTS api_test_step (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    test_case_id INTEGER NOT NULL,
    url VARCHAR(255) NOT NULL,
    method VARCHAR(16) NOT NULL,
    headers JSONB,
    params JSONB,
    body JSONB,
    files JSONB,
    auth JSONB,
    extract JSONB,
    validate JSONB,
    sql_queries JSONB,
    timeout INTEGER NOT NULL DEFAULT 30,
    retry INTEGER NOT NULL DEFAULT 0,
    retry_interval INTEGER NOT NULL DEFAULT 1,
    "order" INTEGER NOT NULL,
    status SMALLINT NOT NULL DEFAULT 1,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES api_test_case(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_api_test_step_test_case_id ON api_test_step(test_case_id);
CREATE INDEX IF NOT EXISTS idx_api_test_step_order ON api_test_step("order");
CREATE INDEX IF NOT EXISTS idx_api_test_step_method ON api_test_step(method);
CREATE INDEX IF NOT EXISTS idx_api_test_step_status ON api_test_step(status);
CREATE INDEX IF NOT EXISTS idx_api_test_step_create_time ON api_test_step(create_time);

-- 添加注释
COMMENT ON TABLE api_test_step IS 'API测试步骤表';
COMMENT ON COLUMN api_test_step.id IS '主键ID';
COMMENT ON COLUMN api_test_step.name IS '步骤名称';
COMMENT ON COLUMN api_test_step.test_case_id IS '所属用例ID';
COMMENT ON COLUMN api_test_step.url IS '请求URL';
COMMENT ON COLUMN api_test_step.method IS '请求方法';
COMMENT ON COLUMN api_test_step.headers IS '请求头';
COMMENT ON COLUMN api_test_step.params IS '查询参数';
COMMENT ON COLUMN api_test_step.body IS '请求体';
COMMENT ON COLUMN api_test_step.files IS '上传文件';
COMMENT ON COLUMN api_test_step.auth IS '认证信息';
COMMENT ON COLUMN api_test_step.extract IS '提取变量';
COMMENT ON COLUMN api_test_step.validate IS '断言列表';
COMMENT ON COLUMN api_test_step.sql_queries IS 'SQL查询列表';
COMMENT ON COLUMN api_test_step.timeout IS '超时时间(秒)';
COMMENT ON COLUMN api_test_step.retry IS '重试次数';
COMMENT ON COLUMN api_test_step.retry_interval IS '重试间隔(秒)';
COMMENT ON COLUMN api_test_step."order" IS '步骤顺序';
COMMENT ON COLUMN api_test_step.status IS '状态 1启用 0禁用';
COMMENT ON COLUMN api_test_step.create_time IS '创建时间';
COMMENT ON COLUMN api_test_step.update_time IS '更新时间';

-- API测试报告表
CREATE TABLE IF NOT EXISTS api_test_report (
    id SERIAL PRIMARY KEY,
    test_case_id INTEGER NOT NULL,
    name VARCHAR(64) NOT NULL,
    success BOOLEAN NOT NULL,
    total_steps INTEGER NOT NULL,
    success_steps INTEGER NOT NULL,
    fail_steps INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL,
    details JSONB NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES api_test_case(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_api_test_report_test_case_id ON api_test_report(test_case_id);
CREATE INDEX IF NOT EXISTS idx_api_test_report_success ON api_test_report(success);
CREATE INDEX IF NOT EXISTS idx_api_test_report_start_time ON api_test_report(start_time);
CREATE INDEX IF NOT EXISTS idx_api_test_report_create_time ON api_test_report(create_time);

-- 添加注释
COMMENT ON TABLE api_test_report IS 'API测试报告表';
COMMENT ON COLUMN api_test_report.id IS '主键ID';
COMMENT ON COLUMN api_test_report.test_case_id IS '所属用例ID';
COMMENT ON COLUMN api_test_report.name IS '报告名称';
COMMENT ON COLUMN api_test_report.success IS '是否成功';
COMMENT ON COLUMN api_test_report.total_steps IS '总步骤数';
COMMENT ON COLUMN api_test_report.success_steps IS '成功步骤数';
COMMENT ON COLUMN api_test_report.fail_steps IS '失败步骤数';
COMMENT ON COLUMN api_test_report.start_time IS '开始时间';
COMMENT ON COLUMN api_test_report.end_time IS '结束时间';
COMMENT ON COLUMN api_test_report.duration IS '执行时长(毫秒)';
COMMENT ON COLUMN api_test_report.details IS '报告详情';
COMMENT ON COLUMN api_test_report.create_time IS '创建时间';

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要自动更新时间的表创建触发器
CREATE TRIGGER update_api_project_updated_at BEFORE UPDATE ON api_project FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_api_test_case_updated_at BEFORE UPDATE ON api_test_case FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_api_test_step_updated_at BEFORE UPDATE ON api_test_step FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入示例数据
INSERT INTO api_project (name, description, base_url, headers, variables) VALUES
('示例API项目', '这是一个示例API测试项目', 'https://jsonplaceholder.typicode.com', 
 '{"Content-Type": "application/json", "Accept": "application/json"}'::jsonb, 
 '{"timeout": 30, "retry": 3}'::jsonb);

INSERT INTO api_test_case (name, project_id, description, pre_script, post_script) VALUES
('获取用户信息测试', 1, '测试获取用户信息接口', 
 'console.log("开始执行测试用例");', 
 'console.log("测试用例执行完成");');

INSERT INTO api_test_step (name, test_case_id, url, method, headers, params, validate, "order") VALUES
('获取用户1信息', 1, '/users/1', 'GET', 
 '{"Accept": "application/json"}'::jsonb, 
 '{}'::jsonb, 
 '[{"source": "json", "type": "equals", "path": "$.id", "expected": 1, "message": "用户ID验证"}]'::jsonb, 
 1);
