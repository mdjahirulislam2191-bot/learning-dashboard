# Day 25: টাইম সিরিজ অ্যানালাইসিস (Time Series Analysis)
## Time Series Analysis: Forecasting & Trends

### টাইম সিরিজ কী?
টাইম সিরিজ হলো সময়ের সাথে সংগ্রহ করা ডেটা পয়েন্টের সিরিজ। স্টক মার্কেট, আবহাওয়া, বিক্রয়, ওয়েব ট্রাফিক等领域 টাইম সিরিজ অ্যানালাইসিস অত্যন্ত গুরুত্বপূর্ণ।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf, kpss
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
```

### টাইম সিরিজ ডেটা তৈরি
```python
print("=" * 60)
print("টাইম সিরিজ ডেটা তৈরি")
print("=" * 60)

np.random.seed(42)

# ডেইলি টাইম সিরিজ (২ বছর)
date_rng = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
n = len(date_rng)

# বিভিন্ন কম্পোনেন্ট
trend = np.linspace(20, 30, n)  # আপট্রেন্ড
seasonal = 5 * np.sin(2 * np.pi * np.arange(n) / 365) + 2 * np.sin(2 * np.pi * np.arange(n) / 30)  # বার্ষিক + মাসিক
noise = np.random.normal(0, 1.5, n)  # র‍্যান্ডম নয়েজ

# কম্পাউন্ড সিরিজ
values = trend + seasonal + noise
values = np.maximum(values, 5)  # নেগেটিভ ভ্যালু এড়ানো

df = pd.DataFrame({
    'date': date_rng,
    'value': values,
    'trend': trend,
    'seasonal_component': seasonal,
    'noise': noise
})
df.set_index('date', inplace=True)

print(f"ডেটা রেঞ্জ: {df.index.min()} থেকে {df.index.max()}")
print(f"মোট পয়েন্ট: {len(df)}")
print("\nপ্রথম ৫টি রেকর্ড:")
print(df.head())
```

### টাইম সিরিজ ভিজুয়ালাইজেশন
```python
print("\n=== টাইম সিরিজ ভিজুয়ালাইজেশন ===")

fig, axes = plt.subplots(4, 1, figsize=(14, 12))

# পুরো সিরিজ
axes[0].plot(df.index, df['value'], color='steelblue', linewidth=0.8)
axes[0].set_title('টাইম সিরিজ (আসল ডেটা)', fontsize=12)
axes[0].set_ylabel('ভ্যালু')
axes[0].grid(True, alpha=0.3)

# ট্রেন্ড
axes[1].plot(df.index, df['trend'], color='green', linewidth=1.5)
axes[1].set_title('ট্রেন্ড কম্পোনেন্ট', fontsize=12)
axes[1].set_ylabel('ট্রেন্ড')
axes[1].grid(True, alpha=0.3)

# সিজনালিটি
axes[2].plot(df.index, df['seasonal_component'], color='orange', linewidth=0.8)
axes[2].set_title('সিজনাল কম্পোনেন্ট', fontsize=12)
axes[2].set_ylabel('সিজনালিটি')
axes[2].grid(True, alpha=0.3)

# নয়েজ
axes[3].plot(df.index, df['noise'], color='red', linewidth=0.5, alpha=0.7)
axes[3].set_title('নয়েজ (রেসিডুয়াল)', fontsize=12)
axes[3].set_ylabel('নয়েজ')
axes[3].set_xlabel('তারিখ')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ts_components.png', dpi=100)
plt.show()
```

### স্ট্যাটিস্টিক্যাল ডিকম্পোজিশন
```python
print("\n=== স্ট্যাটিস্টিক্যাল ডিকম্পোজিশন ===")

# অ্যাডিটিভ ডিকম্পোজিশন
decomposition = seasonal_decompose(df['value'], model='additive', period=365)

fig, axes = plt.subplots(4, 1, figsize=(14, 10))

decomposition.observed.plot(ax=axes[0], color='steelblue')
axes[0].set_title('অরিজিনাল সিরিজ', fontsize=12)
axes[0].grid(True, alpha=0.3)

decomposition.trend.plot(ax=axes[1], color='green')
axes[1].set_title('ট্রেন্ড (statsmodels ডিকম্পোজ)', fontsize=12)
axes[1].grid(True, alpha=0.3)

decomposition.seasonal.plot(ax=axes[2], color='orange')
axes[2].set_title('সিজনাল', fontsize=12)
axes[2].grid(True, alpha=0.3)

