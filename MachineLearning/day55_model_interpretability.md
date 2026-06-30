# Day 55: মডেল ইন্টারপ্রিটেবিলিটি
## Model Interpretability

### মডেল ইন্টারপ্রিটেবিলিটি কি?
মডেল ইন্টারপ্রিটেবিলিটি হল ML মডেলের সিদ্ধান্ত বোঝার এবং ব্যাখ্যা করার ক্ষমতা। এটি ট্রান্সপারেন্সি, ট্রাস্ট এবং রেগুলেটরি কমপ্লায়েন্সের জন্য গুরুত্বপূর্ণ।

### ফাইন্যান্সে ইন্টারপ্রিটেবিলিটি কেন প্রয়োজন?
- **রেগুলেটরি কমপ্লায়েন্স**: ECOA, FCRA
- **রিস্ক ম্যানেজমেন্ট**: মডেল ভুল বোঝা
- **স্টেকহোল্ডার কমিউনিকেশন**: ক্লায়েন্ট, রেগুলেটর
- **ডিবাগিং**: মডেল কেন ভুল করছে তা বোঝা

### ফাইন্যান্স উদাহরণ: সম্পূর্ণ ইন্টারপ্রিটেবিলিটি স্ট্যাক
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import partial_dependence, PartialDependenceDisplay
import warnings
warnings.filterwarnings('ignore')

# SHAP
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

# LIME
try:
    import lime
    import lime.lime_tabular
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False

# ডেটা
np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'credit_score': np.random.randint(500, 850, n),
    'income': np.random.randn(n) * 30000 + 50000,
    'loan_amount': np.random.randn(n) * 20000 + 100000,
    'debt_ratio': np.random.rand(n) * 0.5,
    'employment_years': np.random.randint(0, 30, n),
    'age': np.random.randint(22, 70, n),
    'num_late_payments': np.random.poisson(1, n),
    'credit_lines_ratio': np.random.rand(n) * 0.8
})

risk = (0.001 * (850 - data['credit_score']) + 
        0.3 * data['debt_ratio'] + 
        0.05 * data['num_late_payments'] + 
        0.1 * np.random.randn(n))
risk = np.clip(risk, 0, 1)

feature_cols = [c for c in data.columns]
X = data.values
X_train, X_test, y_train, y_test = train_test_split(X, risk, test_size=0.2, random_state=42)

# ব্ল্যাক বক্স মডেল (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("📊 Credit Risk Model")
print(f"  Features: {len(feature_cols)}")
print(f"  R² Score: {model.score(X_test, y_test):.4f}")
print(f"  Model Type: RandomForest (Black Box)")
```

### 1. গ্লোবাল ইন্টারপ্রিটেবিলিটি
```python
# ============================================
# গ্লোবাল ইন্টারপ্রিটেবিলিটি (পুরো মডেল)
# ============================================
print("\n" + "=" * 60)
print("🌍 GLOBAL INTERPRETABILITY")
print("=" * 60)

print("""
📊 Global Methods (Understanding the whole model):
""")

# 1. ফিচার ইম্পরটেন্স
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("1️⃣ Feature Importance (Gini):")
print(importance.to_string(index=False))

# 2. পার্শিয়াল ডিপেন্ডেন্স
print("\n2️⃣ Partial Dependence (Top 3 features):")
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, feat in zip(axes, importance['feature'].head(3)):
    idx = feature_cols.index(feat)
    PartialDependenceDisplay.from_estimator(
        model, X_test, idx, feature_names=feature_cols, ax=ax, grid_resolution=50
    )
    ax.set_title(f'PDP: {feat}')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 2. লোকাল ইন্টারপ্রিটেবিলিটি
```python
# ============================================
# লোকাল ইন্টারপ্রিটেবিলিটি (একক প্রেডিকশন)
# ============================================
print("=" * 60)
print("🔍 LOCAL INTERPRETABILITY")
print("=" * 60)

print("""
📊 Local Methods (Understanding single predictions):
""")

# একক উদাহরণ
sample_idx = 0
sample = X_test[sample_idx:sample_idx+1]
sample_pred = model.predict(sample)[0]

print(f"1️⃣ Single Prediction Explanation:")
print(f"   Sample: {sample_idx}")
print(f"   Predicted Risk: {sample_pred:.4f}")
print(f"   Feature Values:")
for i, feat in enumerate(feature_cols):
    print(f"     {feat}: {sample[0][i]:.4f}")
```

