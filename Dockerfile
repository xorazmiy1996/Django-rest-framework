FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "8","--threads", "2", "tutorial.wsgi:application"]