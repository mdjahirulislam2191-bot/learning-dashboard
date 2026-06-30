# Day 4: DAX বেসিক — CALCULATE, SUM, AVERAGE, FILTER

## 🎯 আজকের লক্ষ্য
- DAX (Data Analysis Expressions) কি ও কেন বুঝতে হবে
- বেসিক DAX ফাংশন: SUM, AVERAGE, COUNT, DISTINCTCOUNT
- CALCULATE — সবচেয়ে শক্তিশালী DAX ফাংশন
- FILTER — কন্ডিশনাল গণনা
- ফাইন্যান্স ডেটার জন্য Measures তৈরি

---

## ১. DAX কি?

**DAX** = **Data Analysis Expressions**

- Power BI, Excel Power Pivot, SSAS Tabular -এ ব্যবহৃত ফর্মুলা ভাষা
- Excel ফর্মুলার মতো, কিন্তু আরও শক্তিশালী
- **Calculated Columns** ও **Measures** — দুইভাবে ব্যবহার করা যায়

### Calculated Column vs Measure

| | Calculated Column | Measure |
|--|-------------------|---------|
| **কখন হিসাব হয়** | ডেটা লোড হওয়ার সময় | রিপোর্টে ইউজ করার সময় |
| **মেমোরি নেয়** | হ্যাঁ (ডেটাবেসে সেভ হয়) | না (অন-দ্য-ফ্লাই) |
| **কোথায় দেখা যায়** | Fields পেনে কলাম হিসেবে | Fields পেনে Σ আইকন নিয়ে |
| **কখন ব্যবহার করবেন** | প্রতিটি রোতে ভ্যালু লাগলে | এগ্রিগেট (SUM, AVERAGE) লাগলে |
| **পারফরম্যান্স** | ধীর (ডেটা লোডে সময় নেয়) | দ্রুত (প্রয়োজন হলে হিসাব করে) |

> [!WARNING]
> **Measure** ব্যবহার করুন whenever possible। Calculated Column শুধু তখনই ব্যবহার করবেন যখন প্রতিটি রোতে আলাদা ভ্যালু জরুরি (যেমন: Revenue - Cost = Profit)।

---

## ২. ডেমো ডেটা

```csv
Date,Product,Category,Revenue,Cost,Profit,Qty
01-Jan-2024,Laptop,Electronics,50000,35000,15000,10
01-Jan-2024,Mouse,Electronics,1200,800,400,20
02-Jan-2024,Keyboard,Electronics,2500,1500,1000,15
03-Jan-2024,Monitor,Electronics,35000,25000,10000,8
04-Jan-2024,Chair,Furniture,15000,9000,6000,12
05-Jan-2024,Desk,Furniture,25000,15000,10000,5
06-Jan-2024,Laptop,Electronics,52000,36000,16000,11
07-Jan-2024,Tablet,Electronics,18000,12000,6000,20
08-Jan-2024,Printer,Electronics,12000,8000,4000,6
09-Jan-2024,Bookshelf,Furniture,8000,5000,3000,4
10-Jan-2024,LED Light,Electronics,3000,1800,1200,25
```

ডেটা Power BI তে Load করুন (CSV থেকে)।

---

## ৩. Measure তৈরি করার পদ্ধতি

### পদ্ধতি ১: Fields পেন থেকে
1. Fields পেনে টেবিলের নামে **Right-click**
2. **New measure** সিলেক্ট করুন
3. Formula bar এ ফর্মুলা লিখুন

### পদ্ধতি ২: Ribbon থেকে
1. **Home** → **New measure**
2. Formula bar ওপেন হবে

### Measure সেভ করা:
```
Formula bar এ লিখুন → Enter চাপুন → Fields পেনে Σ আইকন নিয়ে আসবে
```

---

## ৪. বেসিক এগ্রিগেট ফাংশন

### SUM — মোট

```dax
Total Revenue = SUM('Sales'[Revenue])
```

```dax
Total Cost = SUM('Sales'[Cost])
```

```dax
Total Profit = SUM('Sales'[Profit])
```

### AVERAGE — গড়

```dax
Avg Revenue = AVERAGE('Sales'[Revenue])
```

```dax
Avg Profit per Transaction = AVERAGE('Sales'[Profit])
```

### COUNT — সংখ্যা

```dax
Total Transactions = COUNTROWS('Sales')
```

