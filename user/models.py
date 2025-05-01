from django.db import models, transaction
from django.contrib.auth.hashers import make_password, check_password
from .managers import UserManager






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



class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='balance')
    main_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    frozen_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_transaction_id = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict)  # Standart Django JSONField

    def update_balance(self, amount, transaction_type, freeze=False):
        """Balansni xavfsiz yangilash"""
        with transaction.atomic():
            if freeze:
                self.frozen_balance += amount
            else:
                self.main_balance += amount
            self.save()

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'deposit', 'Toʻldirish'
        WITHDRAWAL = 'withdrawal', 'Yechib olish'
        TRANSFER = 'transfer', 'Oʻtkazma'
        PAYMENT = 'payment', 'Toʻlov'

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        COMPLETED = 'completed', 'Yakunlangan'
        FAILED = 'failed', 'Bajarilmadi'
        REVERSED = 'reversed', 'Qaytarilgan'

    user = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    details = models.JSONField(default=dict)  # Standart Django JSONField

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]



