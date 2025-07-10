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