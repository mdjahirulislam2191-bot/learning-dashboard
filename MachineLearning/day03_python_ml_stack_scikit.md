# Day 03: Python ML Stack এবং Scikit-learn পরিচিতি
## Python Machine Learning Stack & scikit-learn Introduction

### Python ML Stack এর মূল উপাদান
ফাইন্যান্স এবং ডেটা অ্যানালাইসিসের জন্য Python ML Stack:

1. **NumPy** - সংখ্যাসূচক গণনা
2. **Pandas** - ডেটা ম্যানিপুলেশন
3. **Matplotlib/Seaborn** - ভিজুয়ালাইজেশন
4. **Scikit-learn** - ML মডেল
5. **Statsmodels** - স্ট্যাটিস্টিকাল মডেলিং
6. **XGBoost/LightGBM** - উন্নত ML

### Scikit-learn এর মূল মডিউল
```python
# স্কিকিট-লার্ন ইম্পোর্ট
from sklearn import (
    preprocessing,     # ডেটা প্রিপ্রসেসিং
    model_selection,   # ট্রেইন/টেস্ট স্প্লিট
    linear_model,      # লিনিয়ার মডেল
    ensemble,          # এন্সেম্বল মেথড
    cluster,           # ক্লাস্টারিং
    metrics,           # ইভালুয়েশন মেট্রিক্স
    pipeline,          # পাইপলাইন
    decomposition,     # PCA, ইত্যাদি
    feature_selection  # ফিচার সিলেকশন
)

print("Scikit-learn মডিউল লোডেড!")
```

### ফাইন্যান্স ডেটাসেট লোড করা
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# সিন্থেটিক ফাইন্যান্সিয়াল ডেটা তৈরি
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365, freq='D')

finance_data = pd.DataFrame({
    'date': dates,
    'stock_price': 100 + np.cumsum(np.random.randn(365) * 0.5),
    'volume': np.random.randint(500000, 5000000, 365),
    'volatility': np.abs(np.random.randn(365)) * 0.3 + 0.2,
    'rsi': np.random.uniform(30, 70, 365),
    'sma_20': None,  # সিম্পল মুভিং এভারেজ
    'sma_50': None
})

# SMA গণনা
finance_data['sma_20'] = finance_data['stock_price'].rolling(20).mean()
finance_data['sma_50'] = finance_data['stock_price'].rolling(50).mean()

print("ফাইন্যান্স ডেটার প্রথম ৫ সারি:")
print(finance_data.head())
print(f"\nডেটার তথ্য:")
print(finance_data.info())
```

### Scikit-learn Estimator API
Scikit-learn-এ প্রতিটি ML মডেল একটি Estimator। সাধারণ API:

```python
# Estimator API প্যাটার্ন
from sklearn.linear_model import LinearRegression

# 1. মডেল তৈরি
model = LinearRegression()

# 2. ফিট (ট্রেইন)
# model.fit(X_train, y_train)

# 3. প্রেডিক্ট
# y_pred = model.predict(X_test)

# 4. স্কোর (ইভালুয়েট)
# score = model.score(X_test, y_test)

print("Estimator API প্রস্তুত!")
```

### সম্পূর্ণ উদাহরণ: স্টক মূল্য পূর্বাভাস
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# ফিচার তৈরি
finance_data['day'] = np.arange(len(finance_data))
finance_data['price_lag1'] = finance_data['stock_price'].shift(1)
finance_data['price_lag2'] = finance_data['stock_price'].shift(2)
finance_data['volume_lag1'] = finance_data['volume'].shift(1)
finance_data['return_1d'] = finance_data['stock_price'].pct_change()

# NaN ড্রপ
clean_data = finance_data.dropna()

# ফিচার এবং টার্গেট
features = ['day', 'price_lag1', 'price_lag2', 'volume', 'volume_lag1', 'volatility', 'rsi']
X = clean_data[features]
y = clean_data['stock_price']

# ট্রেইন/টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# স্কেলিং
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# মডেল ট্রেইন
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# প্রেডিকশন
y_pred = model.predict(X_test_scaled)

# ইভালুয়েশন
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.4f}")
print(f"ফিচার গুরুত্ব:")
for feat, coef in zip(features, model.coef_):
    print(f"  {feat}: {coef:.2f}")
```

### ভিজুয়ালাইজেশন
```python
# প্রেডিক্টেড vs Actual
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('প্রেডিক্টেড vs Actual স্টক মূল্য')
plt.tight_layout()
plt.show()
```

### সারসংক্ষেপ
Scikit-learn হল Python ML এর সবচেয়ে গুরুত্বপূর্ণ লাইব্রেরি। এর consistent API (fit/predict/score) সব মডেলের জন্য একই। আমরা ফাইন্যান্স ডেটার সাথে কাজ করার বেসিক সেটআপ শিখলাম।