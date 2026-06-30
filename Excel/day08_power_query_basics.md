# দিন ৮: Power Query — ডেটা ইম্পোর্ট ও ক্লিনিং

## 🎯 আজকের লক্ষ্য
Power Query ব্যবহার করে বিভিন্ন উৎস থেকে ডেটা ইম্পোর্ট, ক্লিন ও ট্রান্সফর্ম করা শেখা।

## 🔌 Power Query কী?
Excel-এর একটি শক্তিশালী ডেটা সংযোগ ও ট্রান্সফরমেশন টুল যা বিভিন্ন উৎস থেকে ডেটা নিয়ে পরিষ্কার ও বিশ্লেষণের উপযোগী করে।

### পাওয়ার কোয়েরি কোথায়?
```
Data → Get Data (From various sources)
অথবা
Data → Get & Transform Data গ্রুপ
```

## 📥 ডেটা ইম্পোর্ট

### সমর্থিত উৎসসমূহ

#### ফাইল উৎস
```excel
From Excel Workbook     → .xlsx, .xls
From CSV/Text           → .csv, .txt
From XML                → .xml
From JSON               → .json
From Folder             → একাধিক ফাইল একসাথে
From PDF                → .pdf
```

#### ডেটাবেস উৎস
```excel
From SQL Server
From Microsoft Access
From Oracle
From MySQL
From PostgreSQL
```

#### অন্যান্য উৎস
```excel
From Web (URL)
From SharePoint
From OData Feed
From ODBC
Blank Query (খালি কোয়েরি)
```

## 🧹 ডেটা ক্লিনিং অপারেশন

### ১. কলাম অপারেশন
```excel
Remove Columns        → অপ্রয়োজনীয় কলাম মুছে ফেলা
Keep Columns          → প্রয়োজনীয় কলাম রাখা
Remove Duplicates     → ডুপ্লিকেট সারি মুছে ফেলা
Remove Rows           → অপ্রয়োজনীয় সারি মুছে ফেলা
```

### ২. রো অপারেশন
```excel
Remove Top Rows       → উপরের N সারি বাদ
Remove Bottom Rows    → নিচের N সারি বাদ
Keep Top Rows         → উপরের N সারি রাখা
Keep Range            → নির্দিষ্ট রেঞ্জ রাখা
Remove Blank Rows     → খালি সারি মুছে ফেলা
```

### ৩. ডেটা ট্রান্সফরমেশন
```excel
Split Column          → কলাম বিভক্ত (ডেলিমিটার দ্বারা)
Group By              → গ্রুপিং ও এগ্রিগেশন
Pivot Column          → কলাম উল্টানো
Unpivot Columns       → কলাম স্বাভাবিক করা
Replace Values        → মান প্রতিস্থাপন
Fill Down/Up          → খালি সেল পূরণ
Transpose             → সারি-কলাম অদলবদল
```

### ৪. ডেটা টাইপ পরিবর্তন
```excel
Data Type:
- Text → সংখ্যা/তারিখ রূপান্তর
- Number → টেক্সট রূপান্তর
- Date/Time → ফরম্যাট পরিবর্তন
- Currency → মুদ্রা ফরম্যাট
```

## 💼 ফাইন্যান্সে Power Query ব্যবহার

### উদাহরণ ১: ব্যাংক স্টেটমেন্ট ক্লিনিং
```excel
প্রবলেম: ব্যাংক থেকে CSV ফাইলে অনেক অপ্রয়োজনীয় ডেটা

Power Query ধাপ:
1. CSV ইম্পোর্ট → প্রথম ৫ সারি বাদ (হেডারের আগে)
2. শুধু প্রয়োজনীয় কলাম রাখা (তারিখ, বিবরণ, ডেবিট, ক্রেডিট)
3. ডেটা টাইপ পরিবর্তন (Date, Currency)
4. খালি সারি মুছে ফেলা
5. ডেবিট ও ক্রেডিট থেকে নেট ব্যালেন্স ক্যালকুলেশন
```

