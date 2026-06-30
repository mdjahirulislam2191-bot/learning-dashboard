# দিন ১০: পোর্টফোলিও প্রজেক্ট — ফাইন্যান্সে পরিসংখ্যান (Portfolio Project: Stats for Finance)

## 📊 ডেটা Analyst / Finance-এ আবেদন

### সারসংক্ষেপ
এটি একটি সমন্বিত প্রজেক্ট যেখানে আমরা পূর্বের ৯ দিনের সব ধারণা একসাথে ব্যবহার করে একটি বাস্তব Finance ডেটা সেট বিশ্লেষণ করব। আমরা একটি মাল্টি-অ্যাসেট পোর্টফোলিও তৈরি করব, ঝুঁকি ও রিটার্ন বিশ্লেষণ করব, এবং ডেটা-চালিত সিদ্ধান্ত নেব।

---

## 📋 প্রজেক্ট ওভারভিউ

একটি বিনিয়োগ সংস্থা ৩টি সেক্টরে বিনিয়োগের সিদ্ধান্ত নিতে চায়:
1. **টেক সেক্টর** (High Growth, High Risk)
2. **ব্যাংক সেক্টর** (Stable, Moderate Risk)
3. **ইউটিলিটি সেক্টর** (Defensive, Low Risk)

**লক্ষ্য:** কোন পোর্টফোলিও সর্বোচ্চ রিস্ক-অ্যাডজাস্টেড রিটার্ন দেয়?

---

## 📊 ডেটাসেট

### ধাপ ১: ডেটা তৈরি

```python
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import ttest_ind, f_oneway
import matplotlib.pyplot as plt

# Simulated monthly returns (%) for 12 months
tech_returns = [5, -2, 8, -5, 12, 3, -3, 7, -1, 10, 4, -4]
bank_returns = [3, 1, 4, 0, 5, 2, 1, 3, 0, 4, 2, 1]
utility_returns = [1, 2, 1, 0.5, 2, 1.5, 1, 2, 0.5, 1, 1.5, 1]

df = pd.DataFrame({
    'Month': range(1, 13),
    'Tech': tech_returns,
    'Bank': bank_returns,
    'Utility': utility_returns
})
```

---

## 📈 অংশ ১: বর্ণনামূলক পরিসংখ্যান (Day 1)

```python
# Descriptive statistics
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    print(f"\n--- {sector} ---")
    print(f"Mean: {np.mean(data):.2f}%")
    print(f"Median: {np.median(data):.2f}%")
    print(f"Range: {np.max(data) - np.min(data):.2f}%")
```

**প্রত্যাশিত ফলাফল:**
| Sector | Mean | Median | Range |
|--------|------|--------|-------|
| Tech | 2.83% | 3.50% | 17.0% |
| Bank | 2.17% | 2.00% | 5.0% |
| Utility | 1.25% | 1.25% | 1.5% |

---

## 📈 অংশ ২: ঝুঁকি বিশ্লেষণ (Day 2)

```python
# Risk analysis
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    var = np.var(data, ddof=1)
    std = np.std(data, ddof=1)
    print(f"{sector}: Variance = {var:.2f}, Std Dev = {std:.2f}%")

# Sharpe Ratio (assuming Rf = 0.5%)
risk_free = 0.5
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    sharpe = (np.mean(data) - risk_free) / np.std(data, ddof=1)
    print(f"{sector} Sharpe: {sharpe:.3f}")
```

**প্রত্যাশিত ফলাফল:**
| Sector | Std Dev | Sharpe |
|--------|---------|--------|
| Tech | 5.76% | 0.404 |
| Bank | 1.59% | 1.047 |
| Utility | 0.52% | 1.442 |

> Utility-র Sharpe Ratio সবচেয়ে বেশি (সবচেয়ে ভালো রিস্ক-অ্যাডজাস্টেড রিটার্ন)

---

## 📈 অংশ ৩: সম্ভাবনা (Day 3)