decomposition.resid.plot(ax=axes[3], color='red')
axes[3].set_title('রেসিডুয়াল', fontsize=12)
axes[3].set_xlabel('তারিখ')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ts_decomposition.png', dpi=100)
plt.show()

print("ডিকম্পোজিশন কম্পোনেন্ট সমষ্টি = অরিজিনাল সিরিজ")
print(f"ট্রেন্ড + সিজনাল + রেসিডুয়াল ≈ অরিজিনাল ভ্যালু")
```

### স্টেশনারিটি টেস্ট (ADF Test)
```python
print("\n=== স্টেশনারিটি টেস্ট ===")

def check_stationarity(series, title=''):
    print(f"\n--- {title} ---")
    
    # Augmented Dickey-Fuller Test
    result = adfuller(series.dropna(), autolag='AIC')
    print(f'ADF স্ট্যাটিস্টিক: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    print(f'ক্রিটিক্যাল ভ্যালু:')
    for key, value in result[4].items():
        print(f'  {key}: {value:.4f}')
    
    if result[1] <= 0.05:
        print('✅ ফলাফল: ডেটা স্টেশনারি (p <= 0.05)')
        return True
    else:
        print('❌ ফলাফল: ডেটা নন-স্টেশনারি (p > 0.05)')
        return False

stationary = check_stationarity(df['value'], 'আসল সিরিজ')

# প্রথম ডিফারেন্স
df['value_diff1'] = df['value'].diff()
stationary_diff1 = check_stationarity(df['value_diff1'], 'প্রথম ডিফারেন্স')

# দ্বিতীয় ডিফারেন্স (প্রয়োজন হলে)
if not stationary_diff1:
    df['value_diff2'] = df['value'].diff().diff()
    check_stationarity(df['value_diff2'], 'দ্বিতীয় ডিফারেন্স')

print("\nস্টেশনারি হতে সাধারণত ১ বার ডিফারেন্সই যথেষ্ট (d=1)")
```

### ACF ও PACF প্লট
```python
print("\n=== ACF ও PACF প্লট ===")

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# আসল সিরিজের ACF/PACF
plot_acf(df['value'].dropna(), lags=40, ax=axes[0, 0])
axes[0, 0].set_title('ACF - আসল সিরিজ', fontsize=12)

plot_pacf(df['value'].dropna(), lags=40, ax=axes[0, 1], method='ywm')
axes[0, 1].set_title('PACF - আসল সিরিজ', fontsize=12)

# ডিফারেন্সড সিরিজের ACF/PACF
plot_acf(df['value_diff1'].dropna(), lags=40, ax=axes[1, 0])
axes[1, 0].set_title('ACF - প্রথম ডিফারেন্স', fontsize=12)

plot_pacf(df['value_diff1'].dropna(), lags=40, ax=axes[1, 1], method='ywm')
axes[1, 1].set_title('PACF - প্রথম ডিফারেন্স', fontsize=12)

plt.tight_layout()
plt.savefig('acf_pacf.png', dpi=100)
plt.show()

print("ACF: MA (q) অর্ডার নির্ধারণে সাহায্য করে")
print("PACF: AR (p) অর্ডার নির্ধারণে সাহায্য করে")
print("সাধারণত ACF কাট অফ = q, PACF কাট অফ = p")
```

### ARIMA মডেল
```python
print("\n=== ARIMA মডেল ===")

# ট্রেন-টেস্ট স্প্লিট (শেষ 90 দিন টেস্ট)
train_size = len(df) - 90
train, test = df['value'][:train_size], df['value'][train_size:]

print(f"ট্রেনিং ডেটা: {train.index[0].date()} থেকে {train.index[-1].date()} ({len(train)} পয়েন্ট)")
print(f"টেস্ট ডেটা: {test.index[0].date()} থেকে {test.index[-1].date()} ({len(test)} পয়েন্ট)")

# ARIMA মডেল (p=5, d=1, q=0)
model_arima = ARIMA(train, order=(5, 1, 0))
fitted_arima = model_arima.fit()

print(f"\nARIMA মডেল সারাংশ:")
print(f"AIC: {fitted_arima.aic:.2f}")
print(f"BIC: {fitted_arima.bic:.2f}")
print(f"\nARIMA প্যারামিটার:")
print(fitted_arima.params.to_string())

# ফোরকাস্ট
forecast_arima = fitted_arima.forecast(steps=len(test))
forecast_index = test.index

# মেট্রিক্স
mae_arima = mean_absolute_error(test, forecast_arima)
rmse_arima = np.sqrt(mean_squared_error(test, forecast_arima))
mape_arima = np.mean(np.abs((test - forecast_arima) / test)) * 100

print(f"\nফোরকাস্ট মেট্রিক্স (ARIMA):")
print(f"MAE: {mae_arima:.3f}")
print(f"RMSE: {rmse_arima:.3f}")
print(f"MAPE: {mape_arima:.2f}%")
```

### Holt-Winters (Exponential Smoothing)
```python
print("\n=== Holt-Winters এক্সপোনেনশিয়াল স্মুথিং ===")

# Holt-Winters মডেল (সিজনালিটি সহ)
model_hw = ExponentialSmoothing(
    train, 
    trend='add',
    seasonal='add',
    seasonal_periods=365
)
fitted_hw = model_hw.fit()

print(f"Holt-Winters মডেল:")
print(f"AIC: {fitted_hw.aic:.2f}")
print(f"BIC: {fitted_hw.bic:.2f}")
print(f"\nস্মুথিং প্যারামিটার:")
print(f"  আলফা (লেভেল): {fitted_hw.params['smoothing_level']:.4f}")
print(f"  বেটা (ট্রেন্ড): {fitted_hw.params['smoothing_trend']:.4f}")
print(f"  গামা (সিজনাল): {fitted_hw.params['smoothing_seasonal']:.4f}")

# ফোরকাস্ট
forecast_hw = fitted_hw.forecast(len(test))

# মেট্রিক্স
mae_hw = mean_absolute_error(test, forecast_hw)
rmse_hw = np.sqrt(mean_squared_error(test, forecast_hw))
mape_hw = np.mean(np.abs((test - forecast_hw) / test)) * 100

print(f"\nফোরকাস্ট মেট্রিক্স (Holt-Winters):")
print(f"MAE: {mae_hw:.3f}")
print(f"RMSE: {rmse_hw:.3f}")
print(f"MAPE: {mape_hw:.2f}%")
```

### ফোরকাস্ট তুলনা
```python
print("\n=== ফোরকাস্ট তুলনা ===")

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# সম্পূর্ণ সিরিজ + ফোরকাস্ট
axes[0].plot(train.index, train, label='ট্রেনিং ডেটা', color='steelblue', alpha=0.7)
axes[0].plot(test.index, test, label='আসল (টেস্ট)', color='green', linewidth=2)
axes[0].plot(forecast_index, forecast_arima, label='ARIMA ফোরকাস্ট', color='red', linestyle='--', linewidth=2)
axes[0].plot(forecast_index, forecast_hw, label='Holt-Winters ফোরকাস্ট', color='orange', linestyle='--', linewidth=2)
axes[0].set_title('টাইম সিরিজ ফোরকাস্টিং: ARIMA vs Holt-Winters', fontsize=14)
axes[0].set_ylabel('ভ্যালু')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].axvline(x=train.index[-1], color='black', linestyle=':', alpha=0.5, label='ট্রেন/টেস্ট বিভাজন')

