# 📘 Day 54: Quant Methods — Time Series Analysis

## 🎯 শেখার উদ্দেশ্য

এই পাঠ শেষে আপনি যা পারবেন:
1. Time Series ডেটার বৈশিষ্ট্য বুঝতে
2. Trend, Seasonality, Cycle বুঝতে
3. Smoothing Techniques বুঝতে
4. Autocorrelation বুঝতে
5. Stationarity ও Random Walk বুঝতে

---

## 📖 1. Time Series কী?

**Time Series:** সময়ের সাথে সাথে সংগ্রহ করা ডেটার সিরিজ — যেমন দৈনিক স্টক প্রাইস, মাসিক GDP, বার্ষিক বিক্রয়।

| বৈশিষ্ট্য | সময় সিরিজ | ক্রস-সেকশনাল |
|-----------|------------|---------------|
| ডেটা সংগ্রহ | সময় অনুযায়ী | একক সময়ে |
| উদাহরণ | স্টক প্রাইস (জানু-ডিসেম্বর) | ১০০ টি স্টকের আজকের দাম |
| অর্ডার | গুরুত্বপূর্ণ (সময়ের ক্রম) | গুরুত্বপূর্ণ নয় |

### Time Series-এর উপাদান

```
Time Series = Trend + Cyclical + Seasonal + Irregular
```

| উপাদান | বর্ণনা | উদাহরণ |
|--------|--------|---------|
| **Trend (দীর্ঘমেয়াদি প্রবণতা)** | দীর্ঘমেয়াদি ঊর্ধ্ব/নিম্নগামী Movement | S&P 500 দীর্ঘমেয়াদি বাড়ছে |
| **Seasonal (মৌসুমি)** | নির্দিষ্ট সময়ে পুনরাবৃত্তি প্যাটার্ন | ডিসেম্বরে খুচরা বিক্রি বাড়ে |
| **Cyclical (চক্রাকার)** | অর্থনৈতিক চক্রের সাথে সম্পর্কিত (২-১০ বছর) | রিয়েল এস্টেট চক্র |
| **Irregular (অনিয়মিত)** | এলোমেলো, অপ্রত্যাশিত পরিবর্তন | COVID-19-এর প্রভাব |

**ট্রেন্ড বিশ্লেষণ উদাহরণ:**
> একটি কোম্পানির বার্ষিক বিক্রয় ($M):
> ২০১৯: $১০০, ২০২০: $১০৫, ২০২১: $১১২, ২০২২: $১২০, ২০২৩: $১৩০
> 
> Linear Trend: প্রতি বছর গড়ে $৭.৫M বৃদ্ধি পাচ্ছে
> ২০২৪-এর পূর্বাভাস: $১৩০ + $৭.৫ = **$১৩৭.৫M**

---

## 📖 2. Moving Average (চলন্ত গড়)

**Moving Average:** সাম্প্রতিক ডেটা পয়েন্টের গড় নিয়ে ট্রেন্ড বের করা — শব্দ (Noise) কমায়।

### Simple Moving Average (SMA)

SMAₙ = (Pt + Pt-1 + ... + Pt-n+1) / n

**উদাহরণ — ৫-দিনের SMA:**
> স্টক প্রাইস: $৫০, $৫২, $৫১, $৫৩, $৫৫, $৫৪, $৫৬
> 
> SMA(দিন ৫) = ($৫০+$৫২+$৫১+$৫৩+$৫৫)/৫ = **$৫২.২০**
> SMA(দিন ৬) = ($৫২+$৫১+$৫৩+$৫৫+$৫৪)/৫ = **$৫৩.০০**
> SMA(দিন ৭) = ($৫১+$৫৩+$৫৫+$৫৪+$৫৬)/৫ = **$৫৩.৮০**
> 
> SMA লাইন বাড়ছে → Uptrend ইঙ্গিত দিচ্ছে 📈

### Exponential Moving Average (EMA)

সাম্প্রতিক ডেটার বেশি গুরুত্ব দেয়।

EMA = Pt × α + EMAyesterday × (1 - α)

যেখানে α = Smoothing Factor = 2/(n+1)

