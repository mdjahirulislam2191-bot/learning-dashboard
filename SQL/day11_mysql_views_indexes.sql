-- =============================================
-- 📚 DAY 11 — SQL Views & Indexes
-- =============================================
-- আজকের টপিক: 
--   VIEW → জটিল কুয়েরি সহজ করা, পুনরায় ব্যবহারযোগ্য
--   INDEX → কুয়েরি স্পিড বাড়ানো
--   EXPLAIN → কুয়েরি অপটিমাইজেশন বুঝা
-- =============================================

USE my_portfolio;

-- =============================================
-- Section 1: পরীক্ষার জন্য ডাটা সেটআপ
-- =============================================

SELECT '--- SETTING UP TEST DATA ---' AS '';

-- ক্যাটাগরি টেবিল তৈরি (যদি না থাকে) — Day 5-এ তৈরি হতে পারে
CREATE TABLE IF NOT EXISTS expense_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    budget_limit DECIMAL(10,2) DEFAULT NULL
);

-- ক্যাটাগরি ডাটা
INSERT IGNORE INTO expense_categories (id, category_name, budget_limit) VALUES
(1, 'Housing', 1300.00),
(2, 'Food', 400.00),
(3, 'Transport', 100.00),
(4, 'Utilities', 150.00),
(5, 'Entertainment', 100.00),
(6, 'Income', NULL);

-- finance_log-এ category_id আপডেট
UPDATE finance_log SET category_id = 6 WHERE transaction_type = 'income';
UPDATE finance_log SET category_id = 1 WHERE description LIKE '%Rent%' OR description LIKE '%Apartment%';
UPDATE finance_log SET category_id = 2 WHERE description LIKE '%Food%' OR description LIKE '%Grocery%';
UPDATE finance_log SET category_id = 3 WHERE description LIKE '%Transport%';
UPDATE finance_log SET category_id = 4 WHERE description LIKE '%Electricity%' OR description LIKE '%Bill%';

SELECT * FROM expense_categories;

-- =============================================
-- Section 2: VIEW তৈরি করা (CREATE VIEW)
-- =============================================

SELECT '--- CREATING VIEW: view_all_transactions ---' AS '';

-- দৃষ্টিভঙ্গি: সব লেনদেন + ক্যাটাগরির নাম
CREATE OR REPLACE VIEW view_all_transactions AS
SELECT 
    f.transaction_id,
    f.description,
    f.amount,
    f.transaction_type,
    c.category_name,
    f.transaction_date
FROM finance_log f
LEFT JOIN expense_categories c ON f.category_id = c.id
ORDER BY f.transaction_date DESC;

-- VIEW ব্যবহার করা — যেকোনো SELECT-এর মতো
SELECT * FROM view_all_transactions;

-- =============================================
-- Section 3: মাসিক সারসংক্ষেপ VIEW
-- =============================================

SELECT '--- CREATING VIEW: view_monthly_summary ---' AS '';

CREATE OR REPLACE VIEW view_monthly_summary AS
SELECT 
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) AS net_savings,
    COUNT(*) AS transaction_count
FROM finance_log
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month DESC;

-- মাসিক সারসংক্ষেপ দেখা
SELECT '--- MONTHLY SUMMARY ---' AS '';
SELECT * FROM view_monthly_summary;

-- =============================================
-- Section 4: ক্যাটাগরি অনুযায়ী খরচের VIEW
-- =============================================

SELECT '--- CREATING VIEW: view_category_expenses ---' AS '';

CREATE OR REPLACE VIEW view_category_expenses AS
SELECT 
    c.category_name,
    COUNT(f.transaction_id) AS num_transactions,
    COALESCE(SUM(f.amount), 0) AS total_spent,
    c.budget_limit,
    CASE 
        WHEN c.budget_limit IS NULL THEN 'N/A'
        WHEN COALESCE(SUM(f.amount), 0) > c.budget_limit THEN 'Over Budget! ⚠️'
        ELSE 'Within Budget ✅'
    END AS budget_status
FROM expense_categories c
LEFT JOIN finance_log f ON c.id = f.category_id AND f.transaction_type = 'expense'
GROUP BY c.id, c.category_name, c.budget_limit
ORDER BY total_spent DESC;

SELECT * FROM view_category_expenses;

-- =============================================
-- Section 5: VIEW ব্যবহার করে জটিল রিপোর্ট
-- =============================================

