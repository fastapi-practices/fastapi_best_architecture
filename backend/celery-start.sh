#!/usr/bin/env bash

celery -A app.task.celery worker -l info -B
