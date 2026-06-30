# Day 23: GRU (Gated Recurrent Unit) 🚀

## GRU কী?
GRU হল LSTM-এর একটি সিম্পলিফাইড ভার্সন যা কম প্যারামিটার ব্যবহার করে অনুরূপ পারফরম্যান্স দেয়। এটি ২০১৪ সালে Kyunghyun Cho প্রস্তাব করেন।

### GRU vs LSTM
| বৈশিষ্ট্য | LSTM | GRU |
|---|---|---|
| Gates | 3 (forget, input, output) | 2 (reset, update) |
| Cell State | আলাদা (c) | নেই, শুধু hidden state |
| Parameters | বেশি | ~33% কম |
| Computation | ধীর | দ্রুত |
| Performance | জটিল ডেটাতে ভালো | ছোট ডেটাসেটে ভালো |

### GRU-এর গেটসমূহ
1. **Reset Gate (r)**: আগের তথ্য কতটা ভুলে যেতে হবে
2. **Update Gate (z)**: কতটা নতুন তথ্য যোগ করতে হবে

## GRU গণিত
```
z_t = σ(W_z · [h_{t-1}, x_t])       # Update gate
r_t = σ(W_r · [h_{t-1}, x_t])       # Reset gate
h̃_t = tanh(W · [r_t * h_{t-1}, x_t]) # Candidate hidden state
h_t = (1 - z_t) * h_{t-1} + z_t * h̃_t # Final hidden state
```

## Pure Python-এ GRU

```python
import numpy as np

class GRU:
    """সিম্পল GRU ইমপ্লিমেন্টেশন"""
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        
        # Update gate
        self.Wz = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bz = np.zeros((hidden_size, 1))
        
        # Reset gate
        self.Wr = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.br = np.zeros((hidden_size, 1))
        
        # Candidate hidden state
        self.Wh = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.bh = np.zeros((hidden_size, 1))
    
    def forward(self, x):
        """ফরওয়ার্ড প্রপাগেশন"""
        h = np.zeros((self.hidden_size, 1))
        
        for t in range(len(x)):
            xt = x[t].reshape(-1, 1)
            concat = np.vstack((h, xt))
            
            z = self._sigmoid(np.dot(self.Wz, concat) + self.bz)
            r = self._sigmoid(np.dot(self.Wr, concat) + self.br)
            
            # Reset gate applied
            r_h = r * h
            concat_r = np.vstack((r_h, xt))
            h_candidate = np.tanh(np.dot(self.Wh, concat_r) + self.bh)
            
            h = (1 - z) * h + z * h_candidate
        
        return h.flatten()
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# টেস্ট
np.random.seed(42)
gru = GRU(input_size=3, hidden_size=5)
x = [np.random.randn(3) for _ in range(10)]
output = gru.forward(x)
print(f"GRU আউটপুট: {output}")
print(f"প্যারামিটার সংখ্যা: LSTM-এর চেয়ে ~25% কম")
```

## PyTorch-এ GRU মডেল

```python
import torch
import torch.nn as nn

class GRUModel(nn.Module):
    """PyTorch GRU মডেল"""
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1, dropout=0.3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, hidden = self.gru(x, h0)
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        return out

# মডেল কম্পেয়ার
lstm_model = nn.LSTM(input_size=5, hidden_size=64, num_layers=2, batch_first=True)
gru_model = nn.GRU(input_size=5, hidden_size=64, num_layers=2, batch_first=True)

lstm_params = sum(p.numel() for p in lstm_model.parameters())
gru_params = sum(p.numel() for p in gru_model.parameters())

print(f"LSTM প্যারামিটার: {lstm_params:,}")
print(f"GRU প্যারামিটার: {gru_params:,}")
print(f"পার্থক্য: {lstm_params - gru_params:,} ({((lstm_params-gru_params)/lstm_params*100):.1f}% কম)")
```

## GRU vs LSTM: টাইম সিরিজ বেঞ্চমার্ক

```python
import numpy as np
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import time

# সিন্থেটিক ডেটা
np.random.seed(42)
N = 2000
seq_len = 20
n_features = 3

X = np.random.randn(N, seq_len, n_features)
y = np.sin(X[:, -1, 0]) + 0.1 * np.random.randn(N)

X_t = torch.FloatTensor(X)
y_t = torch.FloatTensor(y).unsqueeze(1)

dataset = TensorDataset(X_t, y_t)
loader = DataLoader(dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(TensorDataset(X_t[:200], y_t[:200]), batch_size=64)

# উভয় মডেল ট্রেনিং
def train_model(model, name):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    start = time.time()
    for epoch in range(50):
        model.train()
        for bx, by in loader:
            optimizer.zero_grad()
            loss = criterion(model(bx), by)
            loss.backward()
            optimizer.step()
    
    elapsed = time.time() - start
    
    model.eval()
    with torch.no_grad():
        test_loss = criterion(model(X_t[:200]), y_t[:200]).item()
    
    return elapsed, test_loss

# GRU vs LSTM
gru_model = GRUModel(input_size=n_features, hidden_size=64, num_layers=2)
lstm_model = LSTMModel(input_size=n_features, hidden_size=64, num_layers=2)

gru_time, gru_loss = train_model(gru_model, "GRU")
lstm_time, lstm_loss = train_model(lstm_model, "LSTM")

print(f"{'মডেল':<10} {'সময় (সে.)':<15} {'Test MSE':<15}")
print("-" * 40)
print(f"{'GRU':<10} {gru_time:<15.4f} {gru_loss:<15.6f}")
print(f"{'LSTM':<10} {lstm_time:<15.4f} {lstm_loss:<15.6f}")
print(f"\nGRU {((lstm_time-gru_time)/lstm_time*100):.1f}% দ্রুততর")
```

