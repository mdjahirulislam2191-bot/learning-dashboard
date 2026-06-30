-- =============================================
-- 📚 DAY 5 — SQL JOINs (INNER, LEFT, RIGHT)
-- =============================================
-- আজকের টপিক: দুই বা তার বেশি টেবিল থেকে ডাটা JOIN করা।
-- Data Analyst-দের সবচেয়ে দরকারি SQL Skill!
-- =============================================

USE my_portfolio;

-- আগে দেখি আমাদের কি টেবিল আছে
SELECT '--- EXISTING TABLES ---' AS '';
SHOW TABLES;

-- ===== Section 1: INNER JOIN =====
-- INNER JOIN = শুধু ম্যাচ করা রেকর্ড দেখায়

-- প্রথমে finance_log এর সাথে match করার জন্য নতুন টেবিল বানাই
SELECT '--- CREATING CATEGORIES TABLE ---' AS '';
CREATE TABLE IF NOT EXISTS expense_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    budget_limit DECIMAL(10,2)
);

INSERT INTO expense_categories (category_name, budget_limit) VALUES
('Housing', 1300.00),
('Food', 400.00),
('Transport', 100.00),
('Utilities', 150.00),
('Entertainment', 100.00);

SELECT '--- CATEGORIES ---' AS '';
SELECT * FROM expense_categories;

-- finance_log-এ category_id কলাম যোগ করি
-- Note: MySQL 8.4 IF NOT EXISTS syntax আলাদা, তাই সরাসরি ADD COLUMN
ALTER TABLE finance_log ADD COLUMN category_id INT;

-- কিছু ডাটা আপডেট করি
UPDATE finance_log SET category_id = 1 WHERE description LIKE '%Rent%';
UPDATE finance_log SET category_id = 1 WHERE description LIKE '%Apartment%';
UPDATE finance_log SET category_id = 2 WHERE description LIKE '%Food%' OR description LIKE '%Grocery%';
UPDATE finance_log SET category_id = 3 WHERE description LIKE '%Transport%';
UPDATE finance_log SET category_id = 4 WHERE description LIKE '%Electricity%' OR description LIKE '%Internet%' OR description LIKE '%Bill%';

SELECT '--- 📊 INNER JOIN ---' AS '';
-- দুই টেবিল join: finance_log + expense_categories
SELECT 
    f.id,
    f.description,
    f.amount,
    f.transaction_type,
    e.category_name,
    e.budget_limit
FROM finance_log f
INNER JOIN expense_categories e ON f.category_id = e.id;

-- ===== Section 2: LEFT JOIN =====
-- LEFT JOIN = বাম টেবিলের সব রেকর্ড + ডান টেবিলের ম্যাচ করা রেকর্ড

SELECT '--- 📊 LEFT JOIN (all transactions + category if exists) ---' AS '';
SELECT 
    f.description,
    f.amount,
    e.category_name
FROM finance_log f
LEFT JOIN expense_categories e ON f.category_id = e.id;

-- ===== Section 3: RIGHT JOIN =====
-- RIGHT JOIN = ডান টেবিলের সব রেকর্ড + বাম টেবিলের ম্যাচ

SELECT '--- 📊 RIGHT JOIN (all categories + transactions if any) ---' AS '';
SELECT 
    e.category_name,
    e.budget_limit,
    f.description,
    f.amount
FROM finance_log f
RIGHT JOIN expense_categories e ON f.category_id = e.id;

-- ===== Section 4: Real-World Scenario =====
-- আপনার পোর্টফোলিওর জন্য: income_sources + finance_log

SELECT '--- 🏦 YOUR INCOME vs EXPENSES ---' AS '';
SELECT 
    COALESCE(i.source_name, 'EXPENSE') AS item_name,
    COALESCE(i.amount_cad, f.amount) AS amount,
    CASE WHEN i.id IS NOT NULL THEN 'INCOME' ELSE 'EXPENSE' END AS type
FROM income_sources i
LEFT JOIN finance_log f ON i.amount_cad = f.amount
UNION
SELECT 
    f.description,
    f.amount,
    'EXPENSE'
FROM finance_log f
WHERE f.transaction_type = 'expense'
ORDER BY amount DESC;

-- Month-end summary: total income vs total expense
SELECT '--- 💰 MONTHLY SUMMARY ---' AS '';
SELECT 
    'Total Income' AS category,
    SUM(amount_cad) AS total
FROM income_sources
UNION
SELECT 
    'Total Expense',
    SUM(amount)
FROM finance_log
WHERE transaction_type = 'expense';

/*
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: expense_categories টেবিলে 'Savings' নামে নতুন ক্যাটাগরি যোগ করো
        budget_limit = 1000

TASK 2: finance_log থেকে সব income transactions বের করো 
        expense_categories এর সাথে LEFT JOIN করে

TASK 3: কোন ক্যাটাগরিতে সবচেয়ে বেশি খরচ হয়েছে?
        GROUP BY + JOIN + ORDER BY ব্যবহার করে বের করো

TASK 4 (চ্যালেঞ্জ): 
        budget_limit এর চেয়ে বেশি খরচ হয়েছে এমন ক্যাটাগরি বের করো
        (WHERE + JOIN + GROUP BY + HAVING)
============================================
*/