# জুম ইন (শেষ 180 দিন)
axes[1].plot(train.index[-90:], train[-90:], label='ট্রেনিং (শেষাংশ)', color='steelblue', alpha=0.7)
axes[1].plot(test.index, test, label='আসল (টেস্ট)', color='green', linewidth=2)
axes[1].plot(forecast_index, forecast_arima, label='ARIMA', color='red', linestyle='--', linewidth=2)
axes[1].plot(forecast_index, forecast_hw, label='Holt-Winters', color='orange', linestyle='--', linewidth=2)
axes[1].set_title('জুম ইন: শেষ 180 দিন', fontsize=12)
axes[1].set_ylabel('ভ্যালু')
axes[1].set_xlabel('তারিখ')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ts_forecast_comparison.png', dpi=100)
plt.show()

print("\n=== মডেল তুলনা ===")
comparison = pd.DataFrame({
    'ARIMA': [mae_arima, rmse_arima, mape_arima],
    'Holt-Winters': [mae_hw, rmse_hw, mape_hw]
}, index=['MAE', 'RMSE', 'MAPE (%)'])
print(comparison.round(3))

best_model = 'ARIMA' if mape_arima < mape_hw else 'Holt-Winters'
print(f"\n🏆 সেরা মডেল: {best_model} (সবচেয়ে কম MAPE)")
```

### প্র্যাকটিক্যাল: দৈনিক বিক্রয় ফোরকাস্টিং
```python
print("\n=== প্র্যাকটিক্যাল উদাহরণ: দৈনিক বিক্রয় ফোরকাস্টিং ===")

