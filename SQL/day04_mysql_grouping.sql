-- Day 4: Sorting & Grouping (ORDER BY, GROUP BY, HAVING)

USE my_portfolio;

-- 1. ORDER BY: Sort data (ASC = small to big, DESC = big to small)
SELECT '--- SORTED BY AMOUNT DESC ---' AS '';
SELECT * FROM finance_log 
ORDER BY amount DESC;

SELECT '--- TOP 3 LARGEST TRANSACTIONS ---' AS '';
SELECT * FROM finance_log 
ORDER BY amount DESC 
LIMIT 3;

-- 2. Aggregate Functions
SELECT '--- AGGREGATE FUNCTIONS ---' AS '';
SELECT 
    COUNT(*) as total_transactions,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    MIN(amount) as minimum_amount,
    MAX(amount) as maximum_amount
FROM finance_log;

-- Income vs Expense aggregates
SELECT '--- INCOME VS EXPENSE ---' AS '';
SELECT 
    transaction_type,
    COUNT(*) as txn_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount
FROM finance_log
GROUP BY transaction_type;

-- 3. GROUP BY: Group transactions by type
SELECT '--- GROUPED BY TYPE ---' AS '';
SELECT 
    transaction_type, 
    COUNT(*) as txn_count, 
    SUM(amount) as total_amount,
    ROUND(AVG(amount), 2) as avg_amount
FROM finance_log 
GROUP BY transaction_type;

-- 4. HAVING: Filter AFTER grouping (WHERE filters BEFORE grouping)
SELECT '--- GROUPED WITH HAVING (total > 500) ---' AS '';
SELECT 
    transaction_type, 
    SUM(amount) as total_amount
FROM finance_log 
GROUP BY transaction_type
HAVING total_amount > 500.00;

-- 5. Combined example: Real analysis query
SELECT '--- COMBINED: ANALYZE INCOME ---' AS '';
SELECT 
    description,
    amount,
    transaction_date
FROM finance_log
WHERE transaction_type = 'income'
ORDER BY amount DESC
LIMIT 5;