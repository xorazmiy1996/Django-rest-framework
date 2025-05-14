### 1. `PostgreSQL` dagi bazani `Dump` fayli sifatida serverga yuklash.  

- **Buyruqni to'g'ridan-to'g'ri terminalga kiriting:**
    ```bash
    pg_dump -U myuser -h localhost -p 5432 mydb > mydb_backup_$(date +%Y-%m-%d).sql 
    ```
  - **Parametrlar tushuntirishi:**
    - `-U myuser`: PostgreSQL foydalanuvchi nom
    - `-h localhost`: Server manzili (agar lokal bo'lsa)
    - `-p 5432`: PostgreSQL porti (standart 5432)
    - `mydb`: Sajov qilinadigan ma'lumotlar bazasi nomi
    - `mydb_backup_$(date +%Y-%m-%d).sql`: Natijani joriy papkaga .sql fayliga yozish (sana avtomatik qo'shiladi)
  - **Fayl qayerga saqlanadi?**
    - Dump fayli **buyruq ishga tushirilgan joriy papkaga** saqlanadi.
  - **Fayl joyini o'zgartirish (masalan, `/backups` papkasiga):**
      ```bash
      pg_dump -U myuser -h localhost -p 5432 mydb > /backups/mydb_backup_$(date +%Y-%m-%d).sql
      ```
  - **Muvaffaqiyatli `dump` olish belgilari**
    - Terminalda hech qanday xato xabari ko'rinmasligi kerak
    - Fayl ichida `SQL` komandalari ko'rinishi kerak:
  - **Terminal orqali fayl hajmini ko'rish**
    - **Oddiy Ko'rish (`ls`)**
      - `ls -lh mydb_backup.sql`
      - Natija: `-rw-r--r-- 1 user group 1.2G May 14 10:00 mydb_backup.sql` 
    - **Batafsil Ko'rish (`du` - Disk Usage)**
      - `du -h mydb_backup.sql`
      - Natija:`du -h mydb_backup.sql`

### `Dump` faylini serverda yuklab olish.

























































