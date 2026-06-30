-- =============================================
-- 📚 DAY 15 — Backup, Export & GitHub Push
-- =============================================
-- আজকের টপিক: 
--   🔐 mysqldump — সম্পূর্ণ ডাটাবেস ব্যাকআপ
--   📤 SELECT INTO OUTFILE — CSV/Excel এক্সপোর্ট
--   📥 Import — ব্যাকআপ থেকে পুনরুদ্ধার
--   🐙 GitHub — পুশ করা
-- =============================================
-- 
-- ⚠️ নোট: এই ফাইলের কিছু কমান্ড SQL-এর ভিতর চলে না
-- (যেমন mysqldump, GitHub commands) — এগুলো terminal/bash-এ চালাতে হবে।
-- নিচে নির্দেশনা দেওয়া আছে।
-- =============================================

USE my_portfolio;

-- =============================================
-- Section 1: কেন ব্যাকআপ প্রয়োজন?
-- =============================================

SELECT '--- WHY BACKUP? ---' AS '';

/*
🔐 ব্যাকআপ কেন গুরুত্বপূর্ণ:
  ✅ হার্ডওয়্যার ফেইলিওর
  ✅ ভুলবশত DELETE / DROP
  ✅ ডাটা করাপশন
  ✅ হ্যাকিং / র্যানসমওয়্যার
  ✅ প্রোজেক্ট হাতে রাখা (GitHub)
  ✅ ক্লায়েন্ট/চাকরির ইন্টারভিউতে দেখানো

🎯 Backup Strategy (3-2-1 Rule):
  3 → ব্যাকআপের ৩টি কপি
  2 → ২টি ভিন্ন মিডিয়ামে (লোকাল + ক্লাউড)
  1 → ১টি অফসাইটে (GitHub / Cloud)
*/

-- =============================================
-- Section 2: mysqldump — সম্পূর্ণ ডাটাবেস ব্যাকআপ
-- =============================================

SELECT '--- mysqldump COMMANDS (run in TERMINAL) ---' AS '';

/*
📌 নিচের কমান্ডগুলো টার্মিনাল/bash-এ চালাতে হবে:

🔹 1. সম্পূর্ণ ডাটাবেস ব্যাকআপ:
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe" -u root my_portfolio > "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql"

🔹 2. টাইমস্ট্যাম্প সহ ব্যাকআপ ফাইল (Windows PowerShell):
$date = Get-Date -Format "yyyyMMdd_HHmmss"
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe" -u root my_portfolio > "C:\Users\Md Jahirul Islam\LearningPath\SQL\backup_${date}.sql"

🔹 3. নির্দিষ্ট টেবিলের ব্যাকআপ:
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe" -u root my_portfolio finance_log income_sources > "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_finance_tables.sql"

🔹 4. শুধু STRUCTURE (ডাটা ছাড়া):
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe" --no-data -u root my_portfolio > "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_structure_only.sql"

🔹 5. শুধু DATA (structure ছাড়া):
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe" --no-create-info -u root my_portfolio > "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_data_only.sql"

🔹 6. কম্প্রেসড ব্যাকআপ (gzip):
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysqldump.exe" -u root my_portfolio | gzip > "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql.gz"
*/

-- =============================================
-- Section 3: ব্যাকআপ থেকে রিস্টোর (Import)
-- =============================================

SELECT '--- RESTORE COMMANDS (run in TERMINAL) ---' AS '';

/*
📌 ব্যাকআপ থেকে পুনরুদ্ধার:

🔹 1. পুরো ডাটাবেস রিস্টোর:
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysql.exe" -u root < "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql"

🔹 2. নতুন ডাটাবেসে রিস্টোর:
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS my_portfolio_restored;"
"/c/Program Files/MySQL/MySQL Server 8.4/bin/mysql.exe" -u root my_portfolio_restored < "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql"

🔹 3. MySQL-এর ভিতর থেকে:
SOURCE C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql;
*/

-- =============================================
-- Section 4: SELECT INTO OUTFILE — CSV এক্সপোর্ট
-- =============================================

SELECT '--- EXPORTING DATA TO CSV ---' AS '';

-- ⚠️ SELECT INTO OUTFILE-এর জন্য MySQL-এর secure_file_priv সেট করা থাকতে হবে
-- চেক করার জন্য:
-- SHOW VARIABLES LIKE 'secure_file_priv';

SELECT 'Check secure_file_priv setting:' AS '';
SHOW VARIABLES LIKE 'secure_file_priv';

