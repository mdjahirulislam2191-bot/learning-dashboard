-- =============================================
-- DAY 8: Common Table Expressions (CTEs)
-- =============================================
-- CTEs (WITH clause) let you define named temporary
-- result sets that you can reference inside the main query.
-- They make complex queries cleaner, more readable, and reusable.
-- =============================================

USE my_portfolio;

-- Ensure data exists
INSERT IGNORE INTO finance_log (transaction_id, description, amount, transaction_type, transaction_date)
VALUES
(9,  'Part-time Teaching',    800.00,  'income',  '2026-06-12'),
(10, 'Phone Bill',            45.00,   'expense', '2026-06-11'),
(11, 'Gym Membership',        60.00,   'expense', '2026-06-13'),
(12, 'Eating Out',            120.00,  'expense', '2026-06-14'),
(13, 'Dividend Income',       200.00,  'income',  '2026-06-18'),
(14, 'Monthly Base Salary',   4000.00, 'income',  '2026-07-01'),
(15, 'Office Rent',           1100.00, 'expense', '2026-07-02'),
(16, 'Groceries',             320.00,  'expense', '2026-07-03');

SELECT '--- CURRENT DATA ---' AS msg;
SELECT * FROM finance_log ORDER BY transaction_date;

-- =============================================
-- Section 1: Simple CTE - Monthly Summary
-- =============================================

SELECT '--- 1. SIMPLE CTE: Monthly Summary ---' AS msg;

-- CTE to compute monthly income and expense totals
WITH monthly_summary AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month_label,
        SUM(CASE WHEN transaction_type = 'income'  THEN amount ELSE 0 END) AS total_income,
        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) AS total_expense,
        COUNT(*) AS txn_count
    FROM finance_log
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
)
SELECT
    month_label,
    total_income,
    total_expense,
    (total_income - total_expense) AS net_savings,
    ROUND(
        (total_income - total_expense) / total_income * 100,
        2
    ) AS savings_rate_pct,
    txn_count
FROM monthly_summary
ORDER BY month_label;

-- =============================================
-- Section 2: CTE to calculate monthly savings rate
-- =============================================

SELECT '--- 2. MONTHLY SAVINGS RATE ---' AS msg;

-- Step 1: Aggregate income and expense per month
WITH monthly_data AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month_label,
        SUM(CASE WHEN transaction_type = 'income'  THEN amount ELSE 0 END) AS income,
        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) AS expense
    FROM finance_log
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
)
-- Step 2: Calculate savings rate
SELECT
    month_label,
    income,
    expense,
    (income - expense) AS savings,
    ROUND(
        (income - expense) / income * 100,
        2
    ) AS savings_rate_pct,
    CASE
        WHEN (income - expense) / income >= 0.20 THEN 'Excellent'
        WHEN (income - expense) / income >= 0.10 THEN 'Good'
        WHEN (income - expense) / income >= 0.00 THEN 'Needs Improvement'
        ELSE 'Overspending!'
    END AS financial_health
FROM monthly_data
ORDER BY month_label;

-- =============================================
-- Section 3: Multiple CTEs (comma-separated)
-- =============================================

SELECT '--- 3. MULTIPLE CTEs ---' AS msg;

WITH
expense_summary AS (
    SELECT
        transaction_type,
        COUNT(*) AS txn_count,
        SUM(amount) AS total_amount,
        ROUND(AVG(amount), 2) AS avg_amount,
        MAX(amount) AS max_amount,
        MIN(amount) AS min_amount
    FROM finance_log
    WHERE transaction_type = 'expense'
    GROUP BY transaction_type
),
income_summary AS (
    SELECT
        transaction_type,
        COUNT(*) AS txn_count,
        SUM(amount) AS total_amount,
        ROUND(AVG(amount), 2) AS avg_amount,
        MAX(amount) AS max_amount,
        MIN(amount) AS min_amount
    FROM finance_log
    WHERE transaction_type = 'income'
    GROUP BY transaction_type
)
SELECT '--- EXPENSE SUMMARY ---' AS msg, * FROM expense_summary
UNION ALL
SELECT '--- INCOME SUMMARY ---', * FROM income_summary;

-- =============================================
-- Section 4: CTE with JOIN between CTEs
-- =============================================

SELECT '--- 4. CTE + CTE JOIN ---' AS msg;

WITH
monthly_income AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month_label,
        SUM(amount) AS income_total
    FROM finance_log
    WHERE transaction_type = 'income'
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
),
monthly_expense AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month_label,
        SUM(amount) AS expense_total
    FROM finance_log
    WHERE transaction_type = 'expense'
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
)
SELECT
    i.month_label,
    i.income_total,
    e.expense_total,
    (i.income_total - e.expense_total) AS net,
    ROUND((i.income_total - e.expense_total) / i.income_total * 100, 2) AS savings_pct
FROM monthly_income i
LEFT JOIN monthly_expense e ON i.month_label = e.month_label
ORDER BY i.month_label;

-- =============================================
-- Section 5: CTE used in multiple places
-- =============================================

SELECT '--- 5. CTE USED MULTIPLE TIMES ---' AS msg;

WITH high_value_txns AS (
    SELECT *
    FROM finance_log
    WHERE amount > 500
)
SELECT 'High value expenses:', COUNT(*), SUM(amount)
FROM high_value_txns
WHERE transaction_type = 'expense';

