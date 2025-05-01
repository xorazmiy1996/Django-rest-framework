
### 1. `style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)` ushbu sintaksisni tushuntirib ber nima uchun ChardField  ichida choices ishlatilgan.

> Ushbu kod `Django` modelida `CharField` maydoni yaratish uchun ishlatilgan, unda `choices` parametri bilan qiymatlar cheklangan ro'yxatdan tanlanishi ta'minlangan.

**Tushuntirish:**

```python
style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
```
1. `CharField` - Belgilar (text) saqlash uchun `Django` model maydoni
2. `choices=STYLE_CHOICES` - Maydon qiymatlari cheklangan ro'yxatdan tanlanishini belgilaydi
   - `STYLE_CHOICES` bu tuplelar tuple'i bo'lib, har biri (qiymat, insonga o'qish uchun ko'rinish) formatida
3. `default='friendly'` - Agar qiymat kiritilmasa, standart qiymat sifatida `friendly` olinadi
4. `max_length=100` - Maydon maksimal uzunligi (`DB` uchun)

**Nima uchun choices ishlatilgan?**

1. **Ma'lumotlar to'g'riligi:** Faqat ro'yxatdagi qiymatlarni qabul qilish
2. **Foydalanuvchi interfeysi:** Django admin va formlarda `dropdown/select` ko'rinishida ko'rsatish
3. **Ma'lumotlar izchilligi:** Bir xil qiymatlar buta tizimda standart tarzda saqlanishi
