### 1. PostgreSQL foydalanuvchisini tekshirish va muammoni bartaraf etish.

> PostgreSQL foydalanuvchisi login parolini tekshirish uchun quyidagi amallarni bajaring:

1. **`PostgreSQL`-ga `root` foydalanuvchi sifatida ulaning**
    ```bash
    sudo -u postgres psql
    ```
2. **Mavjud foydalanuvchilarni ko'rish**
    ```sql
    SELECT usename FROM pg_user;
    ```
3. **Foydalanuvchi ma'lumotlarini tekshirish**
    ```sql
    \du
    ```
> Bu buyruq barcha foydalanuvchilar va ularning rollarini ko'rsatadi.
4. **Foydalanuvchi parolini o'zgartirish**

    Agar parol noto'g'ri bo'lsa, yangi parol o'rnating:
    
    ```sql
    ALTER USER your_username WITH PASSWORD 'new_password';
    ```
5. **Foydalanuvchining databasega kirish huquqini tekshirish**

    ```sql
    SELECT datname FROM pg_database;
    ```





























































































