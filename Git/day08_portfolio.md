# দিন ৮: Portfolio — GitHub-এ আপনার প্রজেক্ট পুশ করুন

## কেন Data Analyst-দের GitHub Portfolio দরকার?

🔹 **চাকরি পাওয়া সহজ হয়** — রিক্রুটাররা আপনার কোড সরাসরি দেখতে পারে  
🔹 **আপনার দক্ষতা প্রমাণ করে** — শুধু CV-তে লেখা নয়, বাস্তব কাজ দেখান  
🔹 **নেটওয়ার্কিং** — অন্যান্য ডাটা প্রফেশনালদের সাথে সংযোগ  
🔹 **লার্নিং জার্নি** — আপনার অগ্রগতি ট্র্যাক করুন

## ধাপ ১: GitHub প্রোফাইল তৈরি

1. https://github.com-এ অ্যাকাউন্ট খুলুন
2. প্রোফাইল পিকচার আপলোড করুন
3. Bio লিখুন (যেমন: "Data Analyst | Python | SQL | Power BI")
4. Location, LinkedIn, Website যোগ করুন

## ধাপ ২: GitHub README Profile (স্পেশাল)

একটি বিশেষ রিপোজিটরি `username/username` তৈরি করলে GitHub আপনার প্রোফাইলের উপরে README দেখায়।

```bash
# GitHub-এ নতুন repo: আপনার-ইউজারনেম/আপনার-ইউজারনেম
# উদাহরণ: johndoe/johndoe
# Public করুন ✓
# README সহ তৈরি করুন
```

### প্রোফাইল README টেমপ্লেট (বাংলায়):

```markdown
# হ্যালো! 👋 আমি জন doe

## 🧑‍💻 Data Analyst | Python | SQL | Power BI

🔭 বর্তমানে কাজ করছি: সেলস ডাটা এনালাইসিস  
🌱 শিখছি: Machine Learning, Deep Learning  
💬 জিজ্ঞাসা করতে পারেন: Python, SQL, Data Visualization  
📫 ইমেইল: johndoe@email.com  
⚡ মজার তথ্য: আমি ডাটা থেকে গল্প বানাই!

## 🛠️ টেক স্ট্যাক
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- SQL (PostgreSQL, MySQL)
- Power BI / Tableau
- Git & GitHub

## 📊 Featured Projects
[🔗 Sales Dashboard](link) - বিক্রয় বিশ্লেষণ ড্যাশবোর্ড  
[🔗 Customer Segmentation](link) - কাস্টমার সেগমেন্টেশন  
[🔗 COVID-19 Analysis](link) - কোভিড ডাটা এনালাইসিস
```

## ধাপ ৩: পোর্টফোলিও প্রজেক্ট তৈরি

### আইডিয়া ১: সেলস ডাটা এনালাইসিস
```
sales-analysis/
├── data/
│   └── sample_sales.csv
├── notebooks/
│   └── sales_analysis.ipynb
├── scripts/
│   ├── data_cleaning.py
│   └── visualization.py
├── reports/
│   └── dashboard.pbix
├── .gitignore
└── README.md
```

### আইডিয়া ২: কাস্টমার সেগমেন্টেশন
```
customer-segmentation/
├── data/
├── notebooks/
├── src/
│   ├── preprocessing.py
│   ├── clustering.py
│   └── evaluation.py
├── .gitignore
└── README.md
```

### আইডিয়া ৩: COVID-19 ডাটা এনালাইসিস
```
covid19-analysis/
├── data/
├── notebooks/
├── scripts/
├── output/
│   └── charts/
├── .gitignore
└── README.md
```

## ধাপ ৪: প্রজেক্টে Push

```bash
# প্রতিটি প্রজেক্টের জন্য আলাদা রিপোজিটরি তৈরি

# ১. প্রজেক্ট ফোল্ডারে যান
cd ~/projects/sales-analysis

# ২. Git শুরু
git init
git add .
git commit -m "প্রথম commit — প্রোজেক্ট সেটআপ"

# ৩. GitHub-এ new repo তৈরি
# টিউটোরিয়াল: sales-analysis

# ৪. Remote & Push
git remote add origin https://github.com/username/sales-analysis.git
git push -u origin main
```

