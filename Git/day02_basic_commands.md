# দিন ২: Git বেসিক কমান্ড (init, add, commit, status, log)

## ১. Git রিপোজিটরি তৈরি (git init)

```bash
# নতুন প্রজেক্ট ফোল্ডার তৈরি
mkdir my-data-project
cd my-data-project

# Git রিপোজিটরি শুরু করা
git init
```

`git init` একটি `.git` নামের লুকানো ফোল্ডার তৈরি করে — এখানেই Git সব ইতিহাস সংরক্ষণ করে।

## ২. ফাইল স্টেটাস চেক করা (git status)

```bash
git status
```

`git status` দেখায়:
- কোন ফাইল পরিবর্তন হয়েছে (modified)
- কোন ফাইল Git-এ যোগ করা হয়নি (untracked)
- কোন ফাইল commit-এর জন্য প্রস্তুত (staged)

## ৩. ফাইল স্টেজ করা (git add)

```bash
# একটি নির্দিষ্ট ফাইল যোগ করা
git add analysis.py

# একাধিক ফাইল যোগ করা
git add analysis.py data.csv

# সব ফাইল একসঙ্গে যোগ করা
git add .
```

**স্টেজিং (Staging)** মানে হচ্ছে Git-কে বলা — "এই ফাইলগুলো আমি commit করতে চাই"।

## ৪. পরিবর্তন সেভ করা (git commit)

```bash
git commit -m "প্রথম কমিট — ডাটা এনালাইসিস স্ক্রিপ্ট যোগ করা হয়েছে"
```

**Commit** মানে হচ্ছে — ফাইলের বর্তমান অবস্থার একটি স্ন্যাপশট সেভ করে রাখা।

### ভালো commit message লেখার টিপস:
- সংক্ষিপ্ত ও অর্থপূর্ণ হতে হবে
- কী পরিবর্তন হয়েছে তা বোঝাতে হবে
- বাংলা বা ইংরেজি — দুটোই ব্যবহার করতে পারেন

## ৫. ইতিহাস দেখা (git log)

```bash
git log
# সম্পূর্ণ commit ইতিহাস দেখায়

git log --oneline
# সংক্ষিপ্ত আকারে (প্রতি commit একটি লাইনে)

git log --oneline --graph
# ব্রাঞ্চ সহ গ্রাফ ভিউ
```

## প্র্যাকটিক্যাল উদাহরণ — Data Analyst-এর জন্য

```bash
# ১. প্রজেক্ট ফোল্ডার তৈরি
mkdir sales-analysis
cd sales-analysis

# ২. Git শুরু
git init

# ৩. কিছু ফাইল তৈরি
# sales_data.csv, analysis.py, README.md

# ৪. স্টেটাস চেক
git status

# ৫. ফাইল স্টেজ
git add sales_data.csv analysis.py README.md

# ৬. commit
git commit -m "প্রাথমিক সেটআপ: CSV ডাটা ও এনালাইসিস স্ক্রিপ্ট"
```

## বাংলা commit message-এর উদাহরণ

```bash
git commit -m "সেলস ডাটা ক্লিনিং ফাংশন যোগ করা হয়েছে"
git commit -m "ডাটা ভিজুয়ালাইজেশন চার্ট আপডেট"
git commit -m "README-তে প্রজেক্ট ডকুমেন্টেশন যোগ"
```

## সারাংশ

| কমান্ড | কাজ |
|---------|------|
| `git init` | নতুন রিপোজিটরি শুরু |
| `git status` | ফাইলের বর্তমান অবস্থা দেখে |
| `git add <file>` | ফাইল স্টেজ করে |
| `git add .` | সব ফাইল স্টেজ করে |
| `git commit -m "msg"` | পরিবর্তন সেভ করে |
| `git log` | commit ইতিহাস দেখে |

## সাধারণ সমস্যা ও সমাধান

**প্রব্লেম:** `git commit` করলে "please tell me who you are" এরর দেখায়
**সলিউশন:** আগে নাম ও ইমেইল কনফিগার করুন (দিন ১ দেখুন)

**প্রব্লেম:** `git status`-এ অনেক ফাইল দেখাচ্ছে, কিন্তু সব commit করতে চাই না
**সলিউশন:** শুধু প্রয়োজনীয় ফাইল `git add` করুন, বাকিগুলো বাদ দিন

**পরবর্তী ধাপ:** দিন ৩-এ আমরা Branching & Merging শিখব।