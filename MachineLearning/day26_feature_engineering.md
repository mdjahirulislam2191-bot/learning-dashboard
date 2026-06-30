# Day 26: ফিচার ইঞ্জিনিয়ারিং
## Feature Engineering

### ফিচার ইঞ্জিনিয়ারিং কি?
ফিচার ইঞ্জিনিয়ারিং হল কাঁচা ডেটা থেকে নতুন ফিচার তৈরি করার প্রক্রিয়া যা ML মডেলের পারফরম্যান্স উন্নত করে। এটি ডেটা সায়েন্সের সবচেয়ে গুরুত্বপূর্ণ ধাপগুলোর একটি।

### কেন ফিচার ইঞ্জিনিয়ারিং গুরুত্বপূর্ণ?
- মডেল অ্যাকুরেসি উন্নত করে
- ডেটার প্যাটার্ন আরও স্পষ্ট করে
- ডোমেইন নলেজ ব্যবহারের সুযোগ দেয়
- ওভারফিটিং কমাতে সাহায্য করে

### ফাইন্যান্স উদাহরণ: স্টক ফিচার তৈরি
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# স্টক ডেটা তৈরি
np.random.seed(42)
n = 500
dates = pd.date_range('2023-01-01', periods=n, freq='D')
price = 100 + np.cumsum(np.random.randn(n) * 0.5) + np.linspace(0, 20, n)

df = pd.DataFrame({'date': dates, 'close': price})

# ফিচার ইঞ্জিনিয়ারিং
# 1. ল্যাগ ফিচার
for lag in [1, 2, 3, 5, 10]:
    df[f'lag_{lag}'] = df['close'].shift(lag)

# 2. রোলিং উইন্ডো স্ট্যাটিস্টিক্স
for window in [5, 10, 20]:
    df[f'rolling_mean_{window}'] = df['close'].rolling(window).mean()
    df[f'rolling_std_{window}'] = df['close'].rolling(window).std()
    df[f'rolling_min_{window}'] = df['close'].rolling(window).min()
    df[f'rolling_max_{window}'] = df['close'].rolling(window).max()

# 3. রিটার্ন ফিচার
df['return_1d'] = df['close'].pct_change()
df['return_5d'] = df['close'].pct_change(5)
df['return_20d'] = df['close'].pct_change(20)

# 4. ভোলাটিলিটি ফিচার
df['volatility_10d'] = df['return_1d'].rolling(10).std()
df['volatility_20d'] = df['return_1d'].rolling(20).std()

# 5. টেকনিক্যাল ইন্ডিকেটর
# SMA (Simple Moving Average)
df['sma_10'] = df['close'].rolling(10).mean()
df['sma_20'] = df['close'].rolling(20).mean()

# RSI (Relative Strength Index)
def compute_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['rsi_14'] = compute_rsi(df['close'])

# 6. টাইম-বেসড ফিচার
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

# ডেটা ক্লিন
df = df.dropna()
print(f"Dataset shape: {df.shape}")
print(f"Features: {list(df.columns)}")
print(df.head())
```

### ফিচার স্কেলিং ও ট্রান্সফরমেশন
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PolynomialFeatures

# ডেটা স্প্লিট
target = 'close'
feature_cols = [c for c in df.columns if c not in ['date', 'close']]

X = df[feature_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# স্কেলিং তুলনা
scalers = {
    'Standard': StandardScaler(),
    'MinMax': MinMaxScaler(),
    'Robust': RobustScaler()
}

for name, scaler in scalers.items():
    X_scaled = scaler.fit_transform(X_train)
    print(f"\n{name} Scaler - Mean: {X_scaled.mean():.4f}, Std: {X_scaled.std():.4f}")
    print(f"  Min: {X_scaled.min():.4f}, Max: {X_scaled.max():.4f}")

# পলিনোমিয়াল ফিচার (ইন্টারঅ্যাকশন)
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_poly = poly.fit_transform(X_train.iloc[:, :5])
print(f"\nOriginal features (5): {X_train.iloc[:, :5].shape[1]}")
print(f"Polynomial features: {X_poly.shape[1]}")
```

### ফিচার ইঞ্জিনিয়ারিংয়ের প্রভাব
```python
# বেস মডেল (শুধু ল্যাগ ফিচার)
base_features = ['lag_1', 'lag_2', 'lag_3']
X_base = X_train[base_features]
X_test_base = X_test[base_features]

rf_base = RandomForestRegressor(n_estimators=50, random_state=42)
rf_base.fit(X_base, y_train)
base_score = rf_base.score(X_test_base, y_test)

# ফুল মডেল (সব ফিচার)
rf_full = RandomForestRegressor(n_estimators=50, random_state=42)
rf_full.fit(X_train, y_train)
full_score = rf_full.score(X_test, y_test)

print(f"Base Model R² (3 features): {base_score:.4f}")
print(f"Full Model R² ({X_train.shape[1]} features): {full_score:.4f}")
print(f"Improvement: {(full_score - base_score) * 100:.2f}%")

# ফিচার ইম্পরটেন্স
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_full.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(importance.head(10).to_string(index=False))
```

### সারসংক্ষেপ
আজ আমরা ফিচার ইঞ্জিনিয়ারিং এর বিভিন্ন কৌশল শিখলাম:
- **ল্যাগ ফিচার**: টাইম-ল্যাগড ভ্যালু
- **রোলিং স্ট্যাটিস্টিক্স**: মুভিং এভারেজ, স্ট্যান্ডার্ড ডেভিয়েশন
- **রিটার্ন ফিচার**: পার্সেন্টেজ চেঞ্জ
- **টেকনিক্যাল ইন্ডিকেটর**: SMA, RSI
- **টাইম ফিচার**: দিন, মাস, কোয়ার্টার
- **পলিনোমিয়াল ফিচার**: ইন্টারঅ্যাকশন টার্ম

### অনুশীলনী
1. আপনার নিজের স্টক ডেটার জন্য কাস্টম ফিচার তৈরি করুন
2. MACD (Moving Average Convergence Divergence) ইন্ডিকেটর তৈরি করুন
3. বুলিশ/বিয়ারিশ প্যাটার্ন শনাক্ত করার জন্য নতুন ফিচার ডিজাইন করুন
4. ফিচার সিলেকশনের মাধ্যমে সবচেয়ে গুরুত্বপূর্ণ ফিচার চিহ্নিত করুন
