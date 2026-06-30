# Day 24: LSTM দিয়ে টাইম সিরিজ ফোরকাস্টিং 📈

## টাইম সিরিজ ফোরকাস্টিং কী?
টাইম সিরিজ ফোরকাস্টিং হল সময় অনুযায়ী সাজানো ডেটার ভবিষ্যৎ মান পূর্বাভাস করা।

### ফিন্যান্সে টাইম সিরিজ
- স্টক প্রাইস প্রেডিকশন
- ফরেক্স রেট ফোরকাস্টিং
- ইকোনোমিক ইন্ডিকেটর প্রেডিকশন
- ভলাটিলিটি ফোরকাস্টিং
- রিস্ক ম্যানেজমেন্ট

### ট্র্যাডিশনাল vs DL অ্যাপ্রোচ
| পদ্ধতি | ট্র্যাডিশনাল (ARIMA) | ডিপ লার্নিং (LSTM) |
|---|---|---|
| লিনিয়ারিটি | লিনিয়ার | নন-লিনিয়ার |
| ফিচার ইঞ্জিনিয়ারিং | প্রয়োজন | অটোমেটিক |
| মাল্টি-ভেরিয়েট | জটিল | সহজ |
| Long-term | সীমিত | শক্তিশালী |
| অ্যাডাপ্টিভিটি | কম | বেশি |

## সম্পূর্ণ টাইম সিরিজ পাইপলাইন

```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# ডিভাইস সেটআপ
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. ডেটা জেনারেশন ও প্রিপ্রসেসিং

```python
# রিয়েলিস্টিক সিন্থেটিক টাইম সিরিজ
np.random.seed(42)
n_points = 2000

t = np.linspace(0, 100, n_points)
# ট্রেন্ড + সিজনালিটি + নয়েজ
trend = 0.01 * t
seasonal = 2 * np.sin(2 * np.pi * t / 10) + 1.5 * np.sin(2 * np.pi * t / 25)
noise = np.random.randn(n_points) * 0.3
data = 100 + trend + seasonal + noise

# ডেটাফ্রেম
df = pd.DataFrame({
    'value': data,
    'date': pd.date_range('2020-01-01', periods=n_points, freq='D')
})
df['returns'] = df['value'].pct_change()
df['sma_5'] = df['value'].rolling(5).mean()
df['sma_20'] = df['value'].rolling(20).mean()
df['volatility'] = df['returns'].rolling(10).std()

print(df.head(10))
print(f"ডেটা রেঞ্জ: {df['date'].min()} → {df['date'].max()}")
print(f"মোট পয়েন্ট: {len(df)}")
```

## 2. সিকোয়েন্স প্রস্তুতি ফাংশন

```python
def prepare_ts_data(df, feature_cols, target_col, seq_length=30, train_ratio=0.8):
    """টাইম সিরিজ ডেটা প্রস্তুত"""
    # ফিচার এবং টার্গেট আলাদা
    feature_data = df[feature_cols].values
    target_data = df[target_col].values.reshape(-1, 1)
    
    # স্কেলিং
    feature_scaler = MinMaxScaler()
    target_scaler = MinMaxScaler()
    
    scaled_features = feature_scaler.fit_transform(feature_data)
    scaled_target = target_scaler.fit_transform(target_data)
    
    # সিকোয়েন্স তৈরি
    X, y = [], []
    for i in range(len(scaled_features) - seq_length):
        X.append(scaled_features[i:i+seq_length])
        y.append(scaled_target[i+seq_length])
    
    X = np.array(X)
    y = np.array(y)
    
    # ট্রেন-টেস্ট স্প্লিট
    split = int(train_ratio * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    return (X_train, X_test, y_train, y_test,
            feature_scaler, target_scaler)

# ফিচার সিলেক্ট
features = ['value', 'returns', 'sma_5', 'volatility']
target = 'value'

# ফাঁকা মান দূর করুন
df_clean = df.dropna()

X_train, X_test, y_train, y_test, feat_scaler, tgt_scaler = \
    prepare_ts_data(df_clean, features, target, seq_length=30)

print(f"X_train: {X_train.shape}")
print(f"X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}")
print(f"y_test: {y_test.shape}")
```

## 3. LSTM মডেল ডেফিনিশন

```python
class TimeSeriesLSTM(nn.Module):
    """টাইম সিরিজ ফোরকাস্টিং LSTM"""
    def __init__(self, input_size, hidden_size=128, num_layers=2, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.bn = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_size, 32)
        self.fc2 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # লাস্ট টাইমস্টেপ
        out = self.bn(out)
        out = self.dropout(out)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out

model = TimeSeriesLSTM(input_size=len(features), hidden_size=128, num_layers=2)
model = model.to(device)
print(f"মডেল: {model}")
total_params = sum(p.numel() for p in model.parameters())
print(f"মোট প্যারামিটার: {total_params:,}")
```

## 4. অ্যাডভান্সড ট্রেনিং

```python
# DataLoader
train_dataset = TensorDataset(
    torch.FloatTensor(X_train),
    torch.FloatTensor(y_train)
)
test_dataset = TensorDataset(
    torch.FloatTensor(X_test),
    torch.FloatTensor(y_test)
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64)

# লস ও অপ্টিমাইজার
criterion = nn.MSELoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-5)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=10, verbose=True
)

