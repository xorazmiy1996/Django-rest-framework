### 1. Django-REST-Framework da qilinga barcha API larim uzoq vaqtda ishlayapti:

`Misol uchun`:

- **Serverdagi vaqtlar:**
    - `http://35.194.106.39:8000/token/` - **x-latency: `1.691 seconds`**
    - `http://35.194.106.39:8000/users/` - **x-latency: `1.129 seconds`**
    - `http://35.194.106.39:8000/payment/` - **x-latency: `1.658 seconds`**
- **Local kompyuterdag vaqtlar:**
    - `http://127.0.0.1:8000/token/` - **x-latency: `2.226 seconds`**
    - `http://127.0.0.1:8000/users/` - **x-latency: `1.993 seconds`**
    - `http://127.0.0.1:8000/payment/` - **x-latency: `2.930 seconds`**

**Mening kompyuterimning Konfiguratsiyasi uchun optimal `Latency`:**

| Scenario                       | Kutilgan Vaqt (Latency) |
|--------------------------------|-------------------------|
| Oddiy ish rejimi (DEBUG=True)  | 150-500 ms              |
| Produksion rejim (DEBUG=False) | 80-300 ms               |
| Optimallashtirilgan holat      | 50-200 ms               |





































































































