-- Day 2: CRUD Operations (Create, Read, Update, Delete)

USE my_portfolio;

-- CREATE a finance tracking table
CREATE TABLE IF NOT EXISTS finance_log (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    transaction_date DATE NOT NULL
);

-- INSERT records (create data)
INSERT INTO finance_log (description, amount, transaction_type, transaction_date)
VALUES 
('Monthly base pay', 4000.00, 'income', '2026-06-01'),
('Apartment Rent', 1200.00, 'expense', '2026-06-02'),
('Groceries bill', 250.50, 'expense', '2026-06-03'),
('Internet Bill', 75.00, 'expense', '2026-06-05');

-- READ: Show all records
SELECT '--- ALL RECORDS ---' AS '';
SELECT * FROM finance_log;

-- READ: Only descriptions and amounts
SELECT '--- DESCRIPTIONS & AMOUNTS ---' AS '';
SELECT description, amount FROM finance_log;

-- UPDATE: Correct the grocery amount
UPDATE finance_log 
SET amount = 280.00 
WHERE transaction_id = 3;

SELECT '--- AFTER UPDATE ---' AS '';
SELECT * FROM finance_log WHERE transaction_id = 3;

-- DELETE: Remove internet bill record
DELETE FROM finance_log 
WHERE transaction_id = 4;

SELECT '--- AFTER DELETE ---' AS '';
SELECT * FROM finance_log;

-- Practice task: Create a savings goal table
CREATE TABLE IF NOT EXISTS savings_goal (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    goal_name VARCHAR(200) NOT NULL,
    target_amount DECIMAL(10, 2) NOT NULL,
    saved_so_far DECIMAL(10, 2) DEFAULT 0.00,
    target_date DATE NOT NULL
);

-- Insert a goal (e.g. CFA exam fee)
INSERT INTO savings_goal (goal_name, target_amount, target_date)
VALUES ('CFA Exam Fee', 1000.00, '2026-12-31');

SELECT '--- SAVINGS GOALS ---' AS '';
SELECT * FROM savings_goal;