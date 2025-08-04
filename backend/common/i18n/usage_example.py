#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化使用示例

展示如何在 FastAPI 项目中使用 i18n 功能
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from backend.common.exception.errors import CustomError
from backend.common.i18n import I18nMiddleware
from backend.common.i18n.manager import t
from backend.common.response.response_code import CustomErrorCode, CustomResponseCode

app = FastAPI()

# 添加国际化中间件
app.add_middleware(I18nMiddleware, default_language='zh-CN')


@app.get('/api/test')
async def test_endpoint():
    """测试端点 - 展示基本的国际化响应"""
    # 使用响应码（会自动国际化）
    res = CustomResponseCode.HTTP_200
    return {
        'code': res.code,
        'msg': res.msg,  # 会根据请求语言自动翻译
        'data': {'test': 'success'},
    }


@app.get('/api/error')
async def error_endpoint():
    """错误端点 - 展示错误消息的国际化"""
    # 抛出自定义错误（使用翻译键）
    raise CustomError(error=CustomErrorCode.CAPTCHA_ERROR)


@app.get('/api/manual')
async def manual_translation():
    """手动翻译示例"""
    # 手动使用翻译函数
    success_msg = t('success.login_success')
    error_msg = t('error.user_not_found')

    return {
        'success': success_msg,
        'error': error_msg,
        'formatted': t('error.invalid_request_params', message='test parameter'),
    }


@app.get('/api/lang/{lang}')
async def change_language(lang: str):
    """切换语言示例"""
    # 手动指定语言进行翻译
    messages = {
        'zh': t('response.success', language='zh-CN'),
        'en': t('response.success', language='en-US'),
    }

    return {'current_lang': lang, 'messages': messages}


# 如何在业务逻辑中使用
class UserService:
    """用户服务示例"""

    def validate_user(self, username: str) -> dict:
        if not username:
            # 使用翻译键抛出错误
            raise HTTPException(status_code=400, detail=t('error.user_not_found'))

        return {'msg': t('success.login_success'), 'user': {'username': username}}


# 在 Pydantic 模型中使用（需要动态获取）
class UserModel(BaseModel):
    username: str = Field(..., description='用户名')

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v:
            # 在验证器中使用翻译
            raise ValueError(t('validation.missing'))
        return v


def test_basic_functionality():
    """测试基本功能（非异步）"""
    from backend.common.i18n.manager import get_i18n_manager, t

    print('🧪 测试国际化基本功能')
    print('-' * 40)

    # 测试基本翻译
    zh_msg = t('response.success', language='zh-CN')
    en_msg = t('response.success', language='en-US')

    print('✅ 基本翻译测试:')
    print(f'   中文: {zh_msg}')
    print(f'   英文: {en_msg}')

    # 测试响应码翻译
    i18n = get_i18n_manager()

    i18n.set_language('zh-CN')
    res_zh = CustomResponseCode.HTTP_200

    i18n.set_language('en-US')
    res_en = CustomResponseCode.HTTP_200

    print('✅ 响应码翻译测试:')
    print(f'   中文: {res_zh.msg}')
    print(f'   英文: {res_en.msg}')

    print('🎉 基本功能测试完成！')
    return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # 运行FastAPI服务器
        import uvicorn

        print('🚀 启动国际化测试服务器...')
        print('📝 测试不同语言:')
        print('   curl http://localhost:8000/api/test')
        print('   curl -H "X-Language: en-US" http://localhost:8000/api/test')
        print('   curl "http://localhost:8000/api/test?lang=en-US"')
        print()
        uvicorn.run(app, host='0.0.0.0', port=8000)
    else:
        # 运行基本功能测试
        test_basic_functionality()
        print()
        print('📝 运行服务器测试:')
        print('   python backend/common/i18n/usage_example.py server')
        print()
        print('📝 运行完整测试:')
        print('   python backend/common/i18n/run_example.py')
        print('   pytest backend/common/i18n/test_i18n.py -v')
