-- Day 3: Filtering (WHERE, LIKE, BETWEEN, IN)

USE my_portfolio;

-- View all records first
SELECT '--- ALL FINANCE LOG ---' AS '';
SELECT * FROM finance_log;

-- 1. WHERE: Filter by type
SELECT '--- ONLY EXPENSES ---' AS '';
SELECT * FROM finance_log 
WHERE transaction_type = 'expense';

-- 2. BETWEEN: Amount in a range
SELECT '--- AMOUNTS BETWEEN 250 AND 1500 ---' AS '';
SELECT * FROM finance_log 
WHERE amount BETWEEN 250.00 AND 1500.00;

-- 3. IN: Specific description values
SELECT '--- DESCRIPTION IN LIST ---' AS '';
SELECT * FROM finance_log 
WHERE description IN ('Apartment Rent', 'Monthly base pay');

-- 4. LIKE: Pattern matching (% is wildcard)
SELECT '--- CONTAINS "Rent" ---' AS '';
SELECT * FROM finance_log 
WHERE description LIKE '%Rent%';

-- 5. AND / OR logic
SELECT '--- INCOME OR EXPENSES < 300 ---' AS '';
SELECT * FROM finance_log 
WHERE transaction_type = 'income' 
   OR (transaction_type = 'expense' AND amount < 300);

-- Practice: Create more realistic data
INSERT INTO finance_log VALUES
(5, 'Freelance Data Work', 450.00, 'income', '2026-06-10'),
(6, 'Electricity Bill', 95.00, 'expense', '2026-06-08'),
(7, 'Transportation', 55.00, 'expense', '2026-06-07'),
(8, 'Food Delivery', 35.00, 'expense', '2026-06-09');

SELECT '--- ALL RECORDS (NEW) ---' AS '';
SELECT * FROM finance_log;