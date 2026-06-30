# Day 1: Power BI Desktop সেটআপ ও প্রথম রিপোর্ট

## 🎯 আজকের লক্ষ্য
- Power BI Desktop ডাউনলোড ও ইন্সটল করা
- ইউজার ইন্টারফেস চিনে নেওয়া
- CSV ফাইল থেকে প্রথম রিপোর্ট তৈরি করা

---

## ১. Power BI Desktop ডাউনলোড ও ইন্সটল

### ধাপ ১: ডাউনলোড
1. ব্রাউজার খুলে https://powerbi.microsoft.com/desktop/ এ যান
2. **Download free** বাটনে ক্লিক করুন
3. দুইটি অপশন আসবে:
   - Microsoft Store থেকে (সহজ, অটো-আপডেট)
   - Standalone Installer (.exe ফাইল)
4. **Standalone installer** সিলেক্ট করুন (নিচের অপশন)
5. ফাইল নাম: `PBIDesktopSetup_x64.exe` (~500 MB)

### ধাপ ২: ইন্সটল
1. ডাউনলোড করা `.exe` ফাইল ডাবল-ক্লিক করুন
2. **Next > Next > Install** — ডিফল্ট সেটিংস রাখুন
3. ইন্সটল শেষে **Launch Power BI Desktop** চেক করে **Finish** দিন

> [!NOTE]
> Power BI Desktop সম্পূর্ণ **ফ্রি**। শুধু Microsoft অ্যাকাউন্ট দিয়ে সাইন-ইন করতে পারেন (ফ্রি) — তবে সাইন-ইন না করেও অফলাইনে ব্যবহার করা যায়।

---

## ২. ইন্টারফেস পরিচিতি

Power BI Desktop ওপেন করলে দেখবেন:

```
┌─────────────────────────────────────────────────┐
│  🟠 File   Home   Insert   Modeling   Help      │  ← Ribbon (রিবন)
├─────────────────────────────────────────────────┤
│  ☰ Pages  [Canvas]                              │
│  📊                                       │  ← Canvas (ক্যানভাস)
│  Visualizations                                │
│     ☐ ☐ ☐ ☐                                   │  ← Visualizations পেন
│  Fields                                        │
│     ☑ Column1                                 │  ← Fields পেন
│     ☑ Column2                                 │
├─────────────────────────────────────────────────┤
│  Page 1  ➕  ← Page tab                        │
└─────────────────────────────────────────────────┘
```

### গুরুত্বপূর্ণ অংশসমূহ:

| অংশ | নাম | কাজ |
|------|------|------|
| 🟠 **Ribbon** | Home / Insert / Modeling | সব কমান্ডের মেনু |
| ⬜ **Canvas** | Report Canvas | ভিজুয়াল ড্রাগ-ড্রপ করে তৈরি করুন |
| 📐 **Visualizations** | Visualizations Pane | চার্টের ধরন বাছাই |
| 📋 **Fields** | Fields Pane | ডেটার কলাম দেখায় |
| 📄 **Pages** | Page Tabs | একাধিক পেজ তৈরি (যেমন Excel-এর শিট) |

### তিনটি ভিউ (বাঁ পাশে আইকন):

1. **📊 Report View** — রিপোর্ট তৈরি ও ডিজাইন (ডিফল্ট)
2. **📋 Data View** — কাঁচা ডেটা টেবিল আকারে দেখা
3. **🔗 Model View** — টেবিলের মধ্যে সম্পর্ক (Relationships) দেখা

---

## ৩. প্রথম রিপোর্ট: CSV থেকে ডেটা সংযোগ

### ধাপ ১: ডেমো CSV ফাইল তৈরি করুন

নিচের ডেটা Notepad এ কপি করে `finance_data.csv` নামে সেভ করুন:

