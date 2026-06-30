# দিন ৪: Remote Repo ও GitHub

## Remote Repository কী?

Remote Repository হচ্ছে আপনার কোডের **অনলাইন কপি** — GitHub, GitLab, বা Bitbucket-এ হোস্ট করা। এটি আপনার লোকাল রিপোজিটোরির সাথে সংযুক্ত থাকে।

## কেন Remote দরকার?

1. **ব্যাকআপ** — কোড ক্লাউডে সেভ থাকে
2. **কলাবোরেশন** — টিম একসঙ্গে কাজ করতে পারে
3. **পোর্টফোলিও** — GitHub-এ আপনার কাজ দেখাতে পারেন
4. **যেকোনো জায়গা থেকে অ্যাক্সেস** — অফিস, বাসা, ল্যাপটপ

## GitHub-এ অ্যাকাউন্ট তৈরি

1. https://github.com-এ যান
2. Sign Up করে ফ্রি অ্যাকাউন্ট খুলুন
3. আপনার ইউজারনেম নোট করে রাখুন (যেমন: `johndoe`)

## নতুন Remote Repository তৈরি (GitHub)

1. GitHub-এ লগ ইন করুন
2. ➕ (New Repository) বাটনে ক্লিক করুন
3. রিপোজিটরি নাম দিন (যেমন: `sales-analysis`)
4. **Public** সিলেক্ট করুন (পোর্টফোলিওর জন্য)
5. "Create repository" ক্লিক করুন

## লোকাল রিপোজিটরি GitHub-এর সাথে সংযুক্ত করা

```bash
# remote যোগ করা
git remote add origin https://github.com/আপনার-ইউজারনেম/sales-analysis.git

# Remote চেক করা
git remote -v
# origin  https://github.com/... (fetch)
# origin  https://github.com/... (push)
```

## কোড Push করা (লোকাল → GitHub)

```bash
# প্রথম push (main ব্রাঞ্চ)
git push -u origin main

# পরবর্তী push
git push
```

`-u` (upstream) প্রথমবার ব্যবহার করা হয়, এরপর শুধু `git push` লিখলেই হবে।

## কোড Pull করা (GitHub → লোকাল)

```bash
# অন্য কারো পরিবর্তন আনা
git pull origin main
```

## ক্লোন করা (অন্যের রিপোজিটরি কপি)

```bash
# GitHub থেকে সম্পূর্ণ রিপোজিটরি ডাউনলোড
git clone https://github.com/username/repository-name.git

# নির্দিষ্ট ফোল্ডারে ক্লোন
git clone https://github.com/username/repo-name.git my-folder
```

## SSH কী সেটআপ (ঐচ্ছিক, কিন্তু সুবিধাজনক)

পাসওয়ার্ড বারবার না দিয়ে SSH ব্যবহার করতে পারেন।

```bash
# SSH কী তৈরি
ssh-keygen -t ed25519 -C "your-email@example.com"

# পাবলিক কী দেখা
cat ~/.ssh/id_ed25519.pub
```

তারপর GitHub-এ Settings → SSH and GPG keys → New SSH Key-তে পেস্ট করুন।

## Data Analyst-এর জন্য প্র্যাকটিক্যাল

```bash
# ১. GitHub-এ নতুন রিপো খোলার পর:
git remote add origin https://github.com/johndoe/sales-analysis.git

# ২. প্রথম push
git push -u origin main

# ৩. দৈনিক কাজ শেষে
git add .
git commit -m "আজকের এনালাইসিস আপডেট"
git push
```

## GitHub-এ আপনার রিপোজিটরি পেজ

GitHub-এ গেলে আপনি দেখবেন:
- আপনার সব ফাইল ও ফোল্ডার
- commit ইতিহাস
- README.md ফাইলটি রেন্ডার হয়ে দেখাবে
- Fork, Star, Issue, Pull Request অপশন

## গুরুত্বপূর্ণ টিপস

🔹 **প্রথমবার Push করলে** ইউজারনেম ও পাসওয়ার্ড চাইবে — GitHub Personal Access Token ব্যবহার করুন (পাসওয়ার্ডের বদলে)
🔹 **Token তৈরি:** GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
🔹 **আগে Pull, তারপর Push** — যদি কেউ আগে push করে থাকে

## সারাংশ

| কমান্ড | কাজ |
|---------|------|
| `git remote add origin <url>` | remote যোগ |
| `git remote -v` | remote লিস্ট |
| `git push -u origin main` | প্রথম push |
| `git push` | সাধারণ push |
| `git pull` | আপডেট নেওয়া |
| `git clone <url>` | রিপো ক্লোন |

**পরবর্তী ধাপ:** দিন ৫-এ আমরা Pull Requests ও Code Review সম্পর্কে শিখব।