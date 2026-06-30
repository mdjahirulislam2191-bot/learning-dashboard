-- =============================================
-- 📚 DAY 12 — Stored Procedures
-- =============================================
-- আজকের টপিক: 
--   CREATE PROCEDURE → পুনরায় ব্যবহারযোগ্য SQL ব্লক
--   Parameters → IN, OUT, INOUT
--   Variables → DECLARE, SET
--   Control Flow → IF-ELSE, CASE
-- =============================================

USE my_portfolio;

-- =============================================
-- Section 1: সহজ Procedure — সব লেনদেন দেখা
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_get_all_transactions ---' AS '';

-- ডেলিমিটার পরিবর্তন (; এর পরিবর্তে $$ ব্যবহার)
DELIMITER $$

-- সব লেনদেন দেখানোর জন্য সহজ procedure
CREATE PROCEDURE IF NOT EXISTS sp_get_all_transactions()
BEGIN
    SELECT * FROM finance_log ORDER BY transaction_date DESC;
END$$

DELIMITER ;

-- Procedure কল করা
CALL sp_get_all_transactions();

-- =============================================
-- Section 2: IN Parameter — নির্দিষ্ট টাইপের লেনদেন
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_get_by_type ---' AS '';

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_get_by_type(
    IN p_type VARCHAR(10)  -- 'income' অথবা 'expense'
)
BEGIN
    SELECT * FROM finance_log 
    WHERE transaction_type = p_type
    ORDER BY transaction_date DESC;
END$$

DELIMITER ;

-- কল করা: শুধু expense দেখাও
CALL sp_get_by_type('expense');

-- কল করা: শুধু income দেখাও
CALL sp_get_by_type('income');

-- =============================================
-- Section 3: Procedure — নতুন expense যোগ করা (sp_add_expense)
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_add_expense ---' AS '';

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_add_expense(
    IN p_description VARCHAR(255),
    IN p_amount DECIMAL(10,2),
    IN p_category_id INT,
    IN p_notes VARCHAR(500)
)
BEGIN
    -- ভেরিয়েবল ডিক্লেয়ার
    DECLARE v_new_id INT;
    DECLARE v_current_balance DECIMAL(12,2);
    
    -- নতুন expense যোগ করা
    INSERT INTO finance_log (description, amount, transaction_type, transaction_date, category_id)
    VALUES (p_description, p_amount, 'expense', CURDATE(), p_category_id);
    
    -- শেষ INSERT-এর ID পাওয়া
    SET v_new_id = LAST_INSERT_ID();
    
    -- কনফার্মেশন মেসেজ
    SELECT CONCAT('✅ Expense added! ID: ', v_new_id, ', Description: ', p_description) AS result;
END$$

DELIMITER ;

-- নতুন expense যোগ করা
CALL sp_add_expense('Monthly Internet Bill', 65.00, 4, 'Rogers internet June');
CALL sp_add_expense('Dinner Out', 45.00, 5, 'Team dinner');

-- চেক করা
SELECT '--- NEW EXPENSES ADDED ---' AS '';
SELECT * FROM finance_log ORDER BY transaction_id DESC LIMIT 5;

-- =============================================
-- Section 4: Procedure — আয় যোগ করা (sp_add_income)
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_add_income ---' AS '';

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_add_income(
    IN p_description VARCHAR(255),
    IN p_amount DECIMAL(10,2),
    IN p_source_name VARCHAR(100)
)
BEGIN
    DECLARE v_new_id INT;
    
    -- finance_log-এ আয় যোগ করা
    INSERT INTO finance_log (description, amount, transaction_type, transaction_date, category_id)
    VALUES (p_description, p_amount, 'income', CURDATE(), 6);
    
    SET v_new_id = LAST_INSERT_ID();
    
    -- income_sources-এ ও যোগ করা (ঐচ্ছিক)
    INSERT INTO income_sources (source_name, amount_cad, earned_date)
    VALUES (p_source_name, p_amount, CURDATE());
    
    SELECT CONCAT('✅ Income added! Log ID: ', v_new_id, ', Source: ', p_source_name) AS result;
END$$

DELIMITER ;

-- নতুন আয় যোগ করা
CALL sp_add_income('Freelance Project Payment', 750.00, 'Upwork Project Alpha');

-- চেক করা
SELECT '--- NEW INCOME ADDED ---' AS '';
SELECT * FROM finance_log ORDER BY transaction_id DESC LIMIT 3;
SELECT * FROM income_sources ORDER BY id DESC LIMIT 3;

-- =============================================
-- Section 5: Procedure — OUT Parameter ব্যবহার
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_get_total_expenses ---' AS '';

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_get_total_expenses(
    IN p_year INT,
    IN p_month INT,
    OUT p_total DECIMAL(12,2)
)
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO p_total
    FROM finance_log
    WHERE transaction_type = 'expense'
      AND YEAR(transaction_date) = p_year
      AND MONTH(transaction_date) = p_month;
END$$

DELIMITER ;

-- OUT parameter ব্যবহার
SELECT '--- TOTAL EXPENSES FOR JUNE 2026 ---' AS '';

-- Session variable-এ আউটপুট রাখা
CALL sp_get_total_expenses(2026, 6, @june_total);
SELECT @june_total AS total_expense_june;

-- =============================================
-- Section 6: Procedure — IF-ELSE কন্ডিশনাল লজিক
-- =============================================

SELECT '--- CREATING PROCEDURE: sp_check_budget ---' AS '';

