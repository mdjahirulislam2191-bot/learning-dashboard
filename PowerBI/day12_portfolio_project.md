# দিন ১২: পোর্টফোলিও ড্যাশবোর্ড (Portfolio Project) 🏆

## 🎯 আজকে যা করবেন
এটি আপনার **কমপ্লিট ডেটা অ্যানালিস্ট পোর্টফোলিও প্রজেক্ট**। আপনি একটি পূর্ণাঙ্গ, মাল্টি-পেজ ইন্টারঅ্যাকটিভ ফিন্যান্স ড্যাশবোর্ড তৈরি করবেন যা আপনার স্কিল প্রমাণ করবে।

**এই প্রজেক্ট শেষে আপনি যা পারবেন:**
- ✅ মাল্টি-পেজ ড্যাশবোর্ড ডিজাইন
- ✅ Advanced DAX মেজারস
- ✅ কাস্টম ভিজুয়াল ও কন্ডিশনাল ফরম্যাটিং
- ✅ বুকমার্ক ও নেভিগেশন
- ✅ টাইম ইন্টেলিজেন্স
- ✅ Power BI Service পাবলিশ
- ✅ একটি পোর্টফোলিও-রেডি প্রজেক্ট

---

## 📁 প্রজেক্ট ওভারভিউ

### প্রজেক্টের নাম
**"ব্যক্তিগত ও পারিবারিক ফিন্যান্স ম্যানেজমেন্ট ড্যাশবোর্ড"**

### প্রজেক্টের লক্ষ্য
একটি বাংলাদেশী পরিবারের মাসিক আয়-ব্যয়, সঞ্চয়, বিনিয়োগ ও বাজেট ট্র্যাক করার জন্য একটি পূর্ণাঙ্গ Power BI ড্যাশবোর্ড তৈরি করা।

### ডেটা সোর্স
তিনটি প্রধান ডেটা টেবিল:

1. **Family_Transactions** (Fact Table) — ১২ মাসের লেনদেন
2. **Categories** (Dimension) — ক্যাটাগরি ও বাজেট
3. **Accounts** (Dimension) — ব্যাংক, ক্যাশ, ক্রেডিট কার্ড
4. **DateDim** (Calculated Table via DAX)

---

## 📊 সম্পূর্ণ ডেটাসেট (CSV ফরম্যাট)

Create these CSVs in Power BI Desktop or import:

### Table 1: Family_Transactions (500+ rows — here's a sample)

```csv
Date,CustomerID,Category,Account,Amount,Type,PaymentMode,Note
01-Jan-2024,C001,Salary,Bank,85000,Income,BKash,জানুয়ারি বেতন (জাহিরুল)
01-Jan-2024,C002,Salary,Bank,55000,Income,Bank Transfer,জানুয়ারি বেতন (সাথী)
02-Jan-2024,C001,Rent,Bank,-12000,Expense,BKash,বাড়ি ভাড়া
03-Jan-2024,C001,Groceries,Cash,-5000,Expense,Cash,মাসের বাজার
03-Jan-2024,C002,Groceries,Cash,-3500,Expense,Cash,বাজার-সাথী
05-Jan-2024,C001,Utilities,Bank,-3000,Expense,Online,বিদ্যুৎ বিল
05-Jan-2024,C002,Education,Bank,-2500,Expense,Online,কোর্স ফি
06-Jan-2024,C001,Transport,Cash,-1500,Expense,Cash,পেট্রোল
07-Jan-2024,C001,Healthcare,Bank,-2000,Expense,Credit Card,ডাক্তার
08-Jan-2024,C001,Food,Cash,-2500,Expense,Cash,রেস্তোরাঁ
08-Jan-2024,C002,Freelance,Bank,15000,Income,BKash,ফ্রিল্যান্সিং
10-Jan-2024,C001,Savings,Bank,-10000,Expense,Bank Transfer,সঞ্চয় (DPS)
10-Jan-2024,C002,Savings,Bank,-5000,Expense,Bank Transfer,সঞ্চয় (মিউচুয়াল ফান্ড)
12-Jan-2024,C001,Insurance,Bank,-3500,Expense,Online,লাইফ ইন্সুরেন্স
13-Jan-2024,C001,Entertainment,Cash,-2000,Expense,Cash,পরিবার নিয়ে সিনেমা
15-Jan-2024,C001,Investment,Bank,-15000,Expense,Bank Transfer,স্টক মার্কেট
16-Jan-2024,C002,Transport,Cash,-1000,Expense,Cash,বাস ভাড়া
18-Jan-2024,C001,Utilities,Bank,-1200,Expense,Online,ইন্টারনেট বিল
20-Jan-2024,C001,Groceries,Cash,-4000,Expense,Cash,সপ্তাহের বাজার
22-Jan-2024,C001,Food,Cash,-1800,Expense,Cash,লাঞ্চ আউট
25-Jan-2024,C002,Healthcare,Bank,-1500,Expense,Credit Card,ওষুধ
28-Jan-2024,C001,Travel,Bank,-8000,Expense,Online,পারিবারিক ট্রিপ বুকিং
30-Jan-2024,C001,Entertainment,Cash,-2500,Expense,Cash,পিকনিক
31-Jan-2024,C001,Utilities,Bank,-2000,Expense,Online,মোবাইল রিচার্জ
```