```dax
Unique Products = DISTINCTCOUNT('Sales'[Product])
```

### MIN / MAX — সর্বনিম্ন/সর্বোচ্চ

```dax
Max Revenue = MAX('Sales'[Revenue])
Min Revenue = MIN('Sales'[Revenue])
```

### ফাইন্যান্সে ব্যবহার:

| Measure | ফর্মুলা | কী বোঝায় |
|---------|---------|----------|
| মোট রাজস্ব | `SUM(Revenue)` | মোট আয় |
| গড় লেনদেন | `AVERAGE(Revenue)` | প্রতিটি সেলের গড় ভ্যালু |
| মোট লেনদেন | `COUNTROWS(Sales)` | কতটি সেল হয়েছে |
| ইউনিক প্রোডাক্ট | `DISTINCTCOUNT(Product)` | কত ধরনের প্রোডাক্ট |

---

## ৫. Measure বসানো

Measure তৈরি হলে:
1. Fields পেনে **Σ Sales** এর নিচে দেখাবে
2. ড্র্যাগ করে ক্যানভাসে ফেলুন
3. **Card** ভিজুয়ালে সবচেয়ে ভালো দেখায়

**প্র্যাকটিস:** চারটি Card ভিজুয়াল বসান:
- Total Revenue: $222,700
- Total Cost: $149,100
- Total Profit: $73,600
- Total Transactions: 11

---

## ৬. CALCULATE — সবচেয়ে শক্তিশালী DAX

**CALCULATE** = কোনো ফর্মুলাকে **কন্ডিশন/ফিল্টার** দিয়ে পরিবর্তন করে।

### সিনট্যাক্স:
```dax
CALCULATE(
    <Expression>,      -- SUM, AVERAGE ইত্যাদি
    <Filter1>,          -- কন্ডিশন
    <Filter2>...        -- আরও কন্ডিশন (ঐচ্ছিক)
)
```

### উদাহরণ ১: শুধু Electronics এর রাজস্ব

```dax
Electronics Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    'Sales'[Category] = "Electronics"
)
```

### উদাহরণ ২: শুধু Furniture এর রাজস্ব

```dax
Furniture Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    'Sales'[Category] = "Furniture"
)
```

### উদাহরণ ৩: লাভজনক পণ্য (>5000 Profit)

```dax
High Profit Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    'Sales'[Profit] > 5000
)
```

### উদাহরণ ৪: জানুয়ারি মাসের রাজস্ব

```dax
Jan Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    MONTH('Sales'[Date]) = 1
)
```

### CALCULATE ফাইন্যান্সে ব্যবহার:

| Measure | ফর্মুলা | অর্থ |
|---------|---------|------|
| Electronics মোট লাভ | `CALCULATE(SUM(Profit), Category="Electronics")` | শুধু ইলেক্ট্রনিক্সের লাভ |
| বড় অর্ডার সংখ্যা | `CALCULATE(COUNTROWS(Sales), Qty >= 10)` | ১০+ ইউনিটের অর্ডার |
| প্রফিটেবল সেল | `CALCULATE(COUNTROWS(Sales), Profit > 0)` | লাভজনক লেনদেন সংখ্যা |

---

## ৭. FILTER — Advanced কন্ডিশন

**FILTER** = টেবিলের রো ফিল্টার করে — **CALCULATE** এর ভিতরে ব্যবহার হয়।

### সিনট্যাক্স:
```dax
CALCULATE(
    <Expression>,
    FILTER(
        <Table>,
        <Condition>
    )
)
```

### FILTER কেন আলাদা?
- সাধারণ `Category = "Electronics"` শুধু **simple filter**
- FILTER কমপ্লেক্স কন্ডিশন, **ভেরিয়েবল**, **multiple conditions** এর জন্য

### উদাহরণ ১: Revenue > গড় Revenue

```dax
Above Avg Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    FILTER(
        'Sales',
        'Sales'[Revenue] > AVERAGE('Sales'[Revenue])
    )
)
```

### উদাহরণ ২: একাধিক কন্ডিশন (AND)

```dax
High Qty Electronics Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    FILTER(
        'Sales',
        'Sales'[Category] = "Electronics" &&
        'Sales'[Qty] >= 10
    )
)
```

### উদাহরণ ৩: OR কন্ডিশন

