# Day 52: ফিচার ইম্পরটেন্স
## Feature Importance

### ফিচার ইম্পরটেন্স কি?
ফিচার ইম্পরটেন্স নির্ধারণ করে প্রতিটি ফিচার মডেলের প্রেডিকশনে কতটা অবদান রাখে। এটি মডেল ইন্টারপ্রিটেবিলিটি, ফিচার সিলেকশন এবং ডোমেইন ইনসাইটের জন্য গুরুত্বপূর্ণ।

### ফাইন্যান্সে ফিচার ইম্পরটেন্সের ব্যবহার
- **ক্রেডিট রিস্ক**: কোন ফ্যাক্টর ডিফল্ট নির্ধারণ করে?
- **স্টক প্রেডিকশন**: কোন ইন্ডিকেটর সবচেয়ে গুরুত্বপূর্ণ?
- **কাস্টমার সেগমেন্টেশন**: কোন অ্যাট্রিবিউট গ্রাহক গ্রুপ আলাদা করে?
- **ফ্রড ডিটেকশন**: ফ্রডের সবচেয়ে শক্তিশালী সিগন্যাল কি?

### ফাইন্যান্স উদাহরণ: ফিচার ইম্পরটেন্স অ্যানালাইসিস
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
import seaborn as sns
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
    'num_credit_lines': np.random.randint(1, 15, n),
    'late_payments': np.random.poisson(1, n),
    'utilization_rate': np.random.rand(n) * 0.8,
    'income_stability': np.random.rand(n)
})

# টার্গেট
y = (df['credit_score'] * 0.001 + 
     df['income'] * 0.00001 - 
     df['debt_ratio'] * 5 - 
     df['late_payments'] * 2 + 
     df['utilization_rate'] * (-3) + 
     np.random.randn(n) * 0.5)

feature_cols = list(df.columns)
X = df.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("📊 Financial Feature Importance Dataset")
print(f"  Features: {len(feature_cols)}")
print(f"  Samples: {n}")
```

### 1. ট্রি-বেসড ইম্পরটেন্স
```python
# ============================================
# Tree-based Feature Importance
# ============================================
print("\n" + "=" * 60)
print("🌲 TREE-BASED IMPORTANCE")
print("=" * 60)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 1. Gini Importance (built-in)
gini_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\n📊 Gini Importance (Built-in):")
print(gini_importance.to_string(index=False))

# 2. Permutation Importance
perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
perm_df = pd.DataFrame({
    'feature': feature_cols,
    'importance_mean': perm_importance.importances_mean,
    'importance_std': perm_importance.importances_std
}).sort_values('importance_mean', ascending=False)

print("\n📊 Permutation Importance (More Robust):")
print(perm_df.to_string(index=False))
```

### 2. লিনিয়ার মডেল ইম্পরটেন্স (Coefficients)
```python
# ============================================
# Linear Model Coefficients
# ============================================
print("\n" + "=" * 60)
print("📏 LINEAR MODEL COEFFICIENTS")
print("=" * 60)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_s, y_train)

coef_df = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': ridge.coef_,
    'abs_coef': np.abs(ridge.coef_)
}).sort_values('abs_coef', ascending=False)

print("\n📊 Ridge Coefficients:")
print(coef_df[['feature', 'coefficient']].to_string(index=False))

# Lasso (ফিচার সিলেকশন করে)
lasso = Lasso(alpha=0.01)
lasso.fit(X_train_s, y_train)

lasso_df = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': lasso.coef_
}).sort_values('coefficient', key=abs, ascending=False)

print("\n📊 Lasso Coefficients (with feature selection):")
print(lasso_df[lasso_df['coefficient'] != 0].to_string(index=False))
```

### 3. পারমুটেশন ইম্পরটেন্স (মডেল-অ্যাগনস্টিক)
```python
# ============================================
# মডেল-অ্যাগনস্টিক পারমুটেশন ইম্পরটেন্স
# ============================================
print("\n" + "=" * 60)
print("🔄 PERMUTATION IMPORTANCE (Model-Agnostic)")
print("=" * 60)

def permutation_importance_score(model, X, y, feature_names, n_repeats=10):
    """কাস্টম পারমুটেশন ইম্পরটেন্স ইমপ্লিমেন্টেশন"""
    baseline_score = model.score(X, y)
    results = {}
    
    for i, name in enumerate(feature_names):
        scores = []
        for _ in range(n_repeats):
            X_permuted = X.copy()
            X_permuted[:, i] = np.random.permutation(X_permuted[:, i])
            permuted_score = model.score(X_permuted, y)
            scores.append(baseline_score - permuted_score)
        
        results[name] = {
            'importance_mean': np.mean(scores),
            'importance_std': np.std(scores)
        }
    
    return results

# Gradient Boosting এর জন্য পারমুটেশন
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)

gb_perm = permutation_importance_score(gb, X_test, y_test, feature_cols)
gb_perm_df = pd.DataFrame(gb_perm).T.sort_values('importance_mean', ascending=False)

