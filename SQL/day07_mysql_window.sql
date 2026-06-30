-- =============================================
-- DAY 7: Window Functions
-- (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG, SUM OVER)
-- =============================================
-- Window functions perform calculations across a set of rows
-- related to the current row WITHOUT collapsing them into groups.
-- =============================================

USE my_portfolio;

-- Ensure we have data
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

-- View data
SELECT '--- ALL FINANCE_LOG RECORDS ---' AS msg;
SELECT * FROM finance_log ORDER BY transaction_date;

-- =============================================
-- Section 1: ROW_NUMBER() - assign a unique number to each row
-- =============================================

SELECT '--- 1. ROW_NUMBER: Rank expenses by amount ---' AS msg;

SELECT
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
    description,
    amount,
    transaction_type,
    transaction_date
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY row_num;

-- ROW_NUMBER with PARTITION BY - reset numbering per transaction type
SELECT 'ROW_NUMBER within each type (partitioned):' AS msg;
SELECT
    ROW_NUMBER() OVER (PARTITION BY transaction_type ORDER BY amount DESC) AS rank_in_type,
    description,
    amount,
    transaction_type,
    transaction_date
FROM finance_log
ORDER BY transaction_type, rank_in_type;

-- =============================================
-- Section 2: RANK() and DENSE_RANK() - ties handling
-- =============================================

SELECT '--- 2. RANK vs DENSE_RANK ---' AS msg;

-- Insert a duplicate amount to show tie behavior
INSERT IGNORE INTO finance_log (transaction_id, description, amount, transaction_type, transaction_date)
VALUES (17, 'Duplicate Rent', 1200.00, 'expense', '2026-07-05');

SELECT
    description,
    amount,
    transaction_type,
    ROW_NUMBER()  OVER (ORDER BY amount DESC) AS row_num,
    RANK()        OVER (ORDER BY amount DESC) AS rnk,
    DENSE_RANK()  OVER (ORDER BY amount DESC) AS dense_rnk
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY amount DESC;

-- RANK and DENSE_RANK within each transaction type
SELECT 'RANK / DENSE_RANK partitioned by type:' AS msg;
SELECT
    description,
    amount,
    transaction_type,
    RANK()        OVER (PARTITION BY transaction_type ORDER BY amount DESC) AS rnk,
    DENSE_RANK()  OVER (PARTITION BY transaction_type ORDER BY amount DESC) AS dense_rnk
FROM finance_log
ORDER BY transaction_type, amount DESC;

-- =============================================
-- Section 3: LEAD() and LAG() - access next/previous rows
-- =============================================

SELECT '--- 3. LEAD and LAG ---' AS msg;

-- LAG: compare current expense with previous expense (by date)
SELECT
    transaction_date,
    description,
    amount,
    LAG(amount, 1) OVER (ORDER BY transaction_date) AS prev_expense,
    LAG(description, 1) OVER (ORDER BY transaction_date) AS prev_description,
    amount - LAG(amount, 1) OVER (ORDER BY transaction_date) AS difference_from_prev
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY transaction_date;

-- LEAD: what is the NEXT expense amount?
SELECT
    transaction_date,
    description,
    amount,
    LEAD(amount, 1) OVER (ORDER BY transaction_date) AS next_expense,
    LEAD(description, 1) OVER (ORDER BY transaction_date) AS next_description,
    LEAD(amount, 1) OVER (ORDER BY transaction_date) - amount AS diff_to_next
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY transaction_date;

-- LEAD with default value (if no next row, show 0)
SELECT 'LEAD with default value:' AS msg;
SELECT
    transaction_date,
    description,
    amount,
    LEAD(amount, 1, 0) OVER (ORDER BY transaction_date) AS next_expense
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY transaction_date;

-- LAG with partition - compare within same type only
SELECT 'LAG within each transaction type:' AS msg;
SELECT
    transaction_date,
    description,
    amount,
    transaction_type,
    LAG(amount, 1) OVER (
        PARTITION BY transaction_type
        ORDER BY transaction_date
    ) AS prev_amount_same_type
FROM finance_log
ORDER BY transaction_type, transaction_date;

-- =============================================
-- Section 4: Running Total with SUM() OVER()
-- =============================================

SELECT '--- 4. RUNNING TOTAL (SUM OVER) ---' AS msg;

-- Running total of expenses ordered by date
SELECT
    transaction_date,
    description,
    amount,
    SUM(amount) OVER (ORDER BY transaction_date) AS running_total_expenses
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY transaction_date;

