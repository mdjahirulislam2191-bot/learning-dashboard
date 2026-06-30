# দিন ৬: ফিল্টার ও স্লাইসার (Filters & Slicers) 🎛️

## 🎯 আজকে যা শিখবেন
- পেজ, রিপোর্ট ও ভিজুয়াল লেভেলের ফিল্টার
- স্লাইসারের প্রকারভেদ ও ফরম্যাটিং
- ডেট রেঞ্জ স্লাইসার ও Advanced ফিল্টার
- ফিন্যান্স রিপোর্টে ফিল্টার প্রয়োগ

## 📚 তাত্ত্বিক ধারণা

### ফিল্টারের লেভেলসমূহ

| লেভেল | স্কোপ | কোথায় প্রভাব ফেলে |
|--------|-------|-------------------|
| **Visual-Level** | শুধু একটি ভিজুয়াল | ঐ একটি চার্ট/টেবিল |
| **Page-Level** | পুরো একটা পেজ | ওই পেজের সব ভিজুয়াল |
| **Report-Level** | সব পেজ | পুরো রিপোর্ট জুড়ে |
| **Drill-Through** | নির্দিষ্ট পেজে | টার্গেট পেজে বিস্তারিত দেখায় |

### ফিল্টারের প্রকারভেদ

| ধরন | উদাহরণ | কখন ব্যবহার করবেন |
|------|---------|-------------------|
| **Basic Filter** | Category = "Food" | সহজ, নির্দিষ্ট মান |
| **Advanced Filter** | Amount > 5000 | সংখ্যাসূচক শর্ত |
| **Top N** | Top 5 Categories | সর্বোচ্চ/সর্বনিম্ন |
| **Relative Date** | Last 30 days | গতিশীল সময়সীমা |
| **By Expression** | DAX-ভিত্তিক | জটিল লজিক |

### স্লাইসারের প্রকারভেদ

| স্লাইসার টাইপ | ব্যবহার |
|----------------|---------|
| **Dropdown** | ড্রপডাউন থেকে সিলেক্ট |
| **List** | চেকবক্স সহ তালিকা |
| **Between** | দুই মানের মাঝে রেঞ্জ |
| **Less than or equal** | একটি সীমা পর্যন্ত |
| **Greater than or equal** | একটি সীমা থেকে |
| **Relative Date** | গত N দিন/মাস/বছর |
| **Hierarchy** | Year → Quarter → Month |

---

## 💻 স্টেপ বাই স্টেপ: ফিন্যান্স ফিল্টারিং

### Step 1: বেসিক ভিজুয়াল ফিল্টার

1. একটি **Clustered Bar Chart** যোগ করুন
2. Axis: `Category`, Values: `SUM(Amount)`
3. Visualizations প্যান → Filters প্যান → **Visual-Level Filters**
4. `Category` → Filter Type: **Basic filtering**
5. "Food", "Rent", "Transport" চেক করুন → **Apply Filter**

### Step 2: পেজ-লেভেল ফিল্টার

1. Filters প্যানের **Filters on this page** সেকশন
2. `Year` ফিল্ড যোগ করুন → শুধু "2024" নির্বাচন করুন
3. এখন পুরো পেজ শুধু 2024 সালের ডেটা দেখাবে

### Step 3: ডেট রেঞ্জ স্লাইসার

1. Slicer ভিজুয়াল যোগ করুন
2. Field: `DateDim[Date]`
3. Slicer Settings (ফরম্যাট প্যান):
   - Style: **Between** (রেঞ্জ স্লাইডার)
   - Slicer Header: **টগল অন**
   - Title: "তারিখের পরিসর নির্বাচন করুন"

### Step 4: স্লাইসার ফরম্যাটিং

ফরম্যাট প্যান থেকে:

| অপশন | সেটিং |
|-------|--------|
| Background | #0078D4 (নীল) |
| Font Color | সাদা |
| Font Size | 12pt |
| Border | Rounded, 4px |
| Items → Font | Calibri, 11pt |
| Selection Control | Show "Select All" ✅ |