```dax
High Value Items = 
CALCULATE(
    SUM('Sales'[Revenue]),
    FILTER(
        'Sales',
        'Sales'[Revenue] > 20000 || 
        'Sales'[Profit] > 10000
    )
)
```

### FILTER vs সরাসরি কন্ডিশন:

| | সরাসরি | FILTER |
|--|---------|--------|
| Category = "X" | ✅ `CALCULATE(SUM(...), Category="X")` | 😕 বেশি ওয়েট |
| Revenue > Avg | ❌ সম্ভব না | ✅ `CALCULATE(SUM(...), FILTER(..., Revenue > Avg))` |
| Multiple AND/OR | ❌ সীমিত | ✅ ফুল সাপোর্ট |
| Dynamic filter | ❌ | ✅ ভেরিয়েবল + FILTER |

---

## ৮. টাইম ইন্টেলিজেন্স (Time Intelligence)

### YEAR — বছর

```dax
Sales YTD = 
TOTALYTD(
    SUM('Sales'[Revenue]),
    'Sales'[Date]
)
```

### PREVIOUS MONTH — আগের মাস

```dax
Previous Month Revenue = 
CALCULATE(
    SUM('Sales'[Revenue]),
    PREVIOUSMONTH('Sales'[Date])
)
```

### SAME PERIOD LAST YEAR — গত বছর একই সময়

```dax
Revenue LY = 
CALCULATE(
    SUM('Sales'[Revenue]),
    SAMEPERIODLASTYEAR('Sales'[Date])
)
```

### MoM Growth (%) — মাসিক প্রবৃদ্ধি

```dax
Revenue MoM % = 
VAR CurrentMonth = SUM('Sales'[Revenue])
VAR PreviousMonth = 
    CALCULATE(
        SUM('Sales'[Revenue]),
        PREVIOUSMONTH('Sales'[Date])
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)
```

---

## ৯. ফাইন্যান্স KPI Measures (সম্পূর্ণ সেট)

### Measure ১: Gross Profit Margin

```dax
Gross Profit Margin % = 
DIVIDE(
    SUM('Sales'[Profit]),
    SUM('Sales'[Revenue]),
    0
) * 100
```

### Measure ২: Cost Ratio

```dax
Cost Ratio % = 
DIVIDE(
    SUM('Sales'[Cost]),
    SUM('Sales'[Revenue]),
    0
) * 100
```

### Measure ৩: ভেরিয়েবল ব্যবহার

```dax
Profit Analysis = 
VAR TotalRev = SUM('Sales'[Revenue])
VAR TotalCost = SUM('Sales'[Cost])
VAR TotalProfit = TotalRev - TotalCost
VAR ProfitMargin = DIVIDE(TotalProfit, TotalRev, 0)
RETURN
    "Revenue: $" & FORMAT(TotalRev, "#,#") & 
    " | Profit: $" & FORMAT(TotalProfit, "#,#") & 
    " | Margin: " & FORMAT(ProfitMargin, "0.0%")
```

### Measure ৪: Profit Category Breakdown

```dax
Electronics Profit % = 
VAR TotalProfitAll = SUM('Sales'[Profit])
VAR ElectronicsProfit = 
    CALCULATE(
        SUM('Sales'[Profit]),
        'Sales'[Category] = "Electronics"
    )
RETURN
    DIVIDE(ElectronicsProfit, TotalProfitAll, 0) * 100
```

### Measure ৫: Dynamic Title (CALCULATE + HASONEVALUE)

```dax
Dynamic Revenue Title = 
IF(
    HASONEVALUE('Sales'[Category]),
    "Revenue for " & VALUES('Sales'[Category]),
    "Revenue for All Categories"
)
```

---

## ১০. CALCULATE + ALL — Total vs Selected

### ALL — সব ফিল্টার উপেক্ষা করে

```dax
Total Revenue Overall = 
CALCULATE(
    SUM('Sales'[Revenue]),
    ALL('Sales')
)
```

### Percentage of Total

```dax
Revenue % of Total = 
DIVIDE(
    SUM('Sales'[Revenue]),
    CALCULATE(
        SUM('Sales'[Revenue]),
        ALL('Sales')
    ),
    0
) * 100
```

এটা ব্যবহার করে বার চার্টে প্রতিটি ক্যাটাগরি কত % — দেখানো যায়।

---

## 🧪 প্র্যাকটিস টাস্ক

