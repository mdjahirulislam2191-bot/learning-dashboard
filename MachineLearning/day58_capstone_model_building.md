# Day 58: ক্যাপস্টোন প্রোজেক্ট — মডেল বিল্ডিং
## Capstone Project: Model Building

### একাধিক মডেল ট্রেইনিং
বিভিন্ন অ্যালগরিদম ব্যবহার করে মডেল ট্রেইন করব এবং সেরাটি নির্বাচন করব।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (
    cross_val_score, KFold, GridSearchCV, RandomizedSearchCV
)
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor
)
from sklearn.svm import SVR
import xgboost as xgb
import joblib
import time
import warnings
warnings.filterwarnings('ignore')
```

### ডেটা লোড

```python
# ফিচার ইঞ্জিনিয়ারিং করা ডেটা লোড
X_train = joblib.load('X_train_final.pkl')
X_test = joblib.load('X_test_final.pkl')
y_train = joblib.load('y_train.pkl')
y_test = joblib.load('y_test.pkl')

print(f"ট্রেইন সেট: {X_train.shape}")
print(f"টেস্ট সেট: {X_test.shape}")
print(f"ফিচার সংখ্যা: {X_train.shape[1]}")
```

### মডেল ইভালুয়েশন ফাংশন

```python
def evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    """মডেল ইভালুয়েশন এবং মেট্রিক্স"""
    
    start_time = time.time()
    
    # ট্রেইন
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # প্রেডিকশন
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # মেট্রিক্স
    metrics = {
        'model_name': model_name,
        'train_time': train_time,
        'train_r2': r2_score(y_train, y_train_pred),
        'test_r2': r2_score(y_test, y_test_pred),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
        'train_mae': mean_absolute_error(y_train, y_train_pred),
        'test_mae': mean_absolute_error(y_test, y_test_pred),
        'overfitting_gap': r2_score(y_train, y_train_pred) - r2_score(y_test, y_test_pred)
    }
    
    # ক্রস-ভ্যালিডেশন
    cv_scores = cross_val_score(
        model, X_train, y_train, 
        cv=5, scoring='r2'
    )
    metrics['cv_mean'] = cv_scores.mean()
    metrics['cv_std'] = cv_scores.std()
    
    return metrics, y_test_pred

def print_metrics(metrics):
    """মেট্রিক্স প্রিন্ট"""
    print(f"\n{'='*50}")
    print(f"মডেল: {metrics['model_name']}")
    print(f"{'='*50}")
    print(f"ট্রেইন টাইল: {metrics['train_time']:.2f} সেকেন্ড")
    print(f"\nR² স্কোর:")
    print(f"  ট্রেইন: {metrics['train_r2']:.4f}")
    print(f"  টেস্ট:  {metrics['test_r2']:.4f}")
    print(f"\nRMSE:")
    print(f"  ট্রেইন: {metrics['train_rmse']:.2f}")
    print(f"  টেস্ট:  {metrics['test_rmse']:.2f}")
    print(f"\nMAE:")
    print(f"  ট্রেইন: {metrics['train_mae']:.2f}")
    print(f"  টেস্ট:  {metrics['test_mae']:.2f}")
    print(f"\nক্রস-ভ্যালিডেশন R²: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
    print(f"ওভারফিটিং গ্যাপ: {metrics['overfitting_gap']:.4f}")
```

### ১. বেসলাইন মডেল (লিনিয়ার রিগ্রেশন)

```python
print("\n=== বেসলাইন মডেল: লিনিয়ার রিগ্রেশন ===")
lr = LinearRegression()
lr_metrics, lr_pred = evaluate_model(
    lr, X_train, y_train, X_test, y_test, 
    'লিনিয়ার রিগ্রেশন'
)
print_metrics(lr_metrics)
```

### ২. রিজ রিগ্রেশন (L2 রেগুলারাইজেশন)

```python
print("\n=== রিজ রিগ্রেশন ===")
# হাইপারপ্যারামিটার টিউনিং
ridge_params = {'alpha': [0.01, 0.1, 1, 10, 100]}
ridge_grid = GridSearchCV(
    Ridge(), ridge_params, cv=5, scoring='r2'
)
ridge_grid.fit(X_train, y_train)

print(f"সেরা alpha: {ridge_grid.best_params_['alpha']}")
print(f"সেরা স্কোর: {ridge_grid.best_score_:.4f}")

ridge = ridge_grid.best_estimator_
ridge_metrics, ridge_pred = evaluate_model(
    ridge, X_train, y_train, X_test, y_test,
    'রিজ রিগ্রেশন'
)
print_metrics(ridge_metrics)
```

### ৩. লাসো রিগ্রেশন (L1 রেগুলারাইজেশন)

```python
print("\n=== লাসো রিগ্রেশন ===")
lasso_params = {'alpha': [0.001, 0.01, 0.1, 1, 10]}
lasso_grid = GridSearchCV(
    Lasso(max_iter=10000), lasso_params, cv=5, scoring='r2'
)
lasso_grid.fit(X_train, y_train)

print(f"সেরা alpha: {lasso_grid.best_params_['alpha']}")
print(f"সেরা স্কোর: {lasso_grid.best_score_:.4f}")

lasso = lasso_grid.best_estimator_
lasso_metrics, lasso_pred = evaluate_model(
    lasso, X_train, y_train, X_test, y_test,
    'লাসো রিগ্রেশন'
)
print_metrics(lasso_metrics)

# লাসো দ্বারা সিলেক্টেড ফিচার
selected_features = np.sum(lasso.coef_ != 0)
print(f"\nলাসো দ্বারা সিলেক্টেড ফিচার: {selected_features}")
```

### ৪. র্যান্ডম ফরেস্ট

```python
print("\n=== র্যান্ডম ফরেস্ট রিগ্রেসর ===")
rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_random = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    rf_params,
    n_iter=20,
    cv=3,
    scoring='r2',
    random_state=42,
    n_jobs=-1
)
rf_random.fit(X_train, y_train)

