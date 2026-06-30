# দিন ১১: মিনি প্রজেক্ট — পার্সোনাল ফিন্যান্স ড্যাশবোর্ড 💰

## 🎯 আজকে যা করবেন
এই প্রজেক্টে আপনি পূর্বের সব দিনের জ্ঞান ব্যবহার করে একটি **পূর্ণাঙ্গ ব্যক্তিগত ফিন্যান্স ড্যাশবোর্ড** তৈরি করবেন:
- ✅ Expense Tracker
- ✅ Income vs Expense অ্যানালাইসিস
- ✅ Savings Rate ক্যালকুলেশন
- ✅ YoY ব্যয় তুলনা
- ✅ বাজেট ট্র্যাকিং

---

## 📁 ডেটাসেট তৈরি

প্রথমে নিজের জন্য একটি স্যাম্পল ডেটাসেট তৈরি করুন:

### ডেটা টেবিল: Finance_Transactions (CSV)

```csv
Date,Category,Account,Amount,Type,Note
01-Jan-2024,Salary,Bank,45000,Income,জানুয়ারি বেতন
03-Jan-2024,Rent,Bank,-8000,Expense,বাড়ি ভাড়া
05-Jan-2024,Food,Cash,-3000,Expense,বাজার
07-Jan-2024,Transport,Cash,-1200,Expense,পেট্রোল
10-Jan-2024,Utilities,Bank,-2500,Expense,বৈদ্যুতিক বিল
12-Jan-2024,Food,Cash,-1500,Expense,রেস্তোরাঁ
15-Jan-2024,Savings,Bank,-5000,Expense,সঞ্চয়
18-Jan-2024,Entertainment,Cash,-2000,Expense,সিনেমা
20-Jan-2024,Healthcare,Bank,-3000,Expense,ডাক্তার
25-Jan-2024,Groceries,Cash,-4000,Expense,মাসের বাজার
28-Jan-2024,Salary,Bank,45000,Income,জানুয়ারি বেতন (২য় কিস্তি)
01-Feb-2024,Salary,Bank,45000,Income,ফেব্রুয়ারি বেতন
03-Feb-2024,Rent,Bank,-8000,Expense,বাড়ি ভাড়া
05-Feb-2024,Food,Cash,-3500,Expense,বাজার
07-Feb-2024,Transport,Cash,-1000,Expense,পেট্রোল
10-Feb-2024,Utilities,Bank,-2200,Expense,পানি ও গ্যাস বিল
12-Feb-2024,Food,Cash,-1800,Expense,রেস্তোরাঁ
15-Feb-2024,Savings,Bank,-5000,Expense,সঞ্চয়
18-Feb-2024,Entertainment,Cash,-1500,Expense,পিকনিক
20-Feb-2024,Healthcare,Bank,-2000,Expense,ওষুধ
25-Feb-2024,Groceries,Cash,-4500,Expense,মাসের বাজার
28-Feb-2024,Insurance,Bank,-3000,Expense,হেলথ ইন্সুরেন্স
01-Mar-2024,Salary,Bank,45000,Income,মার্চ বেতন
03-Mar-2024,Rent,Bank,-8000,Expense,বাড়ি ভাড়া
05-Mar-2024,Food,Cash,-3200,Expense,বাজার
07-Mar-2024,Transport,Cash,-1300,Expense,পেট্রোল
10-Mar-2024,Utilities,Bank,-2800,Expense,ইন্টারনেট বিল
12-Mar-2024,Food,Cash,-1600,Expense,রেস্তোরাঁ
15-Mar-2024,Savings,Bank,-5000,Expense,সঞ্চয়
18-Mar-2024,Entertainment,Cash,-1000,Expense,বই কেনা
20-Mar-2024,Healthcare,Bank,-1500,Expense,চেকআপ
25-Mar-2024,Groceries,Cash,-4200,Expense,মাসের বাজার
30-Mar-2024,Travel,Bank,-5000,Expense,পারিবারিক ভ্রমণ
01-Apr-2024,Salary,Bank,48500,Income,এপ্রিল বেতন (বৃদ্ধি)
03-Apr-2024,Rent,Bank,-8500,Expense,বাড়ি ভাড়া (বৃদ্ধি)
05-Apr-2024,Food,Cash,-3500,Expense,বাজার
```

