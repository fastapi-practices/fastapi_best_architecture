#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class GenModelSchemaBase(SchemaBase):
    name: str
    comment: str | None = None
    type: str
    default: str | None = None
    sort: int
    length: int
    is_pk: bool
    is_nullable: bool
    gen_business_id: int | None


class CreateGenModelParam(GenModelSchemaBase):
    pass


class UpdateGenModelParam(GenModelSchemaBase):
    pass


class GetGenModelListDetails(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
