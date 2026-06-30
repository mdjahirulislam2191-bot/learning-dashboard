# Day 3: ডেটা ইম্পোর্ট ও পাওয়ার কোয়েরি ট্রান্সফর্মেশন

## 🎯 আজকের লক্ষ্য
- Excel, CSV ও SQL Database থেকে ডেটা ইম্পোর্ট করা
- Power Query এডিটরে ডেটা ক্লিন ও ট্রান্সফর্ম করা
- ফাইন্যান্স ডেটার জন্য রিয়েল-ওয়ার্ল্ড ট্রান্সফরমেশন

---

## ১. ডেটা সোর্সের ধরণ

Power BI Desktop এ **তিনটি প্রধান উৎস** থেকে ডেটা আনা যায়:

| উৎস | ফাইল/কানেকশন | ফাইন্যান্স ইউজ কেস |
|-----|--------------|-------------------|
| **Excel** | `.xlsx`, `.xls` | মাসিক রিপোর্ট, বাজেট শিট |
| **CSV** | `.csv` | ব্যাংক স্টেটমেন্ট, ট্রানজেকশন এক্সপোর্ট |
| **SQL DB** | SQL Server | ERP/অ্যাকাউন্টিং সফটওয়্যার থেকে লাইভ ডেটা |

---

## ২. Excel ফাইল ইম্পোর্ট

### ডেমো Excel ফাইল তৈরি

নিচের ডেটা Excel-এ তৈরি করে `finance_sample.xlsx` নামে সেভ করুন:

**Sheet 1: Transactions**
| TransactionID | Date | Account | Amount | Type | Description |
|--------------|------|---------|--------|------|-------------|
| T001 | 01-Jan-2024 | Revenue | 50000 | Credit | Product Sales |
| T002 | 02-Jan-2024 | Rent | -5000 | Debit | Office Rent |
| T003 | 03-Jan-2024 | Salary | -15000 | Debit | Employee Salary |
| T004 | 04-Jan-2024 | Revenue | 35000 | Credit | Product Sales |
| T005 | 05-Jan-2024 | Utilities | -2000 | Debit | Electricity Bill |
| T006 | 06-Jan-2024 | Revenue | 25000 | Credit | Service Income |
| T007 | 07-Jan-2024 | Supplies | -3000 | Debit | Office Supplies |

**Sheet 2: Accounts**
| AccountID | AccountName | Category |
|-----------|-------------|----------|
| A001 | Revenue | Income |
| A002 | Rent | Expense |
| A003 | Salary | Expense |
| A004 | Utilities | Expense |
| A005 | Supplies | Expense |

### Power BI তে Excel ইম্পোর্ট

1. **Home** → **Get Data** → **Excel Workbook**
2. `finance_sample.xlsx` সিলেক্ট করুন → **Open**
3. **Navigator** উইন্ডো আসবে — দেখাবে দুইটি শিট:
   - ☐ Transactions
   - ☐ Accounts
4. দুইটি শিট চেক করুন → **Load**

> [!NOTE]
> **Load** বাটনের পাশে ছোট **▼** তীর আছে:
> - **Load** → সরাসরি লোড
> - **Transform Data** → Power Query এডিটর খুলবে (আমরা পরে করব)

---

## ৩. CSV ফাইল ইম্পোর্ট (রিভিউ)

### ব্যাংক স্টেটমেন্ট CSV উদাহরণ

```csv
Date,Description,Debit,Credit,Balance
01-01-2024,Opening Balance,,,,50000
02-01-2024,Sales Deposit,,15000,65000
03-01-2024,Office Rent Payment,5000,,60000
04-01-2024,Client Payment,,25000,85000
05-01-2024,Utility Bill,2000,,83000
06-01-2024,Salary Transfer,15000,,68000
```

ইম্পোর্ট: **Get Data > Text/CSV** → ফাইল সিলেক্ট → **Load**

### CSV ইম্পোর্টের টিপস:
- **Delimiter:** Comma
- **Data Type Detection:** Based on first 200 rows
- **Encoding:** UTF-8 (যদি বাংলা থাকে)

---

## ৪. SQL Database সংযোগ

### SQLite ডেমো ডাটাবেস (প্র্যাকটিস)

SQLite ফ্রি — কোনো সার্ভার লাগে না। Power BI SQLite সরাসরি সাপোর্ট না করলেও **ODBC** বা **SQL Server** দিয়ে সংযোগ দেখানো যাক।

### SQL Server/SSMS এর ধাপ:

