import multiprocessing


workers = multiprocessing.cpu_count() * 2 + 1 # 8 CPU uchun worker soni
threads = 30
worker_class = 'gthread'  # Asinxron I/O uchun worker klassi
worker_connections = 1000  # Har bir workerdagi ulanishlar soni
bind = '0.0.0.0:8000' # IP manzil va port
timeout = 30 # So'rovga javob berish vaqti
keepalive = 5 # Ulanishni saqlab turish
max_requests = 1000 # Har bir workerning qayta ishga tushishi uchun so'rovlar soni
max_requests_jitter = 50 # Qayta ishga tushirish vaqtini tasodifiy o'zgartirish