-- নিশ্চিত করি expense_categories টেবিল আছে
CREATE TABLE IF NOT EXISTS expense_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    budget_limit DECIMAL(10,2) DEFAULT NULL
);

INSERT IGNORE INTO expense_categories (id, category_name, budget_limit) VALUES
(1, 'Housing', 1300.00),
(2, 'Food', 400.00),
(3, 'Transport', 100.00),
(4, 'Utilities', 150.00),
(5, 'Entertainment', 100.00);

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_check_budget(
    IN p_category_id INT,
    IN p_amount DECIMAL(10,2)
)
BEGIN
    DECLARE v_budget DECIMAL(10,2);
    DECLARE v_spent DECIMAL(12,2);
    DECLARE v_remaining DECIMAL(12,2);
    DECLARE v_cat_name VARCHAR(50);
    
    -- ক্যাটাগরি তথ্য নেওয়া
    SELECT category_name, budget_limit INTO v_cat_name, v_budget
    FROM expense_categories WHERE id = p_category_id;
    
    -- এই ক্যাটাগরিতে মোট খরচ
    SELECT COALESCE(SUM(amount), 0) INTO v_spent
    FROM finance_log
    WHERE category_id = p_category_id AND transaction_type = 'expense';
    
    SET v_remaining = v_budget - v_spent;
    
    -- IF-ELSE চেক
    IF v_remaining >= p_amount THEN
        SELECT CONCAT('✅ Budget OK for "', v_cat_name, 
                      '" — Remaining: $', v_remaining) AS status;
    ELSEIF v_remaining > 0 THEN
        SELECT CONCAT('⚠️ Partial budget for "', v_cat_name, 
                      '" — Only $', v_remaining, ' left') AS status;
    ELSE
        SELECT CONCAT('❌ Over budget for "', v_cat_name, 
                      '" — Already exceeded by $', ABS(v_remaining)) AS status;
    END IF;
END$$

DELIMITER ;

-- বাজেট চেক করা
CALL sp_check_budget(1, 100);    -- Housing: কত বাকি?
CALL sp_check_budget(4, 50);     -- Utilities: কত বাকি?
CALL sp_check_budget(5, 200);    -- Entertainment: কত বাকি?

-- =============================================
-- Section 7: Procedure লিস্ট দেখা ও ডিলিট
-- =============================================

SELECT '--- SHOWING ALL PROCEDURES ---' AS '';
SHOW PROCEDURE STATUS WHERE Db = 'my_portfolio';

-- Procedure ড্রপ করা
-- DROP PROCEDURE IF EXISTS sp_get_all_transactions;
-- DROP PROCEDURE IF EXISTS sp_get_by_type;
-- DROP PROCEDURE IF EXISTS sp_add_expense;
-- DROP PROCEDURE IF EXISTS sp_add_income;
-- DROP PROCEDURE IF EXISTS sp_get_total_expenses;
-- DROP PROCEDURE IF EXISTS sp_check_budget;

-- =============================================
-- Section 8: Procedure-এর ভিতর আরেক Procedure কল
-- =============================================

SELECT '--- CREATING NESTED PROCEDURE ---' AS '';

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS sp_monthly_report(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    DECLARE v_total_expense DECIMAL(12,2);
    DECLARE v_total_income DECIMAL(12,2);
    DECLARE v_net DECIMAL(12,2);
    
    -- মোট আয়
    SELECT COALESCE(SUM(amount), 0) INTO v_total_income
    FROM finance_log
    WHERE transaction_type = 'income'
      AND YEAR(transaction_date) = p_year
      AND MONTH(transaction_date) = p_month;
    
    -- মোট খরচ (OUT parameter-এর Procedure ব্যবহার করে)
    CALL sp_get_total_expenses(p_year, p_month, @exp);
    SET v_total_expense = @exp;
    
    -- নেট
    SET v_net = v_total_income - v_total_expense;
    
    -- রিপোর্ট দেখানো
    SELECT CONCAT('📊 Monthly Report: ', p_year, '-', LPAD(p_month, 2, '0')) AS report_title;
    SELECT v_total_income AS total_income, 
           v_total_expense AS total_expense, 
           v_net AS net_savings;
    
    IF v_net > 0 THEN
        SELECT '✅ Great month! You saved money.' AS verdict;
    ELSEIF v_net = 0 THEN
        SELECT '⚖️ Break-even month.' AS verdict;
    ELSE
        SELECT '❌ You spent more than you earned!' AS verdict;
    END IF;
END$$

DELIMITER ;

CALL sp_monthly_report(2026, 6);

SELECT '--- Day 12 Complete: Stored Procedures ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: sp_update_expense নামে Procedure বানাও
        যা expense-এর description ও amount UPDATE করবে
        (parameter: p_id, p_new_desc, p_new_amount)

TASK 2: sp_delete_transaction নামে Procedure বানাও
        যা transaction_id দিয়ে DELETE করবে
        (parameter: p_id)

TASK 3: sp_get_balance_sheet নামে Procedure বানাও
        যা total_income, total_expense, net_savings দেখাবে
        (OUT parameter দিয়ে)

TASK 4: sp_get_monthly_comparison নামে Procedure বানাও
        যা দুই মাসের expense তুলনা করবে
        (IN p_month1 INT, IN p_month2 INT, IN p_year INT)

TASK 5 (চ্যালেঞ্জ): 
        sp_transfer_to_savings নামে Procedure বানাও
        যা expense হিসেবে savings_goal-এ টাকা যোগ করবে
        (finance_log এ entry + savings_goal আপডেট)
============================================
*/