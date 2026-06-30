# দিন ৭: টাইম ইন্টেলিজেন্স (Time Intelligence) 🕐

## 🎯 আজকে যা শিখবেন
- DATEADD, SAMEPERIODLASTYEAR ফাংশন
- YTD, QTD, MTD গণনা
- YoY (Year-over-Year) এক্সপেন্স তুলনা
- ফিন্যান্স রিপোর্টে টাইম ইন্টেলিজেন্স

## 📚 তাত্ত্বিক ধারণা

### কেন Time Intelligence দরকার?
ফিন্যান্স অ্যানালাইসিসে সময়-ভিত্তিক তুলনা অত্যন্ত গুরুত্বপূর্ণ:
- এই মাসের খরচ vs গত মাসের খরচ
- এই বছর vs গত বছর
- বাজেট vs প্রকল্পিত ব্য়
- QTD (Quarter-to-Date) পারফরমেন্স

### গুরুত্বপূর্ণ DAX ফাংশনসমূহ

| ফাংশন | বর্ণনা | ফিন্যান্স উদাহরণ |
|--------|---------|-------------------|
| `DATEADD` | নির্দিষ্ট সময় যোগ/বিয়োগ করে | গত মাসের খরচ |
| `SAMEPERIODLASTYEAR` | গত বছরের একই সময় | YoY কম্প্যারিসন |
| `TOTALYTD` | বছর-শুরু থেকে জমা | YTD খরচ |
| `TOTALQTD` | কোয়ার্টার-শুরু থেকে জমা | QTD আয় |
| `TOTALMTD` | মাস-শুরু থেকে জমা | MTD ব্যালেন্স |
| `DATESYTD` | YTD ডেট রেঞ্জ রিটার্ন করে | কাস্টম YTD |
| `PREVIOUSMONTH` | আগের মাস | গত মাস |
| `PREVIOUSQUARTER` | আগের কোয়ার্টার | গত কোয়ার্টার |
| `PREVIOUSYEAR` | আগের বছর | গত বছর |

### Prerequisites: Date টেবিল
Time Intelligence সঠিকভাবে কাজ করার জন্য একটি সম্পূর্ণ Date টেবিল দরকার:

```dax
DateDim = 
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2030,12,31)),
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

✅ DateDim টেবিলকে Mark as Date Table করুন:
- Table Tools → Mark as Date Table → Date কলাম নির্বাচন করুন

---

## 💻 স্টেপ বাই স্টেপ: ফিন্যান্স টাইম ইন্টেলিজেন্স

### Step 1: বেসিক মেজার তৈরি (Measures)
```dax
Total Expense = 
CALCULATE(
    SUM(Transactions[Amount]),
    Transactions[Type] = "Expense"
)

Total Income = 
CALCULATE(
    SUM(Transactions[Amount]),
    Transactions[Type] = "Income"
)
```

### Step 2: PREVIOUSMONTH — গত মাসের খরচ
```dax
Expense Previous Month = 
CALCULATE(
    [Total Expense],
    PREVIOUSMONTH(DateDim[Date])
)
```

এখন একটি কার্ড ভিজুয়ালে দেখান: "গত মাসে খরচ হয়েছে: {মান} টাকা"

### Step 3: SAMEPERIODLASTYEAR — YoY তুলনা
```dax
Expense Same Period Last Year = 
CALCULATE(
    [Total Expense],
    SAMEPERIODLASTYEAR(DateDim[Date])
)

Expense YoY Change = 
[Total Expense] - [Expense Same Period Last Year]

Expense YoY % = 
DIVIDE([Expense YoY Change], [Expense Same Period Last Year], 0)
```

### Step 4: YTD, QTD, MTD
```dax
Expense YTD = 
TOTALYTD([Total Expense], DateDim[Date])

Expense QTD = 
TOTALQTD([Total Expense], DateDim[Date])

Expense MTD = 
TOTALMTD([Total Expense], DateDim[Date])
```

### Step 5: DATEADD — কাস্টম পিরিয়ড তুলনা
```dax
Expense Last 30 Days = 
CALCULATE(
    [Total Expense],
    DATEADD(DateDim[Date], -30, DAY)
)

