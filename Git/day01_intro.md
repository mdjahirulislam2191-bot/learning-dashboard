# দিন ১: Git পরিচিতি, ইনস্টল ও কনফিগারেশন

## Git কী?

**Git** একটি **ভার্সন কন্ট্রোল সিস্টেম (VCS)** যা আপনার কোড বা ফাইলের পরিবর্তন ট্র্যাক রাখে। এটি আপনাকে:

- ফাইলের পুরনো ভার্সনে ফিরে যেতে সহায়তা করে
- একই ফাইলে একাধিক লোক একসঙ্গে কাজ করতে পারে
- কোডের ইতিহাস সংরক্ষণ করে (কে, কী, কখন পরিবর্তন করেছে)

## কেন Data Analyst-দের Git দরকার?

- **এনালাইসিস স্ক্রিপ্ট ভার্সন করা** — Python/R/Jupyter নোটবুকের পরিবর্তন ট্র্যাক রাখা
- **টিম কলাবোরেশন** — অন্যের সাথে একসঙ্গে কোড ডেভেলপ করা
- **প্রজেক্ট ব্যাকআপ** — সব কোড GitHub-এ সেভ করা
- **পোর্টফোলিও তৈরি** — GitHub প্রোফাইলে আপনার কাজ দেখানো

## Git ইনস্টল করা

### Windows-এ ইনস্টল:
1. https://git-scm.com/download/win থেকে Git Download করুন
2. ইনস্টলার রান করে Next ক্লিক করুন (ডিফল্ট অপশন ঠিক আছে)
3. ইনস্টল শেষে Git Bash ওপেন করুন

### ইনস্টল পরীক্ষা:
```bash
git --version
# git version 2.40.0 (বা অন্য কোনো ভার্সন দেখাবে)
```

## কনফিগারেশন (প্রথমবার সেটআপ)

Git ব্যবহার করার আগে আপনার নাম ও ইমেইল সেট করতে হবে।

```bash
git config --global user.name "আপনার নাম"
git config --global user.email "আপনার-ইমেইল@example.com"
```

### কনফিগারেশন চেক করা:
```bash
git config --global --list
# output:
# user.name=আপনার নাম
# user.email=আপনার-ইমেইল@example.com
```

### অন্যান্য গুরুত্বপূর্ণ কনফিগারেশন:
```bash
# ডিফল্ট ব্রাঞ্চের নাম main সেট করা
git config --global init.defaultBranch main

# লাইন এন্ডিং কনফিগার (Windows ব্যবহারকারীদের জন্য)
git config --global core.autocrlf true
```

## ডিফল্ট টেক্সট এডিটর সেট করা (ঐচ্ছিক)

```bash
# VS Code ব্যবহার করতে চাইলে:
git config --global core.editor "code --wait"
```

## সারাংশ

| বিষয় | কমান্ড |
|-------|--------|
| ভার্সন চেক | `git --version` |
| নাম সেট | `git config --global user.name "নাম"` |
| ইমেইল সেট | `git config --global user.email "ইমেইল"` |
| কনফিগ দেখুন | `git config --global --list` |

**পরবর্তী ধাপ:** দিন ২-এ আমরা Git এর বেসিক কমান্ড শিখব — init, add, commit, status, log।