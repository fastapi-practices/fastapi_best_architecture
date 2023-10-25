#!/usr/bin/env bash

celery -A tasks worker --loglevel=INFO -B
