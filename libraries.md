### 1. `pygments` kutubxonasi nima uchun kerak?

> `pygments` - bu Python dasturlash tilida yozilgan kuchli sintaksisni ta'kidlash (`syntax highlighting`) kutubxonasi.

> `syntax highlighting` - sintaksisni ajratib ko'rsatish

**Qo'llanilishi:**

- **Dokumentatsiya vositalari:** `Sphinx`, `Read` the `Docs` kabi vositalarda kod misollarini rangli ko'rsatish
- **Bloglar va forumlar:** Kod parçalarini joylashtirishda
- **IDE va matn muharrirlari:** Kodni tushunarliroq qilish uchun
- **Veb-ilovalar:** Kodni veb-sahifalarda ko'rsatish


**Oddiy Misol**

```python
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

code = 'print("Hello, World!")'
highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())

print(highlighted_code)
```

### 2. `linenos` atamasining ma'nosi

> Dasturlash kontekstida `linenos` so'zi `line numbers` (qator raqamlari) ning qisqartmasidir. O'zbek tilida buni `qator raqamlari` deb tarjima qilish mumkin.


























































