/*
📌 CSV-তে এক্সপোর্ট করার কমান্ড:

🔹 1. সহজ SELECT INTO OUTFILE:
SELECT * FROM finance_log
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.4/Uploads/finance_log_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

🔹 2. কাস্টমাইজড এক্সপোর্ট (প্রয়োজনীয় কলাম + হেডার):
SELECT 'transaction_id','description','amount','transaction_type','transaction_date'
UNION ALL
SELECT 
    COALESCE(transaction_id, ''),
    COALESCE(description, ''),
    COALESCE(amount, ''),
    COALESCE(transaction_type, ''),
    COALESCE(transaction_date, '')
FROM finance_log
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.4/Uploads/finance_log_with_headers.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

🔹 3. VIEW-কে CSV-তে এক্সপোর্ট:
SELECT * FROM view_monthly_summary
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.4/Uploads/monthly_summary.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';
*/

-- বাস্তব উদাহরণ (যদি secure_file_priv অনুমতি দেয়):
SELECT '--- ATTEMPTING CSV EXPORT (may fail if secure_file_priv restricts path) ---' AS '';
-- Try export, use IFNULL to handle potential errors
-- (নিচের কোয়েরিটি আপনার secure_file_priv সেটিং অনুযায়ী পাথ পরিবর্তন করুন)

/*
-- যদি secure_file_priv = 'C:/ProgramData/MySQL/MySQL Server 8.4/Uploads/' হয়:
SELECT * FROM finance_log
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.4/Uploads/finance_log_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';
*/

-- =============================================
-- Section 5: MySQL Client-এ CSV ফরম্যাটে দেখা
-- =============================================

SELECT '--- CSV-STYLE OUTPUT IN MYSQL CLIENT ---' AS '';

-- কমান্ড লাইনে CSV ফরম্যাটে আউটপুট পেতে:
/*
mysql -u root -B -e "SELECT * FROM my_portfolio.finance_log" -H > finance_log.html
mysql -u root -B -e "SELECT * FROM my_portfolio.finance_log" --batch --silent -e > finance_log.csv
*/

-- অথবা MySQL-এর ভিতর থেকে:
-- \T C:/Users/Md Jahirul Islam/LearningPath/SQL/export_finance_log.txt
-- SELECT * FROM finance_log;
-- \t

-- =============================================
-- Section 6: GitHub — পুশ করা ও ভার্সন কন্ট্রোল
-- =============================================

SELECT '--- GITHUB COMMANDS (run in TERMINAL) ---' AS '';

/*
📌 প্রথমবার Git সেটআপ ও পুশ:

🔹 1. Git শুরু করা (একবার):
cd "C:/Users/Md Jahirul Islam/LearningPath/SQL"
git init
git remote add origin https://github.com/YOUR_USERNAME/SQL-Learning.git

🔹 2. .gitignore ফাইল তৈরি করা (ব্যাকআপ ফাইল বাদ দিতে):
echo "backup_*.sql" > .gitignore
echo "*.csv" >> .gitignore
echo "*.gz" >> .gitignore

🔹 3. সব ফাইল অ্যাড ও কমিট:
git add .
git commit -m "🎉 SQL Learning Path: Day 1 to Day 15 complete"

🔹 4. GitHub-এ পুশ:
git branch -M main
git push -u origin main

📌 প্রতিদিনের জন্য (আপডেট পুশ):
cd "C:/Users/Md Jahirul Islam/LearningPath/SQL"
git status
git add .
git commit -m "📝 Updated Day 15 - Backup & Export notes"
git push

📌 ব্রাঞ্চ তৈরি করা (নতুন ফিচার):
git checkout -b feature/normalization-examples
git add .
git commit -m "✨ Added normalization examples"
git push -u origin feature/normalization-examples

📌 Git Log দেখা:
git log --oneline --graph --all

📌 রিমোট রিপোজিটরি ক্লোন করা (অন্য কম্পিউটারে):
git clone https://github.com/YOUR_USERNAME/SQL-Learning.git
*/

-- =============================================
-- Section 7: অটোমেশন — ব্যাকআপ স্ক্রিপ্ট
-- =============================================

SELECT '--- AUTOMATED BACKUP SCRIPT ---' AS '';

/*
📌 Windows Batch Script (backup.bat):
নিচের কন্টেন্ট "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup.bat" ফাইলে সেভ করো:

@echo off
set DB_NAME=my_portfolio
set BACKUP_DIR=C:\Users\Md Jahirul Islam\LearningPath\SQL
set DATE=%date:~10,4%%date:~4,2%%date:~7,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%
set FILENAME=backup_%DB_NAME%_%DATE%_%TIME%.sql

"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe" -u root %DB_NAME% > "%BACKUP_DIR%\%FILENAME%"
echo ✅ Backup created: %FILENAME%

📌 এই স্ক্রিপ্ট চালানোর জন্য:
cd "C:/Users/Md Jahirul Islam/LearningPath/SQL"
./backup.bat
*/

