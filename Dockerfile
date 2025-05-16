FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD gunicorn \
  --workers 9 \
  --thread 50 \
  --worker-class gevent \
  --max-requests 5000 \
  --bind=0.0.0.0:8000 \
  --timeout 90 \
  --keep-alive 5 \
  --max-requests-jitter 100 \
  tutorial.wsgi:application