### Step 5: Advanced ফিল্টার — বড় খরচ দেখানো

Advanced Filter ব্যবহার করে এক্সপেন্স ফিল্টার:

```text
Field: Amount
Filter Type: Advanced Filtering
Show items when: value > 5000 AND Type = "Expense"
```

### Step 6: Relative Date Slicer — গতিশীল সময়

1. নতুন Slicer → `DateDim[Date]`
2. Style: **Relative Date**
3. Show items when: `In the last` → `1` → `Year`
4. এটি সর্বদা গত ১ বছরের ডেটা দেখাবে — ডেটা রিফ্রেশ হলেও অটো আপডেট হবে

---

## 🧪 প্র্যাকটিস টাস্ক (Practice Tasks)

### টাস্ক ১: বিভাগভিত্তিক বাজেট ফিল্টার
একটি Page-Level ফিল্টার তৈরি করুন যেখানে:
- শুধু "Expense" টাইপের লেনদেন দেখাবে
- কিন্তু Total Income আলাদা কার্ডে দেখাবে (ভিজুয়াল লেভেলে Edit Interactions ব্যবহার করে)

### টাস্ক ২: ডায়নামিক ডেট স্লাইসার
তিনটি স্লাইসার তৈরি করুন:
1. Year ড্রপডাউন
2. Month ড্রপডাউন
3. Quarter বাটন (Q1, Q2, Q3, Q4)

সবগুলো একসাথে কাজ করছে কিনা চেক করুন।

### টাস্ক ৩: Top N ফিল্টার
Expense ক্যাটাগরির **Top 5** সবচেয়ে ব্যয়বহুল বিভাগ দেখান।

### টাস্ক ৪: Advanced টেক্সট ফিল্টার
ট্রানজেকশন নোট/বিবরণ থাকলে সেই কলামে "গ্যাস" বা "ইউটিলিটি" শব্দ থাকা সব লেনদেন ফিল্টার করে দেখান।

---

## 💡 ফিন্যান্স টিপস

### Expense vs Income আলাদা করা
```dax
Total Expense = CALCULATE(SUM(Transactions[Amount]), Transactions[Type] = "Expense")

Total Income = CALCULATE(SUM(Transactions[Amount]), Transactions[Type] = "Income")
```

এই মেজারগুলো ফিল্টার হিসেবে ব্যবহার না করে সরাসরি ভিজুয়ালে দিন — এটা ফিল্টারের চেয়ে অনেক বেশি নিয়ন্ত্রণ দেয়।

### স্লাইসারের Best Practices
1. ✅ সব পেজে Consistent স্লাইসার রাখুন (সিঙ্ক করা)
2. ✅ ডেট স্লাইসার সবচেয়ে উপরে রাখুন
3. ✅ "Select All" অপশন দিন
4. ❌ এক পেজে ৫টির বেশি স্লাইসার রাখবেন না
5. ✅ স্লাইসার গ্রুপ করে রাখুন (Sync Slicers ব্যবহার করুন)

---

## 📝 চূড়ান্ত চেকলিস্ট
- [ ] Visual-Level ফিল্টার ব্যবহার করা শিখেছি
- [ ] Page-Level ফিল্টার বুঝতে পেরেছি
- [ ] Report-Level ফিল্টার সেট করতে পারি
- [ ] ডেট রেঞ্জ স্লাইসার কনফিগার করতে পারি
- [ ] স্লাইসার ফরম্যাটিং করতে পারি
- [ ] Advanced ফিল্টার ব্যবহার করতে পারি
- [ ] Relative Date ফিল্টার বুঝতে পেরেছি
- [ ] Top N ফিল্টার প্রয়োগ করতে পারি
- [ ] Sync Slicers ব্যবহার করতে পারি

## 📖 অতিরিক্ত রিসোর্স
- [Microsoft Docs: Filters](https://docs.microsoft.com/en-us/power-bi/create-reports/power-bi-report-add-filter)
- [Microsoft Docs: Slicers](https://docs.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers)