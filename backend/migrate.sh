#!/usr/bin/env bash

alembic revision --autogenerate

alembic upgrade head
