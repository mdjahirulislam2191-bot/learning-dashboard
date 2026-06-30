# Day 2: বেসিক চার্ট — বার, লাইন, পাই, টেবিল

## 🎯 আজকের লক্ষ্য
- বার চার্ট, লাইন চার্ট, পাই চার্ট তৈরি করা
- ভিজুয়াল ফরম্যাটিং ও কালার পরিবর্তন
- ফাইন্যান্স রিপোর্টের জন্য চার্ট কাস্টমাইজ করা

---

## ১. রিভিউ ও ডেটা লোড

গতকালের `finance_data.csv` ফাইল আবার লোড করুন:
- **Home** → **Recent Sources** → `finance_data.csv`

> যদি না থাকে তাহলে আবার **Get Data > Text/CSV** দিয়ে লোড করুন।

ডেটা চেক করুন: Fields পেনে নিচের কলামগুলো থাকতে হবে:
- ✅ Date (Date)
- ✅ Product (Text)
- ✅ Category (Text)
- ✅ Revenue (Decimal Number) — ∑
- ✅ Cost (Decimal Number) — ∑
- ✅ Profit (Decimal Number) — ∑

---

## ২. বার চার্ট (Column Chart)

### ক্লাস্টার্ড বার চার্ট — ক্যাটাগরি অনুযায়ী রাজস্ব

1. ক্যানভাসে ক্লিক করুন (যেখানে চার্ট বসবে)
2. Visualizations পেনে **ক্লাস্টার্ড বার চার্ট** আইকন ক্লিক করুন:
   ```
   📊  — প্রথম আইকন (Stacked/Clustered)
   ```
3. Fields পেন থেকে:
   - **Axis (X-axis):** `Category` ড্র্যাগ করুন
   - **Values (Y-axis):** `Revenue` ড্র্যাগ করুন
4. চার্ট তৈরি হবে — দেখাবে Electronics ও Furniture এর রাজস্ব

### হরিজন্টাল বার চার্ট

1. চার্ট সিলেক্ট করুন
2. Visualizations পেনে **Stacked Bar Chart** (দ্বিতীয় সারি, প্রথম) সিলেক্ট করুন
3. একই ফিল্ড — কিন্তু চার্ট এখন হরিজন্টাল

### ফাইন্যান্স উদাহরণ: Product wise Profit তুলনা

1. নতুন চার্ট — **Clustered Bar Chart** সিলেক্ট করুন
2. Axis: **Product**
3. Values: **Profit**
4. এখন দেখবেন কোন প্রোডাক্ট বেশি লাভ দিচ্ছে

### 🎨 ফরম্যাটিং

চার্ট সিলেক্ট করুন → **Format** পেন (🎨):