1. **Get Data** → **SQL Server**
2. **Server:** `localhost` বা সার্ভার নাম
3. **Database:** `FinanceDB` (অথবা আপনার ডাটাবেস)
4. **Data Connectivity mode:**
   - 🔵 **Import** — ডেটা কপি করে আনে (দ্রুত)
   - 🟢 **DirectQuery** — লাইভ সংযোগ (রিয়েল-টাইম)

### SQL Query ব্যবহার করে ডেটা আনা

**Advanced Options** খুলে **SQL statement** লিখতে পারেন:

```sql
SELECT 
    DATE,
    ACCOUNT,
    AMOUNT,
    TYPE,
    DESCRIPTION
FROM TRANSACTIONS
WHERE AMOUNT > 1000
ORDER BY DATE DESC
```

> [!NOTE]
> **DirectQuery** ফাইন্যান্স রিপোর্টিং-এর জন্য ভালো যখন ডেটা বড় হয় এবং রিয়েল-টাইম দরকার হয়। কিন্তু **Import** অধিকাংশ ক্ষেত্রেই যথেষ্ট।

---

## ৫. Power Query এডিটর — ডেটা ট্রান্সফরমেশন

### Power Query খোলা

1. **Home** → **Transform Data** (অথবা Queries পেনে রাইট-ক্লিক > Edit)
2. Power Query Editor উইন্ডো খুলবে

### ইন্টারফেস:

```
┌─────────────────────────────────────────────┐
│  Home  Transform  Add Column  View          │  ← Ribbon
├──────────────────┬──────────────────────────┤
│ Queries [পেন]    │  Data Preview            │
│ ☰ Transactions   │  ┌─────┬──────┬──────┐  │
│ ☰ Accounts       │  │Date │Amount│Type  │  │
│                  │  ├─────┼──────┼──────┤  │
│                  │  │...  │...   │...   │  │
├──────────────────┴──────────────────────────┤
│ Query Settings [পেন]                        │
│   Properties: Transactions                  │
│   Applied Steps:                            │
│    1. Source                                │
│    2. Navigation                            │
│    3. Changed Type                          │
└─────────────────────────────────────────────┘
```

### গুরুত্বপূর্ণ Power Query Steps:

ডান পাশে **Applied Steps** — প্রতিটি পরিবর্তন রেকর্ড হয়। আপনি যেকোনো স্টেপে ফিরে যেতে পারেন!

---

## ৬. ফাইন্যান্স ডেটা ট্রান্সফরমেশন (রিয়েল উদাহরণ)

### ৬.১ ডুপ্লিকেট রিমুভ

**ব্যবহার:** Transaction ID ডুপ্লিকেট নেই কিনা চেক

1. **TransactionID** কলাম সিলেক্ট করুন
2. **Home** → **Remove Rows** → **Remove Duplicates**

### ৬.২ NULL/খালি ভ্যালু হ্যান্ডেল

**ব্যবহার:** ফাইন্যান্স ডেটায় খালি ঘর থাকলে হিসাব ভুল হয়

1. Amount কলামে NULL আছে কিনা চেক করুন
2. **Home** → **Replace** → **Replace Values**
3. Replace `null` with `0`

### ৬.৩ কলাম বিভক্ত করা (Split Column)

**ব্যবহার:** "John-Doe-Accounts" থেকে নাম আলাদা করা

1. **Description** কলাম সিলেক্ট করুন
2. **Home** → **Split Column** → **By Delimiter**
3. Delimiter: Space → At Each Occurrence

### ৬.৪ ডেটা টাইপ পরিবর্তন

**ব্যবহার:** টেক্সট থেকে নম্বর/ডেটে কনভার্ট

- **Amount** কলাম → Type: **Decimal Number**
- **Date** কলাম → Type: **Date**
- **Type** কলাম → Type: **Text**

### ৬.৫ কন্ডিশনাল কলাম

**ব্যবহার:** Type = "Credit" হলে +1, "Debit" হলে -1

1. **Add Column** → **Conditional Column**
2. New Column Name: `Sign`
3. If `Type` equals `Credit` → Then `1`
4. Else if `Type` equals `Debit` → Then `-1`
5. Else → `0`

### ৬.৬ কাস্টম কলাম (M Formula)

**ব্যবহার:** Net Cash Flow = Amount * Sign

1. **Add Column** → **Custom Column**
2. Custom Column Formula:
```powerquery
[Amount] * [Sign]
```

### ৬.৭ গ্রুপিং (Group By)

**ব্যবহার:** Account অনুযায়ী মোট Amount

1. **Home** → **Group By**
2. Group by: `Account`
3. New Column Name: `TotalAmount`
4. Operation: **Sum**
5. Column: `Amount`

### ৬.৮ মাস/বছর/ত্রৈমাসিক বের করা

