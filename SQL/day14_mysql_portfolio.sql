-- =============================================
-- 📚 DAY 14 — Portfolio Project: Personal Finance DB
-- =============================================
-- আজকের টপিক: একটি সম্পূর্ণ Personal Finance Database
-- সবকিছু একসাথে — টেবিল, রিলেশন, VIEW, INDEX, PROCEDURE
-- =============================================
--
-- 🎯 প্রোজেক্ট: "MyFinance — Personal Finance Manager"
-- যাতে থাকবে:
--   ✅ Accounts (ব্যাংক, ক্যাশ, ক্রেডিট কার্ড)
--   ✅ Categories (আয়/খরচের ক্যাটাগরি)
--   ✅ Transactions (সব লেনদেন)
--   ✅ Budgets (মাসিক বাজেট)
--   ✅ Savings Goals (সঞ্চয় লক্ষ্য)
--   ✅ Reports (VIEW + PROCEDURE দিয়ে)
-- =============================================

USE my_portfolio;

-- =============================================
-- 🗑️ আগের কিছু ক্লিনআপ (নিরাপদে)
-- =============================================

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS pf_transactions;
DROP TABLE IF EXISTS pf_budgets;
DROP TABLE IF EXISTS pf_savings;
DROP TABLE IF EXISTS pf_accounts;
DROP TABLE IF EXISTS pf_categories;
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- Section 1: ACCOUNTS টেবিল
-- =============================================

CREATE TABLE pf_accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    account_type ENUM('Checking', 'Savings', 'Credit Card', 'Cash', 'Investment') NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'CAD',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO pf_accounts (account_name, account_type, balance) VALUES
('TD Bank Checking', 'Checking', 3200.00),
('RBC Savings', 'Savings', 5000.00),
('TD Credit Card', 'Credit Card', -450.00),
('Cash Wallet', 'Cash', 200.00);

SELECT '--- ✅ ACCOUNTS CREATED ---' AS '';
SELECT * FROM pf_accounts;

-- =============================================
-- Section 2: CATEGORIES টেবিল
-- =============================================

CREATE TABLE pf_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_type ENUM('Income', 'Expense', 'Transfer') NOT NULL,
    icon VARCHAR(20) DEFAULT '📁',
    parent_category_id INT DEFAULT NULL,
    FOREIGN KEY (parent_category_id) REFERENCES pf_categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB;

INSERT INTO pf_categories (category_name, category_type, icon) VALUES
-- Income categories
('Salary', 'Income', '💰'),
('Freelance', 'Income', '💼'),
('Investment', 'Income', '📈'),
('Gift', 'Income', '🎁'),
('Other Income', 'Income', '💵'),
-- Expense categories
('Housing', 'Expense', '🏠'),
('Food & Dining', 'Expense', '🍕'),
('Transportation', 'Expense', '🚗'),
('Utilities', 'Expense', '💡'),
('Entertainment', 'Expense', '🎬'),
('Healthcare', 'Expense', '🏥'),
('Education', 'Expense', '📚'),
('Shopping', 'Expense', '🛍️'),
('Personal Care', 'Expense', '🧴'),
('Other Expense', 'Expense', '📦');

SELECT '--- ✅ CATEGORIES CREATED ---' AS '';
SELECT * FROM pf_categories;

-- =============================================
-- Section 3: TRANSACTIONS টেবিল
-- =============================================

CREATE TABLE pf_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    category_id INT,
    transaction_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_type ENUM('Income', 'Expense', 'Transfer') NOT NULL,
    description VARCHAR(255),
    notes TEXT,
    is_recurring BOOLEAN DEFAULT FALSE,
    receipt_path VARCHAR(500) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES pf_accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES pf_categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Indexes for performance
CREATE INDEX idx_pf_trans_date ON pf_transactions(transaction_date);
CREATE INDEX idx_pf_trans_account ON pf_transactions(account_id);
CREATE INDEX idx_pf_trans_category ON pf_transactions(category_id);

