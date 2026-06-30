# দিন ৯: ANOVA — মৌলিক ধারণা (ANOVA Basics)

## 📊 ডেটা Analyst / Finance-এ আবেদন

### সারসংক্ষেপ
ANOVA (Analysis of Variance) দুইয়ের বেশি গ্রুপের গড় তুলনা করতে ব্যবহৃত হয়। t-টেস্ট যেখানে দুই গ্রুপের জন্য, ANOVA তিন বা ততোধিক গ্রুপের জন্য।

---

## ১. ANOVA কী এবং কেন দরকার?

**সমস্যা:** তিনটি মিউচুয়াল ফান্ডের গড় রিটার্ন কি আলাদা?

**ভুল পদ্ধতি:** তিনটি পৃথক t-টেস্ট করা (A-B, A-C, B-C) — এতে Type I Error বেড়ে যায়।

**ANOVA সমাধান:** একসাথে সব গ্রুপের গড় তুলনা করে, সামগ্রিকভাবে পার্থক্য আছে কিনা পরীক্ষা করে।

### Null এবং Alternative Hypothesis:
```
H₀: μ₁ = μ₂ = μ₃ = … = μk
H₁: অন্তত একটি গ্রুপের গড় অন্যদের থেকে আলাদা
```

---

## ২. ANOVA-র মূল ধারণা

ANOVA মোট ভ্যারিয়েশনকে দুই ভাগে ভাগ করে:

**১. Between-group Variation (SSB):** গ্রুপগুলোর মধ্যে পার্থক্য
**২. Within-group Variation (SSW):** গ্রুপের ভিতরের পার্থক্য

### F-statistic:
```
F = MSB / MSW
```
যেখানে,
- MSB = Mean Square Between = SSB / (k-1)
- MSW = Mean Square Within = SSW / (n-k)
- k = গ্রুপ সংখ্যা
- n = মোট নমুনা সংখ্যা

### F-মান ব্যাখ্যা:
| F-মান | অর্থ |
|-------|------|
| F ≈ 1 | গ্রুপগুলোর মধ্যে উল্লেখযোগ্য পার্থক্য নেই |
| F >> 1 | গ্রুপগুলোর মধ্যে উল্লেখযোগ্য পার্থক্য আছে |
| F < 1 | গ্রুপের ভিতরের ভ্যারিয়েশন বেশি |

---

## ৩. One-Way ANOVA

**কখন ব্যবহার করবেন:** একটি ফ্যাক্টর (ক্যাটেগরিক্যাল) অনুযায়ী তিন বা ততোধিক গ্রুপের গড় তুলনা।

### Finance উদাহরণ:
তিনটি ভিন্ন সেক্টরের স্টকের গড় রিটার্ন তুলনা:

| টেক (Tech) | ব্যাংক (Bank) | স্বাস্থ্য (Health) |
|------------|---------------|-------------------|
| 12% | 8% | 10% |
| 15% | 9% | 11% |
| 10% | 7% | 9% |
| 14% | 10% | 12% |
| 13% | 6% | 8% |

### ANOVA টেবিল:

| Source | SS | df | MS | F | p-value |
|--------|----|----|----|---|---------|
| Between | 60.0 | 2 | 30.0 | 7.5 | 0.008 |
| Within | 48.0 | 12 | 4.0 | | |
| Total | 108.0 | 14 | | | |

**সিদ্ধান্ত:** p = 0.008 < 0.05 → অন্তত একটি সেক্টরের গড় রিটার্ন অন্যদের থেকে আলাদা।

---

## ৪. Two-Way ANOVA

**কখন ব্যবহার করবেন:** দুইটি ফ্যাক্টর একসাথে পরীক্ষা করতে।

**Finance উদাহরণ:** সেক্টর × অর্থনৈতিক অবস্থা (Bull/Bear Market)

| Source | ব্যাখ্যা |
|--------|---------|
| Sector | সেক্টরের মূল প্রভাব |
| Market Condition | বাজার অবস্থার প্রভাব |
| Interaction | সেক্টর × অবস্থার মিথষ্ক্রিয়া |

