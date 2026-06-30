# Day 53: SHAP ভ্যালু
## SHAP (SHapley Additive exPlanations)

### SHAP কি?
SHAP হল গেম থিওরি-ভিত্তিক একটি ব্যাখ্যা পদ্ধতি যা প্রতিটি ফিচারের প্রেডিকশনে কতটুকু অবদান আছে তা গণনা করে। এটি শ্যাপলি ভ্যালুর উপর ভিত্তি করে তৈরি।

### কেন SHAP গুরুত্বপূর্ণ?
- **কনসিস্টেন্ট**: ফিচার ইম্পরটেন্স কনসিস্টেন্ট
- **ইন্টারপ্রেটেবল**: প্রতিটি প্রেডিকশনের জন্য ব্যাখ্যা
- **মডেল-অ্যাগনস্টিক**: যেকোনো মডেলের সাথে কাজ করে
- **থিওরিটিক্যাল ফাউন্ডেশন**: শ্যাপলি ভ্যালু (নোবেল পুরস্কার বিজয়ী তত্ত্ব)

### ফাইন্যান্স উদাহরণ: লোন অ্যাপ্রুভাল SHAP
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# SHAP ইনস্টল/ইম্পোর্ট
try:
    import shap
    print("✅ SHAP imported successfully")
except ImportError:
    import subprocess
    subprocess.run(['pip', 'install', 'shap'], capture_output=True)
    import shap
    print("✅ SHAP installed and imported")

# লোন ডেটা
np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'credit_score': np.random.randint(500, 850, n),
    'income': np.random.randn(n) * 30000 + 50000,
    'loan_amount': np.random.randn(n) * 20000 + 100000,
    'debt_ratio': np.random.rand(n) * 0.5,
    'employment_years': np.random.randint(0, 30, n),
    'age': np.random.randint(22, 70, n),
    'num_late_payments': np.random.poisson(2, n),
    'credit_lines': np.random.randint(1, 20, n)
})

# টার্গেট
risk_score = (data['credit_score'] * 0.003 + 
              data['income'] * 1e-5 - 
              data['debt_ratio'] * 5 - 
              data['num_late_payments'] * 2 +
              np.random.randn(n) * 0.3)
data['approved'] = (risk_score > np.median(risk_score)).astype(int)

print(f"📊 Loan Dataset: {data.shape}")
print(f"Approval rate: {data['approved'].mean():.2%}")

feature_cols = [c for c in data.columns if c != 'approved']
X = data[feature_cols]
y = data['approved']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f"Model accuracy: {model.score(X_test, y_test):.4f}")
```

### 1. SHAP ব্যাখ্যাকারী তৈরি
```python
# ============================================
# SHAP Explainer তৈরি
# ============================================
print("\n" + "=" * 60)
print("🔧 SHAP EXPLAINER")
print("=" * 60)

# Tree Explainer (ট্রি মডেলের জন্য দ্রুত)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# শুধুমাত্র ক্লাস 1 (approved) এর জন্য
shap_values_class1 = shap_values[1] if isinstance(shap_values, list) else shap_values

print(f"✅ SHAP Explainer created")
print(f"  SHAP values shape: {shap_values_class1.shape}")
print(f"  Expected value: {explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value:.4f}")
```

### 2. SHAP সামারি প্লট (গ্লোবাল ইম্পরটেন্স)
```python
# ============================================
# SHAP সামারি প্লট
# ============================================
print("\n" + "=" * 60)
print("📊 SHAP SUMMARY PLOT")
print("=" * 60)

# সামারি প্লট
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values_class1, X_test, feature_names=feature_cols, show=False)
plt.title('SHAP Feature Importance (Loan Approval)', fontsize=14)
plt.tight_layout()
plt.show()

