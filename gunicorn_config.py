import multiprocessing


workers = 17 # 8 CPU uchun worker soni
worker_class = 'gevent'
worker_connections = 1000
bind = '0.0.0.0:8000'
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
