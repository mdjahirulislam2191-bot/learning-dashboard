# ✍️ Day 55: Quant Methods — Practice Questions

## 🎯 শেখার উদ্দেশ্য

এই পাঠে আমরা Day 53-54 (Correlation/Regression, Time Series) এর উপর ১৫টি MCQ অনুশীলন করব।

---

## 📝 Part 1: Correlation & Regression (Day 53)

### প্রশ্ন ১:
Correlation Coefficient -০.৮৫ মানে কী?

A) দুর্বল পজিটিভ সম্পর্ক
B) শক্তিশালী নেতিবাচক সম্পর্ক
C) কোনো সম্পর্ক নেই
D) নিখুঁত পজিটিভ সম্পর্ক

<details>
<summary>সমাধান</summary>
-০.৮৫ → শক্তিশালী নেতিবাচক সম্পর্ক (এক বাড়লে অপর কমে)।
**উত্তর: B**
</details>

### প্রশ্ন ২:
Cov(X,Y)=১৮, σx=৪, σy=৬। Correlation Coefficient কত?

A) ০.২৫
B) ০.৫০
C) ০.৭৫
D) ১.০০

<details>
<summary>সমাধান</summary>
r = ১৮ / (৪×৬) = ১৮/২৪ = **০.৭৫**
**উত্তর: C**
</details>

### প্রশ্ন ৩:
রিগ্রেশন সমীকরণ Y = ৫ + ২X। X=১৫ হলে Y-এর পূর্বাভাস কত?

A) ২০
B) ৩০
C) ৩৫
D) ৪৫

<details>
<summary>সমাধান</summary>
Y = ৫ + ২×১৫ = ৫ + ৩০ = **৩৫**
**উত্তর: C**
</details>

### প্রশ্ন ৪:
R² = ০.৮১ মানে কী?

A) X ও Y-এর মধ্যে Correlation ০.৮১
B) X, Y-এর ৮১% পরিবর্তন ব্যাখ্যা করে
C) মডেলটি ৮১% নির্ভুল
D) Error ১৯%

<details>
<summary>সমাধান</summary>
R² = ০.৮১ → Independent Variable, Dependent Variable-এর ৮১% পরিবর্তন ব্যাখ্যা করে। Simple Regression-এ r = √০.৮১ = ০.৯০।
**উত্তর: B**
</details>

### প্রশ্ন ৫:
রিগ্রেশন Hypothesis Test-এ H₀: b₁=০। p-value=০.০৩। ৯৫% Confidence-এ সিদ্ধান্ত কী?

A) H₀ গ্রহণ — কোনো সম্পর্ক নেই
B) H₀ প্রত্যাখ্যান — সম্পর্ক আছে
C) তথ্য অপর্যাপ্ত
D) H₀ গ্রহণ — সম্পর্ক আছে

<details>
<summary>সমাধান</summary>
p-value (০.০৩) < Significance Level (০.০৫) → H₀ Reject → সম্পর্ক আছে।
**উত্তর: B**
</details>

### প্রশ্ন ৬:
Durbin-Watson Statistic ০.৮ হলে কী নির্দেশ করে?

A) পজিটিভ Autocorrelation
B) নেগেটিভ Autocorrelation
C) No Autocorrelation
D) Heteroscedasticity

<details>
<summary>সমাধান</summary>
DW < ২ → Positive Autocorrelation (DW=২=No auto., DW<২=Positive, DW>২=Negative)।
**উত্তর: A**
</details>

### প্রশ্ন ৭:
নিচের কোনটি Correlation-এর সীমাবদ্ধতা?

A) সবসময় নির্ভুল
B) Correlation মানে Causation নয়
C) সবসময় Linear সম্পর্ক দেখায়
D) Outlier প্রভাবিত করে না

<details>
<summary>সমাধান</summary>
Correlation ≠ Causation — এটি সবচেয়ে গুরুত্বপূর্ণ সীমাবদ্ধতা।
**উত্তর: B**
</details>

### প্রশ্ন ৮:
F-test in Regression কী পরীক্ষা করে?

A) Intercept তাৎপর্যপূর্ণ কিনা
B) পুরো মডেল তাৎপর্যপূর্ণ কিনা
C) প্রতিটি Coefficient তাৎপর্যপূর্ণ কিনা
D) Data Normal কিনা

<details>
<summary>সমাধান</summary>
F-test মডেলের সামগ্রিক তাৎপর্য পরীক্ষা করে (সব Slope Coefficient একসাথে ০ কিনা)।
**উত্তর: B**
</details>

---

## 📝 Part 2: Time Series (Day 54)

### প্রশ্ন ৯:
স্টক প্রাইস: $৬০, $৬৩, $৬১, $৬৪, $৬৭। ৩-দিনের SMA (শেষ দিন) কত?

A) $৬২.০০
B) $৬৩.০০
C) $৬৪.০০
D) $৬৫.০০