print("\n📊 SHAP Feature Importance (Mean Absolute SHAP):")
mean_shap = np.abs(shap_values_class1).mean(axis=0)
shap_importance = pd.DataFrame({
    'feature': feature_cols,
    'mean_shap': mean_shap
}).sort_values('mean_shap', ascending=False)
print(shap_importance.to_string(index=False))
```

### 3. SHAP ওয়াটারফল প্লট (লোকাল ব্যাখ্যা)
```python
# ============================================
# SHAP ওয়াটারফল প্লট (একক প্রেডিকশন ব্যাখ্যা)
# ============================================
print("\n" + "=" * 60)
print("💧 SHAP WATERFALL PLOT (Local Explanation)")
print("=" * 60)

# একটি সুনির্দিষ্ট উদাহরণ
sample_idx = 5
sample = X_test.iloc[sample_idx:sample_idx+1]

print(f"📌 Sample {sample_idx} Explanation:")
print(f"  Predicted: {'Approved' if model.predict(sample)[0] == 1 else 'Denied'}")
print(f"  Probability: {model.predict_proba(sample)[0][1]:.4f}")
print(f"  Actual: {'Approved' if y_test.iloc[sample_idx] == 1 else 'Denied'}")

plt.figure(figsize=(12, 6))
shap.waterfall_plot(
    shap.Explanation(
        values=shap_values_class1[sample_idx], 
        base_values=explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
        data=X_test.iloc[sample_idx].values,
        feature_names=feature_cols
    ),
    show=False
)
plt.title(f'SHAP Waterfall Plot - Sample {sample_idx}', fontsize=14)
plt.tight_layout()
plt.show()
```

### 4. SHAP ফোর্স প্লট
```python
# ============================================
# SHAP ফোর্স প্লট
# ============================================
print("\n" + "=" * 60)
print("🏋️ SHAP FORCE PLOT")
print("=" * 60)

# ফোর্স প্লট (একক)
plt.figure(figsize=(20, 4))
shap.force_plot(
    explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
    shap_values_class1[sample_idx],
    X_test.iloc[sample_idx],
    feature_names=feature_cols,
    matplotlib=True,
    show=False
)
plt.title(f'SHAP Force Plot - Sample {sample_idx}', fontsize=14)
plt.tight_layout()
plt.show()
```

### 5. SHAP নির্ভরতা প্লট
```python
# ============================================
# SHAP নির্ভরতা প্লট (ফিচার ইন্টারঅ্যাকশন)
# ============================================
print("\n" + "=" * 60)
print("📈 SHAP DEPENDENCE PLOTS")
print("=" * 60)

# credit_score এর জন্য নির্ভরতা প্লট
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
shap.dependence_plot('credit_score', shap_values_class1, X_test, 
                     feature_names=feature_cols, show=False)
plt.title('SHAP Dependence: credit_score')

plt.subplot(1, 2, 2)
shap.dependence_plot('income', shap_values_class1, X_test,
                     feature_names=feature_cols, show=False)
plt.title('SHAP Dependence: income')

plt.tight_layout()
plt.show()

# ফিচার ইন্টারঅ্যাকশন
print("\n📊 Feature Interaction (credit_score + debt_ratio):")
plt.figure(figsize=(10, 6))
shap.dependence_plot('debt_ratio', shap_values_class1, X_test,
                     interaction_index='credit_score',
                     feature_names=feature_cols, show=False)
plt.title('debt_ratio SHAP (colored by credit_score)')
plt.tight_layout()
plt.show()
```

### 6. SHAP বৈশ্বিক ইম্পরটেন্স বিশ্লেষণ
```python
# ============================================
# SHAP বৈশ্বিক ইম্পরটেন্স
# ============================================
print("\n" + "=" * 60)
print("🌍 SHAP GLOBAL IMPORTANCE ANALYSIS")
print("=" * 60)

# SHAP বার প্লট
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values_class1, X_test, feature_names=feature_cols, 
                  plot_type="bar", show=False)
plt.title('Mean |SHAP| Feature Importance')
plt.tight_layout()
plt.show()

