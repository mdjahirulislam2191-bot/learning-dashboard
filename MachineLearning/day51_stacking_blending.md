# Day 51: স্ট্যাকিং এবং ব্লেন্ডিং
## Stacking & Blending

### স্ট্যাকিং এবং ব্লেন্ডিং কি?
স্ট্যাকিং এবং ব্লেন্ডিং হল এনসেম্বল মেথড যা একাধিক মডেলের প্রেডিকশন একত্রিত করে একটি মেটা-মডেল তৈরি করে। এগুলি সাধারণ ভোটিং/এভারেজিং থেকে বেশি শক্তিশালী।

### ফাইন্যান্স অ্যাপ্লিকেশন
- **স্টক প্রাইস প্রেডিকশন**: একাধিক মডেলের শক্তির সংমিশ্রণ
- **ক্রেডিট স্কোরিং**: বিভিন্ন মডেলের দুর্বলতা কভার
- **ফ্রড ডিটেকশন**: উচ্চতর ডিটেকশন রেট
- **পোর্টফোলিও রিস্ক মডেলিং**: রোবাস্ট প্রেডিকশন

### ফাইন্যান্স উদাহরণ: স্টক রিটার্ন এনসেম্বল
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ফাইন্যান্স ডেটা
np.random.seed(42)
n = 2000
X = np.random.randn(n, 20)
y = X @ np.random.randn(20) * 2 + np.random.randn(n) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("📊 Financial Dataset")
print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
print(f"  Features: {X_train.shape[1]}")
```

### 1. বেস মডেল তৈরি
```python
# ============================================
# বেস মডেল ট্রেইনিং
# ============================================
print("\n" + "=" * 60)
print("📊 BASE MODELS")
print("=" * 60)

base_models = {
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.1),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'SVR': SVR(kernel='rbf', C=1.0)
}

base_predictions = {}
base_scores = {}

for name, model in base_models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    base_predictions[name] = y_pred
    base_scores[name] = r2
    print(f"  {name:<20}: R² = {r2:.4f}")
```

### 2. স্ট্যাকিং ইমপ্লিমেন্টেশন
```python
# ============================================
# স্ট্যাকিং (মেটা-মডেল)
# ============================================
print("\n" + "=" * 60)
print("🏗️ STACKING IMPLEMENTATION")
print("=" * 60)

def stacking_ensemble(base_models_dict, X_train, y_train, X_test, meta_model):
    """স্ট্যাকিং এনসেম্বল ইমপ্লিমেন্টেশন"""
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    n_train = X_train.shape[0]
    meta_features_train = np.zeros((n_train, len(base_models_dict)))
    meta_features_test = np.zeros((X_test.shape[0], len(base_models_dict)))
    
    for i, (name, model) in enumerate(base_models_dict.items()):
        print(f"  Processing {name}...")
        oof_pred = np.zeros(n_train)
        test_pred = np.zeros(X_test.shape[0])
        
        for train_idx, val_idx in kf.split(X_train):
            X_tr, X_val = X_train[train_idx], X_train[val_idx]
            y_tr, y_val = y_train[train_idx], y_train[val_idx]
            
            model_clone = model.__class__(**model.get_params())
            model_clone.fit(X_tr, y_tr)
            
            oof_pred[val_idx] = model_clone.predict(X_val)
            test_pred += model_clone.predict(X_test) / kf.n_splits
        
        meta_features_train[:, i] = oof_pred
        meta_features_test[:, i] = test_pred
    
    # মেটা-মডেল ট্রেইন
    print(f"\n  Training meta-model: {meta_model.__class__.__name__}")
    meta_model.fit(meta_features_train, y_train)
    
    # ফাইনাল প্রেডিকশন
    final_pred = meta_model.predict(meta_features_test)
    
    return {
        'meta_features_train': meta_features_train,
        'meta_features_test': meta_features_test,
        'meta_model': meta_model,
        'final_prediction': final_pred
    }

# স্ট্যাকিং এক্সিকিউট
meta_model = Ridge(alpha=0.5)
stacking_result = stacking_ensemble(base_models, X_train, y_train, X_test, meta_model)

stacking_r2 = r2_score(y_test, stacking_result['final_prediction'])
print(f"\n✅ Stacking Ensemble R²: {stacking_r2:.4f}")
```

### 3. ব্লেন্ডিং ইমপ্লিমেন্টেশন
```python
# ============================================
# ব্লেন্ডিং (ওয়েটেড এভারেজ)
# ============================================
print("\n" + "=" * 60)
print("🎯 BLENDING IMPLEMENTATION")
print("=" * 60)

def blending_ensemble(base_predictions_test, y_test, weights=None):
    """ব্লেন্ডিং এনসেম্বল"""
    if weights is None:
        # সমান ওয়েট
        weights = np.ones(len(base_predictions_test)) / len(base_predictions_test)
    
    # ওয়েটেড এভারেজ
    all_preds = np.column_stack(list(base_predictions_test.values()))
    blended_pred = all_preds @ weights
    
    return blended_pred

# সমান ওয়েট ব্লেন্ডিং
equal_blend = blending_ensemble(base_predictions, y_test)
equal_r2 = r2_score(y_test, equal_blend)
print(f"  Equal Weight Blend R²: {equal_r2:.4f}")

# বেস্ট ওয়েট খোঁজা
from scipy.optimize import minimize

def negative_r2(weights, preds, y_true):
    weighted_pred = np.column_stack(list(preds.values())) @ weights
    return -r2_score(y_true, weighted_pred)

n_models = len(base_predictions)
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = [(0, 1)] * n_models
initial_weights = np.ones(n_models) / n_models

