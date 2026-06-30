# 📘 Day 57: Economics — Economic Growth

## 🎯 শেখার উদ্দেশ্য

এই পাঠ শেষে আপনি যা পারবেন:
1. অর্থনৈতিক প্রবৃদ্ধি কী ও কেন গুরুত্বপূর্ণ বুঝতে
2. উৎপাদন ফাংশন বুঝতে
3. Solow Growth Model বুঝতে
4. টেকসই প্রবৃদ্ধির উপাদান বুঝতে
5. প্রযুক্তি ও প্রবৃদ্ধির সম্পর্ক বুঝতে

---

## 📖 1. অর্থনৈতিক প্রবৃদ্ধি (Economic Growth)

**অর্থনৈতিক প্রবৃদ্ধি:** একটি দেশের পণ্য ও সেবা উৎপাদনের ক্ষমতার বৃদ্ধি — সাধারণত Real GDP-র পরিবর্তন দিয়ে মাপা হয়।

### GDP Growth Rate গণনা

**Growth Rate = (GDPt - GDPt-1) / GDPt-1 × ১০০**

**উদাহরণ:**
> ২০২২ Real GDP = $৩০০B, ২০২৩ Real GDP = $৩১৫B
> Growth = ($৩১৫B - $৩০০B) / $৩০০B × ১০০ = ১৫/৩০০ × ১০০ = **৫%**

### Nominal vs Real GDP Growth

| ধরণ | ব্যাখ্যা | উদাহরণ |
|-----|---------|---------|
| **Nominal Growth** | মূল্য পরিবর্তন অন্তর্ভুক্ত | GDP $৩০০B→$৩৩০B = ১০% |
| **Real Growth** | মুদ্রাস্ফীতি বাদ দিয়ে প্রকৃত বৃদ্ধি | GDP $৩০০B→$৩১৫B = ৫% |
| **GDP Deflator** | মূল্য স্তরের পরিবর্তন | ৩৩০/৩১৫ × ১০০ = ১০৪.৭৬ |

### কেন প্রবৃদ্ধি গুরুত্বপূর্ণ?

| কারণ | ব্যাখ্যা |
|------|---------|
| **জীবনযাত্রার মান উন্নতি** | বেশি GDP → বেশি আয় → ভালো জীবন |
| **Compound Effect** | ছোট Growth Rate দীর্ঘমেয়াদে বড় পরিবর্তন আনে |
| **Rule of ৭০** | দ্বিগুণ হতে সময় = ৭০ / Growth Rate |

**Rule of 70 উদাহরণ:**
> দেশ A: Growth Rate ৭% → ৭০/৭ = **১০ বছরে দ্বিগুণ**
> দেশ B: Growth Rate ৩.৫% → ৭০/৩.৫ = **২০ বছরে দ্বিগুণ**
>
> ৪০ বছর পর:
> দেশ A: ১×(১.০৭)⁴⁰ = **১৫ গুণ**
> দেশ B: ১×(১.০৩৫)⁴⁰ = **৪ গুণ**

---

## 📖 2. উৎপাদন ফাংশন (Production Function)

**উৎপাদন ফাংশন:** একটি অর্থনীতি কতটুকু উৎপাদন করে তা নির্ধারণকারী উপাদানসমূহ।

### Cobb-Douglas Production Function

**Y = A × F(L, K)**

বা বিশেষভাবে: **Y = A × K^α × L^(1-α)**

যেখানে:
- Y = Total Output (GDP)
- A = Total Factor Productivity (প্রযুক্তি)
- K = Capital (মূলধন — মেশিন, কারখানা, অবকাঠামো)
- L = Labor (শ্রমিক)
- α = Capital's Share of Income (০ থেকে ১)

### Per Capita আকারে

**y = A × k^α**

যেখানে y = Y/L (Per Capita Output), k = K/L (Per Capita Capital)