Expense Next Month Forecast = 
CALCULATE(
    [Total Expense],
    DATEADD(DateDim[Date], 1, MONTH)
)
```

### Step 6: YoY Expense Comparison Dashboard
নিচের ভিজুয়ালগুলো নিয়ে একটি পেজ তৈরি করুন:

| ভিজুয়াল | ডেটা |
|-----------|------|
| **Card 1** | Total Expense (এই বছর) |
| **Card 2** | Expense Same Period Last Year |
| **Card 3** | YoY Change (টাকায়) |
| **Card 4** | YoY Change % |
| **Line Chart** | মাসিক Expense — Current Year vs Last Year |
| **Matrix** | Category-wise: Expense, Last Year, Change % |

### Step 7: Line Chart — Current vs Previous Year
1. Line Chart যোগ করুন
2. Axis: `DateDim[Month]`
3. Values: `[Total Expense]` এবং `[Expense Same Period Last Year]`
4. ফরম্যাট:
   - Lines → Colors: Current Year = নীল, Last Year = ধূসর (ড্যাশড)
   - Data Labels: অন
   - Title: "মাসিক খরচ তুলনা: {বর্তমান বছর} vs {গত বছর}"

---

## 🧪 প্র্যাকটিস টাস্ক (Practice Tasks)

### টাস্ক ১: আয়ের জন্য YoY
Income-এর জন্য নিচের মেজারগুলো তৈরি করুন:
- `Income Same Period Last Year`
- `Income YoY Change`
- `Income YoY %`

### টাস্ক ২: Savings Rate MTD
```dax
Savings Rate = 
DIVIDE([Total Income] - [Total Expense], [Total Income], 0)
```
এখন `Savings Rate MTD` তৈরি করুন।

### টাস্ক ৩: রোলিং ১২ মাস
```dax
Expense Rolling 12M = 
CALCULATE(
    [Total Expense],
    DATESINPERIOD(DateDim[Date], MAX(DateDim[Date]), -12, MONTH)
)
```
এটি গত ১২ মাসের মোট খরচ দেখাবে — ট্রেন্ড বুঝতে সহায়ক।

### টাস্ক ৪: বাজেট ভ্যারিয়েন্স
```dax
Expense vs Budget = 
[Total Expense] - SUM(Categories[Budget])

Expense Budget Variance % = 
DIVIDE([Expense vs Budget], SUM(Categories[Budget]), 0)
```
একটি টেবিল তৈরি করুন যেখানে ক্যাটাগরি অনুযায়ী Actual Expense, Budget এবং Variance দেখায়।

### টাস্ক ৫: সর্বনিম্ন ও সর্বোচ্চ মাস
কোন মাসে সবচেয়ে বেশি খরচ হয়েছে এবং কোন মাসে সবচেয়ে কম? একটা Clustered Column Chart তৈরি করুন এবং সর্বোচ্চ কলামটি লাল, বাকিগুলো নীল রাখুন।

---

## 💡 ফিন্যান্স টিপস

### YoY Analysis কেন গুরুত্বপূর্ণ?
- **Seasonality বুঝতে**: ডিসেম্বরে খরচ বাড়ে (বর্ষশেষ)
- **Growth Track**: আয় বাড়ছে নাকি কমছে?
- **Inflation Effect**: গতবছরের তুলনায় ব্যয় কত বেড়েছে?
- **Saving Trend**: সঞ্চয়ের হার কি ইতিবাচক?

### Caution ⚠️
- Time Intelligence ফাংশন শুধু Mark as Date Table করা টেবিলের সাথে কাজ করে
- CALENDERAUTO() ব্যবহার না করে নির্দিষ্ট রেঞ্জ দিন
- DIVIDE() ব্যবহার করুন — Zero Division Error এড়াতে
- YoY%-এর জন্য Decimal Places ঠিক করুন (২ দশমিক)

---

## 📝 চূড়ান্ত চেকলিস্ট
- [ ] Date টেবিল তৈরি করেছি
- [ ] Date টেবিল Mark as Date Table করেছি
- [ ] SAMEPERIODLASTYEAR ব্যবহার করেছি
- [ ] DATEADD ব্যবহার করেছি
- [ ] TOTALYTD/TOTALQTD/TOTALMTD বুঝতে পেরেছি
- [ ] PREVIOUSMONTH ব্যবহার করেছি
- [ ] YoY কম্প্যারিসন ড্যাশবোর্ড তৈরি করেছি
- [ ] Savings Rate MTD বের করতে পারি
- [ ] বাজেট ভ্যারিয়েন্স ট্র্যাক করতে পারি
- [ ] রোলিং ১২ মাসের ট্রেন্ড দেখাতে পারি

## 📖 অতিরিক্ত রিসোর্স
- [Microsoft Docs: Time Intelligence](https://docs.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [SQLBI: Time Intelligence Patterns](https://www.daxpatterns.com/time-patterns/)