| অপশন | কোথায় | কী করবেন |
|-------|-------|----------|
| **Title** | General > Title | "ক্যাটাগরি অনুযায়ী রাজস্ব" |
| **Data colors** | Visual > Data colors | Electronics = নীল, Furniture = কমলা |
| **Data labels** | Visual > Data labels | On → দেখাবে ভ্যালু |
| **Background** | General > Effects > Background | হালকা সাদা (#FFFFFF) |

> [!TIP]
> রঙের কম্বিনেশন: ফাইন্যান্স রিপোর্টে **নীল-কমলা** বা **গাঢ় নেভি-হালকা নীল** ব্যবহার করা পেশাদার দেখায়।

---

## ৩. লাইন চার্ট (Line Chart) — টাইম সিরিজ

লাইন চার্ট **দিন/মাস/বছর** অনুযায়ী ট্রেন্ড দেখানোর জন্য।

### প্রতিদিনের রাজস্ব ট্রেন্ড

1. **Line Chart** আইকন সিলেক্ট করুন:
   ```
   📈 — Line Chart (Vis পেনে)
   ```
2. Fields:
   - **Axis:** `Date`
   - **Values:** `Revenue`

### একাধিক লাইন — Category wise Trend

1. **Line Chart** সিলেক্ট করুন
2. Axis: `Date`
3. Values: `Revenue`
4. Legend: `Category`

এখন Electronics ও Furniture — দুই লাইন দেখাবে। মাউস ঘুরালে টুলটিপে ভ্যালু দেখাবে।

### 🎨 লাইন ফরম্যাটিং

| অপশন | সেটিং |
|-------|--------|
| **Line width** | 3 px |
| **Marker** | On → Shape: Circle |
| **Line Smoothing** | Off (ফাইন্যান্সে সোজা লাইন বেটার) |
| **Y-axis start** | Zero (On — বাধ্যতামূলক, ম্যানিপুলেশন এড়াতে) |

---

## ৪. পাই চার্ট (Pie Chart) — শেয়ার/পার্সেন্টেজ

পাই চার্ট দেখায় **মোটের মধ্যে কত শতাংশ** — যেমন প্রতিটি প্রোডাক্টের রাজস্ব শেয়ার।

### ক্যাটাগরি অনুযায়ী রাজস্ব শেয়ার

1. **Pie Chart** আইকন ক্লিক করুন:
   ```
   🍕 — Pie Chart
   ```
2. Fields:
   - **Legend:** `Category`
   - **Values:** `Revenue`

### ডোনাট চার্ট (মাঝখান ফাঁকা)

একই পাই চার্টে — **Format > Visual > Donut** → **On**

ডোনাট চার্ট মডার্ন দেখায় ও মাঝখানে **Total** দেখানো যায়।

### 🎨 পাই ফরম্যাটিং

| অপশন | সেটিং |
|-------|--------|
| **Legend position** | Right |
| **Data labels** | On → Label contains: Category + Percent |
| **Detail label** | On → Revenue দেখাবে |
| **Colors** | প্যাস্টেল শেড ব্যবহার করুন |

---

## ৫. টেবিল ও ম্যাট্রিক্স

### টেবিল ভিজুয়াল (Table)

গতকালের টেবিল রিভিউ:
1. **Table** আইকন (📋) ক্লিক করুন
2. Fields: **Date, Product, Category, Revenue, Cost, Profit**

### ম্যাট্রিক্স (Matrix) — পিভট টেবিলের মতো

1. **Matrix** আইকন (📊 প্যাটার্নে) ক্লিক করুন
2. Rows: `Category`
3. Columns: `Date` (Power BI অটো Year-Quarter-Month ভাঙবে)
4. Values: `Revenue`

ম্যাট্রিক্স Excel Pivot Table-এর মতো — সারি ও কলাম দুটোই আছে।

### 🎨 টেবিল ফরম্যাটিং

| অপশন | সেটিং |
|-------|--------|
| **Grid** | Style: Minimal |
| **Column headers** | Bold, Background: #E8E8E8 |
| **Value formatting** | Currency ($), Decimal 0 |
| **Total** | Row subtotals: On |

---

## ৬. স্লাইসার (Slicer) — ইন্টারঅ্যাকটিভ ফিল্টার

স্লাইসার রিপোর্টে **ফিল্টার বাটন** এর মতো কাজ করে।

1. **Slicer** আইকন ক্লিক করুন:
   ```
   🔪 — Slicer (Vis পেনে)
   ```
2. Field: `Category`
3. এখন আপনি **Electronics** বা **Furniture** ক্লিক করতে পারেন — সব চার্ট ফিল্টার হবে!

### স্লাইসার ফরম্যাটিং
- **Style:** Tile (বাটনের মতো)
- **Selection:** Multi-select with Ctrl
- **Colors:** সিলেক্টেড = নেভি ব্লু

---

## 🧪 প্র্যাকটিস টাস্ক

### টাস্ক ১: ফাইন্যান্স ড্যাশবোর্ড
একটি পেজে নিচের চার্টগুলো বসান:
1. ক্যাটাগরি ওয়াইজ বার চার্ট (Revenue)
2. ডেইলি রেভিনিউ লাইন চার্ট (Trend)
3. প্রোডাক্ট শেয়ার পাই চার্ট
4. ডেটার টেবিল (Date, Product, Revenue, Profit)

### টাস্ক ২: কাস্টমাইজেশন
- সব চার্টে **Title** দিন (বাংলা)
- একই **Color Theme** ব্যবহার করুন
- **Data Labels** চালু করুন

### টাস্ক ৩: ক্রস-ফিল্টারিং
- বার চার্টের একটা বার ক্লিক করুন → অন্য চার্টগুলো ফিল্টার হচ্ছে?
- **Edit Interactions** (চার্ট সিলেক্ট → Format > Edit Interactions):
  - 🟢 Filter (ডিফল্ট)
  - 🔴 None (এই চার্ট ফিল্টার করবে না)

### টাস্ক ৪: বুকমার্ক
1. **View** → **Bookmarks** → **Add**
2. নাম দিন "Electronics View"
3. স্লাইসার দিয়ে Electronics সিলেক্ট করুন
4. আরেকটি বুকমার্ক যোগ করুন "All Products View"

---

## 🔢 ফাইন্যান্স KPI চার্ট (বোনাস)

### KPI গেজ
1. **KPI** ভিজুয়াল খুঁজুন (Vis পেন -> Gauge)
2. Value: `Profit`
3. Trend Axis: `Date`
4. Target Goal: `35000`

### কার্ড (Card) — বড় নাম্বার
1. **Card** ভিজুয়াল ক্লিক করুন
2. Value: `Revenue`
3. Format > Callout value > Font: 48pt, Bold

---

## ✅ আজকের শেখা

| চার্ট | কখন ব্যবহার করবেন |
|-------|-------------------|
| 📊 Bar/Column | ক্যাটাগরি অনুযায়ী তুলনা |
| 📈 Line | সময়ের সাথে ট্রেন্ড |
| 🍕 Pie/Donut | শতকরা শেয়ার (মোটের অংশ) |
| 📋 Table | বিস্তারিত ডেটা দেখা |
| 🔪 Slicer | ইন্টারঅ্যাকটিভ ফিল্টার |

> [!TIP]
> 🔥 **প্র্যাকটিস:** আপনার নিজের ফাইন্যান্স ডেটা (যেমন মাসিক খরচ) নিয়ে এই চার্টগুলো তৈরি করুন। যত বেশি হাতেকলমে করবেন, তত দ্রুত শিখবেন।

---

*📸 Screenshot Placeholder: Dashboard with Bar + Line + Pie chart on one page*
*📸 Screenshot Placeholder: Slicer in action filtering all charts*
*📸 Screenshot Placeholder: Formatted table with currency and totals*