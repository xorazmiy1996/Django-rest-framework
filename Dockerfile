FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD gunicorn \
  --workers=9 \
  --worker-class=gevent \
  --worker-connections=1000 \
  --bind=0.0.0.0:8000 \
  --timeout=60 \
  --keep-alive=5 \
  --max-requests=500 \
  --max-requests-jitter=50 \
  tutorial.wsgi:application