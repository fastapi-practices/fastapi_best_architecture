# 接口自动化测试插件

基于httpx的接口自动化测试工具，支持请求发送、断言验证、SQL执行和测试报告生成。

## 功能特点

- **接口请求**: 支持各种HTTP方法（GET, POST, PUT, DELETE等）的API请求
- **灵活断言**: 提供20+种断言类型，支持对响应状态码、头信息、JSON内容等进行验证
- **SQL执行**: 支持MySQL和PostgreSQL数据库操作，用于测试前后数据验证
- **变量提取**: 从响应或SQL结果中提取变量，用于后续测试步骤
- **测试报告**: 生成美观的HTML或JSON格式测试报告，包含详细的失败分析
- **失败重试**: 支持请求失败自动重试机制
- **环境变量**: 多环境管理，支持全局、项目、环境、用例和临时变量
- **Mock服务**: 提供接口Mock功能，支持条件匹配和响应定制
- **数据驱动**: 支持CSV、Excel、JSON和数据库数据源的数据驱动测试
- **历史记录**: 记录接口请求历史，支持统计分析和查询

## 安装使用

1. 将本插件目录复制到FastAPI项目的`backend/plugin/`目录下
2. 安装依赖: `pip install httpx jsonpath-ng jinja2 pymysql psycopg pandas xlrd`
3. 重启应用服务器

## API接口

### 请求接口

- **POST** `/v1/api_testing/requests/send`: 发送API请求

### 断言接口

- **POST** `/v1/api_testing/assertions/validate`: 执行单个断言验证
- **POST** `/v1/api_testing/assertions/batch-validate`: 批量执行断言验证

### SQL接口

- **POST** `/v1/api_testing/sql/execute`: 执行SQL查询
- **POST** `/v1/api_testing/sql/batch-execute`: 批量执行SQL查询

### 报告接口

- **POST** `/v1/api_testing/reports/generate`: 生成测试报告
- **POST** `/v1/api_testing/reports/preview`: 预览HTML测试报告

### 环境变量接口

- **POST** `/v1/api_testing/environments`: 创建环境
- **GET** `/v1/api_testing/environments/{environment_id}`: 获取环境信息
- **GET** `/v1/api_testing/environments`: 获取环境列表
- **POST** `/v1/api_testing/environments/variables`: 创建变量
- **GET** `/v1/api_testing/environments/variables`: 获取变量列表

### Mock服务接口

- **POST** `/v1/api_testing/mocks/projects`: 创建Mock项目
- **GET** `/v1/api_testing/mocks/projects`: 获取Mock项目列表
- **POST** `/v1/api_testing/mocks/rules`: 创建Mock规则
- **GET** `/v1/api_testing/mocks/rules`: 获取Mock规则列表

### 数据驱动接口

- **POST** `/v1/api_testing/data-driven/config`: 创建数据驱动配置
- **POST** `/v1/api_testing/data-driven/upload/csv`: 上传CSV数据文件
- **POST** `/v1/api_testing/data-driven/upload/excel`: 上传Excel数据文件

### 历史记录接口

- **POST** `/v1/api_testing/history`: 保存请求历史记录
- **GET** `/v1/api_testing/history/{history_id}`: 获取请求历史记录
- **GET** `/v1/api_testing/history`: 获取请求历史记录列表
- **GET** `/v1/api_testing/history/statistics`: 获取历史记录统计信息

## 断言类型

| 断言类型 | 描述 |
|---------|------|
| equals | 等于 |
| not_equals | 不等于 |
| contains | 包含 |
| not_contains | 不包含 |
| starts_with | 以...开头 |
| ends_with | 以...结尾 |
| match_regex | 匹配正则表达式 |
| less_than | 小于 |
| less_than_or_equals | 小于或等于 |
| greater_than | 大于 |
| greater_than_or_equals | 大于或等于 |
| exists | 存在 |
| not_exists | 不存在 |
| is_empty | 为空 |
| is_not_empty | 不为空 |
| is_null | 为null |
| is_not_null | 不为null |
| is_true | 为true |
| is_false | 为false |
| length_equals | 长度等于 |
| length_greater_than | 长度大于 |
| length_less_than | 长度小于 |