np.random.seed(123)

# বিক্রয় ডেটা তৈরি
sales_dates = pd.date_range(start='2023-01-01', end='2024-06-30', freq='D')
n_sales = len(sales_dates)

# সাপ্তাহিক প্যাটার্ন (সপ্তাহান্তে বেশি বিক্রয়)
day_of_week = sales_dates.dayofweek
weekly_pattern = np.where(day_of_week >= 5, 1.3, 1.0)  # শনি-রবি 30% বেশি

# মাসিক সিজনালিটি (বছরের শেষে বেশি)
monthly_factor = 1 + 0.2 * np.sin(2 * np.pi * sales_dates.month / 12)

# ট্রেন্ড (ক্রমবর্ধমান)
trend_factor = 1 + 0.0003 * np.arange(n_sales)

# বেস সেলস
base_sales = 200
sales = base_sales * weekly_pattern * monthly_factor * trend_factor + np.random.normal(0, 15, n_sales)
sales = np.maximum(sales, 50)

sales_df = pd.DataFrame({'date': sales_dates, 'sales': sales})
sales_df.set_index('date', inplace=True)

print("দৈনিক বিক্রয় ডেটা (প্রথম ১০ দিন):")
print(sales_df.head(10))

# সাপ্তাহিক এগ্রিগেশন
weekly_sales = sales_df['sales'].resample('W').sum()
print(f"\nসাপ্তাহিক বিক্রয় (প্রথম ৪ সপ্তাহ):")
print(weekly_sales.head(4))

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

axes[0].plot(sales_df.index, sales_df['sales'], color='steelblue', alpha=0.7, linewidth=0.5)
axes[0].set_title('দৈনিক বিক্রয় (র ও ডেটা)', fontsize=12)
axes[0].set_ylabel('বিক্রয় (ইউনিট)')
axes[0].grid(True, alpha=0.3)

# 30-দিন মুভিং এভারেজ
sales_df['MA30'] = sales_df['sales'].rolling(window=30).mean()
axes[1].plot(sales_df.index, sales_df['sales'], color='gray', alpha=0.3, linewidth=0.5, label='দৈনিক')
axes[1].plot(sales_df.index, sales_df['MA30'], color='red', linewidth=2, label='30-দিন মুভিং এভারেজ')
axes[1].set_title('দৈনিক বিক্রয় + 30-দিন মুভিং এভারেজ', fontsize=12)
axes[1].set_ylabel('বিক্রয় (ইউনিট)')
axes[1].set_xlabel('তারিখ')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('sales_ts.png', dpi=100)
plt.show()
```

### লিনিয়ার রিগ্রেশন দিয়ে ট্রেন্ড ফোরকাস্টিং
```python
print("\n=== লিনিয়ার রিগ্রেশন দিয়ে ট্রেন্ড ফোরকাস্টিং ===")

# ফিচার তৈরি
sales_df['day_num'] = np.arange(len(sales_df))
sales_df['month'] = sales_df.index.month
sales_df['quarter'] = sales_df.index.quarter
sales_df['dayofweek'] = sales_df.index.dayofweek
sales_df['is_weekend'] = (sales_df['dayofweek'] >= 5).astype(int)

# ভবিষ্যতের জন্য ফিচার
future_dates = pd.date_range(start='2024-07-01', end='2024-12-31', freq='D')
future_df = pd.DataFrame(index=future_dates)
future_df['day_num'] = np.arange(len(sales_df), len(sales_df) + len(future_dates))
future_df['month'] = future_df.index.month
future_df['quarter'] = future_df.index.quarter
future_df['dayofweek'] = future_df.index.dayofweek
future_df['is_weekend'] = (future_df['dayofweek'] >= 5).astype(int)

# মডেল ট্রেনিং
features = ['day_num', 'month', 'is_weekend']
X_train = sales_df[features]
y_train = sales_df['sales']

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# ফোরকাস্ট
X_future = future_df[features]
future_df['sales_forecast'] = lr_model.predict(X_future)

print("ভবিষ্যত বিক্রয় ফোরকাস্ট (২০২৪ সালের শেষার্ধ):")
print(future_df.head())