**উদাহরণ — EMA:**
> স্টক প্রাইস: $১০০, n=১০ দিন, α=২/১১=০.১৮১৮
> EMA(দিন ১) = $১০০ (প্রথম মান)
> EMA(দিন ২) = $১০২×০.১৮১৮ + $১০০×০.৮১৮২ = $১৮.৫৪ + $৮১.৮২ = **$১০০.৩৬**
> 
> SMA সব ডেটাকে সমান গুরুত্ব দেয়, EMA সাম্প্রতিককে বেশি গুরুত্ব দেয়।

### Moving Average ব্যবহার

| ব্যবহার | ব্যাখ্যা |
|---------|---------|
| **ট্রেন্ড সনাক্তকরণ** | SMA বাড়ছে = Uptrend, কমছে = Downtrend |
| **Support/Resistance** | SMA টেকনিক্যাল অ্যানালিসিসে Support Level হিসেবে কাজ করে |
| **ক্রসওভার সিগন্যাল** | Short-term SMA > Long-term SMA → Buy Signal |
| **Noise Reduction** | দৈনিক ওঠানামা কমিয়ে ট্রেন্ড দেখা |

---

## 📖 3. Seasonality (মৌসুমি প্রভাব)

**Seasonality:** বছরের নির্দিষ্ট সময়ে নিয়মিত প্যাটার্ন।

**Seasonality সনাক্তকরণের পদ্ধতি:**

**১. Year-over-Year (YoY) তুলনা:**
> জানুয়ারি ২০২৪ বিক্রয় বনাম জানুয়ারি ২০২৩ — মাসিক Seasonality দূর করে।

**২. Seasonal Indices:**
> প্রতিটি মাসের গড় মান / মাসের সামগ্রিক গড়
> ডিসেম্বরের Index = ১.২৫ (ডিসেম্বরে ২৫% বেশি বিক্রি হয়)

**উদাহরণ — Seasonality Adjustment:**
> একটি আইসক্রিম কোম্পানির ত্রৈমাসিক বিক্রয় ($M):
> Q1: $১৫, Q2: $৩০, Q3: $৪০, Q4: $১৫
> 
> Seasonal Index:
> Q1: ১৫/২৫ = ০.৬০, Q2: ৩০/২৫ = ১.২০, Q3: ৪০/২৫ = ১.৬০, Q4: ১৫/২৫ = ০.৬০
> (গড় = ২৫)
> 
> Seasonally Adjusted Q3 = $৪০ / ১.৬০ = **$২৫** (Seasonality সরিয়ে ফেললে প্রকৃত ট্রেন্ড দেখা যায়)

---

## 📖 4. Autocorrelation (Serial Correlation)

**Autocorrelation:** একটি সময় সিরিজের বর্তমান মান ও অতীত মানের মধ্যে সম্পর্ক।

**Lag-k Autocorrelation:** Yt ও Yt-k-এর মধ্যে Correlation

| Lag | বর্ণনা | উদাহরণ |
|-----|--------|---------|
| Lag-1 | আজ ও গতকাল | আজকের রিটার্ন ও গতকালের রিটার্ন |
| Lag-2 | আজ ও ২ দিন আগে | আজকের রিটার্ন ও ২ দিন আগের রিটার্ন |

**Autocorrelation Interpretation:**

| Autocorrelation | অর্থ | সময় সিরিজের বৈশিষ্ট্য |
|----------------|------|----------------------|
| পজিটিভ | আজ যা ঘটছে, কালও তাই হওয়ার সম্ভাবনা | Trending/Momentum |
| নেতিবাচক | আজ বাড়লে কাল কমার সম্ভাবনা | Mean-Reversion |
| শূন্য | কোনো সম্পর্ক নেই | Random Walk |

**Durbin-Watson Statistic:**
Autocorrelation পরীক্ষার জন্য:
- DW ≈ ২ → No autocorrelation
- DW < ২ → Positive autocorrelation
- DW > ২ → Negative autocorrelation

---

## 📖 5. Stationarity (স্থিরতা) ও Random Walk

### Stationarity

**Stationary Time Series:** যে সিরিজের পরিসংখ্যানগত বৈশিষ্ট্য (গড়, ভ্যারিয়েন্স, Autocorrelation) সময়ের সাথে পরিবর্তিত হয় না।

