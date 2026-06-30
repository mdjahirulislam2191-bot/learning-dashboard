# Day 32: ARIMA
## ARIMA (AutoRegressive Integrated Moving Average)

### ARIMA কি?
ARIMA একটি ক্লাসিক্যাল টাইম সিরিজ ফোরকাস্টিং মডেল যা তিনটি কম্পোনেন্ট নিয়ে গঠিত:
- **AR (AutoRegressive)**: পূর্ববর্তী মানের উপর বর্তমান মানের নির্ভরতা
- **I (Integrated)**: ডিফারেন্সিং করে ডেটা স্টেশনারি করা
- **MA (Moving Average)**: পূর্ববর্তী এরর টার্মের উপর নির্ভরতা

### ARIMA প্যারামিটার: (p, d, q)
- **p**: AR টার্ম সংখ্যা (ল্যাগ সংখ্যা)
- **d**: ডিফারেন্সিং অর্ডার
- **q**: MA টার্ম সংখ্যা (এরর ল্যাগ সংখ্যা)

### ফাইন্যান্স উদাহরণ: স্টক প্রাইস ফোরকাস্টিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# স্টক প্রাইস ডেটা তৈরি
np.random.seed(42)
n = 500
dates = pd.date_range('2022-01-01', periods=n, freq='D')

# ARIMA-সদৃশ ডেটা
errors = np.random.randn(n) * 2
price = np.zeros(n)
price[0] = 100

for t in range(1, n):
    # AR(1) + MA(1) প্রক্রিয়া
    price[t] = price[t-1] + 0.7 * (price[t-1] - price[t-2]) if t > 1 else price[t-1]
    price[t] += errors[t] - 0.3 * errors[t-1] if t > 1 else errors[t]
    price[t] += 0.05  # ড্রিফট

df = pd.DataFrame({'date': dates, 'price': price})
print(f"Dataset: {df.shape}")
print(df.head())
```

### 1. স্টেশনারিটি চেক
```python
# ADF Test
def adf_test(series, name='Series'):
    result = adfuller(series.dropna())
    print(f'📊 {name} ADF Test:')
    print(f'  ADF Statistic: {result[0]:.6f}')
    print(f'  p-value: {result[1]:.6f}')
    print(f'  Critical Values:')
    for key, value in result[4].items():
        print(f'    {key}: {value:.6f}')
    print(f'  → {"✅ Stationary" if result[1] <= 0.05 else "❌ Non-stationary"}\n')

adf_test(df['price'], 'Original Price')

# 1st Difference
df['price_diff'] = df['price'].diff()
adf_test(df['price_diff'].dropna(), 'First Difference')

# ভিজুয়ালাইজ
fig, axes = plt.subplots(2, 1, figsize=(15, 6))
df['price'].plot(ax=axes[0], title='Original Series')
df['price_diff'].plot(ax=axes[1], title='First Difference')
plt.tight_layout()
plt.show()
```

### 2. ACF এবং PACF প্লট (p, q নির্ধারণ)
```python
fig, axes = plt.subplots(2, 2, figsize=(15, 8))

# Original series
plot_acf(df['price'].dropna(), lags=30, ax=axes[0, 0])
axes[0, 0].set_title('ACF - Original Series')
plot_pacf(df['price'].dropna(), lags=30, ax=axes[0, 1])
axes[0, 1].set_title('PACF - Original Series')

# Differenced series
plot_acf(df['price_diff'].dropna(), lags=30, ax=axes[1, 0])
axes[1, 0].set_title('ACF - Differenced')
plot_pacf(df['price_diff'].dropna(), lags=30, ax=axes[1, 1])
axes[1, 1].set_title('PACF - Differenced')

plt.tight_layout()
plt.show()

# ACF/PACF থেকে p, q নির্ধারণ
print("📌 ACF/PACF Analysis:")
print("  PACF cut-off at lag 1 → p = 1 (AR term)")
print("  ACF cut-off at lag 1 → q = 1 (MA term)")
print("  One differencing needed → d = 1")
print("  Suggested: ARIMA(1,1,1)")
```

### 3. ARIMA মডেল ট্রেইনিং
```python
# ট্রেন/টেস্ট স্প্লিট
train_size = int(len(df) * 0.8)
train = df['price'].iloc[:train_size]
test = df['price'].iloc[train_size:]

print(f"Train: {len(train)} observations")
print(f"Test: {len(test)} observations")

# ARIMA(1,1,1) মডেল
model = ARIMA(train, order=(1, 1, 1))
results = model.fit()

print("\n📊 ARIMA Model Summary:")
print(results.summary().tables[1])

# রেসিডুয়াল চেক
residuals = results.resid
print(f"\nResidual stats:")
print(f"  Mean: {residuals.mean():.4f}")
print(f"  Std:  {residuals.std():.4f}")
adf_test(residuals, 'Residuals')
```

### 4. ফোরকাস্টিং
```python
# ফোরকাস্ট
forecast = results.forecast(steps=len(test))

# ইভালুয়েশন
rmse = np.sqrt(mean_squared_error(test, forecast))
mae = mean_absolute_error(test, forecast)
mape = np.mean(np.abs((test - forecast) / test)) * 100

print(f"\n📊 ARIMA(1,1,1) Forecast Performance:")
print(f"  RMSE: {rmse:.4f}")
print(f"  MAE:  {mae:.4f}")
print(f"  MAPE: {mape:.2f}%")

