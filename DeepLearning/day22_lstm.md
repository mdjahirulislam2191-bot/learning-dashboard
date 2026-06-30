# Day 22: LSTM (Long Short-Term Memory) 🧠

## LSTM কী?
LSTM হল RNN-এর একটি উন্নত ভার্সন যা দীর্ঘমেয়াদী ডিপেন্ডেন্সি মনে রাখতে পারে। এটি vanishing gradient সমস্যার সমাধান করে।

### LSTM vs সাধারণ RNN
| বৈশিষ্ট্য | RNN | LSTM |
|---|---|---|
| Hidden State | 1টি | 2টি (h, c) |
| Gates | না | 3টি (forget, input, output) |
| Long-term memory | দুর্বল | শক্তিশালী |
| Vanishing gradient | সমস্যা | সমাধান |

### LSTM-এর সেল স্টেট
LSTM-এ তিনটি গেট থাকে:
1. **Forget Gate (f)**: কোন তথ্য ভুলে যেতে হবে
2. **Input Gate (i)**: নতুন কোন তথ্য সংরক্ষণ করতে হবে
3. **Output Gate (o)**: আউটপুট কী হবে

## LSTM গণিত
```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)    # Forget gate
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)    # Input gate
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C) # Candidate cell state
C_t = f_t * C_{t-1} + i_t * C̃_t          # Cell state update
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)    # Output gate
h_t = o_t * tanh(C_t)                    # Hidden state
```

## Pure Python-এ LSTM

```python
import numpy as np

class LSTM:
    """সিম্পল LSTM ইমপ্লিমেন্টেশন"""
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        
        # Forget gate
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bf = np.zeros((hidden_size, 1))
        
        # Input gate
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bi = np.zeros((hidden_size, 1))
        
        # Cell state
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bc = np.zeros((hidden_size, 1))
        
        # Output gate
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bo = np.zeros((hidden_size, 1))
    
    def forward(self, x):
        """ফরওয়ার্ড প্রপাগেশন"""
        h = np.zeros((self.hidden_size, 1))
        c = np.zeros((self.hidden_size, 1))
        
        for t in range(len(x)):
            xt = x[t].reshape(-1, 1)
            concat = np.vstack((h, xt))
            
            f = self._sigmoid(np.dot(self.Wf, concat) + self.bf)
            i = self._sigmoid(np.dot(self.Wi, concat) + self.bi)
            c_candidate = np.tanh(np.dot(self.Wc, concat) + self.bc)
            o = self._sigmoid(np.dot(self.Wo, concat) + self.bo)
            
            c = f * c + i * c_candidate
            h = o * np.tanh(c)
        
        return h.flatten()
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# টেস্ট
np.random.seed(42)
lstm = LSTM(input_size=3, hidden_size=5)
x = [np.random.randn(3) for _ in range(10)]
output = lstm.forward(x)
print(f"LSTM আউটপুট: {output}")
print(f"আউটপুট শেপ: {output.shape}")
```

## PyTorch-এ LSTM মডেল

```python
import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    """PyTorch LSTM মডেল - স্টক প্রাইস প্রেডিকশনের জন্য"""
    def __init__(self, input_size=1, hidden_size=128, num_layers=2, output_size=1, dropout=0.3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=False
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # x: (batch, seq_len, input_size)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, (hn, cn) = self.lstm(x, (h0, c0))
        # লাস্ট টাইমস্টেপ
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        return out

# মডেল চেক
model = LSTMModel(input_size=5, hidden_size=64, num_layers=2, output_size=1)
x = torch.randn(32, 20, 5)  # batch=32, seq_len=20, features=5
y = model(x)
print(f"ইনপুট: {x.shape} → আউটপুট: {y.shape}")
print(f"মডেল প্যারামিটার: {sum(p.numel() for p in model.parameters()):,}")
```

## মাল্টি-ফিচার স্টক ডেটা

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# সিন্থেটিক স্টক ডেটা
np.random.seed(42)
n_days = 1000

data = pd.DataFrame({
    'open': np.cumsum(np.random.randn(n_days) * 0.5) + 100,
    'high': np.zeros(n_days),
    'low': np.zeros(n_days),
    'close': np.zeros(n_days),
    'volume': np.random.randint(1000000, 10000000, n_days)
})

# OHLC জেনারেট
for i in range(n_days):
    daily_range = np.random.uniform(0.5, 2.0)
    data.loc[i, 'high'] = max(data.loc[i, 'open'], data.loc[i-1, 'close'] if i > 0 else data.loc[i, 'open']) + daily_range
    data.loc[i, 'low'] = min(data.loc[i, 'open'], data.loc[i-1, 'close'] if i > 0 else data.loc[i, 'open']) - daily_range
    data.loc[i, 'close'] = np.random.uniform(data.loc[i, 'low'], data.loc[i, 'high'])

