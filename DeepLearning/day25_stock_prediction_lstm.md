# Day 25: LSTM দিয়ে স্টক প্রাইস প্রেডিকশন 💰

## স্টক প্রাইস প্রেডিকশন
স্টক মার্কেট প্রেডিকশন টাইম সিরিজ ফোরকাস্টিং-এর একটি ক্লাসিক্যাল সমস্যা। LSTM-এর সিকোয়েন্স লার্নিং能力 এটির জন্য আদর্শ।

### চ্যালেঞ্জেস
- **স্টকাস্টিক প্রকৃতি**: মার্কেট এলোমেলো
- **Efficient Market Hypothesis**: সব তথ্য ইতিমধ্যে প্রাইসে প্রতিফলিত
- **মাল্টি-ফ্যাক্টর**: অসংখ্য ভেরিয়েবল প্রভাবিত করে
- **নন-স্টেশনারিটি**: পরিসংখ্যানিক বৈশিষ্ট্য পরিবর্তনশীল

### স্ট্র্যাটেজি
- OHLCV ডেটা ব্যবহার
- টেকনিক্যাল ইন্ডিকেটর যোগ
- মাল্টি-স্টেপ ফোরকাস্টিং
- এনসেম্বল মডেল

## সম্পূর্ণ স্টক প্রেডিকশন পাইপলাইন

```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. সিন্থেটিক স্টক ডেটা জেনারেশন

```python
class StockDataGenerator:
    """রিয়েলিস্টিক স্টক ডেটা জেনারেটর"""
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.price = None
    
    def generate(self, n_days=2000, start_price=100, 
                 trend=0.0005, volatility=0.015):
        """স্টক ডেটা জেনারেট"""
        # GBM (Geometric Brownian Motion)
        returns = np.random.normal(trend, volatility, n_days)
        
        # ভলাটিলিটি ক্লাস্টারিং (GARCH প্রভাব)
        vol = np.ones(n_days) * volatility
        for t in range(20, n_days):
            recent_returns = returns[t-20:t]
            vol[t] = 0.85 * vol[t-1] + 0.15 * np.std(recent_returns)
            returns[t] = np.random.normal(trend, vol[t])
        
        # প্রাইস গণনা
        price = start_price * np.exp(np.cumsum(returns))
        
        # OHLC জেনারেট
        df = pd.DataFrame(index=pd.date_range(
            '2018-01-01', periods=n_days, freq='D'))
        df['close'] = price
        
        # হাই/লো/ওপেন
        daily_vol = returns * price
        df['high'] = df['close'] + np.abs(daily_vol) * np.random.uniform(0.5, 1.5, n_days)
        df['low'] = df['close'] - np.abs(daily_vol) * np.random.uniform(0.5, 1.5, n_days)
        df['open'] = df['close'].shift(1) + daily_vol * np.random.uniform(-0.3, 0.3)
        df['open'] = df['open'].fillna(df['close'])
        
        df['volume'] = np.random.lognormal(mean=14, sigma=1, size=n_days) * \
                       (1 + 0.5 * np.abs(returns))
        
        self.price = df
        return df

# ডেটা জেনারেট
generator = StockDataGenerator(seed=42)
df = generator.generate(n_days=2000, start_price=150)