### 3. SHAP লোকাল ব্যাখ্যা
```python
# ============================================
# SHAP লোকাল + গ্লোবাল
# ============================================
print("\n" + "=" * 60)
print("🔧 SHAP INTERPRETABILITY")
print("=" * 60)

if SHAP_AVAILABLE:
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # লোকাল: ওয়াটারফল
    plt.figure(figsize=(12, 4))
    shap.waterfall_plot(
        shap.Explanation(
            values=shap_values[sample_idx],
            base_values=explainer.expected_value,
            data=X_test[sample_idx],
            feature_names=feature_cols
        ),
        show=False, max_display=10
    )
    plt.title('SHAP Waterfall: Local Explanation')
    plt.tight_layout()
    plt.show()
    
    # গ্লোবাল: সামারি
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_test, feature_names=feature_cols, show=False)
    plt.title('SHAP Summary: Global Importance')
    plt.tight_layout()
    plt.show()
    
    print("✅ SHAP provides both local + global explanations")
else:
    print("SHAP not available")
```

### 4. LIME ব্যাখ্যা
```python
# ============================================
# LIME (Local Interpretable Model-agnostic Explanations)
# ============================================
print("\n" + "=" * 60)
print("🔧 LIME EXPLANATION")
print("=" * 60)

if LIME_AVAILABLE:
    # LIME explainer
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        X_train,
        feature_names=feature_cols,
        mode='regression',
        random_state=42
    )
    
    # একক উদাহরণ ব্যাখ্যা
    exp = lime_explainer.explain_instance(
        X_test[sample_idx],
        model.predict,
        num_features=8
    )
    
    # টেক্সট ব্যাখ্যা
    print("\n📋 LIME Explanation for Sample:")
    print(f"  Prediction: {sample_pred:.4f}")
    print(f"  Intercept: {exp.intercept[1]:.4f}")
    print(f"\n  Feature Contributions:")
    
    for feat, coef in exp.as_list():
        direction = "🔺 Increases" if coef > 0 else "🔻 Decreases"
        print(f"    {feat}: {coef:+.4f} ({direction} risk)")
    
    # ভিজুয়ালাইজ
    fig = exp.as_pyplot_figure()
    plt.title('LIME Feature Contributions')
    plt.tight_layout()
    plt.show()
    
    print("✅ LIME provides local, interpretable explanations")
else:
    print("LIME not available. Install: pip install lime")
```

### 5. ইন্টারপ্রিটেবিলিটি পদ্ধতি তুলনা
```python
# ============================================
# পদ্ধতি তুলনা
# ============================================
print("\n" + "=" * 60)
print("⚖️ INTERPRETABILITY METHODS COMPARISON")
print("=" * 60)

comparison = pd.DataFrame({
    'Method': ['Feature Importance', 'Partial Dependence', 'SHAP', 'LIME'],
    'Scope': ['Global', 'Global', 'Both', 'Local'],
    'Speed': ['Very Fast', 'Fast', 'Fast (Tree)', 'Moderate'],
    'Model Agnostic': ['No (tree only)', 'Yes', 'Yes', 'Yes'],
    'Interaction': ['No', 'Yes (2D)', 'Yes', 'Limited'],
    'Direction (+/-)': ['No', 'Yes', 'Yes', 'Yes'],
    'Theoretical': ['Heuristic', 'Marginal Effect', 'Shapley Values', 'Local Surrogate']
})

print(comparison.to_string(index=False))

print("\n📌 When to Use Which:")
print("""
📋 Method Selection Guide:

1️⃣ Feature Importance (Gini/Permutation):
   ➜ "Which features are generally important?"

2️⃣ Partial Dependence (PDP/ICE):
   ➜ "How does feature X affect predictions?"

3️⃣ SHAP:
   ➜ "Why was this specific prediction made?"
   ➜ "Which features contributed how much?"
   ➜ Best overall method!

4️⃣ LIME:
   ➜ "Local surrogate for this single prediction"
   ➜ Good for non-tech stakeholders

🏆 Recommendation:
Use SHAP as primary method + PDP for visualization
+ LIME for specific stakeholder presentations
""")
```

