# Day 35: স্টক প্রেডিকশন
## Stock Price Prediction

### স্টক প্রেডিকশন কি?
স্টক প্রেডিকশন হল মেশিন লার্নিং এবং ডিপ লার্নিং মডেল ব্যবহার করে ভবিষ্যতের স্টক মূল্য অনুমান করার প্রক্রিয়া। এটি ফাইন্যান্সের সবচেয়ে জনপ্রিয় ML অ্যাপ্লিকেশনগুলোর একটি।

### চ্যালেঞ্জ
- স্টক মার্কেট **অত্যন্ত নয়সি** এবং **আনপ্রেডিক্টেবল**
- **ইফিশিয়েন্ট মার্কেট হাইপোথিসিস**: সব পাবলিক ইনফরমেশন ইতিমধ্যে প্রাইসে রিফ্লেক্টেড
- **নন-স্টেশনারি**: ডিস্ট্রিবিউশন সময়ের সাথে পরিবর্তিত হয়
- **লুক-অ্যাহেড বায়াস**: ভবিষ্যতের তথ্য লিকেজ

### ফাইন্যান্স উদাহরণ: রিয়েল স্টক প্রাইস ফোরকাস্টিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.svm import SVR
import warnings
warnings.filterwarnings('ignore')

# স্টক ডেটা তৈরি
np.random.seed(42)
n = 1000
dates = pd.date_range('2021-06-01', periods=n, freq='D')

# OHLCV ডেটা
base_price = 150
returns = np.random.randn(n) * 0.015 + 0.0005
price = base_price * np.exp(np.cumsum(returns))

df = pd.DataFrame({
    'date': dates,
    'open': price * (1 + np.random.randn(n) * 0.005),
    'high': price * (1 + np.abs(np.random.randn(n)) * 0.01),
    'low': price * (1 - np.abs(np.random.randn(n)) * 0.01),
    'close': price,
    'volume': np.random.randint(1000000, 10000000, n)
})

print("📊 Stock Data:")
print(df.head())
print(f"\nShape: {df.shape}")
print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
```

### 1. ফিচার ইঞ্জিনিয়ারিং (টেকনিক্যাল ইন্ডিকেটর)
```python
# টেকনিক্যাল ইন্ডিকেটর
df['returns'] = df['close'].pct_change()
df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
df['range'] = df['high'] - df['low']
df['range_pct'] = df['range'] / df['close']

# মুভিং এভারেজ
for window in [5, 10, 20, 50]:
    df[f'sma_{window}'] = df['close'].rolling(window).mean()
    df[f'ema_{window}'] = df['close'].ewm(span=window, adjust=False).mean()

# ভোলাটিলিটি
for window in [5, 10, 20]:
    df[f'volatility_{window}'] = df['returns'].rolling(window).std()

# RSI
def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['rsi_14'] = rsi(df['close'])

# MACD
df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
df['macd'] = df['ema_12'] - df['ema_26']
df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
df['macd_hist'] = df['macd'] - df['macd_signal']

# বোলিঙ্গার ব্যান্ড
df['bb_middle'] = df['close'].rolling(20).mean()
df['bb_std'] = df['close'].rolling(20).std()
df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']

# ভলিউম ইন্ডিকেটর
df['volume_sma'] = df['volume'].rolling(20).mean()
df['volume_ratio'] = df['volume'] / df['volume_sma']

# টার্গেট: পরবর্তী দিনের দিক (বাইনারী)
df['target_direction'] = (df['close'].shift(-1) > df['close']).astype(int)
# টার্গেট: পরবর্তী দিনের রিটার্ন (রিগ্রেশন)
df['target_return'] = df['close'].shift(-1) / df['close'] - 1

df = df.dropna()
print(f"\nAfter feature engineering: {df.shape}")
print(f"Features: {[c for c in df.columns if c not in ['date']]}")
```

### 2. ফিচার সিলেকশন এবং প্রিপ্রসেসিং
```python
# ফিচার এবং টার্গেট
feature_cols = [c for c in df.columns if c not in [
    'date', 'open', 'high', 'low', 'close', 'volume',
    'target_direction', 'target_return',
    'ema_12', 'ema_26'  # ডেরাইভড ফিচার
]]

# রিগ্রেশন টার্গেট
X_reg = df[feature_cols].values
y_reg = df['target_return'].values

# ক্লাসিফিকেশন টার্গেট
X_clf = df[feature_cols].values
y_clf = df['target_direction'].values

# ট্রেন/টেস্ট স্প্লিট (টাইম-বেসড)
split_idx = int(len(df) * 0.8)
X_train_r, X_test_r = X_reg[:split_idx], X_reg[split_idx:]
y_train_r, y_test_r = y_reg[:split_idx], y_reg[split_idx:]
X_train_c, X_test_c = X_clf[:split_idx], X_clf[split_idx:]
y_train_c, y_test_c = y_clf[:split_idx], y_clf[split_idx:]

print(f"Train size: {X_train_r.shape[0]}, Test size: {X_test_r.shape[0]}")
print(f"Features: {len(feature_cols)}")
```

### 3. মডেল ট্রেইনিং (রিগ্রেশন)
```python
# রিগ্রেশন মডেল
reg_models = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'SVR': SVR(kernel='rbf')
}

for name, model in reg_models.items():
    model.fit(X_train_r, y_train_r)
    y_pred = model.predict(X_test_r)
    
    # ডিরেকশন অ্যাকুরেসি
    direction_accuracy = np.mean((y_pred > 0) == (y_test_r > 0))
    
    print(f"\n📊 {name}:")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y_test_r, y_pred)):.6f}")
    print(f"  MAE:  {mean_absolute_error(y_test_r, y_pred):.6f}")
    print(f"  Direction Accuracy: {direction_accuracy:.2%}")
