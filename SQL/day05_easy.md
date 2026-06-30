# 🗄️ SQL Day 5 — JOIN: দুই টেবিল জোড়া দেওয়া
## সহজ বাংলায়

---

## 🎯 আজ কী শিখবে:

| # | বিষয় | সময় |
|---|-------|------|
| 1 | JOIN কী? | ১০ মিনিট |
| 2 | INNER JOIN | ১০ মিনিট |
| 3 | LEFT JOIN | ১০ মিনিট |
| 4 | প্র্যাকটিস |

---

## 📖 ১. JOIN কী?

**JOIN = দুইটা টেবিল একটা common column দিয়ে জোড়া দাও**

উদাহরণ:
- `students` টেবিলে আছে: name, age, city
- `orders` টেবিলে আছে: student_id, product, amount

JOIN করলে জানতে পারবে **কে কী কিনেছে**।

---

## 📖 ২. INNER JOIN — মিল আকা ডাটা

```sql
SELECT students.name, orders.product, orders.amount
FROM students
INNER JOIN orders ON students.id = orders.student_id;
```

> শুধু যাদের order আছে তারা দেখাবে।

---

## 📖 ৩. LEFT JOIN — বাম টেবিলের সব

```sql
SELECT students.name, orders.product, orders.amount
FROM students
LEFT JOIN orders ON students.id = orders.student_id;
```

> সবাই দেখাবে — order না থাকলে NULL দেখাবে।

---

## 📖 ৪. JOIN Types Summary

```
INNER JOIN:  মিল আকা ডাটা
LEFT JOIN:   বাম টেবিলের সব + ডান টেবিলের মিল
RIGHT JOIN:  ডান টেবিলের সব + বাম টেবিলের মিল
FULL JOIN:   দুটোই সব
```

---

## ✍️ প্র্যাকটিস

```sql
-- Q1: students + orders INNER JOIN
SELECT s.name, o.product, o.amount
FROM students s
INNER JOIN orders o ON s.id = o.student_id;

-- Q2: LEFT JOIN — যাদের order নেই তারাও দেখো
SELECT s.name, o.product
FROM students s
LEFT JOIN orders o ON s.id = o.student_id;

-- Q3: কে কত টাকা order করেছে
SELECT s.name, SUM(o.amount) as total_spent
FROM students s
LEFT JOIN orders o ON s.id = o.student_id
GROUP BY s.name;
```

---

## ✅ আজ যা শিখলে:

- ✅ JOIN = দুই টেবিল জোড়া
- ✅ INNER JOIN — মিল আকা
- ✅ LEFT JOIN — বাম টেবিলের সব

---

**কোড রান করো:** `mysql -u root < ~/LearningPath/SQL/day05_mysql_joins.sql`