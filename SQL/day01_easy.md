# SQL Day 1 - MySQL Setup & First Database
## Shobuj Bangla te SQL Shikha

---

## Aaj ki shikbo:

| # | Topic | Time |
|---|-------|------|
| 1 | SQL ki? Keno shikbo? | 5 min |
| 2 | MySQL chalu kora | 5 min |
| 3 | Database toiri kora | 10 min |
| 4 | Table toiri kora | 10 min |
| 5 | Data dhokano (INSERT) | 10 min |

---

## 1. SQL ki?

**SQL = Structured Query Language**

Shohj bhashe: **Database er sathe kotha bolar bhasha**.

```
Tumi  ->  SQL  ->  Database
         ^
    "Amarke sob
     customer dekhao"
```

### Bastob udaharon:

| Kaj | SQL Kotha |
|-----|--------|
| Sob data dekhao | `SELECT * FROM customers;` |
| Notun data jog koro | `INSERT INTO customers VALUES (...);` |
| Data baddalo | `UPDATE customers SET name = 'X';` |
| Data muche felo | `DELETE FROM customers WHERE id = 1;` |

---

## 2. MySQL chalu koro

### Step 1: Terminal open koro (Git Bash)

### Step 2: MySQL te connect koro

```bash
mysql -u root
```

> 💡 Tumar kono password nei, tai shorashori `mysql -u root` lekhlei hobe.

### Step 3: Kaj shesh e bero ho

```sql
EXIT;
```

---

## 3. Database toiri koro

**Database = Datar bash** — ekta boro folder jaite onek table thake.

```sql
-- Notun database toiri
CREATE DATABASE my_learning;

-- Kono kono database ache dekho
SHOW DATABASES;

-- Ekhon oi database babohar koro
USE my_learning;
```

### Output:
```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| my_learning        |  ← Tumar ta
| mysql              |
| performance_schema |
+--------------------+
```

---

## 4. Table toiri koro

**Table = Datar table** — Excel sheet er moto.

Chintao ekta Excel sheet:

| id | name | age | city |
|----|------|-----|------|
| 1 | Jahirul | 30 | Toronto |
| 2 | Tanni | 28 | Toronto |

SQL e etaa toiri korte:

```sql
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(50),
    income DECIMAL(10,2)
);
```

### Bhasha:

| Column | Type | Mane |
|--------|------|------|
| `id` | INT | Shongkha, PRIMARY KEY = unique id |
| `name` | VARCHAR(100) | 100 shongkhar porjonto text |
| `age` | INT | Puron shongkha |
| `city` | VARCHAR(50) | 50 shongkhar porjonto text |
| `income` | DECIMAL(10,2) | Doshomik shongkha |

### Table dekho:

```sql
-- Kono kono table ache
SHOW TABLES;

-- Table er structure dekho
DESCRIBE students;
```

---

## 5. Data dhokao - INSERT

```sql
-- Ekta data dhokao
INSERT INTO students (name, age, city, income)
VALUES ('Jahirul', 30, 'Toronto', 4000.00);

-- Arekta data dhokao
INSERT INTO students (name, age, city, income)
VALUES ('Tanni', 28, 'Toronto', 0.00);

-- Ekshathe ekadhik data
INSERT INTO students (name, age, city, income) VALUES
('Rahim', 25, 'Dhaka', 500.00),
('Karim', 35, 'Dhaka', 800.00),
('Salma', 22, 'Chittagong', 300.00);
```

---

## 6. Data dekho - SELECT

```sql
-- Sob data dekho
SELECT * FROM students;

-- Shudhu nam ar boyos dekho
SELECT name, age FROM students;

-- Shongkha diye dekho (boyos 25 er beshi)
SELECT * FROM students WHERE age > 25;
```

### Output:
```
+----+---------+------+---------+---------+
| id | name    | age  | city    | income  |
+----+---------+------+---------+---------+
|  1 | Jahirul |   30 | Toronto | 4000.00 |
|  2 | Tanni   |   28 | Toronto |    0.00 |
|  3 | Rahim   |   25 | Dhaka   |  500.00 |
|  4 | Karim   |   35 | Dhaka   |  800.00 |
|  5 | Salma   |   22 | Chittagong | 300.00 |
+----+---------+------+---------+---------+
```

---

## Practice (15 min)

### Q1: Nijer database toiri koro

```sql
-- 1. Ekta database toiri koro naam 'immigration_ai'
CREATE DATABASE ________;

-- 2. Oi database babohar koro
USE ________;
```

### Q2: Ekta table toiri koro

```sql
-- 'clients' naame table toiri koro:
-- id (auto increment, primary key)
-- name (text, 100 char max)
-- country (text, 50 char max)
-- status (text: 'pending', 'approved', 'rejected')
-- income (decimal)

CREATE TABLE clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    country VARCHAR(50),
    status VARCHAR(20),
    income DECIMAL(10,2)
);
```

### Q3: Data dhokao

```sql
-- 5 ta data dhokao (tomar poribarer shongkha diye)
INSERT INTO clients (name, country, status, income) VALUES
('Jahirul', 'Canada', 'pending', 4000.00),
('Tanni', 'Canada', 'pending', 0.00),
('_______', '_______', '_______', _______),
('_______', '_______', '_______', _______),
('_______', '_______', '_______', _______);
```

### Q4: Data dekho

```sql
-- Sob data dekho
SELECT * FROM clients;

-- Shudhu 'pending' status dekho
SELECT * FROM clients WHERE status = 'pending';

-- Aay 1000 er beshi dekho
SELECT * FROM clients WHERE income > 1000;
```

---

## Aaj ja shikhlo:

- ✅ SQL = Database er sathe kotha bolar bhasha
- ✅ `CREATE DATABASE` — database toiri
- ✅ `CREATE TABLE` — table toiri
- ✅ `INSERT INTO` — data dhokano
- ✅ `SELECT` — data dekha
- ✅ `WHERE` — shongkha dewa

---

## Poroborti: Day 2 — CRUD Operations

> "Data toiri, poro, baddalo, muche felo — char ta mul kaj"

---

**Code run koro:** `mysql -u root < ~/LearningPath/SQL/day01_mysql_setup.sql`