# টপ ফিচারের SHAP বিস্তারিত
top_features = shap_importance.head(3)['feature'].tolist()
print(f"\n📊 Top 3 Features Detailed Analysis:")
for feat in top_features:
    idx = feature_cols.index(feat)
    shap_vals = shap_values_class1[:, idx]
    
    print(f"\n  {feat}:")
    print(f"    Mean |SHAP|: {np.abs(shap_vals).mean():.4f}")
    print(f"    Mean SHAP: {shap_vals.mean():.4f}")
    print(f"    Std SHAP: {shap_vals.std():.4f}")
    print(f"    Max SHAP: {shap_vals.max():.4f}")
    print(f"    Min SHAP: {shap_vals.min():.4f}")
```

### 7. SHAP vs ফিচার ইম্পরটেন্স তুলনা
```python
# ============================================
# SHAP vs Gini Importance
# ============================================
print("\n" + "=" * 60)
print("⚖️ SHAP vs GINI IMPORTANCE")
 print("=" * 60)

gini_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance_gini': model.feature_importances_
})

comparison = shap_importance.merge(gini_importance, on='feature')

# র‍্যাঙ্কিং তুলনা
comparison['rank_shap'] = comparison['mean_shap'].rank(ascending=False)
comparison['rank_gini'] = comparison['importance_gini'].rank(ascending=False)
comparison['rank_diff'] = abs(comparison['rank_shap'] - comparison['rank_gini'])

print("\n📊 SHAP vs Gini Importance Comparison:")
print(comparison.round(4).to_string(index=False))

print("\n📌 Key Differences:")
print("  - Gini: Biased towards high-cardinality features")
print("  - SHAP: Theoretically sound, consistent")
print("  - SHAP: Shows direction (+/-) of impact")
print("  - SHAP: Can show feature interactions")
```

### SHAP বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ SHAP BEST PRACTICES")
print("=" * 60)

print("""
📋 SHAP Explained:

🎲 The Math:
SHAP values are based on Shapley values (game theory).
Each feature's contribution is calculated as:
  φi = Σ [|S|!(M-|S|-1)! / M!] × [fx(S ∪ {i}) - fx(S)]
  Where: S = subset of features, M = total features

📊 Visualization Types:
1️⃣ Summary Plot: Global importance + feature effects
2️⃣ Waterfall Plot: Single prediction breakdown
3️⃣ Force Plot: Local explanation (interactive)
4️⃣ Dependence Plot: Feature effect + interactions
5️⃣ Bar Plot: Mean absolute SHAP

⚡ Speed Comparison:
- TreeExplainer: Very fast (O(TLD²))
- KernelExplainer: Slow (model-agnostic)
- LinearExplainer: Fast (linear models)
- DeepExplainer: Moderate (deep learning)

💡 Tips:
- Use TreeExplainer for random forest/XGBoost
- Use 50-100 background samples for speed
- SHAP works for both classification and regression
- Higher SHAP ≠ causal effect!
""")
```

### সারসংক্ষেপ
আজ আমরা SHAP ভ্যালু শিখলাম:
- **SHAP Explainer**: TreeExplainer, KernelExplainer
- **সামারি প্লট**: গ্লোবাল ফিচার ইম্পরটেন্স
- **ওয়াটারফল প্লট**: একক প্রেডিকশনের ব্যাখ্যা
- **ফোর্স প্লট**: ভিজুয়াল লোকাল ব্যাখ্যা
- **নির্ভরতা প্লট**: ফিচার ইন্টারঅ্যাকশন
- **SHAP vs Gini**: ফিচার ইম্পরটেন্স তুলনা

### অনুশীলনী
1. SHAP KernelExplainer ব্যবহার করে (নন-ট্রি) মডেল ব্যাখ্যা করুন
2. একাধিক প্রেডিকশনের SHAP ওয়াটারফল প্লট একসাথে দেখান
3. SHAP ইন্টারঅ্যাকশন ভ্যালু (shap_interaction_values) এক্সপ্লোর করুন
4. ক্লাসিফিকেশন এবং রিগ্রেশন উভয় টাস্কে SHAP প্রয়োগ করুন