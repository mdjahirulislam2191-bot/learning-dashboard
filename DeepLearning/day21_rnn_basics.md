# Day 21: RNN (Recurrent Neural Network) বেসিক 🔄

## RNN কী?
RNN হল এমন এক ধরণের নিউরাল নেটওয়ার্ক যা সিকোয়েন্সিয়াল ডেটা প্রসেস করতে পারে। এতে প্রতিটি স্টেপের আউটপুট আগের স্টেপের উপর নির্ভরশীল।

### RNN-এর মূল বৈশিষ্ট্য
- **Hidden State**: আগের তথ্য ধরে রাখে
- **Weight Sharing**: প্রতি টাইমস্টেপে একই ওয়েট ব্যবহার করা হয়
- **Sequential Processing**: ডেটা ক্রমানুসারে প্রসেস হয়

### ফিন্যান্সে ব্যবহার
- স্টক প্রাইস প্রেডিকশন
- টাইম সিরিজ ফোরকাস্টিং
- ভলাটিলিটি মডেলিং

## RNN আর্কিটেকচার
```
Output:    y1        y2        y3
           ↑         ↑         ↑
RNN:     [h0]→[h1]→[h2]→[h3]→...
           ↑         ↑         ↑
Input:    x1        x2        x3
```

h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)

## Pure Python-এ RNN ইমপ্লিমেন্টেশন

```python
import numpy as np

class RNN:
    """সিম্পল RNN ইমপ্লিমেন্টেশন"""
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        
        # ওয়েট ম্যাট্রিক্স
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.01  # ইনপুট→হিডেন
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01  # হিডেন→হিডেন
        self.Why = np.random.randn(output_size, hidden_size) * 0.01  # হিডেন→আউটপুট
        self.bh = np.zeros((hidden_size, 1))   # হিডেন বায়াস
        self.by = np.zeros((output_size, 1))   # আউটপুট বায়াস
    
    def forward(self, inputs):
        """ফরওয়ার্ড প্রপাগেশন"""
        h = np.zeros((self.hidden_size, 1))  # ইনিশিয়াল হিডেন স্টেট
        hs, ys = [], []
        
        for x in inputs:
            x = x.reshape(-1, 1)
            # হিডেন স্টেট আপডেট
            h = np.tanh(np.dot(self.Wxh, x) + np.dot(self.Whh, h) + self.bh)
            # আউটপুট
            y = np.dot(self.Why, h) + self.by
            hs.append(h)
            ys.append(y)
        
        return np.array(ys), np.array(hs)

# টেস্ট
np.random.seed(42)
rnn = RNN(input_size=3, hidden_size=5, output_size=1)
inputs = [np.array([0.5, 0.2, 0.8]) for _ in range(10)]
outputs, _ = rnn.forward(inputs)
print(f"RNN আউটপুট শেপ: {outputs.shape}")
print(f"প্রথম ৩ আউটপুট:\n{outputs[:3].flatten()}")
```

## PyTorch-এ RNN

```python
import torch
import torch.nn as nn

class SimpleRNN(nn.Module):
    """PyTorch RNN মডেল"""
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # x: (batch, seq_len, input_size)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, hidden = self.rnn(x, h0)
        # out: (batch, seq_len, hidden_size)
        # শুধু লাস্ট টাইমস্টেপের আউটপুট নিচ্ছি
        out = self.fc(out[:, -1, :])
        return out

# টেস্ট
model = SimpleRNN(input_size=1, hidden_size=32, output_size=1)
x = torch.randn(16, 10, 1)  # batch=16, seq_len=10, features=1
y = model(x)
print(f"ইনপুট শেপ: {x.shape}")
print(f"আউটপুট শেপ: {y.shape}")
```

## সিন্থেটিক টাইম সিরিজ ডেটা

```python
import numpy as np
import matplotlib.pyplot as plt

def generate_sine_wave_data(seq_length=20, num_samples=1000):
    """সাইন ওয়েভ ডেটা জেনারেট"""
    X, y = [], []
    t = np.linspace(0, 50 * np.pi, num_samples + seq_length)
    data = np.sin(t) + 0.1 * np.random.randn(num_samples + seq_length)
    
    for i in range(num_samples):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    
    return np.array(X), np.array(y)

X, y = generate_sine_wave_data(seq_length=20, num_samples=500)
print(f"X শেপ: {X.shape}, y শেপ: {y.shape}")

# ডেটা ভিজুয়ালাইজ
plt.figure(figsize=(12, 4))
plt.plot(X[0], label='ইনপুট সিকোয়েন্স')
plt.axhline(y=y[0], color='r', linestyle='--', label='টার্গেট')
plt.title('টাইম সিরিজ ডেটা')
plt.legend()
plt.show()
```

## RNN ট্রেনিং: টেম্পারেচার ফোরকাস্টিং

```python
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ডেটা প্রস্তুতি
X_tensor = torch.FloatTensor(X).unsqueeze(-1)  # (samples, seq_len, 1)
y_tensor = torch.FloatTensor(y).unsqueeze(-1)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# মডেল
model = SimpleRNN(input_size=1, hidden_size=32, output_size=1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

# ট্রেনিং
epochs = 50
for epoch in range(epochs):
    total_loss = 0
    for batch_X, batch_y in loader:
        optimizer.zero_grad()
        pred = model(batch_X)
        loss = criterion(pred, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")

print("✅ RNN ট্রেনিং সম্পূর্ণ!")
```

## RNN-এর সীমাবদ্ধতা
1. **Vanishing Gradient**: দীর্ঘ সিকোয়েন্সে গ্র্যাডিয়েন্ট ছোট হয়ে যায়
2. **Long-term Dependency**: অনেক আগের তথ্য মনে রাখতে পারে না
3. **Sequential Training**: প্যারালালাইজ করা কঠিন

এর সমাধান হলো LSTM ও GRU যা আমরা পরবর্তী লেসনে দেখব।

## সারাংশ
- RNN সিকোয়েন্সিয়াল ডেটার জন্য ডিজাইন করা
- হিডেন স্টেটের মাধ্যমে টাইমস্টেপের তথ্য সংরক্ষণ
- ফিন্যান্সে টাইম সিরিজ ও স্টক প্রেডিকশনে ব্যবহৃত
- Vanishing gradient সমস্যার কারণে LSTM/GRU বেশি জনপ্রিয়