print("\n📊 Gradient Boosting - Permutation Importance:")
print(gb_perm_df.round(6).to_string())
```

### 4. পারমুটেশন ভিজুয়ালাইজেশন
```python
# ============================================
# ইম্পরটেন্স ভিজুয়ালাইজেশন
# ============================================
print("\n" + "=" * 60)
print("📊 IMPORTANCE VISUALIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Gini Importance
axes[0, 0].barh(gini_importance['feature'], gini_importance['importance'], color='steelblue')
axes[0, 0].set_xlabel('Importance')
axes[0, 0].set_title('Random Forest - Gini Importance')
axes[0, 0].invert_yaxis()
axes[0, 0].grid(True, alpha=0.3)

# Permutation Importance
perm_sorted = perm_df.sort_values('importance_mean', ascending=True)
axes[0, 1].barh(perm_sorted['feature'], perm_sorted['importance_mean'], 
                xerr=perm_sorted['importance_std'], color='coral')
axes[0, 1].set_xlabel('Importance (Mean ± Std)')
axes[0, 1].set_title('Random Forest - Permutation Importance')
axes[0, 1].invert_yaxis()
axes[0, 1].grid(True, alpha=0.3)

# Ridge Coefficients
coef_sorted = coef_df.sort_values('abs_coef', ascending=True)
colors = ['green' if c > 0 else 'red' for c in coef_sorted['coefficient']]
axes[1, 0].barh(coef_sorted['feature'], coef_sorted['coefficient'], color=colors)
axes[1, 0].axvline(x=0, color='black', linewidth=0.5)
axes[1, 0].set_xlabel('Coefficient')
axes[1, 0].set_title('Ridge - Coefficients')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(True, alpha=0.3)

# GB Permutation
gb_perm_sorted = gb_perm_df.sort_values('importance_mean', ascending=True)
axes[1, 1].barh(gb_perm_sorted.index, gb_perm_sorted['importance_mean'], 
                xerr=gb_perm_sorted['importance_std'], color='purple')
axes[1, 1].set_xlabel('Importance')
axes[1, 1].set_title('Gradient Boosting - Permutation Importance')
axes[1, 1].invert_yaxis()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 5. ইম্পরটেন্স এবং কোরিলেশন
```python
# ============================================
# ইম্পরটেন্স এবং কোরিলেশন তুলনা
# ============================================
print("\n" + "=" * 60)
print("🔗 IMPORTANCE vs CORRELATION")
print("=" * 60)

# কোরিলেশন
correlations = df.corrwith(pd.Series(y)).abs().sort_values(ascending=False)

importance_comparison = pd.DataFrame({
    'feature': gini_importance['feature'],
    'importance_rf': gini_importance['importance'],
    'correlation': [correlations[f] for f in gini_importance['feature']]
}).round(4)

print("\n📊 Feature Importance vs Correlation:")
print(importance_comparison.to_string(index=False))

print("\n📌 Key Insight:")
print("  - Importance ≠ Correlation")
print("  - Tree models capture non-linear interactions")
print("  - Permutation importance shows marginal effect")
print("  - Coefficients show linear impact (+/- direction)")
```

### ফিচার ইম্পরটেন্স বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ FEATURE IMPORTANCE BEST PRACTICES")
print("=" * 60)

print("""
📋 Importance Methods Comparison:

1️⃣ Tree-based (Gini/Entropy)
   ✅ Fast, built-in
   ❌ Biased towards high-cardinality features
   ❌ Only available for tree models

2️⃣ Coefficients (Linear Models)
   ✅ Interpretable (+/- direction)
   ❌ Only linear relationships
   ❌ Scale-dependent

3️⃣ Permutation Importance
   ✅ Model-agnostic
   ✅ More robust
   ❌ Computationally expensive
   ❌ Correlated features can reduce importance

4️⃣ SHAP Values (Day 53)
   ✅ Theoretical foundation (game theory)
   ✅ Consistent and accurate
   ✅ Local + global explanations
   - Covered in detail tomorrow!

📋 Recommendations:
- Always use multiple importance methods
- Check for correlated features
- Validate with domain knowledge
- Use permutation or SHAP for production
""")
```

### সারসংক্ষেপ
আজ আমরা ফিচার ইম্পরটেন্স শিখলাম:
- **Gini Importance**: ট্রি-বেসড মডেলের বিল্ট-ইন
- **Permutation Importance**: মডেল-অ্যাগনস্টিক, আরো রোবাস্ট
- **Coefficients**: লিনিয়ার মডেল (+/- ডিরেকশন)
- **কোরিলেশন vs ইম্পরটেন্স**: পার্থক্য বোঝা
- **ভিজুয়ালাইজেশন**: মাল্টিপল মেথডের তুলনা

### অনুশীলনী
1. পারমুটেশন ইম্পরটেন্স মাল্টিপল মডেলে প্রয়োগ করুন
2. কোরিলেটেড ফিচার রিমুভ করে ইম্পরটেন্স রি-ক্যালকুলেট করুন
3. স্কেল-ইন্ডিপেন্ডেন্ট ইম্পরটেন্স মেট্রিক তৈরি করুন
4. এলিমিনেশন বাই এলিমিনেশন (EBD) টেকনিক ইমপ্লিমেন্ট করুন