### টাস্ক ১: বেসিক Measures
নিচের Measure গুলো তৈরি করুন:
1. **Total Revenue** = SUM of Revenue
2. **Total Profit** = SUM of Profit
3. **Avg Transaction Value** = AVERAGE of Revenue
4. **Product Count** = DISTINCTCOUNT of Product
5. **Transaction Count** = COUNTROWS of Sales

### টাস্ক ২: CALCULATE Measures
1. **Furniture Only Revenue** — শুধু Furniture এর Revenue
2. **High Value Sales** — Revenue > 20,000 এর মোট Revenue
3. **Small Orders** — Qty < 10 এর মোট Revenue
4. **Jan Revenue** — জানুয়ারি মাসের Revenue

### টাস্ক ৩: FILTER Measures
1. **Above Average Revenue** — Revenue গড়ের উপরের Transaction গুলোর Revenue
2. **Electronics + High Qty** — Electronics এবং Qty >= 10
3. **Loss Making Items** — যেখানে Profit <= 0

### টাস্ক ৪: ফাইন্যান্স ড্যাশবোর্ড
একটি পেজে নিচের KPI বসান:
| KPI | Measure |
|-----|---------|
| Total Revenue | SUM |
| Profit Margin % | DIVIDE(Profit, Revenue) |
| Electronics Share | CALCULATE + Category Filter |
| Revenue vs Last Year | SAMEPERIODLASTYEAR |

### টাস্ক ৫: Matrix Table
**Matrix** ভিজুয়ালে:
- Rows: Category
- Columns: Date (by Month)
- Values: Revenue Measure
→ CALCULATE ফিল্টার নিজে থেকেই কাজ করবে!

---

## ✅ আজকের শেখা

| ফাংশন | ব্যবহার |
|--------|---------|
| **SUM** | মোট যোগফল |
| **AVERAGE** | গড় |
| **COUNTROWS** | সারি সংখ্যা |
| **DISTINCTCOUNT** | ইউনিক ভ্যালু সংখ্যা |
| **CALCULATE** | কন্ডিশন সহ এগ্রিগেশন |
| **FILTER** | জটিল কন্ডিশন |
| **ALL** | সব ফিল্টার রিমুভ |
| **DIVIDE** | নিরাপদ ভাগ (0 error এড়ায়) |
| **VAR / RETURN** | ভেরিয়েবল ডিক্লেয়ার |
| **TOTALYTD / PREVIOUSMONTH** | টাইম ইন্টেলিজেন্স |

> [!TIP]
> 🔥 **পরবর্তী ধাপ:** Power BI Service এ রিপোর্ট পাবলিশ করা, ড্যাশবোর্ড শেয়ার করা, Row Level Security (RLS) — পেশাদার Power BI ডেভেলপার হওয়ার পথে এগিয়ে যান!

---

## 📚 বোনাস: DAX সিনট্যাক্স চিটশিট

### অপারেটর:
| অপারেটর | অর্থ | উদাহরণ |
|----------|------|---------|
| `=` | সমান | `[Category] = "Electronics"` |
| `<>` | সমান নয় | `[Category] <> "Electronics"` |
| `>` | বড় | `[Revenue] > 10000` |
| `<` | ছোট | `[Revenue] < 5000` |
| `>=` | বড় বা সমান | `[Qty] >= 10` |
| `<=` | ছোট বা সমান | `[Qty] <= 5` |
| `&&` | AND | `[A] > 10 && [B] < 20` |
| `\|\|` | OR | `[A] > 10 \|\| [B] < 20` |

### ফাইন্যান্স KPI লাইব্রেরি:
```dax
Gross Profit = SUM(Sales[Revenue]) - SUM(Sales[Cost])

Gross Margin % = DIVIDE([Gross Profit], SUM(Sales[Revenue]), 0)

Average Order Value = DIVIDE(SUM(Sales[Revenue]), COUNTROWS(Sales), 0)

Revenue per Product = DIVIDE(SUM(Sales[Revenue]), DISTINCTCOUNT(Sales[Product]), 0)

Cost Efficiency = DIVIDE(SUM(Sales[Cost]), SUM(Sales[Revenue]), 0)
```

---

*📸 Screenshot Placeholder: DAX formula bar with Total Revenue measure*
*📸 Screenshot Placeholder: Card visuals showing KPI measures*
*📸 Screenshot Placeholder: Matrix table with Category + Month breakdown*