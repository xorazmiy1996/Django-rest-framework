FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .

CMD gunicorn \
  --workers=5 \
  --threads=8 \
  --worker-class=gthread \
  --bind=0.0.0.0:8000 \
  --max-requests=1000 \
  --timeout=25 \
  --preload \
  tutorial.wsgi:application

