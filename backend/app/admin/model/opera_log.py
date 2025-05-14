#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import JSON, LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key
from backend.utils.timezone import timezone


class OperaLog(DataClassBase):
    """Operations Log Table"""

    __tablename__ = 'sys_opera_log'

    id: Mapped[id_key] = mapped_column(init=False)
    trace_id: Mapped[str] = mapped_column(String(32), comment='REQUEST TRACKING ID')
    username: Mapped[str | None] = mapped_column(String(20), comment='Username')
    method: Mapped[str] = mapped_column(String(20), comment='Type of request')
    title: Mapped[str] = mapped_column(String(255), comment='Operation module')
    path: Mapped[str] = mapped_column(String(500), comment='Request Path')
    ip: Mapped[str] = mapped_column(String(50), comment='IP ADDRESS')
    country: Mapped[str | None] = mapped_column(String(50), comment='Country')
    region: Mapped[str | None] = mapped_column(String(50), comment='Region')
    city: Mapped[str | None] = mapped_column(String(50), comment='Urban')
    user_agent: Mapped[str] = mapped_column(String(255), comment='Request Header')
    os: Mapped[str | None] = mapped_column(String(50), comment='Operating systems')
    browser: Mapped[str | None] = mapped_column(String(50), comment='Browser')
    device: Mapped[str | None] = mapped_column(String(50), comment='Equipment')
    args: Mapped[str | None] = mapped_column(JSON(), comment='Request parameters')
    status: Mapped[int] = mapped_column(comment='Operational status (0 anomaly 1)')
    code: Mapped[str] = mapped_column(String(20), insert_default='200', comment='Operational status code')
    msg: Mapped[str | None] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='Message')
    cost_time: Mapped[float] = mapped_column(insert_default=0.0, comment='request time-consuming (ms)')
    opera_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment='Operation Time')
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=timezone.now, comment='Created'
    )
