# Day 47: এক্সপেরিমেন্ট ডিজাইন
## Experiment Design

### এক্সপেরিমেন্ট ডিজাইন কি?
এক্সপেরিমেন্ট ডিজাইন (DOE) হল সিস্টেম্যাটিক পদ্ধতি যা টেস্টের পরিকল্পনা, পরিচালনা এবং বিশ্লেষণ করে। ML-তে এটি মডেল উন্নতি এবং হাইপারপ্যারামিটার অপ্টিমাইজেশনের জন্য গুরুত্বপূর্ণ।

### ফাইন্যান্স অ্যাপ্লিকেশন
- **বিভিন্ন ML মডেলের তুলনা**
- **ফিচার ইঞ্জিনিয়ারিং কৌশলের প্রভাব**
- **ট্রেডিং স্ট্র্যাটেজি ব্যাকটেস্টিং**
- **রিস্ক মডেল ভ্যালিডেশন**

### ফাইন্যান্স উদাহরণ: ML এক্সপেরিমেন্ট
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
import itertools
import warnings
warnings.filterwarnings('ignore')

# ফাইন্যান্স ডেটা
np.random.seed(42)
n = 1000
X = np.random.randn(n, 10)
y = X @ np.array([0.5, -0.3, 0.8, 0, 0.2, 1.2, -0.5, 0, 0.3, 0]) + np.random.randn(n) * 0.3
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("📊 Financial Prediction Dataset")
print(f"  Features: {X.shape[1]}")
print(f"  Train: {len(X_train)}, Test: {len(X_test)}")
```

### 1. এক্সপেরিমেন্ট প্ল্যানিং
```python
# ============================================
# এক্সপেরিমেন্ট প্ল্যান
# ============================================
print("\n" + "=" * 60)
print("📋 EXPERIMENT PLAN")
print("=" * 60)

experiment_plan = {
    "experiment_id": "EXP-001",
    "name": "Stock Return Prediction Model Comparison",
    "hypothesis": "GradientBoosting outperforms RandomForest for this dataset",
    "variables": {
        "independent": ["model_type", "n_estimators", "max_depth"],
        "dependent": ["RMSE", "R²", "Training Time"]
    },
    "control_model": "LinearRegression",
    "treatment_models": ["RandomForest", "GradientBoosting"],
    "validation": "5-fold Cross Validation",
    "success_criteria": "R² improvement > 0.05 over baseline"
}

print("📌 Experiment Plan:")
for key, val in experiment_plan.items():
    print(f"  {key}: {val}")
```

### 2. ফ্যাক্টোরিয়াল ডিজাইন
```python
# ============================================
# ফ্যাক্টোরিয়াল ডিজাইন (মাল্টিপল প্যারামিটার)
# ============================================
print("\n" + "=" * 60)
print("📊 FACTORIAL DESIGN")
print("=" * 60)

# প্যারামিটার কম্বিনেশন
params = {
    'model_type': ['RF', 'GB', 'Ridge'],
    'n_estimators': [50, 100],
    'max_depth': [5, 10, None]
}

# ফুল ফ্যাক্টোরিয়াল
all_combinations = list(itertools.product(*params.values()))
print(f"Full factorial design: {len(all_combinations)} combinations")

# র‍্যান্ডম সাবসেট (ফ্র্যাকশনাল ফ্যাক্টোরিয়াল)
import random
random.seed(42)
n_samples = min(8, len(all_combinations))
sampled_combinations = random.sample(all_combinations, n_samples)

print(f"Sampled (fractional): {len(sampled_combinations)} combinations")
print("\n📋 Experiment Matrix:")
print(f"{'Exp #':<6} {'Model':<15} {'n_est':<10} {'max_depth':<10}")
print("-" * 45)
for i, combo in enumerate(sampled_combinations):
    print(f"{i+1:<6} {str(combo[0]):<15} {str(combo[1]):<10} {str(combo[2]):<10}")
```

### 3. এক্সপেরিমেন্ট রান
```python
# ============================================
# এক্সপেরিমেন্ট এক্সিকিউশন
# ============================================
print("\n" + "=" * 60)
print("🚀 EXPERIMENT EXECUTION")
print("=" * 60)

