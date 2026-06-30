# Day 31: টাইম সিরিজ ফোরকাস্টিং
## Time Series Forecasting

### টাইম সিরিজ ফোরকাস্টিং কি?
টাইম সিরিজ ফোরকাস্টিং হল সময়ের সাথে সংগ্রহ করা ডেটা পয়েন্ট ব্যবহার করে ভবিষ্যতের মান অনুমান করার প্রক্রিয়া। ফাইন্যান্সে এটি সবচেয়ে গুরুত্বপূর্ণ টুলগুলোর একটি।

### ফাইন্যান্সে টাইম সিরিজের ব্যবহার
- **স্টক প্রাইস প্রেডিকশন**: ভবিষ্যতের শেয়ার দর অনুমান
- **ভোলাটিলিটি ফোরকাস্টিং**: রিস্ক মেজারমেন্ট
- **ইকোনমিক ইন্ডিকেটর**: জিডিপি, মুদ্রাস্ফীতি পূর্বাভাস
- **সেলস ফোরকাস্টিং**: রাজস্ব অনুমান

### টাইম সিরিজ উদাহরণ
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose

# টাইম সিরিজ ডেটা তৈরি
np.random.seed(42)
n = 1000
dates = pd.date_range('2021-01-01', periods=n, freq='D')

# ট্রেন্ড + সিজনালিটি + নয়েজ
trend = np.linspace(0, 50, n)
seasonal = 10 * np.sin(2 * np.pi * np.arange(n) / 365)  # বার্ষিক
weekly = 3 * np.sin(2 * np.pi * np.arange(n) / 7)       # সাপ্তাহিক
noise = np.random.randn(n) * 5

price = 100 + trend + seasonal + weekly + noise

df = pd.DataFrame({
    'date': dates,
    'price': price
})

plt.figure(figsize=(15, 6))
plt.plot(df['date'], df['price'], linewidth=0.5)
plt.title('Stock Price Time Series')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True, alpha=0.3)
plt.show()

print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Price range: {df['price'].min():.2f} to {df['price'].max():.2f}")
print(f"Mean price: {df['price'].mean():.2f}")
```

### 1. টাইম সিরিজ ডিকম্পোজিশন
```python
# সিজনাল ডিকম্পোজ
decomposition = seasonal_decompose(df['price'], model='additive', period=365)

fig, axes = plt.subplots(4, 1, figsize=(15, 10))
df['price'].plot(ax=axes[0], title='Original')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
plt.show()
```

### 2. স্টেশনারিটি চেক
```python
# Augmented Dickey-Fuller Test
def check_stationarity(series, name='Series'):
    result = adfuller(series.dropna())
    print(f'\n📊 {name} - ADF Test:')
    print(f'  ADF Statistic: {result[0]:.6f}')
    print(f'  p-value: {result[1]:.6f}')
    print(f'  Critical Values:')
    for key, value in result[4].items():
        print(f'    {key}: {value:.6f}')
    
    if result[1] <= 0.05:
        print('  ✅ Stationary (reject H0)')
    else:
        print('  ❌ Non-stationary (fail to reject H0)')

check_stationarity(df['price'], 'Original Price')

# ডিফারেন্সিং
df['price_diff'] = df['price'].diff()
check_stationarity(df['price_diff'], 'First Difference')

