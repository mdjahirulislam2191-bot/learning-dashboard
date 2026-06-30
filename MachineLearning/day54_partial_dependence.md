# Day 54: পার্শিয়াল ডিপেন্ডেন্স
## Partial Dependence Plots

### পার্শিয়াল ডিপেন্ডেন্স কি?
পার্শিয়াল ডিপেন্ডেন্স প্লট (PDP) একটি ফিচারের মান পরিবর্তন করলে মডেলের প্রেডিকশনের গড় পরিবর্তন দেখায়। এটি ফিচার এবং টার্গেটের মধ্যে সম্পর্ক ভিজুয়ালাইজ করে।

### ফাইন্যান্স অ্যাপ্লিকেশন
- **ক্রেডিট স্কোরিং**: ক্রেডিট স্কোর বনাম ডিফল্ট সম্ভাবনা
- **স্টক প্রেডিকশন**: ভলিউম বনাম প্রাইস ইমপ্যাক্ট
- **রিস্ক ম্যানেজমেন্ট**: কনসেন্ট্রেশন বনাম পোর্টফোলিও রিস্ক

### ফাইন্যান্স উদাহরণ: PDP অ্যানালাইসিস
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import partial_dependence, PartialDependenceDisplay
import warnings
warnings.filterwarnings('ignore')

# ফাইন্যান্স ডেটা
np.random.seed(42)
n = 2000

df = pd.DataFrame({
    'credit_score': np.random.randint(500, 850, n),
    'income': np.random.randn(n) * 30000 + 50000,
    'loan_amount': np.random.randn(n) * 20000 + 100000,
    'debt_ratio': np.random.rand(n) * 0.5,
    'employment_years': np.random.randint(0, 30, n),
    'age': np.random.randint(22, 70, n),
    'num_late_payments': np.random.poisson(1, n),
    'credit_lines': np.random.randint(1, 20, n)
})

# টার্গেট: লোন ডিফল্ট রিস্ক স্কোর
risk = (0.001 * (850 - df['credit_score']) + 
        0.3 * df['debt_ratio'] + 
        0.05 * df['num_late_payments'] + 
        0.1 * np.random.randn(n))
risk = np.clip(risk, 0, 1)