> 💡 **টিপস:** আপনি আপনার নিজের বাস্তব ডেটা ব্যবহার করতে পারেন! শুধু ক্যাটাগরি ও অ্যাকাউন্ট ঠিক রাখুন।

### ডাইমেনশন টেবিল: Categories

| CategoryID | CategoryName | CategoryType | Budget | Icon |
|-----------|-------------|-------------|--------|------|
| 1 | Salary | Income | NULL | 💼 |
| 2 | Rent | Expense | 8500 | 🏠 |
| 3 | Food | Expense | 10000 | 🍽️ |
| 4 | Transport | Expense | 5000 | 🚗 |
| 5 | Utilities | Expense | 8000 | 💡 |
| 6 | Entertainment | Expense | 4000 | 🎬 |
| 7 | Healthcare | Expense | 5000 | 🏥 |
| 8 | Groceries | Expense | 12000 | 🛒 |
| 9 | Savings | Expense | 15000 | 🐷 |
| 10 | Insurance | Expense | 3000 | 🛡️ |
| 11 | Travel | Expense | 10000 | ✈️ |

### ডাইমেনশন টেবিল: DateDim (DAX এ তৈরি)

```dax
DateDim = 
VAR StartDate = DATE(2023, 1, 1)
VAR EndDate = DATE(2025, 12, 31)
RETURN
ADDCOLUMNS(
    CALENDAR(StartDate, EndDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT(QUARTER([Date]), "0"),
    "QuarterNumber", QUARTER([Date]),
    "Month", FORMAT([Date], "mmmm"),
    "MonthNumber", MONTH([Date]),
    "MonthShort", FORMAT([Date], "mmm"),
    "Day", DAY([Date]),
    "Weekday", FORMAT([Date], "dddd"),
    "WeekdayNumber", WEEKDAY([Date], 2),
    "YearMonth", FORMAT([Date], "yyyy-mm"),
    "IsWeekend", WEEKDAY([Date], 2) > 5
)
```

---

## 📐 ডেটামডেল (Star Schema)

```
DateDim ──────┐
               ├── Finance_Transactions ──── Categories
Account ───────┘
```

**রিলেশনশিপ:**
- DateDim[Date] → Finance_Transactions[Date] (1:\*, Single)
- Categories[CategoryName] → Finance_Transactions[Category] (1:\*, Single)
- Account টেবিল → Finance_Transactions[Account] (1:\*, Single)

---

## 📊 প্রয়োজনীয় Measures

```dax
-- বেসিক মেজার
Total Expense = 
CALCULATE(
    SUM(Finance_Transactions[Amount]),
    Finance_Transactions[Type] = "Expense"
)

Total Income = 
CALCULATE(
    SUM(Finance_Transactions[Amount]),
    Finance_Transactions[Type] = "Income"
)

Net Savings = [Total Income] - [Total Expense]

Savings Rate = 
DIVIDE([Net Savings], [Total Income], 0)

-- Time Intelligence
Expense YTD = 
TOTALYTD([Total Expense], DateDim[Date])

Income YTD = 
TOTALYTD([Total Income], DateDim[Date])

Expense Previous Month = 
CALCULATE(
    [Total Expense],
    PREVIOUSMONTH(DateDim[Date])
)

Expense YoY = 
CALCULATE(
    [Total Expense],
    SAMEPERIODLASTYEAR(DateDim[Date])
)

Expense YoY Change = [Total Expense] - [Expense YoY]

Expense YoY % = 
DIVIDE([Expense YoY Change], [Expense YoY], 0)

-- Budget Variance
Total Budget = SUM(Categories[Budget])

Budget Variance = [Total Budget] - [Total Expense]

Budget Utilization % = 
DIVIDE([Total Expense], [Total Budget], 0)

-- Rolling 12 Month
Expense Rolling 12M = 
CALCULATE(
    [Total Expense],
    DATESINPERIOD(DateDim[Date], MAX(DateDim[Date]), -12, MONTH)
)
```