-- Sample transactions
INSERT INTO pf_transactions (account_id, category_id, transaction_date, amount, transaction_type, description) VALUES
-- June income
(1, 1, '2026-06-01', 4000.00, 'Income', 'Monthly Salary - Tech Corp'),
(1, 2, '2026-06-10', 450.00, 'Income', 'Freelance Data Analysis'),
(2, 3, '2026-06-15', 150.00, 'Income', 'Dividend Payment'),
-- June expenses
(1, 6, '2026-06-02', 1200.00, 'Expense', 'Apartment Rent'),
(1, 7, '2026-06-03', 280.00, 'Expense', 'Monthly Groceries'),
(3, 7, '2026-06-09', 35.00, 'Expense', 'Food Delivery'),
(1, 9, '2026-06-05', 95.00, 'Expense', 'Electricity Bill'),
(1, 9, '2026-06-06', 65.00, 'Expense', 'Internet Bill'),
(1, 8, '2026-06-07', 55.00, 'Expense', 'Gas'),
(3, 10, '2026-06-12', 25.00, 'Expense', 'Netflix Subscription'),
(1, 11, '2026-06-14', 80.00, 'Expense', 'Pharmacy - Vitamins'),
-- July
(1, 6, '2026-07-01', 1200.00, 'Expense', 'July Rent'),
(1, 7, '2026-07-02', 150.00, 'Expense', 'Weekly Groceries'),
(1, 1, '2026-07-01', 4000.00, 'Income', 'July Salary');

SELECT '--- ✅ TRANSACTIONS CREATED ---' AS '';
SELECT COUNT(*) AS total_transactions FROM pf_transactions;

-- =============================================
-- Section 4: BUDGETS টেবিল
-- =============================================

CREATE TABLE pf_budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    month DATE NOT NULL,  -- Use first day of month: '2026-06-01'
    budget_amount DECIMAL(12,2) NOT NULL,
    spent_amount DECIMAL(12,2) DEFAULT 0.00,
    warning_threshold DECIMAL(5,2) DEFAULT 80.00,  -- % at which to warn
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES pf_categories(category_id) ON DELETE CASCADE,
    UNIQUE KEY unique_budget (category_id, month)
) ENGINE=InnoDB;

-- June budgets
INSERT INTO pf_budgets (category_id, month, budget_amount) VALUES
(6, '2026-06-01', 1300.00),   -- Housing
(7, '2026-06-01', 400.00),    -- Food
(8, '2026-06-01', 100.00),    -- Transport
(9, '2026-06-01', 150.00),    -- Utilities
(10, '2026-06-01', 100.00),   -- Entertainment
(11, '2026-06-01', 200.00),   -- Healthcare
(12, '2026-06-01', 300.00),   -- Education
(13, '2026-06-01', 200.00);   -- Shopping

-- Update spent amounts (calculated from transactions)
UPDATE pf_budgets b
JOIN (
    SELECT category_id, SUM(amount) AS total_spent
    FROM pf_transactions
    WHERE transaction_type = 'Expense'
      AND MONTH(transaction_date) = 6
      AND YEAR(transaction_date) = 2026
    GROUP BY category_id
) t ON b.category_id = t.category_id
SET b.spent_amount = COALESCE(t.total_spent, 0)
WHERE MONTH(b.month) = 6 AND YEAR(b.month) = 2026;

SELECT '--- ✅ BUDGETS CREATED ---' AS '';
SELECT * FROM pf_budgets;

-- =============================================
-- Section 5: SAVINGS GOALS টেবিল (আপগ্রেডেড)
-- =============================================

CREATE TABLE pf_savings (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    goal_name VARCHAR(200) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    saved_amount DECIMAL(12,2) DEFAULT 0.00,
    target_date DATE,
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    notes TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO pf_savings (goal_name, target_amount, saved_amount, target_date, priority) VALUES
('Emergency Fund', 10000.00, 5000.00, '2026-12-31', 'High'),
('CFA Exam Fee', 1000.00, 0.00, '2026-10-31', 'High'),
('New Laptop', 2500.00, 800.00, '2026-09-30', 'Medium'),
('Vacation Fund', 2000.00, 300.00, '2026-12-31', 'Low');

SELECT '--- ✅ SAVINGS GOALS CREATED ---' AS '';
SELECT * FROM pf_savings;

-- =============================================
-- Section 6: VIEWS — রিপোর্টের জন্য
-- =============================================

SELECT '--- CREATING VIEWS ---' AS '';

-- মাসিক সারসংক্ষেপ VIEW
CREATE OR REPLACE VIEW pf_view_monthly_summary AS
SELECT 
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE -amount END) AS net_flow,
    COUNT(*) AS transaction_count