```csv
Date,Product,Category,Revenue,Cost,Profit
01-Jan-2024,Laptop,Electronics,50000,35000,15000
01-Jan-2024,Mouse,Electronics,1200,800,400
02-Jan-2024,Keyboard,Electronics,2500,1500,1000
03-Jan-2024,Monitor,Electronics,35000,25000,10000
04-Jan-2024,Chair,Furniture,15000,9000,6000
05-Jan-2024,Desk,Furniture,25000,15000,10000
06-Jan-2024,Laptop,Electronics,52000,36000,16000
07-Jan-2024,Tablet,Electronics,18000,12000,6000
08-Jan-2024,Printer,Electronics,12000,8000,4000
09-Jan-2024,Bookshelf,Furniture,8000,5000,3000
10-Jan-2024,LED Light,Electronics,3000,1800,1200
```

### ধাপ ২: Power BI তে CSV ইম্পোর্ট

1. **Home** রিবন → **Get Data** → **Text/CSV** ক্লিক করুন
2. আপনার `finance_data.csv` ফাইল সিলেক্ট করুন → **Open**
3. Preview উইন্ডো আসবে — ডেটা ঠিক মতো দেখালে **Load** ক্লিক করুন

> **❗ সমস্যা হলে:**
> - এনকোডিং: যদি বাংলা/ইংরেজি ঠিক না দেখায়, **File Origin** থেকে **UTF-8** সিলেক্ট করুন
> - ডিলিমিটার: **Comma** সিলেক্টেড কিনা চেক করুন

### ধাপ ৩: Fields পেন চেক

ডান পাশে Fields পেনে এখন দেখাবে:
- ✅ Date
- ✅ Product
- ✅ Category
- ✅ Revenue
- ✅ Cost
- ✅ Profit

প্রতিটি কলামের পাশে সিগমা (∑) আইকন = Numeric কলাম। না থাকলে Text কলাম।

### ধাপ ৪: প্রথম ভিজুয়াল — টেবিল

1. Visualizations পেনে **টেবিল আইকন** (📋) ক্লিক করুন
2. Fields থেকে **Product** এবং **Revenue** চেক করুন
3. ক্যানভাসে টেবিল তৈরি হবে

### ধাপ ৫: টাইটেল ও ফরম্যাটিং

1. টেবিল সিলেক্ট করুন
2. Visualizations পেনের নিচে **Format** (🎨) আইকন ক্লিক করুন
3. **Title** → **On** → লিখুন "পণ্য অনুযায়ী রাজস্ব"

---

## 🧪 প্র্যাকটিস টাস্ক

### টাস্ক ১: ফিল্টারিং
Fields পেন থেকে **Category** ড্র্যাগ করুন **Filters on this page** এ। শুধু "Electronics" দেখান।

### টাস্ক ২: সর্টিং
টেবিলের **Revenue** হেডারে ক্লিক করুন — বড় থেকে ছোট (Descending) সাজান।

### টাস্ক ৩: নম্বর ফরম্যাট
Revenue কলাম সিলেক্ট করুন → **Column tools** রিবন → **Format** → **Currency ($)** সিলেক্ট করুন।

### টাস্ক ৪: নতুন পেজ
নিচের ➕ বাটনে ক্লিক করে নতুন পেজ যোগ করুন। নাম দিন "Summary"।

---

## ✅ আজকের শেখা

| বিষয় | শিখলেন |
|------|--------|
| Power BI Desktop ইন্সটল | ✅ |
| ইন্টারফেস চেনা (Ribbon, Canvas, Fields) | ✅ |
| CSV ফাইল থেকে ডেটা আনা | ✅ |
| টেবিল ভিজুয়াল তৈরি | ✅ |
| বেসিক ফরম্যাটিং | ✅ |

> [!TIP]
> 🔥 **পরবর্তী ধাপ:** কাল শিখবেন বার চার্ট, লাইন চার্ট, পাই চার্ট — ডেটা ভিজুয়ালাইজেশনের মজার জিনিস!

---

*📸 Screenshot Placeholder: Power BI Desktop main interface with CSV loaded*
*📸 Screenshot Placeholder: Table visual showing Product and Revenue*