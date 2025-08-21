# 腾讯云短信服务插件

该插件用于通过腾讯云短信服务发送短信验证码。

## 功能
- 发送短信验证码
- 支持国内短信和国际/港澳台短信

## 使用方法
1. 在腾讯云控制台申请短信应用并获取 AppID、AppKey
2. 在腾讯云控制台申请短信签名和模板
3. 在系统中配置相关参数
4. 调用API发送短信 
5. 必须在环境变量`.env`中添加以下内容：
```text
# SMS
TENCENTCLOUD_SECRET_ID='' # 腾讯云密钥ID
TENCENTCLOUD_SECRET_KEY='' # 腾讯云密钥KEY
SMS_LOGIN_TEMPLATE_ID='' # 短信登录模板ID
SMS_SIGN_NAME='' # 短信签名
SMS_SDK_APP_ID='' # 短信应用ID
```
6. 在 `core/conf.py` 中添加以下内容
```text
# 短信验证码
TENCENTCLOUD_SECRET_ID: str
TENCENTCLOUD_SECRET_KEY: str
SMS_LOGIN_REDIS_PREFIX: str = "fba:sms:login"
SMS_LOGIN_EXPIRE_SECONDS: int = 300  # 短信验证码有效期，5分钟
SMS_LOGIN_TEMPLATE_ID: str  # 短信登录模板ID
SMS_SIGN_NAME: str  # 短信签名
SMS_SDK_APP_ID: str  # 短信应用ID
```

## 例子
```text
{
  "phone_numbers": [
    "132xxxxxxx"
  ],
  "template_id": "2475017",
  "template_params": ["12123"], # 验证码参数
  "sign_name": "测试短信",
  "sms_sdk_app_id": "1400898160",
  "extend_code": "",
  "session_context": "",
  "sender_id": ""
}
```