---

## 🏗️ ড্যাশবোর্ড স্ট্রাকচার

### পেজ ১: Overview Dashboard

```
┌──────────────────────────────────────────────────┐
│ 💰 পার্সোনাল ফিন্যান্স ড্যাশবোর্ড                 │
│ 📅 [Month Slicer]  [Year Slicer]  [Category Slicer]│
├──────────┬──────────┬──────────┬──────────────────┤
│  Total   │  Total   │   Net    │   Savings        │
│  Income  │  Expense │  Savings │   Rate           │
│  1,38,500│  53,200  │  85,300  │   61.6%          │
├──────────┴──────────┴──────────┴──────────────────┤
│ 📈 মাসিক আয় vs ব্যয় (Line Chart)                  │
│                                                    │
├────────────────────────────────────────────────────┤
│ 📊 ক্যাটাগরি অনুযায়ী ব্যয় (Bar Chart)             │
│                                                    │
└────────────────────────────────────────────────────┘
```

### পেজ ২: Expense Analysis

```
┌──────────────────────────────────────────────────┐
│ 📉 ব্যয় বিশ্লেষণ                                  │
├──────────┬──────────┬─────────────────────────────┤
│ Expense  │ Previous │  YoY Change                 │
│ Breakdown│  Month   │  +5.2%                      │
├──────────┴──────────┴─────────────────────────────┤
│ 🎯 বাজেট vs প্রকল্পিত (Bullet Chart)               │
│                                                    │
├────────────────────────────────────────────────────┤
│ 💧 ক্যাশ ফ্লো (Waterfall Chart)                     │
│                                                    │
└────────────────────────────────────────────────────┘
```

### পেজ ৩: Savings & Goals

```
┌──────────────────────────────────────────────────┐
│ 💰 সঞ্চয় ও লক্ষ্য                                  │
├──────────────────────────────────────────────────┤
│ 🎯 সঞ্চয়ের লক্ষ্য (Gauge Chart)                    │
│  Target: 20% | Current: 61.6%                    │
├──────────────────────────────────────────────────┤
│ 📈 Savings Trend (Area Chart)                     │
│                                                    │
├──────────────────────────────────────────────────┤
│ 📊 ক্যাটাগরি ওয়াইজ সেভিংস রেট                     │
└──────────────────────────────────────────────────┘
```

---

## 📋 প্রজেক্ট স্টেপ বাই স্টেপ

### Step 1: ডেটা লোডিং
1. Power BI Desktop → Get Data → CSV/Excel
2. Finance_Transactions.csv লোড করুন
3. Categories.csv লোড করুন
4. DateDim DAX দিয়ে তৈরি করুন

### Step 2: ডেটা মডেলিং
1. Model View-এ যান
2. রিলেশনশিপ তৈরি করুন (উপরের ডায়াগ্রাম অনুযায়ী)
3. Mark as Date Table → DateDim

### Step 3: Measures তৈরি
উপরের সব Measures টাইপ করুন (বা কপি-পেস্ট করুন)।

**টিপ:** Measures → 'Finance_Transactions' টেবিলে রাখুন। কিন্তু DateDim ও Category সম্পর্কিত Measures আলাদা টেবিলে রাখতে পারেন।

### Step 4: Page 1 — Overview
1. **4 Cards**: Total Income, Total Expense, Net Savings, Savings Rate
2. **Line Chart**: মাসিক আয় vs ব্যয় (Month on X-axis, Total Income & Total Expense as Values)
3. **Bar Chart**: ক্যাটাগরি অনুযায়ী ব্যয়
4. **Slicers**: Month, Year, Category (friendly names)

