#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class GenModelSchemaBase(SchemaBase):
    name: str
    comment: str | None = None
    type: str
    default: str | None = None
    length: int
    is_pk: bool
    is_nullable: bool
    gen_business_id: int


class CreateGenModel(GenModelSchemaBase):
    pass


class UpdateGenModel(GenModelSchemaBase):
    pass


class GetGenModelListDetails(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