> 💡 এই প্যাটার্ন অনুসরণ করে **১২ মাস** (Jan-Dec 2024) এবং প্রতিমাসে ৪০-৫০টি লেনদেন তৈরি করুন। মোট **৫০০+ রow** থাকা উচিত। Category, Amount ও Note ভ্যারিয়েশন রাখুন।

### Table 2: Categories

```csv
CategoryID,CategoryName,CategoryType,Budget,Priority
1,Salary,Income,0,High
2,Freelance,Income,0,Medium
3,Rent,Expense,12000,High
4,Groceries,Expense,15000,High
5,Food,Expense,8000,Medium
6,Transport,Expense,5000,Medium
7,Utilities,Expense,8000,High
8,Healthcare,Expense,5000,High
9,Education,Expense,5000,Medium
10,Entertainment,Expense,4000,Low
11,Savings,Expense,20000,High
12,Insurance,Expense,5000,High
13,Travel,Expense,10000,Low
14,Investment,Expense,15000,High
```

### Table 3: Accounts

```csv
AccountID,AccountName,AccountType,Balance,Goal
1,Bank,Bank Account,250000,জরুরি তহবিল
2,BKash,Mobile Banking,25000,দৈনিক খরচ
3,Credit Card,Credit Card,0,আপৎকালীন
4,Cash,Physical Cash,10000,দৈনিক খরচ
5,Savings Account,Bank Account,500000,ভবিষ্যৎ সঞ্চয়
```

### Table 4: DateDim (DAX)

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
    "DayOfWeek", FORMAT([Date], "dddd"),
    "Weekend", WEEKDAY([Date], 2) >= 6,
    "YearMonth", FORMAT([Date], "yyyy-mm"),
    "YearQuarter", "FY" & FORMAT(YEAR([Date]), "0") & " Q" & FORMAT(QUARTER([Date]), "0"),
    "DaysInMonth", DAY(EOMONTH([Date], 0))
)
```

---

## 🏗️ ডেটা মডেল

```
          ┌─────────────┐
          │   DateDim    │
          └──────┬──────┘
                 │ (1:*)
          ┌──────┴──────┐
          │ Family_     │
          │ Transactions │
          └──┬───┬───┬──┘
             │   │   │
        (1:*)│   │   │(1:*)
         ┌───┘   │   └────────────┐
         ▼       ▼                ▼
   ┌────────┐ ┌──────┐   ┌────────────────┐
   │Accounts│ │Cate- │   │Customer (New)   │
   │        │ │gories│   │Optional: Family │
   └────────┘ └──────┘   │Members          │
                         └────────────────┘
```

---

## 📐 অ্যাডভান্সড Measures (প্রয়োজনীয়)

```dax
-- ============================
-- বেসিক মেজারস
-- ============================
Total Expense = 
CALCULATE(
    SUM(Family_Transactions[Amount]),
    Family_Transactions[Type] = "Expense"
)

Total Income = 
CALCULATE(
    SUM(Family_Transactions[Amount]),
    Family_Transactions[Type] = "Income"
)

Net Savings = [Total Income] - [Total Expense]

