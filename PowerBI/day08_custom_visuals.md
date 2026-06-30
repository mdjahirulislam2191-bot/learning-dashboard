# দিন ৮: কাস্টম ভিজুয়ালস (Custom Visuals) 🎨

## 🎯 আজকে যা শিখবেন
- Power BI Marketplace থেকে কাস্টম ভিজুয়াল ইনস্টল
- জনপ্রিয় ফিন্যান্স-ফোকাসড ভিজুয়াল
- ফরম্যাটিং টিপস ও বেস্ট প্র্যাকটিস
- কন্ডিশনাল ফরম্যাটিং
- Custom Visual দিয়ে ফিন্যান্স ড্যাশবোর্ড সাজানো

## 📚 তাত্ত্বিক ধারণা

### কাস্টম ভিজুয়াল কেন দরকার?
Power BI-তে বিল্ট-ইন ভিজুয়াল ভালো, কিন্তু ফিন্যান্স ড্যাশবোর্ডের জন্য কাস্টম ভিজুয়াল অনেক বেশি তথ্যবহুল ও আকর্ষণীয় হতে পারে।

### কাস্টম ভিজুয়ালের প্রকার

| টাইপ | উদাহরণ |
|------|---------|
| **AppSource Visuals** | মানচিত্র, গেজ, টর্নেডো চার্ট |
| **Certified Visuals** | Microsoft-এর সার্টিফিকেশনপ্রাপ্ত |
| **Organizational Visuals** | নিজের অর্গানাইজেশনের তৈরি |
| **Custom Code Visuals** | নিজে কোড করে তৈরি (D3.js/React) |

### ফিন্যান্সের জন্য জনপ্রিয় কাস্টম ভিজুয়াল

| ভিজুয়াল নাম | ব্যবহার |
|--------------|---------|
| **Bullet Chart** | বাজেট vs প্রকল্পিত ব্যয় |
| **Waterfall Chart** | আয়-ব্যয়ের ক্যাশ ফ্লো |
| **Gauge** | সঞ্চয়ের লক্ষ্য vs প্রকল্পিত |
| **Hierarchy Slicer** | Year → Quarter → Month |
| **Chiclet Slicer** | বাটন-স্টাইল স্লাইসার |
| **Card with States** | KPI স্ট্যাটাস (Green/Red) |
| **Thermometer** | ফান্ড্রেইজিং বা সেভিংস গোল |
| **Play Axis** | টাইম-ল্যাপস অ্যানিমেশন |
| **Mekko Chart** | মার্কেট শেয়ার বা ক্যাটাগরি ডিস্ট্রিবিউশন |
| **Enlighten Data Story** | AI-ভিত্তিক টেক্সট সামারি |

---

## 💻 স্টেপ বাই স্টেপ: কাস্টম ভিজুয়াল ইন্সটল ও ব্যবহার

### Step 1: কাস্টম ভিজুয়াল ইন্সটল
1. Visualizations প্যান → **... (More Visuals)** আইকন → **Get more visuals**
2. অথবা সরাসরি **AppSource** থেকে সার্চ করুন
3. সার্চ করুন: `Bullet Chart by Microsoft`
4. **Add** ক্লিক করুন

### Step 2: Bullet Chart — বাজেট ট্র্যাকিং
**Bullet Chart** বাজেট বনাম প্রকল্পিত ব্যয় দেখানোর জন্য পারফেক্ট:

1. Bullet Chart ভিজুয়াল যোগ করুন
2. Value: `[Total Expense]`
3. Target: `SUM(Categories[Budget])`
4. Axis: `Categories[CategoryName]`

**ফরম্যাটিং:**
- Good/Bad Zones কনফিগার করুন:
  - Good: 0-80% (সবুজ)
  - Acceptable: 80-100% (হলুদ)
  - Bad: >100% (লাল)

### Step 3: Waterfall Chart — ক্যাশ ফ্লো অ্যানালাইসিস
Waterfall Chart আয়-ব্যয়ের ওঠা-নামা দেখায়:

| উপাদান | টাইপ | পরিমাণ |
|---------|------|--------|
| Opening Balance | Increase | 10,000 |
| Salary | Increase | 30,000 |
| Rent | Decrease | -8,000 |
| Food | Decrease | -5,000 |
| Transport | Decrease | -2,000 |
| **Closing Balance** | **Total** | **25,000** |

### Step 4: Chiclet Slicer — বাটন স্টাইল ফিল্টার
Chiclet Slicer সাধারণ স্লাইসারের চেয়ে বেশি আধুনিক দেখায়:

1. Chiclet Slicer যোগ করুন
2. Values: `Year`
3. Categories: `Quarter`
4. ফরম্যাট:
   - Columns: 4 (কোয়ার্টারের জন্য)
   - Rounded corners
   - Selected color: নীল, Unselected: হালকা ধূসর

### Step 5: Gauge — Savings Goal ট্র্যাকার
```dax
Savings Rate = 
VAR Income = [Total Income]
VAR Expense = [Total Expense]
RETURN DIVIDE(Income - Expense, Income, 0)
```

Gauge ভিজুয়াল:
- Value: `[Savings Rate]`
- Minimum: 0
- Maximum: 25% (টার্গেট)
- Target: 20% (মিনিমাম সেভিংস রেট)

