#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化功能测试

专门用于pytest测试的国际化功能验证
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.common.i18n import I18nMiddleware, get_i18n_manager
from backend.common.i18n.manager import t
from backend.common.response.response_code import CustomErrorCode, CustomResponseCode


class TestI18nManager:
    """测试国际化管理器"""

    def setup_method(self):
        """测试前准备"""
        self.i18n = get_i18n_manager()

    def test_basic_translation(self):
        """测试基本翻译功能"""
        # 测试中文翻译
        msg_zh = t('response.success', language='zh-CN')
        assert msg_zh == '请求成功'

        # 测试英文翻译
        msg_en = t('response.success', language='en-US')
        assert msg_en == 'Request successful'

    def test_parameter_formatting(self):
        """测试参数格式化"""
        # 测试带参数的翻译
        msg_zh = t('error.invalid_request_params', language='zh-CN', message='用户名')
        assert '用户名' in msg_zh

        msg_en = t('error.invalid_request_params', language='en-US', message='username')
        assert 'username' in msg_en

    def test_nested_keys(self):
        """测试嵌套键翻译"""
        # 测试验证消息
        msg_zh = t('validation.missing', language='zh-CN')
        assert msg_zh == '字段为必填项'

        msg_en = t('validation.missing', language='en-US')
        assert msg_en == 'Field required'

    def test_fallback_mechanism(self):
        """测试回退机制"""
        # 测试不存在的键
        result = t('non_existent.key')
        assert result == 'non_existent.key'  # 应该返回键名本身

    def test_supported_languages(self):
        """测试支持的语言"""
        assert 'zh-CN' in self.i18n.supported_languages
        assert 'en-US' in self.i18n.supported_languages


class TestResponseCodeI18n:
    """测试响应码国际化"""

    def test_response_code_translation(self):
        """测试响应码自动翻译"""
        # 设置不同语言并测试
        i18n = get_i18n_manager()

        # 测试中文
        i18n.set_language('zh-CN')
        res = CustomResponseCode.HTTP_200
        assert res.msg == '请求成功'

        # 测试英文
        i18n.set_language('en-US')
        res = CustomResponseCode.HTTP_200
        assert res.msg == 'Request successful'

    def test_error_code_translation(self):
        """测试错误码翻译"""
        i18n = get_i18n_manager()

        # 测试中文
        i18n.set_language('zh-CN')
        error = CustomErrorCode.CAPTCHA_ERROR
        assert error.msg == '验证码错误'

        # 测试英文
        i18n.set_language('en-US')
        error = CustomErrorCode.CAPTCHA_ERROR
        assert error.msg == 'Captcha error'


class TestI18nMiddleware:
    """测试国际化中间件"""

    def setup_method(self):
        """设置测试应用"""
        self.app = FastAPI()
        self.app.add_middleware(I18nMiddleware, default_language='zh-CN')

        @self.app.get('/test')
        async def test_endpoint():
            res = CustomResponseCode.HTTP_200
            return {'code': res.code, 'msg': res.msg}

        self.client = TestClient(self.app)

    def test_default_language(self):
        """测试默认语言"""
        response = self.client.get('/test')
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == '请求成功'  # 默认中文

    def test_url_parameter_language(self):
        """测试URL参数语言切换"""
        response = self.client.get('/test?lang=en-US')
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == 'Request successful'  # 英文

    def test_header_language(self):
        """测试请求头语言切换"""
        headers = {'X-Language': 'en-US'}
        response = self.client.get('/test', headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == 'Request successful'  # 英文

    def test_accept_language_header(self):
        """测试Accept-Language头"""
        headers = {'Accept-Language': 'en-US,en;q=0.9'}
        response = self.client.get('/test', headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == 'Request successful'  # 英文

    def test_language_priority(self):
        """测试语言优先级"""
        # URL参数应该优先于请求头
        headers = {'X-Language': 'zh-CN', 'Accept-Language': 'zh-CN'}
        response = self.client.get('/test?lang=en-US', headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == 'Request successful'  # URL参数的英文优先

    def test_unsupported_language_fallback(self):
        """测试不支持语言的回退"""
        headers = {'X-Language': 'ja-JP'}  # 不支持的日语
        response = self.client.get('/test', headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['msg'] == '请求成功'  # 回退到默认中文

    def test_response_language_header(self):
        """测试响应语言头"""
        headers = {'X-Language': 'en-US'}
        response = self.client.get('/test', headers=headers)
        assert response.headers.get('Content-Language') == 'en-US'


class TestValidationI18n:
    """测试验证消息国际化"""

    def test_validation_messages(self):
        """测试验证消息翻译"""
        # 测试几个常用的验证消息
        validation_keys = [
            'validation.missing',
            'validation.string_too_short',
            'validation.string_too_long',
            'validation.int_type',
            'validation.email_type',
        ]

        for key in validation_keys:
            # 测试中文
            msg_zh = t(key, language='zh-CN')
            assert msg_zh != key  # 应该有翻译
            assert isinstance(msg_zh, str)
            assert len(msg_zh) > 0

            # 测试英文
            msg_en = t(key, language='en-US')
            assert msg_en != key  # 应该有翻译
            assert isinstance(msg_en, str)
            assert len(msg_en) > 0

            # 中英文不应该相同
            assert msg_zh != msg_en


if __name__ == '__main__':
    # 如果直接运行此文件，执行基本测试
    print('🧪 运行国际化功能基础测试...')

    # 测试基本翻译
    print('✅ 测试基本翻译:')
    print(f'  中文: {t("response.success", language="zh-CN")}')
    print(f'  英文: {t("response.success", language="en-US")}')

    # 测试参数化翻译
    print('✅ 测试参数化翻译:')
    print(f'  中文: {t("error.invalid_request_params", language="zh-CN", message="用户名")}')
    print(f'  英文: {t("error.invalid_request_params", language="en-US", message="username")}')

    # 测试响应码
    print('✅ 测试响应码翻译:')
    i18n = get_i18n_manager()
    i18n.set_language('zh-CN')
    res_zh = CustomResponseCode.HTTP_200
    print(f'  中文: {res_zh.msg}')

    i18n.set_language('en-US')
    res_en = CustomResponseCode.HTTP_200
    print(f'  英文: {res_en.msg}')

    print('🎉 基础测试完成！所有功能正常工作。')
    print('\n📝 运行完整测试套件:')
    print('  pytest backend/common/i18n/test_i18n.py -v')