-- =============================================
-- Section 8: চেকলিস্ট — সবকিছু করা হলো?
-- =============================================

SELECT '--- COMPLETION CHECKLIST ---' AS '';

/*
✅ Day 1-15 Complete Checklist:

📆 Day 1:  ✅ Database & Tables
📆 Day 2:  ✅ CRUD Operations
📆 Day 3:  ✅ Filtering (WHERE, LIKE, BETWEEN)
📆 Day 4:  ✅ Grouping (GROUP BY, HAVING)
📆 Day 5:  ✅ JOINs (INNER, LEFT, RIGHT)
📆 Day 6:  ✅ Subqueries
📆 Day 7:  ✅ Window Functions
📆 Day 8:  ✅ Advanced Functions
📆 Day 9:  ✅ Database Design
📆 Day 10: ✅ ALTER / CREATE / DROP
📆 Day 11: ✅ Views & Indexes
📆 Day 12: ✅ Stored Procedures
📆 Day 13: ✅ Normalization (1NF, 2NF, 3NF)
📆 Day 14: ✅ Portfolio Project
📆 Day 15: ✅ Backup & GitHub

💪 Great job completing the MySQL Learning Path!
*/

-- =============================================
-- Section 9: Backup আর্কাইভের তথ্য দেখা
-- =============================================

SELECT '--- CHECK BACKUP FILES (TERMINAL) ---' AS '';

/*
📌 ব্যাকআপ ফাইল চেক করার কমান্ড:

🔹 1. SQL ফোল্ডারের ফাইল তালিকা:
ls -la "C:/Users/Md Jahirul Islam/LearningPath/SQL/"*.sql

🔹 2. ব্যাকআপ ফাইলের আকার দেখা:
ls -lh "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_*.sql"

🔹 3. ব্যাকআপ ফাইলের প্রথম কয়েক লাইন দেখা:
head -20 "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql"

🔹 4. ব্যাকআপ ফাইলে কতগুলো INSERT আছে?
grep -c "INSERT INTO" "C:/Users/Md Jahirul Islam/LearningPath/SQL/backup_my_portfolio.sql"
*/

-- =============================================
-- Section 10: SELECT INTO OUTFILE — SQL-এ কাজ করে
-- =============================================

SELECT '--- SELECT INTO DUMPFILE (binary safe alternative) ---' AS '';

-- DUMPFILE একটি single row কে binary ফাইল হিসেবে আউটপুট করে
-- (প্র্যাকটিক্যাল ব্যবহার: BLOB ডাটা এক্সপোর্ট)

SELECT 'Knowing your options:' AS '';
SELECT '  mysqldump → Full DB backup (recommended)' AS option1;
SELECT '  SELECT INTO OUTFILE → CSV/TSV export' AS option2;
SELECT '  SELECT INTO DUMPFILE → Binary export (single row)' AS option3;
SELECT '  mysql -B -e → Batch mode text export' AS option4;

SELECT '--- Day 15 Complete: Backup, Export & GitHub ---' AS '';

/* 
============================================
🏋️ PRACTICE — তোমার পালা!
============================================

TASK 1: mysqldump ব্যবহার করে my_portfolio ডাটাবেসের
        সম্পূর্ণ ব্যাকআপ নাও → backup_my_portfolio.sql

TASK 2: finance_log টেবিলকে CSV-তে এক্সপোর্ট করো
        (SELECT INTO OUTFILE বা mysql -B দিয়ে)

TASK 3: উপরের ব্যাকআপ ফাইল থেকে শুধু finance_log
        টেবিলটি রিস্টোর করো

TASK 4: Git শুরু করো → add, commit, এবং GitHub-এ push করো
        (https://github.com/YOUR_USERNAME/SQL-Learning)

TASK 5 (চ্যালেঞ্জ): 
        একটি Shell/Batch স্ক্রিপ্ট বানাও যা:
        1. স্বয়ংক্রিয়ভাবে mysqldump করে
        2. ফাইলের নামে timestamp যোগ করে
        3. সফল ব্যাকআপের পর git add + commit + push করে
        4. ৩০ দিনের পুরনো ব্যাকআপ ফাইল ডিলিট করে
============================================
*/