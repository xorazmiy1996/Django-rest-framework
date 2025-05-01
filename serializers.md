### 1. `serialization` nima?

> `Serialization` (**serializatsiya**) - bu ma'lumotlarni bir formatdan boshqa formatga aylantirish jarayoni. Django
> REST Framework (DRF)da serializatsiya quyidagilarni anglatadi:

**Serializatsiya nima?**

1. `Model → JSON/XML` - `Django` modellarini yoki Python ma'lumotlar tuzilmalarini (masalan, `querysets`) `frontend`yoki
   boshqa tizimlar uchun ishlatiladigan `JSON` yoki `XML` formatiga aylantirish.
2. `JSON/XML → Model` - Kelgan `JSON` yoki `XML` ma'lumotlarini `Django` modellariga aylantirish (deserialization).

**Nega Kerak?**

- **`API` yaratish:** `Frontend` (`JavaScript`) bilan `backend` (`Python`) o'rtasida ma'lumot almashinuvi uchun
- **Ma'lumotlarni standartlashtirish:** Barcha ma'lumotlar bir xil strukturada bo'lishi uchun
- **Xavfsizlik:** Faqat kerakli maydonlarni **jo'natish/o'qish** imkoniyati

**Serializer Turlari:**

1. **`ModelSerializer` (eng ko'p ishlatiladi):**
    ```python
    from rest_framework import serializers
    from .models import Book
    
    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ['id', 'title', 'author', 'price']
    ```
2. **`Serializer` (asosiy klass):**
    ```python
    class UserSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField(max_length=100)
    ```

**Misol: Serializatsiya va Deserializatsiya**

```python
# Modeldan JSONga
book = Book.objects.get(id=1)
serializer = BookSerializer(book)
serializer.data  # {'id': 1, 'title': 'Django for Beginners', ...}

# JSONdan Modelga
data = {'title': 'New Book', 'author': 'John Doe', 'price': 29.99}
serializer = BookSerializer(data=data)
if serializer.is_valid():
    book = serializer.save()
```

> `DRF` serializatorlari shuningdek **validatsiya** qilish, **murakkab maydonlar** (`relations`) bilan ishlash va *
*custom maydonlar** qo'shish imkoniyatlarini beradi.

### 2. **Serializatorlar** bilan ishlash

`serializers.py`:

```python
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Tekshirilgan ma'lumotlarga asoslanib, yangi Snippet instansiyasini yarating va qaytaring.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Tekshirilgan ma'lumotlarga asoslanib, mavjud Snippet instansiyasini yangilang va qaytaring. 
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```

> Biz `Serializer` klassimizdan qanday foydalanishni o'rganamiz. Keling, `Django shell` iga o'tamiz.

   ```bash
       python manage.py shell
   ```

   ```bash
      from snippets.models import Snippet
      from snippets.serializers import SnippetSerializer
      from rest_framework.renderers import JSONRenderer
      from rest_framework.parsers import JSONParser
   
      snippet = Snippet(code='foo = "bar"\n')
      snippet.save()
   
      snippet = Snippet(code='print("hello, world")\n')
      snippet.save()
   ```

Hozirgacha bizda bir nechta `snippet` (koddan parchalar) namunalari mavjud. Keling, ulardan birini **serializatsiya**
qilishni ko'rib chiqaylik.

> `serializatsiya => serializer qilish` — bu ma'lumotlarni saqlangan shakldan (masalan, **ob'ektlar**) internetda
> ishlatiladigan shaklga (masalan, `JSON`) o'tkazish jarayonidir.