```python
# Probability analysis
# What's the probability of negative return in each sector?
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    neg_prob = sum(1 for r in data if r < 0) / len(data)
    print(f"P({sector} negative): {neg_prob:.2%}")

# Probability of both Tech and Bank positive
tech_positive = [r > 0 for r in tech_returns]
bank_positive = [r > 0 for r in bank_returns]
both_positive = sum(1 for i in range(12) if tech_positive[i] and bank_positive[i]) / 12
print(f"P(Tech + Bank both positive): {both_positive:.2%}")
```

---

## 📈 অংশ ৪: Normal Distribution (Day 4)

```python
# Z-scores for the worst Tech return
worst_tech = min(tech_returns)
mean_tech = np.mean(tech_returns)
std_tech = np.std(tech_returns, ddof=1)
z_worst = (worst_tech - mean_tech) / std_tech
print(f"Worst Tech return: {worst_tech}%")
print(f"Z-score: {z_worst:.2f}")
print(f"Probability of worse: {stats.norm.cdf(z_worst):.4f}")

# Value at Risk (95%)
z_05 = stats.norm.ppf(0.05)
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    var_95 = np.mean(data) + z_05 * np.std(data, ddof=1)
    print(f"{sector} VaR(95%): {var_95:.2f}%")
```

---

## 📈 অংশ ৫: Confidence Intervals (Day 5)

```python
# 95% CI for each sector's mean return
for sector in ['Tech', 'Bank', 'Utility']:
    data = df[sector]
    n = len(data)
    se = np.std(data, ddof=1) / np.sqrt(n)
    ci = stats.t.interval(0.95, df=n-1, loc=np.mean(data), scale=se)
    print(f"{sector} 95% CI: [{ci[0]:.2f}%, {ci[1]:.2f}%]")
```

---

## 📈 অংশ ৬: Hypothesis Testing (Day 6)

```python
# Question: Is Tech return significantly different from Bank return?
t_stat, p_val = ttest_ind(tech_returns, bank_returns, equal_var=False)
print(f"Tech vs Bank: t = {t_stat:.3f}, p = {p_val:.4f}")

if p_val < 0.05:
    print("→ উল্লেখযোগ্য পার্থক্য আছে (Reject H₀)")
else:
    print("→ উল্লেখযোগ্য পার্থক্য নেই (Fail to reject H₀)")

# Question: Is Utility return significantly different from 1%?
t_stat, p_val = stats.ttest_1samp(utility_returns, 1.0)
print(f"Utility vs 1%: t = {t_stat:.3f}, p = {p_val:.4f}")
```

---

## 📈 অংশ ৭: Correlation (Day 7)

```python
# Correlation matrix
corr_matrix = df[['Tech', 'Bank', 'Utility']].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# Interpretation
# If Tech and Utility have low/negative correlation → diversification benefit
```

---

## 📈 অংশ ৮: Regression (Day 8)

```python
from sklearn.linear_model import LinearRegression

# Does Bank return predict Tech return?
X = df[['Bank']]  # Independent
y = df['Tech']    # Dependent

model = LinearRegression()
model.fit(X, y)
print(f"\nRegression: Tech = {model.intercept_:.2f} + {model.coef_[0]:.2f} × Bank")
print(f"R² = {model.score(X, y):.4f}")
```

---

## 📈 অংশ ৯: ANOVA (Day 9)

```python
# Are the sector mean returns significantly different?
f_stat, p_val = f_oneway(tech_returns, bank_returns, utility_returns)
print(f"\nANOVA: F = {f_stat:.3f}, p = {p_val:.4f}")

from statsmodels.stats.multicomp import pairwise_tukeyhsd
# Create long-form data for Tukey test
long_df = pd.DataFrame({
    'return': tech_returns + bank_returns + utility_returns,
    'sector': ['Tech']*12 + ['Bank']*12 + ['Utility']*12
})
tukey = pairwise_tukeyhsd(long_df['return'], long_df['sector'], alpha=0.05)
print(tukey)
```

---

## 🎯 সর্বোত্তম পোর্টফোলিও নির্ণয়

