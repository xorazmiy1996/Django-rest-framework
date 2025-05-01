### 1. `JWT Token` qachon olinadi?

`JWT` (`JSON Web Token`) tokenlar quyidagi holatlarda olinadi:

1. **Foydalanuvchi tizimga birinchi marta kirganda (`login`)**
    - Foydalanuvchi `username` va `password` ni kiritganda
    - Server ma'lumotlarni tekshirib, to'g'ri bo'lsa `JWT token` generatsiya qiladi
    - `Token` foydalanuvchiga qaytariladi va keyingi so'rovlarda ishlatiladi

2. **Tokenning muddati tugaganda (`refresh`)**
    - `Access token` odatda qisqa muddatli (**1 soat**) bo'ladi
    - `Refresh token` uzoqroq muddatli (**1 kun**) bo'ladi
    - **`Access token` eskirganda, `refresh token` yordamida yangi `access token` olinadi**

3. **Yangi qurilma yoki brauzerdan kirganda**
    - Har bir yangi qurilma yoki `brauzer` uchun yangi token olinadi
    - Bu xavfsizlik nuqtai nazaridan muhim (`token` bitta qurilmada buzilsa, boshqalarda hali amal qiladi)

4. `Token invalid` holatga kelganda
    - Agar token admin tomonidan bekor qilingan bo'lsa
    - Foydalanuvchi parolini o'zgartirganda
    - `Token` buzilgan yoki o'chirilgan bo'lsa

5. **Maxsus holatlarda**
    - `Role` (lavozim) o'zgartirilganda yangi `token` talab qilinishi mumkin
    - Qo'shimcha `permissions` (ruxsatlar) berilganda
    - Tizim xavfsizlik siyosati o'zgartirilganda

**Misol:**
**Tasavvur qiling foydalanuvchi mobil ilovadan tizimga kirishni xohlaydi:**

1. Login va parolni kiritadi
2. `Server` 2 ta `token` qaytaradi: `access` (**1 soatlik**) va `refresh` (**1 kunlik**)
3. 1 soat o'tgach, `access` token ishlamay qoladi
4. Ilova `refresh token` yordamida yangi `access token` oladi
5. Agar 1 kun o'tsa, foydalanuvchi qaytadan login-parol kiritishi kerak

> `Token` olish jarayoni odatda tizimga kirish (`authentication`) bosqichida amalga oshiriladi va keyin bu token barcha
himoyalangan so'rovlar uchun ishlatiladi.

### 2. "Agar loyihaga `JWT` qo'shilsa `AuthToken` Modeli kerak bo'lmaydi" shu to'g'rimi?

> **Ha, bu to'g'ri.** Agar loyihangizga `JWT` (`JSON Web Tokens`) ni qo'shsangiz, odatda alohida `AuthToken` modeliga
ehtiyoj qolmaydi, chunki:

**Nega AuthToken Modeli Kerak Bo'lmaydi?**

1. **`JWT` O'z-o'zini boshqaradi:**
    - `JWT` tokenlari ma'lumotlarni o'zida saqlaydi (self-contained)
    - **Serverda** tokenlarni saqlash shart emas (`stateless`)

2. **Built-in Xususiyatlar:**
    - `djangorestframework-simplejwt` paketi token yaratish, yangilash va tekshirish uchun tayyor yechimlarni taqdim
      etadi
    - Tokenlarning amal qilish muddati konfiguratsiya orqali boshqariladi

3. **Xavfsizlik afzalliklari:**
    - **Har bir token imzolangan (`signature`) bo'ladi**
    - `Token` ichidagi ma'lumotlar (`payload`) buzilganligini aniqlash mumkin

**Qachon authToken modeli kerak bo'ladi?**

1. **Maxsus talablar bo'lsa:**
    - Tokenlarni qo'lda boshqarish zarur bo'lganda
    - Har bir `token` haqida qo'shimcha ma'lumot saqlash kerak bo'lsa (masalan, `IP` `manzil`, `foydalanuvchi` agenti)

2. **Tokenlarni blacklist qilish:**

   ```python
   # settings.py
   SIMPLE_JWT = {
       'BLACKLIST_AFTER_ROTATION': True,
   }
   ```
    - Bu holda `djangorestframework-simplejwt[blacklist]` paketi o'zining modelidan foydalanadi

3. **`Multi-device` boshqaruv:**
    - Agar har bir qurilma uchun alohida token yaratish va ularni alohida boshqarish kerak bo'lsa

**Amaliy Misol**

**`JWT` bilan (`AuthToken` modelsiz):**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

**`AuthToken` bilan (eski usul):**

   ```python
   # models.py
class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
   ```

