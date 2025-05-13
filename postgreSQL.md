### 1. `Django REST Framework` loyihasini `PostgreSQL` ga `Docker` ishlatmasdan ulash.

> Agar siz Docker ishlatmasdan, to'g'ridan-to'g'ri serverda PostgreSQL bilan Django REST Framework loyihasini ulamoqchi bo'lsangiz, quyidagi bosqichlarni bajaring.

1. **`PostgreSQL` ni o'rnatish**
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```
2. **`PostgreSQL` ni ishga tushirish**
    ```bash
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    ```
3. **Yangi foydalanuvchi va ma'lumotlar bazasini yaratish**
PostgreSQLga kirish:
    ```bash
    sudo -u postgres psql
    ```
    Foydalanuvchi va bazani yaratish:

    ```sql
    CREATE DATABASE mydb;
    CREATE USER myuser WITH PASSWORD 'mypassword';
    ALTER ROLE myuser SET client_encoding TO 'utf8';
    ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
    \q
    ```
4. **`Psycopg2` ni o'rnatish**

    ```bash
    pip install psycopg2-binary
    ```
5. **`Django` loyihasini sozlash**.`settings.py` faylini tahrirlang:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
6. `PostgreSQL` konfiguratsiyasini o'zgartirish

    `pg_hba.conf` faylini tahrirlang (odatda `/etc/postgresql/12/main/pg_hba.conf`):

    ```bash
      sudo nano /etc/postgresql/12/main/pg_hba.conf
    ```
    Quyidagi satrni topib o'zgartiring:

    ```ini
    # Original
    local   all             all                                     peer
    
    # Yangi
    local   all             all                                     md5
    ```

    **Keyin `PostgreSQL` ni qayta ishga tushiring:**
    ```bash
    sudo systemctl restart postgresql
    ```
7. **Migratsiyalarni bajarish**
    ```bash
    python manage.py migrate
    ```
8. **`Superuser` yaratish**
    ```bash
    python manage.py createsuperuser
    ```
9. **Serverni ishga tushirish**
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
**Muhim tekshirishlar**

1. PostgreSQL ulanganligini tekshirish:
    ```bash
        psql -h localhost -U myuser -d mydb -W
    ```
2. `Firewall` sozlamalari:
    ```bash
    sudo ufw allow 5432/tcp  # PostgreSQL uchun
    sudo ufw allow 8000/tcp  # Django uchun
    ```
3. `Remote` ulanish uchun (agar kerak bo'lsa):

    ```bash
    sudo nano /etc/postgresql/12/main/postgresql.conf
    ```
    `listen_addresses` parametrini o'zgartiring:

    ```bash
    listen_addresses = '*'
    ```

**Qo'shimcha xavfsizlik choralari**

1. `.env` faylidan foydalaning:
    ```python
    # settings.py
    from dotenv import load_dotenv
    load_dotenv()
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
    ```
2. `PostgreSQL` `backup` qilish:
    ```bash
    sudo -u postgres pg_dump mydb > mydb_backup.sql
    ```











































































