# 热插拔实现说明

## 概述

本次实现解决了代码生成和插件安装时的热重载冲突问题，采用**锁文件机制 + 原子写入 + 动态配置加载**的组合方案。

## 核心机制

### 1. 锁文件机制

**文件**: `backend/utils/reload_lock.py`

```python
@asynccontextmanager
async def reload_lock():
    """批量文件操作时暂停热重载"""
    lock_path = anyio.Path(RELOAD_LOCK_FILE)
    await lock_path.touch()
    try:
        yield
    finally:
        await lock_path.unlink(missing_ok=True)
```

**工作原理**:
- 批量文件操作前创建 `.reload.lock` 文件
- `CustomReloadFilter` 检测到锁文件存在时跳过重载
- 操作完成后删除锁文件，恢复正常重载

### 2. 原子写入（代码生成）

**文件**: `backend/plugin/code_generator/service/gen_service.py`

```python
async def generate(self, *, db: AsyncSession, pk: int) -> str:
    async with reload_lock():
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 1. 先写入临时目录
            for filepath, content in files.items():
                write_to_temp(tmp_dir, filepath, content)

            # 2. 原子移动到目标位置
            for item in os.listdir(tmp_dir):
                shutil.copytree/copy2(src, dst)
```

**优势**:
- 所有文件在临时目录准备完毕
- 一次性移动到目标位置
- 避免部分文件触发重载

### 3. 动态配置加载（插件配置）

**文件**: `backend/plugin/config_loader.py`

使用 Pydantic Settings 的自定义配置源机制：

```python
class PluginSettingsSource(PydanticBaseSettingsSource):
    def __call__(self) -> dict[str, Any]:
        """从所有插件的 plugin.toml 加载配置"""
        merged_settings = {}
        for plugin in plugins:
            config = load_toml(f'{plugin}/plugin.toml')
            merged_settings.update(config.get('settings', {}))
        return merged_settings
```

**配置优先级**（从高到低）:
1. 环境变量
2. `.env` 文件
3. 插件 `plugin.toml` 配置
4. 字段默认值

## 使用方式

### 插件配置示例

**plugin.toml**:
```toml
[plugin]
summary = '阿里云 OSS'
version = '0.1.0'
author = 'xxx'

[app]
router = ['v1']

[settings]
# 非敏感配置，提供默认值
OSS_BUCKET_NAME = 'fba-test'
OSS_ENDPOINT = 'https://oss-cn-hangzhou.aliyuncs.com'
OSS_USE_SIGNED_URL = true
OSS_SIGNED_URL_EXPIRE_SECONDS = 300
```

**.env**:
```env
# 敏感配置，必须在环境变量中设置
OSS_ACCESS_KEY='your_access_key'
OSS_SECRET_KEY='your_secret_key'

# 可选：覆盖插件默认配置
OSS_BUCKET_NAME='my-custom-bucket'
```

**代码中使用**:
```python
from backend.core.conf import settings

# 直接访问，无需修改 Settings 类
bucket = settings.OSS_BUCKET_NAME
access_key = settings.OSS_ACCESS_KEY
```

### 代码生成使用

```bash
# CLI 命令
fba codegen import --app myapp --tn users
fba codegen

# 或通过 API
POST /api/v1/code_generator/generate
```

生成过程中：
1. 创建 `.reload.lock`
2. 在临时目录生成所有文件
3. 原子移动到目标位置
4. 删除 `.reload.lock`
5. 服务检测到变更，触发重载

### 插件安装使用

```bash
# ZIP 安装
fba plugin add --path /path/to/plugin.zip

# Git 安装
fba plugin add --repo-url https://github.com/xxx/plugin.git
```

安装过程中：
1. 创建 `.reload.lock`
2. 解压/克隆插件
3. 安装依赖
4. 设置 Redis 变更标记
5. 删除 `.reload.lock`
6. 服务检测到变更，触发重载
7. 重载时自动加载插件配置

## 修改的文件

### 新增文件
- `backend/utils/reload_lock.py` - 锁文件上下文管理器
- `backend/plugin/config_loader.py` - 插件配置加载器

### 修改文件
- `backend/core/path_conf.py` - 新增 `RELOAD_LOCK_FILE`
- `backend/cli.py` - `CustomReloadFilter` 支持锁文件检测
- `backend/plugin/code_generator/service/gen_service.py` - 原子写入
- `backend/plugin/installer.py` - 安装时使用锁文件
- `backend/core/conf.py` - 自定义配置源，支持插件配置

## 优势

1. **无需手动重启**: 操作完成后自动触发重载
2. **避免部分写入**: 原子操作确保完整性
3. **配置自动加载**: 插件配置无需手动添加到 Settings 类
4. **优先级清晰**: 环境变量 > .env > plugin.toml > 默认值
5. **向后兼容**: 不影响现有插件和代码

## 注意事项

1. **敏感配置**: 仍需在 `.env` 中设置（如密钥、密码）
2. **配置命名**: 插件配置字段名应避免与核心配置冲突
3. **锁文件清理**: 异常情况下可能残留 `.reload.lock`，需手动删除
4. **依赖安装**: 插件依赖安装可能耗时，期间服务不会重载
