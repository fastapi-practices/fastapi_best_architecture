#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses

from collections import defaultdict
from enum import Enum
from pathlib import PurePath
from types import GeneratorType
from typing import Any, Callable, Iterable

from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE

SetIntStr = set[int | str]
DictIntStrAny = dict[int | str, Any]

PRIMITIVE_TYPE = (str, bool, int, float, type(None))
ARRAY_TYPES = (list, set, frozenset, GeneratorType, tuple)


def _generate_encoders_by_class_tuples(
    type_encoder_map: dict[Any, Callable[[Any], Any]]
) -> dict[Callable[[Any], Any], tuple[Any, ...]]:
    encoders_by_class_tuples: dict[Callable[[Any], Any], tuple[Any, ...]] = defaultdict(tuple)
    for type_, encoder in type_encoder_map.items():
        encoders_by_class_tuples[encoder] += (type_,)
    return encoders_by_class_tuples


encoders_by_class_tuples = _generate_encoders_by_class_tuples(ENCODERS_BY_TYPE)


def jsonable_encoder(
    obj: Any,
    include: SetIntStr | DictIntStrAny | None = None,
    exclude: SetIntStr | DictIntStrAny | None = None,
    by_alias: bool = True,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    custom_encoder: dict[Any, Callable[[Any], Any]] | None = None,
    sqlalchemy_safe: bool = True,
) -> Any:
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)

    def encode_dict(obj: Any) -> Any:
        encoded_dict = {}
        allowed_keys = set(obj.keys())
        if include is not None:
            allowed_keys &= set(include)
        if exclude is not None:
            allowed_keys -= set(exclude)

        for key, value in obj.items():
            if (
                (not sqlalchemy_safe or (not isinstance(key, str)) or (not key.startswith('_sa')))
                and (value is not None or not exclude_none)
                and key in allowed_keys
            ):
                if isinstance(key, PRIMITIVE_TYPE):
                    encoded_key = key
                else:
                    encoded_key = jsonable_encoder(
                        key,
                        by_alias=by_alias,
                        exclude_unset=exclude_unset,
                        exclude_none=exclude_none,
                        custom_encoder=custom_encoder,
                        sqlalchemy_safe=sqlalchemy_safe,
                    )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict

    def encode_array(obj: Iterable[Any]) -> Any:
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    def encode_base_model(obj: BaseModel) -> Any:
        encoder = getattr(obj.__config__, 'json_encoders', {})
        if custom_encoder:
            encoder.update(custom_encoder)

        obj_dict = obj.dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if '__root__' in obj_dict:
            obj_dict = obj_dict['__root__']

        return jsonable_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            custom_encoder=encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )

    # Use type comparisons on common types before expensive isinstance checks
    if type(obj) in PRIMITIVE_TYPE:
        return obj
    if isinstance(obj, dict):
        return encode_dict(obj)
    if type(obj) in ARRAY_TYPES:
        return encode_array(obj)

    if isinstance(obj, BaseModel):
        return encode_base_model(obj)
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)
        return encode_dict(obj_dict)
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)

    # Back up for Inherited types
    if isinstance(obj, PRIMITIVE_TYPE):
        return obj
    if isinstance(obj, dict):
        return encode_dict(obj)
    if isinstance(obj, ARRAY_TYPES):
        return encode_array(obj)

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    try:
        data = dict(obj)
    except Exception as e:
        errors: list[Exception] = [e]
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors)

    return encode_dict(data)