Savings Rate = 
DIVIDE([Net Savings], [Total Income], 0)

-- ============================
-- পার ক্যাপিটা (প্রতি ব্যক্তি)
-- ============================
Expense Per Person = 
DIVIDE([Total Expense], DISTINCTCOUNT(Family_Transactions[CustomerID]), 0)

Income Per Person = 
DIVIDE([Total Income], DISTINCTCOUNT(Family_Transactions[CustomerID]), 0)

-- ============================
-- টাইম ইন্টেলিজেন্স
-- ============================
Expense MTD = 
TOTALMTD([Total Expense], DateDim[Date])

Expense QTD = 
TOTALQTD([Total Expense], DateDim[Date])

Expense YTD = 
TOTALYTD([Total Expense], DateDim[Date])

Income YTD = 
TOTALYTD([Total Income], DateDim[Date])

Expense Prev Month = 
CALCULATE([Total Expense], PREVIOUSMONTH(DateDim[Date]))

Income Prev Month = 
CALCULATE([Total Income], PREVIOUSMONTH(DateDim[Date]))

Expense SPYL = 
CALCULATE([Total Expense], SAMEPERIODLASTYEAR(DateDim[Date]))

Income SPYL = 
CALCULATE([Total Income], SAMEPERIODLASTYEAR(DateDim[Date]))

Expense YoY % = 
VAR PrevYear = [Expense SPYL]
RETURN
DIVIDE([Total Expense] - PrevYear, PrevYear, 0)

Income YoY % = 
VAR PrevYear = [Income SPYL]
RETURN
DIVIDE([Total Income] - PrevYear, PrevYear, 0)

-- ============================
-- বাজেট মেজারস
-- ============================
Total Budget = 
SUM(Categories[Budget])

Budget Utilization % = 
DIVIDE([Total Expense], [Total Budget], 0)

Budget Remaining = [Total Budget] - [Total Expense]

-- ============================
-- অ্যাকাউন্ট ব্যালেন্স
-- ============================
Account Balance = 
CALCULATE(
    SUM(Family_Transactions[Amount]),
    Family_Transactions[Type] = "Income"
) - 
CALCULATE(
    SUM(Family_Transactions[Amount]),
    Family_Transactions[Type] = "Expense"
)

-- ============================
-- র‍্যাঙ্কিং মেজারস
-- ============================
Category Rank = 
RANKX(
    ALL(Categories[CategoryName]),
    [Total Expense],
    ,
    DESC,
    Dense
)

Top 3 Category = 
IF([Category Rank] <= 3, [Total Expense], BLANK())

-- ============================
-- অ্যাডভান্সড ফিন্যান্স
-- ============================
Expense Ratio = 
DIVIDE([Total Expense], [Total Income], 0)

Monthly Run Rate = 
[Total Expense] / MAX(DateDim[DaysInMonth]) * DAY(MAX(DateDim[Date]))

Projected Monthly Expense = 
AVERAGEX(
    VALUES(DateDim[YearMonth]),
    [Total Expense]
)

Disposable Income = 
[Total Income] - [Total Expense] - 
CALCULATE(
    SUM(Family_Transactions[Amount]),
    Family_Transactions[Category] = "Savings"
)

