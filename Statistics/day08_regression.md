# দিন ৮: রিগ্রেশন অ্যানালাইসিস — প্রাথমিক ধারণা (Regression Analysis Intro)

## 📊 ডেটা Analyst / Finance-এ আবেদন

### সারসংক্ষেপ
রিগ্রেশন অ্যানালাইসিস একটি পরিসংখ্যানিক পদ্ধতি যা ভেরিয়েবলের মধ্যে সম্পর্ক মডেল করে এবং ভবিষ্যদ্বাণী করতে সাহায্য করে। Finance-এ এটি সম্পদ মূল্যায়ন, ঝুঁকি পরিমাপ, এবং পূর্বাভাসে ব্যাপকভাবে ব্যবহৃত হয়।

---

## ১. লিনিয়ার রিগ্রেশন (Linear Regression)

**মূল ধারণা:** একটি নির্ভরশীল ভেরিয়েবল (Y) এবং এক বা একাধিক স্বাধীন ভেরিয়েবলের (X) মধ্যে রৈখিক সম্পর্ক স্থাপন।

### সরল লিনিয়ার রিগ্রেশন (Simple Linear Regression):
```
Y = β₀ + β₁X + ε
```

যেখানে,
- Y = Dependent variable (নির্ভরশীল)
- X = Independent variable (স্বাধীন)
- β₀ = Intercept (Y-অক্ষের ছেদক)
- β₁ = Slope (ঢাল — X-এ ১ ইউনিট পরিবর্তনে Y-এ পরিবর্তন)
- ε = Error term (ত্রুটি)

---

## ২. Finance উদাহরণ: স্টক রিটার্ন পূর্বাভাস

**প্রশ্ন:** S&P 500 রিটার্ন (X) ব্যবহার করে একটি স্টকের রিটার্ন (Y) পূর্বাভাস করা যায়?

| মাস | S&P 500 (X) | স্টক ABC (Y) |
|-----|-------------|--------------|
| 1 | 2% | 3% |
| 2 | 1% | 2% |
| 3 | -1% | -2% |
| 4 | 3% | 4% |
| 5 | 0% | 0.5% |

### ধাপ ১: Best Fit Line খোঁজা (OLS Method)

OLS = Ordinary Least Squares — ত্রুটির বর্গের যোগফল ন্যূনতম করে।

**সূত্র:**
```
β₁ = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²
β₀ = ȳ - β₁x̄
```

### ধাপ ২: মডেল ব্যাখ্যা

ধরি, β₀ = 0.2, β₁ = 1.1

```
Y = 0.2 + 1.1X
```

**ব্যাখ্যা:**
- β₀ = 0.2%: S&P 500 রিটার্ন 0% হলেও স্টক ABC-র প্রত্যাশিত রিটার্ন 0.2%
- β₁ = 1.1: S&P 500 1% বাড়লে স্টক ABC 1.1% বাড়ে (স্টকটি বেশি উদ্বায়ী)

### ধাপ ৩: পূর্বাভাস

S&P 500 রিটার্ন 2.5% হলে স্টক ABC-র প্রত্যাশিত রিটার্ন:
```
Y = 0.2 + 1.1(2.5) = 0.2 + 2.75 = 2.95%
```

---

## ৩. R-squared (R²) — মডেলের গুণগত মান

**সংজ্ঞা:** স্বাধীন ভেরিয়েবল নির্ভরশীল ভেরিয়েবলের কতটা ভ্যারিয়েশন ব্যাখ্যা করে।

```
R² = ব্যাখ্যাকৃত ভ্যারিয়েশন / মোট ভ্যারিয়েশন
R² = 1 — SSE / SST
```

| R² | ব্যাখ্যা |
|----|---------|
| 0.00 | মডেল কিছুই ব্যাখ্যা করে না |
| 0.25 | দুর্বল ফিট |
| 0.50 | মাঝারি ফিট |
| 0.75 | ভালো ফিট |
| 0.90+ | খুব ভালো ফিট (overfitting-এর ঝুঁকি) |

**উদাহরণ:** R² = 0.64 → S&P 500 স্টক ABC-র রিটার্নের 64% ভ্যারিয়েশন ব্যাখ্যা করে।

---

## ৪. Beta (β) — Finance-এর সবচেয়ে গুরুত্বপূর্ণ রিগ্রেশন