**Stationary হওয়ার শর্ত:**
1. **Constant Mean:** গড় সময়ের সাথে পরিবর্তিত হয় না
2. **Constant Variance:** ভ্যারিয়েন্স সময়ের সাথে পরিবর্তিত হয় না
3. **Constant Covariance:** Covariance শুধু Lag-এর উপর নির্ভর করে, সময়ের উপর নয়

**কেন Stationarity গুরুত্বপূর্ণ?**
> অধিকাংশ Time Series মডেল (AR, MA, ARIMA) Stationary ডেটা প্রয়োজন। Non-stationary ডেটা ব্যবহার করলে Spurious Regression হতে পারে।

### Non-Stationarity Transformations

| পদ্ধতি | বিবরণ | উদাহরণ |
|--------|--------|---------|
| **Differencing** | Yt - Yt-1 | স্টক প্রাইস → Daily Return |
| **Log Transformation** | ln(Yt) | দ্রুত বাড়ছে এমন সিরিজ |
| **Detrending** | ট্রেন্ড সরানো | ট্রেন্ড লাইন থেকে বিচ্যুতি |

### Random Walk

**Random Walk:** ভবিষ্যতের পরিবর্তন অতীত থেকে স্বাধীন — পূর্বাভাস করা যায় না।

**Random Walk Model:**
Yt = Yt-1 + εt

যেখানে εt = White Noise (গড় ০, Constant Variance)

**Random Walk বৈশিষ্ট্য:**
1. Non-stationary (গড় পরিবর্তিত হয়)
2. Best forecast of tomorrow = Today's value
3. Returns are unpredictable

**উদাহরণ — স্টক প্রাইস:**
> Efficient Market Hypothesis অনুযায়ী, স্টক প্রাইস প্রায় Random Walk-এর মতো।
> 
> স্টক প্রাইস আজ $১০০:
> - কালকের Best Estimate = $১০০
> - পরিবর্তন (Return) = Random (পূর্বাভাসযোগ্য নয়)
> 
> ```
> Price
>  ↑
>  |    *--*    *--*--*
>  | *    *--* *        *--*
>  |                  *
>  +------------------------→ Time
> ```
> দেখতে Random কিন্তু কোনো Predictable Pattern নেই।

### Unit Root Test (Dickey-Fuller Test)

**H₀:** Time Series-এ Unit Root আছে (Non-stationary)
**Hₐ:** Time Series Stationary

- p-value < ০.০৫ → H₀ Reject → Stationary
- p-value > ০.০৫ → H₀ Fail to Reject → Non-stationary (Difference প্রয়োজন)

---

## ✍️ অনুশীলন

### প্রশ্ন ১:
স্টক প্রাইস: $৪৫, $৪৭, $৪৬, $৪৮, $৫০। ৩-দিনের SMA কত (শেষ দিন)?

**সমাধান:**
SMA = ($৪৬ + $৪৮ + $৫০) / ৩ = $১৪৪/৩ = **$৪৮**

### প্রশ্ন ২:
Random Walk-এ আগামীকালের সেরা পূর্বাভাস কী?

**উত্তর:** আজকের মান। Random Walk: Yt = Yt-1 + εt, তাই E[Yt+1] = Yt

### প্রশ্ন ৩:
Time Series Stationary না হলে কী সমস্যা?

**উত্তর:** Spurious Regression হতে পারে — দুটি অসম্পর্কিত ভেরিয়েবলের মধ্যে মিথ্যা সম্পর্ক পাওয়া যেতে পারে। Difference বা Log Transformation দিয়ে Stationary করতে হবে।

---

## 📊 মূল ধারণা সারাংশ

| ধারণা | কী-পয়েন্ট |
|-------|-----------|
| Time Series | সময় অনুযায়ী ডেটা |
| Moving Average | Trend বের করতে — SMA (সমান) vs EMA (সাম্প্রতিক বেশি গুরুত্ব) |
| Seasonality | নিয়মিত পুনরাবৃত্তি প্যাটার্ন |
| Autocorrelation | Yt ও Yt-k-এর সম্পর্ক |
| Stationarity | Constant Mean, Variance — মডেলিংয়ের জন্য প্রয়োজন |
| Random Walk | Unpredictable — Best forecast = Current Value |

---

**পড়ার সময়:** ৪৫ মিনিট
**লক্ষ্য:** Time Series-এর মূল ধারণা, Moving Average, এবং Stationarity বুঝতে পারা