SELECT 'High value income:', COUNT(*), SUM(amount)
FROM high_value_txns
WHERE transaction_type = 'income';

-- =============================================
-- Section 6: CTE with Window Functions
-- =============================================

SELECT '--- 6. CTE + WINDOW FUNCTIONS ---' AS msg;

WITH ranked_expenses AS (
    SELECT
        description,
        amount,
        transaction_date,
        ROW_NUMBER() OVER (ORDER BY amount DESC) AS rn,
        RANK()       OVER (ORDER BY amount DESC) AS rnk,
        DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_rnk
    FROM finance_log
    WHERE transaction_type = 'expense'
)
SELECT description, amount, transaction_date, rn
FROM ranked_expenses
WHERE rn <= 3
ORDER BY rn;

-- =============================================
-- Section 7: CTE with income_sources
-- =============================================

SELECT '--- 7. CTE WITH income_sources ---' AS msg;

WITH income_analysis AS (
    SELECT
        source_name,
        amount_cad,
        earned_date,
        ROW_NUMBER() OVER (ORDER BY amount_cad DESC) AS income_rank,
        SUM(amount_cad) OVER () AS grand_total,
        ROUND(amount_cad / SUM(amount_cad) OVER () * 100, 2) AS pct_share
    FROM income_sources
)
SELECT
    source_name,
    amount_cad,
    earned_date,
    income_rank,
    pct_share || '%' AS share_pct
FROM income_analysis
ORDER BY income_rank;

-- =============================================
-- Section 8: Recursive CTE (advanced)
-- =============================================

SELECT '--- 8. RECURSIVE CTE (date range generator) ---' AS msg;

-- Generate a sequence of dates for the month of June 2026
-- Useful for filling gaps in date-based analysis
WITH RECURSIVE date_series AS (
    -- Anchor: start date
    SELECT DATE('2026-06-01') AS dt
    UNION ALL
    -- Recursive: add 1 day each iteration
    SELECT dt + INTERVAL 1 DAY
    FROM date_series
    WHERE dt < '2026-06-30'
)
SELECT
    ds.dt,
    COUNT(f.transaction_id) AS txn_count,
    COALESCE(SUM(f.amount), 0) AS total_amount
FROM date_series ds
LEFT JOIN finance_log f ON f.transaction_date = ds.dt
GROUP BY ds.dt
ORDER BY ds.dt;

-- =============================================
-- Section 9: Real-world portfolio analysis
-- =============================================

SELECT '--- 9. PORTFOLIO ANALYSIS ---' AS msg;

WITH
-- Step 1: Get all income sources
all_income AS (
    SELECT source_name AS item, amount_cad AS amt, earned_date AS dt, 'income' AS src
    FROM income_sources
),
-- Step 2: Get all transactions
all_txns AS (
    SELECT description AS item, amount AS amt, transaction_date AS dt, transaction_type AS src
    FROM finance_log
),
-- Step 3: Combine them
combined AS (
    SELECT * FROM all_income
    UNION ALL
    SELECT * FROM all_txns
),
-- Step 4: Summarize by source
source_summary AS (
    SELECT
        CASE WHEN src = 'income' THEN 'Income Sources'
             WHEN src = 'expense' THEN 'Expenses'
             ELSE src
        END AS category,
        COUNT(*) AS entries,
        SUM(amt) AS total_amount
    FROM combined
    GROUP BY src
)
SELECT
    category,
    entries,
    total_amount,
    ROUND(total_amount / SUM(total_amount) OVER () * 100, 2) AS share_pct
FROM source_summary
ORDER BY total_amount DESC;

-- =============================================
-- Section 10: CTE with subquery alternative comparison
-- =============================================

SELECT '--- 10. CTE vs SUBQUERY comparison ---' AS msg;

-- Same result: find transactions above average
-- Method A: Subquery (from Day 6)
SELECT description, amount
FROM finance_log
WHERE transaction_type = 'expense'
  AND amount > (SELECT AVG(amount) FROM finance_log WHERE transaction_type = 'expense');

-- Method B: CTE (cleaner for complex queries)
WITH avg_expense AS (
    SELECT AVG(amount) AS avg_amt
    FROM finance_log
    WHERE transaction_type = 'expense'
)
SELECT f.description, f.amount
FROM finance_log f, avg_expense a
WHERE f.transaction_type = 'expense'
  AND f.amount > a.avg_amt;

/*
============================================
PRACTICE TASKS - Your turn!
============================================

TASK 1:
  Create a CTE called 'large_expenses' that selects all expenses
  with amount > 100. Then query the CTE to find the total and average.

TASK 2:
  Using multiple CTEs, calculate:
  - The month with the highest income
  - The month with the highest expense
  Then JOIN the CTEs to compare them side by side.

TASK 3:
  Write a CTE that ranks income_sources by amount_cad descending.
  Use ROW_NUMBER in the CTE, then select only the top 2 sources.

TASK 4 (Challenge):
  Use a recursive CTE to generate a series of numbers from 1 to 20.
  Then label each number as 'Even' or 'Odd' in the final SELECT.

TASK 5 (Challenge):
  Create a CTE that calculates the running total of expenses.
  Then use ANOTHER CTE to find the point where running total
  exceeds 2000 for the first time.
============================================
*/