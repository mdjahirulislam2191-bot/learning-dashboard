# Day 06: লিনিয়ার রিগ্রেশন
## Linear Regression

### লিনিয়ার রিগ্রেশন কি?
লিনিয়ার রিগ্রেশন একটি supervised learning অ্যালগরিদম যা একটি নির্ভরশীল ভেরিয়েবল (y) এবং এক বা একাধিক স্বাধীন ভেরিয়েবল (X) এর মধ্যে সম্পর্ক মডেল করে।

**সমীকরণ:** y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε

### ফাইন্যান্স উদাহরণ: স্টক মূল্য পূর্বাভাস
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# স্টক ডেটা তৈরি
np.random.seed(42)
n = 200
days = np.arange(n).reshape(-1, 1)

# ট্রেন্ড + নয়েজ
stock_prices = 100 + days.squeeze() * 0.3 + np.random.randn(n) * 5

# ফিচার তৈরি: lagged features
df = pd.DataFrame({'day': days.squeeze(), 'price': stock_prices})
df['lag_1'] = df['price'].shift(1)
df['lag_2'] = df['price'].shift(2)
df['return_1d'] = df['price'].pct_change()
df = df.dropna()

X = df[['day', 'lag_1', 'lag_2']]
y = df['price']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# মডেল ট্রেইন
model = LinearRegression()
model.fit(X_train, y_train)

# কোএফিসিয়েন্টস
print("Intercept (β₀):", model.intercept_)
print("\nCoefficients:")
for feat, coef in zip(X.columns, model.coef_):
    print(f"  {feat}: {coef:.4f}")
```

### মডেল ইভালুয়েশন
```python
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n📊 Model Performance:")
print(f"MSE:  {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAE:  {mae:.2f}")
print(f"R²:   {r2:.4f}")

# Actual vs Predicted
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Actual vs Predicted')

plt.subplot(1, 2, 2)
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.title('Residual Plot')

plt.tight_layout()
plt.show()
```

### OLS (Ordinary Least Squares) পদ্ধতি
লিনিয়ার রিগ্রেশন OLS ব্যবহার করে যা RSS (Residual Sum of Squares) মিনিমাইজ করে:

```python
# ম্যানুয়াল OLS
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

X_with_const = sm.add_constant(X_train)
ols_model = OLS(y_train, X_with_const).fit()
print(ols_model.summary())
```

### ফাইন্যান্সে ব্যবহার: CAPM মডেল
```python
# CAPM: Ri = Rf + β(Rm - Rf)
# সিম্পল CAPM উদাহরণ
market_returns = np.random.randn(n) * 0.02
stock_returns = 0.001 + 1.2 * market_returns + np.random.randn(n) * 0.01

# β (Beta) গণনা
X_market = market_returns.reshape(-1, 1)
beta_model = LinearRegression().fit(X_market, stock_returns)
beta = beta_model.coef_[0]
alpha = beta_model.intercept_

print(f"\n📈 CAPM Analysis:")
print(f"Alpha (α): {alpha:.4f}")
print(f"Beta  (β): {beta:.4f}")
print(f"R²: {r2_score(stock_returns, beta_model.predict(X_market)):.4f}")

if beta > 1:
    print("→ Aggressive stock (high risk/high return)")
elif beta < 1:
    print("→ Defensive stock (low risk)")
else:
    print("→ Market-neutral")
```

### Linear Regression এর Assumptions
1. **Linearity** - X এবং y এর মধ্যে লিনিয়ার সম্পর্ক
2. **Independence** - observations independent
3. **Homoscedasticity** - constant variance of residuals
4. **Normality** - residuals normally distributed

### সারসংক্ষেপ
লিনিয়ার রিগ্রেশন সবচেয়ে বেসিক কিন্তু শক্তিশালী ML অ্যালগরিদম। ফাইন্যান্সে স্টক প্রেডিকশন, CAPM মডেল, এবং রিস্ক অ্যানালাইসিসে ব্যাপকভাবে ব্যবহৃত হয়।