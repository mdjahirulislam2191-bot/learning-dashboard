# Day 16: লিনিয়ার রিগ্রেশন
## Linear Regression

### লিনিয়ার রিগ্রেশন কী?
লিনিয়ার রিগ্রেশন একটি পরিসংখ্যানিক মডেল যা একটি ডিপেন্ডেন্ট ভ্যারিয়েবল (y) এবং এক বা একাধিক ইন্ডিপেন্ডেন্ট ভ্যারিয়েবল (x) এর মধ্যে লিনিয়ার সম্পর্ক খুঁজে বের করে। এটি ডেটা সায়েন্সের সবচেয়ে মৌলিক ও শক্তিশালী টুল।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# স্যাম্পল ডেটা তৈরি: বাড়ির আকার ও দাম
np.random.seed(42)
n = 200
house_size = np.random.uniform(500, 4000, n)  # স্কয়ার ফিটে আকার
house_price = 50000 + 150 * house_size + np.random.normal(0, 50000, n)  # দাম

df = pd.DataFrame({
    'আকার_স্কয়ার_ফুট': house_size,
    'দাম': house_price
})

print("=== ডেটাসেট ===")
print(df.head())
print(f"\nপরিসংখ্যান:")
print(df.describe())
```

### সিম্পল লিনিয়ার রিগ্রেশন (একটি ফিচার):
```python
print("\n=== সিম্পল লিনিয়ার রিগ্রেশন ===")

X = df[['আকার_স্কয়ার_ফুট']]
y = df['দাম']

# মডেল তৈরি ও ট্রেনিং
model = LinearRegression()
model.fit(X, y)

# কোফিসিয়েন্ট ও ইন্টারসেপ্ট
print(f"ইন্টারসেপ্ট (β₀): {model.intercept_:.2f}")
print(f"কোফিসিয়েন্ট (β₁): {model.coef_[0]:.4f}")
print(f"\nসমানীকরণ: দাম = {model.intercept_:.2f} + {model.coef_[0]:.2f} × আকার")

# প্রেডিকশন
y_pred = model.predict(X)
print(f"\nপ্রথম ৫ প্রেডিকশন:")
predictions = pd.DataFrame({
    'আকার': X.values.flatten()[:5],
    'প্রকৃত_দাম': y.values[:5],
    'প্রেডিক্টেড_দাম': y_pred[:5],
    'পার্থক্য': y.values[:5] - y_pred[:5]
})
print(predictions.round(2))
```

### মডেল ইভালুয়েশন:
```python
print("\n=== মডেল ইভালুয়েশন ===")

# R² Score
r2 = r2_score(y, y_pred)
print(f"R² Score: {r2:.4f}")
print(f"(মডেল ডেটার {r2*100:.2f}% ভ্যারিয়েন্স ব্যাখ্যা করতে পারে)")

# MSE
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"(গড়ে মডেলের প্রেডিকশন {rmse:.2f} টাকা ভুল)")

# MAE
mae = mean_absolute_error(y, y_pred)
print(f"MAE: {mae:.2f}")

# MAPE
mape = np.mean(np.abs((y - y_pred) / y)) * 100
print(f"MAPE: {mape:.2f}%")
```

### ভিজুয়ালাইজেশন:
```python
print("\n=== ভিজুয়ালাইজেশন ===")

plt.figure(figsize=(15, 5))

# ১. ডেটা পয়েন্ট ও রিগ্রেশন লাইন
plt.subplot(1, 3, 1)
plt.scatter(X, y, alpha=0.5, label='ডেটা')
plt.plot(X, y_pred, color='red', linewidth=2, label='রিগ্রেশন লাইন')
plt.xlabel('আকার (স্কয়ার ফুট)')
plt.ylabel('দাম (টাকা)')
plt.title('লিনিয়ার রিগ্রেশন: আকার vs দাম')
plt.legend()

# ২. রেসিডুয়াল প্লট
plt.subplot(1, 3, 2)
residuals = y - y_pred
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('প্রেডিক্টেড দাম')
plt.ylabel('রেসিডুয়াল')
plt.title('রেসিডুয়াল প্লট')

