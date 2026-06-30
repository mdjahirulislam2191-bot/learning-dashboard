-- =============================================
-- DAY 9: Constraints
-- (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, DEFAULT)
-- =============================================
-- Constraints enforce rules on data to maintain integrity.
-- We will review existing, add new ones, and alter tables.
-- =============================================

USE my_portfolio;

-- First, view current table structures
SELECT '--- CURRENT TABLE STRUCTURES ---' AS msg;
SHOW CREATE TABLE finance_log;
SHOW CREATE TABLE income_sources;
SHOW CREATE TABLE expense_categories;

-- =============================================
-- Section 1: Review existing constraints
-- =============================================

SELECT '--- 1. REVIEW EXISTING CONSTRAINTS ---' AS msg;

-- Check PRIMARY KEYs and indexes
SELECT 'Finance_log indexes:' AS msg;
SHOW INDEX FROM finance_log;

SELECT 'Income_sources indexes:' AS msg;
SHOW INDEX FROM income_sources;

SELECT 'Expense_categories indexes:' AS msg;
SHOW INDEX FROM expense_categories;

-- =============================================
-- Section 2: PRIMARY KEY constraint
-- =============================================
-- Ensures each row is uniquely identifiable.
-- AUTO_INCREMENT columns are usually PRIMARY KEYs.

SELECT '--- 2. PRIMARY KEY ---' AS msg;

-- These already exist, but let's ensure they are correct
-- Drop and re-add if needed (safe with IF NOT EXISTS)
ALTER TABLE finance_log MODIFY COLUMN transaction_id INT NOT NULL;
ALTER TABLE finance_log ADD PRIMARY KEY (transaction_id);

-- For income_sources
ALTER TABLE income_sources MODIFY COLUMN id INT NOT NULL;
ALTER TABLE income_sources ADD PRIMARY KEY (id);

-- For expense_categories
ALTER TABLE expense_categories MODIFY COLUMN id INT NOT NULL;
ALTER TABLE expense_categories ADD PRIMARY KEY (id);

SELECT 'Primary keys verified.' AS msg;

-- =============================================
-- Section 3: FOREIGN KEY constraint
-- =============================================
-- Ensures a column value exists in another table's PK.
-- Links finance_log.category_id -> expense_categories.id

SELECT '--- 3. FOREIGN KEY ---' AS msg;

-- First, ensure category_id column exists and has valid data
-- (category_id was added in Day 5)

-- Check current category_id values
SELECT 'Current category_id values:' AS msg;
SELECT DISTINCT category_id FROM finance_log WHERE category_id IS NOT NULL;