# ভিজুয়ালাইজেশন
plt.figure(figsize=(14, 6))
plt.plot(sales_df.index[-180:], sales_df['sales'][-180:], 
         label='ঐতিহাসিক বিক্রয়', color='steelblue')
plt.plot(future_df.index, future_df['sales_forecast'], 
         label='লিনিয়ার রিগ্রেশন ফোরকাস্ট', color='red', linestyle='--', linewidth=2)
plt.title('লিনিয়ার রিগ্রেশন দিয়ে বিক্রয় ফোরকাস্টিং', fontsize=14)
plt.xlabel('তারিখ')
plt.ylabel('বিক্রয় (ইউনিট)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('lr_forecast.png', dpi=100)
plt.show()
```

### টাইম সিরিজ টিপস ও বেস্ট প্র্যাকটিস
```python
print("\n=== টাইম সিরিজ টিপস ও বেস্ট প্র্যাকটিস ===")

tips = """
## টাইম সিরিজ অ্যানালাইসিসের গুরুত্বপূর্ণ টিপস

### ডেটা প্রিপারেশন:
• মিসিং ডেটা হ্যান্ডেল করুন (ফরওয়ার্ড ফিল, ইন্টারপোলেশন)
• রেগুলার টাইম ইন্টারভাল নিশ্চিত করুন
• আউটলায়ার সনাক্ত করুন (Z-score, IQR)
• স্টেশনারিটি চেক করুন (ADF/KPSS test)
• নন-স্টেশনারি ডেটা ডিফারেন্স করুন

### মডেল সিলেকশন:
• ARIMA: স্টেশনারি ডেটার জন্য
• SARIMA: সিজনাল ডেটার জন্য
• Holt-Winters: স্পষ্ট সিজনালিটি থাকলে
• Prophet (Meta): ছুটির দিন, ইভেন্ট ইফেক্ট সহ
• LSTM/GRU: বড় ডেটাসেট, জটিল প্যাটার্নের জন্য

### ইভালুয়েশন:
• কখনো টেস্ট ডেটায় ফিট করবেন না
• ওয়াক-ফরওয়ার্ড ভ্যালিডেশন ব্যবহার করুন
• MAPE/RMSE/MAE সবগুলো দেখুন
• রেসিডুয়াল চেক করুন (সাদা শব্দ হতে হবে)
• বেঞ্চমার্ক (naive forecast) এর সাথে তুলনা করুন

### সাধারণ ভুল:
• ভুল train/test split (টাইম সিরিজে শাফল করবেন না!)
• ফিউচার ডেটা লিকেজ
• পর্যাপ্ত সিজনালিটি ক্যাপচার না করা
• মডেল ওভারফিটিং (বেশি প্যারামিটার)
• স্টেশনারিটি চেক না করে ARIMA ব্যবহার
"""
print(tips)
```

### সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("টাইম সিরিজ অ্যানালাইসিস - সারসংক্ষেপ")
print("=" * 60)

summary = """
## টাইম সিরিজ মূল পয়েন্ট

✅ টাইম সিরিজ = সময় অনুসারে ডেটা পয়েন্টের ক্রম
✅ ট্রেন্ড, সিজনালিটি, সাইক্লিক্যাল, নয়েজ — প্রধান কম্পোনেন্ট
✅ স্টেশনারিটি টেস্ট (ADF) ARIMA ব্যবহারের পূর্বশর্ত
✅ ACF & PACF প্লট p ও q অর্ডার নির্ধারণে সাহায্য করে
✅ ARIMA নন-সিজনাল, Holt-Winters সিজনাল ডেটার জন্য ভালো
✅ কখনো টাইম সিরিজ ডেটা শাফল করবেন না
✅ রোলিং ফোরকাস্ট ও ওয়াক-ফরওয়ার্ড ভ্যালিডেশন গুরুত্বপূর্ণ

## ডেটা অ্যানালিস্টের জন্য ব্যবহার
📊 বিক্রয় ফোরকাস্টিং (ইনভেন্টরি প্ল্যানিং)
📊 ফিন্যান্সিয়াল অ্যানালাইসিস (স্টক, বাজেট)
📊 ওয়েব ট্রাফিক অ্যানালাইসিস
📊 সাপ্লাই চেইন ডিমান্ড ফোরকাস্টিং
📊 HR এনালিটিক্স (অ্যাট্রিশন ট্রেন্ড)
"""
print(summary)
```