# অটোকোরিলেশন
fig, axes = plt.subplots(1, 2, figsize=(15, 4))
plot_acf(df['price_diff'].dropna(), lags=40, ax=axes[0])
plot_pacf(df['price_diff'].dropna(), lags=40, ax=axes[1])
axes[0].set_title('Autocorrelation Function (ACF)')
axes[1].set_title('Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
```

### 3. ফিচার ইঞ্জিনিয়ারিং (ল্যাগ ফিচার)
```python
# ল্যাগ ফিচার তৈরি
def create_lag_features(data, target_col, lags=[1, 2, 3, 5, 10, 20]):
    df_feat = data.copy()
    for lag in lags:
        df_feat[f'{target_col}_lag_{lag}'] = df_feat[target_col].shift(lag)
    return df_feat

# রোলিং উইন্ডো ফিচার
def create_rolling_features(data, target_col, windows=[5, 10, 20]):
    df_feat = data.copy()
    for w in windows:
        df_feat[f'{target_col}_rolling_mean_{w}'] = df_feat[target_col].rolling(w).mean()
        df_feat[f'{target_col}_rolling_std_{w}'] = df_feat[target_col].rolling(w).std()
        df_feat[f'{target_col}_rolling_min_{w}'] = df_feat[target_col].rolling(w).min()
        df_feat[f'{target_col}_rolling_max_{w}'] = df_feat[target_col].rolling(w).max()
    return df_feat

# ডেট প্রিপ
df_feat = create_lag_features(df, 'price', lags=[1, 2, 3, 5, 10])
df_feat = create_rolling_features(df_feat, 'price', windows=[5, 10, 20])
df_feat = df_feat.dropna()

# ফিচার সেট
feature_cols = [c for c in df_feat.columns if c not in ['date', 'price', 'price_diff']]
target_col = 'price'

print(f"Feature set: {len(feature_cols)} features")
print(f"Features: {feature_cols}")
print(f"Dataset after feature creation: {df_feat.shape}")
```

### 4. টাইম সিরিজ ট্রেন/টেস্ট স্প্লিট
```python
# টাইম-বেসড স্প্লিট (not random!)
train_size = int(len(df_feat) * 0.8)
train = df_feat.iloc[:train_size]
test = df_feat.iloc[train_size:]

X_train = train[feature_cols]
y_train = train[target_col]
X_test = test[feature_cols]
y_test = test[target_col]

print(f"Train: {train.index[0].date()} to {train.index[-1].date()}")
print(f"Test: {test.index[0].date()} to {test.index[-1].date()}")
print(f"Train size: {len(train)}, Test size: {len(test)}")
```

### 5. টাইম সিরিজ ফোরকাস্টিং মডেল
```python
# লিনিয়ার রিগ্রেশন
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# র‍্যান্ডম ফরেস্ট
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# ইভালুয়েশন
def evaluate_forecast(y_true, y_pred, model_name='Model'):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # MAPE
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print(f"\n📊 {model_name}:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    print(f"  MAPE: {mape:.2f}%")
    return rmse, mae, r2, mape

lr_metrics = evaluate_forecast(y_test, y_pred_lr, 'Linear Regression')
rf_metrics = evaluate_forecast(y_test, y_pred_rf, 'Random Forest')
```

### 6. ভিজুয়ালাইজেশন
```python
plt.figure(figsize=(15, 8))

# Actual vs Predicted
plt.subplot(2, 1, 1)
plt.plot(test.index, y_test, label='Actual', linewidth=2)
plt.plot(test.index, y_pred_lr, label='Linear Regression', linewidth=1, alpha=0.8)
plt.plot(test.index, y_pred_rf, label='Random Forest', linewidth=1, alpha=0.8)
plt.title('Time Series Forecast Comparison')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)

# রেসিডুয়াল
plt.subplot(2, 1, 2)
residuals_rf = y_test - y_pred_rf
plt.plot(test.index, residuals_rf, label='Residuals (RF)', color='red')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.title('Residuals (Random Forest)')
plt.xlabel('Date')
plt.ylabel('Residual')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 7. ফোরকাস্টিং বেস্ট প্র্যাকটিস
```python
print("""
✅ Time Series Best Practices:
1️⃣ Always use time-based split (not random)
2️⃣ Check stationarity before modeling
3️⃣ Use lag features carefully (avoid look-ahead bias)
4️⃣ Consider seasonality (daily, weekly, yearly)
5️⃣ Use walk-forward validation
6️⃣ Don't use future information in features
7️⃣ Consider multiple time horizons

⚠️ Common Mistakes:
- Using future data in training (look-ahead bias)
- Random train/test split (leaks future info)
- Ignoring non-stationarity
- Overfitting to noise
""")
```

### সারসংক্ষেপ
আজ আমরা টাইম সিরিজ ফোরকাস্টিং শিখলাম:
- **টাইম সিরিজ ডিকম্পোজ**: Trend + Seasonal + Residual
- **স্টেশনারিটি**: ADF Test, Differencing
- **ল্যাগ ফিচার**: Auto-regressive features
- **রোলিং উইন্ডো**: Moving averages, volatility
- **টাইম-বেজড স্প্লিট**: Preventing look-ahead bias

### অনুশীলনী
1. মাল্টি-স্টেপ ফোরকাস্টিং (7 দিন, 30 দিন) ইমপ্লিমেন্ট করুন
2. ওয়াক-ফরওয়ার্ড ভ্যালিডেশন ইমপ্লিমেন্ট করুন
3. বিভিন্ন ল্যাগ এবং উইন্ডো সাইজ নিয়ে এক্সপেরিমেন্ট করুন
4. রিয়েল-ওয়ার্ল্ড স্টক ডেটা (yfinance) ব্যবহার করে ফোরকাস্টিং করুন
