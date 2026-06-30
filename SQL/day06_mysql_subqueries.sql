-- =============================================
-- DAY 6: Subqueries (subquery in WHERE, FROM, SELECT)
-- =============================================
-- A subquery is a query nested inside another query.
-- It can live in WHERE, FROM, or SELECT clause.
-- =============================================

USE my_portfolio;

-- Make sure we have enough data for meaningful subqueries
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

INSERT IGNORE INTO income_sources (id, source_name, amount_cad, earned_date)
VALUES
(3, 'Part-time Teaching',     800.00,  '2026-06-12'),
(4, 'Dividend Income',        200.00,  '2026-06-18'),
(5, 'Monthly Base Salary',    4000.00, '2026-07-01');

-- View current data
SELECT '--- CURRENT DATA ---' AS msg;
SELECT * FROM finance_log ORDER BY transaction_date;

-- =============================================
-- Section 1: Subquery in WHERE clause
-- =============================================
-- Find transactions with amount ABOVE the average expense

SELECT '--- 1. SUBQUERY IN WHERE ---' AS msg;

-- First, let's see what the average expense amount is
SELECT 'Average expense amount:' AS msg;
SELECT ROUND(AVG(amount), 2) AS avg_expense
FROM finance_log
WHERE transaction_type = 'expense';

-- Now: find all expenses that are higher than the average expense
SELECT 'Expenses above average:' AS msg;
SELECT description, amount, transaction_date
FROM finance_log
WHERE transaction_type = 'expense'
  AND amount > (
    SELECT AVG(amount)
    FROM finance_log
    WHERE transaction_type = 'expense'
  )
ORDER BY amount DESC;

-- Find income sources that are ABOVE the average income
SELECT 'Income above average income:' AS msg;
SELECT description, amount, transaction_date
FROM finance_log
WHERE transaction_type = 'income'
  AND amount > (
    SELECT AVG(amount)
    FROM finance_log
    WHERE transaction_type = 'income'
  )
ORDER BY amount DESC;

-- Find transactions with amount greater than the MAX expense
-- (useful to check if any income is smaller than the biggest expense)
SELECT 'Transactions > max expense (corner case check):' AS msg;
SELECT description, amount, transaction_type
FROM finance_log
WHERE amount > (
    SELECT MAX(amount)
    FROM finance_log
    WHERE transaction_type = 'expense'
);

-- =============================================
-- Section 2: Subquery in FROM clause (derived table)
-- =============================================
-- Use a subquery as a temporary table in FROM

SELECT '--- 2. SUBQUERY IN FROM (derived table) ---' AS msg;

-- Monthly summary using subquery in FROM
-- Total income, total expense, and net for each month
SELECT
    month_label,
    total_income,
    total_expense,
    (total_income - total_expense) AS net_savings
FROM (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month_label,
        SUM(CASE WHEN transaction_type = 'income'  THEN amount ELSE 0 END) AS total_income,
        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) AS total_expense
    FROM finance_log
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
) AS monthly_summary
ORDER BY month_label;

-- Top 3 largest transactions of each type using derived table
SELECT 'Top 3 incomes:' AS msg;
SELECT * FROM (
    SELECT description, amount, transaction_date
    FROM finance_log
    WHERE transaction_type = 'income'
    ORDER BY amount DESC
    LIMIT 3
) AS top_incomes;

SELECT 'Top 3 expenses:' AS msg;
SELECT * FROM (
    SELECT description, amount, transaction_date
    FROM finance_log
    WHERE transaction_type = 'expense'
    ORDER BY amount DESC
    LIMIT 3
) AS top_expenses;

-- Find income sources that earn MORE than the average income source
SELECT 'Income sources above average (FROM + income_sources):' AS msg;
SELECT source_name, amount_cad, earned_date
FROM income_sources
WHERE amount_cad > (
    SELECT AVG(amount_cad) FROM income_sources
)
ORDER BY amount_cad DESC;

-- =============================================
-- Section 3: Subquery in SELECT clause (scalar subquery)
-- =============================================
-- Use a subquery to add a computed column to every row

SELECT '--- 3. SUBQUERY IN SELECT ---' AS msg;