### 6. কমপ্লায়েন্স রিপোর্ট
```python
# ============================================
# রেগুলেটরি কমপ্লায়েন্স রিপোর্ট
# ============================================
print("\n" + "=" * 60)
print("📋 COMPLIANCE REPORT")
print("=" * 60)

compliance_report = f"""
📊 Model Interpretability Compliance Report

Model Info:
- Model Type: Random Forest Regressor
- Task: Credit Risk Assessment
- Features: {len(feature_cols)}
- Training Samples: {len(X_train)}
- Test R²: {model.score(X_test, y_test):.4f}

✅ Interpretability Methods Applied:
1. Feature Importance (Gini) - Global
2. Partial Dependence Plots - Global
3. SHAP Values - Both Global & Local
4. LIME - Local Explanations

📋 Compliance Checklist:
[✓] Global feature importance documented
[✓] Partial dependence plots for top features
[✓] Single prediction explanations available
[✓] Model bias assessment completed (Day 49)
[✓] Model card prepared (Day 50)

📌 Adverse Action Reasons (ECOA Compliance):
For denied loans, provide:
1. Primary factor: {importance.iloc[0]['feature']}
2. Secondary factor: {importance.iloc[1]['feature']}
3. Actionable feedback: Improve credit score or reduce debt ratio

Report Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
"""

print(compliance_report)
```

### ইন্টারপ্রিটেবিলিটি বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ INTERPRETABILITY BEST PRACTICES")
print("=" * 60)

print("""
📋 Interpretability Framework:

1️⃣ Intrinsic Interpretability (White Box)
   - Linear Regression, Decision Trees (shallow)
   - Sparse models (Lasso)
   - Pros: Naturally interpretable
   - Cons: May sacrifice accuracy

2️⃣ Post-Hoc Interpretability (Black Box)
   - SHAP, LIME, PDP, Importance
   - Pros: Any model works
   - Cons: Approximations, can be misleading

3️⃣ By Audience:
   - Data Scientists: SHAP, PDP, ICE
   - Business Stakeholders: Feature Importance, PDP
   - Regulators: Compliance Report, Fairness Metrics
   - End Users: Simple explanations (top 2-3 reasons)

4️⃣ Key Principles (Doshi-Velez & Kim, 2017):
   - Transparency: How does the model work?
   - Post-hoc: Can we explain decisions?
   - [x] Global: Whole model behavior
   - [x] Local: Single prediction behavior

⚠️ Remember:
- Interpretability is about building TRUST
- Different stakeholders need different explanations
- Always validate explanations with domain experts
- No single method is perfect → use multiple
""")
```

### সারসংক্ষেপ
আজ আমরা সম্পূর্ণ মডেল ইন্টারপ্রিটেবিলিটি স্ট্যাক শিখলাম:
- **গ্লোবাল**: Feature Importance, PDP, SHAP Summary
- **লোকাল**: SHAP Waterfall, LIME
- **তুলনা**: SHAP vs LIME vs PDP vs Importance
- **কমপ্লায়েন্স**: রেগুলেটরি রিপোর্টিং
- **প্র্যাকটিস**: কখন কোন পদ্ধতি ব্যবহার করবেন

### অনুশীলনী
1. সমস্ত ইন্টারপ্রিটেবিলিটি পদ্ধতি একসাথে একটি ইন্টারেক্টিভ ড্যাশবোর্ডে দেখান
2. হোয়াইট বক্স (Linear) এবং ব্ল্যাক বক্স (RF) মডেলের ইন্টারপ্রিটেবিলিটি তুলনা করুন
3. একাধিক স্টেকহোল্ডারের জন্য বিভিন্ন রিপোর্ট তৈরি করুন
4. এলিম (ELI5) লাইব্রেরি ব্যবহার করে ইন্টারপ্রিটেবিলিটি এক্সপ্লোর করুন