import time

experiment_results = []

for exp_id, combo in enumerate(sampled_combinations):
    model_type, n_est, max_depth = combo
    
    if model_type == 'RF':
        model = RandomForestRegressor(n_estimators=n_est, max_depth=max_depth, random_state=42)
    elif model_type == 'GB':
        model = GradientBoostingRegressor(n_estimators=n_est, max_depth=max_depth if max_depth else 3, random_state=42)
    else:
        model = Ridge(alpha=1.0)
    
    start_time = time.time()
    
    # CV
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    
    # ট্রেন
    model.fit(X_train, y_train)
    
    # টেস্ট
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    train_time = time.time() - start_time
    
    experiment_results.append({
        'exp_id': exp_id + 1,
        'model': model_type,
        'n_estimators': n_est,
        'max_depth': max_depth if model_type != 'Ridge' else 'N/A',
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_rmse': rmse,
        'test_r2': r2,
        'train_time_s': train_time
    })
    
    print(f"Exp {exp_id+1:2d}: {model_type:<6} n_est={n_est:3d} depth={str(max_depth):>4} "
          f"→ CV R²={cv_scores.mean():.4f} Test R²={r2:.4f} Time={train_time:.2f}s")

results_df = pd.DataFrame(experiment_results)
```

### 4. এক্সপেরিমেন্ট বিশ্লেষণ
```python
# ============================================
# ফলাফল বিশ্লেষণ
# ============================================
print("\n" + "=" * 60)
print("📊 EXPERIMENT ANALYSIS")
print("=" * 60)

print("\n📋 Top 3 Experiments by Test R²:")
print(results_df.sort_values('test_r2', ascending=False)[
    ['exp_id', 'model', 'n_estimators', 'max_depth', 'test_r2', 'cv_mean']
].head(3).to_string(index=False))

# মডেল টাইপ অনুযায়ী পারফরম্যান্স
print("\n📊 Performance by Model Type:")
model_perf = results_df.groupby('model').agg({
    'test_r2': ['mean', 'std', 'max'],
    'train_time_s': 'mean'
}).round(4)
print(model_perf.to_string())

# বেস্ট মডেল
best = results_df.loc[results_df['test_r2'].idxmax()]
print(f"\n🏆 Best Model: {best['model']} (n_est={best['n_estimators']}, depth={best['max_depth']})")
print(f"   Test R²: {best['test_r2']:.4f}, CV Mean: {best['cv_mean']:.4f}")
```

### 5. লার্নিং কার্ভ এবং ডায়াগনস্টিক
```python
# ============================================
# লার্নিং কার্ভ অ্যানালাইসিস
# ============================================
print("\n" + "=" * 60)
print("📈 LEARNING CURVE ANALYSIS")
print("=" * 60)

from sklearn.model_selection import learning_curve

