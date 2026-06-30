# 🗄️ SQL Day 3 — WHERE: শর্ত দিয়ে ডাটা খোঁজা
## সহজ বাংলায়

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | WHERE basics | ১০ মিনিট |
| 2 | LIKE (pattern matching) | ১০ মিনিট |
| 3 | IN ও BETWEEN | ১০ মিনিট |
| 4 | AND / OR / NOT | ১০ মিনিট |

---

## 📖 ১. WHERE কী?

**WHERE = "যেখানে"** — শর্ত দিয়ে ডাটা ফিল্টার করো।

```sql
SELECT * FROM students WHERE age > 25;
```

---

## 📖 ২. Comparison Operators

| চিহ্ন | মানে | Example |
|-------|------|---------|
| `=` | সমান | `WHERE city = 'Toronto'` |
| `!=` বা `<>` | সমান নয় | `WHERE city != 'Toronto'` |
| `>` | বড় | `WHERE age > 25` |
| `<` | ছোট | `WHERE age < 30` |
| `>=` | বড় বা সমান | `WHERE income >= 1000` |
| `<=` | ছোট বা সমান | `WHERE income <= 5000` |

---

## 📖 ৩. LIKE — Pattern খোঁজা

```sql
-- 'J' দিয়ে শুরু হওয়া নাম
SELECT * FROM students WHERE name LIKE 'J%';

-- 'a' দিয়ে শেষ হওয়া নাম
SELECT * FROM students WHERE name LIKE '%a';

-- 'ann' আকা নাম
SELECT * FROM students WHERE name LIKE '%ann%';
```

| Pattern | মানে |
|---------|------|
| `'J%'` | J দিয়ে শুরু |
| `'%a'` | a দিয়ে শেষ |
| `'%ann%'` | মাঝে ann আছে |

---

## 📖 ৪. IN — যেকোনো একটা মিললে

```sql
-- Toronto বা Dhaka
SELECT * FROM students WHERE city IN ('Toronto', 'Dhaka');
```

---

## 📖 ৫. BETWEEN — রেঞ্জের মধ্যে

```python
-- বয়স 25-30 এর মধ্যে
SELECT * FROM students WHERE age BETWEEN 25 AND 30;

-- আয় 500-4000 এর মধ্যে
SELECT * FROM students WHERE income BETWEEN 500 AND 4000;
```

---

## 📖 ৬. AND / OR / NOT

```sql
# AND — দুটোই সত্য
SELECT * FROM students WHERE age > 25 AND city = 'Toronto';

-- OR — যেকোনো একটা সত্য
SELECT * FROM students WHERE city = 'Toronto' OR city = 'Dhaka';

-- NOT — উল্টো
SELECT * FROM students WHERE NOT city = 'Toronto';
```

---

## ✍️ প্র্যাকটিস

```sql
-- Q1: আয় 1000 এর বেশি দেখো
SELECT * FROM students WHERE _____;

-- Q2: Dhaka-বাসী দেখো
SELECT * FROM students WHERE _____;

-- Q3: বয়স 25-35 এর মধ্যে এবং আয় 500 এর বেশি
SELECT * FROM students WHERE _____ AND _____;

-- Q4: নাম 'J' দিয়ে শুরু
SELECT * FROM students WHERE name LIKE _____;

-- Q5: Dhaka বা Chittagong-বাসী
SELECT * FROM students WHERE city IN (_____);
```

---

## ✅ আজ যা শিখলে:

- ✅ `WHERE` — শর্ত দিয়ে ফিল্টার
- ✅ `LIKE` — pattern খোঁজা
- ✅ `IN` / `BETWEEN` — রেঞ্জ ও লিস্ট
- ✅ `AND` / `OR` / `NOT` — যৌগিক শর্ত

---

**কোড রান করো:** `mysql -u root < ~/LearningPath/SQL/day03_mysql_filtering.sql`