# Day 09: রেগুলারাইজেশন (Ridge/Lasso)
## Regularization - Ridge & Lasso

### Overfitting এবং Regularization
Overfitting তখন ঘটে যখন মডেল ট্রেনিং ডেটার নয়েজও শিখে ফেলে। Regularization পেনাল্টি টার্ম যোগ করে জটিলতা কমায়।

### L1 (Lasso) এবং L2 (Ridge) Regularization
- **Ridge (L2)**: β² পেনাল্টি → ফিচার কোএফিসিয়েন্ট ছোট করে
- **Lasso (L1)**: |β| পেনাল্টি → কিছু কোএফিসিয়েন্ট 0 করে (feature selection)

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

# হাই-ডাইমেনশনাল ফাইন্যান্স ডেটা
np.random.seed(42)
n = 200
n_features = 50  # অনেক ফিচার

# কিছু ফিচারই আসলে গুরুত্বপূর্ণ
true_features = 5
all_features = n_features

X = np.random.randn(n, all_features)
true_coefs = np.zeros(all_features)
true_coefs[:true_features] = np.random.randn(true_features) * 2

y = X @ true_coefs + np.random.randn(n) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"ডেটা আকৃতি: {X.shape}")
print(f"প্রকৃত গুরুত্বপূর্ণ ফিচার: {true_features}")
print(f"মোট ফিচার: {all_features}")
```

### Ridge Regression (L2)
```python
ridge = Ridge(alpha=1.0)  # alpha = regularization strength
ridge.fit(X_train, y_train)

y_pred_ridge = ridge.predict(X_test)
print("🏔️ Ridge Regression:")
print(f"R²: {r2_score(y_test, y_pred_ridge):.4f}")
print(f"Non-zero coefficients: {np.sum(ridge.coef_ != 0)}")
print(f"Mean |coef|: {np.abs(ridge.coef_).mean():.4f}")
```

### Lasso Regression (L1)
```python
lasso = Lasso(alpha=0.1)  # alpha = regularization strength
lasso.fit(X_train, y_train)

y_pred_lasso = lasso.predict(X_test)
print("\n🗡️ Lasso Regression:")
print(f"R²: {r2_score(y_test, y_pred_lasso):.4f}")
print(f"Non-zero coefficients: {np.sum(lasso.coef_ != 0)}")
print(f"Mean |coef|: {np.abs(lasso.coef_).mean():.4f}")

# কোন ফিচারগুলো বেছে নিয়েছে
selected = np.where(lasso.coef_ != 0)[0]
print(f"Selected features: {selected}")
```

### Regularization Strength এর প্রভাব
```python
alphas = [0.001, 0.01, 0.1, 1, 10, 100]
results = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    train_r2 = r2_score(y_train, ridge.predict(X_train))
    test_r2 = r2_score(y_test, ridge.predict(X_test))
    results.append({
        'alpha': alpha,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'n_coef': np.sum(np.abs(ridge.coef_) > 0.001)
    })

results_df = pd.DataFrame(results)
print("\n📊 Alpha টিউনিং:")
print(results_df.to_string(index=False))
```

### Ridge vs Lasso তুলনা
```python
plt.figure(figsize=(14, 5))

# Ridge
plt.subplot(1, 2, 1)
ridge_coef_path = []
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    ridge_coef_path.append(ridge.coef_)
ridge_coef_path = np.array(ridge_coef_path)

for i in range(5):
    plt.plot(alphas, ridge_coef_path[:, i], 'o-', label=f'Feature {i}')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Coefficient')
plt.title('Ridge (L2) - Coefficient Shrinkage')
plt.legend()
plt.grid(True, alpha=0.3)

# Lasso
plt.subplot(1, 2, 2)
lasso_coef_path = []
for alpha in alphas:
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train)
    lasso_coef_path.append(lasso.coef_[:5])
lasso_coef_path = np.array(lasso_coef_path)

for i in range(5):
    plt.plot(alphas, lasso_coef_path[:, i], 'o-', label=f'Feature {i}')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Coefficient')
plt.title('Lasso (L1) - Feature Selection')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### ElasticNet (Ridge + Lasso)
```python
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # l1_ratio: 0=Ridge, 1=Lasso
elastic.fit(X_train, y_train)
y_pred_elastic = elastic.predict(X_test)

print("\n🔄 ElasticNet:")
print(f"R²: {r2_score(y_test, y_pred_elastic):.4f}")
print(f"Non-zero coefficients: {np.sum(elastic.coef_ != 0)}")
```

### Cross-validation দিয়ে Best Alpha
```python
from sklearn.model_selection import GridSearchCV

# Ridge CV
ridge_cv = GridSearchCV(
    Ridge(), 
    param_grid={'alpha': [0.001, 0.01, 0.1, 1, 10, 100]},
    cv=5, scoring='r2'
)
ridge_cv.fit(X_train, y_train)
print(f"\n🏆 Best Ridge alpha: {ridge_cv.best_params_['alpha']}")
print(f"Best CV R²: {ridge_cv.best_score_:.4f}")

# Lasso CV
lasso_cv = GridSearchCV(
    Lasso(max_iter=5000), 
    param_grid={'alpha': [0.001, 0.01, 0.1, 1, 10]},
    cv=5, scoring='r2'
)
lasso_cv.fit(X_train, y_train)
print(f"🏆 Best Lasso alpha: {lasso_cv.best_params_['alpha']}")
print(f"Best CV R²: {lasso_cv.best_score_:.4f}")
```

### পোর্টফোলিও অপ্টিমাইজেশন (Regularization সাদৃশ্য)
```python
# রেগুলারাইজেশন পোর্টফোলিও ডাইভার্সিফিকেশন এনকোরেজ করে
print("\n💼 Portfolio Optimization Analogy:")
print("- Ridge = Equal Weight Portfolio (সবাই কিছু না কিছু পায়)")
print("- Lasso = Concentrated Portfolio (শুধু সেরা কয়েকটি)")
print("- Alpha = Risk Aversion Parameter")

# উদাহরণ: পোর্টফোলিও রেগুলারাইজেশন
n_stocks = 10
stock_returns = np.random.randn(100, n_stocks)
print(f"\nস্টক রিটার্ন ডেটা: {stock_returns.shape}")
```

### Ridge vs Lasso - কখন কী ব্যবহার করবেন?
```python
print("""
📋 When to use which:

Ridge (L2):
✅ সব ফিচারই কিছুটা গুরুত্বপূর্ণ
✅ ফিচার সংখ্যা কম
✅ গ্রুপড ফিচার (multi-collinearity)
✅ Stable solution

Lasso (L1):
✅ স্পার্সিটি প্রয়োজন (feature selection)
✅ অনেক ফিচার, অল্প গুরুত্বপূর্ণ
✅ Interpretability চান
✅ Noisy features আছে

ElasticNet:
✅ Best of both worlds
✅ গ্রুপড ফিচার + ফিচার সিলেকশন
""")
```

### সারসংক্ষেপ
Regularization overfitting কমায় এবং মডেল জেনারেলাইজেশন বাড়ায়। Ridge সব কোএফিসিয়েন্ট ছোট করে, Lasso স্পার্সিটি তৈরি করে (feature selection)। ফাইন্যান্সে নয়েজি ডেটার জন্য Regularization অপরিহার্য।