# ট্রেনিং লুপ
epochs = 150
best_test_loss = float('inf')
train_losses, test_losses = [], []

for epoch in range(epochs):
    # ট্রেন
    model.train()
    train_loss = 0
    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        train_loss += loss.item()
    
    avg_train_loss = train_loss / len(train_loader)
    train_losses.append(avg_train_loss)
    
    # ইভালুয়েট
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            predictions = model(batch_X)
            test_loss += criterion(predictions, batch_y).item()
    
    avg_test_loss = test_loss / len(test_loader)
    test_losses.append(avg_test_loss)
    
    scheduler.step(avg_test_loss)
    
    # বেস্ট মডেল সেভ
    if avg_test_loss < best_test_loss:
        best_test_loss = avg_test_loss
        torch.save(model.state_dict(), 'best_ts_model.pt')
    
    if (epoch + 1) % 15 == 0:
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.6f} | Test Loss: {avg_test_loss:.6f}")

print(f"\n✅ সেরা Test Loss: {best_test_loss:.6f}")
```

## 5. প্রেডিকশন ও ভিজুয়ালাইজেশন

```python
# বেস্ট মডেল লোড
model.load_state_dict(torch.load('best_ts_model.pt'))
model.eval()

# প্রেডিকশন
with torch.no_grad():
    X_test_tensor = torch.FloatTensor(X_test).to(device)
    predictions = model(X_test_tensor).cpu().numpy()

# আনস্কেল
predictions_actual = tgt_scaler.inverse_transform(predictions)
y_test_actual = tgt_scaler.inverse_transform(y_test)

# পারফরম্যান্স মেট্রিক্স
mse = np.mean((predictions_actual - y_test_actual) ** 2)
mae = np.mean(np.abs(predictions_actual - y_test_actual))
mape = np.mean(np.abs((predictions_actual - y_test_actual) / y_test_actual)) * 100
r2 = 1 - np.sum((predictions_actual - y_test_actual)**2) / \
          np.sum((y_test_actual - np.mean(y_test_actual))**2)

print(f"{'মেট্রিক':<20} {'মান':<15}")
print("-" * 35)
print(f"{'MSE':<20} {mse:<15.4f}")
print(f"{'RMSE':<20} {np.sqrt(mse):<15.4f}")
print(f"{'MAE':<20} {mae:<15.4f}")
print(f"{'MAPE':<20} {mape:<15.2f}%")
print(f"{'R² Score':<20} {r2:<15.4f}")

# ভিজুয়ালাইজেশন
plt.figure(figsize=(14, 6))
plt.plot(y_test_actual[:100], label='আসল মান', linewidth=2)
plt.plot(predictions_actual[:100], label='প্রেডিকশন', linewidth=2, linestyle='--')
plt.title('LSTM টাইম সিরিজ ফোরকাস্টিং (প্রথম ১০০ টেস্ট পয়েন্ট)')
plt.xlabel('টাইম স্টেপ')
plt.ylabel('ভ্যালু')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 6. মাল্টি-স্টেপ ফোরকাস্টিং