SELECT '--- USING VIEWS FOR COMPLEX REPORTS ---' AS '';

-- VIEW-এর উপর আরেকটি কুয়েরি
SELECT * FROM view_monthly_summary
WHERE total_expense > 0;

-- VIEW + WHERE + ORDER BY
SELECT * FROM view_all_transactions
WHERE transaction_type = 'expense' AND amount > 100
ORDER BY amount DESC;

-- =============================================
-- Section 6: INDEXES — কুয়েরি স্পিড বাড়ানো
-- =============================================

SELECT '--- CREATING INDEXES ---' AS '';

-- transaction_date-এ INDEX (তারিখ দিয়ে সার্চ দ্রুত হয়)
CREATE INDEX idx_finance_date ON finance_log(transaction_date);

-- একাধিক কলামে কম্পোজিট INDEX
CREATE INDEX idx_finance_type_date ON finance_log(transaction_type, transaction_date);

-- ইউনিক INDEX (description + date যেন unique হয়)
-- CREATE UNIQUE INDEX idx_unique_entry ON finance_log(description, transaction_date);

SHOW INDEX FROM finance_log;

-- =============================================
-- Section 7: EXPLAIN — কুয়েরি অপটিমাইজেশন
-- =============================================

SELECT '--- EXPLAIN QUERY EXECUTION PLAN ---' AS '';

-- INDEX ছাড়া কুয়েরি এক্সপ্লেন
EXPLAIN SELECT * FROM finance_log WHERE transaction_date = '2026-06-01';

-- INDEX সহ কুয়েরি
EXPLAIN SELECT * FROM finance_log 
WHERE transaction_type = 'expense' 
  AND transaction_date BETWEEN '2026-06-01' AND '2026-06-30';

-- জয়েন সহ EXPLAIN
EXPLAIN SELECT * FROM view_all_transactions WHERE category_name = 'Food';

-- =============================================
-- Section 8: VIEW-এর তালিকা দেখা ও মুছে ফেলা
-- =============================================

SELECT '--- SHOWING ALL VIEWS ---' AS '';
SHOW FULL TABLES WHERE Table_Type = 'VIEW';

-- VIEW ড্রপ করা
-- DROP VIEW IF EXISTS view_all_transactions;
-- DROP VIEW IF EXISTS view_monthly_summary;
-- DROP VIEW IF EXISTS view_category_expenses;

-- =============================================
-- Section 9: INDEX ব্যবহারের বেস্ট প্র্যাকটিস
-- =============================================

/*
📌 INDEX কখন ব্যবহার করবেন:
  ✅ WHERE-এ ঘন ঘন ব্যবহার করা কলামে
  ✅ JOIN-এর ON কন্ডিশনে থাকা কলামে
  ✅ ORDER BY / GROUP BY-তে থাকা কলামে
  ✅ বড় টেবিলে (>১০,০০০ রো)

❌ INDEX কখন ব্যবহার করবেন না:
  ❌ ছোট টেবিলে (<১০০ রো)
  ❌ খুব কম পরিবর্তিত ভ্যালু (যেমন BOOLEAN)
  ❌ যে কলামে অনেক INSERT/UPDATE হয় (INDEX maintenance cost)

📊 তুলনা:
  WITH INDEX  → SELECT দ্রুত, কিন্তু INSERT/UPDATE ধীর
  WITHOUT INDEX → SELECT ধীর, কিন্তু INSERT/UPDATE দ্রুত
*/

SELECT '--- Day 11 Complete: Views & Indexes ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: 'view_high_expenses' নামে VIEW তৈরি করো
        যেখানে expense, amount > 100, তারিখ অনুযায়ী সাজানো

TASK 2: income_sources টেবিলের জন্য INDEX তৈরি করো
        earned_date কলামে

TASK 3: view_income_vs_expense নামে VIEW তৈরি করো
        যেখানে প্রতি মাসে income vs expense তুলনা

TASK 4: EXPLAIN ব্যবহার করে দেখাও কোন INDEX ব্যবহার হচ্ছে
        finance_log-এ transaction_date দিয়ে সার্চ করলে

TASK 5 (চ্যালেঞ্জ): 
        view_top_categories নামে VIEW বানাও
        যেখানে সবচেয়ে বেশি খরচের ক্যাটাগরি TOP 3 দেখায়
        (LIMIT 3 + ORDER BY total_spent DESC)

============================================
*/