print(f"সেরা প্যারামিটার:")
for param, value in rf_random.best_params_.items():
    print(f"  {param}: {value}")
print(f"সেরা স্কোর: {rf_random.best_score_:.4f}")

rf = rf_random.best_estimator_
rf_metrics, rf_pred = evaluate_model(
    rf, X_train, y_train, X_test, y_test,
    'র্যান্ডম ফরেস্ট'
)
print_metrics(rf_metrics)
```

### ৫. গ্রেডিয়েন্ট বুস্টিং

```python
print("\n=== গ্রেডিয়েন্ট বুস্টিং রিগ্রেসর ===")
gbr_params = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 0.9, 1.0]
}
gbr_random = RandomizedSearchCV(
    GradientBoostingRegressor(random_state=42),
    gbr_params,
    n_iter=20,
    cv=3,
    scoring='r2',
    random_state=42
)
gbr_random.fit(X_train, y_train)

print(f"সেরা প্যারামিটার:")
for param, value in gbr_random.best_params_.items():
    print(f"  {param}: {value}")
print(f"সেরা স্কোর: {gbr_random.best_score_:.4f}")

gbr = gbr_random.best_estimator_
gbr_metrics, gbr_pred = evaluate_model(
    gbr, X_train, y_train, X_test, y_test,
    'গ্রেডিয়েন্ট বুস্টিং'
)
print_metrics(gbr_metrics)
```

### ৬. XGBoost

```python
print("\n=== XGBoost রিগ্রেসর ===")
xgb_params = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}
xgb_random = RandomizedSearchCV(
    xgb.XGBRegressor(random_state=42, verbosity=0),
    xgb_params,
    n_iter=20,
    cv=3,
    scoring='r2',
    random_state=42
)
xgb_random.fit(X_train, y_train)

print(f"সেরা প্যারামিটার:")
for param, value in xgb_random.best_params_.items():
    print(f"  {param}: {value}")
print(f"সেরা স্কোর: {xgb_random.best_score_:.4f}")

xgb_model = xgb_random.best_estimator_
xgb_metrics, xgb_pred = evaluate_model(
    xgb_model, X_train, y_train, X_test, y_test,
    'XGBoost'
)
print_metrics(xgb_metrics)
```

### মডেল তুলনা

```python
# সব মডেলের মেট্রিক্স একসাথে
all_metrics = [
    lr_metrics, ridge_metrics, lasso_metrics,
    rf_metrics, gbr_metrics, xgb_metrics
]