# ৩. রেসিডুয়াল হিস্টোগ্রাম
plt.subplot(1, 3, 3)
plt.hist(residuals, bins=20, edgecolor='black', alpha=0.7)
plt.axvline(x=0, color='red', linestyle='--')
plt.xlabel('রেসিডুয়াল')
plt.ylabel('ফ্রিকোয়েন্সি')
plt.title('রেসিডুয়াল ডিস্ট্রিবিউশন')

plt.tight_layout()
plt.savefig('linear_regression.png')
plt.show()
print("গ্রাফ সেভ করা হয়েছে!")
```

### OLS (Ordinary Least Squares) - ম্যানুয়ালি:
```python
print("\n=== OLS ম্যানুয়ালি ===")

# OLS ফর্মুলা: β = (XᵀX)⁻¹Xᵀy
X_b = np.c_[np.ones((n, 1)), X]  # ইন্টারসেপ্টের জন্য ১ যোগ
theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y.values

print(f"ইন্টারসেপ্ট (ম্যানুয়াল): {theta[0]:.2f}")
print(f"কোফিসিয়েন্ট (ম্যানুয়াল): {theta[1]:.4f}")

# ম্যানুয়াল প্রেডিকশন
y_pred_manual = X_b @ theta
print(f"\nম্যানুয়াল আর স্কোয়ার: {r2_score(y, y_pred_manual):.4f}")
print(f"স্কলার্ন আর স্কোয়ার: {r2_score(y, y_pred):.4f}")
```

### স্ট্যাটিস্টিকাল ইনফারেন্স:
```python
print("\n=== স্ট্যাটিস্টিকাল ইনফারেন্স ===")

# স্ট্যাটসমডেল ব্যবহার করে বিস্তারিত রেজাল্ট
import statsmodels.api as sm

X_sm = sm.add_constant(X)
sm_model = sm.OLS(y, X_sm).fit()
print(sm_model.summary().tables[1])

# কনফিডেন্স ইন্টারভ্যাল
ci = sm_model.conf_int()
print(f"\nকোফিসিয়েন্টের ৯৫% কনফিডেন্স ইন্টারভ্যাল:")
print(f"ইন্টারসেপ্ট: ({ci[0][0]:.2f}, {ci[0][1]:.2f})")
print(f"আকার: ({ci[1][0]:.4f}, {ci[1][1]:.4f})")

# p-ভ্যালু
print(f"\np-ভ্যালু (ইন্টারসেপ্ট): {sm_model.pvalues[0]:.6f}")
print(f"p-ভ্যালু (আকার): {sm_model.pvalues[1]:.6f}")
```

### অ্যাসাম্পশন চেকিং:
```python
print("\n=== লিনিয়ার রিগ্রেশন অ্যাসাম্পশন চেক ===")

# ১. লিনিয়ারিটি
print("১. লিনিয়ারিটি: ডেটা বনাম প্রেডিক্টেড প্লট দেখুন")

# ২. ইন্ডিপেন্ডেন্স অব রেসিডুয়াল (Durbin-Watson)
dw = sm_model.durbin_watson
print(f"২. Durbin-Watson: {dw:.4f} (২ এর কাছাকাছি হলে ভালো)")

# ৩. হোমোসকেডাস্টিসিটি (Breusch-Pagan test)
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residuals, X_sm)
print(f"৩. Breusch-Pagan p-ভ্যালু: {bp_test[1]:.4f} (p>0.05 হলে হোমোসকেডাস্টিক)")

# ৪. নরমালিটি অব রেসিডুয়াল (Jarque-Bera test)
jb_test = stats.jarque_bera(residuals)
print(f"৪. Jarque-Bera p-ভ্যালু: {jb_test[1]:.4f} (p>0.05 হলে নরমাল)")

# ৫. নো মাল্টিকোলিনিয়ারিটি (VIF) - মাল্টিপল রিগ্রেশনে ব্যবহার হবে
```

### নন-লিনিয়ার রিলেশনশিপ:
```python
print("\n=== নন-লিনিয়ার রিলেশনশিপ ===")

# নন-লিনিয়ার ডেটা
np.random.seed(42)
x_nonlin = np.linspace(0, 10, 100)
y_nonlin = 2 + 3 * x_nonlin - 0.5 * x_nonlin**2 + np.random.normal(0, 2, 100)

# পলিনমিয়াল ফিচার
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(x_nonlin.reshape(-1, 1))

poly_model = LinearRegression()
poly_model.fit(X_poly, y_nonlin)
y_poly_pred = poly_model.predict(X_poly)

