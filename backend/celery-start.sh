#!/usr/bin/env bash

# work && beat
celery -A app.task.celery worker -l info -P gevent -c 100 &

# beat
celery -A app.task.celery beat -l info &

# flower
celery -A app.task.celery flower --port=8555 --basic-auth=admin:123456
