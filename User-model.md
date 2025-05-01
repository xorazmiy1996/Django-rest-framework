### 1. `Django REST Framework` uchun `User Model` ni qanday tanlash kerak?

`Django` standart `user` modelidan foydalanmasdan to'liq `custom` yechim yaratish haqida qaror qabul qilishda quyidagi omillarni hisobga olish kerak:

**Standart User Modeldan Foydalanish Afzalliklari**

1. **Vaqtni tejash:**
    - `Django` allaqachon tayyor `authentication` tizimini taklif qiladi
    - **Parol hashlash**, `session` boshqaruv, `permission` tizimi o'rnatilgan
2. **Xavfsizlik:**
   - Ko'p yillik tajriba bilan ishlab chiqilgan
   - `OOV` (`OWASP`) talablariga javob beradi
3. **Ekosistema bilan mosligi:**
   - `Admin panel`, `third-party` paketlar (`allauth`, `django-rest-auth`) bilan ishlaydi
   - DRF ning barcha `authentication` klasslari bilan mos keladi
4. **Qo'llab-quvvatlash:**
   - Katta jamoatchilik tomonidan qo'llab-quvvatlanadi
   - Har doim yangilanib turadi

**To'liq `custom` yechim afzalliklari**

1. **Moslashuvchanlik:**
   - Har qanday maydonlarni qo'shish imkoniyati
   - O'zingizning `authentication` mantiqingiz
2. **Oddiylik:**
   - Faqat kerakli funksiyalarni implement qilish
   - Keraksiz narsalarsiz ishlash
3. **Maxsus talablar:**
   - Noan'anaviy `authentication` usullari (`SMS`, `biometrics`)
   - `Mikroservis` arxitekturasida ishlatish

> Qachon `Custom` yechim tanlash kerak?

Quyidagi hollarda to'liq `custom` yechim yaxshi fikr bo'lishi mumkin:

1. Standart `user model` talablaringizga to'liq mos kelmasa:
   - Misol uchun, faqat telefon raqam bilan autentifikatsiya
2. Django `admin` paneli umuman ishlatilmasa:
   - Faqat `API` orqali ishlaydigan tizim
3. Maxsus xavfsizlik talablari bo'lsa:
   - `Industry-specific` standartlar (`HIPAA`, `PCI` `DSS`)
4. **Microservice arxitekturada ishlatilsa:**
   - `Minimal Django` funksionalligi kerak bo'lganda

**Tavsiya**

> Agar yangi boshlayotgan bo'lsangiz yoki maxsus talablaringiz bo'lmasa, `Django` standart `user` modelidan foydalaning (`AbstractUser` yoki `AbstractBaseUser`).

**Buning uchun `minimal custom` yechim:**

```python
# models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    
    # DRF uchun kerak bo'ladigan metodlar
    @property
    def is_authenticated(self):
        return True
```

**Agar quyidagilar kerak bo'lsa, to'liq `custom` yechim yarating:**

- Standart `username/email/parol` tizimidan boshqa **autentifikatsiya**
- `Django` `admin` paneli ishlatilmaydi
- `Mikroservis` arxitektura
- `Maxsus permission` tizimi

**`Custom` yechimda diqqatga olish kerak bo'lgan narsalar:**

1. **Parol xavfsizligi:**
   ```python
   from django.contrib.auth.hashers import make_password, check_password
   
   user.password = make_password(raw_password)
   check_password(raw_password, user.password)
   ```
2. **Session boshqaruvi:**
   - `DRF TokenAuthentication` yoki `JWT` ishlatish
3. **Permission tizimi:**
   - `DRF` `permission` klasslarini to'g'ri `implement` qilish

4. **Migratsiyalar:**
   - `Custom` modelni `AUTH_USER_MODEL` sifatida belgilash
**Yakuniy Qaror**

**Agar loyihangizda:**
- `API` orqali `autentifikatsiya` (`DRF`)
- Standart `username/email` va `parol` ishlatilsa
- `Admin panel` kerak bo'lmasa
> `AbstractBaseUser` dan foydalaning - bu optimal yechim bo'ladi. To'liq `custom` yechim faqat chindan ham zarurat bo'lganda yarating.