## 使用示例

### 发送请求

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/api_testing/requests/send",
    json={
        "url": "https://api.example.com/users",
        "method": "GET",
        "headers": {
            "Authorization": "Bearer token123",
            "Content-Type": "application/json"
        },
        "params": {
            "page": 1,
            "limit": 10
        }
    }
)

print(response.json())
```

### 执行断言

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/api_testing/assertions/validate",
    json={
        "assertion": {
            "source": "json",
            "type": "equals",
            "path": "$.data.id",
            "expected": 123,
            "message": "用户ID验证"
        },
        "response_data": {
            "status_code": 200,
            "json": {
                "data": {
                    "id": 123,
                    "name": "测试用户"
                }
            }
        }
    }
)

print(response.json())
```

### 执行SQL查询

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/api_testing/sql/execute",
    json={
        "name": "查询用户",
        "query": "SELECT id, username FROM users WHERE id = 1",
        "extract": {
            "user_id": "0.id",
            "username": "0.username"
        },
        "use_default_db": true
    }
)

print(response.json())
```

### 使用环境变量

```python
import requests

# 创建环境变量
response = requests.post(
    "http://localhost:8000/v1/api_testing/environments/variables",
    json={
        "name": "base_url",
        "value": "https://api.example.com",
        "scope": "project",
        "project_id": 1,
        "description": "API基础URL"
    }
)

# 使用变量发送请求
response = requests.post(
    "http://localhost:8000/v1/api_testing/requests/send",
    json={
        "url": "{{base_url}}/users",  # 使用变量
        "method": "GET",
    }
)

print(response.json())
```

### 创建Mock服务

```python
import requests

# 创建Mock项目
response = requests.post(
    "http://localhost:8000/v1/api_testing/mocks/projects",
    json={
        "id": 1,
        "name": "用户API Mock",
        "base_path": "/api",
        "port": 3000
    }
)

# 创建Mock规则
response = requests.post(
    "http://localhost:8000/v1/api_testing/mocks/rules",
    json={
        "id": "user_rule_1",
        "name": "获取用户信息",
        "url": "/users/:id",
        "method": "GET",
        "project_id": 1,
        "responses": [{
            "id": "resp_1",
            "name": "成功响应",
            "status_code": 200,
            "response_type": "json",
            "content": '{"id": 1, "name": "Test User", "email": "test@example.com"}'
        }]
    }
)
```

### 数据驱动测试

```python
import requests

# 创建数据驱动配置
response = requests.post(
    "http://localhost:8000/v1/api_testing/data-driven/config",
    json={
        "enabled": True,
        "data_source": {
            "name": "用户数据",
            "type": "csv",
            "file_path": "data/users.csv"
        },
        "parameters": [
            {"name": "user_id", "value": "1"},
            {"name": "username", "value": "test"}
        ],
        "loop_mode": "sequential"
    }
)
```

### 查询历史记录

```python
import requests

# 获取历史记录列表
response = requests.get(
    "http://localhost:8000/v1/api_testing/history?project_id=1&limit=10&sort_desc=true"
)

# 获取历史统计信息
response = requests.get(
    "http://localhost:8000/v1/api_testing/history/statistics?project_id=1"
)

print(response.json())
```

## 注意事项

1. 文件上传请确保服务器有权限访问指定的文件路径
2. SQL执行时请注意权限控制，避免安全风险
3. 大型测试报告可能会占用较多内存，请根据服务器配置合理使用
4. Mock服务需要单独运行，默认监听端口为3000
5. 环境变量中的敏感信息会进行简单加密存储

## 版本信息

- 版本: 0.1.0
- 作者: ranyong