feature_cols = [c for c in df.columns]
X = df.values
X_train, X_test, y_train, y_test = train_test_split(X, risk, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(f"📊 Dataset: {df.shape}")
print(f"R² Score: {model.score(X_test, y_test):.4f}")
```

### 1. একক ফিচার PDP
```python
# ============================================
# সিঙ্গেল ফিচার পার্শিয়াল ডিপেন্ডেন্স
# ============================================
print("\n" + "=" * 60)
print("📈 SINGLE FEATURE PDP")
print("=" * 60)

# credit_score এর PDP
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

features_to_plot = ['credit_score', 'debt_ratio', 'num_late_payments', 'income']

for ax, feat in zip(axes.flat, features_to_plot):
    feat_idx = feature_cols.index(feat)
    
    PartialDependenceDisplay.from_estimator(
        model, X_test, feat_idx,
        feature_names=feature_cols,
        ax=ax,
        grid_resolution=50
    )
    ax.set_title(f'Partial Dependence: {feat}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2. দ্বি-ফিচার ইন্টারঅ্যাকশন PDP
```python
# ============================================
# টু-ওয়ে পার্শিয়াল ডিপেন্ডেন্স (ইন্টারঅ্যাকশন)
# ============================================
print("\n" + "=" * 60)
print("🔗 TWO-WAY INTERACTION PDP")
print("=" * 60)

# credit_score + debt_ratio ইন্টারঅ্যাকশন
fig, ax = plt.subplots(figsize=(10, 8))
PartialDependenceDisplay.from_estimator(
    model, X_test, 
    [(feature_cols.index('credit_score'), feature_cols.index('debt_ratio'))],
    feature_names=feature_cols,
    ax=ax,
    grid_resolution=30
)
ax.set_title('Partial Dependence: credit_score × debt_ratio')
plt.tight_layout()
plt.show()

print("📌 Interpretation:")
print("  - Heatmap shows joint effect of two features")
print("  - Bright = higher risk")
print("  - Dark = lower risk")
print("  - Non-parallel contours = interaction effect!")
```

### 3. আইস লাইন (ICE - Individual Conditional Expectation)
```python
# ============================================
# ICE প্লট (পার্শিয়াল ডিপেন্ডেন্সের ভ্যারিয়েন্ট)
# ============================================
print("\n" + "=" * 60)
print("📊 ICE (Individual Conditional Expectation) PLOTS")
print("=" * 60)

from sklearn.inspection import PartialDependenceDisplay

# ICE প্লট (প্রতি ডেটা পয়েন্টের জন্য)
fig, ax = plt.subplots(figsize=(12, 6))
PartialDependenceDisplay.from_estimator(
    model, X_test, 
    feature_cols.index('credit_score'),
    feature_names=feature_cols,
    kind='individual',  # ICE লাইন দেখায়
    ax=ax,
    grid_resolution=50,
    subsample=50  # ৫০টি র‍্যান্ডম স্যাম্পল
)
ax.set_title('ICE Plot: credit_score (50 Individual Lines)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("📌 ICE vs PDP:")
print("  - PDP: Average of all ICE lines")
print("  - ICE: Each individual line")
print("  - Heterogeneous ICE lines → possible interactions!")
```

### 4. PDP এবং ICE একত্রে
```python
# ============================================
# PDP + ICE কম্বিনেশন
# ============================================
print("\n" + "=" * 60)
print("📊 PDP + ICE COMBINATION PLOT")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

for ax, feat in zip(axes.flat, ['debt_ratio', 'num_late_payments', 'income', 'age']):
    feat_idx = feature_cols.index(feat)
    
    PartialDependenceDisplay.from_estimator(
        model, X_test, feat_idx,
        feature_names=feature_cols,
        kind='both',  # PDP + ICE
        ax=ax,
        grid_resolution=50,
        subsample=30
    )
    ax.set_title(f'PDP + ICE: {feat}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 5. মাল্টিপল ফিচার PDP বিশ্লেষণ
```python
# ============================================
# একাধিক ফিচারের PDP বিশ্লেষণ
# ============================================
print("\n" + "=" * 60)
print("🔍 MULTI-FEATURE PDP ANALYSIS")
print("=" * 60)

# একাধিক ফিচার একসাথে
fig, ax = plt.subplots(figsize=(12, 6))
PartialDependenceDisplay.from_estimator(
    model, X_test,
    [feature_cols.index(f) for f in ['credit_score', 'debt_ratio', 'num_late_payments']],
    feature_names=feature_cols,
    ax=ax,
    grid_resolution=50
)
ax.set_title('Multiple PDPs: credit_score, debt_ratio, late_payments')
plt.tight_layout()
plt.show()
```

### 6. PDP থেকে ইনসাইটস
```python
# ============================================
# PDP থেকে গুরুত্বপূর্ণ ইনসাইট
# ============================================
print("\n" + "=" * 60)
print("💡 PDP INSIGHTS")
print("=" * 60)

# PDP ডেটা এক্সট্র্যাক্ট
pdp_results = {}
for feat in feature_cols:
    feat_idx = feature_cols.index(feat)
    pdp = partial_dependence(model, X_test, features=[feat_idx], grid_resolution=50)
    pdp_results[feat] = {
        'values': pdp['values'][0],
        'average': pdp['average'][0]
    }

print("\n📊 Feature Impact Analysis:")
for feat in feature_cols:
    pdp_data = pdp_results[feat]
    vals = pdp_data['average']
    impact = vals.max() - vals.min()
    
    # Non-linearity check
    linear_reg = np.polyfit(pdp_data['values'], vals, 1)
    non_linearity = np.std(vals - np.polyval(linear_reg, pdp_data['values']))
    
    print(f"\n  {feat}:")
    print(f"    Impact range: {impact:.4f}")
    print(f"    Non-linearity: {non_linearity:.4f}")
    print(f"    Min effect at: {pdp_data['values'][vals.argmin()]:.2f}")
    print(f"    Max effect at: {pdp_data['values'][vals.argmax()]:.2f}")

# সারসংক্ষেপ
print("\n📌 Key Business Insights:")
print("  - credit_score: Higher score → lower risk (expected)")
print("  - debt_ratio: Higher ratio → higher risk (non-linear)")
print("  - num_late_payments: Each late payment increases risk")
print("  - Interaction: credit_score + debt_ratio interact!")
```

### PDP বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ PDP BEST PRACTICES")
print("=" * 60)

print("""
📋 PDP Analysis Framework:

1️⃣ Single PDP:
   ✅ Shows marginal effect of one feature
   ✅ Easy to interpret
   ❌ Hides individual variation (solution: ICE)

2️⃣ ICE Plots:
   ✅ Shows individual variation
   ✅ Detects heterogeneous effects
   ❌ Cluttered with many lines

3️⃣ 2-way PDP:
   ✅ Shows interaction effects
   ✅ Heatmap is intuitive
   ❌ Grid resolution matters

4️⃣ Centered PDP:
   ✅ Shows deviation from baseline
   ✅ Better for comparing features
   ❌ Less intuitive originally

📊 When to Use:
- Model debugging (does it make sense?)
- Feature importance validation
- Regulatory compliance (ECOA)
- Business stakeholder communication

⚠️ Limitations:
- Assumes feature independence
- Extrapolation beyond data range
- Computationally expensive for many features
- Does not show causality
""")
```

### সারসংক্ষেপ
আজ আমরা পার্শিয়াল ডিপেন্ডেন্স প্লট শিখলাম:
- **PDP**: গড় প্রভাব দেখায় (credit_score → risk)
- **ICE**: ব্যক্তিগত ভ্যারিয়েশন দেখায়
- **2-way PDP**: ফিচার ইন্টারঅ্যাকশন
- **PDP + ICE**: কম্বিনেশন ভিজুয়ালাইজেশন
- **ইনসাইট**: নন-লিনিয়ারিটি, ইমপ্যাক্ট রেঞ্জ

### অনুশীলনী
1. সেন্টার্ড PDP (deviation from baseline) ইমপ্লিমেন্ট করুন
2. মাল্টিপল মডেলের PDP তুলনা করুন
3. PDP-তে কনফিডেন্স ইন্টারভাল যোগ করুন (bootstrapping)
4. কাস্টম ক্যাটেগোরিক্যাল ফিচারের জন্য PDP তৈরি করুন