Emergency Fund Coverage = 
DIVIDE(
    CALCULATE(
        SUM(Accounts[Balance]),
        Accounts[Goal] = "জরুরি তহবিল"
    ),
    [Total Expense],
    0
)
```

---

## 🏛️ পেজ ডিজাইন (৬ পৃষ্ঠা)

### Page 1: 🏠 Home / Executive Dashboard

```
┌──────────────────────────────────────────────────────────────────┐
│ 🏠 পারিবারিক ফিন্যান্স ড্যাশবোর্ড ২০২৪                         │
│ [Year Slicer] [Month Slicer] [Category Slicer] [Customer Slicer]│
├───────────┬──────────┬───────────┬────────────┬─────────────────┤
│Total Income│Total     │Net Savings│Savings Rate│Expense Ratio    │
│ 1,40,000  │Expense   │ 75,000    │ 53.6%      │ 46.4%           │
│           │ 65,000   │           │            │                 │
├───────────┴──────────┴───────────┴────────────┴─────────────────┤
│                                                                   │
│  📈 মাসিক আয়, ব্যয় ও সঞ্চয়ের প্রবণতা (Line & Clustered Column)  │
│  (Months on X: Income Line (Green), Expense Line (Red),           │
│   Savings Column (Blue))                                         │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  💰 ক্যাটাগরি অনুযায়ী ব্যয় (Treemap)    |  🎯 ক্যাশ ফ্লো (Waterfall)│
│                                          |                           │
│                                          |                           │
└──────────────────────────────────────────────────────────────────┘
```

**ভিজুয়ালস:**
- 5 Cards (গুরুত্বপূর্ণ KPI)
- Line & Clustered Column Chart (আয়-ব্যয়-সঞ্চয় ট্রেন্ড)
- Treemap (ক্যাটাগরি ব্রেকডাউন)
- Waterfall Chart (মাসিক ক্যাশ ফ্লো)
- 4 Slicers (Year, Month, Category, Customer)

### Page 2: 📊 Expense Analysis

```
┌──────────────────────────────────────────────────────────────────┐
│ 📊 ব্যয় বিশ্লেষণ                                                 │
├────────┬────────┬──────────┬──────────┬──────────────────────────┤
│ Current│Previous│ YoY      │ Avg      │ Budget                   │
│ Month  │ Month  │ Change   │ Monthly  │ Utilization              │
│ 65,000 │ 62,000 │ +4.8%    │ 5,417    │ 81.3%                    │
├────────┴────────┴──────────┴──────────┴──────────────────────────┤
│                                                                   │
│ 🎯 ক্যাটাগরি অনুযায়ী বাজেট vs প্রকল্পিত (Bullet Chart)            │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
| 📋 বিস্তারিত ম্যাট্রিক্স (Category × Month: Actual, Budget,       │
|   Variance, Utilization %, YoY Change)                           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**কন্ডিশনাল ফরম্যাটিং:**
- Utilization > 100% → লাল ব্যাকগ্রাউন্ড
- Utilization 80-100% → হলুদ
- Utilization < 80% → সবুজ
- YoY Change পজিটিভ → লাল তীর ↑ (Expense বেড়েছে)
- YoY Change নেগেটিভ → সবুজ তীর ↓ (Expense কমেছে — ভালো)

### Page 3: 💰 Income Breakdown

```
┌──────────────────────────────────────────────────────────────────┐
│ 💰 আয় বিশ্লেষণ                                                  │
├──────────┬──────────┬───────────┬────────────────────────────────┤
│ Total    │ Per      │ YoY Income│ Income Growth                 │
│ Income   │ Person   │ Growth    | Rate                         │
│ 1,55,000 │ 77,500   │ +10.7%    | 1.09% (MoM)                 │
├──────────┴──────────┴───────────┴────────────────────────────────┤
│                                                                   │
│ 📊 আয়ের উৎস (Donut Chart: Salary vs Freelance vs Others)        │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 📈 সদস্য অনুযায়ী আয় তুলনা (Clustered Bar Chart)                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Page 4: 🐷 Savings & Investments

```
┌──────────────────────────────────────────────────────────────────┐
│ 🐷 সঞ্চয় ও বিনিয়োগ                                              │
├────────────────┬─────────────────┬───────────────────────────────┤
│                │                  │                               │
│ 🎯 Savings     │ 💰 Investment     │ 🏦 Emergency Fund             │
│    Rate Gauge  │    Breakdown      │    Coverage                  │
│  Current: 53.6%│    Pie Chart     │    7.7 Months                │
│  Target: 40%   │                  │                               │
│                │                  │                               │
├────────────────┴─────────────────┴───────────────────────────────┤
│                                                                   │
│ 📈 Savings Rate Trend (Area Chart)                                │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 📊 মাসিক সঞ্চয়ের লক্ষ্য (Stacked Bar: Actual Savings vs Target)  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Page 5: 👥 Family Member Analysis

