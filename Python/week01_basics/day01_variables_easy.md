# Python Day 1 - Variables & Data Types
## Shohj Bangla te Python Shikha

---

## Aaj ki shikbo:

| # | Topic | Time |
|---|-------|------|
| 1 | Variable ki? | 5 min |
| 2 | Data Types (int, float, string, bool) | 10 min |
| 3 | Type check & conversion | 10 min |
| 4 | Practice | 15 min |

---

## 1. Variable ki? (Variable)

**Variable = Ekta box jaite data rakho**

Chintao tomar kichu box ache. Protita box e ekta nam lekha ache, ar vitore kichu rakha ache.

```
+-------------+
|  name       |  ->  "Jahirul"
+-------------+
|  age        |  ->  30
+-------------+
|  income     |  ->  4000
+-------------+
```

### Python e variable toiri:

```python
name = "Jahirul"        # Text (string)
age = 30                # Shongkha (integer)
income = 4000           # Shongkha (integer)
hourly_rate = 22.50     # Doshomik (float)
is_student = True       # Sothyo/Mithya (boolean)
```

> 💡 **Mone rakho**: Python e `var` ba `let` lage na — shorashori nam likhe `=` diye value bosoao.

---

## 2. Data Types (Data Types)

Python e 4 ta basic data type ache:

### int — Puron shongkha (Integer)

```python
age = 30
year = 2026
temperature = -5
```

### float — Doshomik shongkha

```python
hourly_rate = 22.50
tax_rate = 0.15
pi = 3.14159
```

### str — Text (String)

```python
name = "Jahirul Islam"
city = "Toronto"
email = 'whitepaperidea@gmail.com'
```

> 💡 **Mone rakho**: Text shongshomay quotes er vitore — `"..."` ba `'...'`

### bool — Sothyo/Mithya (Boolean)

```python
is_student = True
is_working = False
is_refugee = True
```

> 💡 **Mone rakho**: `True` ar `False` — prothom shongkha boro hater hobe.

---

## 3. Type check kora — type()

Kon variable e ki type er data ashe jante:

```python
print(type(name))        # <class 'str'>
print(type(age))         # <class 'int'>
print(type(hourly_rate)) # <class 'float'>
print(type(is_student))  # <class 'bool'>
```

---

## 4. Type conversion (Type Conversion)

Theke ek type theke onk type e badlo:

```python
# String -> Integer
age_text = "30"
age_number = int(age_text)     # 30 (integer)

# Integer -> String
year = 2026
year_text = str(year)          # "2026" (string)

# String -> Float
price = "22.50"
price_num = float(price)       # 22.5 (float)

# Integer -> Float
x = 10
y = float(x)                   # 10.0
```

---

## 5. Input — User theke data nea

```python
name = input("Tumar nam ki? ")
age = input("Boyos koto? ")

print("Hello", name)
print("Tumar boyos:", age)
```

> ⚠️ **Sotorkota**: `input()` shongshomay string dey. Shongkha hishebe babohar korte `int()` ba `float()` dorkar.

```python
age = int(input("Boyos koto? "))  # integer hishebe nebe
```

---

## Practice (15 min)

### Q1: Nijer tthongkho variable e rakho

```python
# Eta tumi nije likho:
my_name = "____________"
my_age = ___
my_city = "____________"
my_income = ___
is_learning = ___

print(my_name, my_age, my_city, my_income, is_learning)
```

### Q2: Type check koro

```python
# Protita variable er type print koro
print(type(my_name))      # Ki asbe?
print(type(my_age))       # Ki asbe?
print(type(my_income))    # Ki asbe?
```

### Q3: User theke input nao

```python
# Emon ekta program likho ja:
# 1. User er nam jiggesh korbe
# 2. Boyos jiggesh korbe
# 3. "Hello [nam], tumar boyos [boyos] boshor" print korbe
```

### Q4: Tax calculator

```python
# monthly_income theke 15% tax ber koro
monthly_income = 4000
tax_rate = 0.15
tax_amount = ________
net_income = ________

print("Tax:", tax_amount)
print("Net aay:", net_income)
```

---

## Aaj ja shikhlo:

- ✅ Variable = Data rakhar box
- ✅ 4 ta basic type: int, float, str, bool
- ✅ `type()` diye type check
- ✅ `int()`, `float()`, `str()` diye conversion
- ✅ `input()` diye user theke data nea

---

## Poroborti: Day 2 — Conditions (if/else)

> "Jodi aay 5000 er beshi hoy, tahole savings barao — na hole khorch komoao"

---

**Code run koro:** `python ~/LearningPath/Python/week01_basics/day01_variables.py`