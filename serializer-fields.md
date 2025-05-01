### 1. `DRF Serializer Field` parametrlari haqida to'liq ma'lumot.

> `Django REST Framework` (`DRF`) Serializerlarda fieldlar uchun ko'plab parametrlar mavjud. Bu parametrlar fieldlarning xatti-harakatini, validatsiyasini va ko'rinishini nazorat qilish imkonini beradi.

**Asosiy Field Parametrlari**

1. **Umumiy parametrlar**
    - `read_only` (**bool**) - Faqat o'qish uchun (`POST/PUT` so'rovlarida qabul qilinmaydi)

        ```python
        id = serializers.IntegerField(read_only=True)
        ```

   - `write_only` (**bool**) - Faqat yozish uchun (**responselarda chiqmaydi**)   

        ```python
        password = serializers.CharField(write_only=True)
        ```

   - `required` (**bool**) - Majburiy maydon (`default: True`)

       ```python
       username = serializers.CharField(required=True)
       ```

   - `default` - Standart qiymat

        ```python
        is_active = serializers.BooleanField(default=True)
        ```
   - `allow_null` (**bool**) - Null qiymatga ruxsat (`default: False`)
        ```python
        middle_name = serializers.CharField(allow_null=True)
        ```
   - `source` - Manba maydoni nomi
        ```python
        full_name = serializers.CharField(source='get_full_name')
        ```
2. **Validatsiya parametrlari**

   - `validators` - Maxsus validatsiya funksiyalari ro'yxati
        ```python
        age = serializers.IntegerField(validators=[validate_age])
        ``` 
   - `min_length/max_length` - **Minimal/maksimal** uzunlik (CharField uchun)
        ```python
        password = serializers.CharField(min_length=8, max_length=32)
        ``` 
   - `min_value/max_value` - **Minimal/maksimal** qiymat (Raqamli fieldlar uchun)
        ```python
        age = serializers.IntegerField(min_value=18, max_value=120)
        ``` 
     
**`Field` turlari va ularga xos parametrlar**

1. `CharField`:
    ```python
    name = serializers.CharField(
        max_length=100,
        trim_whitespace=True,  # Boshlang'ich va oxirgi bo'shliqlarni olib tashlash
        allow_blank=False,     # Faqat bo'sh satrga ruxsat
    )
    ```
2. `IntegerField`:

    ```python
    quantity = serializers.IntegerField(
        min_value=0,
        max_value=100,
    )
    ```
3. `BooleanField`:

    ```python
    is_active = serializers.BooleanField(
        default=False,
        allow_null=True,  # Null qiymatga ruxsat
    )
    ```

4. `DateTimeField`:
    ```python
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M',  # Formatlash
        input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d'],  # Kirish formatlari
        default_timezone=pytz.UTC,  # Vaqt zonasi
    )
    ```
5. `EmailField`:

    ```python
    email = serializers.EmailField(
        allow_blank=False,
        max_length=254,
    )
    ```
6. `ChoiceField`:

    ```python
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
        allow_blank=True,
    )
    ```
7. `ListField`:
    ```python
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),  # Ichki field turi
        allow_empty=True,
    )
    ```
8. `DictField`:

    ```python
    metadata = serializers.DictField(
        child=serializers.IntegerField(),  # Value field turi
        allow_empty=True,
    )
    ```

`SerializerMethodField` - **Bu maxsus field turi bo'lib, metod orqali qiymat qaytaradi:**

```python
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
```
`Custom Validatsiya`

1. `validate_<field_name>` - Maxsus field validatsiyasi
    ```python
    def validate_username(self, value):
        if 'admin' in value.lower():
            raise serializers.ValidationError("Username cannot contain 'admin'")
        return value
    ```
2. `validate` - Bir nechta fieldlarni birga tekshirish

    ```python
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be before end date")
        return data
    ```

`SlugRelatedField` - **Boshqa modelga bog'lanish uchun ishlatiladi:**

```python
author = serializers.SlugRelatedField(
    queryset=User.objects.all(),
    slug_field='username'  # Ko'rsatiladigan field
)
```
>Bu `SlugRelatedField` parametrlar `DRF` serializatorlarida maydonlarni aniq nazorat qilish va ma'lumotlarni to'g'ri validatsiya qilish uchun ishlatiladi. Har bir loyiha talablariga qarab kerakli parametrlarni tanlab ishlatishingiz mumkin.

**`SlugRelatedField` ni `frontend-backend` almashinuviga misollar bilan tushuntiraman:**