```

### 4. মডেল ট্রেইনিং (ক্লাসিফিকেশন)
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ক্লাসিফিকেশন মডেল
clf_models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

for name, model in clf_models.items():
    model.fit(X_train_c, y_train_c)
    y_pred = model.predict(X_test_c)
    y_pred_binary = (y_pred > 0.5).astype(int)
    
    print(f"\n📊 {name} (Classification):")
    print(f"  Accuracy:  {accuracy_score(y_test_c, y_pred_binary):.4f}")
    print(f"  Precision: {precision_score(y_test_c, y_pred_binary):.4f}")
    print(f"  Recall:    {recall_score(y_test_c, y_pred_binary):.4f}")
    print(f"  F1-Score:  {f1_score(y_test_c, y_pred_binary):.4f}")
```

### 5. ট্রেডিং সিগন্যাল এবং ব্যাকটেস্টিং
```python
# ট্রেডিং সিমুলেশন
def backtest_strategy(predictions, actual_returns, initial_capital=10000):
    capital = initial_capital
    positions = []  # 1 = long, 0 = cash
    portfolio_value = [capital]
    
    for pred, ret in zip(predictions, actual_returns):
        # সিগন্যাল
        if pred > 0:  # বুলিশ
            position = 1
            capital *= (1 + ret)
        else:  # বিয়ারিশ
            position = 0
        
        positions.append(position)
        portfolio_value.append(capital)
    
    total_return = (capital - initial_capital) / initial_capital
    
    # মেট্রিক্স
    sharpe = np.mean(actual_returns[predictions > 0]) / \
             (np.std(actual_returns[predictions > 0]) + 1e-6) * np.sqrt(252)
    
    return {
        'total_return': total_return,
        'final_capital': capital,
        'sharpe_ratio': sharpe,
        'positions': positions,
        'portfolio_value': portfolio_value
    }

# বেস্ট মডেল দিয়ে ব্যাকটেস্ট
best_model = RandomForestRegressor(n_estimators=100, random_state=42)
best_model.fit(X_train_r, y_train_r)
y_pred = best_model.predict(X_test_r)

results = backtest_strategy(y_pred, y_test_r)
print(f"\n📈 Backtest Results:")
print(f"  Initial Capital: $10,000")
print(f"  Final Capital: ${results['final_capital']:.2f}")
print(f"  Total Return: {results['total_return']:.2%}")
print(f"  Sharpe Ratio: {results['sharpe_ratio']:.4f}")
print(f"  Long positions: {sum(results['positions'])}/{len(results['positions'])}")

# পোর্টফোলিও ভ্যালু চার্ট
plt.figure(figsize=(15, 5))
plt.plot(results['portfolio_value'], linewidth=2)
plt.title('Trading Strategy Performance')
plt.xlabel('Trading Day')
plt.ylabel('Portfolio Value ($)')
plt.grid(True, alpha=0.3)
plt.axhline(y=10000, color='gray', linestyle='--', alpha=0.5)
plt.show()
```

### 6. মডেল ইন্টারপ্রিটেশন
```python
# ফিচার ইম্পরটেন্স
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_r, y_train_r)

importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 15 Most Important Features:")
print(importance.head(15).to_string(index=False))

# টপ ফিচার ভিজুয়ালাইজেশন
plt.figure(figsize=(12, 6))
plt.barh(importance.head(15)['feature'], importance.head(15)['importance'])
plt.xlabel('Importance')
plt.title('Feature Importance for Stock Prediction')
plt.gca().invert_yaxis()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### স্টক প্রেডিকশন বেস্ট প্র্যাকটিস
```python
print("""
✅ Stock Prediction Best Practices:
1️⃣ Always use time-based split (not random)
2️⃣ Avoid look-ahead bias at all costs
3️⃣ Use multiple features (technical + fundamental)
4️⃣ Focus on direction prediction, not exact price
5️⃣ Combine multiple models (ensemble)
6️⃣ Use walk-forward validation
7️⃣ Account for transaction costs

⚠️ Important Reality Check:
Stock prediction is extremely difficult!
A model with >55% directional accuracy is considered good.
Always use proper risk management.
""")
```

### সারসংক্ষেপ
আজ আমরা স্টক প্রেডিকশনের সম্পূর্ণ পাইপলাইন শিখলাম:
- **টেকনিক্যাল ইন্ডিকেটর**: SMA, EMA, RSI, MACD, Bollinger Bands
- **ফিচার ইঞ্জিনিয়ারিং**: Returns, Volatility, Volume indicators
- **মডেল**: Regression (RMSE, MAE) + Classification (Direction Accuracy)
- **ব্যাকটেস্টিং**: ট্রেডিং সিমুলেশন, Sharpe Ratio
- **ইন্টারপ্রিটেশন**: Feature Importance Analysis

### অনুশীলনী
1. yfinance ব্যবহার করে রিয়েল স্টক (AAPL, TSLA) ডেটা ডাউনলোড করুন
2. ফান্ডামেন্টাল ডেটা (PE ratio, EPS) যোগ করে মডেল উন্নত করুন
3. সেন্টিমেন্ট অ্যানালাইসিস (news, Twitter) ফিচার যোগ করুন
4. মাল্টি-স্টক পোর্টফোলিও অপ্টিমাইজেশন মডেল তৈরি করুন