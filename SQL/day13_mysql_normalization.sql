-- =============================================
-- 📚 DAY 13 — Normalization (1NF, 2NF, 3NF)
-- =============================================
-- আজকের টপিক: 
--   1NF → প্রতিটি সেলে একক মান, PRIMARY KEY
--   2NF → Partial Dependency দূর করা
--   3NF → Transitive Dependency দূর করা
-- =============================================
-- 
-- 🎯 লক্ষ্য: একটি denormalized (অসংগঠিত) টেবিলকে
--   3NF-তে নিয়ে আসা — Redundancy কমানো, Data Integrity বাড়ানো
-- =============================================

USE my_portfolio;

-- =============================================
-- 🚫 শুরু: Denormalized টেবিল (যা আমরা ঠিক করব)
-- =============================================

SELECT '--- CREATING DENORMALIZED TABLE (BAD DESIGN) ---' AS '';

-- একটি অসংগঠিত টেবিল — যেখানে redundancy আছে
CREATE TABLE IF NOT EXISTS expenses_denormalized (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_desc VARCHAR(255),
    amount DECIMAL(10,2),
    transaction_date DATE,
    category_name VARCHAR(50),         -- 🚫 Redundant: একই নাম বারবার
    category_budget DECIMAL(10,2),     -- 🚫 Redundant: budget একই মান বারবার
    vendor_name VARCHAR(100),
    vendor_phone VARCHAR(20),          -- 🚫 Transitive: vendor-এর সাথে সম্পর্কিত, transaction-এর না
    vendor_address VARCHAR(200),       -- 🚫 Transitive: একই
    payment_method VARCHAR(50)
);

-- Redundant ডাটা ঢোকানো
INSERT INTO expenses_denormalized VALUES
(NULL, 'Apartment Rent', 1200.00, '2026-06-01', 'Housing', 1300.00, 'Greenwood Apartments', '555-0101', '123 Main St', 'Bank Transfer'),
(NULL, 'Electricity Bill', 95.00, '2026-06-05', 'Utilities', 150.00, 'Hydro One', '555-0202', '456 Power Ave', 'Auto Debit'),
(NULL, 'Internet Bill', 65.00, '2026-06-06', 'Utilities', 150.00, 'Rogers', '555-0303', '789 Cable Rd', 'Auto Debit'),
(NULL, 'Groceries', 280.00, '2026-06-07', 'Food', 400.00, 'Walmart', '555-0404', '321 Shop St', 'Debit Card'),
(NULL, 'Gas', 55.00, '2026-06-08', 'Transport', 100.00, 'Shell', '555-0505', '654 Fuel Blvd', 'Credit Card'),
(NULL, 'Dinner Out', 45.00, '2026-06-09', 'Food', 400.00, 'Boston Pizza', '555-0606', '987 Eat St', 'Credit Card'),
(NULL, 'Apartment Rent', 1200.00, '2026-07-01', 'Housing', 1300.00, 'Greenwood Apartments', '555-0101', '123 Main St', 'Bank Transfer'); -- 🚫 Duplicate vendor & category info

SELECT * FROM expenses_denormalized;

-- =============================================
-- 📋 1NF (First Normal Form)
-- =============================================
-- ✅ প্রতিটি কলামে atomic (একক) মান
-- ✅ PRIMARY KEY আছে
-- ✅ প্রতিটি সারি ইউনিক
-- 
-- expenses_denormalized ইতিমধ্যে 1NF তে আছে (কারণ সব মান atomic)

SELECT '--- ✅ 1NF: Atomic values, PK exists ---' AS '';
SELECT 'expenses_denormalized is already in 1NF' AS note;

-- =============================================
-- 📋 2NF (Second Normal Form)
-- =============================================
-- ✅ 1NF তে থাকতে হবে
-- ✅ Partial Dependency নেই (non-key কলামগুলো PK-র পুরো অংশের উপর নির্ভরশীল)
-- 
-- আমাদের টেবিলে Partial Dependency আছে:
--   category_name, category_budget → category_name-এর উপর নির্ভর (transaction-এর সাথে সরাসরি সম্পর্ক না)
--   vendor_name, vendor_phone, vendor_address → vendor-এর উপর নির্ভর
-- 
-- সমাধান: আলাদা টেবিলে ভাগ করা

SELECT '--- 🔨 Converting to 2NF: Removing Partial Dependencies ---' AS '';

-- 🔹 Category টেবিল (একবার স্টোর, বারবার ব্যবহার)
CREATE TABLE IF NOT EXISTS norm_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    budget_limit DECIMAL(10,2) DEFAULT NULL
);

INSERT IGNORE INTO norm_categories (category_name, budget_limit) VALUES
('Housing', 1300.00),
('Utilities', 150.00),
('Food', 400.00),
('Transport', 100.00),
('Entertainment', 100.00),
('Health', 200.00),
('Education', 300.00);

-- 🔹 Vendor টেবিল (একবার স্টোর, বারবার ব্যবহার)
CREATE TABLE IF NOT EXISTS norm_vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(200)
);

INSERT IGNORE INTO norm_vendors (vendor_name, phone, address) VALUES
('Greenwood Apartments', '555-0101', '123 Main St'),
('Hydro One', '555-0202', '456 Power Ave'),
('Rogers', '555-0303', '789 Cable Rd'),
('Walmart', '555-0404', '321 Shop St'),
('Shell', '555-0505', '654 Fuel Blvd'),
('Boston Pizza', '555-0606', '987 Eat St');