-- Running total of ALL transactions (income + expense)
SELECT
    transaction_date,
    description,
    amount,
    transaction_type,
    SUM(amount) OVER (ORDER BY transaction_date) AS running_total
FROM finance_log
ORDER BY transaction_date;

-- Running total with type tracking
-- For expenses, subtract; for income, add
-- Using CASE to handle credit/debit style
SELECT
    transaction_date,
    description,
    CASE WHEN transaction_type = 'income'  THEN amount ELSE 0 END AS income_amt,
    CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END AS expense_amt,
    SUM(CASE WHEN transaction_type = 'income' THEN amount
             WHEN transaction_type = 'expense' THEN -amount
             ELSE 0 END
       ) OVER (ORDER BY transaction_date) AS net_running_balance
FROM finance_log
ORDER BY transaction_date;

-- SUM with PARTITION BY - running total within each type
SELECT 'Running total per transaction type:' AS msg;
SELECT
    transaction_date,
    description,
    amount,
    transaction_type,
    SUM(amount) OVER (
        PARTITION BY transaction_type
        ORDER BY transaction_date
    ) AS running_total_by_type
FROM finance_log
ORDER BY transaction_type, transaction_date;

-- =============================================
-- Section 5: Moving Average / Window Frame
-- =============================================

SELECT '--- 5. MOVING AVERAGE (3-row window) ---' AS msg;

-- 3-row moving average of expense amounts
SELECT
    transaction_date,
    description,
    amount,
    ROUND(AVG(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY transaction_date;

-- Running count - how many transactions so far
SELECT 'Running count of transactions:' AS msg;
SELECT
    transaction_date,
    description,
    amount,
    transaction_type,
    COUNT(*) OVER (ORDER BY transaction_date) AS txn_count_so_far
FROM finance_log
ORDER BY transaction_date;

-- =============================================
-- Section 6: FIRST_VALUE and LAST_VALUE
-- =============================================

SELECT '--- 6. FIRST_VALUE and LAST_VALUE ---' AS msg;

-- First expense and last expense in the ordered set
SELECT
    transaction_date,
    description,
    amount,
    FIRST_VALUE(description) OVER (ORDER BY amount DESC) AS highest_expense,
    FIRST_VALUE(amount) OVER (ORDER BY amount DESC) AS highest_amount,
    LAST_VALUE(description) OVER (
        ORDER BY amount DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_expense
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY amount DESC;

-- =============================================
-- Section 7: NTILE - divide into buckets
-- =============================================

SELECT '--- 7. NTILE (quartiles example) ---' AS msg;

-- Split expenses into 4 quartiles by amount
SELECT
    description,
    amount,
    NTILE(4) OVER (ORDER BY amount DESC) AS quartile
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY amount DESC;

-- Split into 3 groups (terciles)
SELECT
    description,
    amount,
    NTILE(3) OVER (ORDER BY amount DESC) AS expense_tier
FROM finance_log
WHERE transaction_type = 'expense'
ORDER BY amount DESC;

-- =============================================
-- Section 8: Window Functions on income_sources
-- =============================================

SELECT '--- 8. WINDOW FUNCTIONS ON income_sources ---' AS msg;

SELECT
    source_name,
    amount_cad,
    earned_date,
    ROW_NUMBER() OVER (ORDER BY amount_cad DESC) AS rank_by_amount,
    SUM(amount_cad) OVER (ORDER BY earned_date) AS running_total_income,
    ROUND(
        amount_cad / SUM(amount_cad) OVER () * 100,
        2
    ) AS pct_of_total
FROM income_sources
ORDER BY earned_date;

-- Remove the duplicate row we added
DELETE FROM finance_log WHERE transaction_id = 17;

/*
============================================
PRACTICE TASKS - Your turn!
============================================

TASK 1:
  Use ROW_NUMBER to find the 2nd highest expense.
  Hint: wrap in a subquery and filter WHERE row_num = 2.

TASK 2:
  For each expense, use LAG to calculate the day-to-day
  change in amount compared to the PREVIOUS expense by date.
  Show: date, description, amount, prev_amount, change.

TASK 3:
  Calculate a running total of income only (partitioned).
  Use SUM() OVER with PARTITION BY transaction_type = 'income'.

TASK 4 (Challenge):
  Use NTILE(2) to split expenses into "High" and "Low" groups.
  Show each expense with its group label (CASE WHEN ntile=1 THEN 'High' ELSE 'Low' END).

TASK 5 (Challenge):
  For income_sources, use LEAD to find the NEXT income amount
  and calculate the percentage change between consecutive incomes.
============================================
*/