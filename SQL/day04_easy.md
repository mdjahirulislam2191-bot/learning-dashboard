# 🗄️ SQL Day 4 — GROUP BY: ডাটা গ্রুপ করা ও হিসাব
## সহজ বাংলায়

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | GROUP BY basics | ১০ মিনিট |
| 2 | COUNT, SUM, AVG, MAX, MIN | ১০ মিনিট |
| 3 | HAVING (গ্রুপ ফিল্টার) | ১০ মিনিট |
| 4 | প্র্যাকটিস |

---

## 📖 ১. GROUP BY কী?

**GROUP BY = একই ধরনের ডাটা একসাথে গ্রুপ করো**

উদাহরণ: city অনুযায়ী গ্রুপ করলে প্রতিটা city-তে কতজন আছে জানতে পারবে।

```sql
SELECT city, COUNT(*) as total
FROM students
GROUP BY city;
```

### আউটপুট:
```
+------------+-------+
| city       | total |
+------------+-------+
| Dhaka      |     2 |
| Toronto    |     2 |
| Chittagong |     1 |
+------------+-------+
```

---

## 📖 ২. Aggregate Functions (হিসাব করার ফাংশন)

| ফাংশন | কাজ | উদাহরণ |
|-------|-----|--------|
| `COUNT(*)` | কতটা row | `SELECT COUNT(*) FROM students` |
| `SUM(col)` | যোগফল | `SELECT SUM(income) FROM students` |
| `AVG(col)` | গড় | `SELECT AVG(age) FROM students` |
| `MAX(col)` | সর্বোচ্চ | `SELECT MAX(income) FROM students` |
| `MIN(col)` | সর্বনিম্ন | `SELECT MIN(income) FROM students` |

---

## 📖 ৩. GROUP BY + Aggregate

```sql
-- প্রতিটাতে city-তে কতজন আছে, গড় আয় কত
SELECT city,
       COUNT(*) as total_people,
       AVG(income) as avg_income,
       MAX(income) as max_income
FROM students
GROUP BY city;
```

### আউটপুট:
```
+------------+--------------+------------+------------+
| city       | total_people | avg_income | max_income |
+------------+--------------+------------+------------+
| Dhaka      |            2 |     650.00 |     800.00 |
| Toronto    |            2 |    2000.00 |    4000.00 |
| Chittagong |            1 |     300.00 |     300.00 |
+------------+--------------+------------+------------+
```

---

## 📖 ৪. HAVING — গ্রুপ ফিল্টার

> **WHERE = row ফিল্টার, HAVING = গ্রুপ ফিল্টার**

```sql
-- যেখানে ১ জন বেশি আছে
SELECT city, COUNT(*) as total
FROM students
GROUP BY city
HAVING total > 1;
```

---

## ✍️ প্র্যাকটিস

```sql
-- Q1: মোট কতজন আছে
SELECT COUNT(*) FROM students;

-- Q2: মোট আয় কত
SELECT SUM(income) FROM students;

-- Q3: গড় বয়স
SELECT AVG(age) FROM students;

-- Q4: City অনুযায়ী গ্রুপ করো, গড় আয় সহ
SELECT city, COUNT(*) as total, AVG( Income) as avg_income
FROM students
GROUP BY city;

-- Q5: ১ জন বেশি আসা city দেখো
SELECT city, COUNT(*) as total
FROM students
GROUP BY city
HAVING total > 1;
```

---

## ✅ আজ যা শিখলে:

- ✅ `GROUP BY` — ডাটা গ্রুপ করো
- ✅ `COUNT/SUM/AVG/MAX/MIN` — হিসাব
- ✅ `HAVING` — গ্রুপ ফিল্টার

---

**কোড রান করো:** `mysql -u root < ~/LearningPath/SQL/day04_mysql_grouping.sql`