<details>
<summary>সমাধান</summary>
SMA = ($৬১ + $৬৪ + $৬৭) / ৩ = $১৯২/৩ = **$৬৪.০০**
**উত্তর: C**
</details>

### প্রশ্ন ১০:
Random Walk মডেলের মূল বৈশিষ্ট্য কী?

A) পূর্বাভাসযোগ্য
B) ভবিষ্যতের পরিবর্তন অতীত থেকে স্বাধীন
C) সবসময় বাড়ে
D) Trend থাকে

<details>
<summary>সমাধান</summary>
Random Walk: Yt = Yt-1 + εt — ভবিষ্যতের পরিবর্তন (εt) অতীত থেকে স্বাধীন, তাই পূর্বাভাসযোগ্য নয়।
**উত্তর: B**
</details>

### প্রশ্ন ১১:
Stationary Time Series-এর বৈশিষ্ট্য নয় কোনটি?

A) Constant Mean
B) Constant Variance
C) Time-dependent Covariance
D) Constant Covariance (lag-এর উপর নির্ভরশীল)

<details>
<summary>সমাধান</summary>
Stationary Series-এ Covariance শুধু Lag-এর উপর নির্ভর করে, সময়ের উপর নয়। Time-dependent Covariance → Non-stationary।
**উত্তর: C**
</details>

### প্রশ্ন ১২:
কোন Transformations Non-stationary ডেটাকে Stationary করতে পারে?

A) Log Transformation
B) Differencing
C) Detrending
D) উপরের সবকটি

<details>
<summary>সমাধান</summary>
Log, Difference, Detrend — সবগুলোই Non-stationary ডেটাকে Stationary করতে পারে।
**উত্তর: D**
</details>

### প্রশ্ন ১৩:
Seasonality-র উদাহরণ কী?

A) ১০ বছরের অর্থনৈতিক চক্র
B) ডিসেম্বরে খুচরা বিক্রি বেড়ে যাওয়া
C) দীর্ঘমেয়াদি GDP বৃদ্ধি
D) COVID-19-এর প্রভাব

<details>
<summary>সমাধান</summary>
ডিসেম্বরে খুচরা বিক্রি বেড়ে যাওয়া = নির্দিষ্ট সময়ে পুনরাবৃত্তি প্যাটার্ন = Seasonality।
চক্র (Cycle) ≠ Seasonality — চক্র ২-১০ বছর, Seasonality ১ বছরের মধ্যে।
**উত্তর: B**
</details>

### প্রশ্ন ১৪:
Moving Average-এর মূল উদ্দেশ্য কী?

A) ভবিষ্যদ্বাণী করা
B) Noise/শব্দ কমানো এবং Trend দেখা
C) মুনাফা বের করা
D) Correlation গণনা করা

<details>
<summary>সমাধান</summary>
Moving Average দৈনিক ওঠানামা (Noise) কমিয়ে ট্রেন্ড বের করতে সাহায্য করে।
**উত্তর: B**
</details>

### প্রশ্ন ১৫:
Unit Root Test (Dickey-Fuller)-এ H₀ কী?

A) Time Series Stationary
B) Time Series-এ Unit Root আছে (Non-stationary)
C) No Autocorrelation
D) Regression তাৎপর্যপূর্ণ

<details>
<summary>সমাধান</summary>
Dickey-Fuller Test: H₀ = Unit Root আছে (Non-stationary)। p-value < ০.০৫ হলে H₀ Reject → Stationary।
**উত্তর: B**
</details>

---

## 📊 স্কোর টেবিল

| সঠিক | স্তর | সুপারিশ |
|-------|------|----------|
| ১৫ | 🏆 নিপুণ | ✅ পরবর্তী টপিকে যান |
| ১২-১৪ | ✅ ভালো | দুর্বল টপিক রিভিউ করুন |
| ৯-১১ | ⚠️ মাঝারি | আরও অনুশীলন প্রয়োজন |
| ৮ বা কম | 🔴 দুর্বল | Day 53-54 পুনরায় পড়ুন |

## 📝 উত্তর চাবি

| Q | Ans | টপিক | Q | Ans | টপিক |
|---|-----|------|---|-----|------|
| ১ | B | Correlation | ৯ | C | SMA |
| ২ | C | Correlation | ১০ | B | Random Walk |
| ৩ | C | Regression | ১১ | C | Stationarity |
| ৪ | B | R² | ১২ | D | Transformation |
| ৫ | B | Hypothesis | ১৩ | B | Seasonality |
| ৬ | A | Durbin-Watson | ১৪ | B | Moving Avg |
| ৭ | B | Correlation | ১৫ | B | Unit Root |
| ৮ | B | F-test | | | |

---

**পড়ার সময়:** ৪৫ মিনিট
**লক্ষ্য:** ৮০% (১২/১৫) সঠিক