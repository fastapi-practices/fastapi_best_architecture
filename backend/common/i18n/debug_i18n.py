#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化调试脚本

用于诊断翻译文件加载和路径问题
"""

import json
import os

from backend.common.i18n.manager import get_i18n_manager
from backend.core.path_conf import BASE_PATH


def debug_translation_files():
    """调试翻译文件"""
    print('🔍 国际化功能调试')
    print('=' * 60)
    print()

    # 1. 检查BASE_PATH
    print(f'📁 BASE_PATH: {BASE_PATH}')
    print(f'   存在: {os.path.exists(BASE_PATH)}')
    print()

    # 2. 检查翻译文件目录
    translations_dir = os.path.join(BASE_PATH, 'backend', 'common', 'i18n', 'locales')
    print(f'📁 翻译文件目录: {translations_dir}')
    print(f'   存在: {os.path.exists(translations_dir)}')

    if os.path.exists(translations_dir):
        files = os.listdir(translations_dir)
        print(f'   文件列表: {files}')
    print()

    # 3. 检查具体的翻译文件
    for lang in ['zh-CN', 'en-US']:
        lang_file = os.path.join(translations_dir, f'{lang}.json')
        print(f'📄 {lang}.json')
        print(f'   路径: {lang_file}')
        print(f'   存在: {os.path.exists(lang_file)}')

        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print('   JSON有效: ✅')
                print(f'   顶级键: {list(data.keys())}')

                # 检查一些关键翻译
                if 'response' in data and 'success' in data['response']:
                    print(f"   示例翻译: response.success = '{data['response']['success']}'")
                else:
                    print('   ❌ 缺少 response.success 翻译')

            except json.JSONDecodeError as e:
                print(f'   JSON错误: ❌ {e}')
            except Exception as e:
                print(f'   读取错误: ❌ {e}')
        print()

    # 4. 测试翻译管理器
    print('🔧 测试翻译管理器')
    print('-' * 40)

    try:
        i18n = get_i18n_manager()
        print('✅ 管理器创建成功')
        print(f'   默认语言: {i18n.default_language}')
        print(f'   支持语言: {i18n.supported_languages}')
        print(f'   翻译缓存键: {list(i18n.translations.keys())}')

        # 检查翻译缓存内容
        for lang in i18n.supported_languages:
            if lang in i18n.translations:
                trans_data = i18n.translations[lang]
                print(f'   {lang} 缓存: {len(trans_data)} 个顶级键')
                if trans_data:
                    print(f'     顶级键: {list(trans_data.keys())}')

                    # 测试一个具体的翻译
                    if 'response' in trans_data and isinstance(trans_data['response'], dict):
                        if 'success' in trans_data['response']:
                            print(f"     response.success: '{trans_data['response']['success']}'")
                        else:
                            print('     ❌ response.success 不存在')
                    else:
                        print('     ❌ response 键不存在或格式错误')
                else:
                    print(f'     ❌ {lang} 翻译为空')
            else:
                print(f'   ❌ {lang} 未加载到缓存')

    except Exception as e:
        print(f'❌ 管理器创建失败: {e}')
        import traceback

        traceback.print_exc()

    print()

    # 5. 测试翻译函数
    print('🧪 测试翻译函数')
    print('-' * 40)

    from backend.common.i18n.manager import t

    test_keys = ['response.success', 'response.error', 'error.captcha_error']

    for key in test_keys:
        try:
            zh_result = t(key, language='zh-CN')
            en_result = t(key, language='en-US')

            print(f'📝 {key}')
            print(f"   中文: '{zh_result}' {'✅' if zh_result != key else '❌'}")
            print(f"   英文: '{en_result}' {'✅' if en_result != key else '❌'}")

        except Exception as e:
            print(f'❌ 翻译 {key} 失败: {e}')
        print()


def fix_common_issues():
    """尝试修复常见问题"""
    print('🔧 尝试修复常见问题')
    print('=' * 60)
    print()

    translations_dir = os.path.join(BASE_PATH, 'backend', 'common', 'i18n', 'locales')

    # 确保目录存在
    if not os.path.exists(translations_dir):
        print(f'📁 创建翻译目录: {translations_dir}')
        os.makedirs(translations_dir, exist_ok=True)

    # 检查并重新创建翻译文件（如果有问题）
    translations = {
        'zh-CN': {
            'response': {'success': '请求成功', 'error': '请求错误', 'server_error': '服务器内部错误'},
            'error': {'captcha_error': '验证码错误', 'user_not_found': '用户不存在'},
            'success': {'login_success': '登录成功'},
            'validation': {'missing': '字段为必填项'},
        },
        'en-US': {
            'response': {
                'success': 'Request successful',
                'error': 'Request error',
                'server_error': 'Internal server error',
            },
            'error': {'captcha_error': 'Captcha error', 'user_not_found': 'User not found'},
            'success': {'login_success': 'Login successful'},
            'validation': {'missing': 'Field required'},
        },
    }

    for lang, data in translations.items():
        lang_file = os.path.join(translations_dir, f'{lang}.json')

        # 检查文件是否需要重新创建
        needs_recreation = False

        if not os.path.exists(lang_file):
            needs_recreation = True
            print(f'📄 {lang}.json 不存在，需要创建')
        else:
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)

                # 检查关键键是否存在
                if not existing_data.get('response', {}).get('success') or not existing_data.get('error', {}).get(
                    'captcha_error'
                ):
                    needs_recreation = True
                    print(f'📄 {lang}.json 内容不完整，需要重新创建')

            except Exception as e:
                needs_recreation = True
                print(f'📄 {lang}.json 有问题，需要重新创建: {e}')

        if needs_recreation:
            try:
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f'✅ 成功创建/修复 {lang}.json')
            except Exception as e:
                print(f'❌ 创建 {lang}.json 失败: {e}')

    print()
    print('🔄 重新测试翻译功能...')

    # 重新加载翻译管理器
    try:
        # 清除缓存
        import backend.common.i18n.manager

        if hasattr(backend.common.i18n.manager, '_i18n_manager'):
            backend.common.i18n.manager._i18n_manager = None

        from backend.common.i18n.manager import get_i18n_manager, t

        # 强制重新加载
        i18n = get_i18n_manager()
        i18n._load_translations()

        # 测试翻译
        zh_msg = t('response.success', language='zh-CN')
        en_msg = t('response.success', language='en-US')

        print('🧪 测试结果:')
        print(f"   中文: '{zh_msg}' {'✅' if zh_msg == '请求成功' else '❌'}")
        print(f"   英文: '{en_msg}' {'✅' if en_msg == 'Request successful' else '❌'}")

        if zh_msg == '请求成功' and en_msg == 'Request successful':
            print('🎉 翻译功能修复成功！')
            return True
        else:
            print('❌ 翻译功能仍有问题')
            return False

    except Exception as e:
        print(f'❌ 重新测试失败: {e}')
        import traceback

        traceback.print_exc()
        return False


if __name__ == '__main__':
    print('🚀 开始国际化问题诊断...')
    print()

    # 先进行诊断
    debug_translation_files()

    print()
    print('🔧 是否尝试自动修复？(y/n): ', end='')
    try:
        response = input().lower().strip()
        if response in ['y', 'yes', '']:
            if fix_common_issues():
                print('\n✅ 问题已修复！现在可以重新运行测试:')
                print('   python backend/common/i18n/run_example.py')
            else:
                print('\n❌ 自动修复失败，请检查错误信息')
        else:
            print('\n📝 请根据诊断信息手动修复问题')
    except (EOFError, KeyboardInterrupt):
        print('\n📝 请根据诊断信息手动修复问题')
