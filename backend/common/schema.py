#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validate_email

from backend.core.conf import settings

# 自定义验证错误信息
# 不包含验证预期内容（也就是输入内容），受支持的预期内容字段参考以下链接
# https://github.com/pydantic/pydantic-core/blob/a5cb7382643415b716b1a7a5392914e50f726528/tests/test_errors.py#L266
# 替换预期内容字段方式，参考以下链接
# https://github.com/pydantic/pydantic/blob/caa78016433ec9b16a973f92f187a7b6bfde6cb5/docs/errors/errors.md?plain=1#L232
CUSTOM_VALIDATION_ERROR_MESSAGES = {
    'arguments_type': '参数类型输入错误',
    'assertion_error': '断言执行错误',
    'bool_parsing': '布尔值输入解析错误',
    'bool_type': '布尔值类型输入错误',
    'bytes_too_long': '字节长度输入过长',
    'bytes_too_short': '字节长度输入过短',
    'bytes_type': '字节类型输入错误',
    'callable_type': '可调用对象类型输入错误',
    'dataclass_exact_type': '数据类实例类型输入错误',
    'dataclass_type': '数据类类型输入错误',
    'date_from_datetime_inexact': '日期分量输入非零',
    'date_from_datetime_parsing': '日期输入解析错误',
    'date_future': '日期输入非将来时',
    'date_parsing': '日期输入验证错误',
    'date_past': '日期输入非过去时',
    'date_type': '日期类型输入错误',
    'datetime_future': '日期时间输入非将来时间',
    'datetime_object_invalid': '日期时间输入对象无效',
    'datetime_parsing': '日期时间输入解析错误',
    'datetime_past': '日期时间输入非过去时间',
    'datetime_type': '日期时间类型输入错误',
    'decimal_max_digits': '小数位数输入过多',
    'decimal_max_places': '小数位数输入错误',
    'decimal_parsing': '小数输入解析错误',
    'decimal_type': '小数类型输入错误',
    'decimal_whole_digits': '小数位数输入错误',
    'dict_type': '字典类型输入错误',
    'enum': '枚举成员输入错误，允许 {expected}',
    'extra_forbidden': '禁止额外字段输入',
    'finite_number': '有限值输入错误',
    'float_parsing': '浮点数输入解析错误',
    'float_type': '浮点数类型输入错误',
    'frozen_field': '冻结字段输入错误',
    'frozen_instance': '冻结实例禁止修改',
    'frozen_set_type': '冻结类型禁止输入',
    'get_attribute_error': '获取属性错误',
    'greater_than': '输入值过大',
    'greater_than_equal': '输入值过大或相等',
    'int_from_float': '整数类型输入错误',
    'int_parsing': '整数输入解析错误',
    'int_parsing_size': '整数输入解析长度错误',
    'int_type': '整数类型输入错误',
    'invalid_key': '输入无效键值',
    'is_instance_of': '类型实例输入错误',
    'is_subclass_of': '类型子类输入错误',
    'iterable_type': '可迭代类型输入错误',
    'iteration_error': '迭代值输入错误',
    'json_invalid': 'JSON 字符串输入错误',
    'json_type': 'JSON 类型输入错误',
    'less_than': '输入值过小',
    'less_than_equal': '输入值过小或相等',
    'list_type': '列表类型输入错误',
    'literal_error': '字面值输入错误',
    'mapping_type': '映射类型输入错误',
    'missing': '缺少必填字段',
    'missing_argument': '缺少参数',
    'missing_keyword_only_argument': '缺少关键字参数',
    'missing_positional_only_argument': '缺少位置参数',
    'model_attributes_type': '模型属性类型输入错误',
    'model_type': '模型实例输入错误',
    'multiple_argument_values': '参数值输入过多',
    'multiple_of': '输入值非倍数',
    'no_such_attribute': '分配无效属性值',
    'none_required': '输入值必须为 None',
    'recursion_loop': '输入循环赋值',
    'set_type': '集合类型输入错误',
    'string_pattern_mismatch': '字符串约束模式输入不匹配',
    'string_sub_type': '字符串子类型（非严格实例）输入错误',
    'string_too_long': '字符串输入过长',
    'string_too_short': '字符串输入过短',
    'string_type': '字符串类型输入错误',
    'string_unicode': '字符串输入非 Unicode',
    'time_delta_parsing': '时间差输入解析错误',
    'time_delta_type': '时间差类型输入错误',
    'time_parsing': '时间输入解析错误',
    'time_type': '时间类型输入错误',
    'timezone_aware': '缺少时区输入信息',
    'timezone_naive': '禁止时区输入信息',
    'too_long': '输入过长',
    'too_short': '输入过短',
    'tuple_type': '元组类型输入错误',
    'unexpected_keyword_argument': '输入意外关键字参数',
    'unexpected_positional_argument': '输入意外位置参数',
    'union_tag_invalid': '联合类型字面值输入错误',
    'union_tag_not_found': '联合类型参数输入未找到',
    'url_parsing': 'URL 输入解析错误',
    'url_scheme': 'URL 输入方案错误',
    'url_syntax_violation': 'URL 输入语法错误',
    'url_too_long': 'URL 输入过长',
    'url_type': 'URL 类型输入错误',
    'uuid_parsing': 'UUID 输入解析错误',
    'uuid_type': 'UUID 类型输入错误',
    'uuid_version': 'UUID 版本类型输入错误',
    'value_error': '值输入错误',
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