### 2. `Django REST Framework` uchun to'liq `custom user model` yaratish (`Step-by-Step`)

Agar siz Django standart `user` modelidan butunlay voz kechib, to'liq `custom` yechim yaratmoqchi bo'lsangiz, quyidagi qadamlarni bajaring:

1. Asosiy `User` Modelini Yaratish

   ```python
   # models.py
   from django.db import models
   from django.contrib.auth.hashers import make_password, check_password
   
   class User(models.Model):
       USER_TYPES = (
           ('customer', 'Mijoz'),
           ('admin', 'Administrator'),
           ('manager', 'Menejer'),
       )
       
       # Identifikatsiya maydonlari
       username = models.CharField(max_length=50, unique=True)
       email = models.EmailField(unique=True, blank=True, null=True)
       phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
       
       # Autentifikatsiya maydonlari
       password = models.CharField(max_length=128)
       last_login = models.DateTimeField(blank=True, null=True)
       
       # Status maydonlari
       user_type = models.CharField(max_length=20, choices=USER_TYPES)
       is_active = models.BooleanField(default=True)
       created_at = models.DateTimeField(auto_now_add=True)
       
       # Parol bilan ishlash metodlari
       def set_password(self, raw_password):
           self.password = make_password(raw_password)
       
       def check_password(self, raw_password):
           return check_password(raw_password, self.password)
       
       # Django REST Framework uchun kerak bo'ladigan metodlar
       @property
       def is_authenticated(self):
           return True
       
       def __str__(self):
           return self.username
   ```
2. `Custom authentication backend` yaratish

   ```python
   # backends.py
   from django.contrib.auth.backends import BaseBackend
   from .models import User
   
   class CustomUserBackend(BaseBackend):
       def authenticate(self, request, username=None, password=None, **kwargs):
           try:
               # Telefon yoki email orqali ham login qilish imkoniyati
               if '@' in username:
                   user = User.objects.get(email=username)
               elif username.isdigit():
                   user = User.objects.get(phone=username)
               else:
                   user = User.objects.get(username=username)
               
               if user.check_password(password):
                   return user
           except User.DoesNotExist:
               return None
       
       def get_user(self, user_id):
           try:
               return User.objects.get(pk=user_id)
           except User.DoesNotExist:
               return None
   ```
3. `settings.py` sozlamalari

   ```python
   # settings.py
   AUTH_USER_MODEL = 'yourapp.User'  # Custom modelni ko'rsating
   AUTHENTICATION_BACKENDS = ['yourapp.backends.CustomUserBackend']
   
   # REST Framework sozlamalari
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'yourapp.authentication.CustomTokenAuthentication',  # Keyingi qadamda yaratamiz
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```
4. **`Token` autentifikatsiya tizimi (`JWT` yoki `Custom Token`)**

   ```python
   # authentication.py
   from rest_framework.authentication import BaseAuthentication
   from rest_framework.exceptions import AuthenticationFailed
   from .models import User, AuthToken
   import secrets
   from datetime import datetime, timedelta
   
   class CustomTokenAuthentication(BaseAuthentication):
       def authenticate(self, request):
           token = request.headers.get('Authorization', '').split(' ')[-1]
           if not token:
               return None
           
           try:
               auth_token = AuthToken.objects.get(token=token)
               if auth_token.expires_at < datetime.now():
                   raise AuthenticationFailed('Token muddati tugagan')
               return (auth_token.user, None)
           except AuthToken.DoesNotExist:
               raise AuthenticationFailed('Yaroqsiz token')
   
   # Token modeli
   class AuthToken(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       token = models.CharField(max_length=64, unique=True)
       created_at = models.DateTimeField(auto_now_add=True)
       expires_at = models.DateTimeField()
   
       @classmethod
       def create_token(cls, user, expires_in=3600*24*7):  # 1 hafta
           token = secrets.token_hex(32)
           expires_at = datetime.now() + timedelta(seconds=expires_in)
           return cls.objects.create(
               user=user,
               token=token,
               expires_at=expires_at
           )
   ```
