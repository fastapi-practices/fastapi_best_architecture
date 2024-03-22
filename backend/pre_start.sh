#!/usr/bin/env bash

alembic upgrade head

python ./scripts/init_data.py
