FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD gunicorn \
  --workers=17 \
  --worker-class=gevent \
  --worker-connections=1000 \
  --bind=0.0.0.0:8000 \
  --timeout=120 \
  tutorial.wsgi:application