result = minimize(negative_r2, initial_weights, method='SLSQP',
                  bounds=bounds, constraints=constraints,
                  args=(base_predictions, y_test))

optimal_weights = result.x
optimal_blend = blending_ensemble(base_predictions, y_test, optimal_weights)
optimal_r2 = r2_score(y_test, optimal_blend)

print(f"  Optimal Weight Blend R²: {optimal_r2:.4f}")
print(f"\n  Optimal Weights:")
for name, weight in zip(base_predictions.keys(), optimal_weights):
    print(f"    {name:<20}: {weight:.4f}")
```

### 4. মডেল তুলনা
```python
# ============================================
# মডেল তুলনা
# ============================================
print("\n" + "=" * 60)
print("📊 MODEL COMPARISON")
print("=" * 60)

comparison = {
    **{f"Base_{name}": score for name, score in base_scores.items()},
    "Equal_Blend": equal_r2,
    "Optimal_Blend": optimal_r2,
    "Stacking_Ensemble": stacking_r2
}

print(f"\n{'Model':<25} {'R² Score':<12}")
print("-" * 40)
for model, score in sorted(comparison.items(), key=lambda x: x[1], reverse=True):
    marker = "🏆" if score == max(comparison.values()) else ""
    print(f"{marker} {model:<25} {score:<12.4f}")
```

### 5. ফিচার ইম্পরটেন্স (মেটা-লেভেল)
```python
# ============================================
# মেটা-ফিচার ইম্পরটেন্স
# ============================================
print("\n" + "=" * 60)
print("🔍 META-FEATURE IMPORTANCE")
print("=" * 60)

# মেটা-মডেল কোফিসিয়েন্টস
meta_coef = stacking_result['meta_model'].coef_
meta_feature_names = list(base_models.keys())

importance_df = pd.DataFrame({
    'base_model': meta_feature_names,
    'meta_weight': meta_coef.round(4)
}).sort_values('meta_weight', ascending=False)

print("\n📊 Meta Model Feature Weights:")
print(importance_df.to_string(index=False))

# ভিজুয়ালাইজেশন
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
models = list(comparison.keys())
scores = list(comparison.values())
colors = ['lightblue'] * len(base_models) + ['lightgreen', 'green', 'gold']
bars = plt.bar(models, scores, color=colors)
plt.xticks(rotation=45, ha='right')
plt.ylabel('R² Score')
plt.title('Model Comparison: Base vs Ensemble')
plt.axhline(y=max(scores), color='red', linestyle='--', alpha=0.5)
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.bar(importance_df['base_model'], importance_df['meta_weight'], color='coral')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Meta Model Weight')
plt.title('Meta-Model Feature Importance')
plt.axhline(y=0, color='black', linewidth=0.5)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 6. স্ট্যাকিং vs ব্লেন্ডিং
```python
# ============================================
# স্ট্যাকিং vs ব্লেন্ডিং
# ============================================
print("\n" + "=" * 60)
print("⚖️ STACKING vs BLENDING")
print("=" * 60)

print("""
📌 Key Differences:

Stacking (Stacked Generalization):
✅ Uses out-of-fold predictions for meta-features
✅ More robust (no data leakage)
✅ Meta-model learns from validation patterns
✅ Better generalization typically
❌ More computationally expensive (CV training)
❌ More complex to implement

Blending (Weighted Average):
✅ Simpler and faster
✅ Easy to interpret (explicit weights)
✅ Works well with diverse models
✅ Less risk of overfitting
❌ May not learn complex interactions
❌ Optimal weights can overfit

📋 When to Use:
Stacking: Large dataset, computational resources available
Blending: Small dataset, need quick ensemble, simplicity
Both: Always test both and compare!
""")
```

### স্ট্যাকিং/ব্লেন্ডিং বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ ENSEMBLE BEST PRACTICES")
print("=" * 60)

print("""
📋 Ensemble Strategy:

1️⃣ Base Model Diversity
   - Different algorithms (linear, tree, kernel)
   - Different hyperparameters
   - Different feature subsets
   - Diversity > individual accuracy

2️⃣ Meta-Model Selection
   - Simple model (Ridge, Logistic Regression)
   - Avoid complex meta-models (overfitting risk)
   - Linear meta-model is often enough

3️⃣ Validation Strategy
   - Out-of-fold predictions (no leakage)
   - Holdout set for meta-model
   - Nested cross-validation for tuning

4️⃣ Common Pitfalls
   - Too many similar base models
   - Overfitting meta-model
   - Not enough diversity
   - Data leakage in meta-features

🚀 Advanced Techniques:
- Stacking with different feature subsets
- Multi-level stacking
- Blending with correlation-based weights
- Bayesian model averaging
""")
```

### সারসংক্ষেপ
আজ আমরা স্ট্যাকিং এবং ব্লেন্ডিং শিখলাম:
- **স্ট্যাকিং**: OOF প্রেডিকশন + মেটা-মডেল
- **ব্লেন্ডিং**: ওয়েটেড এভারেজ (সমান + অপ্টিমাল)
- **মেটা-ফিচার ইম্পরটেন্স**: কোন বেস মডেল সবচেয়ে উপযোগী
- **স্ট্যাকিং vs ব্লেন্ডিং**: কখন কোনটি ব্যবহার করবেন

### অনুশীলনী
1. 3-লেভেল স্ট্যাকিং ইমপ্লিমেন্ট করুন
2. কোরিলেশন-বেসড ব্লেন্ডিং ওয়েট তৈরি করুন
3. ক্লাসিফিকেশন টাস্কের জন্য স্ট্যাকিং ইমপ্লিমেন্ট করুন
4. ML-Ensemble লাইব্রেরি ব্যবহার করে সুপার-লার্নার তৈরি করুন