def plot_learning_curve(model, X, y, title):
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5, scoring='r2', n_jobs=-1
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='orange')
    plt.plot(train_sizes, train_mean, 'b-o', label='Training Score')
    plt.plot(train_sizes, test_mean, 'o-', color='orange', label='Cross-validation Score')
    plt.xlabel('Training Examples')
    plt.ylabel('R² Score')
    plt.title(f'Learning Curve: {title}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# বেস্ট মডেলের লার্নিং কার্ভ
best_model_type = best['model']
if best_model_type == 'RF':
    model_lc = RandomForestRegressor(n_estimators=int(best['n_estimators']), 
                                      max_depth=best['max_depth'], random_state=42)
elif best_model_type == 'GB':
    model_lc = GradientBoostingRegressor(n_estimators=int(best['n_estimators']), random_state=42)
else:
    model_lc = Ridge(alpha=1.0)

print("📊 Plotting Learning Curve...")
# plot_learning_curve(model_lc, X_train, y_train, f"{best_model_type} (best model)")
```

### 6. রিপ্রোডিউসিবিলিটি
```python
# ============================================
# রিপ্রোডিউসিবিলিটি চেক
# ============================================
print("\n" + "=" * 60)
print("🔬 REPRODUCIBILITY CHECK")
print("=" * 60)

def run_reproducible_experiment(seeds=[42, 123, 456]):
    """মাল্টিপল সিড দিয়ে এক্সপেরিমেন্ট রিপ্রোডিউস"""
    results = []
    
    for seed in seeds:
        np.random.seed(seed)
        X_s = np.random.randn(n, 10)
        y_s = X_s @ np.array([0.5, -0.3, 0.8, 0, 0.2, 1.2, -0.5, 0, 0.3, 0]) + np.random.randn(n) * 0.3
        
        X_tr, X_te, y_tr, y_te = train_test_split(X_s, y_s, test_size=0.2, random_state=seed)
        
        rf = RandomForestRegressor(n_estimators=100, random_state=seed)
        rf.fit(X_tr, y_tr)
        
        r2 = r2_score(y_te, rf.predict(X_te))
        results.append({'seed': seed, 'test_r2': r2})
    
    results_df_s = pd.DataFrame(results)
    print(f"\n📊 Reproducibility Results:")
    print(results_df_s.to_string(index=False))
    print(f"\n  Mean R²: {results_df_s['test_r2'].mean():.4f} ± {results_df_s['test_r2'].std():.4f}")
    print(f"  Range: [{results_df_s['test_r2'].min():.4f}, {results_df_s['test_r2'].max():.4f}]")

run_reproducible_experiment()
```

### এক্সপেরিমেন্ট ডিজাইন বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ EXPERIMENT DESIGN BEST PRACTICES")
print("=" * 60)

print("""
📋 Experiment Design Framework:

1️⃣ Planning Phase
   - Define clear hypothesis (H₀ and H₁)
   - Identify variables (independent vs dependent)
   - Choose control and treatment
   - Determine success metrics
   - Calculate required sample size

2️⃣ Design Phase
   - Full factorial (all combinations)
   - Fractional factorial (efficient sampling)
   - Latin hypercube (continuous parameters)
   - Random search (high-dimensional)
   - Bayesian optimization (adaptive)

3️⃣ Execution Phase
   - Randomize experiment order
   - Block on known confounders
   - Record all parameters and metadata
   - Log system state (versions, seeds)
   - Run multiple replicates

4️⃣ Analysis Phase
   - Compare to baseline
   - Statistical significance testing
   - Practical significance (business impact)
   - Sensitivity analysis
   - Failure analysis (why did it fail?)

5️⃣ Documentation
   - Experiment registry (MLflow, Neptune)
   - Share findings with team
   - Reproduce key results
   - Archive all artifacts
   - Deploy winning model

⚠️ Common Pitfalls:
- Not using random seeds (non-deterministic)
- Over-testing (data snooping)
- Ignoring multiple comparison problem
- Not logging enough metadata
- Hacking p-values
""")
```

### সারসংক্ষেপ
আজ আমরা এক্সপেরিমেন্ট ডিজাইন শিখলাম:
- **এক্সপেরিমেন্ট প্ল্যানিং**: হাইপোথেসিস, ভেরিয়েবল, সুসেস ক্রাইটেরিয়া
- **ফ্যাক্টোরিয়াল ডিজাইন**: ফুল এবং ফ্র্যাকশনাল
- **এক্সিকিউশন**: প্যারামিটার কম্বিনেশন ট্র্যাকিং
- **লার্নিং কার্ভ**: আন্ডারফিটিং/ওভারফিটিং ডায়াগনস্টিক
- **রিপ্রোডিউসিবিলিটি**: সিড এবং এনভায়রনমেন্ট ভ্যারিয়েন্স

### অনুশীলনী
1. ল্যাটিন হাইপারকিউব স্যাম্পলিং ইমপ্লিমেন্ট করুন
2. বায়েসিয়ান অপ্টিমাইজেশন দিয়ে এক্সপেরিমেন্ট ডিজাইন করুন
3. মাল্টি-মেট্রিক অপ্টিমাইজেশনের জন্য প্যারেটো ফ্রন্টিয়ার ব্যবহার করুন
4. আপনার ML প্রজেক্টের জন্য একটি পূর্ণাঙ্গ এক্সপেরিমেন্ট প্ল্যান তৈরি করুন