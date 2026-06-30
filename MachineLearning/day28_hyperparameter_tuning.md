# Day 28: হাইপারপ্যারামিটার টিউনিং
## Hyperparameter Tuning

### হাইপারপ্যারামিটার টিউনিং কি?
হাইপারপ্যারামিটার হল মডেলের কনফিগারেশন সেটিংস যা ট্রেইনিং শুরু হওয়ার আগে সেট করা হয়। টিউনিং হল সেরা কম্বিনেশন খুঁজে বের করার প্রক্রিয়া যা মডেল পারফরম্যান্স সর্বোচ্চ করে।

### কেন হাইপারপ্যারামিটার টিউনিং গুরুত্বপূর্ণ?
- মডেল অ্যাকুরেসি উন্নত করে
- ওভারফিটিং/আন্ডারফিটিং নিয়ন্ত্রণ করে
- মডেলের জেনারালাইজেশন ক্ষমতা বাড়ায়

### ফাইন্যান্স উদাহরণ: স্টক রিটার্ন প্রেডিকশন
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     RandomizedSearchCV, cross_val_score)
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from scipy.stats import randint, uniform

# ফাইন্যান্স ডেটা তৈরি
np.random.seed(42)
n = 500
X = np.random.randn(n, 10)
true_coef = np.array([0.5, -0.3, 0.8, 0, 0, 1.2, -0.5, 0, 0.3, 0])
y = X @ true_coef + np.random.randn(n) * 0.5

feature_names = [f'feat_{i}' for i in range(10)]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")
```

### 1. গ্রিড সার্চ (GridSearchCV)
```python
# Random Forest এর জন্য গ্রিড সার্চ
rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

rf = RandomForestRegressor(random_state=42)
rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring='r2', 
                       n_jobs=-1, verbose=0)

print("Running GridSearchCV for Random Forest...")
rf_grid.fit(X_train, y_train)

print(f"Best parameters: {rf_grid.best_params_}")
print(f"Best CV score: {rf_grid.best_score_:.4f}")
print(f"Test score: {rf_grid.score(X_test, y_test):.4f}")

# GridSearchCV ফলাফল
results = pd.DataFrame(rf_grid.cv_results_)
print(f"\nTotal combinations searched: {len(results)}")
print(f"Time taken: {results['mean_fit_time'].sum():.2f}s")
```

### 2. র্যান্ডম সার্চ (RandomizedSearchCV)
```python
# Gradient Boosting এর জন্য র্যান্ডম সার্চ
gb_params = {
    'n_estimators': randint(50, 300),
    'max_depth': randint(3, 15),
    'learning_rate': uniform(0.01, 0.3),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'subsample': uniform(0.6, 0.4)
}

gb = GradientBoostingRegressor(random_state=42)
gb_random = RandomizedSearchCV(gb, gb_params, n_iter=30, cv=5,
                                scoring='r2', n_jobs=-1, 
                                random_state=42, verbose=0)

print("\nRunning RandomizedSearchCV for Gradient Boosting...")
gb_random.fit(X_train, y_train)

print(f"Best parameters: {gb_random.best_params_}")
print(f"Best CV score: {gb_random.best_score_:.4f}")
print(f"Test score: {gb_random.score(X_test, y_test):.4f}")
```

### 3. বেইসিয়ান অপ্টিমাইজেশন (Optuna উদাহরণ)
```python
# Optuna দিয়ে বেইসিয়ান অপ্টিমাইজেশন
try:
    import optuna
    
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 20),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
        }
        
        model = RandomForestRegressor(**params, random_state=42)
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        return scores.mean()
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=30)
    
    print(f"\nBest Optuna parameters: {study.best_params}")
    print(f"Best CV score: {study.best_value:.4f}")
    
    # Train best model
    best_rf = RandomForestRegressor(**study.best_params, random_state=42)
    best_rf.fit(X_train, y_train)
    print(f"Optuna test score: {best_rf.score(X_test, y_test):.4f}")
    
    # Visualization
    fig = optuna.visualization.plot_optimization_history(study)
    fig.show()
    