**Interaction উদাহরণ:** টেক স্টক Bull market-এ ভালো করে কিন্তু Bear-এ খারাপ করে, অন্যদিকে Defensive স্টক উল্টো আচরণ করে।

---

## ৫. Post-Hoc টেস্ট (ANOVA-র পরে)

ANOVA বলে যে "কমপক্ষে এক গ্রুপ আলাদা" কিন্তু **কোন গ্রুপ(গুলি)** তা বলে না।

**জনপ্রিয় Post-Hoc টেস্ট:**

| টেস্ট | ব্যবহার |
|-------|---------|
| Tukey's HSD | সব গ্রুপের pairwise তুলনা |
| Bonferroni | ছোট সংখ্যক তুলনা |
| Scheffe | জটিল তুলনা |

**Python উদাহরণ:** Tukey's HSD ব্যবহার করে কোন সেক্টর আলাদা তা নির্ণয়।

---

## ৬. ANOVA Assumptions

| Assumption | পরীক্ষা | লঙ্ঘিত হলে |
|-----------|---------|------------|
| Normality | Shapiro-Wilk / Q-Q plot | Kruskal-Wallis |
| Homogeneity of Variance | Levene's test | Welch's ANOVA |
| Independence | Study design | Mixed-effects model |

---

## ✅ Python উদাহরণ

```python
import scipy.stats as stats
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Three sectors returns
tech = [12, 15, 10, 14, 13]
bank = [8, 9, 7, 10, 6]
health = [10, 11, 9, 12, 8]

# One-way ANOVA
f_stat, p_value = stats.f_oneway(tech, bank, health)
print(f"ANOVA: F = {f_stat:.3f}, p = {p_value:.4f}")

# Tukey's HSD post-hoc test
df = pd.DataFrame({
    'returns': tech + bank + health,
    'sector': ['Tech']*5 + ['Bank']*5 + ['Health']*5
})

tukey = pairwise_tukeyhsd(df['returns'], df['sector'], alpha=0.05)
print(tukey)

# Two-way ANOVA example
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Simulate two-factor data
df_twoway = pd.DataFrame({
    'return': [12, 15, 10, 8, 9, 7, 10, 11, 9],
    'sector': ['Tech', 'Tech', 'Tech', 'Bank', 'Bank', 'Bank', 'Health', 'Health', 'Health'],
    'market': ['Bull', 'Bear', 'Neutral'] * 3
})

model = ols('return ~ C(sector) + C(market) + C(sector):C(market)', data=df_twoway).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

---

## 📋 ANOVA vs t-Test

| বৈশিষ্ট্য | t-Test | ANOVA |
|-----------|--------|-------|
| গ্রুপ সংখ্যা | ২ | ৩+ |
| Hypothesis | μ₁ = μ₂ | μ₁ = μ₂ = … = μk |
| Test Statistic | t | F |
| Post-hoc প্রয়োজন? | না (সরাসরি) | হ্যাঁ |
| Type I Error | নিয়ন্ত্রিত | Bonferroni correction |

---

## 📋 ANOVA Decision Tree

| পরিস্থিতি | কোন টেস্ট |
|-----------|----------|
| ২ গ্রুপ তুলনা | t-Test |
| ৩+ গ্রুপ, ১ ফ্যাক্টর | One-Way ANOVA |
| ৩+ গ্রুপ, ২ ফ্যাক্টর | Two-Way ANOVA |
| ANOVA significant → কোন গ্রুপ আলাদা? | Post-hoc (Tukey) |
| Assumption লঙ্ঘিত | Kruskal-Wallis (Non-parametric) |

---

## 🧪 অনুশীলনী
1. চারটি ভিন্ন ট্রেডিং স্ট্র্যাটেজির রিটার্ন: [5,7,6], [8,9,10], [3,4,5], [12,11,13] — ANOVA চালান।
2. ANOVA-র F-statistic বলতে কী বোঝায়?
3. Post-hoc টেস্ট কেন প্রয়োজন?
4. একটি বিনিয়োগ সংস্থা তিনটি ভিন্ন অ্যাসেট ক্লাসের (Stock, Bond, Commodity) রিটার্ন তুলনা করতে চায় — কোন পরিসংখ্যানিক টেস্ট ব্যবহার করবেন?