-- Add foreign key constraint (if not already present)
-- This ensures no one can set a category_id that doesn't exist
-- in expense_categories
ALTER TABLE finance_log
ADD CONSTRAINT fk_category
FOREIGN KEY (category_id) REFERENCES expense_categories(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

SELECT 'Foreign key added: finance_log.category_id -> expense_categories.id' AS msg;

-- Verify: try to insert an invalid category_id (should FAIL)
-- Uncomment the line below to test the constraint:
-- INSERT INTO finance_log (description, amount, transaction_type, transaction_date, category_id)
-- VALUES ('Test Invalid Category', 100.00, 'expense', '2026-07-10', 999);

SELECT 'Note: INSERT with invalid category_id (999) would fail.' AS msg;

-- =============================================
-- Section 4: UNIQUE constraint
-- =============================================
-- Ensures all values in a column (or column combination) are distinct

SELECT '--- 4. UNIQUE ---' AS msg;

-- Add UNIQUE to expense_categories.category_name
-- so we cannot have duplicate category names
ALTER TABLE expense_categories
ADD CONSTRAINT uq_category_name UNIQUE (category_name);

-- Test: try inserting a duplicate category (should FAIL)
-- Uncomment to test:
-- INSERT INTO expense_categories (category_name, budget_limit) VALUES ('Food', 500.00);

SELECT 'Unique constraint added on expense_categories.category_name' AS msg;

-- Add UNIQUE constraint on income_sources.source_name
ALTER TABLE income_sources
ADD CONSTRAINT uq_source_name UNIQUE (source_name);

SELECT 'Unique constraint added on income_sources.source_name' AS msg;

-- =============================================
-- Section 5: NOT NULL constraint
-- =============================================
-- Ensures a column cannot have NULL values

SELECT '--- 5. NOT NULL ---' AS msg;

-- Check which columns allow NULLs
SELECT 'Columns allowing NULL in finance_log:' AS msg;
SHOW COLUMNS FROM finance_log WHERE `Null` = 'YES';

SELECT 'Columns allowing NULL in income_sources:' AS msg;
SHOW COLUMNS FROM income_sources WHERE `Null` = 'YES';

-- Add NOT NULL to important columns that should always have data
ALTER TABLE finance_log MODIFY COLUMN description VARCHAR(255) NOT NULL;
ALTER TABLE finance_log MODIFY COLUMN amount DECIMAL(10,2) NOT NULL;
ALTER TABLE finance_log MODIFY COLUMN transaction_type VARCHAR(10) NOT NULL;
ALTER TABLE finance_log MODIFY COLUMN transaction_date DATE NOT NULL;

ALTER TABLE income_sources MODIFY COLUMN source_name VARCHAR(100) NOT NULL;
ALTER TABLE income_sources MODIFY COLUMN amount_cad DECIMAL(10,2) NOT NULL;

-- Add a phone column with NOT NULL to demonstrate adding a new column
-- (this is commented out - just for demonstration)
-- ALTER TABLE income_sources ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '';

SELECT 'NOT NULL constraints verified on key columns.' AS msg;

-- =============================================
-- Section 6: CHECK constraint (MySQL 8.0.16+)
-- =============================================
-- Ensures values meet a specific condition

SELECT '--- 6. CHECK ---' AS msg;

-- Ensure amount is always positive
ALTER TABLE finance_log
ADD CONSTRAINT chk_positive_amount CHECK (amount > 0);

SELECT 'Check constraint added: amount > 0 on finance_log' AS msg;

-- Ensure transaction_type is only 'income' or 'expense'
ALTER TABLE finance_log
ADD CONSTRAINT chk_valid_type CHECK (transaction_type IN ('income', 'expense'));

SELECT 'Check constraint added: transaction_type IN (income, expense)' AS msg;

-- Ensure budget_limit is positive in expense_categories
ALTER TABLE expense_categories
ADD CONSTRAINT chk_positive_budget CHECK (budget_limit > 0);

SELECT 'Check constraint added: budget_limit > 0 on expense_categories' AS msg;

-- Ensure amount_cad is positive in income_sources
ALTER TABLE income_sources
ADD CONSTRAINT chk_positive_income CHECK (amount_cad > 0);

SELECT 'Check constraint added: amount_cad > 0 on income_sources' AS msg;

-- =============================================
-- Section 7: DEFAULT constraint
-- =============================================
-- Provides a default value when none is specified

SELECT '--- 7. DEFAULT ---' AS msg;

-- Add DEFAULT to transaction_date (today's date)
ALTER TABLE finance_log
MODIFY COLUMN transaction_date DATE NOT NULL DEFAULT (CURRENT_DATE);

SELECT 'Default added: transaction_date = CURRENT_DATE' AS msg;

-- Add DEFAULT transaction_type as 'expense'
ALTER TABLE finance_log
MODIFY COLUMN transaction_type VARCHAR(10) NOT NULL DEFAULT 'expense';

SELECT 'Default added: transaction_type = expense' AS msg;

-- Demonstrate DEFAULT with an INSERT
INSERT INTO finance_log (description, amount)
VALUES ('Auto-date expense', 75.00);

SELECT 'Inserted with defaults (date = today, type = expense):' AS msg;
SELECT * FROM finance_log WHERE description = 'Auto-date expense';

-- =============================================
-- Section 8: Adding a new table with full constraints
-- =============================================

SELECT '--- 8. NEW TABLE WITH ALL CONSTRAINTS ---' AS msg;

-- Create a savings goals table with ALL constraint types
CREATE TABLE IF NOT EXISTS savings_goals (
    goal_id       INT AUTO_INCREMENT PRIMARY KEY,         -- PRIMARY KEY
    goal_name     VARCHAR(200) NOT NULL,                   -- NOT NULL
    target_amount DECIMAL(10,2) NOT NULL CHECK (target_amount > 0),  -- CHECK
    saved_so_far  DECIMAL(10,2) DEFAULT 0.00,             -- DEFAULT
    deadline_date DATE NOT NULL,                           -- NOT NULL
    priority      INT CHECK (priority BETWEEN 1 AND 5),   -- CHECK (range)
    source_id     INT,                                     -- For FOREIGN KEY
    CONSTRAINT uq_goal_name UNIQUE (goal_name),            -- UNIQUE
    CONSTRAINT fk_saving_source FOREIGN KEY (source_id)    -- FOREIGN KEY
        REFERENCES income_sources(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT chk_saved_not_over CHECK (saved_so_far <= target_amount) -- CHECK
);

SELECT 'Created savings_goals table with all constraint types.' AS msg;
DESCRIBE savings_goals;

-- Insert sample data
INSERT INTO savings_goals (goal_name, target_amount, saved_so_far, deadline_date, priority)
VALUES
('Emergency Fund',    5000.00, 1200.00, '2026-12-31', 1),
('CFA Exam Fee',      1000.00,  500.00, '2026-09-30', 2),
('Vacation Fund',     2000.00,    0.00, '2027-06-30', 3);

SELECT 'Sample data inserted:' AS msg;
SELECT * FROM savings_goals;

-- =============================================
-- Section 9: Dropping constraints (if needed)
-- =============================================

SELECT '--- 9. DROPPING CONSTRAINTS (reference only) ---' AS msg;

-- Examples of how to drop constraints (commented out - do not run)
/*
-- Drop a FOREIGN KEY
ALTER TABLE finance_log DROP FOREIGN KEY fk_category;

-- Drop a UNIQUE constraint
ALTER TABLE expense_categories DROP INDEX uq_category_name;

-- Drop a CHECK constraint
ALTER TABLE finance_log DROP CHECK chk_positive_amount;

-- Drop a DEFAULT (set to NULL)
ALTER TABLE finance_log ALTER COLUMN transaction_type DROP DEFAULT;
*/

SELECT 'See commented section for DROP CONSTRAINT syntax.' AS msg;

-- =============================================
-- Section 10: Show all constraints on all tables
-- =============================================

SELECT '--- 10. ALL CONSTRAINTS SUMMARY ---' AS msg;

-- Information schema query to view all constraints
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'my_portfolio'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- Check constraints with their definitions
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CHECK_CLAUSE
FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'my_portfolio';

/*
============================================
PRACTICE TASKS - Your turn!
============================================

TASK 1:
  Create a new table 'budget_plan' with:
  - plan_id (PRIMARY KEY, AUTO_INCREMENT)
  - plan_name (UNIQUE, NOT NULL)
  - monthly_limit (CHECK > 0, NOT NULL)
  - start_date (NOT NULL)
  - is_active (DEFAULT 'YES')

TASK 2:
  Add a FOREIGN KEY to savings_goals that references
  expense_categories(id). Call it fk_goal_category.

TASK 3:
  Add a CHECK constraint on income_sources to ensure
  amount_cad <= 100000 (no unrealistic income).

TASK 4 (Challenge):
  Try inserting a row that violates a constraint.
  (e.g., negative amount, duplicate category name, invalid type)
  Observe the error. Then rollback or fix it.

TASK 5 (Challenge):
  Create a table 'transaction_tags' with:
  - tag_id (PK)
  - tag_name (UNIQUE, NOT NULL)
  - created_at (DEFAULT CURRENT_DATE)
  Add a FOREIGN KEY in finance_log referencing transaction_tags.
  Note: You'll need to add a tag_id column to finance_log first.
============================================
*/