```
┌──────────────────────────────────────────────────────────────────┐
│ 👥 সদস্য বিশ্লেষণ                                                │
├──────────────┬──────────────┬──────────────┬─────────────────────┤
| Member       | Total Income | Total Expense| Contribution %      |
| জাহিরুল(C001)|  85,000      |  38,000      | 55.8%               |
| সাথী   (C002)|  70,000      |  27,000      | 44.2%               |
├──────────────┴──────────────┴──────────────┴─────────────────────┤
│                                                                   │
| 📊 সদস্য অনুযায়ী ক্যাটাগরি ভিত্তিক খরচ (Stacked Bar Chart)       │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
| 📋 পার ক্যাপিটা ব্যয় (Table: Member, Category, Amount, Share)   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Page 6: 📈 Insights & Forecast

**AI Insights:**
1. **Line Chart** — Forecast using Analytics Pane
2. **Decomposition Tree** — AI Visual দিয়ে Expense Breakdown
3. **Q&A Visual** — Natural Language প্রশ্ন
4. **Key Influencers** — কোন ফ্যাক্টর Expense-কে বেশি প্রভাবিত করে

**Key Insights:**
- সবচেয়ে ব্যয়বহুল মাস: ডিসেম্বর (বর্ষশেষ)
- সবচেয়ে সাশ্রয়ী মাস: ফেব্রুয়ারি
- Highest YoY Growth Category: Travel (+25%)
- Savings Rate Peak: মার্চ (60%)
- Budget Overrun Categories: Entertainment, Food

---

## 🧭 নেভিগেশন সিস্টেম

### বাটন নেভিগেশন:

```
┌──────────────────────────────────────────────────────────────────┐
│ [🏠 হোম]  [📊 ব্যয়]  [💰 আয়]  [🐷 সঞ্চয়]  [👥 সদস্য]  [📈 ইনসাইট] │
│                                                                   │
│                                                                    │
│                        পেজ কন্টেন্ট                               │
│                                                                    │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

প্রতিটি ট্যাব বাটন:
- Default: হালকা ধূসর ব্যাকগ্রাউন্ড
- Active/Selected: গাঢ় রঙ (প্রতি পেজের আলাদা কালার)
- Hover: একটু গাঢ় শেড
- Click Action → Page Navigation

### বুকমার্ক ব্যবহার:
1. "Detail View" বুকমার্ক — সব ডিটেল ভিজুয়াল দেখাবে
2. "Compact View" বুকমার্ক — শুধু KPI Cards দেখাবে
3. "Print View" বুকমার্ক — প্রিন্ট করার মতো সিম্পল ভিউ

---

## 🎨 থিম & কালার স্কিম

```json
{
  "name": "ফিন্যান্স প্রিমিয়াম থিম",
  "dataColors": [
    "#0078D4", "#00B050", "#FF0000", "#FF8C00",
    "#7030A0", "#00B0F0", "#FFC000", "#70AD47",
    "#5B9BD5", "#ED7D31", "#264478", "#9DC3E6"
  ],
  "background": "#F5F5F5",
  "foreground": "#333333",
  "tableAccent": "#0078D4",
  "visualStyles": {
    "titleFontSize": 16,
    "titleFontFamily": "Segoe UI",
    "titleHorizontalAlignment": "Left"
  }
}
```

**কালার ম্যাপিং:**
| এলিমেন্ট | কালার | হেক্স |
|----------|-------|-------|
| Income | সবুজ | #00B050 |
| Expense | লাল | #FF0000 |
| Savings | নীল | #0078D4 |
| Budget | কমলা | #FF8C00 |
| Investment | বেগুনি | #7030A0 |
| Target | সোনালি | #FFC000 |

---

## ✅ প্রজেক্ট কমপ্লিশন চেকলিস্ট

### Phase 1: ডেটা প্রিপারেশন
- [ ] 500+ রow ডেটা তৈরি/ইম্পোর্ট
- [ ] Categories টেবিল
- [ ] Accounts টেবিল
- [ ] DateDim DAX টেবিল
- [ ] Star Schema মডেল
- [ ] Mark as Date Table

### Phase 2: Measures
- [ ] বেসিক Aggregate Measures
- [ ] Time Intelligence Measures
- [ ] YoY Measures
- [ ] Budget Variance Measures
- [ ] Ranking Measures
- [ ] Financial Ratio Measures

### Phase 3: Page 1 — Executive Dashboard
- [ ] 5 KPI Cards
- [ ] Line & Clustered Column Chart
- [ ] Treemap
- [ ] Waterfall Chart
- [ ] 4 Slicers