# ফিচার ইঞ্জিনিয়ারিং
data['returns'] = data['close'].pct_change()
data['range'] = data['high'] - data['low']
data['sma_5'] = data['close'].rolling(5).mean()
data['sma_20'] = data['close'].rolling(20).mean()

print(data.head())
print(f"ডেটা শেপ: {data.shape}")
```

## LSTM ডেটা প্রিপ্রসেসিং

```python
def create_sequences(data, seq_length=20):
    """LSTM-এর জন্য সিকোয়েন্স ডেটা তৈরি"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, 0])  # ক্লোজ প্রাইস টার্গেট
    return np.array(X), np.array(y)

# ফিচার সিলেক্ট ও স্কেল
features = ['open', 'high', 'low', 'close', 'volume', 'returns', 'range']
feature_data = data[features].dropna().values

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

scaled_data = scaler_X.fit_transform(feature_data)
close_scaled = scaler_y.fit_transform(feature_data[:, 3].reshape(-1, 1))

# X, y ডেটা
X, y = create_sequences(scaled_data, seq_length=20)
print(f"X শেপ: {X.shape}, y শেপ: {y.shape}")

# ট্রেন-টেস্ট স্প্লিট
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"ট্রেন: {X_train.shape}, টেস্ট: {X_test.shape}")
```

## LSTM ট্রেনিং

```python
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# টেন্সরে রূপান্তর
X_train_t = torch.FloatTensor(X_train)
y_train_t = torch.FloatTensor(y_train).unsqueeze(1)
X_test_t = torch.FloatTensor(X_test)
y_test_t = torch.FloatTensor(y_test).unsqueeze(1)

# DataLoader
train_dataset = TensorDataset(X_train_t, y_train_t)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# মডেল
model = LSTMModel(input_size=X.shape[2], hidden_size=64, num_layers=2, output_size=1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ট্রেনিং লুপ
epochs = 100
for epoch in range(epochs):
    model.train()
    total_loss = 0
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # গ্র্যাডিয়েন্ট ক্লিপিং
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")

# ইভালুয়েশন
model.eval()
with torch.no_grad():
    train_pred = model(X_train_t)
    test_pred = model(X_test_t)
    train_loss = criterion(train_pred, y_train_t)
    test_loss = criterion(test_pred, y_test_t)
    print(f"\n✅ Train MSE: {train_loss:.6f}")
    print(f"✅ Test MSE: {test_loss:.6f}")

# প্রেডিকশন আনস্কেল
train_pred_actual = scaler_y.inverse_transform(train_pred.numpy())
test_pred_actual = scaler_y.inverse_transform(test_pred.numpy())
y_test_actual = scaler_y.inverse_transform(y_test_t.numpy())

print(f"প্রথম ৫ প্রেডিকশন: {test_pred_actual[:5].flatten()}")
print(f"প্রথম ৫ আসল মান: {y_test_actual[:5].flatten()}")
```

## LSTM হাইপারপ্যারামিটার টিউনিং

```python
# বিভিন্ন হাইপারপ্যারামিটার টেস্ট
configs = [
    {"hidden_size": 32, "num_layers": 1, "lr": 0.01},
    {"hidden_size": 64, "num_layers": 2, "lr": 0.001},
    {"hidden_size": 128, "num_layers": 2, "lr": 0.001},
    {"hidden_size": 64, "num_layers": 3, "lr": 0.0005},
]

results = []
for config in configs:
    model = LSTMModel(
        input_size=X.shape[2],
        hidden_size=config["hidden_size"],
        num_layers=config["num_layers"],
        output_size=1
    )
    optimizer = optim.Adam(model.parameters(), lr=config["lr"])
    
    # ২০ ইপক ট্রেইন
    for epoch in range(20):
        model.train()
        for bx, by in train_loader:
            optimizer.zero_grad()
            loss = nn.MSELoss()(model(bx), by)
            loss.backward()
            optimizer.step()
    
    model.eval()
    with torch.no_grad():
        test_loss = nn.MSELoss()(model(X_test_t), y_test_t).item()
    
    results.append({**config, "test_loss": test_loss})
    print(f"Config {config}: Test MSE = {test_loss:.6f}")

best = min(results, key=lambda r: r["test_loss"])
print(f"\n🏆 সেরা কনফিগ: hidden_size={best['hidden_size']}, "
      f"layers={best['num_layers']}, lr={best['lr']}, loss={best['test_loss']:.6f}")
```

## সারাংশ
- LSTM vanishing gradient সমস্যার সমাধান করে
- থ্রি গেট সিস্টেম: forget, input, output
- ফিন্যান্সে টাইম সিরিজ ফোরকাস্টিংয়ে বহুল ব্যবহৃত
- স্টক প্রাইস, ভলাটিলিটি, রিস্ক ম্যানেজমেন্টে অ্যাপ্লিকেশন
- হাইপারপ্যারামিটার টিউনিং পারফরম্যান্সের জন্য গুরুত্বপূর্ণ