**CAPM মডেল (Capital Asset Pricing Model):**
```
Ri = Rf + βi(Rm — Rf)
```

**Beta (β)** স্টকের বাজার ঝুঁকি (Market Risk) পরিমাপ করে।

| Beta | অর্থ |
|------|------|
| β = 1 | বাজারের সমান উদ্বায়ী |
| β > 1 | বাজারের চেয়ে বেশি উদ্বায়ী (Aggressive) |
| β < 1 | বাজারের চেয়ে কম উদ্বায়ী (Defensive) |
| β = 0 | বাজার ঝুঁকি নেই (Risk-free) |
| β < 0 | বাজারের বিপরীতে চলে (Rare) |

**Finance উদাহরণ:**
- টেসলা (TSLA) β ≈ 2.0 → বাজার 1% বাড়লে টেসলা 2% বাড়ে
- ইউটিলিটি স্টক β ≈ 0.5 → বাজারের অর্ধেক উদ্বায়ী
- ট্রেজারি বিল β ≈ 0 → বাজার ঝুঁকি নেই

---

## ৫. মাল্টিপল রিগ্রেশন (Multiple Regression)

**একাধিক স্বাধীন ভেরিয়েবল সহ মডেল:**
```
Y = β₀ + β₁X₁ + β₂X₂ + … + βkXk + ε
```

**Finance উদাহরণ:** স্টক রিটার্ন পূর্বাভাস একাধিক ফ্যাক্টর দিয়ে:
```
Stock Return = β₀ + β₁(Market Return) + β₂(Interest Rate) + β₃(GDP Growth) + ε
```

**Fama-French 3-Factor Model:**
```
R = Rf + β₁(Rm — Rf) + β₂(SMB) + β₃(HML)
```
- SMB = Small Minus Big (আকার ফ্যাক্টর)
- HML = High Minus Low (মূল্য ফ্যাক্টর)

---

## ৬. রিগ্রেশন Assumptions (OLS)

| Assumption | বিবরণ | লঙ্ঘিত হলে |
|-----------|--------|------------|
| Linearity | সম্পর্ক রৈখিক | Non-linear models |
| Independence | Error স্বাধীন | Time-series issues |
| Homoscedasticity | ভ্যারিয়েন্স স্থির | Heteroscedasticity |
| Normality | Error Normal | Robust SE ব্যবহার |

---

## ✅ Python উদাহরণ

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Data
sp500 = np.array([2, 1, -1, 3, 0]).reshape(-1, 1)
stock_abc = np.array([3, 2, -2, 4, 0.5])

# Using sklearn
model = LinearRegression()
model.fit(sp500, stock_abc)

print(f"Intercept (β₀): {model.intercept_:.4f}")
print(f"Coefficient (β₁): {model.coef_[0]:.4f}")
print(f"R²: {model.score(sp500, stock_abc):.4f}")

# Prediction
pred = model.predict([[2.5]])
print(f"Predicted return at 2.5% market: {pred[0]:.2f}%")

# Using statsmodels (more detailed)
X = sm.add_constant(sp500)
sm_model = sm.OLS(stock_abc, X).fit()
print(sm_model.summary())
```

---

## 📋 রিগ্রেশন Output ব্যাখ্যা

| Element | কী বোঝায় |
|---------|-----------|
| Coefficient | X-এ ১ ইউনিট পরিবর্তনে Y-এ পরিবর্তন |
| p-value | Coefficient কি statistically significant? |
| R² | মডেল কত % ভ্যারিয়েশন ব্যাখ্যা করে |
| F-statistic | মডেল কি সামগ্রিকভাবে significant? |
| Residuals | Actual — Predicted |

---

## 🧪 অনুশীলনী
1. নিচের ডেটা দিয়ে Simple Linear Regression মডেল তৈরি করুন:
   - X (বাজার রিটার্ন): [1, 2, 3, 4, 5]
   - Y (স্টক রিটার্ন): [1.5, 3, 4.5, 6, 7.5]
2. β₀, β₁ এবং R² নির্ণয় করুন।
3. মডেল ব্যাখ্যা করুন: β₁ = 0.8, R² = 0.49 বলতে কী বোঝায়?
4. CAPM মডেল ব্যবহার করে β = 1.5, Rf = 3%, Rm = 10% হলে প্রত্যাশিত রিটার্ন কত?