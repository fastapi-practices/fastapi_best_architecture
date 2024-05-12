#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.generator.model import GenModel


class CRUDGenModel(CRUDPlus[GenModel]):
    async def get_with_relation(self, db: AsyncSession, business_id: int) -> Sequence[GenModel]:
        gen_model = await db.execute(select(self.model).where(self.model.gen_business_id == business_id))
        return gen_model.scalars().all()


gen_model_dao = CRUDGenModel(GenModel)
