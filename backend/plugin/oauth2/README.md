# OAuth2

OAuth 2.0 第三方登录插件，支持 GitHub、Google 等社交平台登录

## 全局配置

在 `backend/core/conf.py` 中添加以下内容：

```python
##################################################
# [ Plugin ] oauth2
##################################################
# .env
OAUTH2_GITHUB_CLIENT_ID: str
OAUTH2_GITHUB_CLIENT_SECRET: str
OAUTH2_GOOGLE_CLIENT_ID: str
OAUTH2_GOOGLE_CLIENT_SECRET: str

# 基础配置（in plugin.toml）
OAUTH2_STATE_REDIS_PREFIX: str
OAUTH2_STATE_EXPIRE_SECONDS: int
OAUTH2_GITHUB_REDIRECT_URI: str
OAUTH2_GOOGLE_REDIRECT_URI: str
OAUTH2_FRONTEND_LOGIN_REDIRECT_URI: str
OAUTH2_FRONTEND_BINDING_REDIRECT_URI: str
```
