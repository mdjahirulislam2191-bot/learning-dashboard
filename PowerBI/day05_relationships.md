# দিন ৫: টেবিল রিলেশনশিপ (Table Relationships) 🔗

## 🎯 আজকে যা শিখবেন
- Star Schema কী ও কেন গুরুত্বপূর্ণ
- One-to-Many ও Many-to-Many রিলেশনশিপ
- কার্ডিনালিটি ও ক্রস ফিল্টার দিকনির্দেশনা
- একাধিক টেবিল সংযুক্ত করে একটি ফিন্যান্স ডেটামডেল তৈরি

## 📚 তাত্ত্বিক ধারণা

### ১. Star Schema (স্টার স্কিমা)
Power BI-তে **Star Schema** হলো সবচেয়ে জনপ্রিয় ডেটা মডেলিং কৌশল। এতে দুই ধরনের টেবিল থাকে:

| টাইপ | বর্ণনা | উদাহরণ |
|------|--------|--------|
| **Fact Table** (ঘটনা সারণি) | সংখ্যাসূচক ডেটা, মাপার উপযোগী মান | `expense_amount`, `income_amount`, `quantity` |
| **Dimension Table** (মাত্রা সারণি) | বর্ণনামূলক ডেটা, ক্যাটাগরি | `Date`, `Category`, `Account`, `Customer` |

**কেন Star Schema?**
- ✅ দ্রুত কোয়েরি পারফরম্যান্স
- ✅ সহজে বোধগম্য মডেল
- ✅ DAX ফর্মুলা সহজ হয়
- ✅ ফিল্টারিং স্বাভাবিকভাবে কাজ করে

### ২. কার্ডিনালিটি (Cardinality)
দুটি টেবিলের মধ্যে সম্পর্কের ধরন:

| কার্ডিনালিটি | অর্থ | কখন ব্যবহার করবেন |
|---------------|------|-------------------|
| **Many-to-One (\*:1)** | এক টেবিলের অনেক রow অপর টেবিলের এক রow-এর সাথে ম্যাচ করে | সবচেয়ে সাধারণ; ফ্যাক্ট → ডাইমেনশন |
| **One-to-One (1:1)** | এক রow ↔ এক রow | খুবই বিরল; বিশেষ ক্ষেত্রে |
| **One-to-Many (1:\*)** | Many-to-One-এর উল্টো দিক ।  |  |
| **Many-to-Many (\*:\*)** | অনেক রow ↔ অনেক রow | জটিল; এড়িয়ে চলা ভালো |

### ৩. ক্রস ফিল্টার দিকনির্দেশনা (Cross Filter Direction)

| দিক | বর্ণনা |
|-----|--------|
| **Single** | ডাইমেনশন → ফ্যাক্ট (একমুখী) |
| **Both** | উভয় দিকেই ফিল্টার কাজ করে (দ্বিমুখী) — সতর্কতার সাথে ব্যবহার করুন |

### ৪. Finance Data Model উদাহরণ

```
[Date Dimension] ────┐
                     ├── [Expense Fact] ──── [Category Dimension]
[Account Dim.] ──────┘
```

---

## 💻 স্টেপ বাই স্টেপ: ফিন্যান্স ডেটামডেল তৈরি

### Step 1: ডেটা লোড করুন
Power BI Desktop → Get Data → Excel/CSV → নিচের দুটি ফাইল লোড করুন

**টেবিল ১: Finance_Transactions** (Fact Table)
| Date | Category | Account | Amount | Type |
|------|----------|---------|--------|------|
| 01-Jan-2024 | Food | Cash | 500 | Expense |
| 02-Jan-2024 | Salary | Bank | 30000 | Income |
| ... | ... | ... | ... | ... |

**টেবিল ২: Categories** (Dimension Table)
| CategoryID | CategoryName | CategoryType | Budget |
|------------|-------------|--------------|--------|
| 1 | Food | Expense | 5000 |
| 2 | Salary | Income | - |
| 3 | Rent | Expense | 8000 |

### Step 2: Model View খুলুন
Left sidebar → **Model View** (তৃতীয় আইকন)

### Step 3: রিলেশনশিপ তৈরি করুন

1. `Finance_Transactions[Category]` → ড্র্যাগ করুন → `Categories[CategoryName]`-এ ফেলে দিন
2. **Edit Relationship** ডায়ালগ বক্স আসবে:

```
Table 1: Finance_Transactions
Column: Category

Table 2: Categories
Column: CategoryName

Cardinality: Many-to-One (*:1)
Cross Filter Direction: Single
Make this relationship active: ✅
```

3. **OK** ক্লিক করুন

### Step 4: Date টেবিল যোগ করুন

```dax
DateDim = CALENDAR(DATE(2024,1,1), DATE(2024,12,31))
```

এরপর DateDim থেকে Date → Finance_Transactions[Date]-এর সাথে Many-to-One রিলেশন সেট করুন।

### Step 5: রিলেশনশিপ টেস্ট করুন

1. Report View-তে যান
2. Matrix ভিজুয়াল যোগ করুন
3. Rows: Categories[CategoryName]
4. Values: SUM(Finance_Transactions[Amount])
5. Slicer যোগ করুন → DateDim[Date] → তারিখ সিলেক্ট করলে সব ফিল্টার হবে

---

## 🧪 প্র্যাকটিস টাস্ক (Practice Tasks)

### টাস্ক ১: Account Dimension তৈরি
একটি Account টেবিল তৈরি করুন:
| AccountID | AccountName | AccountType | Balance |
|-----------+------------+-------------|---------|
| 1 | Cash | Asset | 10000 |
| 2 | Bank | Asset | 50000 |
| 3 | Credit Card | Liability | -5000 |

এখন Finance_Transactions[Account] → Accounts[AccountName]-এর সাথে রিলেশন তৈরি করুন।

### টাস্ক ২: Star Schema কনফিগারেশন
নিশ্চিত করুন সব ডাইমেনশন টেবিল ফ্যাক্ট টেবিলের সাথে \*:1 রিলেশনশিপে আছে।

### টাস্ক ৩: Cross Filter পরিবর্তন
Category টেবিলের সাথে দ্বিমুখী (Both) ফিল্টার সেট করে দেখুন কী পরিবর্তন হয়।

### টাস্ক ৪: মডেল ডায়াগ্রাম
Model View-তে গিয়ে আপনার মডেলের একটি স্ক্রিনশট নিন। সব রিলেশনশিপ লাইন দেখানো উচিত।

---

## 📝 চূড়ান্ত চেকলিস্ট
- [ ] Fact Table আছে?
- [ ] Dimension Table(s) আছে?
- [ ] Star Schema ফর্ম্যাট অনুসরণ করা হয়েছে?
- [ ] সকল সম্পর্কে Active Relationship সেট করা আছে?
- [ ] Cross Filter Direction সঠিকভাবে সেট করা আছে?
- [ ] Slicer দিয়ে ফিল্টার কাজ করছে?

## 📖 অতিরিক্ত রিসোর্স
- [Microsoft Docs: Relationships](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships)
- [SQLBI: Star Schema](https://www.sqlbi.com/articles/star-schema-in-power-bi/)