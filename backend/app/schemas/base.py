#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel

SCHEMA_ERROR_MSG_TEMPLATES: dict[str, str] = {
    # Type Errors
    'type_error.arbitrary_type': '预期为 {expected_arbitrary_type} 的实例',
    'type_error.bool': '值不是有效的布尔值',
    'type_error.callable': '{value} 不可调用',
    'type_error.class': '预计将是一个类',
    'type_error.dataclass': '{class_name} 的实例，预期为元组或字典',
    'type_error.decimal': '值不是有效的小数（Decimal）',
    'type_error.deque': '值不是有效的双端队列',
    'type_error.dict': '值不是有效的字典',
    'type_error.enum_instance': '{value} 不是有效的枚举实例',
    'type_error.enum': '值不是有效的枚举成员; 允许：{permitted}',
    'type_error.float': '值不是有效的浮点数',
    'type_error.frozenset': '值不是有效的冻结集',
    'type_error.hashable': '值不是有效的哈希值',
    'type_error.int_enum_instance': '{value} 不是有效的 IntEnum 实例',
    'type_error.integer': '值不是有效的整数',
    'type_error.iterable': '值不是有效的可迭代对象',
    'type_error.json': 'JSON 对象必须是字符串，字节或字节数组',
    'type_error.list': '值不是有效的列表',
    'type_error.none.allowed': '值不是 None',
    'type_error.none.not_allowed': '不允许的值: None',
    'type_error.not_none': '值不是 None',
    'type_error.path': '值不是有效路径',
    'type_error.pyobject': '确保此值包含有效的导入路径或有效的可调用对象：{error_message}',
    'type_error.sequence': '值不是有效的序列',
    'type_error.set': '值不是有效的集合',
    'type_error.subclass': '预期 {expected_class} 的子类',
    'type_error.tuple': '值不是有效的元组',
    'type_error.uuid': '值不是有效的 UUID',
    # Value Errors
    'value_error.any_str.max_length': '确保此值最多包含 {limit_value} 个字符',
    'value_error.any_str.min_length': '确保此值至少包含 {limit_value} 个字符',
    'value_error.color': '值不是有效的颜色: {reason}',
    'value_error.const': '意外值; 允许: {permitted}',
    'value_error.date.not_in_the_future': '日期不在未来时间',
    'value_error.date.not_in_the_past': '日期不是过去时间',
    'value_error.decimal.max_digits': '确保总共不超过 {max_digits} 位数字',
    'value_error.decimal.max_places': '确保小数位数不超过 {decimal_places} 位',
    'value_error.decimal.not_finite': '值不是有效的小数（Decimal）',
    'value_error.decimal.whole_digits': '确保小数点前不超过 {whole_digits} 位',
    'value_error.discriminated_union.invalid_discriminator': '不匹配鉴别器 {discriminator_key!r} 和值 {discriminator_value!r}（允许的值：{allowed_values}）',  # noqa: E501
    'value_error.discriminated_union.missing_discriminator': '鉴别器 {discriminator_key!r} 的值缺失',
    'value_error.extra': '不允许使用额外字段',
    'value_error.frozenset.max_items': '确保此值最多包含 {limit_value} 个项目',
    'value_error.frozenset.min_items': '确保此值至少包含 {limit_value} 个项目',
    'value_error.invalidbytesizeunit': '无法解释字节单位: {unit}',
    'value_error.list.max_items': '确保此值最多包含 {limit_value} 个项目',
    'value_error.list.min_items': '确保此值至少包含 {limit_value} 个项目',
    'value_error.list.unique_items': '列表包含重复项',
    'value_error.missing': '必填字段',
    'value_error.number.not_finite_number': '确保此值是有限数',
    'value_error.number.not_ge': '确保此值大于或等于 {limit_value}',
    'value_error.number.not_gt': '确保此值大于 {limit_value}',
    'value_error.number.not_le': '确保此值小于或等于 {limit_value}',
    'value_error.number.not_lt': '确保此值小于 {limit_value}。',
    'value_error.number.not_multiple': '确保此值是 {multiple_of} 的倍数。',
    'value_error.path.not_a_directory': '路径 "{path}" 没有指向一个目录',
    'value_error.path.not_a_file': '路径 "{path}" 没有指向一个文件',
    'value_error.path.not_exists': '路径为 "{path}" 的文件或目录不存在',
    'value_error.payment_card_number.digits': '卡号不全是数字',
    'value_error.payment_card_number.invalid_length_for_brand': '{brand} 卡的长度必须为 {required_length}',
    'value_error.payment_card_number.luhn_check': '卡号无效',
    'value_error.regex_pattern': '无效的正则表达式',
    'value_error.set.max_items': '确保此值最多有 {limit_value} 项',
    'value_error.set.min_items': '确保此值至少有 {limit_value} 项',
    'value_error.str.regex': '字符串不符合正则 "{pattern}" 的要求。',
    'value_error.tuple.length': '错误的元组长度 {actual_length}，预期的 {expected_length}。',
    'value_error.url.extra': 'URL 无效，在有效的 URL 后发现额外的字符： [extra!r].',
    'value_error.url.host': 'URL 地址无效',
    'value_error.url.port': 'URL 端口无效，端口不能超过 65535',
    'value_error.url.scheme': '不允许的 URL 方案',
    'value_error.url.userinfo': 'URL 中需要用户信息，但缺少用户信息',
    'value_error.uuid.version': 'UUID 预期的版本 {required_version}',
}


class SchemaBase(BaseModel):
    class Config:
        use_enum_values = True
        # 错误信息模板对于模型嵌套无效
        # https://github.com/pydantic/pydantic/issues/5651
        error_msg_templates = SCHEMA_ERROR_MSG_TEMPLATES