### উদাহরণ ২: একাধিক ফাইল মার্জ করা
```excel
প্রবলেম: ১২ মাসের বিক্রয় ডেটা আলাদা ফাইলে

সমাধান:
1. From Folder → ফোল্ডার সিলেক্ট
2. Combine & Load → Excel অটো সব ফাইল মার্জ করবে
3. মাসের নাম কলাম যোগ করা
4. ডেটা ক্লিন করে লোড
```

### উদাহরণ ৩: ওয়েব থেকে এক্সচেঞ্জ রেট
```excel
প্রবলেম: দৈনিক এক্সচেঞ্জ রেট দরকার

সমাধান:
1. From Web → URL দিন (যেমন: exchangerate-api.com)
2. JSON ডেটা পার্স করুন
3. শুধু প্রয়োজনীয় মুদ্রার রেট আনুন
4. আপনার Excel শীটে লোড করুন
```

## 🔧 M ভাষার পরিচিতি

### M ল্যাঙ্গুয়েজ কী?
Power Query-র পিছনের ফর্মুলা ভাষা — প্রতিটি অপারেশন M কোডে রূপান্তরিত হয়।

### সাধারণ M ফাংশন
```m
// মৌলিক অপারেশন
Table.SelectRows        → সারি ফিল্টার
Table.RemoveColumns     → কলাম মুছে ফেলা
Table.TransformColumnTypes → ডেটা টাইপ পরিবর্তন
Table.Group             → গ্রুপিং
Table.UnpivotOtherColumns → আনপিভট

// কাস্টম কলাম
Table.AddColumn(Source, "লাভ", each [বিক্রয়] - [খরচ])
```

### Advanced Editor
```
View → Advanced Editor
এখানে পুরো M কোড দেখা ও এডিট করা যায়
```

## 📋 Power Query Workflow

### সাধারণ ওয়ার্কফ্লো
```
১. সংযোগ (Connect)
   ↓
২. ট্রান্সফর্ম (Transform)
   ↓
৩. লোড (Load)
   ↓
৪. রিফ্রেশ (Refresh)
```

### লোড অপশন
```
Close & Load          → নতুন শীটে লোড
Close & Load To...    → গন্তব্য নির্ধারণ
- Table (নতুন শীট)
- PivotTable Report
- PivotChart
- Only Create Connection
- Add to Data Model
```

## ✅ প্র্যাকটিস টাস্ক
1. একটি CSV ফাইল ইম্পোর্ট করুন এবং ক্লিন করুন:
   - অপ্রয়োজনীয় কলাম বাদ
   - ডুপ্লিকেট মুছে ফেলা
   - ডেটা টাইপ ঠিক করা
2. একাধিক Excel ফাইল এক ফোল্ডার থেকে মার্জ করুন
3. Split Column ব্যবহার করে একটি কলাম বিভক্ত করুন
4. Group By দিয়ে মাসিক বিক্রয় যোগফল বের করুন
5. Unpivot ব্যবহার করে ডেটা লং ফরম্যাটে আনুন

## 📝 টিপস
- Power Query মৌলিক ডেটা পরিবর্তন করে না — শুধু রেফারেন্স
- **Applied Steps** প্যানেলে প্রতিটি ধাপ দেখা যায়
- ধাপের নাম পরিবর্তন করে অর্থপূর্ণ নাম দিন
- কোনো ধাপ মুছে ফেললে পরবর্তী ধাপগুলোর উপর প্রভাব পড়ে
- **Query Dependencies** দিয়ে কোয়েরির সম্পর্ক দেখা
- ডেটা রিফ্রেশ করতে **Data → Refresh All**
- Power Query শিখলে ডেটা ক্লিনিংয়ের সময় ৮০% কমে যায়

> **পরবর্তী দিন:** অ্যাডভান্সড ফর্মুলা — SUMIFS, COUNTIFS, অ্যারে ফর্মুলা!