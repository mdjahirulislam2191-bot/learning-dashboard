# Day 11: SQL & Excel Interview Questions (SQL ও Excel ইন্টারভিউ প্রশ্ন)

## 🔤 Daily Vocabulary (দৈনিক শব্দভাণ্ডার)
| English | Bangla | Example |
|---------|--------|---------|
| Database | ডাটাবেজ | "I work with relational databases." |
| Table | টেবিল | "The 'Customers' table has 5 columns." |
| Column | কলাম | "Each column represents a data field." |
| Row | সারি | "There are 10,000 rows in the dataset." |
| Primary key | প্রাইমারি কী | "CustomerID is the primary key." |
| Foreign key | ফরেন কী | "OrderID links via foreign key." |
| Filter | ফিল্টার | "I filtered data for the last quarter." |
| Sort | সাজানো | "I sorted results by date descending." |

## 📝 Common SQL Interview Questions

### Q1: "Write a query to find all customers from Toronto."
```sql
SELECT * 
FROM Customers 
WHERE City = 'Toronto';
```

### Q2: "How would you join two tables?"
**Answer:** "I would use a JOIN clause. For example, to combine Orders with Customers:"
```sql
SELECT Orders.OrderID, Customers.CustomerName
FROM Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
```

### Q3: "How do you find duplicate records?"
**Answer:** "I can use GROUP BY and HAVING COUNT:"
```sql
SELECT Email, COUNT(*)
FROM Customers
GROUP BY Email
HAVING COUNT(*) > 1;
```

### Q4: "What is the difference between WHERE and HAVING?"
**Answer:** "WHERE filters rows before grouping. HAVING filters after grouping. WHERE cannot be used with aggregate functions, but HAVING can."

## 📝 Common Excel Interview Questions

### Q1: "What is a VLOOKUP and when do you use it?"
**Answer:** "VLOOKUP searches for a value in the first column of a table and returns a value from another column. For example, I used VLOOKUP to find employee department names based on their ID."
```
=VLOOKUP(A2, Employees!A:D, 3, FALSE)
```

### Q2: "How do you create a Pivot Table?"
**Answer:** "I select the data range, go to Insert → PivotTable, then drag fields into Rows, Columns, Values, and Filters areas. For example, I can drag 'Region' to Rows and 'Sales' to Values to see sales by region."

### Q3: "How do you handle errors in Excel?"
**Answer:** "I use IFERROR to handle errors like #N/A or #DIV/0!. For example:"
```
=IFERROR(A2/B2, "Not Available")
```

## 📖 Grammar Point: Giving Instructions (নির্দেশ দেওয়া)
Use **imperative sentences** (অনুজ্ঞাসূচক বাক্য) when explaining steps.

| Step | Example |
|------|---------|
| First | "First, select your data range." |
| Next | "Next, go to the Insert tab." |
| Then | "Then, click PivotTable." |
| Finally | "Finally, drag fields to create your report." |

## 💡 Interview Tip
If you don't know the answer to a technical question, **say what you DO know**:
- "I haven't used that specific function, but I know the concept. I believe it works like..."
- "I am more comfortable with [X], but I can learn [Y] quickly."

## 🏠 Homework (বাড়ির কাজ)
1. Write a SQL query that would filter data for the year 2024.
2. Write a short explanation of Pivot Tables in your own words.
3. Practice explaining how VLOOKUP works in 1 minute.
