FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
#CMD gunicorn \
#  --bind=0.0.0.0:8000 \
#  --workers 9 \
#  --threads 4 \
#  --worker-class gthread \
#  --max-requests 1000 \
#  --timeout 25 \
#  tutorial.wsgi:application

# Gunicorn bilan ishga tushirish, gevent worker-classini qo'shing
CMD gunicorn \
  --workers 17 \
  --worker-class gevent \
  --max-requests 1000 \
  --bind=0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive=5 \
  --max-requests-jitter=100 \
  tutorial.wsgi:application