### 1. `Django REST Framework` uchun `Swagger` (`DRF Spectacular`) ni to'liq sozlash.

1. **Kerakli paketlarni o'rnatish**
    ```bash
    pip install drf-spectacular
    ```
2. Asosiy Sozlamalar (`settings.py`)   
    ```python
    INSTALLED_APPS = [
        ...
        'drf_spectacular',
        'drf_spectacular_sidecar',  # Static fayllar uchun (ixtiyoriy)
        ...
    ]
    
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        # Boshqa DRF sozlamalari...
    }
    
    SPECTACULAR_SETTINGS = {
        'TITLE': 'Loyiha API Dokumentatsiyasi',
        'DESCRIPTION': 'Loyiha API si uchun to\'liq dokumentatsiya',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
        
        # Swagger UI sozlamalari
        'SWAGGER_UI_DIST': 'SIDECAR',  # Sidecar modda uchun
        'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
        'SWAGGER_UI_SETTINGS': {
            'deepLinking': True,
            'persistAuthorization': True,
            'displayOperationId': True,
        },
        
        # API ni guruhlash
        'TAGS': [
            {'name': 'users', 'description': 'Foydalanuvchilar bilan ishlash'},
            {'name': 'products', 'description': 'Mahsulotlar bilan ishlash'},
        ],
        
        # Autentifikatsiya sozlamalari (JWT uchun)
        'SECURITY_DEFINITIONS': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Token format: Bearer <token>'
            }
        },
    }
    ```

3. **`URL` manzillarini sozlash (`urls.py`)**
    ```python
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView
    )
    
    urlpatterns = [
        ...
        # Schema YAML formatda
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        
        # Swagger UI
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        
        # ReDoc (alternativ dokumentatsiya)
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ...
    ]
    ```

4. **Viewlar va Serializerlar uchun qo'shimcha izohlar**

    ```python
    from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
    
    @extend_schema(
        tags=['users'],
        summary='Foydalanuvchilar ro\'yxati',
        description='Barcha foydalanuvchilarni ko\'rish uchun API',
        parameters=[
            OpenApiParameter(
                name='is_active',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Faol foydalanuvchilarni filterlash',
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='Faol foydalanuvchilar',
                        value=True
                    ),
                ]
            ),
        ],
        responses={
            200: UserSerializer(many=True),
            401: {'description': 'Kirish rad etildi'},
        }
    )
    class UserListView(APIView):
        ...
    ```

5. **`JWT` `Token` bilan ishlash uchun qo'shimcha sozlash**

    ```python
    SPECTACULAR_SETTINGS = {
        ...
        'PREPROCESSING_HOOKS': [
            'drf_spectacular.hooks.preprocess_exclude_path_format',
        ],
        'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
        'AUTHENTICATION_WHITELIST': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }
    ```
6. **Model fieldlari uchun izohlar**

    ```python
    from drf_spectacular.utils import extend_schema_field
    
    class UserSerializer(serializers.ModelSerializer):
        status = serializers.SerializerMethodField()
        
        @extend_schema_field(
            field=serializers.ChoiceField(choices=['active', 'inactive']),
            description='Foydalanuvchi holati'
        )
        def get_status(self, obj):
            return 'active' if obj.is_active else 'inactive'
    ```

7. **`Swagger UI` ni sozlash (`CSS/JS`)**

    Agar siz `Swagger` interfeysini o'zgartirmoqchi bo'lsangiz:
    ```python
    SPECTACULAR_SETTINGS = {
        ...
        'SWAGGER_UI_SETTINGS': {
            'docExpansion': 'none',
            'defaultModelRendering': 'model',
            'defaultModelExpandDepth': 2,
            'defaultModelsExpandDepth': 2,
            'showExtensions': True,
            'showCommonExtensions': True,
        },
        'SWAGGER_UI_FAVICON_HREF': 'https://example.com/favicon.ico',
        'SWAGGER_UI_CUSTOM_CSS': '/static/css/swagger-custom.css',
        'SWAGGER_UI_CUSTOM_JS': '/static/js/swagger-custom.js',
    }
    ```
8. **`Server` sozlamalari**

    ```python
    SPECTACULAR_SETTINGS = {
        ...
        'SERVERS': [
            {'url': 'https://api.example.com', 'description': 'Production server'},
            {'url': 'https://sandbox.api.example.com', 'description': 'Staging server'},
            {'url': 'http://127.0.0.1:8000', 'description': 'Local development server'},
        ],
    }
    ```

9. **Sozlamalarni tekshirish**

    ```bash
    python manage.py spectacular --file schema.yml --validate
    ```

10. **Produksiya uchun muhim eslatmalar**

    - Produksiya uchun muhim eslatmalar
    - `DEBUG=False` bo'lganda ham ishlashi uchun:

      ```python
      if not DEBUG:
          SPECTACULAR_SETTINGS['SWAGGER_UI_DIST'] = None  # Sidecar ni o'chirish
          SPECTACULAR_SETTINGS['SWAGGER_UI_FAVICON_HREF'] = None
      ```
> Bu sozlashlar orqali siz `Django REST Framework` loyihangiz uchun to'liq funktsional `Swagger` dokumentatsiyasini yaratishingiz mumkin bo'ladi.

























































































