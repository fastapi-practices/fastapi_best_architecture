# 监听内网端口
bind = "0.0.0.0:8001"

# 工作目录
chdir = "/fba/backend/"

# 并行工作进程数
workers = 1

# 指定每个工作者的线程数
threads = 4

# 监听队列
backlog = 512

# 超时时间
timeout = 120

# 设置守护进程,将进程交给 supervisor 管理；如果设置为 True 时，supervisor 启动日志为：
# gave up: fastapi_server entered FATAL state, too many start retries too quickly
# 则需要将此改为: False
daemon = False

# 工作模式协程
worker_class = "uvicorn.workers.UvicornWorker"

# 设置最大并发量
worker_connections = 2000

# 设置进程文件目录
pidfile = "/fba/gunicorn.pid"

# 设置访问日志和错误信息日志路径
accesslog = "/var/log/fastapi_server/gunicorn_access.log"
errorlog = "/var/log/fastapi_server/gunicorn_error.log"

# 设置这个值为true 才会把打印信息记录到错误日志里
capture_output = True

# 设置日志记录水平
loglevel = "debug"

# python程序
pythonpath = "/usr/local/lib/python3.10/site-packages"

# 启动 gunicorn -c gunicorn.conf.py main:app