comparison_df = pd.DataFrame(all_metrics)
comparison_df = comparison_df.sort_values('test_r2', ascending=False)

print("\n=== মডেল তুলনা ===")
print("\nটেস্ট R² অনুযায়ী র‍্যাঙ্কিং:")
print(comparison_df[['model_name', 'test_r2', 'test_rmse', 'test_mae', 
                      'train_time', 'overfitting_gap']].to_string(index=False))

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# R² তুলনা
axes[0, 0].barh(comparison_df['model_name'], comparison_df['test_r2'])
axes[0, 0].set_xlabel('R² স্কোর')
axes[0, 0].set_title('টেস্ট R² তুলনা')

# RMSE তুলনা
axes[0, 1].barh(comparison_df['model_name'], comparison_df['test_rmse'])
axes[0, 1].set_xlabel('RMSE')
axes[0, 1].set_title('টেস্ট RMSE তুলনা')

# ট্রেইনিং টাইম
axes[1, 0].barh(comparison_df['model_name'], comparison_df['train_time'])
axes[1, 0].set_xlabel('সেকেন্ড')
axes[1, 0].set_title('ট্রেইনিং টাইম')

# ওভারফিটিং গ্যাপ
axes[1, 1].barh(comparison_df['model_name'], comparison_df['overfitting_gap'])
axes[1, 1].set_xlabel('R² গ্যাপ (ট্রেইন - টেস্ট)')
axes[1, 1].set_title('ওভারফিটিং গ্যাপ')

plt.tight_layout()
plt.savefig('capstone_model_comparison.png', dpi=100)
plt.show()
print("মডেল তুলনা চার্ট সেভ করা হয়েছে")
```

### সেরা মডেল নির্বাচন এবং সেভ

```python
# সেরা মডেল (সর্বোচ্চ টেস্ট R²)
best_model_idx = comparison_df['test_r2'].idxmax()
best_model_name = comparison_df.loc[best_model_idx, 'model_name']
best_model = [lr, ridge, lasso, rf, gbr, xgb_model][best_model_idx]

print(f"\n{'='*50}")
print(f"সেরা মডেল: {best_model_name}")
print(f"{'='*50}")
print(f"টেস্ট R²: {comparison_df.loc[best_model_idx, 'test_r2']:.4f}")
print(f"টেস্ট RMSE: {comparison_df.loc[best_model_idx, 'test_rmse']:.2f}")

# মডেল সেভ
joblib.dump(best_model, 'best_model.pkl')
joblib.dump(all_metrics, 'model_metrics.pkl')

print("\nসেরা মডেল সেভ করা হয়েছে: best_model.pkl")

# সব মডেল সেভ (প্রয়োজন হলে)
models = {
    'linear_regression': lr,
    'ridge': ridge,
    'lasso': lasso,
    'random_forest': rf,
    'gradient_boosting': gbr,
    'xgboost': xgb_model
}
joblib.dump(models, 'all_models.pkl')
print("সব মডেল সেভ করা হয়েছে: all_models.pkl")
```

### অ্যাকচুয়াল vs প্রেডিক্টেড

```python
plt.figure(figsize=(8, 8))
plt.scatter(y_test, best_model.predict(X_test), alpha=0.6, s=50)
plt.plot([y_test.min(), y_test.max()], 
         [y_test.min(), y_test.max()], 
         'r--', lw=2, label='পারফেক্ট প্রেডিকশন')
plt.xlabel('অ্যাকচুয়াল ভ্যালু')
plt.ylabel('প্রেডিক্টেড ভ্যালু')
plt.title(f'অ্যাকচুয়াল vs প্রেডিক্টেড — {best_model_name}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('capstone_actual_vs_predicted.png', dpi=100)
plt.show()
print("অ্যাকচুয়াল vs প্রেডিক্টেড প্লট সেভ করা হয়েছে")
```

### সারাংশ
- ✅ ৬টি ভিন্ন মডেল ট্রেইন করা হয়েছে
- ✅ হাইপারপ্যারামিটার টিউনিং (Grid/Randomized Search)
- ✅ ক্রস-ভ্যালিডেশন সহ মূল্যায়ন
- ✅ মডেল তুলনা এবং সেরা মডেল নির্বাচন
- ✅ ওভারফিটিং চেক
- ✅ সেরা মডেল সেভ (best_model.pkl)