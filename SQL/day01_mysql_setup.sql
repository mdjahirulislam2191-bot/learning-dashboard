-- Day 1: MySQL Setup & First Database

-- 1. Create your portfolio database
CREATE DATABASE IF NOT EXISTS my_portfolio;

-- 2. Use the database
USE my_portfolio;

-- 3. Create a table for tracking income sources
CREATE TABLE IF NOT EXISTS income_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    amount_cad DECIMAL(10, 2) NOT NULL,
    earned_date DATE
);

-- 4. Insert sample data (your income)
INSERT INTO income_sources (source_name, amount_cad, earned_date) 
VALUES 
('Monthly Base Salary', 4000.00, '2026-06-01'),
('Freelance Analyst Work', 350.00, '2026-06-15');

-- 5. View your data
SELECT * FROM income_sources;