-- Show each expense with its % of total expenses
SELECT
    description,
    amount,
    transaction_date,
    ROUND(
        amount / (SELECT SUM(amount) FROM finance_log WHERE transaction_type = 'expense') * 100,
        2
    ) AS pct_of_total_expense
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY pct_of_total_expense DESC;

-- Show each income with its % of total income
SELECT
    description,
    amount,
    transaction_date,
    ROUND(
        amount / (SELECT SUM(amount) FROM finance_log WHERE transaction_type = 'income') * 100,
        2
    ) AS pct_of_total_income
FROM finance_log
WHERE transaction_type = 'income'
ORDER BY pct_of_total_income DESC;

-- Show each expense compared to the overall average (ALL transactions)
SELECT
    description,
    amount,
    (SELECT ROUND(AVG(amount), 2) FROM finance_log) AS overall_avg,
    ROUND(amount - (SELECT AVG(amount) FROM finance_log), 2) AS diff_from_avg
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY diff_from_avg DESC;

-- =============================================
-- Section 4: EXISTS and NOT EXISTS subqueries
-- =============================================

SELECT '--- 4. EXISTS / NOT EXISTS ---' AS msg;

-- Income sources that have matching records in finance_log
SELECT 'Income sources that appear in finance_log:' AS msg;
SELECT source_name, amount_cad
FROM income_sources i
WHERE EXISTS (
    SELECT 1
    FROM finance_log f
    WHERE f.description LIKE CONCAT('%', i.source_name, '%')
      AND f.amount = i.amount_cad
);

-- Income sources that do NOT appear in finance_log
SELECT 'Income sources NOT yet logged in finance_log:' AS msg;
SELECT source_name, amount_cad
FROM income_sources i
WHERE NOT EXISTS (
    SELECT 1
    FROM finance_log f
    WHERE f.description LIKE CONCAT('%', i.source_name, '%')
      AND f.amount = i.amount_cad
);

-- =============================================
-- Section 5: IN with subquery
-- =============================================

SELECT '--- 5. IN WITH SUBQUERY ---' AS msg;

-- Find finance_log records that match income_sources amounts
SELECT 'finance_log records matching income_sources amounts:' AS msg;
SELECT description, amount, transaction_type, transaction_date
FROM finance_log
WHERE amount IN (
    SELECT amount_cad FROM income_sources
)
ORDER BY amount DESC;

-- =============================================
-- Section 6: Nested subqueries (subquery inside subquery)
-- =============================================

SELECT '--- 6. NESTED SUBQUERIES ---' AS msg;

-- Find the transaction that has the highest amount among those
-- above the average (double nesting)
SELECT description, amount, transaction_type
FROM finance_log
WHERE amount = (
    SELECT MAX(amount)
    FROM finance_log
    WHERE amount > (
        SELECT AVG(amount)
        FROM finance_log
        WHERE transaction_type = 'expense'
    )
);

-- =============================================
-- Section 7: Subquery with JOIN
-- =============================================

SELECT '--- 7. SUBQUERY + JOIN ---' AS msg;

-- For each expense category, show its most expensive transaction
-- (using expense_categories table created in Day 5)
SELECT
    e.category_name,
    f.description,
    f.amount,
    f.transaction_date
FROM expense_categories e
INNER JOIN finance_log f ON f.category_id = e.id
WHERE f.amount = (
    SELECT MAX(f2.amount)
    FROM finance_log f2
    WHERE f2.category_id = e.id
)
ORDER BY f.amount DESC;

/*
============================================
PRACTICE TASKS - Your turn!
============================================

TASK 1:
  Find all expenses that are LESS than the average expense amount.
  Use a subquery in the WHERE clause.

TASK 2:
  Using a subquery in FROM, find the month that had the highest
  total expense amount.

TASK 3:
  Using a subquery in SELECT, show each income_sources entry with
  its percentage contribution to the grand total of all income_sources.

TASK 4 (Challenge):
  Find all transactions whose amount is within 10% of the average
  transaction amount. Use a subquery in WHERE.
  Hint: BETWEEN (avg * 0.9) AND (avg * 1.1)

TASK 5 (Challenge):
  Use a subquery to find income_sources that have a total matching
  finance_log amount (aggregated). Find income sources whose amount
  equals the SUM of some group of finance_log transactions.
============================================
*/