5. **Serializerlar va Viewlar**

`serializers.py`:

   ```python
   # serializers.py
   from rest_framework import serializers
   from .models import User
   
   class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = User
           fields = ['id', 'username', 'email', 'phone', 'user_type']
           extra_kwargs = {'password': {'write_only': True}}
   
   class LoginSerializer(serializers.Serializer):
       username = serializers.CharField()
       password = serializers.CharField(write_only=True)
   
       def validate(self, attrs):
           user = CustomUserBackend().authenticate(
               request=self.context.get('request'),
               username=attrs['username'],
               password=attrs['password']
           )
           if not user:
               raise serializers.ValidationError("Login yoki parol noto'g'ri")
           return {'user': user}
   ```
`views.py`:

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from .authentication import AuthToken

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AuthToken.create_token(user)
        return Response({
            'token': token.token,
            'user': UserSerializer(user).data
        })
```
6. **`Permission` Tizimi**

`permissions.py`:

```python
# permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'admin'

class HasUserType(permissions.BasePermission):
    def __init__(self, user_types):
        self.user_types = user_types
    
    def has_permission(self, request, view):
        return request.user.user_type in self.user_types
```

7. **`Migratsiyalarni` Qo'llash**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
**Muhim Nuqtalar:**

1. **Parol Xavfsizligi:**
   - Har doim `make_password` va `check_password` dan foydalaning
   - Hech qachon parollarni oddiy text shaklda saqlamang

2. **Token Xavfsizligi:**
   - Tokenlarni xavfsiz generatsiya qiling (`secrets` moduli)
   - Tokenlarning muddatini cheklang
   
3. **Test Qilish:**
   - Barcha `authentication` va `permission` scenariylarini test qiling
   - Xatoliklarni qayta ishlashni unutmang
4. **Dokumentatsiya:**
   - `API` endpointlari uchun yaxshi dokumentatsiya yozing (`Swagger` yoki `drf-yasg`)

**Bu yondashuv sizga:**
   - `Django` standart `user` modeliga bog'liq bo'lmaslik
   -  To'liq `custom` `authentication` tizimi
   - O'zingizning `permission` mantiqingiz
   - Moslashuvchan arxitektura

### 3. `JWT` yoki `Custom Token`, qaysi birini tanlash kerak

1. **`JWT` (JSON Web Token)**
   - `Afzalliklari`:
     - **Standartlashtirilgan:** `RFC 7519` standarti bo'yicha ishlab chiqilgan
     - **Stateless:** Serverda `session` saqlash shart emas
     - **Keng qo'llab-quvvatlash:** Ko'plab tillar va frameworklar uchun kutubxonalar mavjud
     - **O'z ichiga ma'lumot oladi (payload):** Foydalanuvchi haqida qo'shimcha ma'lumotlarni saqlash mumkin
     - **Yaroqlilik muddati:** Tokenning amal qilish muddatini o'rnatish oson
   **Kamchiliklari**
     - **Kattaroq hajm:** Har bir so'rovda yuboriladi
     - **Bekor qilib bo'lmaydi:** Token yaroqli bo'lsa, muddati tugagunga qadar foydalanish mumkin
     - **Xavfsizlik nuqtalari:** Agar o'g'irlansa, muddati tugagunga qadar foydalanish mumkin

   **Qo'llash Misoli:**

      ```python
      # settings.py
      REST_FRAMEWORK = {
          'DEFAULT_AUTHENTICATION_CLASSES': [
              'rest_framework_simplejwt.authentication.JWTAuthentication',
          ],
      }
      ```

2. **Custom Token**
   - **Afzalliklari:**
     - **Oddiy va yengil:** Faqat random string va ma'lumotlar bazasi yozuvi
     - **To'liq nazorat:** Tokenlarni bekor qilish, yangilash imkoniyati
     - **Kichik hajm:** Faqat token stringini saqlash kifoya
     - **Xavfsizroq:** Har bir tokenni alohida tekshirish mumkin

   **Kamchiliklari**
   - **Stateful:** Har bir token uchun ma'lumotlar bazasida yozuv bo'lishi kerak
   - **Scalability muammolari:** Ko'p foydalanuvchilar bilan ishlashda muammolar yuzaga kelishi mumkin
   - **Qo'lda implementatsiya:** Barcha funksionallikni o'zingiz yozishingiz kerak

   **Qo'llash Misoli:**
   ```python
   # authentication.py
   class CustomTokenAuthentication(BaseAuthentication):
       def authenticate(self, request):
           token = request.headers.get('Authorization', '').split(' ')[-1]
           if not token:
               return None
           
           try:
               auth_token = AuthToken.objects.get(token=token)
               if auth_token.expires_at < timezone.now():
                   raise AuthenticationFailed('Token expired')
               return (auth_token.user, None)
           except AuthToken.DoesNotExist:
               raise AuthenticationFailed('Invalid token')
   ```

**Qaysi Birini Tanlash Kerak?**

**`JWT` ni tanlang, agar:**
   - `Mikroservice` arxitekturada ishlayotgan bo'lsangiz
   - `Stateless authentication` kerak bo'lsa
   - Tokenlarni tez-tez bekor qilish shart bo'lmasa
   - Ko'plab tizimlar o'rtasida `token` almashinuvi kerak bo'lsa

**Custom Token ni tanlang, agar:**
   - Tokenlarni bekor qilish imkoniyati muhim bo'lsa
   - Oddiy va nazorat qilinadigan yechim kerak bo'lsa
   - Kichik loyihalar uchun ishlayotgan bo'lsangiz
   - Ma'lumotlar bazasiga bog'liq bo'lish muammo bo'lmasa

**(`Hybrid`=texnologiyalar yoki tizimlarning birlashuvi) Yechim (Tavsiya etilgan)**

   ```python
   # settings.py
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
           'yourapp.authentication.CustomTokenAuthentication',
       ],
   }
   ```

   **Bu yondashuvda:**

   1. Asosiy autentifikatsiya uchun `JWT` dan foydalaning  
   2. Maxsus holatlar uchun (masalan, parolni o'zgartirgandan keyin) `Custom Token` yordamida eski tokenlarni bekor qiling

**Xavfsizlik Choralari**
   1. **`HTTPS`:** Har doim `HTTPS` orqali tokenlarni uzating
   2. **Qisqa muddat:** Tokenlarning yaroqlilik muddatini qisqa qilib o'rnating
   3. **`Refresh token`:** `JWT` uchun refresh tokenlardan foydalaning
   4. **`Blacklist`:** `JWT` uchun `blacklist` implement qiling (agar kerak bo'lsa)

> Har ikkala yechim ham `Django REST Framework` bilan yaxshi ishlaydi, tanlov loyihangizning talablariga bog'liq.


### 4. Quyida UserBalance  modeli:
```python
class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='balance')
    main_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    frozen_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_transaction_id = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict)  # Standart Django JSONField
```

Ushbu modeldan foydalanib `UserBalance` obyekti  yaratish uchun `UserBalance.objects.create(user = ?)` `?` o'rniga  nima qo'yish kerak.

`Javob`:

> So'roq belgisi (`?`) o'rniga faqat `User` **obyekti** berishingiz kerak. `UserBalance` modelidagi `user` fieldi `OneToOneField` bo'lgani uchun, u faqat `User` obyektini qabul qiladi. Boshqa turdagi ma'lumotlar (masalan, `User` obyektining `ID` si, `username`  yoki `email`) qabul qilinmaydi. Siz aynan `User` obyektining o'zini berishingiz kerak.

`Misol`:

```python
from django.contrib.auth.models import User

# Mavjud User obyektini olish (username bo'yicha)
username = 'testuser'
user = User.objects.get(username=username)

# UserBalance obyektini yaratish
user_balance = UserBalance.objects.create(user=user)

print(f"UserBalance obyekti yaratildi: {user_balance}")
```










































































