## ধাপ ৫: README.md — সবচেয়ে গুরুত্বপূর্ণ ফাইল

প্রতিটি প্রজেক্টের জন্য একটি ভালো README লিখুন:

```markdown
# 📊 সেলস ডাটা এনালাইসিস

## 📝 প্রোজেক্ট বিবরণ
এই প্রোজেক্টে আমি একটি ফার্মাসিউটিক্যাল কোম্পানির সেলস ডাটা 
এনালাইসিস করেছি। Pandas ও Matplotlib ব্যবহার করে ডাটা ক্লিনিং, 
এক্সপ্লোরেটরি এনালাইসিস ও ভিজুয়ালাইজেশন করা হয়েছে।

## 📂 ফাইল স্ট্রাকচার
- `data/sample_sales.csv` — নমুনা ডাটাসেট
- `notebooks/sales_analysis.ipynb` — Jupyter নোটবুক
- `scripts/data_cleaning.py` — ডাটা ক্লিনিং স্ক্রিপ্ট
- `scripts/visualization.py` — ভিজুয়ালাইজেশন স্ক্রিপ্ট

## 🛠️ প্রয়োজনীয় টুলস
- Python 3.11+
- Pandas
- NumPy
- Matplotlib
- Seaborn

## 📊 ফলাফল
![Sales Trend](images/sales_trend.png)
![Monthly Report](images/monthly_report.png)

## 🚀 কিভাবে চালাবেন
```bash
git clone https://github.com/username/sales-analysis.git
cd sales-analysis
pip install -r requirements.txt
python scripts/visualization.py
```

## 📫 যোগাযোগ
ইমেইল: johndoe@email.com  
LinkedIn: linkedin.com/in/johndoe
```

## ধাপ ৬: প্রজেক্ট শেয়ার করা

### পোর্টফোলিও দেখানোর জায়গা:

1. **LinkedIn** — Featured Section-এ প্রজেক্ট যুক্ত করুন
2. **জব অ্যাপ্লিকেশন** — CV-তে GitHub লিংক দিন
3. **পোর্টফোলিও ওয়েবসাইট** — GitHub Pages ব্যবহার করে
4. **ব্লগ** — Medium বা Dev.to-তে লেখা

## ধাপ ৭: GitHub স্ট্রিক বজায় রাখা

```bash
# প্রতিদিন কমপক্ষে ১টি commit
# GitHub গ্রিন স্কোয়ার দেখে !

# ছোট ছোট contribution:
# - ডকুমেন্টেশন আপডেট
# - বাগ ফিক্স
# - নতুন ফিচার
```

## চেকলিস্ট — পোর্টফোলিও রেডি?

- [ ] GitHub প্রোফাইল কমপ্লিট
- [ ] প্রোফাইল README তৈরি
- [ ] কমপক্ষে ৩টি ভালো প্রজেক্ট
- [ ] প্রতিটি প্রজেক্টে বিস্তারিত README
- [ ] প্রজেক্টে .gitignore আছে
- [ ] কোড পরিষ্কার ও কমেন্টেড
- [ ] LinkedIn-এ GitHub লিংক দেওয়া
- [ ] CV-তে GitHub লিংক দেওয়া

## Congratulations! 🎉

আপনি ৮ দিনের এই কোর্স শেষ করেছেন। এখন আপনি Git ও GitHub-এ দক্ষ।

### আপনি এখন যা পারেন:
✅ Git ইন্সটল ও কনফিগার  
✅ লোকাল রিপোজিটরি ম্যানেজ  
✅ Branching & Merging  
✅ GitHub-এ Push/Pull  
✅ Pull Request ও Code Review  
✅ .gitignore ও Branching Strategy  
✅ টিমে কলাবোরেশন  
✅ GitHub পোর্টফোলিও তৈরি

**শুভ কামনা!** আপনার ডাটা এনালাইসিস কেরিয়ার হোক সফল। 🚀