### Step 6: Card with States — KPI ইন্ডিকেটর
একটি Smart Card (নতুন Power BI ভিজুয়াল) ব্যবহার করে YoY Change দেখান:

YoY > 0 → সবুজ ↑ (সঞ্চয় বেড়েছে)
YoY < 0 → লাল ↓ (সঞ্চয় কমেছে)

### Step 7: কন্ডিশনাল ফরম্যাটিং

**টেবিল/ম্যাট্রিক্সের জন্য কন্ডিশনাল ফরম্যাটিং:**

1. Matrix/Table ভিজুয়াল নির্বাচন করুন
2. Fields প্যান → Values → ড্রপডাউন → **Conditional Formatting**
3. **Icons** নির্বাচন করুন
4. Rules:
   - If value ≥ 0 → ✅ Green
   - If value < 0 → ❌ Red

**Background Color Scale:**
```dax
// Variance % কন্ডিশনাল ফরম্যাটিং এর জন্য
-10% → লাল (Bad)
0% → সাদা
+10% → সবুজ (Good)
```

**ডেটা বার ফরম্যাটিং:**
Percentage-এর জন্য ডেটা বার ব্যবহার করলে বোঝা সহজ হয় → সবচেয়ে লম্বা বার = সবচেয়ে ভালো পারফর্মার।

---

## 🧪 প্র্যাকটিস টাস্ক (Practice Tasks)

### টাস্ক ১: ফিন্যান্স ড্যাশবোর্ড কিট ইন্সটল
AppSource থেকে নিচের ভিজুয়ালগুলো ইন্সটল করুন:
1. Bullet Chart (Microsoft)
2. Chiclet Slicer
3. Card with States (Microsoft)

### টাস্ক ২: বাজেট ভ্যারিয়েন্স ড্যাশবোর্ড
Bullet Chart, Chiclet Slicer ও কন্ডিশনাল ফরম্যাটিং নিয়ে একটি পেজ তৈরি করুন যেখানে বাজেট ভ্যারিয়েন্স স্পষ্ট দেখা যায়।

### টাস্ক ৩: কন্ডিশনাল আইকন
সেভিংস রেটের জন্য কন্ডিশনাল ফরম্যাটিং সেট করুন:
- >20%: ✅ সবুজ
- 10-20%: ⚠️ হলুদ
- <10%: ❌ লাল

### টাস্ক ৪: টুলটিপ কাস্টমাইজেশন
একটা বিল্ট-ইন চার্টের জন্য **Report Page Tooltip** তৈরি করুন:
- যে পেজে ক্লিক করলে Bullet Chart-এর বিস্তারিত দেখাবে
- Page Format → Page Information → Type: Tooltip
- Tooltip পেজে Bullet Chart + Gauge রাখুন

### টাস্ক ৫: থিম সেট করুন
View → Themes → Browse Themes → আপনার ফিন্যান্স ড্যাশবোর্ডের জন্য একটি থিম নির্বাচন করুন (যেমন: "Financial" বা "Innovate")

---

## 💡 ফিন্যান্স টিপস

### কাস্টম ভিজুয়াল ব্যবহারের Best Practices
1. ✅ সার্টিফাইড ভিজুয়াল ব্যবহার করুন (পারফরম্যান্স ভালো)
2. ✅ এক পেজে ৩-৪টির বেশি কাস্টম ভিজুয়াল না রাখুন
3. ✅ কালার স্কিম Consistent রাখুন (Company Brand)
4. ❌ অপ্রয়োজনীয় ভিজুয়াল দিয়ে পেজ ভারী করবেন না
5. ✅ লোড টাইম চেক করুন — অনেক কাস্টম ভিজুয়াল স্লো করতে পারে

### কালার স্কিম (ফিন্যান্স থিম)
| এলিমেন্ট | কালার | হেক্স কোড |
|----------|-------|-----------|
| Income | সবুজ | #00B050 |
| Expense | লাল | #FF0000 |
| Target | নীল | #0078D4 |
| Savings | কমলা | #FF8C00 |
| Budget | বেগুনি | #7030A0 |
| Background | হালকা ধূসর | #F2F2F2 |

---

## 📝 চূড়ান্ত চেকলিস্ট
- [ ] AppSource থেকে কাস্টম ভিজুয়াল ইন্সটল করতে পারি
- [ ] Bullet Chart ব্যাবহার করে বাজেট ট্র্যাক করি
- [ ] Waterfall Chart দিয়ে ক্যাশ ফ্লো দেখাই
- [ ] Chiclet Slicer কাস্টমাইজ করি
- [ ] Gauge চার্ট সেটআপ করি
- [ ] কন্ডিশনাল ফরম্যাটিং ব্যবহার করি
- [ ] ব্যাকগ্রাউন্ড কালার স্কেল সেট করি
- [ ] ডেটা বার ফরম্যাটিং করি
- [ ] টুলটিপ পেজ তৈরি করি
- [ ] থিম সেটআপ করি

## 📖 অতিরিক্ত রিসোর্স
- [Microsoft AppSource](https://appsource.microsoft.com/en-US/marketplace/apps?product=power-bi-visuals)
- [Power BI Custom Visuals Guide](https://docs.microsoft.com/en-us/power-bi/developer/visuals/power-bi-custom-visuals)