FROM pf_transactions
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month DESC;

-- ক্যাটাগরি অনুযায়ী খরচের VIEW
CREATE OR REPLACE VIEW pf_view_category_spending AS
SELECT 
    c.category_name,
    c.icon,
    COALESCE(SUM(t.amount), 0) AS total_spent,
    COUNT(*) AS num_transactions,
    b.budget_amount,
    CASE 
        WHEN b.budget_amount IS NULL THEN 'No Budget Set'
        WHEN COALESCE(SUM(t.amount), 0) > b.budget_amount THEN 'Over Budget! ❌'
        ELSE 'On Track ✅'
    END AS status
FROM pf_categories c
LEFT JOIN pf_transactions t ON c.category_id = t.category_id 
    AND t.transaction_type = 'Expense'
LEFT JOIN pf_budgets b ON c.category_id = b.category_id 
    AND MONTH(b.month) = MONTH(CURDATE())
    AND YEAR(b.month) = YEAR(CURDATE())
WHERE c.category_type = 'Expense'
GROUP BY c.category_id, c.category_name, c.icon, b.budget_amount
ORDER BY total_spent DESC;

-- অ্যাকাউন্ট ব্যালেন্স VIEW
CREATE OR REPLACE VIEW pf_view_account_balances AS
SELECT 
    account_name,
    account_type,
    balance,
    CASE 
        WHEN balance > 0 AND account_type IN ('Credit Card') THEN 'Good ✅'
        WHEN balance < 0 AND account_type IN ('Credit Card') THEN 'Balance Due ⚠️'
        ELSE 'Active'
    END AS status
FROM pf_accounts
WHERE is_active = TRUE;

SELECT '--- VIEWS CREATED ---' AS '';

-- =============================================
-- Section 7: PROCEDURES — দৈনন্দিন কাজের জন্য
-- =============================================

SELECT '--- CREATING PROCEDURES ---' AS '';

DELIMITER $$

-- নতুন লেনদেন যোগ করার Procedure
CREATE PROCEDURE IF NOT EXISTS pf_add_transaction(
    IN p_account_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(12,2),
    IN p_type ENUM('Income', 'Expense', 'Transfer'),
    IN p_description VARCHAR(255),
    IN p_notes TEXT
)
BEGIN
    DECLARE v_transaction_id INT;
    
    INSERT INTO pf_transactions 
        (account_id, category_id, transaction_date, amount, transaction_type, description, notes)
    VALUES 
        (p_account_id, p_category_id, CURDATE(), p_amount, p_type, p_description, p_notes);
    
    SET v_transaction_id = LAST_INSERT_ID();
    
    -- অ্যাকাউন্ট ব্যালেন্স আপডেট
    IF p_type = 'Income' THEN
        UPDATE pf_accounts SET balance = balance + p_amount WHERE account_id = p_account_id;
    ELSEIF p_type = 'Expense' THEN
        UPDATE pf_accounts SET balance = balance - p_amount WHERE account_id = p_account_id;
    END IF;
    
    SELECT CONCAT('✅ Transaction #', v_transaction_id, ' added. Account updated.') AS result;
END$$

