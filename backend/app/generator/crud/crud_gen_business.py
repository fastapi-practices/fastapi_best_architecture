#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.generator.model import GenBusiness


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    pass