**Xulosa**

**`JWT` foydalaning, agar:**

- Sizga oddiy va `standart token` autentifikatsiyasi kerak bo'lsa
- Serverda tokenlarni saqlash shart bo'lmasa
- Tokenlarning amal qilish muddati yetarli bo'lsa

**`AuthToken` modelidan foydalaning, agar:**

- Tokenlarni qo'lda boshqarish zarur bo'lsa
- Har bir token haqida qo'shimcha ma'lumotlarni saqlash kerak bo'lsa
- Tokenlarni aniqroq monitoring qilish talab qilinsa

### 3. `Django REST Framework` da [Custom User Model](User-model.md)  uchun  `JWT` sozlash: ketma-ket qadmlar.

1. **Kerakli paketlarni o'rnatish**
   ```python
    pip install djangorestframework djangorestframework-simplejwt
   ```
2. **`settings.py` fayliga sozlamalarni qo'shish.**

   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'rest_framework_simplejwt',
       'yourapp',  # yourapp - dasturingiz nomi
       ...
   ]
   
   # My add settings
   AUTH_USER_MODEL = 'yourapp.User'  # app_name.ModelName

   AUTHENTICATION_BACKENDS = [
        'yourapp.backends.CustomUserAuthBackend', # yourapp - dasturingiz nomi, CustomUserAuthBackend - Sinzning yangi Custom User modelongiz
        'django.contrib.auth.backends.ModelBackend',
   ]

   REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',)
   }
      
   # Ixtiyoriy: Token sozlamalari (standart qiymatlar)
   SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': True,
        'UPDATE_LAST_LOGIN': False,
   
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
   }
      ```


3. **Token Serializer** `serializers.py`:
    ```python
    # serializers.py
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    from .models import User
    
    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['username'] = user.username
            return token
    
        def validate(self, attrs):
            data = super().validate(attrs)
            user = User.objects.get(username=self.user.username)
            data.update({
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
            return data
    ```






4. **`URL` manzillarini qo'shish (`urls.py`)**

   ```python
   from rest_framework_simplejwt.views import (
       TokenObtainPairView,
       TokenRefreshView,
       TokenVerifyView,
   )
   
   urlpatterns = [
       ...
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
       ...
   ]
   ```
5. **`User` Modelini Takomillashtirish**
    ```python
    class User(models.Model):
    
        # Faqat username va paroldan foydalanadigan custom user model
    
        username = models.CharField(max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
        first_name = models.CharField(max_length=30, blank=True, null=True)
        last_name = models.CharField(max_length=30, blank=True, null=True)
        password = models.CharField(max_length=128)
        last_login = models.DateTimeField(null=True, blank=True)
        is_active = models.BooleanField(default=True)  # JWT uchun kerak
    
        # Yangi manager
        objects = UserManager()
    
        # REQUIRED_FIELDS ni bo'sh ro'yxat qilib qo'ying
        REQUIRED_FIELDS = []
    
        # USERNAME_FIELD ni aniqlang
        USERNAME_FIELD = 'username'
    
    
        def set_password(self, raw_password):
            self.password = make_password(raw_password)
    
        def check_password(self, raw_password):
            return check_password(raw_password, self.password)
    
        @property
        def is_authenticated(self):
            return True
    
        @property
        def is_anonymous(self):
            """Foydalanuvchi noma'lum (anonymous) ekanligini tekshiradi"""
            return False
    
        def __str__(self):
            return self.username
    
        class Meta:
            indexes = [
                models.Index(fields=['username']),  # Qidiruvni tezlashtirish
            ]
    
    ```
6. **`User Manager` qo'shish**, `managers.py`:
    ```python
    from django.contrib.auth.base_user import BaseUserManager
    
    
    class UserManager(BaseUserManager):
        def get_by_natural_key(self, username):
            return self.get(**{self.model.USERNAME_FIELD: username})
    
        def create_user(self, username, password=None, **extra_fields):
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
        def create_superuser(self, username, password=None, **extra_fields):
            extra_fields.setdefault('is_active', True)
            return self.create_user(username, password, **extra_fields)
    ```
7. **Tokenlardan foydalanish (misollar)**

   Token olish (`login`):

   ```python
   POST /api/token/
   Content-Type: application/json
   
   {
       "username": "your_username",
       "password": "your_password"
   }
   
   # Javob:
   {
       "refresh": "eyJ0eXAiOiJKV1Qi...",
       "access": "eyJ0eXAiOiJKV1Qi..."
   }
   ```

   **Yangi `access token` olish:**

   ```python
   POST /api/token/refresh/
   Content-Type: application/json
   Authorization: Bearer your_refresh_token
   
   {
       "refresh": "eyJ0eXAiOiJKV1Qi..."
   }
   
   # Javob:
   {
       "access": "eyJ0eXAiOiJKV1Qi..."
   }
   ```
   **Tokenni tekshirish:**

   ```python
   POST /api/token/verify/
   Content-Type: application/json
   
   {
       "token": "your_token_here"
   }
   
   # Agar token yaroqli bo'lsa: status 200 OK
   # Yaroqsiz bo'lsa: status 401 Unauthorized
   ```

8. **Himoyalangan `endpoint` yaratish**

   ```python
   # views.py
   from rest_framework.views import APIView
   from rest_framework.response import Response
   from rest_framework.permissions import IsAuthenticated
   
   class ProtectedView(APIView):
       permission_classes = [IsAuthenticated]
       
       def get(self, request):
           content = {'message': 'Bu himoyalangan sahifa!'}
           return Response(content)
   ```

   **Qo'shimcha xavfsizlik choralari**

    1. **`HTTPS` majburiy qiling:**
       ```python
       # settings.py
       CSRF_COOKIE_SECURE = True
       SESSION_COOKIE_SECURE = True
       ```      
    2. **`Token` muddatini qisqartiring:**
       ```python
       # settings.py
       SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        }
        ```
    3. **`Token blacklist` ni qo'shing:**
       ```bash
       pip install django-rest-framework-simplejwt[blacklist]
       ```
       ```python
       # settings.py
       INSTALLED_APPS += ('rest_framework_simplejwt.token_blacklist',)
       SIMPLE_JWT = {
           'ROTATE_REFRESH_TOKENS': True,
           'BLACKLIST_AFTER_ROTATION': True,
       }
       ```

> Bu qadamlarni amalga oshirgandan so'ng, sizning `Django` loyihangizda `JWT` asosida to'liq ishlaydigan *
*autentifikatsiya** tizimi tayyor bo'ladi.

### 4. Barcha `JWT` xatolarini to'liq boshqarish?



### 5. `Django REST Framework` da `IsAuthenticated` ni tekchirish uchun **dekoratorlar** yoki **annotatsiyalardan**  foydalanish.

1. **`@permission_classes` Dekoratori orqali**

   **Bu eng ko‘p ishlatiladigan usul:**

   ```python
   from rest_framework.decorators import permission_classes
   from rest_framework.permissions import IsAuthenticated
   from rest_framework.response import Response
   from rest_framework.views import APIView
   
   @permission_classes([IsAuthenticated])
   class MyProtectedView(APIView):
       def get(self, request):
           return Response({"message": "Faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun!"})
   ```

   **Agar faqat bitta metoddagi so‘rovni himoya qilmoqchi bo‘lsangiz:**

   ```python
   from rest_framework.decorators import api_view, permission_classes
   
   @api_view(['GET'])
   @permission_classes([IsAuthenticated])
   def my_protected_view(request):
       return Response({"message": "Faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun!"})
   ```
2. **`@authentication_classes` bilan birgalikda**

   **Agar maxsus autentifikatsiya (`Token`, `JWT`, `Session`) kerak bo‘lsa:**

   ```python
   from rest_framework.decorators import authentication_classes, permission_classes
   from rest_framework.authentication import TokenAuthentication
   
   @api_view(['GET'])
   @authentication_classes([TokenAuthentication])
   @permission_classes([IsAuthenticated])
   def token_protected_view(request):
       return Response({"message": "Token bilan himoyalangan API!"})
   ```
3. **Annotatsiyalar orqali (`Python 3.9+` va `DRF 3.12+`)**

   `Python 3.9+` da `type` annotatsiyalardan foydalanib, `@permission_classes` ni kamroq kod bilan ishlatish mumkin:


   ```python
   from typing import Annotated
   from rest_framework.permissions import IsAuthenticated
   from rest_framework.request import Request
   from rest_framework.response import Response
   from rest_framework.decorators import api_view
   
   @api_view(['GET'])
   def my_view(request: Annotated[Request, IsAuthenticated()]):
       return Response({"message": "Annotatsiya orqali himoyalangan API!"})
   ```
4. **`DEFAULT_PERMISSION_CLASSES` orqali (`Global` sozlama)**

   Agar barcha `API` endpointlarni avtomatik himoya qilmoqchi bo‘lsangiz, `settings.py` ga yozishingiz mumkin:

   `settings.py`:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
           'rest_framework.authentication.SessionAuthentication',
       ],
   }
   ```

**Xatolikni qaytarish**


> Agar foydalanuvchi **autentifikatsiyadan** o‘tmagan bo‘lsa, `DRF` avtomatik `403 Forbidden` qaytaradi. Buni o‘zgartirish uchun `permission_denied` ni `override` qilishingiz mumkin:

```python
from rest_framework.exceptions import PermissionDenied

class CustomPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("Iltimos, avval tizimga kiring!")
        return True
```

**Natija**
- `IsAuthenticated` – faqat tizimga kirgan foydalanuvchilarga ruxsat beradi.
- `@permission_classes([IsAuthenticated])` – eng ko‘p ishlatiladigan usul.
- **Annotatsiyalar** – zamonaviy `Python` loyihalarida qulay.
- **Global sozlama** – har bir viewda yozmasdan barcha `API` ni himoya qilish uchun.

> Agar `TokenAuthentication`, `JWT` yoki boshqa usullardan foydalansangiz, `IsAuthenticated` avtomatik ishlaydi! 🔒


### 6. Quyidagi  `code` ni tushuntirib ber:

`setting.py`:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework_simplejwt.authentication.JWTAuthentication',
           # 'rest_framework.authentication.TokenAuthentication',
       ),
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```

**Tushuntirish:**

1. `DEFAULT_SCHEMA_CLASS`

   ```python
   'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
   ```
   - **Vazifasi:** `API` uchun avtomatik dokumentatsiya yaratish (`Swagger/OpenAPI`)
   - **Tushuncha:**
     - `drf_spectacular` - `DRF` uchun kuchli dokumentatsiya kutubxonasi.
     - `AutoSchema` - `API` endpointlaridan avtomatik ravishda `schema` generatsiya qiladi.

   - **Natija:** `/swagger/` yoki `/redoc/` manzillarida chiroyli `API` dokumentatsiyasi ko'rinadi.


2. `DEFAULT_AUTHENTICATION_CLASSES`

   ```python
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework_simplejwt.authentication.JWTAuthentication',
       'rest_framework.authentication.TokenAuthentication',
   ),
   ```
   - **Vazifasi:** Foydalanuvchilarni autentifikatsiya qilish usullarini belgilaydi.
   - **Tushuncha:**
     - **`JWTAuthentication` (Asosiy):**
       - `JSON` `Web` `Token` (`JWT`) asosida ishlaydi.
       - `Access` va `Refresh` tokenlarni qo'llab-quvvatlaydi.
       - Muddatli tokenlar (`access_token` 5 minut, `refresh_token` 24 soat).

     - **`TokenAuthentication` (Qo'shimcha):** 
       - Oddiy kalit so'z (`token`) asosida ishlaydi.
       - Muddatsiz, faqat `token` o'chirilgunga qadar amal qiladi.
   - **Ishlatilishi:**

     ```python
     # JWT uchun
     Authorization: Bearer <access_token>
     
     # Token uchun
     Authorization: Token <token_key>
     ```
   - **Muhim:** Agar ikkala usul ham qo'yilgan bo'lsa, `DRF` birinchisidan boshlab tekshiradi.

3. `DEFAULT_PERMISSION_CLASSES`

   ```python
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
   ```
   - **Vazifasi:** `API` endpointlariga kirish huquqini nazorat qilish.
   - **Tushuncha:**
     - `IsAuthenticated` - faqat tizimga kirgan foydalanuvchilarga ruxsat beradi.
     - Agar foydalanuvchi **autentifikatsiyadan** o'tmagan bo'lsa, `403 Forbidden` qaytaradi.
   - **Istisnolar:**
     - Agar ba'zi endpointlar ochiq bo'lishi kerak bo'lsa, `permission_classes = [AllowAny]` qo'llashingiz kerak.
   

**Umumiy tushuncha**

**Bu sozlamalar butun loyiha bo'ylab qo'llaniladi. Agar siz:**
- **Faqat `JWT` ishlatmoqchi bo'lsangiz**, `TokenAuthentication` ni olib tashlang.
- **Dokumentatsiyani o'chirmoqchi bo'lsangiz**, `DEFAULT_SCHEMA_CLASS` ni kommentga oling.
- **Barcha endpointlarni ochiq qilmoqchi bo'lsangiz**, `DEFAULT_PERMISSION_CLASSES` dan `IsAuthenticated` ni olib tashlang.

Umumiy himoylangan endpoitlarni ichidagi ba'zi endpoinlarni ochiq endpoint qilish:

```python
from rest_framework.permissions import AllowAny

class OpenView(APIView):
    permission_classes = [AllowAny]  # DEFAULT_PERMISSION_CLASSES ni bekor qiladi
    
    def get(self, request):
        return Response({"message": "Hamma ko'ra oladi!"})
```

















































































































