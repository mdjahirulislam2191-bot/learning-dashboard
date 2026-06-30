# 🐍 Python Day 4 — Lists & Dictionaries
## অনেক ডাটা একসাথে রাখো — সহজ বাংলায়

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | List কী? | ১০ মিনিট |
| 2 | List methods | ১০ মিনিট |
| 3 | Dictionary | ১০ মিনিট |
| 4 | প্র্যাকটিস |

---

## 📖 ১. List কী?

**List = অনেকটা ডাটা একটা ভেরিয়েবলে রাখো**

```python
fruits = ["apple", "banana", "mango"]
numbers = [10, 20, 30, 40, 50]
mixed = ["Jahirul", 30, True, 4000.00]
```

### Index (সূচক) দিয়ে ডাটা পড়ো:

```python
fruits = ["apple", "banana", "mango"]
#         [0]       [1]       [2]

print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[-1])  # mango (শেষ থেকে)
```

---

## 📖 ২. List Methods (যোগ/মুছা/সাজানো)

```python
fruits = ["apple", "banana"]

# যোগ করো
fruits.append("mango")     # ["apple", "banana", "mango"]

# মুছো
fruits.remove("banana")    # ["apple", "mango"]

# সাজাও
fruits.sort()              # alphabetical

# লেংথ
len(fruits)                # 2
```

---

## 📖 ৩. Dictionary — Key-Value জোড়া

**Dictionary = নাম দিয়ে ডাটা রাখো**

```python
student = {
    "name": "Jahirul",
    "age": 30,
    "city": "Toronto",
    "income": 4000
}
```

### ডাটা পড়ো:

```python
print(student["name"])    # Jahirul
print(student["age"])     # 30
print(student["city"])    # Toronto
```

### ডাটা বদলাও:

```python
student["income"] = 5000
student["status"] = "active"  # নতুন key যোগ
```

---

## ✍️ প্র্যাকটিস

### Q1: নিজের info dictionary বানাও

```python
me = {
    "name": "_____",
    "age": ___,
    "city": "_____",
    "income": ___,
    "goal": "_____"
}

print(me["name"], "earns", me["income"])
```

### Q2: List থেকে গড় বের করো

```python
incomes = [4000, 4200, 3800, 4500, 4100, 4300]

total = 0
for income in incomes:
    total = total + income

average = total / len(incomes)
print("গড় আয়:", average)
```

### Q3: Dictionary list

```python
students = [
    {"name": "Jahirul", "age": 30},
    {"name": "Tanni", "age": 28},
    {"name": "Rahim", "age": 25}
]

for student in students:
    print(student["name"], student["age"])
```

---

## ✅ আজ যা শিখলে:

- ✅ List — অনেক ডাটা একসাথে
- ✅ Index দিয়ে পড়ো
- ✅ Dictionary — key-value জোড়া
- ✅ append/remove/sort

---

**কোড রান করো:** `python ~/LearningPath/Python/week01_basics/day04_lists_dicts.py`