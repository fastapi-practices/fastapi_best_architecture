# 国际化 (i18n) 模块

FastAPI 项目的完整国际化解决方案，支持多语言响应消息、验证错误消息和业务逻辑消息的自动翻译。

## 🌍 功能特性

- **自动语言检测**: 支持从 URL 参数、请求头、Accept-Language 等多种方式检测用户语言偏好
- **响应码国际化**: 自动翻译所有响应状态码消息
- **验证消息国际化**: 支持 100+ 条 Pydantic 验证错误消息的翻译
- **业务消息国际化**: 支持业务逻辑中的错误和成功消息翻译
- **灵活的翻译管理**: 基于 JSON 文件的翻译资源管理
- **上下文感知**: 支持参数格式化的动态翻译

## 📁 文件结构

```
backend/common/i18n/
├── __init__.py              # 模块导出
├── manager.py               # 国际化管理器
├── middleware.py            # 国际化中间件
├── locales/                 # 翻译文件目录
│   ├── zh-CN.json          # 中文翻译
│   └── en-US.json          # 英文翻译
├── usage_example.py         # 使用示例
└── README.md               # 文档说明
```

## 🚀 快速开始

### 1. 启用国际化中间件

在 `main.py` 中添加国际化中间件：

```python
from fastapi import FastAPI
from backend.common.i18n import I18nMiddleware

app = FastAPI()

# 添加国际化中间件
app.add_middleware(I18nMiddleware, default_language='zh-CN')
```

### 2. 基本使用

```python
from backend.common.i18n.manager import t
from backend.common.response.response_code import CustomResponseCode

# 使用响应码（自动国际化）
res = CustomResponseCode.HTTP_200
print(res.msg)  # 根据当前语言显示 "请求成功" 或 "Request successful"

# 手动翻译
message = t('error.user_not_found')
formatted_msg = t('error.invalid_request_params', message="用户名")
```

### 3. 语言切换方式

客户端可以通过以下方式指定语言：

1. **URL 参数**: `GET /api/users?lang=en-US`
2. **请求头**: `X-Language: en-US`
3. **Accept-Language**: `Accept-Language: en-US,en;q=0.9`

优先级: URL 参数 > X-Language 头 > Accept-Language 头 > 默认语言

## 📖 API 文档

### I18nManager

国际化管理器，负责加载和管理翻译资源。

```python
from backend.common.i18n.manager import get_i18n_manager, t

# 获取管理器实例
i18n = get_i18n_manager()

# 翻译方法
def t(key: str, language: str = None, **kwargs) -> str:
    """
    翻译函数
    
    Args:
        key: 翻译键，支持点号分隔的嵌套键
        language: 目标语言，None 则使用当前语言
        **kwargs: 格式化参数
    
    Returns:
        翻译后的文本
    """
```

### I18nMiddleware

国际化中间件，自动检测和设置请求语言。

```python
class I18nMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_language: str = 'zh-CN'):
        """
        Args:
            app: FastAPI 应用实例
            default_language: 默认语言
        """
```

## 🔧 翻译文件格式

翻译文件使用 JSON 格式，支持嵌套结构：

```json
{
  "response": {
    "success": "请求成功",
    "error": "请求错误"
  },
  "error": {
    "user_not_found": "用户不存在",
    "invalid_request_params": "请求参数非法: {message}"
  },
  "validation": {
    "missing": "字段为必填项",
    "string_too_short": "字符串应至少有 {min_length} 个字符"
  }
}
```

## 💡 使用示例

### 在 API 端点中使用

```python
from fastapi import APIRouter
from backend.common.i18n.manager import t
from backend.common.response.response_code import CustomResponseCode

router = APIRouter()

@router.get("/users")
async def get_users():
    # 响应码会自动国际化
    res = CustomResponseCode.HTTP_200
    return {
        "code": res.code,
        "msg": res.msg,  # 自动翻译
        "data": []
    }

@router.post("/users")
async def create_user(user_data: dict):
    if not user_data.get('username'):
        # 手动翻译错误消息
        raise HTTPException(
            status_code=400,
            detail=t('error.user_not_found')
        )
    
    return {
        "msg": t('success.create_success', name="用户")
    }
```

### 在服务层中使用

```python
from backend.common.exception.errors import CustomError
from backend.common.response.response_code import CustomErrorCode
from backend.common.i18n.manager import t

class UserService:
    def get_user(self, user_id: int):
        user = self.user_repository.get(user_id)
        if not user:
            # 使用预定义的错误码
            raise CustomError(error=CustomErrorCode.USER_NOT_FOUND)
        
        return user
    
    def validate_password(self, password: str):
        if len(password) < 8:
            # 使用动态翻译
            raise ValueError(t('error.password_too_short', min_length=8))
```

### 在 Pydantic 模型中使用

```python
from pydantic import BaseModel, Field, validator
from backend.common.i18n.manager import t

class UserCreateSchema(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    
    @validator('username')
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError(t('validation.string_too_short', min_length=3))
        return v
```

## 🔄 扩展新语言

1. 在 `locales/` 目录下创建新的语言文件，如 `ja-JP.json`
2. 复制现有翻译文件结构，翻译所有文本
3. 在 `I18nManager` 中添加新语言到 `supported_languages` 列表
4. 在中间件的 `_normalize_language` 方法中添加语言映射

## 📝 翻译键命名规范

- **响应码**: `response.{type}` (如: `response.success`)
- **错误消息**: `error.{error_type}` (如: `error.user_not_found`)
- **成功消息**: `success.{action}` (如: `success.login_success`)
- **验证消息**: `validation.{validation_type}` (如: `validation.missing`)
- **任务消息**: `task.{task_type}` (如: `task.execute_failed`)

## ⚠️ 注意事项

1. **性能考虑**: 翻译文件在启动时加载到内存，避免频繁的文件 I/O
2. **缓存机制**: 使用 `@lru_cache` 缓存管理器实例
3. **参数格式化**: 支持 Python 字符串格式化语法，如 `{name}`, `{count:d}`
4. **回退机制**: 如果翻译不存在，会回退到默认语言或返回翻译键
5. **上下文变量**: 使用 `contextvars` 确保请求级别的语言隔离

## 🔍 故障排除

### 翻译不生效
- 检查翻译文件是否存在且格式正确
- 确认中间件已正确添加
- 验证翻译键是否正确

### 语言检测不准确
- 检查请求头格式
- 确认支持的语言列表包含目标语言
- 验证语言代码规范化映射

### 格式化参数错误
- 确保参数名与翻译文件中的占位符匹配
- 检查参数类型是否正确
- 验证格式化语法

## 🤝 贡献指南

1. 添加新的翻译键时，请同时更新所有语言文件
2. 保持翻译文件结构的一致性
3. 为新功能编写相应的使用示例
4. 更新文档说明

---

通过这个国际化模块，你的 FastAPI 项目可以轻松支持多语言，为全球用户提供本地化的体验。 