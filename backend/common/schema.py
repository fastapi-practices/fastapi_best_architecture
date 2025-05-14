#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validate_email

from backend.core.conf import settings

# Customised authentication error information, reference：
# https://github.com/pydantic/pydantic-core/blob/a5cb7382643415b716b1a7a5392914e50f726528/tests/test_errors.py#L266
# https://github.com/pydantic/pydantic/blob/caa78016433ec9b16a973f92f187a7b6bfde6cb5/docs/errors/errors.md?plain=1#L232
CUSTOM_VALIDATION_ERROR_MESSAGES = {
    'no_such_attribute': "object has no attribute '{attribute}'",
    'json_invalid': 'Invalid JSON: {error}',
    'json_type': 'JSON INPUT SHOULD BE A STRING, BYTE OR BYTE ARRAY',
    'recursion_loop': 'Recursive error - loop references detected',
    'model_type': 'enter an example that should be a valid dictionary or {class_name}',
    'model_attributes_type': 'Enter the object that should be a valid dictionary or extractable field',
    'dataclass_exact_type': 'enter an example to {class_name}',
    'dataclass_type': 'enter an example to be a dictionary or {class_name}',
    'missing': 'Fields are required',
    'frozen_field': 'Field frozen',
    'frozen_instance': 'Examples frozen',
    'extra_forbidden': 'Additional input is not allowed',
    'invalid_key': 'Key should read String',
    'get_attribute_error': 'error extracting attribute: {error}',
    'none_required': 'Input should read None',
    'enum': 'input should read {expected}',
    'greater_than': 'input should be greater than {gt}',
    'greater_than_equal': 'enter should be greater than or equal to {ge}',
    'less_than': 'input should be less than {lt}',
    'less_than_equal': 'input should be less than or equal to {le}',
    'finite_number': 'Enter should be limited',
    'too_short': '{field_type} should have at least {min_length} items after validation, not {actual_length} items',
    'too_long': '{field_type} up to {max_length} items after validation, not {actual_length}',
    'string_type': 'Enter should be a valid string',
    'string_sub_type': 'enter as a string, not an example of a sstr subcategory',
    'string_unicode': 'Enter to be a valid string. The original data cannot be parsed as a Unicode string',
    'string_pattern_mismatch': "string should match mode '{pattern} '",
    'string_too_short': 'string should have at least {min_length} characters',
    'string_too_long': 'string should have up to {max_length} characters',
    'dict_type': 'Enter should be a valid dictionary',
    'mapping_type': 'input should be a valid map, error: {error}',
    'iterable_type': 'Input should be an iterative object',
    'iteration_error': 'error while',
    'list_type': 'Enter a list that should be valid',
    'tuple_type': 'Input should be a valid group',
    'set_type': 'Input should be a valid collection',
    'bool_type': 'Enter should be a valid boolean value',
    'bool_parsing': 'The input should be a valid boolean value, which cannot be explained',
    'int_type': 'Enter the integer to be valid',
    'int_parsing': 'Enter to be a valid integer, unable to resolve string to integer',
    'int_parsing_size': 'Unable to resolve input string to integer, exceeding maximum size',
    'int_from_float': 'Enter the integer to be valid and get a number with decimal parts',
    'multiple_of': 'enter the multiple of {multiple_of}',
    'float_type': 'Enter should be a valid number',
    'float_parsing': 'Enter should be a valid number and cannot resolve a string to a number',
    'bytes_type': 'Enter should be valid bytes',
    'bytes_too_short': 'data should have at least {min_length} bytes',
    'bytes_too_long': 'data should have up to {max_length} bytes',
    'value_error': 'error value, {error}',
    'assertion_error': 'the claim fails',
    'literal_error': 'input should read {expected}',
    'date_type': 'Enter should be the valid date',
    'date_parsing': 'Enter a valid date in YYY-MM-DD format, {error}',
    'date_from_datetime_parsing': 'enter to be valid date or date time, {error}',
    'date_from_datetime_inexact': 'The date given should have zero time - e.g. precise date',
    'date_past': 'The date should be the past time',
    'date_future': 'The date shall be the time of the future',
    'time_type': 'Enter should be valid time',
    'time_parsing': 'input should be a valid time format, {error}',
    'datetime_type': 'Enter to be valid date time',
    'datetime_parsing': 'enter should be valid date time, {error}',
    'datetime_object_invalid': 'invalid date time object, get {error}',
    'datetime_past': 'Enter should be the past time',
    'datetime_future': 'The input should be the time of the future',
    'timezone_naive': 'Enter should not contain time zone information',
    'timezone_aware': 'Enter should contain time zone information',
    'timezone_offset': 'timezone offset to {z_expected}, actually {z_actual}',
    'time_delta_type': 'Enter should be a valid time difference',
    'time_delta_parsing': 'input should be a valid time difference, {error}',
    'frozen_set_type': 'Enter should be a valid freeze collection',
    'is_instance_of': 'enter an instance to {class}',
    'is_subclass_of': 'enter subcategory to {class}',
    'callable_type': 'Input should be a callable object',
    'union_tag_invalid': "use {discriminator} to find input label '{tag}' that does not match any expected label: {expected_tags}",
    'union_tag_not_found': 'could not use the differentiated {discriminator} extract label',
    'arguments_type': 'Parameters must be form, list or dictionary',
    'missing_argument': 'Missing required parameters',
    'unexpected_keyword_argument': 'unexpected keyword parameter',
    'missing_keyword_only_argument': 'Lack of required keyword-specific parameters',
    'unexpected_positional_argument': 'Unexpected location parameters',
    'missing_positional_only_argument': 'Missing required location-specific parameters',
    'multiple_argument_values': 'Multiple values provided for parameters',
    'url_type': 'URL INPUT SHOULD BE STRING OR URL',
    'url_parsing': 'Input should be a valid URL, {error}',
    'url_syntax_violation': 'The input violated strict URL syntax, {error}',
    'url_too_long': 'URL should have a maximum of {max_length} characters',
    'url_scheme': 'URL scheme should read',
    'uuid_type': 'UUID INPUT SHOULD BE A STRING, BYTE OR UUID OBJECT',
    'uuid_parsing': 'Input should be valid UUID, {error}',
    'uuid_version': 'Expected UUID version to {expected_version}',
    'decimal_type': 'Decimal input should be integer, floating point number, string or Decimal object',
    'decimal_parsing': 'Enter to be a valid decimal number',
    'decimal_max_digits': 'decimal input should not exceed {max_digits} bits',
    'decimal_max_places': 'decimal input should not exceed {decimal_places} decimal places',
    'decimal_whole_digits': 'decimal input should not exceed {whole_digits} bits before decimal points',
}

CustomPhoneNumber = Annotated[str, Field(pattern=r'^1[3-9]\d{9}$')]


class CustomEmailStr(EmailStr):
    """Custom Mailbox Type"""

    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == '' else validate_email(__input_value)[1]


class SchemaBase(BaseModel):
    """Basic model configuration"""

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda x: x.strftime(
            settings.DATETIME_FORMAT)},
    )