**উদাহরণ:**
> α = ০.৩ (Capital Share ৩০%), A=২, K=$৫০০B, L=১০M
>
> Y = ২ × ($৫০০B)^০.৩ × (১০M)^০.৭
>
> Per Capita: k = $৫০০B/১০M = $৫০,০০০
> y = ২ × ($৫০,০০০)^০.৩
>
> *বিশেষ নোট:* α=০.৩ মানে Capital ১০% বাড়লে Output বাড়ে ৩% (উৎপাদনের diminishing returns)।

---

## 📖 3. Solow Growth Model

**Solow Model:** একটি দেশের দীর্ঘমেয়াদি অর্থনৈতিক প্রবৃদ্ধি নির্ধারণকারী উপাদান ব্যাখ্যা করে।

### Solow Model-এর মূল ধারণা

| ধারণা | ব্যাখ্যা |
|-------|---------|
| **Steady State** | দীর্ঘমেয়াদে অর্থনীতি একটি ভারসাম্যে পৌঁছায় |
| **Capital Accumulation** | বিনিয়োগ Capital Stock বাড়ায় |
| **Depreciation** | Capital প্রতিবছর কিছুটা ক্ষয় হয় |
| **Diminishing Returns** | Capital বাড়ালে Marginal Product কমে |

### Solow Diagram

```
Output (Y)
  ↑
  |  Production Function: Y = Af(k)
  |     /
  |    /  ← Saving/Investment: sf(k)
  |   /
  |  /
  | / ← Depreciation: δk
  |/
  +----|--------------------→ Capital (k)
       k*
       (Steady State)
```

**Steady State Conditions:**
- Investment = Depreciation (sf(k*) = δk*)
- Per Capita Output Constant
- Total Output grows at Population Rate

**Convergence Hypothesis:**
> ধনী দেশ ও গরিব দেশের মধ্যে পার্থক্য কমতে থাকে — গরিব দেশ দ্রুত বাড়ে (Catch-up Effect)।
>
> **Conditional Convergence:** শুধুমাত্র একই প্রযুক্তি, সেভিংস রেট, এবং জনসংখ্যা বৃদ্ধির হারের দেশগুলোর মধ্যে।

---

## 📖 4. প্রবৃদ্ধির উপাদান (Sources of Growth)

### Growth Accounting

GDP Growth = 
- Labor Growth Contribution
- Capital Growth Contribution
- Total Factor Productivity (TFP) Growth

**Growth Accounting Equation:**
%ΔY = %ΔA + α × %ΔK + (1-α) × %ΔL

**উদাহরণ — Growth Accounting:**
> দেশ XYZ:
> - GDP Growth = ৬%
> - Capital Growth = ৫%, α=০.৩
> - Labor Growth = ২%, (1-α)=০.৭
> - TFP Growth = ?
>
> ৬% = %ΔA + ০.৩×৫% + ০.৭×২%
> ৬% = %ΔA + ১.৫% + ১.৪%
> %ΔA = ৬% - ২.৯% = **৩.১%**
>
> অর্থ: GDP Growth-এর ৩.১% প্রযুক্তি/দক্ষতা বৃদ্ধির কারণে হয়েছে।

### প্রবৃদ্ধির চালিকাশক্তি

| উপাদান | ব্যাখ্যা | উদাহরণ |
|--------|---------|---------|
| **Capital Deepening** | Per Worker Capital বৃদ্ধি | নতুন মেশিন, কারখানা |
| **Labor Force Growth** | শ্রমশক্তির সংখ্যা বৃদ্ধি | জনসংখ্যা বৃদ্ধি, ইমিগ্রেশন |
| **Human Capital** | শিক্ষা, দক্ষতা, স্বাস্থ্য | প্রশিক্ষিত কর্মী |
| **Technology (TFP)** | প্রযুক্তি ও দক্ষতা উন্নতি | AI, Automation |
| **Institutions** | আইন, সম্পত্তির অধিকার, শাসন | দুর্বল শাসন Growth কমায় |