## ফিন্যান্স: ভলাটিলিটি প্রেডিকশন

```python
import pandas as pd

# সিন্থেটিক ভলাটিলিটি ডেটা
np.random.seed(42)
n = 1500
returns = np.random.randn(n) * 0.02
volatility = np.zeros(n)

# GARCH-like ভলাটিলিটি
for t in range(1, n):
    volatility[t] = np.sqrt(0.0001 + 0.1 * returns[t-1]**2 + 0.85 * volatility[t-1]**2)

data = pd.DataFrame({
    'return': returns,
    'volatility': volatility,
    'abs_return': np.abs(returns),
    'squared_return': returns**2
})

# ফিচার তৈরি
features = ['abs_return', 'squared_return']
target = 'volatility'

def create_seq(data, cols, target_col, seq_len=10):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[cols].iloc[i:i+seq_len].values)
        y.append(data[target_col].iloc[i+seq_len])
    return np.array(X), np.array(y)

X_vol, y_vol = create_seq(data, features, target, seq_len=10)
print(f"ভলাটিলিটি ডেটা: X={X_vol.shape}, y={y_vol.shape}")

# GRU মডেল ট্রেনিং
X_t = torch.FloatTensor(X_vol)
y_t = torch.FloatTensor(y_vol).unsqueeze(1)

gru_vol = GRUModel(input_size=2, hidden_size=32, num_layers=1, output_size=1)
optimizer = optim.Adam(gru_vol.parameters(), lr=0.005)
criterion = nn.MSELoss()

for epoch in range(30):
    gru_vol.train()
    optimizer.zero_grad()
    loss = criterion(gru_vol(X_t[:1200]), y_t[:1200])
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.6f}")

# টেস্ট
gru_vol.eval()
with torch.no_grad():
    preds = gru_vol(X_t[1200:]).numpy().flatten()
    actuals = y_t[1200:].numpy().flatten()
    
    mae = np.mean(np.abs(preds - actuals))
    print(f"\n✅ Test MAE: {mae:.6f}")
    print(f"প্রথম ৫ প্রেডিকশন: {preds[:5]}")
    print(f"প্রথম ৫ আসল:      {actuals[:5]}")
```

## GRU-এর সুবিধা ও অসুবিধা

### সুবিধা
1. **কম প্যারামিটার** → দ্রুত ট্রেনিং, কম মেমরি
2. **ছোট ডেটাসেটে ভালো** → ওভারফিটিং কম
3. **Vanishing gradient** → LSTM-এর মতোই সমাধান
4. **সিম্পল আর্কিটেকচার** → ইমপ্লিমেন্ট করা সহজ

### অসুবিধা
1. **কম expressiveness** → কিছু জটিল প্যাটার্ন ধরতে পারে না
2. **Cell state নেই** → খুব দীর্ঘমেয়াদী মেমরি LSTM-এর চেয়ে দুর্বল

### কখন GRU ব্যবহার করবেন?
- ছোট থেকে মাঝারি ডেটাসেট
- কম্পিউটেশনাল রিসোর্স সীমিত
- ফাস্ট প্রোটোটাইপিং
- LSTM-এর সাথে ensemble করতে পারেন

```python
# Ensemble: GRU + LSTM
class GRULSTMEnsemble(nn.Module):
    """GRU + LSTM Ensemble"""
    def __init__(self, input_size, hidden_size=64, output_size=1):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size * 2, output_size)
    
    def forward(self, x):
        _, gru_h = self.gru(x)
        _, (lstm_h, _) = self.lstm(x)
        combined = torch.cat([gru_h[-1], lstm_h[-1]], dim=1)
        return self.fc(combined)

ensemble = GRULSTMEnsemble(input_size=5)
x = torch.randn(16, 10, 5)
print(f"Ensemble আউটপুট: {ensemble(x).shape}")
```

## সারাংশ
- GRU LSTM-এর সিম্পল অল্টারনেটিভ
- ২টি গেট: reset ও update
- ~33% কম প্যারামিটার, ~25% দ্রুত
- ফিন্যান্সে ভলাটিলিটি প্রেডিকশন, রিস্ক ম্যানেজমেন্টে ব্যবহৃত
- ছোট ডেটাসেট ও রিয়েল-টাইম অ্যাপ্লিকেশনের জন্য উপযুক্ত