-- মাসিক রিপোর্ট Procedure
CREATE PROCEDURE IF NOT EXISTS pf_monthly_report(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT CONCAT('📊 Report: ', p_year, '-', LPAD(p_month, 2, '0')) AS title;
    
    -- Headline numbers
    SELECT 
        (SELECT COALESCE(SUM(amount), 0) FROM pf_transactions 
         WHERE transaction_type = 'Income' AND YEAR(transaction_date)=p_year AND MONTH(transaction_date)=p_month) AS income,
        (SELECT COALESCE(SUM(amount), 0) FROM pf_transactions 
         WHERE transaction_type = 'Expense' AND YEAR(transaction_date)=p_year AND MONTH(transaction_date)=p_month) AS expenses,
        (SELECT COALESCE(SUM(CASE WHEN transaction_type='Income' THEN amount ELSE -amount END), 0) FROM pf_transactions 
         WHERE YEAR(transaction_date)=p_year AND MONTH(transaction_date)=p_month) AS net_savings;
    
    -- Top 5 expenses
    SELECT c.category_name, SUM(t.amount) AS total
    FROM pf_transactions t
    JOIN pf_categories c ON t.category_id = c.category_id
    WHERE t.transaction_type = 'Expense'
      AND YEAR(t.transaction_date) = p_year
      AND MONTH(t.transaction_date) = p_month
    GROUP BY c.category_name
    ORDER BY total DESC
    LIMIT 5;
END$$

DELIMITER ;

SELECT '--- PROCEDURES CREATED ---' AS '';

-- =============================================
-- Section 8: ডেমো — সবকিছু একসাথে
-- =============================================

SELECT '--- 🚀 DEMO: USING THE PORTFOLIO ---' AS '';

-- 1. সব অ্যাকাউন্ট দেখা
SELECT '=== ACCOUNT BALANCES ===' AS '';
SELECT * FROM pf_view_account_balances;

-- 2. মাসিক সারসংক্ষেপ
SELECT '=== MONTHLY SUMMARY ===' AS '';
SELECT * FROM pf_view_monthly_summary;

-- 3. ক্যাটাগরি অনুযায়ী খরচ
SELECT '=== CATEGORY SPENDING ===' AS '';
SELECT * FROM pf_view_category_spending;

-- 4. সেভিংস গোল
SELECT '=== SAVINGS GOALS ===' AS '';
SELECT * FROM pf_savings;

-- 5. নতুন লেনদেন যোগ (Procedure দিয়ে)
SELECT '=== ADDING NEW TRANSACTION ===' AS '';
CALL pf_add_transaction(4, 7, 35.50, 'Expense', 'Coffee & Snacks', 'Starbucks treat');

-- 6. মাসিক রিপোর্ট
SELECT '=== MONTHLY REPORT ===' AS '';
CALL pf_monthly_report(2026, 6);

-- =============================================
-- 🧠 স্কিমা ডায়াগ্রাম (টেক্সট ভিজুয়ালাইজেশন)
-- =============================================

/*
📊 pf_accounts ──┐
                 ├── pf_transactions ──┐
📊 pf_categories ─┘                     │
                                        │
📊 pf_budgets ───── category_id ────────┘

📊 pf_savings (independent)

Foreign Keys:
  pf_transactions.account_id  → pf_accounts.account_id
  pf_transactions.category_id → pf_categories.category_id
  pf_budgets.category_id      → pf_categories.category_id
  pf_categories.parent_category_id → pf_categories.category_id
*/

SELECT '--- Day 14 Complete: Portfolio Project ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: pf_accounts-এ 'credit_limit' কলাম যোগ করো
        (Credit Card type-এর জন্য DECIMAL(12,2))

TASK 2: pf_view_top_savings নামে VIEW বানাও
        priority = 'High' বা 'Critical' গোলগুলো দেখায়

TASK 3: pf_transfer_money নামে Procedure বানাও
        যা এক অ্যাকাউন্ট থেকে অন্য অ্যাকাউন্টে টাকা সরায়
        (একটায় debits, অন্যটায় credits)

TASK 4: pf_budgets টেবিলের জন্য 'remaining_percent' কলাম যোগ করো
        ও percent complete হিসাব করার VIEW বানাও

TASK 5 (চ্যালেঞ্জ):
        pf_view_dashboard নামে একটি VIEW বানাও
        যা এক লাইনে সব গুরুত্বপূর্ণ সংখ্যা দেখায়:
        - Total Balance (all accounts)
        - This Month Income
        - This Month Expense
        - Total Saved (savings goals)
        - Budget Utilization %
============================================
*/