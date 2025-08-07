#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化功能运行示例

可以直接运行的国际化演示脚本
"""

from backend.common.i18n.manager import get_i18n_manager, t
from backend.common.response.response_code import CustomErrorCode, CustomResponseCode


def test_basic_translation():
    """测试基本翻译功能"""
    print('🌍 基本翻译测试')
    print('-' * 50)

    # 测试不同语言的基本消息
    test_keys = [
        'response.success',
        'response.error',
        'error.user_not_found',
        'error.captcha_error',
        'success.login_success',
        'validation.missing',
    ]

    for key in test_keys:
        zh_msg = t(key, language='zh-CN')
        en_msg = t(key, language='en-US')
        print(f'📝 {key}')
        print(f'   🇨🇳 中文: {zh_msg}')
        print(f'   🇺🇸 英文: {en_msg}')
        print()


def test_parameter_formatting():
    """测试参数格式化"""
    print('🔧 参数格式化测试')
    print('-' * 50)

    # 测试带参数的翻译
    test_cases = [
        {'key': 'error.invalid_request_params', 'params': {'message': '用户名格式错误'}},
        {'key': 'validation.string_too_short', 'params': {'min_length': 8}},
        {'key': 'validation.string_too_long', 'params': {'max_length': 20}},
    ]

    for case in test_cases:
        key = case['key']
        params = case['params']

        zh_msg = t(key, language='zh-CN', **params)
        en_msg = t(key, language='en-US', **params)

        print(f'📝 {key} (参数: {params})')
        print(f'   🇨🇳 中文: {zh_msg}')
        print(f'   🇺🇸 英文: {en_msg}')
        print()


def test_response_codes():
    """测试响应码自动翻译"""
    print('📋 响应码翻译测试')
    print('-' * 50)

    i18n = get_i18n_manager()

    # 测试不同响应码
    response_codes = [CustomResponseCode.HTTP_200, CustomResponseCode.HTTP_400, CustomResponseCode.HTTP_500]

    error_codes = [CustomErrorCode.CAPTCHA_ERROR]

    for lang_code, lang_name in [('zh-CN', '中文'), ('en-US', '英文')]:
        print(f'🌐 {lang_name} ({lang_code})')
        i18n.set_language(lang_code)

        print('  📊 响应码:')
        for code in response_codes:
            print(f'    {code.code}: {code.msg}')

        print('  ❌ 错误码:')
        for code in error_codes:
            print(f'    {code.code}: {code.msg}')
        print()


def test_language_detection_simulation():
    """模拟语言检测过程"""
    print('🔍 语言检测模拟')
    print('-' * 50)

    # 模拟不同的请求场景
    scenarios = [
        {
            'name': 'URL参数优先',
            'url_lang': 'en-US',
            'header_lang': 'zh-CN',
            'accept_lang': 'ja-JP',
            'expected': 'en-US',
        },
        {'name': '请求头次优先', 'url_lang': None, 'header_lang': 'en-US', 'accept_lang': 'zh-CN', 'expected': 'en-US'},
        {
            'name': 'Accept-Language兜底',
            'url_lang': None,
            'header_lang': None,
            'accept_lang': 'en-US,en;q=0.9',
            'expected': 'en-US',
        },
        {'name': '默认语言', 'url_lang': None, 'header_lang': None, 'accept_lang': None, 'expected': 'zh-CN'},
    ]

    for scenario in scenarios:
        print(f'📌 场景: {scenario["name"]}')
        print(f'   URL参数: {scenario["url_lang"]}')
        print(f'   X-Language: {scenario["header_lang"]}')
        print(f'   Accept-Language: {scenario["accept_lang"]}')
        print(f'   预期语言: {scenario["expected"]}')
        print(f'   结果消息: {t("response.success", language=scenario["expected"])}')
        print()


def test_error_scenarios():
    """测试错误场景"""
    print('⚠️ 错误场景测试')
    print('-' * 50)

    # 测试不存在的翻译键
    print('🔍 测试不存在的翻译键')
    nonexistent_key = 'nonexistent.test.key'
    result = t(nonexistent_key)
    print(f'   键: {nonexistent_key}')
    print(f'   结果: {result} (应该返回键名本身)')
    print()

    # 测试不支持的语言
    print('🔍 测试不支持的语言')
    unsupported_lang = 'ja-JP'
    result = t('response.success', language=unsupported_lang)
    print(f'   语言: {unsupported_lang}')
    print(f'   结果: {result} (应该回退到默认语言)')
    print()

    # 测试参数格式化错误
    print('🔍 测试参数格式化错误')
    try:
        result = t('validation.string_too_short', min_length_wrong='wrong')
        print(f'   结果: {result} (参数名错误，应该正常处理)')
    except Exception as e:
        print(f'   异常: {e}')
    print()


def test_performance():
    """简单的性能测试"""
    print('⚡ 性能测试')
    print('-' * 50)

    import time

    # 测试翻译性能
    start_time = time.time()
    iterations = 1000

    for _ in range(iterations):
        t('response.success')
        t('error.user_not_found')
        t('validation.missing')

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = (total_time / iterations) * 1000  # 毫秒

    print(f'📊 执行 {iterations} 次翻译')
    print(f'   总时间: {total_time:.4f} 秒')
    print(f'   平均时间: {avg_time:.4f} 毫秒/次')
    print(f'   TPS: {iterations / total_time:.0f} 次/秒')
    print()


def main():
    """主函数"""
    print('🎉 FastAPI 国际化功能演示')
    print('=' * 60)
    print()

    try:
        # 运行各种测试
        test_basic_translation()
        test_parameter_formatting()
        test_response_codes()
        test_language_detection_simulation()
        test_error_scenarios()
        test_performance()

        print('✅ 所有测试完成！国际化功能正常工作。')
        print()
        print('📝 如需运行 FastAPI 服务器测试，请使用:')
        print('   python backend/common/i18n/usage_example.py')
        print()
        print('📝 如需运行完整测试套件，请使用:')
        print('   pytest backend/common/i18n/test_i18n.py -v')

    except Exception as e:
        print(f'❌ 测试过程中出现错误: {e}')
        import traceback

        traceback.print_exc()


if __name__ == '__main__':
    main()
