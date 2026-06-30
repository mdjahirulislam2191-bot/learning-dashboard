# দিন ৬: .gitignore ও Branching Strategies

## .gitignore কী?

`.gitignore` একটি ফাইল যেখানে আপনি বলে দেন — "এই ফাইলগুলো Git ট্র্যাক করবে না।"

## কেন Data Analyst-দের .gitignore দরকার?

- **বড় ডাটাসেট** — CSV/Excel ফাইল (৫০০MB+) Git-এ রাখা উচিত না
- **সিক্রেট ফাইল** — API কী, পাসওয়ার্ড, ডাটাবেস কানেকশন
- **ক্যাশ/টেম্প ফাইল** — Python `__pycache__`, `.ipynb_checkpoints`
- **এনভায়রনমেন্ট** — `.env` ফাইল, virtual environment

## .gitignore ফাইল তৈরি

```bash
# প্রোজেক্টের root-এ .gitignore ফাইল তৈরি
touch .gitignore
```

### Data Analyst-দের জন্য স্ট্যান্ডার্ড .gitignore

```gitignore
# === Python ===
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
*.egg

# === Jupyter Notebook ===
.ipynb_checkpoints/
*.ipynb_checkpoints/

# === Data Files (বড় ফাইল) ===
*.csv
*.xlsx
*.xls
*.parquet
*.feather
*.pkl
*.h5
data/raw/
data/processed/
*.db
*.sqlite

# === Environment & Secrets ===
.env
.env.local
venv/
.venv/
env/

# === IDE & OS ===
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# === Logs & Reports ===
*.log
output/
reports/*.html
```

### ডাটা ফাইল নিয়ে সতর্কতা

🔴 **GitHub-এ বড় ফাইল Push করবেন না** — রিপোজিটরি স্লো হয়  
✅ ছোট নমুনা ডাটা (`sample_data.csv`) রাখতে পারেন  
✅ ডাটা পাবলিশ করার লিংক রাখুন README-এ  
✅ GitHub Large File Storage (LFS) ব্যবহার করতে পারেন

## Branching Strategies (ব্রাঞ্চিং স্ট্র্যাটেজি)

### ১. GitHub Flow (সহজ — সবার জন্য)

```
main
  └── feature-branch (কাজ)
         ↓
       PR → মার্জ → main
```

**নিয়ম:**  
- সব কাজ নতুন ব্রাঞ্চে  
- PR তৈরি করে main-এ মার্জ  
- দিনে কয়েকবার push/pull  
- Data Analyst-দের জন্য সেরা

### ২. Git Flow (জটিল — বড় টিমের জন্য)

```
master
  └── develop
        ├── feature/...
        └── release/...
```

**কখন ব্যবহার করবেন:** বড় প্রজেক্ট, নির্দিষ্ট রিলিজ সাইকেল

### ৩. Feature Branch Strategy (প্র্যাকটিক্যাল)

Data Analyst-দের জন্য উপযোগী:

```bash
# ফিচার ব্রাঞ্চ
feature/sales-dashboard
feature/customer-segment
feature/monthly-report

# ফিক্স ব্রাঞ্চ
fix/data-cleaning-bug
fix/wrong-aggregation

# এক্সপেরিমেন্ট
experiment/ml-model-v2
```

## Data Analyst-দের জন্য ব্রাঞ্চিং ওয়ার্কফ্লো

```bash
# ১. main থেকে ব্রাঞ্চ তৈরি
git checkout -b feature/monthly-sales

# ২. কাজ করুন, commit করুন
git add .
git commit -m "মাসিক সেলস এনালাইসিস ফাংশন"

# ৩. Push & PR
git push -u origin feature/monthly-sales

# ৪. GitHub-এ PR তৈরি (দিন ৫ দেখুন)

# ৫. মার্জ শেষে ব্রাঞ্চ ডিলিট
git checkout main
git pull
git branch -d feature/monthly-sales
```

## .gitignore টেস্ট করা

```bash
# .gitignore কাজ করছে কিনা চেক
git status

# যদি কোনো ফাইল track করা না থাকে, তাহলে সেটি .gitignore-এ আছে
```

## গুরুত্বপূর্ণ টিপস

🔹 `.gitignore` **প্রথম commit-এর আগে** তৈরি করুন  
🔹 ইতিমধ্যে tracked ফাইল .gitignore-এ যোগ করলে কাজ করবে না — `git rm --cached` দরকার  
🔹 প্রতিটি প্রজেক্টের জন্য আলাদা `.gitignore` বানান  
🔹 https://gitignore.io-এ গিয়ে আপনার টেক স্ট্যাক সিলেক্ট করে জেনারেট করতে পারেন

## সারাংশ

| বিষয় | কমান্ড/ব্যাখ্যা |
|------|----------------|
| `.gitignore` | কোন ফাইল Git ট্র্যাক করবে না তা নির্ধারণ |
| `git rm --cached <file>` | tracked ফাইল আনট্র্যাক করা |
| GitHub Flow | main + feature branch — সহজ ও কার্যকর |
| Feature branch | `feature/`, `fix/`, `experiment/` নামকরণ |

**পরবর্তী ধাপ:** দিন ৭-এ আমরা Collaboration Workflow শিখব।