print(df.head())
print(f"\nস্টক প্রাইস রেঞ্জ: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
print(f"মোট ট্রেডিং ডে: {len(df)}")
```

## 2. টেকনিক্যাল ইন্ডিকেটর

```python
def add_technical_indicators(df):
    """টেকনিক্যাল ইন্ডিকেটর যোগ করুন"""
    # Moving Averages
    df['sma_10'] = df['close'].rolling(10).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    
    # RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    macd_line = df['ema_12'] - df['ema_26']
    signal_line = macd_line.ewm(span=9).mean()
    df['macd'] = macd_line
    df['macd_signal'] = signal_line
    df['macd_diff'] = macd_line - signal_line
    
    # Bollinger Bands
    bb_mid = df['close'].rolling(20).mean()
    bb_std = df['close'].rolling(20).std()
    df['bb_upper'] = bb_mid + 2 * bb_std
    df['bb_lower'] = bb_mid - 2 * bb_std
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / bb_mid
    
    # Volume Indicators
    df['volume_sma'] = df['volume'].rolling(20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_sma']
    
    # Price Returns
    df['return_1'] = df['close'].pct_change(1)
    df['return_5'] = df['close'].pct_change(5)
    df['return_20'] = df['close'].pct_change(20)
    
    # Volatility
    df['volatility'] = df['return_1'].rolling(20).std()
    
    return df

# ইন্ডিকেটর যোগ
df = add_technical_indicators(df)
df_clean = df.dropna()

print(f"ফিচারের সংখ্যা: {len(df_clean.columns)}")
print(f"ফিচার লিস্ট: {list(df_clean.columns)}")
print(f"\nক্লিন ডেটা: {df_clean.shape}")
```

## 3. ফিচার সিলেকশন ও ডেটা প্রিপারেশন

```python
# ফিচার সিলেকশন
feature_cols = [
    'open', 'high', 'low', 'volume',
    'sma_10', 'sma_50', 'rsi', 'macd', 'macd_diff',
    'bb_width', 'volume_ratio', 'return_1', 'return_5',
    'volatility'
]
target_col = 'close'

SEQUENCE_LENGTH = 30
BATCH_SIZE = 64

# ডেটা প্রিপারেশন
def prepare_stock_data(df, features, target, seq_len=30):
    data = df[features].values
    target_data = df[[target]].values
    
    # স্কেলার
    feat_scaler = MinMaxScaler()
    tgt_scaler = MinMaxScaler()
    
    scaled_feat = feat_scaler.fit_transform(data)
    scaled_tgt = tgt_scaler.fit_transform(target_data)
    
    # সিকোয়েন্স
    X, y = [], []
    for i in range(len(scaled_feat) - seq_len):
        X.append(scaled_feat[i:i+seq_len])
        y.append(scaled_tgt[i+seq_len])
    
    X, y = np.array(X), np.array(y)
    
    # ট্রেন/ভ্যাল/টেস্ট (70/15/15)
    n = len(X)
    train_end = int(0.7 * n)
    val_end = int(0.85 * n)
    
    return {
        'X_train': X[:train_end], 'y_train': y[:train_end],
        'X_val': X[train_end:val_end], 'y_val': y[train_end:val_end],
        'X_test': X[val_end:], 'y_test': y[val_end:],
        'feat_scaler': feat_scaler, 'tgt_scaler': tgt_scaler
    }

data = prepare_stock_data(df_clean, feature_cols, target_col, SEQUENCE_LENGTH)

for k, v in data.items():
    if isinstance(v, np.ndarray):
        print(f"{k}: {v.shape}")
```

## 4. স্টক প্রেডিকশন LSTM মডেল

```python
class StockPredictor(nn.Module):
    """স্টক প্রাইস প্রেডিকশন LSTM"""
    def __init__(self, input_size, hidden_size=256, num_layers=2, dropout=0.4):
        super().__init__()
        self.lstm1 = nn.LSTM(input_size, hidden_size, num_layers=1, 
                             batch_first=True, dropout=0)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size//2, num_layers=1,
                             batch_first=True, dropout=0)
        self.dropout = nn.Dropout(dropout)
        self.bn = nn.BatchNorm1d(hidden_size//2)
        self.fc1 = nn.Linear(hidden_size//2, 64)
        self.fc2 = nn.Linear(64, 16)
        self.fc3 = nn.Linear(16, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out, _ = self.lstm1(x)
        out = self.dropout(out)
        out, _ = self.lstm2(out)
        out = out[:, -1, :]
        out = self.bn(out)
        out = self.dropout(out)
        out = self.relu(self.fc1(out))
        out = self.relu(self.fc2(out))
        out = self.fc3(out)
        return out

model = StockPredictor(
    input_size=len(feature_cols),
    hidden_size=256,
    num_layers=2
).to(device)

print(f"মডেল প্যারামিটার: {sum(p.numel() for p in model.parameters()):,}")

# DataLoader
train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(data['X_train']), 
                  torch.FloatTensor(data['y_train'])),
    batch_size=BATCH_SIZE, shuffle=True
)
val_loader = DataLoader(
    TensorDataset(torch.FloatTensor(data['X_val']),
                  torch.FloatTensor(data['y_val'])),
    batch_size=BATCH_SIZE
)
```

## 5. ট্রেনিং ফাংশন

```python
def train_stock_model(model, train_loader, val_loader, epochs=100):
    """স্টক মডেল ট্রেনিং"""
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_val_loss = float('inf')
    patience = 15
    patience_counter = 0
    
    for epoch in range(epochs):
        # ট্রেন
        model.train()
        train_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            pred = model(batch_X)
            loss = criterion(pred, batch_y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # ভ্যালিডেশন
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                val_loss += criterion(model(batch_X), batch_y).item()
        
        avg_val_loss = val_loss / len(val_loader)
        scheduler.step()
        
        # Early stopping
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'best_stock_model.pt')
            patience_counter = 0
        else:
            patience_counter += 1
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Train: {avg_train_loss:.6f} | Val: {avg_val_loss:.6f}")
        
        if patience_counter >= patience:
            print(f"\n⏹️ Early stopping at epoch {epoch+1}")
            break
    
    print(f"\n✅ সেরা Val Loss: {best_val_loss:.6f}")
    model.load_state_dict(torch.load('best_stock_model.pt'))
    return model

model = train_stock_model(model, train_loader, val_loader, epochs=150)
```

## 6. ইভালুয়েশন ও ভিজুয়ালাইজেশন

```python
# টেস্ট সেটে ইভালুয়েশন
model.eval()
X_test_tensor = torch.FloatTensor(data['X_test']).to(device)
y_test_tensor = torch.FloatTensor(data['y_test']).to(device)

with torch.no_grad():
    predictions = model(X_test_tensor).cpu().numpy()

# আনস্কেল
predictions_actual = data['tgt_scaler'].inverse_transform(predictions)
y_test_actual = data['tgt_scaler'].inverse_transform(data['y_test'])

# মেট্রিক্স
mse = np.mean((predictions_actual - y_test_actual) ** 2)
mae = np.mean(np.abs(predictions_actual - y_test_actual))
mape = np.mean(np.abs((predictions_actual - y_test_actual) / y_test_actual)) * 100

print(f"{'মেট্রিক':<20} {'মান':<15}")
print("-" * 35)
print(f"{'MSE':<20} {mse:<15.4f}")
print(f"{'RMSE':<20} {np.sqrt(mse):<15.4f}")
print(f"{'MAE':<20} {mae:<15.4f}")
print(f"{'MAPE':<20} {mape:<15.2f}%")
print(f"{'Accuracy (≈)':<20} {(100-mape):<15.2f}%")

# ট্রেডিং সিমুলেশন
def simulate_trading(predictions, actuals, threshold=0.0):
    """প্রেডিকশন বনাম বাই-এন্ড-হোল্ড সিমুলেশন"""
    capital = 10000
    position = 0
    trades = []
    
    for i in range(1, len(predictions)):
        pred_change = (predictions[i] - actuals[i-1]) / actuals[i-1]
        actual_change = (actuals[i] - actuals[i-1]) / actuals[i-1]
        
        if pred_change > threshold and position == 0:
            position = capital / actuals[i-1]
            capital = 0
            trades.append(('BUY', i))
        elif pred_change < -threshold and position > 0:
            capital = position * actuals[i]
            position = 0
            trades.append(('SELL', i))
    
    # ফাইনাল পজিশন ক্লোজ
    if position > 0:
        capital = position * actuals[-1]
    
    final_value = capital
    buy_hold = 10000 * actuals[-1] / actuals[0]
    
    return final_value, buy_hold, trades

strategy_return, buy_hold_return, trades = simulate_trading(
    predictions_actual.flatten(), y_test_actual.flatten()
)

print(f"\n💰 ট্রেডিং সিমুলেশন (Initial: $10,000)")
print(f"{'স্ট্র্যাটেজি':<25} {'বাই-এন্ড-হোল্ড':<25}")
print("-" * 50)
print(f"${strategy_return:<24,.2f} ${buy_hold_return:<24,.2f}")
print(f"{(strategy_return/10000 - 1)*100:<24.2f}% {(buy_hold_return/10000 - 1)*100:<24.2f}%")
print(f"মোট ট্রেড: {len(trades)}")
```

## 7. ডাইরেকশনাল অ্যাকুরেসি

```python
# ডাইরেকশনাল অ্যাকুরেসি (প্রাইস মুভমেন্ট দিক)
pred_direction = np.sign(np.diff(predictions_actual.flatten()))
actual_direction = np.sign(np.diff(y_test_actual.flatten()))
directional_accuracy = np.mean(pred_direction == actual_direction) * 100

print(f"🎯 ডাইরেকশনাল অ্যাকুরেসি: {directional_accuracy:.2f}%")
print(f"(মার্কেট র্যান্ডম হাইপোথিসিস: 50%)")

# কনফিউশন ম্যাট্রিক্স
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(actual_direction, pred_direction)
print(f"\nকনফিউশন ম্যাট্রিক্স:")
print(f"{'':>15} {'প্রেডিক্টেড আপ':<20} {'প্রেডিক্টেড ডাউন':<20}")
print(f"{'আসল আপ':<15} {cm[1][1]:<20} {cm[1][0]:<20}")
print(f"{'আসল ডাউন':<15} {cm[0][1]:<20} {cm[0][0]:<20}")

# ভিজুয়ালাইজেশন
plt.figure(figsize=(14, 8))

plt.subplot(2, 1, 1)
plt.plot(y_test_actual, label='আসল প্রাইস', linewidth=2)
plt.plot(predictions_actual, label='প্রেডিকশন', linewidth=2, linestyle='--')
plt.title('LSTM স্টক প্রাইস প্রেডিকশন')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
residuals = y_test_actual - predictions_actual
plt.plot(residuals, label='রেসিডুয়াল (আসল - প্রেডিকশন)', color='red')
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.title('প্রেডিকশন এরর')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## গুরুত্বপূর্ণ সতর্কতা
- **স্টক প্রেডিকশন 100% নির্ভুল নয়**
- মার্কেট অপ্রত্যাশিত ইভেন্টে প্রভাবিত হয়
- পেস্ট ডেটা → ভবিষ্যতের গ্যারান্টি নয়
- **রিস্ক ম্যানেজমেন্ট সবচেয়ে গুরুত্বপূর্ণ**
- পেপার ট্রেডিং দিয়ে শুরু করুন

## সারাংশ
- LSTM স্টক প্রাইস প্রেডিকশনের জন্য শক্তিশালী টুল
- টেকনিক্যাল ইন্ডিকেটর পারফরম্যান্স উন্নত করে
- ডাইরেকশনাল অ্যাকুরেসি 50%+ হলে কার্যকর
- ডেটা কোয়ালিটি ও ফিচার ইঞ্জিনিয়ারিং গুরুত্বপূর্ণ
- প্রেডিকশন 100% নির্ভরযোগ্য নয় → রিস্ক ম্যানেজমেন্ট জরুরি