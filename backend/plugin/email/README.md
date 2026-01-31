# Email

电子邮件插件，提供邮件发送功能，支持验证码、通知等场景

## 全局配置

在 `backend/core/conf.py` 中添加以下内容：

```python
##################################################
# [ Plugin ] email
##################################################
# .env
EMAIL_USERNAME: str
EMAIL_PASSWORD: str

# 基础配置（in plugin.toml）
EMAIL_HOST: str
EMAIL_PORT: int
EMAIL_SSL: bool
EMAIL_CAPTCHA_REDIS_PREFIX: str
EMAIL_CAPTCHA_EXPIRE_SECONDS: int
```
