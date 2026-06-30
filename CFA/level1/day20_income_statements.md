# 📘 Day 20: FSA — Income Statements

## 🎯 শেখার উদ্দেশ্য

এই পাঠ শেষে আপনি যা পারবেন:
1. আয় বিবরণীর (Income Statement) কাঠামো বুঝতে
2. রাজস্ব স্বীকৃতি (Revenue Recognition) বুঝতে
3. বিভিন্ন ধরনের ব্যয় চিহ্নিত করতে
4. মুনাফার বিভিন্ন স্তর বুঝতে (Gross, Operating, Net)
5. EPS (Earnings Per Share) গণনা করতে

---

## 📖 1. আয় বিবরণীর কাঠামো

**আয় বিবরণী (Income Statement):** একটি নির্দিষ্ট সময়ে কোম্পানির আর্থিক কর্মক্ষমতা দেখায়।

**মৌলিক কাঠামো:**
```
রাজস্ব (Revenue)
- বিক্রিত পণ্যের খরচ (COGS)
= মোট মুনাফা (Gross Profit)
- পরিচালন ব্যয় (Operating Expenses)
= পরিচালন মুনাফা (Operating Profit / EBIT)
- সুদ ব্যয় (Interest Expense)
+ সুদ আয় (Interest Income)
= কর পূর্ব মুনাফা (EBT)
- কর (Tax)
= নিট মুনাফা (Net Income)
```

---

## 📖 2. রাজস্ব স্বীকৃতি (Revenue Recognition)

**মূল নীতি:** রাজস্ব তখনই স্বীকৃত হয় যখন এটি অর্জিত (Earned) এবং প্রাপ্তিযোগ্য (Realizable) হয়।

**IFRS 15 / ASC 606 — ৫ ধাপ প্রক্রিয়া:**

| ধাপ | বিবরণ |
|-----|--------|
| ১ | গ্রাহকের সাথে চুক্তি চিহ্নিত করুন |
| ২ | চুক্তিতে কর্মদক্ষতার বাধ্যবাধকতা চিহ্নিত করুন |
| ৩ | লেনদেনের মূল্য নির্ধারণ করুন |
| ৪ | বাধ্যবাধকতায় মূল্য বরাদ্দ করুন |
| ৫ | বাধ্যবাধকতা পূরণ হলে রাজস্ব স্বীকৃতি দিন |

**উদাহরণ — ডেটা অ্যানালিস্ট:**
> একটি SaaS কোম্পানি $১২০০/বছরে সাবস্ক্রিপশন বিক্রি করে। কোম্পানি পুরো $১২০০ আজই স্বীকৃতি দিতে পারে না — প্রতি মাসে $১০০ করে স্বীকৃতি দিতে হবে (পরিষেবা দেওয়ার সাথে সাথে)।

---

## 📖 3. ব্যয়ের প্রকার (Types of Expenses)

### COGS (Cost of Goods Sold)
পণ্য উৎপাদনের সরাসরি খরচ — কাঁচামাল, শ্রম, কারখানা ওভারহেড।

### SG&A (Selling, General & Administrative)
বিক্রয়, বিপণন, প্রশাসনিক ব্যয় — যেমন বেতন, ভাড়া, ইউটিলিটি।

### D&A (Depreciation & Amortization)
দীর্ঘমেয়াদি সম্পদের খরচ বরাদ্দ — Depreciation (ভৌত সম্পদ), Amortization (অভৌত সম্পদ)।

### সুদ ও কর (Interest & Tax)
ঋণের খরচ ও সরকারকে প্রদেয় কর।

---

## 📖 4. মুনাফার বিভিন্ন স্তর

| স্তর | গণনা | অর্থ |
|------|------|------|
| **Gross Profit** | Revenue - COGS | মূল ব্যবসায়িক দক্ষতা |
| **Operating Profit (EBIT)** | Gross Profit - Operating Exp | পরিচালন দক্ষতা |
| **EBT** | EBIT - Interest + Interest Income | কর পূর্ব মুনাফা |
| **Net Income** | EBT - Tax | শেয়ারহোল্ডারদের জন্য অবশিষ্ট |

**মার্জিন (Margins):**
- **Gross Margin** = Gross Profit / Revenue
- **Operating Margin** = Operating Profit / Revenue
- **Net Margin** = Net Income / Revenue

**উদাহরণ:**
> কোম্পানি X: Revenue $১M, COGS $৬০০K, Op Exp $২৫০K
> Gross Profit = $৪০০K → Gross Margin = ৪০%
> Operating Profit = $১৫০K → Op Margin = ১৫%
> Net Income (কর ২০%) = $১২০K → Net Margin = ১২%

---

## 📖 5. EPS (Earnings Per Share)

**মৌলিক EPS:**
`EPS = (Net Income - Preferred Dividends) / Weighted Avg Common Shares`

**পাতলা EPS (Diluted EPS):**
সকল সম্ভাব্য শেয়ার (স্টক অপশন, কনভার্টিবল বন্ড) বিবেচনা করে।

**উদাহরণ:**
> Net Income = $৫০০K, Preferred Dividend = $৫০K, Shares = ২০০K
> Basic EPS = ($৫০০K - $৫০K) / ২০০K = **$২.২৫**

---

## ✍️ অনুশীলন (Practice Questions)

### প্রশ্ন ১:
কোম্পানি ABC: Revenue $২M, COGS $১.২M, SG&A $৪০۰K, Depreciation $১০০K, Interest $৫০K, Tax ২৫%। Net Income কত?

**সমাধান:**
Gross Profit = $২M - $১.২M = $৮০০K
EBIT = $৮০০K - $৪০০K - $১০০K = $৩০০K
EBT = $৩০০K - $৫০K = $২৫০K
Net Income = $২৫০K × (১-০.২৫) = **$১৮৭.৫K**

### প্রশ্ন ২:
কোম্পানির Net Income $১০M, Preferred Dividend $১M, ২M শেয়ার থাকলে Basic EPS কত?

**সমাধান:**
EPS = ($১০M - $১M) / ২M = **$৪.৫০**

### প্রশ্ন ৩:
Gross Margin ৪৫% এবং Revenue $৫০০K হলে COGS কত?

**সমাধান:**
Gross Profit = $৫০০K × ০.৪৫ = $২২৫K
COGS = $৫০০K - $২২৫K = **$২৭৫K**

---

## 📝 সূত্র সংক্ষেপ

| ধারণা | সূত্র |
|-------|-------|
| Gross Profit | Revenue - COGS |
| Operating Profit | GP - Operating Expenses |
| Net Income | Revenue - All Expenses |
| Basic EPS | (NI - Preferred Div) / Shares |
| Gross Margin | Gross Profit / Revenue |

---

**পড়ার সময়:** ৪৫ মিনিট
**অগ্রাধিকার:** 🔥🔥 খুব উচ্চ — FSA এর ভিত্তি