# ভিজুয়ালাইজেশন
plt.figure(figsize=(15, 6))
plt.plot(train.index, train, label='Train', linewidth=1)
plt.plot(test.index, test, label='Actual', linewidth=2)
plt.plot(test.index, forecast, label='ARIMA Forecast', linewidth=2, linestyle='--')
plt.title('ARIMA(1,1,1) - Stock Price Forecast')
plt.xlabel('Day')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 5. অটো ARIMA (সেরা প্যারামিটার অটো-ফাইন্ড)
```python
# অটো ARIMA
try:
    import pmdarima as pm
    
    auto_model = pm.auto_arima(train, start_p=0, max_p=5,
                               start_d=0, max_d=2,
                               start_q=0, max_q=5,
                               seasonal=False,
                               stepwise=True,
                               trace=True,
                               error_action='ignore',
                               suppress_warnings=True)
    
    print(f"\n✅ Auto-ARIMA best order: {auto_model.order}")
    print(f"   Best seasonal order: {auto_model.seasonal_order}")
    
    # অটো ARIMA ফোরকাস্ট
    auto_forecast = auto_model.predict(n_periods=len(test))
    
    auto_rmse = np.sqrt(mean_squared_error(test, auto_forecast))
    print(f"  Auto-ARIMA RMSE: {auto_rmse:.4f}")
    
except ImportError:
    print("pmdarima not installed. Install with: pip install pmdarima")
```

### 6. সারাবছিক ARIMA (SARIMA)
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# SARIMA(p,d,q)(P,D,Q)s - ঋতুভিত্তিক কম্পোনেন্ট সহ
sarima_model = SARIMAX(train, order=(1, 1, 1), 
                       seasonal_order=(1, 1, 1, 7),  # সাপ্তাহিক সিজনালিটি
                       enforce_stationarity=False,
                       enforce_invertibility=False)
sarima_results = sarima_model.fit(disp=False)

print("\n📊 SARIMA Model Summary:")
print(sarima_results.summary().tables[1])

sarima_forecast = sarima_results.forecast(steps=len(test))
sarima_rmse = np.sqrt(mean_squared_error(test, sarima_forecast))
print(f"\nSARIMA RMSE: {sarima_rmse:.4f}")

# সব মডেল তুলনা
plt.figure(figsize=(15, 6))
plt.plot(test.index, test, label='Actual', linewidth=2)
plt.plot(test.index, forecast, label='ARIMA(1,1,1)', linewidth=1.5, linestyle='--')
plt.plot(test.index, sarima_forecast, label='SARIMA', linewidth=1.5, linestyle=':')
plt.title('ARIMA vs SARIMA Forecast Comparison')
plt.xlabel('Day')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 7. ডায়াগনস্টিক চেক
```python
# রেসিডুয়াল অ্যানালাইসিস
fig, axes = plt.subplots(2, 2, figsize=(15, 8))

# Standardized residuals
residuals = results.resid
axes[0, 0].plot(residuals)
axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
axes[0, 0].set_title('Standardized Residuals')
axes[0, 0].grid(True, alpha=0.3)

# Histogram + KDE
axes[0, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Residual Distribution')
axes[0, 1].grid(True, alpha=0.3)

# Q-Q plot
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Q-Q Plot')

# ACF of residuals
plot_acf(residuals.dropna(), lags=30, ax=axes[1, 1])
axes[1, 1].set_title('ACF of Residuals')

plt.tight_layout()
plt.show()

# Ljung-Box Test for residual autocorrelation
from statsmodels.stats.diagnostic import acorr_ljungbox
lb_test = acorr_ljungbox(residuals, lags=[10, 20], return_df=True)
print("\n🔍 Ljung-Box Test:")
print(lb_test)
print("\n(If p-values > 0.05, residuals are white noise = good model)")
```

### ARIMA বেস্ট প্র্যাকটিস
```python
print("""
✅ ARIMA Best Practices:
1️⃣ Always check stationarity first (ADF test)
2️⃣ Use ACF/PACF plots to determine p, q
3️⃣ Check residual diagnostics
4️⃣ Compare multiple ARIMA orders
5️⃣ Consider SARIMA for seasonal data
6️⃣ Use auto_arima for automatic selection
7️⃣ Validate with out-of-sample testing

📊 Model Selection Criteria:
- AIC (Akaike Information Criterion): Lower is better
- BIC (Bayesian Information Criterion): Lower is better
- Residual diagnostics: White noise residuals
- Forecast accuracy: RMSE, MAE, MAPE
""")
```

### সারসংক্ষেপ
আজ আমরা ARIMA মডেল শিখলাম:
- **ARIMA(p,d,q)**: AR + Integration + MA
- **ACF/PACF**: প্যারামিটার নির্ধারণ
- **স্টেশনারিটি**: ADF Test, Differencing
- **SARIMA**: Seasonal ARIMA
- **অটো ARIMA**: অটোমেটিক প্যারামিটার সিলেকশন
- **ডায়াগনস্টিকস**: Residual Analysis, Ljung-Box Test

### অনুশীলনী
1. ARIMA(2,1,2) মডেল তৈরি করে ARIMA(1,1,1)-এর সাথে তুলনা করুন
2. রিয়েল স্টক ডেটা (yfinance) ব্যবহার করে ARIMA ফোরকাস্টিং করুন
3. বিভিন্ন p, d, q ভ্যালু নিয়ে Grid Search করুন (AIC মিনিমাইজ)
4. ARIMA এবং মেশিন লার্নিং মডেল (RF, XGBoost) এর পারফরম্যান্স তুলনা করুন