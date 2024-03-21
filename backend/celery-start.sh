#!/usr/bin/env bash

celery -A app.task.tasks worker -l info -B
