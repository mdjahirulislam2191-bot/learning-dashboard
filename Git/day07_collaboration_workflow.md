# দিন ৭: Collaboration Workflow — টিমে কাজ করা

## টিম কলাবোরেশন ওয়ার্কফ্লো

একটি ডাটা টিমে একসঙ্গে কাজ করার জন্য Git ও GitHub-এর সঠিক ব্যবহার জরুরি।

## ১. টিম প্রোজেক্ট সেটআপ

### টিম লিডার (Owner) যা করবেন:

```bash
# ১. GitHub-এ রিপোজিটরি তৈরি
# ২. লোকাল clone
git clone https://github.com/team/sales-analysis.git
cd sales-analysis

# ৩. README.md ও .gitignore যোগ
# ৪. প্রথম commit ও push
git add .
git commit -m "প্রাথমিক প্রজেক্ট সেটআপ"
git push
```

### টিম মেম্বাররা যা করবেন:

```bash
# ১. রিপোজিটরি fork (GitHub-এ)
# অথবা সরাসরি clone (যদি access থাকে)

# ২. Clone
git clone https://github.com/team/sales-analysis.git

# ৩. নিজের ব্রাঞ্চ তৈরি
git checkout -b feature/sarah-dashboard
```

## ২. GitHub-এ Collaborator যোগ করা

1. GitHub → Repository → Settings
2. Collaborators → Add people
3. টিম মেম্বারের ইউজারনেম বা ইমেইল দিন

## ৩. দিনের কাজ শুরু (Morning Routine)

```bash
# ১. main ব্রাঞ্চে যান
git checkout main

# ২. latest changes নিন
git pull origin main

# ৩. নতুন ব্রাঞ্চ তৈরি
git checkout -b feature/today-task
```

## ৪. কাজ করার সময়

```bash
# এনালাইসিস করছেন
# data_cleaning.py, visualization.py edit

# ছোট ছোট commit
git add data_cleaning.py
git commit -m "NULL ভ্যালু হ্যান্ডলিং ফিক্স"

git add visualization.py
git commit -m "সেলস ট্রেন্ড চার্ট যোগ"
```

## ৫. দিনের শেষে (End of Day)

```bash
# ব্রাঞ্চ Push
git push -u origin feature/today-task

# GitHub-এ PR তৈরি
# টিমকে জানান — "PR ready for review"
```

## ৬. Conflict সমাধান — টিম পরিবেশে

### Conflict এড়ানোর টিপস:
- প্রতিদিন সকালে `git pull` করুন
- বড় পরিবর্তনের আগে টিমের সাথে কথা বলুন
- আলাদা ফাইল বা আলাদা ফাংশনে কাজ করুন
- ছোট commit করুন (বড় পরিবর্তন কনফ্লিক্ট বাড়ায়)

### Conflict হলে:

```bash
# ১. main থেকে আপডেট নিন
git checkout main
git pull
git checkout feature/branch-name

# ২. main-কে আপনার ব্রাঞ্চে মার্জ করুন
git merge main

# ৩. Conflict সমাধান করুন (দিন ৩ দেখুন)
# ৪. Push করুন
git push
```

## ৭. Code Review কালচার

### Reviewer-এর জন্য টিপস:
- ২৪ ঘণ্টার মধ্যে রিভিউ দেওয়ার চেষ্টা করুন
- সম্মানজনক ভাষা ব্যবহার করুন
- "কেন পরিবর্তন করতে হবে" তা বুঝিয়ে বলুন
- শুধু ভুল না — ভালো কাজেরও প্রশংসা করুন

### রিভিউ কমেন্ট — বাংলায়:

```
👍 ভালো কাজ! ডাটা ক্লিনিং ফাংশন খুবই ক্লিন।

❌ একটা জিনিস: ফাইল পাথ হার্ডকোডেড। প্যারামিটার হিসেবে নিলে ভালো হয়।

🤔 চিন্তা: এই ফিল্টারটা কি Q1-এর জন্যও কাজ করবে?
```

## ৮. Data Analyst টিমের জন্য রিয়েল ওয়ার্কফ্লো

### সকাল ১০টা:
```bash
git checkout main
git pull origin main
git checkout -b feature/q4-report
```

### দুপুর ২টা (প্রথম commit):
```bash
git add q4_analysis.py
git commit -m "Q4 সেলস এনালাইসিস — বেসিক মেট্রিক্স"
git push -u origin feature/q4-report
```

### বিকাল ৫টা (PR তৈরি):
```bash
# GitHub → PR তৈরি
# টাইটেল: "Q4 সেলস রিপোর্ট — ড্যাশবোর্ড রেডি"
# মার্জ: Squash and merge
```

## ৯. টিম কমিউনিকেশন

### GitHub Issues ব্যবহার করুন:
- বাগ রিপোর্ট: "ডাটা ফিল্টার সঠিকভাবে কাজ করছে না"
- ফিচার রিকোয়েস্ট: "নতুন কাস্টমার সেগমেন্টেশন ফিচার চাই"
- প্রশ্ন: "sales_data.csv-এর কলাম নাম কী?"

### Project Board (GitHub Projects):
- **To Do** — কাজ শুরু করা হয়নি
- **In Progress** — চলমান কাজ
- **In Review** — রিভিউ অপেক্ষায়
- **Done** — সম্পন্ন

## সংক্ষিপ্ত — টিম কলাবোরেশন চেকলিস্ট

- [ ] GitHub রিপোজিটরি তৈরি
- [ ] টিম মেম্বার যোগ করা
- [ ] .gitignore সেটআপ
- [ ] Branching strategy ঠিক করা
- [ ] PR রিভিউ প্রক্রিয়া ফিক্স করা
- [ ] প্রতিদিন `git pull` করা
- [ ] ছোট commit করা
- [ ] PR-এ ভালো টাইটেল ও ডেসক্রিপশন দেওয়া

**পরবর্তী ধাপ:** দিন ৮-এ আমরা পোর্টফোলিও তৈরি করে GitHub-এ পুশ করব।