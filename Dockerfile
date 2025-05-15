FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD gunicorn \
  --worker-class=gevent \
  --workers=4 \
  --bind=0.0.0.0:8000 \
  tutorial.wsgi:application