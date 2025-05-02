FROM python:3.13.2
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
COPY . .
CMD python manage.py migrate && \
    exec gunicorn --bind 0.0.0.0:8000 tutorial.wsgi:application