print(f"পলিনমিয়াল রিগ্রেশন R²: {r2_score(y_nonlin, y_poly_pred):.4f}")
print(f"লিনিয়ার রিগ্রেশন R² (সাদৃশ্যের জন্য): {r2_score(y_nonlin, 2+3*x_nonlin):.4f}")

plt.figure(figsize=(8, 5))
plt.scatter(x_nonlin, y_nonlin, alpha=0.5, label='ডেটা')
plt.plot(x_nonlin, y_poly_pred, 'r-', linewidth=2, label='পলিনমিয়াল ফিট (degree=2)')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('পলিনমিয়াল রিগ্রেশন')
plt.legend()
plt.savefig('polynomial_regression.png')
plt.show()
print("পলিনমিয়াল রিগ্রেশন গ্রাফ সেভ করা হয়েছে!")
```

### প্রেডিকশন:
```python
print("\n=== প্রেডিকশন ===")

# নতুন ডেটার জন্য প্রেডিকশন
new_houses = pd.DataFrame({'আকার_স্কয়ার_ফুট': [1000, 1500, 2000, 2500, 3000]})
predicted_prices = model.predict(new_houses)

predictions = pd.DataFrame({
    'আকার': new_houses.values.flatten(),
    'প্রেডিক্টেড_দাম': predicted_prices
})
print("নতুন বাড়ির দাম পূর্বাভাস:")
print(predictions.round(2))

# ইন্টারপ্রিটেশন
print(f"\nইন্টারপ্রিটেশন:")
print(f"বাড়ির আকার প্রতি ১ স্কয়ার ফুট বাড়লে দাম গড়ে {model.coef_[0]:.2f} টাকা বাড়ে।")
print(f"আকার ০ হলে বেস দাম {model.intercept_:.2f} টাকা (প্লটের দাম)।")

# ফিচার ইম্পরট্যান্স
print(f"\nফিচার ইম্পরট্যান্স:")
print(f"আকার → দাম: {model.coef_[0]:.2f} টাকা/স্কয়ার ফুট")
```

### হাউস প্রাইস প্রেডিকশন - সম্পূর্ণ ওয়ার্কফ্লো:
```python
print("\n=== সম্পূর্ণ ওয়ার্কফ্লো ===")

# ট্রেন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# মডেল ট্রেন
model_final = LinearRegression()
model_final.fit(X_train, y_train)

# প্রেডিকশন
y_train_pred = model_final.predict(X_train)
y_test_pred = model_final.predict(X_test)

print(f"ট্রেন সেট পারফরম্যান্স:")
print(f"  R² = {r2_score(y_train, y_train_pred):.4f}")
print(f"  RMSE = {np.sqrt(mean_squared_error(y_train, y_train_pred)):.2f}")

print(f"\nটেস্ট সেট পারফরম্যান্স:")
print(f"  R² = {r2_score(y_test, y_test_pred):.4f}")
print(f"  RMSE = {np.sqrt(mean_squared_error(y_test, y_test_pred)):.2f}")

# ওভারফিটিং চেক
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
print(f"\nওভারফিটিং চেক:")
print(f"  ট্রেন R² - টেস্ট R² = {train_r2 - test_r2:.4f}")
if train_r2 - test_r2 < 0.1:
    print("  সাধারণ পার্থক্য — মডেল ভালো জেনারেলাইজ করছে ✅")
else:
    print("  বড় পার্থক্য — ওভারফিটিং হতে পারে ⚠️")
```

### সারাংশ:
- **লিনিয়ার রিগ্রেশন**: y = β₀ + β₁x + ε ফর্মের মডেল
- **R² Score**: মডেল ডেটার কত শতাংশ ভ্যারিয়েন্স ব্যাখ্যা করতে পারে
- **RMSE**: প্রেডিকশনের গড় ত্রুটি (আসল ইউনিটে)
- **কোফিসিয়েন্ট**: ফিচারের প্রতি ইউনিট পরিবর্তনে টার্গেটের পরিবর্তনের পরিমাণ
- **অ্যাসাম্পশন**: লিনিয়ারিটি, ইন্ডিপেন্ডেন্স, হোমোসকেডাস্টিসিটি, নরমালিটি
- ভালো মডেলের ট্রেন ও টেস্ট R² এর মধ্যে বড় গ্যাপ থাকা উচিত নয়