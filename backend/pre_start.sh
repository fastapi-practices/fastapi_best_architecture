#!/usr/bin/env bash

alembic revision --autogenerate

alembic upgrade head

python ./scripts/init_data.py