### Step 5: Page 2 — Expense Analysis
1. **Matrix**: ক্যাটাগরি × মাস → Expense, Budget, Variance %
2. **Bullet Chart** (কাস্টম ভিজুয়াল): ক্যাটাগরি অনুযায়ী বাজেট vs প্রকল্পিত
3. **Waterfall Chart**: মাসিক ক্যাশ ফ্লো

### Step 6: Page 3 — Savings & Goals
1. **Gauge Chart**: Savings Rate — Min: 0, Max: 30%, Target: 20%
2. **Area Chart**: সময়ের সাথে Savings Rate ট্রেন্ড
3. **Table**: মাসভিত্তিক Income, Expense, Savings, Rate

### Step 7: নেভিগেশন ও ফরম্যাটিং
1. প্রতিটি পেজে **Page Navigator** যোগ করুন
2. থিম সিলেক্ট করুন (View → Themes)
3. কন্ডিশনাল ফরম্যাটিং:
   - Expense > Budget → লাল ব্যাকগ্রাউন্ড
   - Savings Rate > 20% → সবুজ ✅
   - YoY Change নেগেটিভ → লাল ↓

### Step 8: টেস্টিং
- সব ফিল্টার কাজ করছে?
- সব রিলেশনশিপ ঠিক আছে?
- YoY তুলনা সঠিক?
- বাজেট ভ্যারিয়েন্স ঠিক?

---

## 🧪 চেকলিস্ট

### Data Layer
- [ ] Finance_Transactions টেবিল লোড করা
- [ ] Categories টেবিল লোড করা
- [ ] DateDim DAX টেবিল তৈরি
- [ ] Star Schema রিলেশনশিপ

### Measures Layer
- [ ] Total Expense & Total Income
- [ ] Net Savings & Savings Rate
- [ ] Expense YTD, QTD, MTD
- [ ] YoY Comparison Measures
- [ ] Budget Variance Measures
- [ ] Rolling 12 Month

### Visualization Layer
- [ ] Overview Dashboard (Page 1)
- [ ] Expense Analysis (Page 2)
- [ ] Savings & Goals (Page 3)
- [ ] Slicers with proper formatting
- [ ] Bullet Chart (Custom Visual)
- [ ] Waterfall Chart
- [ ] Gauge Chart
- [ ] Conditional Formatting

### Navigation & UX
- [ ] Page Navigator / Buttons
- [ ] Consistent theme
- [ ] All interactions working

---

## 🎯 চ্যালেঞ্জ (অপশনাল)

নিজেকে চ্যালেঞ্জ করুন! নিচের ফিচারগুলো যোগ করুন:
1. **ডেটা অ্যালার্ট**: Expense Target-এর 80% অতিক্রম করলে Alert
2. **AI Visual**: Decomposition Tree দিয়ে Expense Breakdown
3. **কাস্টম থিম**: আপনার নিজের কালার স্কিম
4. **টুলটিপ পেজ**: ক্যাটাগরির বিস্তারিত দেখানোর জন্য
5. **Power BI Service**: পাবলিশ & শেয়ার

### সমাপ্তি 🎉
অভিনন্দন! আপনি একটি পূর্ণাঙ্গ ব্যক্তিগত ফিন্যান্স ড্যাশবোর্ড তৈরি করেছেন। এটি আপনার:
- মাসিক আয়-ব্যয় ট্র্যাক করে
- বাজেট ম্যানেজমেন্টে সহায়তা করে
- সঞ্চয়ের প্রবণতা দেখায়
- বিনিয়োগের সিদ্ধান্ত নিতে সাহায্য করে

**পরবর্তী দিন:** Day 12 — Portfolio Dashboard-এ একটি কমপ্লিট ডেটা অ্যানালিস্ট প্রজেক্ট তৈরি করবেন!