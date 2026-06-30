# দিন ৩: Branching & Merging

## Branch (শাখা) কী?

Branch হচ্ছে Git-এর একটি **প্যারালাল ভার্সন**। main ব্রাঞ্চ থেকে আলাদা করে নতুন কাজ করা যায়, পরে সেটি main-এ মージ করা যায়।

**কল্পনা করুন:** main হচ্ছে আপনার পাবলিশ হওয়া ফাইনাল রিপোর্ট, আর branch হচ্ছে আপনার ড্রাফট কপি — যেখানে আপনি নির্বিঘ্নে কাজ করতে পারেন।

## Data Analyst-এর জন্য Branch-এর ব্যবহার

- **experiment ব্রাঞ্চে** নতুন এনালাইসিস টেস্ট করা
- **feature ব্রাঞ্চে** আলাদা ডাটা সোর্স নিয়ে কাজ করা
- **fix ব্রাঞ্চে** বাগ ফিক্স করা main-এ প্রভাব না ফেলে

## Branch কমান্ড

### নতুন ব্রাঞ্চ তৈরি:
```bash
# নতুন ব্রাঞ্চ তৈরি
git branch experiment-analysis

# সব ব্রাঞ্চ দেখা
git branch
# * main (বর্তমান ব্রাঞ্চের পাশে * থাকে)
```

### ব্রাঞ্চ সুইচ করা:
```bash
# experiment-analysis ব্রাঞ্চে যাওয়া
git checkout experiment-analysis

# আবার main-এ ফিরে আসা
git checkout main
```

### এক লাইনে ব্রাঞ্চ তৈরি ও সুইচ:
```bash
git checkout -b new-feature
# উপরের কমান্ড একসঙ্গে branch তৈরি ও checkout করে
```

## Merging (মার্জিং)

কোনো ব্রাঞ্চের কাজ শেষ হলে সেটি **main**-এ মার্জ করা হয়।

```bash
# প্রথমে main ব্রাঞ্চে আসুন
git checkout main

# তারপর মার্জ করুন
git merge experiment-analysis
```

### মার্জ কনফ্লিক্ট (Merge Conflict)

যখন দুই ব্রাঞ্চে একই ফাইলের একই লাইন পরিবর্তন হয়, তখন Git কনফ্লিক্ট দেখায়।

**সিগন্যাল:** Git বলে — "CONFLICT (content): Merge conflict in filename"

**সমাধান:**
1. ফাইলটি খুলুন
2. `<<<<<<<`, `=======`, `>>>>>>>` চিহ্নিত অংশ দেখুন
3. কোন ভার্সন রাখবেন তা ঠিক করুন
4. কনফ্লিক্ট চিহ্নগুলো মুছে ফেলুন
5. ফাইল স্টেজ ও commit করুন

```bash
# কনফ্লিক্ট সমাধানের পর
git add filename
git commit -m "মার্জ কনফ্লিক্ট সমাধান করা হয়েছে"
```

## প্র্যাকটিক্যাল উদাহরণ — Data Analyst-এর জন্য

```bash
# ১. কোড পরিবর্তন না করেই আলাদা ব্রাঞ্চে কাজ শুরু
cd sales-analysis
git checkout -b add-monthly-report

# ২. নতুন ফিচার নিয়ে কাজ
# monthly_report.py তৈরি ও edit

git add monthly_report.py
git commit -m "মাসিক রিপোর্ট ফিচার যোগ করা হয়েছে"

# ৩. main-এ ফিরে মার্জ
git checkout main
git merge add-monthly-report
```

## ব্রাঞ্চ ব্যবস্থাপনা

```bash
# ব্রাঞ্চ ডিলিট করা (মার্জ করার পর)
git branch -d add-monthly-report

# ফোর্স ডিলিট (মার্জ না করলেও)
git branch -D experiment-failed

# রিমোট ব্রাঞ্চ ডিলিট
git push origin --delete add-monthly-report
```

## ভালো Branch নামকরণ

| নাম | অর্থ |
|-----|------|
| `feature/sales-dashboard` | নতুন ফিচার |
| `fix/data-cleaning-bug` | বাগ ফিক্স |
| `experiment/ml-model` | পরীক্ষামূলক কাজ |
| `docs/update-readme` | ডকুমেন্টেশন |

## সারাংশ

| কমান্ড | কাজ |
|---------|------|
| `git branch <name>` | নতুন ব্রাঞ্চ |
| `git branch` | ব্রাঞ্চ লিস্ট |
| `git checkout <name>` | ব্রাঞ্চ পরিবর্তন |
| `git checkout -b <name>` | ব্রাঞ্চ তৈরি ও সুইচ |
| `git merge <name>` | ব্রাঞ্চ মার্জ |
| `git branch -d <name>` | ব্রাঞ্চ ডিলিট |

**পরবর্তী ধাপ:** দিন ৪-এ আমরা Remote Repo ও GitHub-এর সাথে কাজ করব।