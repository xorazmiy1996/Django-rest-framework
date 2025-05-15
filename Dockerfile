FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN apk update && apk add curl
COPY . .
CMD ["gunicorn", "-c", "gunicorn_config.py", "tutorial.wsgi:application"]