-- 🔹 Payment Method টেবিল
CREATE TABLE IF NOT EXISTS norm_payment_methods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT IGNORE INTO norm_payment_methods (method_name) VALUES
('Bank Transfer'), ('Auto Debit'), ('Debit Card'), ('Credit Card'), ('Cash');

-- 🔹 Transactions টেবিল (2NF — শুধু transaction-এর নিজস্ব ডাটা)
CREATE TABLE IF NOT EXISTS norm_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_desc VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_date DATE NOT NULL,
    category_id INT,
    vendor_id INT,
    payment_method_id INT,
    FOREIGN KEY (category_id) REFERENCES norm_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (vendor_id) REFERENCES norm_vendors(id) ON DELETE SET NULL,
    FOREIGN KEY (payment_method_id) REFERENCES norm_payment_methods(id) ON DELETE SET NULL
);

INSERT INTO norm_transactions (transaction_desc, amount, transaction_date, category_id, vendor_id, payment_method_id) VALUES
('Apartment Rent', 1200.00, '2026-06-01', 1, 1, 1),
('Electricity Bill', 95.00, '2026-06-05', 2, 2, 2),
('Internet Bill', 65.00, '2026-06-06', 2, 3, 2),
('Groceries', 280.00, '2026-06-07', 3, 4, 3),
('Gas', 55.00, '2026-06-08', 4, 5, 4),
('Dinner Out', 45.00, '2026-06-09', 3, 6, 4),
('Apartment Rent', 1200.00, '2026-07-01', 1, 1, 1);

SELECT '--- ✅ 2NF: Tables are now in 2NF ---' AS '';

-- =============================================
-- 📋 3NF (Third Normal Form)
-- =============================================
-- ✅ 2NF তে থাকতে হবে
-- ✅ Transitive Dependency নেই (non-key কলাম অন্য non-key কলামের উপর নির্ভরশীল নয়)
-- 
-- norm_vendors-এ vendor_name → phone, address (এটি ঠিক আছে, কারণ PK-র উপর নির্ভর)
-- 3NF ইতিমধ্যেই satisfied!

SELECT '--- ✅ 3NF: No transitive dependencies ---' AS '';
SELECT 'All tables already satisfy 3NF' AS note;

-- =============================================
-- 🎯 তুলনা: Denormalized vs Normalized
-- =============================================

SELECT '--- 📊 COMPARISON: Denormalized vs Normalized ---' AS '';

-- Denormalized: সব তথ্য এক টেবিলে
SELECT COUNT(*) AS denormalized_rows FROM expenses_denormalized;

-- Normalized: সম্পর্কিত টেবিল জোড়া দিয়ে
SELECT 
    t.transaction_desc,
    t.amount,
    t.transaction_date,
    c.category_name,
    c.budget_limit,
    v.vendor_name,
    v.phone,
    p.method_name
FROM norm_transactions t
JOIN norm_categories c ON t.category_id = c.id
JOIN norm_vendors v ON t.vendor_id = v.id
JOIN norm_payment_methods p ON t.payment_method_id = p.id;

-- =============================================
-- 🔍 Redundancy চেক
-- =============================================

SELECT '--- 🔍 CHECKING DATA REDUNDANCY ---' AS '';

-- Denormalized: category_budget কতবার রিপিট হয়েছে?
SELECT 'Denormalized: budget data repeated' AS problem;
SELECT category_name, COUNT(*) AS repeats 
FROM expenses_denormalized 
GROUP BY category_name;

-- Normalized: category_budget একবারই স্টোর করা
SELECT 'Normalized: budget stored once' AS solution;
SELECT * FROM norm_categories;

-- =============================================
-- 🧹 ক্লিনআপ
-- =============================================

-- DROP TABLE IF EXISTS expenses_denormalized;
-- DROP TABLE IF EXISTS norm_transactions;
-- DROP TABLE IF EXISTS norm_categories;
-- DROP TABLE IF EXISTS norm_vendors;
-- DROP TABLE IF EXISTS norm_payment_methods;

SELECT '--- Day 13 Complete: Normalization 1NF→2NF→3NF ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: student_courses_denormalized নামে একটি denormalized টেবিল বানাও
        (student_name, course_name, course_teacher, teacher_email, grade)
        — এখানে course_teacher এবং teacher_email redundant

TASK 2: উপরের টেবিলটিকে 1NF→2NF→3NF-তে ভাগ করো
        students, courses, teachers, enrollments টেবিলে

TASK 3: norm_transactions-এ 'quantity' কলাম যোগ করো
        (1NF চেক: quantity কি atomic?)

TASK 4: expenses_denormalized থেকে 'Housing' ক্যাটাগরির
        সব transaction বের করো — Denormalized vs Normalized দুইভাবে
        কোনটা সহজ ও দ্রুত?

TASK 5 (চ্যালেঞ্জ): 
        একটি 3NF স্কিমা ডিজাইন করো একটি ছোট লাইব্রেরি ম্যানেজমেন্ট সিস্টেমের জন্য
        (members, books, authors, loans)
============================================
*/