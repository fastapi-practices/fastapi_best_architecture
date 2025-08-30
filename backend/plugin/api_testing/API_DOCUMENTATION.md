# API测试插件完整接口文档

## 概述

本文档详细介绍了API测试插件的所有接口，包括数据管理接口和功能接口。插件提供了完整的API测试解决方案，支持项目管理、测试用例管理、测试步骤管理和测试报告管理。

## 数据管理接口

### 1. 项目管理接口

#### 1.1 创建API项目
- **接口**: `POST /v1/api_testing/projects`
- **描述**: 创建新的API测试项目
- **请求体**:
```json
{
    "name": "项目名称",
    "description": "项目描述",
    "base_url": "https://api.example.com",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer token"
    },
    "variables": {
        "timeout": 30,
        "retry": 3
    },
    "status": 1
}
```

#### 1.2 获取项目详情
- **接口**: `GET /v1/api_testing/projects/{project_id}`
- **描述**: 根据项目ID获取项目详细信息

#### 1.3 获取项目列表
- **接口**: `GET /v1/api_testing/projects`
- **参数**: 
  - `skip`: 跳过数量 (默认: 0)
  - `limit`: 限制数量 (默认: 100)

#### 1.4 更新项目
- **接口**: `PUT /v1/api_testing/projects/{project_id}`
- **描述**: 更新项目信息

#### 1.5 删除项目
- **接口**: `DELETE /v1/api_testing/projects/{project_id}`
- **描述**: 删除项目及其关联的测试用例和步骤

### 2. 测试用例管理接口

#### 2.1 创建测试用例
- **接口**: `POST /v1/api_testing/test-cases`
- **请求体**:
```json
{
    "name": "用例名称",
    "project_id": 1,
    "description": "用例描述",
    "pre_script": "console.log('前置脚本');",
    "post_script": "console.log('后置脚本');",
    "status": 1
}
```

#### 2.2 获取用例详情
- **接口**: `GET /v1/api_testing/test-cases/{case_id}`
- **描述**: 获取测试用例详情，包含关联的测试步骤

#### 2.3 获取用例列表
- **接口**: `GET /v1/api_testing/test-cases`
- **参数**:
  - `project_id`: 项目ID (可选)
  - `skip`: 跳过数量 (默认: 0)
  - `limit`: 限制数量 (默认: 100)

#### 2.4 更新测试用例
- **接口**: `PUT /v1/api_testing/test-cases/{case_id}`

#### 2.5 删除测试用例
- **接口**: `DELETE /v1/api_testing/test-cases/{case_id}`

### 3. 测试步骤管理接口

#### 3.1 创建测试步骤
- **接口**: `POST /v1/api_testing/test-steps`
- **请求体**:
```json
{
    "name": "步骤名称",
    "test_case_id": 1,
    "url": "/api/users",
    "method": "GET",
    "headers": {
        "Authorization": "Bearer {{token}}"
    },
    "params": {
        "page": 1,
        "limit": 10
    },
    "body": {
        "username": "test",
        "password": "123456"
    },
    "validate": [
        {
            "source": "json",
            "type": "equals",
            "path": "$.success",
            "expected": true,
            "message": "响应成功验证"
        }
    ],
    "extract": {
        "user_id": "$.data.id",
        "token": "$.data.token"
    },
    "sql_queries": [
        {
            "name": "查询用户",
            "query": "SELECT * FROM users WHERE id = 1",
            "extract": {
                "db_user_id": "0.id"
            }
        }
    ],
    "timeout": 30,
    "retry": 3,
    "retry_interval": 1,
    "order": 1,
    "status": 1
}
```

#### 3.2 获取步骤详情
- **接口**: `GET /v1/api_testing/test-steps/{step_id}`

#### 3.3 获取步骤列表
- **接口**: `GET /v1/api_testing/test-steps`
- **参数**:
  - `test_case_id`: 测试用例ID (可选)
  - `skip`: 跳过数量 (默认: 0)
  - `limit`: 限制数量 (默认: 100)

#### 3.4 更新测试步骤
- **接口**: `PUT /v1/api_testing/test-steps/{step_id}`

#### 3.5 删除测试步骤
- **接口**: `DELETE /v1/api_testing/test-steps/{step_id}`