```python
# Portfolio optimization - equal weight
weights = np.array([1/3, 1/3, 1/3])
returns_portfolio = weights[0]*np.array(tech_returns) + \
                    weights[1]*np.array(bank_returns) + \
                    weights[2]*np.array(utility_returns)

port_mean = np.mean(returns_portfolio)
port_std = np.std(returns_portfolio, ddof=1)
port_sharpe = (port_mean - 0.5) / port_std

print(f"\n=== Equal-Weight Portfolio ===")
print(f"Portfolio Mean Return: {port_mean:.2f}%")
print(f"Portfolio Std Dev: {port_std:.2f}%")
print(f"Portfolio Sharpe: {port_sharpe:.3f}")

# Try different weights
for w1 in np.arange(0, 1.1, 0.2):
    for w2 in np.arange(0, 1.1 - w1, 0.2):
        w3 = 1 - w1 - w2
        w = np.array([w1, w2, w3])
        r = w[0]*np.array(tech_returns) + w[1]*np.array(bank_returns) + w[2]*np.array(utility_returns)
        s = (np.mean(r) - 0.5) / np.std(r, ddof=1)
        print(f"Tech:{w1:.0%} Bank:{w2:.0%} Utility:{w3:.0%} → Sharpe: {s:.3f}")
```

---

## 📋 চূড়ান্ত রিপোর্ট টেমপ্লেট

```
========================================
পোর্টফোলিও প্রজেক্ট — চূড়ান্ত রিপোর্ট
========================================

বর্ণনামূলক পরিসংখ্যান:
- Tech: Mean={}%, Median={}%, Range={}%
- Bank: Mean={}%, Median={}%, Range={}%
- Utility: Mean={}%, Median={}%, Range={}%

ঝুঁকি বিশ্লেষণ:
- সর্বনিম্ন SD: Utility ({:.2f}%) — সবচেয়ে নিরাপদ
- সর্বোচ্চ Sharpe: Utility ({:.3f}) — সেরা রিস্ক-অ্যাডজাস্টেড

হাইপোথিসিস টেস্টিং:
- Tech vs Bank: p={:.4f} — {} পার্থক্য
- ANOVA: F={:.3f}, p={:.4f}

কোরিলেশন:
- Tech-Bank: {:.2f}
- Tech-Utility: {:.2f}

প্রস্তাবিত পোর্টফোলিও:
- Tech: {:.0%}, Bank: {:.0%}, Utility: {:.0%}
- প্রত্যাশিত রিটার্ন: {:.2f}%
- SD: {:.2f}%
- Sharpe Ratio: {:.3f}

========================================
```

---

## ✅ সম্পূর্ণ প্রজেক্ট রান করা

```python
# Run everything in one script
if __name__ == "__main__":
    print("=== দশদিনের পরিসংখ্যান প্রজেক্ট ===")
    print("ফাইন্যান্সে পরিসংখ্যানের প্রয়োগ\n")
    
    # আপনার কোড এখানে রান করুন
```

---

## 🧪 অনুশীলনী
1. নিজের পছন্দমত ৪টি স্টক বেছে নিয়ে পোর্টফোলিও তৈরি করুন।
2. উপরের সবগুলো বিশ্লেষণ সেই পোর্টফোলিওতে প্রয়োগ করুন।
3. কোন ওয়েটিং সর্বোচ্চ Sharpe Ratio দেয় তা খুঁজুন।
4. একটি 2-পৃষ্ঠার রিপোর্ট তৈরি করুন (বাংলায়) যাতে আপনার ফলাফল এবং সুপারিশ থাকে।

---

## 🎉 অভিনন্দন! আপনি ১০ দিনের পরিসংখ্যান কোর্স সম্পন্ন করেছেন!

| দিন | বিষয় | শিখলেন |
|-----|-------|---------|
| ১ | Descriptive Stats | Mean, Median, Mode, Range |
| ২ | Variance & SD | ঝুঁকি পরিমাপ |
| ৩ | Probability | শর্তাধীন সম্ভাবনা, Bayes |
| ৪ | Normal Distribution | Z-scores, VaR |
| ৫ | Sampling & CI | CLT, Confidence Intervals |
| ৬ | Hypothesis Testing | t-tests, p-values |
| ৭ | Correlation | Diversification |
| ৮ | Regression | Beta, CAPM, Prediction |
| ৯ | ANOVA | Multiple group comparison |
| ১০ | Portfolio Project | Real-world application |