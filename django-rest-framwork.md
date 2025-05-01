### 1. `Django REST Framework` (`DRF`) nima?

> `Django REST Framework` (`DRF`) - bu `Django` uchun kuchli va moslashuvchan `toolkit` bo'lib, `RESTful` `API` lar
> yaratishni osonlashtiradi.

**Asosiy Xususiyatlari:**

1. `Serializer`  - Ma'lumotlarni `JSON` yoki boshqa formatlarga aylantirish va aksincha.
2. `Viewset` - `CRUD` operatsiyalarini soddalashtiradi.
3. `Authentication` - `Token`, `Session`, `OAuth` va boshqa usullarni qo'llab-quvvatlaydi.
4. `Permission`  - API'ga kirish huquqlarini boshqarish.
5. `Throttling` - So'rovlar tezligini cheklash.

### 2. `RESTful API` ma'nosi:

> `RESTful API` nomi "Representational State Transfer" (Resurslarni Tasvirlash va Ularni Almashish Uchun Dasturlararo
> Interfeys) iborasidan kelib chiqqan bo'lib, uning shunday yozilishining bir qancha mantiqiy sabablari bor:

**"Representational State Transfer" so'zma-so'z tarjima qilinganda:**

- **Representational** - Ko'rinma (ma'lumotning `JSON`, `XML` kabi formatlardagi ifodasi)
- **State** - Holat (resursning ma'lum bir vaqtdagi holati)
- `Transfer` - O'tkazish (holatning `klient-server` o'rtasida uzatilishi)
- `-ful` qo'shimchasi `tamoyillarga to'la` degan ma'noni anglatadi
- `API REST` tamoyillariga qanchalik to'liq amal qilishiga qarab:
    - Agar barcha tamoyillarga qat'iy rioya qilsa - `RESTful API`
    - Agar ba'zi tamoyillarni buzsa - `REST-like API`

**`RESTful API` ning asosiy g'oyasi:**

- Har bir `URL` (endpoint) aniq bir `resurs` ni (resource) anglatadi.
- `HTTP` metodlari (GET, POST, PUT, DELETE) orqali ushbu `resurs` ustida amallar bajariladi.
- Har bir so'rov mustaqil (`stateless`) bo'lib, server klient holatini saqlamaydi.

**Xulosa:**

> `RESTful API` - bu veb-dunyo tilida dasturlar o'rtasida ma'lumot almashishning tushunarli va tartibli usuli.

### 3. `HTTP` (`HyperText Transfer Protocol`)  nima?

> `HTTP` — bu internetda maʼlumot almashish uchun ishlatiladigan asosiy `protokol` boʻlib,
`HyperText Transfer Protocol` (Gipermatn uzatish protokoli) degan maʼnoni anglatadi.

**Asosiy `HTTP` metodlari:**

| Metod  | Oʻzbekcha        | Tavsifi                      |
|--------|------------------|------------------------------|
| GET    | OLISH            | 	Maʼlumot olish              |
| POST   | YUBORISH         | Yangi maʼlumot yuborish      |
| PUT    | YANGILASH        | 	Toʻliq maʼlumotni yangilash |
| PATCH  | QISMAN YANGILASH | Faqat bir qismini yangilash  |
| DELETE | OʻCHIRISH        | Maʼlumotni oʻchirish         |

> `HTTP` — hozirgi internetning asosi boʻlib, har bir veb-sahifaga kirganimizda, har bir `API` dan foydalanganimizda ishlatiladi. Bu `protokol` boʻlmaganida, `internet` hozirgi koʻrinishida ishlamaydi.

### 4. `Django` da `Serializer` deb nimaga aytiladi?

> `Serializer` lar `Django REST Framework` (`DRF`) ning asosiy qismi bo'lib, ma'lumotlarni bir formatdan ikkinchi formatga o'tkazish uchun ishlatiladi.

`Serializer` - bu `Django` `model` ma'lumotlarini:
1. `JSON`, `XML` kabi tushunarli formatlarga aylantirish (`serialization`)
2. Tushunarli formatlardan `Django` modeliga qayta aylantirish (`deserialization`)

**`Serializer` larning vazifalari:**
1. **Ma'lumotlarni tayyorlash** - `API` orqali yuborish uchun.
2. **Ma'lumotlarni tekshirish** - kelgan ma'lumotlarning to'g'riligini validatsiya qilish.
3. **Murakkab operatsiyalarni soddalashtirish** - `model` va `API` o'rtasida vositachi.

**`Serializer` turlari:**

1. `ModelSerializer` (eng ko'p ishlatiladi):
    
    ```python
    from rest_framework import serializers
    from .models import Book
    
    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ['id', 'title', 'author', 'price']
    ```
2. `Serializer` (asosiy klass):
    ```python
    class BookSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        author = serializers.CharField(max_length=100)
        price = serializers.DecimalField(max_digits=5, decimal_places=2)
    ```

### 5. `Django` ga `django_rest_framwork` ni o'rnatish.

```bash
    pip install django
    pip install djangorestframework
```

1. **O'rnatish bosqichlari:**
   - Birinchi navbatda virtual muhit yaratish (tavsiya etiladi):

        ```bash
        python -m venv myenv       # Virtual muhit yaratish
        source myenv/bin/activate  # Linux/MacOS uchun aktivlashtirish
        # yoki
        myenv\Scripts\activate     # Windows uchun aktivlashtirish
        ```

   - `Django` ni o'rnatish (agar hali o'rnatilmagan bo'lsa): 
       ```bash
       pip install django
       ```
   -  `Pygments` ni o'rnatish (browsable API uchun tavsiya etiladi):

       ```bash
       pip install pygments
       ```
2. `Django` loyihasida `DRF` ni sozlash:

   - `settings.py` fayliga qo'shimcha qilish:
     ```python
     INSTALLED_APPS = [
         ...
         'rest_framework',
         'rest_framework.authtoken',  # Token autentifikatsiyasi uchun (agar kerak bo'lsa)
     ]
     ```
     
   - Asosiy `DRF` konfiguratsiyasi (`settings.py` da):
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_PERMISSION_CLASSES': [
             'rest_framework.permissions.IsAuthenticated',
         ],
         'DEFAULT_AUTHENTICATION_CLASSES': [
             'rest_framework.authentication.SessionAuthentication',
             'rest_framework.authentication.TokenAuthentication',
         ],
     }
     ```
     - `DEFAULT_PERMISSION_CLASSES` - `API` endpointlariga kimlar kirishi mumkinligini belgilaydi.
       - `IsAuthenticated` - faqat tizimga kirgan (autentifikatsiyadan o'tgan) foydalanuvchilar `API` dan foydalana oladi
       - Agar foydalanuvchi tizimga kirmagan bo'lsa, `403 Forbidden` xatosi qaytariladi
       - **Boshqa variantlar:** `AllowAny` (hammaga ruxsat), `IsAdminUser` (faqat adminlar uchun)

     - `DEFAULT_AUTHENTICATION_CLASSES` - Foydalanuvchilar qanday usulda tizimga kirishi mumkinligini belgilaydi.
       - `SessionAuthentication`
         - `Django` ning standart sessiyaga asoslangan autentifikatsiya usuli
         - Brauzer orqali kirishda ishlatiladi
         - `CSRF` himoyasini talab qiladi
       - `TokenAuthentication`
         - `API` uchun maxsus `token` (kalit) asosida autentifikatsiya
         - Har bir foydalanuvchiga alohida token beriladi
         - **Headerda `Authorization`:** `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b` ko'rinishida yuboriladi
         - `Mobil` ilovalar yoki boshqa klientlar uchun qulay

 


































































































































