```python
def multi_step_forecast(model, initial_seq, n_steps, feature_scaler, target_scaler, n_features):
    """মাল্টি-স্টেপ ফরওয়ার্ড ফোরকাস্ট"""
    model.eval()
    current_seq = initial_seq.copy()  # (seq_len, n_features)
    forecasts = []
    
    with torch.no_grad():
        for _ in range(n_steps):
            # প্রেডিক্ট
            x_tensor = torch.FloatTensor(current_seq).unsqueeze(0).to(device)
            pred = model(x_tensor).cpu().numpy()[0, 0]
            
            # আনস্কেল
            pred_actual = target_scaler.inverse_transform([[pred]])[0, 0]
            forecasts.append(pred_actual)
            
            # সিকোয়েন্স আপডেট (পরবর্তী স্টেপের জন্য)
            new_step = current_seq[-1].copy()
            new_step[0] = pred  # value আপডেট
            current_seq = np.vstack([current_seq[1:], new_step])
    
    return np.array(forecasts)

# ফোরকাস্ট
initial = X_test[0]  # প্রথম টেস্ট সিকোয়েন্স
forecast_30 = multi_step_forecast(model, initial, n_steps=30,
                                   feat_scaler, tgt_scaler, len(features))

print(f"৩০-দিনের ফোরকাস্ট:\n{forecast_30}")
print(f"শেষ প্রেডিক্টেড ভ্যালু: {forecast_30[-1]:.2f}")
```

## 7. মডেল সেভ ও লোড

```python
import pickle

# সম্পূর্ণ মডেল সেভ
torch.save({
    'model_state_dict': model.state_dict(),
    'input_size': len(features),
    'hidden_size': 128,
    'num_layers': 2,
    'feature_scaler': feat_scaler,
    'target_scaler': tgt_scaler,
    'features': features,
}, 'ts_lstm_complete.pth')

print("✅ মডেল সেভ করা হয়েছে: ts_lstm_complete.pth")

# মডেল লোড
def load_ts_model(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    model = TimeSeriesLSTM(
        input_size=checkpoint['input_size'],
        hidden_size=checkpoint['hidden_size'],
        num_layers=checkpoint['num_layers']
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    return model, checkpoint

loaded_model, ckpt = load_ts_model('ts_lstm_complete.pth')
print(f"✅ মডেল লোড করা হয়েছে (input_size={ckpt['input_size']})")
```

## টাইম সিরিজ বেস্ট প্র্যাকটিস

### 1. ডেটা প্রিপ্রসেসিং
- স্টেশনারিটি চেক (ADF টেস্ট)
- ডিফারেন্সিং যদি নন-স্টেশনারি
- আউটলায়ার হ্যান্ডলিং
- মিসিং ভ্যালু ইম্পিউটেশন

### 2. ফিচার ইঞ্জিনিয়ারিং
- Lag features
- Rolling statistics
- Date/Time features (দিন, মাস, কোয়ার্টার)
- টেকনিক্যাল ইন্ডিকেটর

### 3. মডেলিং
- Walk-forward validation
- Early stopping
- Learning rate scheduling
- Gradient clipping

```python
# ADF টেস্ট
from statsmodels.tsa.stattools import adfuller

def check_stationarity(series):
    result = adfuller(series.dropna())
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    if result[1] <= 0.05:
        print("✅ ডেটা স্টেশনারি (p <= 0.05)")
    else:
        print("❌ ডেটা নন-স্টেশনারি, ডিফারেন্সিং প্রয়োজন")

check_stationarity(df['value'])
```

## সারাংশ
- LSTM টাইম সিরিজ ফোরকাস্টিংয়ে অত্যন্ত কার্যকর
- মাল্টি-ভেরিয়েট ইনপুট সাপোর্ট করে
- মাল্টি-স্টেপ ফোরকাস্টিং সম্ভব
- সঠিক ডেটা প্রিপ্রসেসিং গুরুত্বপূর্ণ
- ওয়াক-ফরোয়ার্ড ভ্যালিডেশন বেস্ট প্র্যাকটিস
- ফিন্যান্সে স্টক, ফরেক্স, ভলাটিলিটি প্রেডিকশনে ব্যবহৃত