**উদাহরণ — Human Capital:**
> ১ বছর শিক্ষা বৃদ্ধি → দীর্ঘমেয়াদি GDP বৃদ্ধি ৪-৭% (অনুমান)
> দক্ষ কর্মী → বেশি Productivity → বেশি GDP

---

## 📖 5. প্রযুক্তি ও প্রবৃদ্ধি (Technology & Growth)

**Total Factor Productivity (TFP):** ইনপুট (K,L) একই থাকলেও আউটপুট বাড়ানো — প্রযুক্তি ও দক্ষতার কারণে।

### TFP উন্নতির উপায়

| উপায় | ব্যাখ্যা |
|-------|---------|
| **R&D বিনিয়োগ** | নতুন আবিষ্কার, পেটেন্ট |
| **প্রযুক্তি স্থানান্তর** | উন্নত দেশ থেকে প্রযুক্তি আনা |
| **Institutional Reform** | ভালো শাসন, সম্পত্তির অধিকার |
| **Open Trade** | আন্তর্জাতিক বাণিজ্য প্রযুক্তি আনে |

### Endogenous Growth Theory

Solow Model-এর বাইরে — প্রযুক্তি বাইরে থেকে আসে না, বরং অর্থনীতির ভেতর থেকেই তৈরি হয়।

| তত্ত্ব | মূল ধারণা |
|--------|-----------|
| **Solow (Exogenous)** | প্রযুক্তি বহির্গত — মডেলের বাইরে থেকে আসে |
| **Endogenous Growth** | প্রযুক্তি অর্থনীতির ভেতর থেকে আসে (R&D, শিক্ষা) |

### Sustainable Growth

**Sustainable Growth Rate:** মুদ্রাস্ফীতি না বাড়িয়ে সর্বোচ্চ Growth Rate।

**Sustainable Growth = Labor Force Growth + Labor Productivity Growth**

**উদাহরণ:**
> বাংলাদেশ:
> - Labor Force Growth = ২.২%
> - Productivity Growth = ৩.৫%
> - Sustainable Growth = **৫.৭%**
>
> যদি সরকার ৮% Growth চায়, কিন্তু Sustainable Growth ৫.৭% → মুদ্রাস্ফীতি বাড়বে।

---

## ✍️ অনুশীলন

### প্রশ্ন ১:
দেশের GDP $৫০০B, Capital $১২০০B, Labor ২০M, α=০.৪। Solow Model-এ Per Capita Output কত?

**সমাধান:**
k = $১২০০B / ২০M = $৬০,০০০
y = Y/L = $৫০০B / ২০M = **$২৫,০০০**

### প্রশ্ন ২:
Rule of 70 অনুযায়ী, ৫% Growth Rate-এ GDP দ্বিগুণ হতে কত বছর লাগে?

**সমাধান:**
৭০/৫ = **১৪ বছর**

### প্রশ্ন ৩:
GDP Growth=৪%, Capital Growth=৩% (α=০.৩), Labor Growth=১%। TFP Growth কত?

**সমাধান:**
%ΔA = ৪% - (০.৩×৩%) - (০.৭×১%)
%ΔA = ৪% - ০.৯% - ০.৭%
%ΔA = **২.৪%**

---

## 📊 মূল ধারণা সারাংশ

| ধারণা | কী-পয়েন্ট |
|-------|-----------|
| Economic Growth | Real GDP বৃদ্ধির হার |
| Production Function | Y = A × K^α × L^(1-α) |
| Solow Model | Steady State, Convergence |
| TFP | প্রযুক্তি ও দক্ষতা বৃদ্ধি |
| Rule of 70 | দ্বিগুণ হতে সময় = ৭০/Growth Rate |

---

**পড়ার সময়:** ৪৫ মিনিট
**লক্ষ্য:** প্রবৃদ্ধির মৌলিক তত্ত্ব, Solow Model, এবং Growth Accounting বুঝতে পারা