except ImportError:
    print("\nOptuna not installed. Install with: pip install optuna")
```

### 4. হাইপারপ্যারামিটার টিউনিং বিশ্লেষণ
```python
# ডিফল্ট vs টিউনড মডেল তুলনা
models = {
    'Default RF': RandomForestRegressor(random_state=42),
    'Tuned RF (Grid)': RandomForestRegressor(**rf_grid.best_params_, random_state=42),
    'Default GB': GradientBoostingRegressor(random_state=42),
    'Tuned GB (Random)': GradientBoostingRegressor(**gb_random.best_params_, random_state=42)
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    results.append({
        'Model': name,
        'Train R²': train_score,
        'Test R²': test_score,
        'RMSE': rmse
    })

comparison = pd.DataFrame(results)
print("\nDefault vs Tuned Models:")
print(comparison.to_string(index=False))

# ওভারফিটিং চেক
print("\nOverfitting Check (Train - Test gap):")
for r in results:
    gap = r['Train R²'] - r['Test R²']
    print(f"{r['Model']}: {gap:.4f}")
```

### 5. হাইপারপ্যারামিটার ইমপ্যাক্ট ভিজুয়ালাইজেশন
```python
# n_estimators vs score
n_ests = range(10, 201, 10)
scores = []

for n in n_ests:
    rf = RandomForestRegressor(n_estimators=n, max_depth=10, random_state=42)
    s = cross_val_score(rf, X_train, y_train, cv=3, scoring='r2').mean()
    scores.append(s)

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(n_ests, scores, 'b-', linewidth=2)
plt.xlabel('Number of Estimators')
plt.ylabel('CV R² Score')
plt.title('n_estimators vs Performance')
plt.grid(True, alpha=0.3)

# max_depth vs score
depths = range(1, 21)
depth_scores = []

for d in depths:
    rf = RandomForestRegressor(n_estimators=100, max_depth=d, random_state=42)
    s = cross_val_score(rf, X_train, y_train, cv=3, scoring='r2').mean()
    depth_scores.append(s)

plt.subplot(1, 2, 2)
plt.plot(depths, depth_scores, 'r-', linewidth=2)
plt.xlabel('Max Depth')
plt.ylabel('CV R² Score')
plt.title('max_depth vs Performance')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### হাইপারপ্যারামিটার টিউনিং বেস্ট প্র্যাকটিস
```python
print("""
📌 Hyperparameter Tuning Best Practices:
1️⃣ Start with Random Search for broad exploration
2️⃣ Fine-tune with Grid Search around promising regions
3️⃣ Use cross-validation (min 5-fold)
4️⃣ Set aside a validation set before tuning
5️⃣ Consider model complexity vs. performance trade-off
6️⃣ Use Bayesian Optimization for expensive models
7️⃣ Don't tune on the test set!
8️⃣ Parallelize with n_jobs for speed
""")
```

### সারসংক্ষেপ
আজ আমরা হাইপারপ্যারামিটার টিউনিং এর বিভিন্ন পদ্ধতি শিখলাম:
- **GridSearchCV**: সব কম্বিনেশন ব্রুট-ফোর্স চেক
- **RandomizedSearchCV**: র্যান্ডম কম্বিনেশন চেক (দ্রুত)
- **Bayesian Optimization**: (Optuna) - ইতিহাস ব্যবহার করে স্মার্ট সার্চ
- **ডিফল্ট vs টিউনড মডেল**: স্পষ্ট পারফরম্যান্স ইম্প্রুভমেন্ট

### অনুশীলনী
1. SVR মডেলের জন্য GridSearchCV ব্যবহার করে সেরা প্যারামিটার খুঁজুন
2. Optuna ব্যবহার করে XGBoost মডেল টিউন করুন
3. হাইপারপ্যারামিটার টিউনিং এর সময় vs পারফরম্যান্স ট্রেড-অফ অ্যানালাইসিস করুন
4. হ্যাল্পিং প্যারামিটার (HalvingGridSearchCV) ব্যবহার করে আরও ইফিশিয়েন্ট সার্চ করুন