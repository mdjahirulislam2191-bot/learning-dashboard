# 🐍 Python Day 3 — Loops (for / while)
## বারবার কাজ করা — সহজ বাংলায়

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | for loop | ১০ মিনিট |
| 2 | while loop | ১০ মিনিট |
| 3 | break / continue | ১০ মিনিট |
| 4 | প্র্যাকটিস |

---

## 📖 ১. for Loop — "প্রতিটা item-এর জন্য"

```python
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)
```

### আউটপুট:
```
apple
banana
mango
```

### range() দিয়ে সংখ্যা:

```python
for i in range(5):    # 0 থেকে 4
    print(i)

for i in range(1, 6): # 1 থেকে 5
    print(i)
```

---

## 📖 ২. while Loop — "যতক্ষণ শর্ত সত্য"

```python
count = 1

while count <= 5:
    print(count)
    count = count + 1  # ← ভুলে গেলে infinite loop!
```

---

## 📖 ৩. break & continue

```python
# break — লুথ থামাও
for i in range(10):
    if i == 5:
        break      # এখনই থামো
    print(i)       # 0,1,2,3,4

# continue — এই বার স্কিপ
for i in range(10):
    if i == 5:
        continue   # ৫ স্কিপ
    print(i)       # 0,1,2,3,4,6,7,8,9
```

---

## ✍️ প্র্যাকটিস

### Q1: ১ থেকে ১০০ যোগফল

```python
total = 0
for i in range(1, 101):
    total = total + i
print("যোগফল:", total)  # 5050
```

### Q2: লিস্টের গড়

```python
numbers = [10, 20, 30, 40, 50]
total = 0

for num in numbers:
    total = total + num

average = total / len(numbers)
print("গড়:", average)  # 30.0
```

---

## ✅ আজ যা শিখলে:

- ✅ `for` — লিস্টের প্রতিটা item-এর জন্য
- ✅ `while` — শর্ত সত্য থাকলে
- ✅ `break` / `continue` — নিয়ন্ত্রণ

---

**কোড রান করো:** `python ~/LearningPath/Python/week01_basics/day03_loops.py`