#### 3.6 重新排序测试步骤
- **接口**: `POST /v1/api_testing/test-steps/reorder`
- **参数**: `test_case_id`: 测试用例ID
- **请求体**:
```json
{
    "step_orders": [
        {"step_id": 1, "order": 1},
        {"step_id": 2, "order": 2},
        {"step_id": 3, "order": 3}
    ]
}
```

### 4. 测试报告管理接口

#### 4.1 创建测试报告
- **接口**: `POST /v1/api_testing/test-reports`
- **请求体**:
```json
{
    "test_case_id": 1,
    "name": "测试报告_20240829_001",
    "success": true,
    "total_steps": 5,
    "success_steps": 5,
    "fail_steps": 0,
    "start_time": "2024-08-29T10:00:00",
    "end_time": "2024-08-29T10:05:00",
    "duration": 300000,
    "details": {
        "steps": [
            {
                "step_id": 1,
                "name": "登录请求",
                "success": true,
                "response_time": 150,
                "status_code": 200,
                "error": null
            }
        ],
        "environment": {
            "base_url": "https://api.example.com",
            "variables": {}
        }
    }
}
```

#### 4.2 获取报告详情
- **接口**: `GET /v1/api_testing/test-reports/{report_id}`

#### 4.3 获取报告列表
- **接口**: `GET /v1/api_testing/test-reports`
- **参数**:
  - `test_case_id`: 测试用例ID (可选)
  - `start_date`: 开始日期 YYYY-MM-DD (可选)
  - `end_date`: 结束日期 YYYY-MM-DD (可选)
  - `success_only`: 仅显示成功报告 (可选)
  - `skip`: 跳过数量 (默认: 0)
  - `limit`: 限制数量 (默认: 100)

#### 4.4 删除测试报告
- **接口**: `DELETE /v1/api_testing/test-reports/{report_id}`

#### 4.5 获取报告统计信息
- **接口**: `GET /v1/api_testing/test-reports/statistics`
- **参数**:
  - `test_case_id`: 测试用例ID (可选)
  - `days`: 统计天数 (默认: 30)

#### 4.6 清理旧报告
- **接口**: `DELETE /v1/api_testing/test-reports/cleanup`
- **参数**: `days`: 保留天数 (默认: 90)

## 功能接口

### 1. 请求发送接口
- **接口**: `POST /v1/api_testing/requests/send`
- **描述**: 发送HTTP请求并返回响应结果

### 2. 断言验证接口
- **接口**: `POST /v1/api_testing/assertions/validate`
- **描述**: 执行断言验证

### 3. SQL执行接口
- **接口**: `POST /v1/api_testing/sql/execute`
- **描述**: 执行SQL查询

### 4. 报告生成接口
- **接口**: `POST /v1/api_testing/reports/generate`
- **描述**: 生成HTML或JSON格式的测试报告

### 5. 环境管理接口
- **接口**: `GET/POST /v1/api_testing/environments`
- **描述**: 管理测试环境和变量

### 6. Mock服务接口
- **接口**: `GET/POST /v1/api_testing/mocks`
- **描述**: 管理Mock服务和规则

### 7. 数据驱动接口
- **接口**: `POST /v1/api_testing/data-driven`
- **描述**: 支持数据驱动测试

### 8. 历史记录接口
- **接口**: `GET/POST /v1/api_testing/history`
- **描述**: 管理请求历史记录

## 数据库安装

### MySQL
执行以下SQL文件创建数据表：
```bash
mysql -u username -p database_name < backend/plugin/api_testing/sql/mysql/001_create_api_testing_tables.sql
```

### PostgreSQL
执行以下SQL文件创建数据表：
```bash
psql -U username -d database_name -f backend/plugin/api_testing/sql/postgresql/001_create_api_testing_tables.sql
```

## 响应格式

所有接口都遵循统一的响应格式：

### 成功响应
```json
{
    "code": 200,
    "msg": "Success",
    "data": {
        // 具体数据内容
    }
}
```

### 错误响应
```json
{
    "code": 400,
    "msg": "错误信息",
    "data": null
}
```

## 状态码说明

- `1`: 启用状态
- `0`: 禁用状态

## 注意事项

1. 删除项目会级联删除其下的所有测试用例、测试步骤和测试报告
2. 删除测试用例会级联删除其下的所有测试步骤和测试报告
3. 测试步骤的`order`字段用于控制执行顺序
4. JSON字段支持复杂的数据结构，用于存储请求参数、响应数据等
5. 时间字段统一使用ISO 8601格式
6. 所有列表接口都支持分页查询
