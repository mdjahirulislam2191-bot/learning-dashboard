-- =============================================
-- 📚 DAY 10 — ALTER / CREATE / DROP
-- =============================================
-- আজকের টপিক: টেবিলের গঠন পরিবর্তন (schema modification)।
-- ALTER → কলাম যোগ/পরিবর্তন/মুছে ফেলা
-- DROP   → টেবিল/ডাটাবেস নিরাপদে মুছে ফেলা
-- =============================================

USE my_portfolio;

-- =============================================
-- Section 1: কলাম যোগ করা (ADD COLUMN)
-- =============================================

SELECT '--- ADDING notes COLUMN TO finance_log ---' AS '';

-- finance_log-এ 'notes' নামে নতুন কলাম যোগ করুন
ALTER TABLE finance_log
ADD COLUMN notes VARCHAR(500) DEFAULT NULL
AFTER description;

SELECT '--- ADDING category_id COLUMN TO finance_log ---' AS '';

-- category_id কলাম যোগ করুন (Day 5-এর JOIN-এর জন্য প্রয়োজন)
ALTER TABLE finance_log
ADD COLUMN category_id INT DEFAULT NULL
AFTER amount;

DESCRIBE finance_log;

-- =============================================
-- Section 2: কলাম মডিফাই করা (MODIFY COLUMN)
-- =============================================

SELECT '--- MODIFYING COLUMN DATATYPE ---' AS '';

-- description-এর আকার বাড়ানো (VARCHAR 255 → 500)
ALTER TABLE finance_log
MODIFY COLUMN description VARCHAR(500) NOT NULL;

-- notes কলামের ডিফল্ট ভ্যালু পরিবর্তন করা
ALTER TABLE finance_log
MODIFY COLUMN notes VARCHAR(300) DEFAULT 'No notes added';

DESCRIBE finance_log;

-- =============================================
-- Section 3: কলাম রিনেম করা (RENAME COLUMN)
-- =============================================

SELECT '--- RENAMING COLUMN ---' AS '';

-- notes কলামের নাম পরিবর্তন করে 'additional_notes'
ALTER TABLE finance_log
RENAME COLUMN notes TO additional_notes;

DESCRIBE finance_log;

-- =============================================
-- Section 4: কলাম ড্রপ করা (DROP COLUMN)
-- =============================================

SELECT '--- DROPPING additional_notes COLUMN ---' AS '';

-- additional_notes কলাম মুছে ফেলা
ALTER TABLE finance_log
DROP COLUMN additional_notes;

DESCRIBE finance_log;

-- =============================================
-- Section 5: টেবিলের নাম পরিবর্তন (RENAME TABLE)
-- =============================================

SELECT '--- RENAMING TABLE (temporary) ---' AS '';

-- টেবিলের নাম সাময়িকভাবে পরিবর্তন
ALTER TABLE finance_log
RENAME TO expense_log;

SHOW TABLES;

-- আবার আগের নামে ফিরিয়ে আনা
ALTER TABLE expense_log
RENAME TO finance_log;

SHOW TABLES;

-- =============================================
-- Section 6: নিরাপদে DROP (DROP IF EXISTS)
-- =============================================

SELECT '--- SAFE DROP EXAMPLES ---' AS '';

-- একটি অস্থায়ী টেবিল তৈরি করি
CREATE TABLE IF NOT EXISTS temp_table_demo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    demo_data VARCHAR(100)
);

INSERT INTO temp_table_demo (demo_data) VALUES ('This is temporary');

SELECT * FROM temp_table_demo;

-- নিরাপদে ড্রপ — IF EXISTS থাকলে error আসবে না
DROP TABLE IF EXISTS temp_table_demo;

-- চেক করি ডিলিট হয়েছে কিনা
SHOW TABLES;

-- =============================================
-- Section 7: একসাথে একাধিক পরিবর্তন
-- =============================================

SELECT '--- MULTIPLE ALTER OPERATIONS ---' AS '';

-- এক ALTER স্টেটমেন্টে একাধিক কাজ
ALTER TABLE finance_log
    ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Cash' AFTER transaction_type,
    ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE AFTER payment_method,
    MODIFY COLUMN amount DECIMAL(12,2) NOT NULL,
    ADD INDEX idx_transaction_date (transaction_date);

DESCRIBE finance_log;

-- =============================================
-- Section 8: DROP করা কলাম আবার ফিরিয়ে আনা
-- =============================================

SELECT '--- RE-ADDING DROPPED COLUMNS ---' AS '';

-- আগে যে payment_method ও is_recurring যোগ করেছি, সেগুলো ড্রপ করি
ALTER TABLE finance_log
    DROP COLUMN payment_method,
    DROP COLUMN is_recurring,
    DROP INDEX idx_transaction_date;

DESCRIBE finance_log;

-- =============================================
-- Section 9: DROP DATABASE (শুধু উদাহরণ — চালাবেন না!)
-- =============================================

/*
⚠️ সাবধান! নিচের কমান্ড পুরো ডাটাবেস মুছে ফেলবে!
⚠️ শুধু তখনই চালান যখন আপনি নিশ্চিত।

-- পুরো ডাটাবেস ড্রপ:
-- DROP DATABASE IF EXISTS my_portfolio;

-- আবার তৈরি:
-- CREATE DATABASE my_portfolio;
*/

SELECT '--- Day 10 Complete: ALTER/CREATE/DROP ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: finance_log-এ 'urgency_level' নামে VARCHAR(20) কলাম যোগ করো
        ('High', 'Medium', 'Low' ভ্যালু রাখার জন্য)

TASK 2: finance_log-এর 'transaction_type' কলামের সাইজ VARCHAR(10)→VARCHAR(20) করো

TASK 3: income_sources টেবিলে 'notes' কলাম যোগ করো (VARCHAR(300))

TASK 4: income_sources-এর 'source_name' কলাম VARCHAR(100)→VARCHAR(200) করো

TASK 5: 'test_backup' নামে একটি অস্থায়ী টেবিল তৈরি করো,
        তারপর DROP TABLE IF EXISTS দিয়ে নিরাপদে মুছে ফেলো

============================================
*/