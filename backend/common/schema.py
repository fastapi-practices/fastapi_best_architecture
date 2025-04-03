#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validate_email

from backend.core.conf import settings

# 自定义验证错误信息，参考：
# https://github.com/pydantic/pydantic-core/blob/a5cb7382643415b716b1a7a5392914e50f726528/tests/test_errors.py#L266
# https://github.com/pydantic/pydantic/blob/caa78016433ec9b16a973f92f187a7b6bfde6cb5/docs/errors/errors.md?plain=1#L232
CUSTOM_VALIDATION_ERROR_MESSAGES = {
    'no_such_attribute': "对象没有属性 '{attribute}'",
    'json_invalid': '无效的 JSON: {error}',
    'json_type': 'JSON 输入应为字符串、字节或字节数组',
    'recursion_loop': '递归错误 - 检测到循环引用',
    'model_type': '输入应为有效的字典或 {class_name} 的实例',
    'model_attributes_type': '输入应为有效的字典或可提取字段的对象',
    'dataclass_exact_type': '输入应为 {class_name} 的实例',
    'dataclass_type': '输入应为字典或 {class_name} 的实例',
    'missing': '字段为必填项',
    'frozen_field': '字段已冻结',
    'frozen_instance': '实例已冻结',
    'extra_forbidden': '不允许额外的输入',
    'invalid_key': '键应为字符串',
    'get_attribute_error': '提取属性时出错: {error}',
    'none_required': '输入应为 None',
    'enum': '输入应为 {expected}',
    'greater_than': '输入应大于 {gt}',
    'greater_than_equal': '输入应大于或等于 {ge}',
    'less_than': '输入应小于 {lt}',
    'less_than_equal': '输入应小于或等于 {le}',
    'finite_number': '输入应为有限数字',
    'too_short': '{field_type} 在验证后应至少有 {min_length} 个项目，而不是 {actual_length}',
    'too_long': '{field_type} 在验证后最多应有 {max_length} 个项目，而不是 {actual_length}',
    'string_type': '输入应为有效的字符串',
    'string_sub_type': '输入应为字符串，而不是 str 子类的实例',
    'string_unicode': '输入应为有效的字符串，无法将原始数据解析为 Unicode 字符串',
    'string_pattern_mismatch': "字符串应匹配模式 '{pattern}'",
    'string_too_short': '字符串应至少有 {min_length} 个字符',
    'string_too_long': '字符串最多应有 {max_length} 个字符',
    'dict_type': '输入应为有效的字典',
    'mapping_type': '输入应为有效的映射，错误: {error}',
    'iterable_type': '输入应为可迭代对象',
    'iteration_error': '迭代对象时出错，错误: {error}',
    'list_type': '输入应为有效的列表',
    'tuple_type': '输入应为有效的元组',
    'set_type': '输入应为有效的集合',
    'bool_type': '输入应为有效的布尔值',
    'bool_parsing': '输入应为有效的布尔值，无法解释输入',
    'int_type': '输入应为有效的整数',
    'int_parsing': '输入应为有效的整数，无法将字符串解析为整数',
    'int_parsing_size': '无法将输入字符串解析为整数，超出最大大小',
    'int_from_float': '输入应为有效的整数，得到一个带有小数部分的数字',
    'multiple_of': '输入应为 {multiple_of} 的倍数',
    'float_type': '输入应为有效的数字',
    'float_parsing': '输入应为有效的数字，无法将字符串解析为数字',
    'bytes_type': '输入应为有效的字节',
    'bytes_too_short': '数据应至少有 {min_length} 个字节',
    'bytes_too_long': '数据最多应有 {max_length} 个字节',
    'value_error': '值错误，{error}',
    'assertion_error': '断言失败，{error}',
    'literal_error': '输入应为 {expected}',
    'date_type': '输入应为有效的日期',
    'date_parsing': '输入应为 YYYY-MM-DD 格式的有效日期，{error}',
    'date_from_datetime_parsing': '输入应为有效的日期或日期时间，{error}',
    'date_from_datetime_inexact': '提供给日期的日期时间应具有零时间 - 例如为精确日期',
    'date_past': '日期应为过去的时间',
    'date_future': '日期应为未来的时间',
    'time_type': '输入应为有效的时间',
    'time_parsing': '输入应为有效的时间格式，{error}',
    'datetime_type': '输入应为有效的日期时间',
    'datetime_parsing': '输入应为有效的日期时间，{error}',
    'datetime_object_invalid': '无效的日期时间对象，得到 {error}',
    'datetime_past': '输入应为过去的时间',
    'datetime_future': '输入应为未来的时间',
    'timezone_naive': '输入不应包含时区信息',
    'timezone_aware': '输入应包含时区信息',
    'timezone_offset': '需要时区偏移为 {tz_expected}，实际得到 {tz_actual}',
    'time_delta_type': '输入应为有效的时间差',
    'time_delta_parsing': '输入应为有效的时间差，{error}',
    'frozen_set_type': '输入应为有效的冻结集合',
    'is_instance_of': '输入应为 {class} 的实例',
    'is_subclass_of': '输入应为 {class} 的子类',
    'callable_type': '输入应为可调用对象',
    'union_tag_invalid': "使用 {discriminator} 找到的输入标签 '{tag}' 与任何预期标签不匹配: {expected_tags}",
    'union_tag_not_found': '无法使用区分器 {discriminator} 提取标签',
    'arguments_type': '参数必须是元组、列表或字典',
    'missing_argument': '缺少必需参数',
    'unexpected_keyword_argument': '意外的关键字参数',
    'missing_keyword_only_argument': '缺少必需的关键字专用参数',
    'unexpected_positional_argument': '意外的位置参数',
    'missing_positional_only_argument': '缺少必需的位置专用参数',
    'multiple_argument_values': '为参数提供了多个值',
    'url_type': 'URL 输入应为字符串或 URL',
    'url_parsing': '输入应为有效的 URL，{error}',
    'url_syntax_violation': '输入违反了严格的 URL 语法规则，{error}',
    'url_too_long': 'URL 最多应有 {max_length} 个字符',
    'url_scheme': 'URL 方案应为 {expected_schemes}',
    'uuid_type': 'UUID 输入应为字符串、字节或 UUID 对象',
    'uuid_parsing': '输入应为有效的 UUID，{error}',
    'uuid_version': '预期 UUID 版本为 {expected_version}',
    'decimal_type': '十进制输入应为整数、浮点数、字符串或 Decimal 对象',
    'decimal_parsing': '输入应为有效的十进制数',
    'decimal_max_digits': '十进制输入总共应不超过 {max_digits} 位数字',
    'decimal_max_places': '十进制输入应不超过 {decimal_places} 位小数',
    'decimal_whole_digits': '十进制输入在小数点前应不超过 {whole_digits} 位数字',
}

CustomPhoneNumber = Annotated[str, Field(pattern=r'^1[3-9]\d{9}$')]


class CustomEmailStr(EmailStr):
    """自定义邮箱类型"""

    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == '' else validate_email(__input_value)[1]


class SchemaBase(BaseModel):
    """基础模型配置"""

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)},
    )