1. `Oddiy `ForeignKey` Misoli (`Article` va `User`)`

    `Model`:
    ```python
    # models.py
    class User(models.Model):
        username = models.CharField(max_length=100, unique=True)
        
    class Article(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
    ```

    `Serializer` `serializers.py`:
    ```python
    # serializers.py
    class ArticleSerializer(serializers.ModelSerializer):
        author = serializers.SlugRelatedField(
            queryset=User.objects.all(),
            slug_field='username'
        )
        
        class Meta:
            model = Article
            fields = ['id', 'title', 'author']
    ```
    **Scenario 1: Maqola yaratish (`POST`)**

    **Frontend yuboradi:**
    ```json
    {
        "title": "DRF Tutorial",
        "author": "john_doe"  # <- Faqat username yuboriladi
    }
    ```

   **Backend jarayoni:**
   - `SlugRelatedField` **"john_doe"** `username` li **userni** bazadan qidiradi
   - Topilsa, yangi maqola yaratiladi
   - Topilmasa, 400 xato qaytaradi
   
   **Backend javobi (201 Created):**

    ```json
    {
        "id": 1,
        "title": "DRF Tutorial",
        "author": "john_doe"  # <- Frontendga yana username qaytariladi
    }
    ```
   **Scenario 2: Maqolani olish (GET)**
   **Frontend so'radi:**

    ```ini
    GET /api/articles/1/
    ```
    **Backend javobi (`200 OK`):**

    ```json
    {
        "id": 1,
        "title": "DRF Tutorial",
        "author": "john_doe"  # <- ID emas, username qaytariladi
    }
    ```
2. **`ManyToMany` misoli (`Article` va `Tag`)**

   `Model`:
   
   ```python
   # models.py
   class Tag(models.Model):
       name = models.CharField(max_length=50, unique=True)
   
   class Article(models.Model):
       title = models.CharField(max_length=200)
       tags = models.ManyToManyField(Tag)
   ```
   `Serializer`:

   ```python
   # serializers.py
   class ArticleSerializer(serializers.ModelSerializer):
       tags = serializers.SlugRelatedField(
           queryset=Tag.objects.all(),
           slug_field='name',
           many=True  # <- Ko'p bog'lanish ekanligi
       )
       
       class Meta:
           model = Article
           fields = ['id', 'title', 'tags']
   ```
   **Scenario 1: Maqola yaratish (`POST`)**

   **Frontend yuboradi:**
   ```json
   {
       "title": "Python Tips",
       "tags": ["programming", "python", "tips"]  # <- Tag nomlari listi
   }
   ```

   **Backend jarayoni:**

   - Har bir `tag` nomi uchun bazadan qidiradi
   - Mavjud bo'lmagan taglar uchun `400` xato qaytaradi
   - Barchasi topilsa, maqola yaratiladi va taglar bog'lanadi

   **Backend javobi (`201 Created`):**

   ```json
   {
       "id": 2,
       "title": "Python Tips",
       "tags": ["programming", "python", "tips"]  # <- Yaratilgan taglar
   }
   ```

   **Scenario 2: Maqolani yangilash (`PATCH`)**

   **Frontend yuboradi:**

   ```json
   {
       "tags": ["python", "django"]  # <- Faqat 2 tag qoldirildi
   }
   ```

   **Backend javobi (`200 OK`):**

   ```json
   {
       "id": 2,
       "title": "Python Tips",
       "tags": ["python", "django"]  # <- Yangilangan taglar
   }
   ```   

3. **Xato holatlari**

   **Noto'g'ri `username` yuborilganda:**

   ```json
   {
       "title": "New Article",
       "author": "nonexistent_user"
   }
   ```

   **Backend javobi (`400 Bad Request`):**

   ```json
   {
       "author": [
           "Object with username=nonexistent_user does not exist."
       ]
   }
   ```

   **Qanday qilib ishlaydi - `diagramma`:**
   
   ```ini
   Frontend (JSON)                  Backend (Python/Django)
   -------------                    ----------------------
   {                                ArticleSerializer(data=request.data)
     "title": "...",                 -> SlugRelatedField:
     "author": "john_doe"              1. User.objects.get(username="john_doe")
   }                                     2. article.author = found_user
                                      -> Maqola yaratildi
   
   {                                Article.objects.get(pk=1)
     "id": 1,                        -> SlugRelatedField:
     "title": "...",                    article.author.username => "john_doe"
     "author": "john_doe"           }
   }
   ```
**Xulosa:**

   - `Frontend` faqat `slug` qiymatini (`username`, `tag` nomi, etc.) yuboradi
   - `Backend` bu qiymat orqali asl obyektni topib bog'laydi
   - Javobda ham `slug` qiymati qaytariladi (obyekt emas)
   - Bu `JSON` strukturasini soddalashtiradi va frontendga ishlashni osonlashtiradi






















































































