# 🐍 Python Day 2 — Conditions (if / elif / else)
## সহজ বাংলায় — শর্ত লেখা

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | if statement | ১০ মিনিট |
| 2 | if-else | ১০ মিনিট |
| 3 | if-elif-else | ১০ মিনিট |
| 4 | প্র্যাকটিস |

---

## 📖 ১. if Statement — "যদি"

**মানে**: একটা শর্ত সত্য হলে কাজ করো।

```python
age = 30

if age >= 18:
    print("তুমি ভোট দিতে পারো")
```

### আউটপুট:
```
তুমি ভোট দিতে পারো
```

> 💡 **মনে রাখো**: `:` দিয়ে শেষ + indentation (স্পেস) দিতে হবে

---

## 📖 ২. if-else — "যদি...না হলে"

```python
income = 4000

if income > 5000:
    print("তুমি সেভিংস বাড়াতে পারো")
else:
    print("আগে আয় বাড়াও")
```

---

## 📖 ৩. if-elif-else — "যদি...যদি না...না হলে"

```python
income = 4000

if income >= 10000:
    print("লাক্সারি লাইফ!")
elif income >= 5000:
    print("ভালো লাইফ")
elif income >= 3000:
    print("চলবে গা")
else:
    print("কষ্ট করতে হবে")
```

---

## 💡 তুলনামূলক চিহ্ন (Comparison Operators)

| চিহ্ন | মানে | উদাহরণ |
|-------|------|--------|
| `==` | সমান | `age == 30` |
| `!=` | সমান নয় | `age != 25` |
| `>` | বড় | `income > 5000` |
| `<` | ছোট | `age < 18` |
| `>=` | বড় বা সমান | `age >= 18` |
| `<=` | ছোট বা সমান | `age <= 60` |

---

## ✍️ প্র্যাকটিস

### Q1: গ্রেড ক্যালকুলেটর

```python
marks = 75

if marks >= 80:
    grade = "A"
elif marks >= 70:
    grade = "B"
elif marks >= 60:
    grade = "C"
elif marks >= 50:
    grade = "D"
else:
    grade = "F"

print("গ্রেড:", grade)
```

---

## ✅ আজ যা শিখলে:

- ✅ `if` — শর্ত সত্য হলে
- ✅ `if-else` — সত্য না মিথ্যা
- ✅ `if-elif-else` — একাধিক শর্ত

---

**কোড রান করো:** `python ~/LearningPath/Python/week01_basics/day02_conditions.py`