### Phase 4: Page 2 — Expense Analysis
- [ ] 5 Cards
- [ ] Bullet Chart (Custom Visual)
- [ ] Matrix with Conditional Formatting
- [ ] YoY Comparison Visuals

### Phase 5: Page 3 — Income Analysis
- [ ] Income Donut Chart
- [ ] Per Person Comparison
- [ ] Income Trend

### Phase 6: Page 4 — Savings & Investments
- [ ] Gauge Chart
- [ ] Investment Pie Chart
- [ ] Savings Trend Area Chart
- [ ] Emergency Fund Coverage Card

### Phase 7: Page 5 — Family Members
- [ ] Member-wise Table
- [ ] Stacked Bar (Category per Member)
- [ ] Per Capita Analysis

### Phase 8: Page 6 — Insights
- [ ] Forecast Line Chart
- [ ] Decomposition Tree
- [ ] Q&A Visual
- [ ] Key Influencers Visual

### Phase 9: নেভিগেশন & UX
- [ ] Page Navigator Buttons
- [ ] Active Button Highlight
- [ ] Consistent Theme
- [ ] Bookmarks (Detail/Compact/Print)
- [ ] Tooltip Pages
- [ ] Mobile Layout

### Phase 10: Power BI Service
- [ ] রিপোর্ট পাবলিশ
- [ ] ড্যাশবোর্ড তৈরি
- [ ] Schedule Refresh সেটআপ
- [ ] রিপোর্ট শেয়ার (ভিউ লিংক)
- [ ] App পাবলিশ

---

## 📝 পোর্টফোলিও প্রেজেন্টেশন

### GitHub / Portfolio-তে কীভাবে শেয়ার করবেন

1. **PBIX ফাইল** GitHub-এ আপলোড করুন
2. **README.md** তৈরি করুন:

```markdown
# পারিবারিক ফিন্যান্স ম্যানেজমেন্ট ড্যাশবোর্ড

## 📌 প্রজেক্ট ওভারভিউ
একটি ইন্টারঅ্যাকটিভ Power BI ড্যাশবোর্ড যা একটি বাংলাদেশী পরিবারের...
```

### README-তে যা থাকবে:
- 📸 Screenshots (প্রতিটি পেজের)
- 🎯 প্রজেক্টের উদ্দেশ্য
- 📊 ডেটা স্ট্রাকচার
- 🛠️ ব্যবহৃত টেকনোলজি (Power BI, DAX, Star Schema)
- 📈 Key Insights
- 🔗 Live Demo Link (Power BI Service)

### ইন্টারভিউতে বলবেন:
1. **Star Schema** ব্যবহার করে ডেটামডেল অপ্টিমাইজ করেছি
2. **Advanced DAX** (Time Intelligence, YoY, Budget Variance)
3. **UX ডিজাইন** (Bookmarks, Navigation, Conditional Formatting)
4. **Power BI Service** পাবলিশ ও শেয়ারিং

---

## 🎉 অভিনন্দন! আপনি একজন Data Analyst!

আপনি এখন:
- ✅ Power BI Desktop-এ দক্ষ
- ✅ Advanced DAX জানেন
- ✅ Star Schema বোঝেন
- ✅ Time Intelligence আয়ত্ত করেছেন
- ✅ Custom Visuals ব্যবহার করতে পারেন
- ✅ Power BI Service-এ পাবলিশ করতে পারেন
- ✅ একটি পূর্ণাঙ্গ পোর্টফোলিও প্রজেক্ট তৈরি করেছেন

**আপনার পরবর্তী পদক্ষেপ:**
1. 📊 আরও জটিল প্রজেক্ট করুন (Sales, HR, Supply Chain)
2. 📚 SQL শিখুন (ডেটা এক্সট্র্যাকশনের জন্য)
3. 📈 Python (Pandas, Matplotlib) — বড় ডেটা হ্যান্ডলিংয়ের জন্য
4. 🧪 DAX Optimization & Performance Tuning
5. 🌍 Power BI Certification (PL-300)

### শুভকামনা! 🚀 আপনার ডেটা অ্যানালিস্ট ক্যারিয়ার শুরু হোক!