## 任务介绍

当前任务使用 Celery
实现，实施方案请查看 [#225](https://github.com/fastapi-practices/fastapi_best_architecture/discussions/225)

## 添加任务

> [!IMPORTANT]
> 由于 Celery 任务扫描规则，使其对任务的目录结构要求及其严格，务必在 celery_task 目录下添加任务

### 简单任务

可以直接在 `tasks.py` 文件内编写相关任务代码

### 层级任务

如果你想对任务进行目录层级划分，使任务结构更加清晰，你可以新建任意目录，但必须注意的是

1. 新建目录后，务必更新任务配置 `CELERY_TASKS_PACKAGES`，将新建目录添加到此列表
2. 在新建目录下，务必添加 `tasks.py` 文件，并在此文件中编写相关任务代码

## 消息代理

你可以通过 `CELERY_BROKER` 控制消息代理选择，它支持 redis 和 rabbitmq

对于本地调试，建议使用 redis

对于线上环境，强制使用 rabbitmq