```powerquery
// Add Column > Custom Column > Formula
Date.Year([Date])        // বছর
Date.Month([Date])       // মাস নাম্বার
Date.QuarterOfYear([Date])  // ত্রৈমাসিক
Date.MonthName([Date])   // মাসের নাম (January, February...)
```

---

## ৭. ডেটা মডেলিং — সম্পর্ক (Relationships)

### Transactions + Accounts সংযুক্তি

1. **Model View** (🔗) এ যান
2. দুইটি টেবিল দেখবেন: **Transactions** ও **Accounts**
3. **Transactions** টেবিলের **Account** কলাম → **Accounts** টেবিলের **AccountName** এ ড্র্যাগ করুন
4. Relationship তৈরি হবে — **Many-to-One**

### রিলেশনশিপ টাইপ:

| Type | মানে |
|------|------|
| **Many-to-One (\*:1)** | Transactions এ অনেক রো → Accounts এ এক রো |
| **One-to-One (1:1)** | এক-এক করে ম্যাচ |
| **Many-to-Many (\*:\*)** | দুই পাশেই ডুপ্লিকেট |

> [!WARNING]
> ফাইন্যান্স ডেটায় **Many-to-One** সবচেয়ে কমন। ভুল রিলেশনশিপ রিপোর্ট ভুল করবে!

---

## ৮. মার্জ (Merge) ও অ্যাপেন্ড (Append)

### Merge (JOIN) — Excel VLOOKUP/INDEX MATCH এর বিকল্প

Transactions এর সাথে Account Category যোগ করা:

1. **Home** → **Merge Queries**
2. Top table: **Transactions**
3. Bottom table: **Accounts**
4. Match column: Transactions[Account] → Accounts[AccountName]
5. Join Kind: **Left Outer** (Transactions এর সব রো রাখবে)

### Append (UNION) — একাধিক টেবিল স্ট্যাক

যদি Jan, Feb, Mar — তিন মাসের আলাদা টেবিল থাকে:

1. **Home** → **Append Queries**
2. **Three or more tables**
3. Jan, Feb, Mar যোগ করুন

---

## 🧪 প্র্যাকটিস টাস্ক

### টাস্ক ১: Excel + CSV ডেটা ক্লিনিং
1. Excel ফাইল ইম্পোর্ট করুন (Transactions)
2. Power Query তে:
   - NULL ভ্যালু 0 দিয়ে Replace
   - Date কলামের টাইপ Date করুন
   - Debit Amount গুলো পজিটিভ করবেন? (Conditional Column)

### টাস্ক ২: মাসিক সারসংক্ষেপ
1. Group By ব্যবহার করে মাস অনুযায়ী Total Amount বের করুন
2. Credit ও Debt আলাদাভাবে গ্রুপ করুন

### টাস্ক ৩: SQL Query প্র্যাকটিস
নিচের SQL কোয়েরি Power BI তে চালান (যদি SQL Server থাকে):
```sql
SELECT 
    FORMAT(Date, 'yyyy-MM') AS Month,
    Account,
    SUM(Amount) AS TotalAmount
FROM Transactions
GROUP BY FORMAT(Date, 'yyyy-MM'), Account
ORDER BY Month
```

### টাস্ক ৪: ফাইন্যান্স ড্যাশবোর্ড
ক্লিন করা ডেটা ব্যবহার করে:
1. Month on Month Revenue Trend (লাইন চার্ট)
2. Expense Breakdown (পাই চার্ট)
3. Account wise Summary (টেবিল)

---

## ✅ আজকের শেখা

| দক্ষতা | শিখলেন |
|--------|--------|
| Excel ইম্পোর্ট | ✅ |
| CSV ইম্পোর্ট | ✅ |
| SQL Database সংযোগ | ✅ |
| Power Query: Remove Duplicates | ✅ |
| Power Query: Conditional Column | ✅ |
| Power Query: Group By | ✅ |
| Merge Queries (JOIN) | ✅ |
| Append Queries (UNION) | ✅ |
| ডেটা মডেলিং ও Relationships | ✅ |

> [!TIP]
> 🔥 **প্র্যাকটিস টিপ:** আপনার ব্যক্তিগত ব্যাংক স্টেটমেন্ট CSV এক্সপোর্ট করে Power Query তে ক্লিন করুন। রিয়েল ডেটা নিয়ে কাজ করলেই সবচেয়ে ভালো শিখবেন।

---

*📸 Screenshot Placeholder: Power Query Editor with Applied Steps panel*
*📸 Screenshot Placeholder: Merge Queries dialog showing Transactions and Accounts*
*📸 Screenshot Placeholder: Model View showing relationship line between tables*