```ini
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

Bu nuqtada biz model **instansiyasini** `Python` ning tabiiy ma'lumot turlariga tarjima qildik. `Serialization`
jarayonini yakunlash uchun ma'lumotlarni `JSON` formatida chiqaramiz.

```ini
content = JSONRenderer().render(serializer.data)
content
# b'{"id":2,"title":"","code":"print(\\"hello, world\\")\\n","linenos":false,"language":"python","style":"friendly"}'
```

`Deserialization` jarayoni ham shunga o'xshash. Avval biz oqimni `Python` ning tabiiy ma'lumot turlariga `parse`
qilamiz...

```ini
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```

...keyin biz ushbu tabiiy ma'lumot turlarini to'liq to'ldirilgan **ob'ekt instansiyasiga** tiklaymiz

```ini
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}
serializer.save()
# <Snippet: Snippet object>
```

**`serializer = SnippetSerializer(data=data)` ushbu sintaksis quyidagi vazifani bajaradi:**

- `data=data`:
    - `data` argumenti orqali siz serializerga yuboriladigan ma'lumotlarni berasiz. Bu yerda `data` o'zgaruvchisi,
      odatda, foydalanuvchi tomonidan yuborilgan ma'lumotlar (masalan, `JSON` formatida) bo'ladi.
    - Ushbu kod `SnippetSerializer` ga yangi ma'lumotlarni (masalan, yangi `Snippet` ob'ekti yaratish uchun) qo'shish
      uchun tayyorlaydi. `Serializer` data argumentidagi ma'lumotlarni tekshiradi va **validatsiya** qiladi. Agar
      ma'lumotlar to'g'ri bo'lsa, keyin siz `serializer.is_valid()` va `serializer.save()` metodlarini chaqirib, yangi *
      *ob'ektni** yaratishingiz mumkin.
    - Umuman olganda, bu **sintaksis** yordamida siz `SnippetSerializer` orqali yangi ma'lumotlarni tayyorlashingiz va
      ularni ishlatishga tayyorlashingiz mumkin.

`API` ning shakllar bilan ishlashga qanchalik o'xshashligini e'tiborga oling. `Serializer` imizdan foydalanadigan`views`
yozishni boshlaganda, o'xshashlik yanada aniqroq bo'ladi.

Biz `model` **instansiyalari** o'rniga `querysets` ni ham `serialization` qilamiz. Buni amalga oshirish uchun
`serializer` argumentlariga `many=True` bayrog'ini qo'shamiz.

```ini
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [{'id': 1, 'title': '', 'code': 'foo = "bar"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
```

### 3. `serializer = SnippetSerializer(data=data, many=True)` ushbu sintaksis nima uchun ishlatilinadi?

**Tushuntirish:**

- `data=data` argumenti orqali foydalanuvchi tomonidan yuborilgan yangi ma'lumotlar ro'yxati beriladi. Bu ma'lumotlar
  odatda `JSON` formatida bo'ladi.
- `many=True` parametri, **serializerga** bir nechta **ob'ektlar** bilan ishlash kerakligini bildiradi. Bu foydalanuvchi
  bir vaqtda bir nechta `Snippet` ob'ektlarini yaratmoqchi bo'lganda qulay.

**Misol:**

Foydalanuvchi ma'lumotlarni `list` ko'rinishida yuborsa. Masalan, quyidagi `JSON` formatida:

```json
[
  {
    "title": "Snippet 1",
    "code": "print('Hello World')"
  },
  {
    "title": "Snippet 2",
    "code": "print('Hello Again')"
  }
]
```

> **Foydalanuvchi** tomonidan bir nechta ma'lumotlar ro'yxat (`list`) shaklida yuborilganida, siz buni
`Django REST Framework` yordamida bir nechta **ob'ektlarni** hosil qilish uchun ishlatishingiz mumkin. Buning uchun
`many=True` parametrini **serializerda** belgilashingiz kerak.

1. **Serializerni yaratish:**
   Serializerda `many=True` parametrini qo'shishingiz kerak:
    ```python
    serializer = SnippetSerializer(data=data, many=True)
    ```
2. **Validatsiya va saqlash:**

   Serializerni validatsiya qilish va ob'ektlarni saqlash jarayoni:
    ```python
    if serializer.is_valid():
        serializer.save()  # Bu yerda bir nechta ob'ektlar yaratiladi
    ```

**Natijasi:**
> Agar ma'lumotlar to'g'ri bo'lsa, yuqoridagi jarayon orqali siz bir nechta `Snippet` **ob'ektlarini** yaratishingiz
> mumkin. `Serializer` avtomatik ravishda har bir **ob'ektni** alohida saqlaydi. Shunday qilib, **foydalanuvchi**
> tomonidan
> yuborilgan bir nechta ma'lumotlarni olib, bir nechta **ob'ekt** hosil qilish mumkin.

### 4. `serializer = SnippetSerializer(data=data, many=True)` va

`serializer = SnippetSerializer(Snippet.objects.all(), many=True)` nimasi bilan farq qiladi to'liq tushuntiring

1. **Ma'lumot manbai:**

- `data=data, many=True`:
    - Bu sintaksisda `data` argumenti orqali foydalanuvchidan kelayotgan yangi ma'lumotlar ro'yxati (masalan, `JSON`
      formatida) beriladi.
    - `many=True` parametri, bu yerda ko'plab yangi **ob'ektlar** yaratish kerakligini bildiradi. Ushbu ma'lumotlar *
      *validatsiya** qilinadi va yangi **ob'ektlar** hosil qilish uchun ishlatiladi.

- `Snippet.objects.all(), many=True`:
    - Bu sintaksisda `Snippet.objects.all()` orqali ma'lumotlar bazasidagi mavjud `Snippet` **ob'ektlari** olinadi.
    - `many=True` parametri bu holatda, mavjud **ob'ektlarni serializatsiya** qilish kerakligini bildiradi. Bu yerda
      ma'lumotlar o'zgartirilmaydi, faqat mavjud **ob'ektlar** ko'rsatiladi.

2. **Vazifa:**

- `data=data, many=True`:
    - Bu kod yangi **ob'ektlar** yaratish uchun mo'ljallangan. Foydalanuvchi tomonidan yuborilgan ma'lumotlar asosida
      yangi `Snippet` ob'ektlari hosil qilinadi.
    - `Serializer` `is_valid()` chaqirilganda, ma'lumotlarni tekshiradi va agar to'g'ri bo'lsa, `save()` metodi orqali
      yangi **ob'ektlarni** yaratadi.

- `Snippet.objects.all(), many=True`:

- Bu kod mavjud **ob'ektlarni** olish va ularni `JSON` formatida ko'rsatish (**serializatsiya qilish**) uchun
  mo'ljallangan.
    - Bu kod mavjud **ob'ektlarni** olish va ularni `JSON` formatida ko'rsatish (**serializatsiya qilish**) uchun
      mo'ljallangan.
    - `Serializer` `data` sifatida mavjud ob'ektlarni qaytaradi, bu esa `API` orqali foydalanuvchilarga ko'rsatish uchun
      qulay.

3. **Natija:**

- `data=data, many=True`:
    - Ushbu kod bajarilganda, foydalanuvchi tomonidan yuborilgan ma'lumotlar asosida yangi **ob'ektlar** yaratiladi
- `Snippet.objects.all(), many=True`:
    - Ushbu kod bajarilganda, ma'lumotlar bazasidagi barcha `Snippet` **ob'ektlari** olish va ularni ko'rsatish uchun
      tayyorlanadi.

**Xulosa:**
> Umuman olganda, birinchi sintaksis yangi ob'ektlarni yaratish uchun ishlatiladi, ikkinchisi esa mavjud ob'ektlarni
> olish va ko'rsatish uchun ishlatiladi. Ikkisi bir xil serializerni ishlatgan bo'lsada, ma'lumot manbai va vazifalari
> farq qiladi.

### 5. **`JSONRenderer().render()` va `JSONParser().parse()` nima uchun kerak**

`JSONRenderer().render()`:

> `Python` obyektlarini `JSON` formatidagi byte stringga aylantiradi.

**Misol:**

   ```python
   from rest_framework.renderers import JSONRenderer

data = {'title': 'Example', 'code': 'print("hello")'}
json_data = JSONRenderer().render(data)
# Natija: b'{"title":"Example","code":"print(\\"hello\\")"}'
   ```

`JSONParser().parse()`:

> `JSON` formatidagi ma'lumotni `Python` obyektiga aylantiradi.

```python
from rest_framework.parsers import JSONParser
from io import BytesIO

json_string = '{"title":"New","code":"x=5"}'
stream = BytesIO(json_string.encode('utf-8'))
parsed_data = JSONParser().parse(stream)
# Natija: {'title': 'New', 'code': 'x=5'}
```

### 6. `ModelSerializers` dan foydalanish.

Bizning `SnippetSerializer` klassimiz `Snippet` `modelida` mavjud bo'lgan ko'p ma'lumotlarni takrorlamoqda.

`Django` qanday qilib `Form` klasslari va `ModelForm` klasslarini taqdim etsa, `REST framework` ham `Serializer`
klasslari va `ModelSerializer` klasslarini o'z ichiga oladi.

Keling, `ModelSerializer` klassidan foydalanib, **serializerimizni** qayta tuzishni ko'rib chiqaylik.
`snippet/serializers.py` faylini yana oching va `SnippetSerializer` klassini quyidagi bilan almashtiring.

```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

**Serializerlarning** bir yoqimli xususiyati shundaki, siz `serializer` instansiyasidagi barcha maydonlarni uning
ko'rinishini chop etish (`print` qilish) orqali tekshirishingiz mumkin. `Django shell`-ni `python manage.py shell`
buyrug'i orqali oching va quyidagilarni sinab ko'ring:

```ini
from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```    

> Esda tutish kerakki, `ModelSerializer` klasslari hech qanday ajoyib ish bajarmaydi, ular shunchaki `serializer`
> klasslarini yaratishning qisqa yo‘lidir:

- Avtomatik aniqlanadigan maydonlar to‘plami.
- `create()` va `update()` metodlari uchun oddiy standart amallar.

### 7. Keling, yangi `Serializer` klasimiz yordamida `API view`-larini qanday yozishimiz mumkinligini ko'ramiz. Hozircha

`REST framework`**-ning boshqa imkoniyatlaridan foydalanmaymiz**, shunchaki oddiy `Django view`-larini yozamiz.

**`snippet/views.py` fayliga quyidagi kodni qo'shamiz:**

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

`API`-mizning asosiy manzili barcha **snippetlarni** ko'rsatish va yangi `snippet` **qo'shish** imkonini beruvchi `view`
bo'ladi

```python
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```

Diqqat qiling, `CSRF` tokenisiz so'rov yuboradigan mijozlar ham ushbu `view`-ga `POST` so'rov yuborishi uchun, `view`-ni
`csrf_exempt` bilan belgilashimiz kerak. Bu odatda foydalanish tavsiya etilmaydigan usuldir, aslida`REST framework view`
-lari bunday emas, balki ancha mantiqiyroq ishlaydi. Lekin hozircha bizning maqsadlarimiz uchun bu yetarli.

`@csrf_exempt`:

- Bu dekorator `CSRF` **himoyasini o'chirib qo'yadi** (ya'ni, shu `view`-ga **tokenisiz** `POST` so'rovlarni qabul
  qilishga ruxsat beradi).
- **Misol:** Agar brauzerdan emas, balki **mobil ilova** yoki boshqa serverdan `API`-ga so'rov yuborilsa, `CSRF`tokensiz
  ishlashi uchun kerak.

**`Snippets/urls.py` faylini yarating:**

```python
from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]
```

Bundan tashqari, parcha ilovamizning `URL` manzillarini kiritish uchun `tutorial/urls.py` faylidagi `root` `urlconf`-ni
ulashimiz kerak.

```python
from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
]
```

> Shuni ta'kidlash joizki, Hozircha dasturimiz ba'zi maxsus holatlarni to'liq qayta ishlay olmaydi. Agar noto'g'ri
> formatdagi json yuborilsa yoki view tomonidan qo'llab-quvvatlanmaydigan metod bilan so'rov yuborilsa, server 500
> xatosi
> bilan javob qaytaradi. Biroq, hozircha bu bizning ehtiyojlarimiz uchun yetarli.

### 8. `API` `view`-larini o‘rab olish

> `REST framework API` ko'rinishlarini yozish uchun ikkita o'rash moslamasini taqdim etadi:

1. **Funksiyaga** asoslangan ko'rinishlar (`views`) uchun `@api_view` dekoratori.
2. Klassga asoslangan ko'rinishlar uchun `APIView` klassi.

**Tushuntirishlar:**

1. `@api_view` **dekoratori** - Funksiyalarni `API` endpointiga aylantirish uchun ishlatiladi. Misol:
    ```python
    from rest_framework.decorators import api_view
    
    @api_view(['GET', 'POST'])  # Ruxsat berilgan HTTP metodlari
    def my_function_view(request):
        # API logikasi
        return Response(...)
    ```
2. `APIView` **Klassi** - `Class-based views` (`CBV`) uchun asosiy klass. Misol:
    ```python
    from rest_framework.views import APIView
    
    class MyClassView(APIView):
        def get(self, request):
            # GET so'rovi uchun logika
            return Response(...)
        
        def post(self, request):
            # POST so'rovi uchun logika
            return Response(...)
    ```

**Afzalliklar:**

- `@api_view`: Oddiy funksiyalarni tezda `API` endpointiga aylantirish
- `APIView`: Murakkab logikalar uchun moslashuvchan klass struktura

> Bu ikkala usul ham `REST` frameworkda `API` yaratishning standart usullaridir.

### 9. `URL` manzillarimizga ixtiyoriy `format` qo'shimchalarini qo'shish.

1. **Nima uchun `format` qo'shimchalari kerak?**

- `API` ga so'rov yuborayotganda, ma'lumot qanday formatda (`JSON`, `XML`) qaytarilishini ko'rsatish uchun
- Masalan: `.json` qo'shsangiz - `JSON` formatida, `.xml` qo'shsangiz - `XML` formatida javob olasiz

2. **Qanday ishlaydi?**

    ```python
    # urls.py
    from django.urls import path
    from .views import article_list
    
    urlpatterns = [
        path('articles/', article_list),          # Oddiy URL
        path('articles.<format>/', article_list), # Format qo'shimchasi bilan
    ]
    ```

3. **`View` da qo'llash:**
    ```python
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    @api_view(['GET'])
    def article_list(request, format=None):
        articles = Article.objects.all()
        if format == 'json' or format is None:
            return Response({'articles': articles})  # JSON formatida
        elif format == 'xml':
            return Response(xml_serializer(articles))  # XML formatida
    ```

4. **Amaliy misollar**

- `GET /api/articles/` - standart javob (odatda `JSON`)
- `GET /api/articles.json` - aniq `JSON` so'rash
- `GET /api/articles.xml` - `XML` formatida so'rash

5. **Afzalliklari:**

- Bir xil `API` dan turli formatlarda ma'lumot olish mumkin
- `Frontend` dasturchilar o'zlari uchun qulay formatni tanlay oladi
- `Test` qilish osonlashadi

> Bu xususiyat ayniqsa turli tizimlar bilan **integratsiya** qilishda qo'l keladi.

### 10. `API`-ni klass asosidagi ko'rinishlar (`views`) yordamida qayta yozish haqida batafsil tushuntiring.

1. **Asosiy Tushuncha**
   > `Class-Base-Views` (`CBV`) - bu `Django` va `DRF` (**Django REST Framework**) da `API` yaratishning tizimli usuli
   bo'lib, har bir `HTTP` metodiga (`GET`, `POST`, `PUT`, `DELETE`) alohida klass metodlari bilan javob beradi.

2. **Oddiy `APIView` Misoli:**
    ```python
    from rest_framework.views import APIView
    from rest_framework.response import Response
    
    class ArticleAPIView(APIView):
        def get(self, request):
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
    
        def post(self, request):
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    ```
3. **`GenericAPIView` afzalliklari**

   `DRF` quyidagi `generic` **viewlarni** taklif etadi:
    - `ListAPIView` - faqat ro'yxat ko'rish
    - `CreateAPIView` - faqat yaratish
    - `RetrieveAPIView` - bitta obyektni ko'rish
    - `UpdateAPIView` - yangilash
    - `DestroyAPIView` - o'chirish
4. **ViewSetlar**

   Kodni yanada soddalashtirish uchun:

    ```python
    from rest_framework import viewsets
    
    class ArticleViewSet(viewsets.ModelViewSet):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

5. **Router bilan Bog'lash**

    ```python
    from rest_framework.routers import DefaultRouter
    
    router = DefaultRouter()
    router.register(r'articles', ArticleViewSet)
    urlpatterns = router.urls
    ```

6. **Asosiy Afzalliklar:**

- **Kodni qayta ishlatish** - Bir nechta `API` lar uchun umumiy logika
- **Meros** - Asosiy klasslardan xususiyatlarni **meros** olish
- **Tashkilot** - Har bir metod alohida va aniq
- **DRF imkoniyatlari** - `Pagination`, `filterlar`, `permissionlar` bilan oson **integratsiya**

7. **Funksiyaga nisbatan farqlar**

   | Xususiyat        | Funksiya Ko'rinishi       | Klass Ko'rinishi      |
                                                |------------------|---------------------------|-----------------------|
   | HTTP metodlari   | @api_view dekoratori      | Alohida metodlar      |
   | Kod tashkiloti   | Har bir URL uchun alohida | Meros asosida         |
   | Murakkablik      | Oddiy loyihalar uchun     | Katta loyihalar uchun |
   | Moslashuvchanlik | Cheklangan                | Keng imkoniyatlar     |

8. **Amaliy Maslahatlar**
    - **Kichik API lar uchun `APIView` dan boshlang**
    - **Standart CRUD amallari uchun `GenericAPIView` yoki `ViewSet` dan foydalaning**
    - **Murakkab logikalar uchun metodlarni alohida yozing**
    - **`get_queryset()` va `get_serializer_class()` metodlaridan foydalaning**

> Class asosidagi ko'rinishlar dasturingizni yanada tizimli va **professional** qiladi, ayniqsa katta miqyosdagi
> loyihalarda.

### 11. **`APIView` nima uchun kerak?**

1. **`HTTP` metodlarini aniq boshqarish**
    - Har bir `HTTP` soʻrov turi (`GET`, `POST`, `PUT`, `DELETE`) uchun alohida metod yozish mumkin.
    - Misol:
      ```python
      from rest_framework.views import APIView
      from rest_framework.response import Response
      
      class ArticleAPIView(APIView):
          def get(self, request):
              articles = Article.objects.all()
              return Response({"articles": articles})
      
          def post(self, request):
              # Ma'lumot yaratish
              return Response({"message": "Yangi maqola yaratildi"})
       ```
2. **`Request` va `Response` ni avtomatik tahlil qilish**
    - `request.data` – `JSON`, `FormData` kabi turli formatdagi maʼlumotlarni avtomatik qabul qiladi.
    - `Response()` – `DRF` tomonidan taqdim etilgan yaxshilangan javob obyekti (`content negotiation`, `status` kodlari
      bilan ishlash qulay).

3. **`authentication` va `permissionlarni` oson qoʻllash**

- `APIView` `permission_classes` va `authentication_classes` orqali kirish huquqini boshqarish imkonini beradi:

    ```python
    from rest_framework.permissions import IsAuthenticated
    
    class PrivateAPIView(APIView):
        permission_classes = [IsAuthenticated]  # Faqat avtorizatsiyadan o'tgan foydalanuvchilar uchun
    ```

4. **`DRF` ning boshqa imkoniyatlaridan foydalanish**

- **Throttling** (soʻrovlar tezligini cheklash)
- **Pagination** (sahifalash)
- **Versioning** (API versiyalari)
- Renderer/Parser **(JSON, XML formatlari bilan ishlash)**

**`APIView` vs `Django` ning oddiy view klassi**

| Xususiyat           | Django `View`                   | DRF `APIView`                                  |
|---------------------|---------------------------------|------------------------------------------------|
| **HTTP metodlari**  | `self.request.method` orqali    | `get()`, `post()`, `put()`, `delete()`         |
| **Request parsing** | `request.POST`, `request.GET`   | `request.data` (`JSON`, `FormData`, `XML`)     |
| **Response**        | `HttpResponse`, `JsonResponse`	 | `Response()` (avtomatik formatlash)            |
| **Authentication**  | **Qoʻlda yozish kerak**         | `permission_classes`, `authentication_classes` |
| **Pagination**      | **Qoʻlda amalga oshirish**      | `pagination_class` bilan oson                  |

> Qachon `APIView` Ishlatiladi?

1. **Oddiy `CRUD API` yaratishda (`GET`, `POST`, `PUT`, `DELETE`)**
2. **Custom (maxsus) API logikasi kerak boʻlganda**
3. **`DRF` ning boshqa imkoniyatlaridan (auth, pagination) foydalanish zarur boʻlganda**
4. **Klass asosida koʻproq tashkil etilgan kod yozish zarur boʻlganda**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer


class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

**Xulosa**

`APIView` `Django REST Framework` ning asosiy qismi boʻlib, `RESTful API` larni tez va tizimli yaratishga yordam beradi.
Agar siz:

- Aniq `HTTP` metodlari bilan ishlashni xohlasangiz,
- `DRF` ning `request/response` imkoniyatlaridan foydalanmoqchi boʻlsangiz,
- `Authentication`, `pagination` kabi funksiyalarni qoʻshmoqchi boʻlsangiz,
  `APIView` siz uchun eng yaxshi tanlov!

### 12. `APIView` bir nechta methodalrni ya'ni `GET`, `POST`, `UPDATE`, `PATCH` va `DELETE` method larini bir

`class` da yozishga yordam beradimi?

> Ha, `APIView` bir klassda `GET`, `POST`, `PUT/PATCH`, `DELETE` kabi barcha `HTTP` metodlarini birlashtirishga imkon
> beradi!

`APIView` bilan `CRUD` (`Create`, `Read`, `Update`, `Delete`) amallarini bitta klassda qo'llash:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer


class ArticleAPIView(APIView):
    """Bitta klassda barcha HTTP metodlari"""

    # 1. GET - Barcha maqolalarni olish
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # 2. POST - Yangi maqola yaratish
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # 201 Created
        return Response(serializer.errors, status=400)  # 400 Bad Request

    # 3. PUT - To'liq yangilash (barcha maydonlar talab qilinadi)
    def put(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 4. PATCH - Qisman yangilash (faqat berilgan maydonlar yangilanadi)
    def patch(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 5. DELETE - Maqolani o'chirish
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=204)  # 204 No Content
```

**`URL` sozlamalari (`urls.py`):**

```python
from django.urls import path
from .views import ArticleAPIView

urlpatterns = [
    path('articles/', ArticleAPIView.as_view()),  # GET/POST
    path('articles/<int:pk>/', ArticleAPIView.as_view()),  # PUT/PATCH/DELETE
]
```

**`APIView` metodlarining ishlashi:**

| HTTP Metod | URL            | Vazifa                         |
|------------|----------------|--------------------------------|
| `GET`      | `	/articles/`  | Barcha maqolalarni olish       |
| `POST`     | `	/articles/`  | Yangi maqola yaratish          |
| `PUT`      | `/articles/1/` | ID=1 maqolani to'liq yangilash |
| `PATCH`    | `/articles/1/` | ID=1 maqolani qisman yangilash |
| `DELETE`   | `/articles/1/` | ID=1 maqolani o'chirish        |

**Afzalliklari:**

1. **Barcha metodlar bir joyda** - Kodni tashkil qilish oson
2. **Har bir metod alohida** - Har bir `HTTP` so'rov turi uchun aniq funksiya
3. **Moslashuvchanlik** - Har bir metodni mustaqil o'zgartirish mumkin
4. **`DRF` imkoniyatlari** - `request.data`, `Response()`, `authentication` va boshqalardan foydalanish

> Agar sizga `CRUD` (**Yaratish**, **O'qish**, **Yangilash**, **O'chirish**) operatsiyalarini bitta klassda boshqarish
> kerak bo'lsa, `APIView` aynan sizga kerak bo'lgan yechimdir!

### 13. `APIView`  ichida maxsus method yozsa bo'ladimi

> `DRF` (`Django REST Framework`) ning `APIView` klassi faqat standart `HTTP` metodlari (`get`, `post`, `put`, `patch`,
`delete`) bilan cheklanmaydi. Siz o‘zingizga kerakli bo‘lgan har qanday maxsus metodlarni qo‘shishingiz mumkin.

1. **Maxsus Metod Qqo‘shish misoli**

   > Aytaylik, siz `/articles/<id>/publish/` manziliga `POST` so‘rov yuborib, maqolani **"nashr qilish"** (`publish`) *
   *funksiyasini** yaratmoqchisiz:

   ```python
      from rest_framework.views import APIView
      from rest_framework.response import Response
      from rest_framework import status
      from .models import Article
      
      class ArticleAPIView(APIView):
          # ... avvalgi GET, POST, PUT metodlari ...
      
          # MAXSUS METOD: Maqolani nashr qilish
          def publish(self, request, pk):
              article = Article.objects.get(pk=pk)
              article.is_published = True
                article.save()
              return Response(
                  {"message": "Maqola nashr qilindi!"},
                   status=status.HTTP_200_OK
              )
   ```
   **`URL` sozlamalari (`urls.py`):**
    ```python
    from django.urls import path
    from .views import ArticleAPIView
    
    urlpatterns = [
        path('articles/<int:pk>/publish/', ArticleAPIView.as_view({'post': 'publish'})),
    ]
    ```

   👉 **Eslatma:**

    - `as_view()` ichida metodni `HTTP` bilan bog‘lash kerak (masalan, `{'post': 'publish'}`).
    - Bu yerda `POST` `/articles/1/publish/` so‘rovi `publish()` metodini chaqiradi.

2. **Boshqa Misol: `Custom` `GET` Metodi**

   Aytaylik, siz faqat `active` maqolalarni qaytaruvchi maxsus `GET` `metod` yaratmoqchisiz:

   `Viewda`:

    ```python
     class ArticleAPIView(APIView):
         # Oddiy GET (barcha maqolalar)
         def get(self, request):
             articles = Article.objects.all()
             # ...
     
         # MAXSUS GET: Faqat active maqolalar
         def get_active(self, request):
             active_articles = Article.objects.filter(is_active=True)
             serializer = ArticleSerializer(active_articles, many=True)
             return Response(serializer.data)
    ```
   **`URL` da:**

    ```python
    urlpatterns = [
        path('articles/active/', ArticleAPIView.as_view({'get': 'get_active'})),
    ]
    ```    
   Endi `GET` `/articles/active/` so‘rovi faqat **aktiv** maqolalarni qaytaradi.

3. **Metodga `Permission` (**Ruxsat**) qo‘shish**
   Agar maxsus metod faqat adminlar uchun bo‘lishi kerak bo‘lsa:
    ```python
    from rest_framework.permissions import IsAdminUser
    
    class ArticleAPIView(APIView):
        permission_classes = [IsAdminUser]  # Faqat adminlar kirishi mumkin
    
        def special_admin_action(self, request):
            return Response("Bu faqat adminlar uchun!")
    ```

4. **Foydali Maslahatlar**

    - **Nom berish:** Metod nomi aniq bo‘lishi kerak (`send_email`, `calculate_stats`).
    - `HTTP` metodni to‘g‘ri tanlash:
        - `GET` - Ma‘lumot olish
        - `POST` - Yangi amal bajaring (masalan, publish, activate)
        - `PUT/PATCH` - Yangilash
    - `URL` mantiqiy bo‘lsin:
        - `/articles/<pk>/publish/` (`POST`)
        - `/articles/active/` (`GET`)

**Xulosa**

- `APIView` ichida istalgan maxsus metodlarni yozish mumkin.
- Uni `urls.py` da `as_view({'http_method': 'custom_method'})` ko‘rinishida bog‘lash kerak.
- Metodga `permission`, `authentication`, `throttling` qo‘llash mumkin.
  Bu usul `Django REST Framework` da moslashuvchan va kuchli `API` yaratish imkonini beradi!

### 14.  `GenericAPIView` yoki `ViewSet` dan **qachon** va **qanday**  foydalanish ni batafsil tushuntiring.

1. `GenericAPIView` - Standart `CRUD` operatsiyalari uchun
   **Qachon ishlatiladi?**
    - Agar sizga `oddiy CRUD` (`Create`, `Read`, `Update`, `Delete`) operatsiyalari kerak bo‘lsa.
    - Har bir **alohida URL** uchun alohida view yozish zarur bo‘lsa.
    - `API` logikasi **moslashuvchan** bo‘lishi kerak (masalan, `filter`, `pagination`, `permissions`).

   **Misol: `GenericAPIView` bilan `CRUD`**

    ```python
    from rest_framework.generics import (
        ListCreateAPIView,  # GET (list) + POST (create)
        RetrieveUpdateDestroyAPIView,  # GET (one) + PUT/PATCH + DELETE
    )
    from .models import Article
    from .serializers import ArticleSerializer
    
    # 1. Ro'yxat ko'rish + yangi yaratish
    class ArticleListCreateView(ListCreateAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    
    # 2. Bitta maqolani ko'rsatish/yangilash/o'chirish
    class ArticleDetailView(RetrieveUpdateDestroyAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

   **`URL` Sozlamalari**

    ```python
    from django.urls import path
    from .views import ArticleListCreateView, ArticleDetailView
    
    urlpatterns = [
        path('articles/', ArticleListCreateView.as_view()),  # GET/POST
        path('articles/<int:pk>/', ArticleDetailView.as_view()),  # GET/PUT/PATCH/DELETE
    ]
    ```
   **Afzalliklari:**

    - Kodni qisqartirish (`DRF` tayyor `generic` `view` lar).
    - Har bir operatsiya uchun alohida klass.
    - `Pagination`, `filter`, `permission` larni oson qo‘llash.

   **Kamchiliklari:**

    - Har bir yangi funksiya uchun alohida view yozish kerak.
    - Agar API juda murakkab bo‘lsa, ko‘p klasslar paydo bo‘lishi mumkin.

___

2. `ViewSet` - **Bir klassda Barcha operatsiyalar**

   **Qachon ishlatiladi?**

    - Agar siz **bir klassda barcha CRUD operatsiyalarini** birlashtirmoqchi bo‘lsangiz.
    - `Router` yordamida `URL`-larni avtomatik yaratish kerak bo‘lsa.
    - **Admin panelga o‘xshash** tez ishlab chiqish zarur bo‘lsa (masalan, `Django` `Admin`).

   **Misol: `ModelViewSet` (Eng Kuchli Variant)**

    ```python
    from rest_framework.viewsets import ModelViewSet
    from .models import Article
    from .serializers import ArticleSerializer
    
    class ArticleViewSet(ModelViewSet):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

   **Router bilan `URL` avtomatik yaratish**
    ```python
    from rest_framework.routers import DefaultRouter
    from .views import ArticleViewSet
    
    router = DefaultRouter()
    router.register(r'articles', ArticleViewSet)  # Avtomatik URL yaratadi
    
    urlpatterns = router.urls
    ```
   👉 **`URL`-lar avtomatik yaratiladi:**

    - `GET /articles/` → Ro'yxat
    - `POST /articles/` → Yangi yaratish
    - `GET /articles/1/` → Bitta maqola
    - `PUT /articles/1/` → To‘liq yangilash
    - `DELETE /articles/1/` → O‘chirish


3. **Qaysi birini tanlash kerak?**

| **Xususiyat**          | `GenericAPIView`                        | `ViewSet`                                |
|------------------------|-----------------------------------------|------------------------------------------|
| `CRUD` Operatsiyalari  | Har biri alohida klass                  | Bitta klassda barchasi                   |
| `URL` Sozlamalari      | Qo‘lda yoziladi                         | `Router` avtomatik yaratadi                |
| Moslashuvchanlik       | Yuqori (har bir metodni sozlash mumkin) | Cheklangan (faqat `DRF` metodlari)         |
| Ishlab Chiqish Tezligi | Sekinroq (ko‘p kod)                     | Tez (bir klass + `router`)                 |
| Murakkab Logika        | Yaxshi (custom metodlar qo‘shish oson)  | Qiyin (metodlarni `override` qilish kerak) |

4. **Qo‘shimcha maslahatlar**

1. **Agar oddiy CRUD kerak bo‘lsa** → `ModelViewSet` ishlating.
2. **Agar maxsus operatsiyalar kerak bo‘lsa** → `GenericAPIView` yoki `APIView`.
3. **Agar API juda murakkab bo‘lsa** → `ViewSet` ni `@action` bilan kengaytiring.

**Misol: `ViewSet` + Maxsus Amal (`@action`)**

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # MAXSUS AMAL: /articles/<pk>/publish/
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.is_published = True
        article.save()
        return Response({'status': 'published'})
```
👉 `URL`: `POST` `/articles/1/publish/`

**Xulosa:**

- `GenericAPIView` → Har bir operatsiya uchun alohida klass (moslashuvchan, lekin ko‘p kod).
- `ViewSet` → Bir klassda barchasi (tez ishlab chiqish, lekin cheklangan sozlash).
- `@action` → ViewSet ga maxsus metod qo‘shish.

> Agar loyiha oddiy `CRUD` dan iborat bo‘lsa, `ViewSet` + `Router` eng yaxshi tanlov. Agar murakkab biznes logika kerak bo‘lsa, `GenericAPIView` yoki oddiy `APIView` ishlating!

### 15. `Django REST Framework` (`DRF`)  dagi `rest_framework.generics` ichidagi `Generic View` lar

> `DRF` `GenericAPIView` asosida yaratilgan bir qator tayyor klasslarni taklif etadi. Ular tez `CRUD` (`Create`, `Read`, `Update`, `Delete`) `API` yaratish uchun moʻljallangan. Quyida barchasi haqida tushuntiraman:

1. Roʻyxat Koʻrish va Yaratish (`List` + `Create`)

    `ListCreateAPIView`

   - `GET`: Barcha obyektlarni koʻrsatish
   - `POST`: Yangi obyekt yaratish

        ```python
        from rest_framework.generics import ListCreateAPIView
        
        class ArticleListCreateView(ListCreateAPIView):
            queryset = Article.objects.all()
            serializer_class = ArticleSerializer
        ```
   `URL`: `GET /articles/`, `POST /articles/`

2. **Bitta Obyektni Koʻrish/Yangilash/Oʻchirish**

    `RetrieveUpdateDestroyAPIView`
    - `GET`: Bitta obyektni koʻrsatish
    - `PUT/PATCH`: Yangilash
    - `DELETE`: Oʻchirish
   
      ```python
      from rest_framework.generics import RetrieveUpdateDestroyAPIView
      
      class ArticleDetailView(RetrieveUpdateDestroyAPIView):
          queryset = Article.objects.all()
          serializer_class = ArticleSerializer
      ```
    **URL**: `GET /articles/1/`, `PUT /articles/1/`, `DELETE /articles/1/`

3. **Faqat Roʻyxat Koʻrish (`List`)**

    `ListAPIView`
    
    - Faqat `GET` soʻrovi (obyektlar roʻyxati)
   
      ```python
      from rest_framework.generics import ListAPIView
      
      class ArticleListView(ListAPIView):
          queryset = Article.objects.all()
          serializer_class = ArticleSerializer
      ```
    `URL: GET /articles/`

4. **Faqat Yaratish (`Create`)**
    `CreateAPIView`
    - Faqat `POST` soʻrovi (yangi obyekt yaratish)

      ```python
      from rest_framework.generics import CreateAPIView
      
      class ArticleCreateView(CreateAPIView):
          queryset = Article.objects.all()
          serializer_class = ArticleSerializer
      ```
    `URL: POST /articles/`

5. **Faqat Oʻchirish (`Destroy`)**

    `DestroyAPIView`
    - Faqat `DELETE` soʻrovi (obyektni oʻchirish)
      ```python
      from rest_framework.generics import DestroyAPIView
      
      class ArticleDeleteView(DestroyAPIView):
          queryset = Article.objects.all()
          serializer_class = ArticleSerializer
      ```
    `URL: DELETE /articles/1/`

6. **Bitta Obyektni Koʻrish (`Retrieve`)**

    `RetrieveAPIView`

    - Faqat `GET` (bitta obyektni koʻrsatish)
   
      ```python  
      from rest_framework.generics import RetrieveAPIView
      
      class ArticleDetailView(RetrieveAPIView):
          queryset = Article.objects.all()
          serializer_class = ArticleSerializer
      ```    
    `URL: GET /articles/1/`

**Qoʻshma `Generic View` lar**

1. `RetrieveUpdateAPIView` - **Koʻrish** + **Yangilash**

    Bitta obyektni koʻrsatish (`GET`) va yangilash (`PUT/PATCH`)

    ```python
    from rest_framework.generics import RetrieveUpdateAPIView
    
    class ArticleRetrieveUpdateView(RetrieveUpdateAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

    **Ishlatilishi:**

    - `GET /articles/1/` - Maqolani koʻrish
    - `PUT /articles/1/` - Toʻliq yangilash
    - `PATCH /articles/1/` - Qisman yangilash
   
2. `RetrieveDestroyAPIView` - **Koʻrish** + **Oʻchirish**

    Bitta obyektni koʻrsatish (`GET`) va oʻchirish (`DELETE`)

    ```python
    from rest_framework.generics import RetrieveDestroyAPIView
    
    class ArticleRetrieveDeleteView(RetrieveDestroyAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

    **Ishlatilishi:**

    - `GET /articles/1/` - Maqolani koʻrish
    - `DELETE /articles/1/` - Maqolani oʻchirish

3. `RetrieveUpdateDestroyAPIView` - **Koʻrish** + **Yangilash** + **Oʻchirish**

    Bitta obyekt uchun barcha asosiy operatsiyalar (`GET`, `PUT`, `PATCH`, `DELETE`)

    ```python
    from rest_framework.generics import RetrieveUpdateDestroyAPIView
    
    class ArticleDetailView(RetrieveUpdateDestroyAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```

    **Ishlatilishi:**

   - `GET /articles/1/` - Koʻrish
   - `PUT /articles/1/` - Yangilash
   - `PATCH /articles/1/` - Qisman yangilash
   - `DELETE /articles/1/` - Oʻchirish

4. `ListCreateAPIView` - **Roʻyxat** + **Yaratish**

    Roʻyxat koʻrish (`GET`) va yangi yaratish (`POST`)

    ```python
    from rest_framework.generics import ListCreateAPIView
    
    class ArticleListCreateView(ListCreateAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
    ```
    **Ishlatilishi:**
    - `GET /articles/` - Barcha maqolalar
    - `POST /articles/` - Yangi maqola yaratish
    
**Yangilash paytida qoʻshimcha logika yozish**

```python
class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_update(self, serializer):
        # Yangilash paytida qoʻshimcha logika
        serializer.save(updated_by=self.request.user)
```

**`URL` Sozlamalari**

```python
from django.urls import path
from .views import ArticleListCreateView, ArticleDetailView

urlpatterns = [
    path('articles/', ArticleListCreateView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
]
```

**Afzalliklari**
- **Kodni qisqartirish** - Har bir operatsiya uchun alohida metod yozish shart emas.
- **Standart DRF funksiyalari** - `Pagination`, `filter`, `permission` bilan ishlaydi.
- **Tez ishlab chiqish** - `CRUD` `API` ni bir necha qatorda yozish mumkin.

**Kamchiliklari**
 - **Murakkab logikalar uchun mos emas** - Agar sizga `get_queryset()` yoki `get_serializer()` ni qoʻlda sozlash kerak boʻlsa, oddiy `APIView` yaxshiroq variant.
 - **Har bir operatsiya uchun alohida klass** - Agar barcha `CRUD` kerak boʻlsa, `ViewSet` samaraliroq.

### 16. "`Generic View` lar ning kamchiliklari ya'ni Agar sizga `get_queryset()` yoki `get_serializer()` ni qoʻlda sozlash kerak boʻlsa" ushbu joyga tushunmadim.

1. Nima uchun `get_queryset()` va `get_serializer()` kerak?

    **`Generic` `view` lar odatda  quyidagilarni sozlaydi:**    

    ```python
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    ```

    **Lekin murakkab loyihalarda sizga quyidagilar kerak bo'lishi mumkin:**
    
    - Foydalanuvchiga tegishli ma'lumotlarni ko'rsatish
    - Vaqtinchalik filtrlar qo'llash
    - Turli sharoitlarda turli serializerlardan foydalanish

2. **Muammo nimada?**

    `Generic view` larda:

    ```python
    class ArticleListView(ListAPIView):
        queryset = Article.objects.all()  # Bu STATIK queryset
        serializer_class = ArticleSerializer  # Bu STATIK serializer
    ```

    Agar sizga **dinamik ravishda** quyidagilarni o'zgartirish kerak bo'lsa:
    - Foydalanuvchi `A` uchun queryset `A`
    - Foydalanuvchi `B` uchun queryset `B`
    - `GET` so'rovi uchun serializer `A`
    - `POST` so'rovi uchun serializer `B`

3. Yechim: `get_queryset()` va `get_serializer()` ni override qilish

    **a) `get_queryset()` misoli:**

    ```python
    class ArticleListView(ListAPIView):
        serializer_class = ArticleSerializer
        
        def get_queryset(self):
            # Faqat published maqolalarni ko'rsatish
            if self.request.user.is_staff:
                return Article.objects.all()  # Admin uchun hammasi
            return Article.objects.filter(is_published=True)  # Oddiy foydalanuvchi uchun
    ```    

    **b) `get_serializer()` misoli:**

    ```python
    class ArticleListView(ListAPIView):
        def get_serializer_class(self):
            if self.request.method == 'GET':
                return ArticleReadSerializer  # Faqat o'qish uchun
            return ArticleWriteSerializer  # Yozish/yangilash uchun
    ```

4. Nega bu `Generic View` lar uchun muammo?

   - **Qo'shimcha kod** - Agar sizga ko'p sozlash kerak bo'lsa, `Generic view` ning afzalligi yo'qoladi
   - **Murakkab holatlar** - Ba'zi `kompleks filtr` larni amalga oshirish qiyin
   - **O'qiluvchanlik** - **Ko'p `override` qilingan metodlar kodni chalkashtirib yuborishi mumkin**


5. **Qachon `Generic View` ishlatmaslik kerak?**

    **Agar sizda:**
    - **Juda ko'p shartli mantiq (`if-else` zanjirlari)**
    - **Bir nechta modellarga bir vaqtning o'zida murojaat**
    - **Noan'anaviy `API` endpointlari**

    > Bunday holatlarda oddiy `APIView` yoki `ViewSet` ishlatish yaxshiroq.


6. **Misollar bilan solishtirish**
    
    **`Generic View` (cheklangan moslashuvchanlik)**

    ```python
    class UserArticlesView(ListAPIView):
        queryset = Article.objects.all()  # STATIK
        serializer_class = ArticleSerializer  # STATIK
    ```

    **`APIView` (to'liq nazorat)**

    ```python
    class UserArticlesView(APIView):
        def get(self, request):
            articles = Article.objects.filter(owner=request.user)
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
    ```
    > **Xulosa:** Agar sizga ko'p sozlash kerak bo'lsa, `Generic` viewlarning soddaligi uning kamchiligiga aylanadi.


### 17. `Generic View` va `APIView` farqini tushunarli misollar bilan solishtiraylik

1. **MISOL: Foydalanuvchiga tegishli maqolalarni ko‘rsatish**

    **`GenericAPIView` yordamida (cheklangan moslashuvchanlik)**

    ```python
    from rest_framework.generics import ListAPIView
    
    class UserArticlesGenericView(ListAPIView):
        serializer_class = ArticleSerializer
        
        def get_queryset(self):
            # Faqat o'z maqolalarini ko'rish uchun qo'lda sozlash kerak
            return Article.objects.filter(author=self.request.user)
    ```
   **Kamchiligi:**

    > Agar sizga `request.user` ga qarab boshqa `filtr` qo‘shish kerak bo‘lsa, yana `get_queryset()` ni o‘zgartirish kerak. Bu `Generic View` ning asl maqsadi **(kodni qisqartirish) bilan ziddiyatli**.

    **APIView yordamida (to‘liq nazorat)**

    ```python
    from rest_framework.views import APIView
    from rest_framework.response import Response
    
    class UserArticlesAPIView(APIView):
        def get(self, request):
            articles = Article.objects.filter(
                author=request.user,
                is_published=True  # Qo'shimcha filter
            )
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
    ```    
    **Afzalligi:**
    - Har bir qadamni qo‘lda boshqarish mumkin.
    - Murakkab shartlarni osongina qo‘shish mumkin.


2. **MISOL: Turli `HTTP` metodlari uchun turli serializerlar**

    `GenericAPIView` yordamida (**murakkabroq**)

    ```python
    from rest_framework.generics import RetrieveUpdateAPIView
    
    class ArticleGenericView(RetrieveUpdateAPIView):
        queryset = Article.objects.all()
        
        def get_serializer_class(self):
            if self.request.method == 'GET':
                return ArticleDetailSerializer  # Ko'rish uchun batafsil serializer
            return ArticleUpdateSerializer  # Yangilash uchun maxsus serializer
    ```

    **Kamchiligi:**

    - `get_serializer_class()` ni override qilish kerak.
    - Agar ko‘p shartlar bo‘lsa, kod chalkashib ketadi.

    `APIView` yordamida (oddiyroq)

    ```python
    class ArticleAPIView(APIView):
        def get(self, request, pk):
            article = Article.objects.get(pk=pk)
            serializer = ArticleDetailSerializer(article)
            return Response(serializer.data)
        
        def put(self, request, pk):
            article = Article.objects.get(pk=pk)
            serializer = ArticleUpdateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    ```
   **Afzalligi:**

    - Har bir metod uchun alohida serializer tanlash oson.
    - Kod aniqroq va boshqarish oson.
    
   
### 18. Quyidagi code ichidagi `raise_exception=True` nima uchun kerka.

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Xato bo'lsa 400 qaytaradi
        serializer.save()  # Bazaga saqlaydi
        return Response(serializer.data, status=201)
```

**Tushuntirish:**

`raise_exception=True` `Django REST Framework (DRF)` serializersida muhim parametr bo‘lib, u validatsiya (ma'lumotlarni tekshirish) jarayonini soddalashtiradi va xatoliklarni avtomatik tarzda boshqarish imkonini beradi.

1. **`raise_exception=True` nima qiladi?**
   - Agar ma'lumotlar serializer qoidalariga mos kelmasa (ya'ni `is_valid()` `False` qaytarsa), `DRF` avtomatik ravishda `HTTP` `400 Bad Request` javobi bilan xatolikni qaytaradi.
   - Xatolik tafsilotlari `JSON` formatida ko'rinadi (masalan, qaysi maydon noto‘g‘ri yoki yetishmayotgani).

2. **Agar `raise_exception=True` bo'lmasa nima bo'ladi?**
   - Siz validatsiyani manual tekshirishingiz kerak:

   ```python
   if serializer.is_valid():
       serializer.save()
       return Response(serializer.data)
   else:
       return Response(serializer.errors, status=400)  # Xatoliklarni qo'lda qaytarish
   ```

   **"Manual tekshirish"** deganda, siz o'zingiz quyidagilarni amalga oshirasiz:

   - `Serializer` yoki `model` da belgilangan qoidalarga mosligini tekshirish.
   - Xatolik bo'lsa, qanday qaytarishni (`status` `code`, xabar formati) o'zingiz belgilaysiz.
   - Xatoliklarni qo'lda qayta ishlash (`logging`, `notification`, `custom format`).

   **`Manual` tekshirish:**

   ```python
   if serializer.is_valid():  # Xatoni o'zingiz tekshirasiz 
       serializer.save()
       return Response(serializer.data)
   else:
       # Xatoliklarni o'zingiz formatlab qaytarasiz
       return Response(
           {"success": False, "errors": serializer.errors},
           status=status.HTTP_422_UNPROCESSABLE_ENTITY
       )
   ```
   **`Manual` tekshirish qachon kerak?**
   - **Custom xato formati** talab qilinganda (`frontend` aynan shu strukturada kutgan bo'lsa).
   - **Xatolarni `log` qilish** (ma'lumotlar bazasiga yuborish, `Telegram` bildirishnoma yuborish).
   - **Maxsus `status` codelar** (masalan, `422`, `409` ishlatish).

    **Misollar:**
   - **a) Oddiy `manual` tekshirish** 
     ```python
     def post(self, request):
         serializer = PaymentSerializer(data=request.data)
         if not serializer.is_valid():  # Validatsiyani o'zimiz tekshiramiz
             log_errors(serializer.errors)  # Xatoliklarni log qilamiz
             return Response(
                 {"detail": "Validation failed", "errors": serializer.errors},
                 status=status.HTTP_400_BAD_REQUEST
             )
         serializer.save()
         return Response(serializer.data, status=201)
     ```
   - **b) `Field-level` validatsiya (qo'shimcha tekshirish)** 
        ```python
        class PaymentSerializer(serializers.ModelSerializer):
            def validate_amount(self, value):
                if value <= 0:
                    raise serializers.ValidationError("Amount must be positive!")
                return value
        
        # Viewda
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            # Bu yerda DRF avtomatik tarzda validate_amount dagi xatoni qo'shib qo'yadi
        ```
3. **Xulosa**

   - `raise_exception=True` - tezkor va oddiy yechim (90% loyihalar uchun yetarli).
   - **Manual tekshirish** - qo'shimcha kontrol talab qilinganda ishlatiladi (masalan, `startup` loyihalarda `custom error handling`).

> Agar sizga aniq talablar bo'lmasa, avtomatik tekshirish (`raise_exception=True`) ishlating — kod qisqa va xatosiz bo'ladi!


















































































































































































