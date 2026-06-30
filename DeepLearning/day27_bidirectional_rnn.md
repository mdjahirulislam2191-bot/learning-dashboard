# Day 27: বিডাইরেকশনাল RNN 🔄

## বিডাইরেকশনাল RNN কী?
বিডাইরেকশনাল RNN (BiRNN) দুই দিক থেকে সিকোয়েন্স প্রসেস করে - ফরওয়ার্ড ও ব্যাকওয়ার্ড। এটি কনটেক্সট উভয় দিক থেকে বুঝতে সাহায্য করে।

### আর্কিটেকচার
```
আউটপুট:      y1          y2          y3
            ↗   ↖      ↗   ↖      ↗   ↖
ফরওয়ার্ড:  →h1_f→    →h2_f→    →h3_f→
ব্যাকওয়ার্ড: ←h1_b←    ←h2_b←    ←h3_b←
            ↗   ↖      ↗   ↖      ↗   ↖
ইনপুট:      x1         x2         x3
```

ফাইনাল হিডেন স্টেট: h_t = [h_t^f; h_t^b] (কনক্যাট)

### কেন বিডাইরেকশনাল?
- NLP-তে অপরিহার্য (প্রসঙ্গ আগে-পরে বুঝতে)
- টাইম সিরিজেও ব্যাকওয়ার্ড কনটেক্সট সহায়ক
- ফিচার রিপ্রেজেন্টেশন আরও রিচ

## PyTorch-এ BiLSTM

```python
import torch
import torch.nn as nn
import numpy as np

class BiLSTMModel(nn.Module):
    """বিডাইরেকশনাল LSTM মডেল"""
    def __init__(self, input_size=5, hidden_size=64, num_layers=2, output_size=1, dropout=0.3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,  # বিডাইরেকশনাল
            dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        # বিডাইরেকশনাল → hidden_size * 2
        self.fc = nn.Linear(hidden_size * 2, output_size)
    
    def forward(self, x):
        out, (hidden, cell) = self.lstm(x)
        # হিডেন: (num_layers * 2, batch, hidden_size)
        
        # লাস্ট লেয়ারের ফরওয়ার্ড + ব্যাকওয়ার্ড
        h_f = hidden[-2, :, :]  # ফরওয়ার্ড
        h_b = hidden[-1, :, :]  # ব্যাকওয়ার্ড
        h_combined = torch.cat((h_f, h_b), dim=1)
        
        out = self.dropout(h_combined)
        out = self.fc(out)
        return out

# ইউনিডাইরেকশনাল vs বিডাইরেকশনাল
uni_model = nn.LSTM(5, 64, 2, batch_first=True)
bi_model = nn.LSTM(5, 64, 2, batch_first=True, bidirectional=True)

uni_params = sum(p.numel() for p in uni_model.parameters())
bi_params = sum(p.numel() for p in bi_model.parameters())

print(f"ইউনিডাইরেকশনাল প্যারামিটার: {uni_params:,}")
print(f"বিডাইরেকশনাল প্যারামিটার: {bi_params:,}")
print(f"পার্থক্য: {bi_params - uni_params:,} (বিডাইরেকশনাল {(bi_params/uni_params - 1)*100:.0f}% বেশি)")
```

## ফিন্যান্স: BiLSTM দিয়ে স্টক ট্রেন্ড ক্লাসিফিকেশন

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ডেটা জেনারেশন
np.random.seed(42)
n = 2000

returns = np.random.randn(n) * 0.02
price = 100 * np.exp(np.cumsum(returns))

df = pd.DataFrame({'price': price, 'returns': returns})
df['sma_10'] = df['price'].rolling(10).mean()
df['sma_30'] = df['price'].rolling(30).mean()
df['volatility'] = df['returns'].rolling(20).std()
df['rsi'] = 50 + np.random.randn(n) * 10

# ট্রেন্ড লেবেল (৩ ক্লাস: আপ/ডাউন/নিউট্রাল)
df['future_return'] = df['price'].pct_change(5).shift(-5)
df['trend'] = pd.cut(df['future_return'], 
                     bins=[-np.inf, -0.02, 0.02, np.inf],
                     labels=[0, 1, 2])  # 0=ডাউন, 1=নিউট্রাল, 2=আপ

df_clean = df.dropna()

# ফিচার
features = ['returns', 'sma_10', 'sma_30', 'volatility', 'rsi']
target = 'trend'

# সিকোয়েন্স তৈরি
seq_len = 20

def create_trend_sequences(df, features, target, seq_len):
    X, y = [], []
    data = df[features].values
    labels = df[target].values
    
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(labels[i+seq_len])
    
    return np.array(X), np.array(y)

X, y = create_trend_sequences(df_clean, features, target, seq_len)
print(f"X: {X.shape}, y: {y.shape}")
print(f"ক্লাস ডিস্ট্রিবিউশন:")
for cls in range(3):
    print(f"  ক্লাস {cls}: {(y==cls).sum()} ({((y==cls).sum()/len(y)*100):.1f}%)")
```

## BiLSTM ক্লাসিফায়ার ট্রেনিং

```python
class BiLSTMClassifier(nn.Module):
    """বিডাইরেকশনাল LSTM ক্লাসিফায়ার"""
    def __init__(self, input_size, hidden_size=128, num_layers=2, num_classes=3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, bidirectional=True,
            dropout=0.4 if num_layers > 1 else 0
        )
        self.bn = nn.BatchNorm1d(hidden_size * 2)
        self.dropout = nn.Dropout(0.4)
        self.fc1 = nn.Linear(hidden_size * 2, 64)
        self.fc2 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out, _ = self.lstm(x)
        # গ্লোবাল এভারেজ পুলিং
        out = out.mean(dim=1)  # (batch, hidden*2)
        out = self.bn(out)
        out = self.dropout(out)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out

# ডেটা প্রিপারেশন
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# স্ট্যান্ডার্ডাইজ
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
X_test_s = scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)

# Tensor
X_train_t = torch.FloatTensor(X_train_s)
y_train_t = torch.LongTensor(y_train)
X_test_t = torch.FloatTensor(X_test_s)
y_test_t = torch.LongTensor(y_test)

train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=64, shuffle=True)

# মডেল
model = BiLSTMClassifier(input_size=len(features), hidden_size=64, num_layers=2, num_classes=3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)

# ট্রেনিং
epochs = 80
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        pred = model(batch_X)
        loss = criterion(pred, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

# ইভালুয়েশন
model.eval()
with torch.no_grad():
    preds = model(X_test_t)
    _, predicted = torch.max(preds, 1)
    accuracy = (predicted == y_test_t).float().mean()
    
    from sklearn.metrics import classification_report
    print(f"\n✅ BiLSTM ট্রেন্ড ক্লাসিফিকেশন অ্যাকুরেসি: {accuracy:.4f}")
    print("\nক্লাসিফিকেশন রিপোর্ট:")
    print(classification_report(y_test, predicted.numpy(),
          target_names=['ডাউন', 'নিউট্রাল', 'আপ']))
```

## ইউনিডাইরেকশনাল vs বিডাইরেকশনাল তুলনা

```python
class UniLSTMClassifier(nn.Module):
    """ইউনিডাইরেকশনাল LSTM ক্লাসিফায়ার (তুলনার জন্য)"""
    def __init__(self, input_size, hidden_size=128, num_layers=2, num_classes=3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, bidirectional=False,
            dropout=0.4 if num_layers > 1 else 0
        )
        self.bn = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(0.4)
        self.fc1 = nn.Linear(hidden_size, 64)
        self.fc2 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = out.mean(dim=1)
        out = self.bn(out)
        out = self.dropout(out)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out

# উভয় মডেল ট্রেন
def train_and_eval(model_class, name):
    model = model_class(input_size=len(features), hidden_size=64, num_layers=2, num_classes=3)
    optimizer = optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(50):
        model.train()
        for bx, by in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(bx), by)
            loss.backward()
            optimizer.step()
    
    model.eval()
    with torch.no_grad():
        acc = (torch.argmax(model(X_test_t), 1) == y_test_t).float().mean()
    
    params = sum(p.numel() for p in model.parameters())
    return acc.item(), params

bi_acc, bi_params = train_and_eval(BiLSTMClassifier, "BiLSTM")
uni_acc, uni_params = train_and_eval(UniLSTMClassifier, "UniLSTM")

print(f"{'মডেল':<15} {'প্যারামিটার':<15} {'অ্যাকুরেসি':<15}")
print("-" * 45)
print(f"{'BiLSTM':<15} {bi_params:<15,} {bi_acc:<15.4f}")
print(f"{'UniLSTM':<15} {uni_params:<15,} {uni_acc:<15.4f}")
print(f"\nBiLSTM {(bi_acc/uni_acc - 1)*100:+.2f}% বেশি অ্যাকুরেট")
```

## অ্যাটেনশন মেকানিজম যোগ

```python
class BiLSTMWithAttention(nn.Module):
    """অ্যাটেনশন সহ বিডাইরেকশনাল LSTM"""
    def __init__(self, input_size, hidden_size=128, num_classes=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, 2, 
                           batch_first=True, bidirectional=True, dropout=0.3)
        
        # অ্যাটেনশন লেয়ার
        self.attention_weights = nn.Linear(hidden_size * 2, 1)
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # (batch, seq_len, hidden*2)
        
        # অ্যাটেনশন স্কোর
        attn_scores = self.attention_weights(lstm_out)  # (batch, seq_len, 1)
        attn_weights = torch.softmax(attn_scores, dim=1)
        
        # ওয়েটেড সাম
        context = torch.sum(attn_weights * lstm_out, dim=1)
        
        out = self.dropout(context)
        out = self.fc(out)
        return out

# অ্যাটেনশন ভিজুয়ালাইজেশন
model_attn = BiLSTMWithAttention(input_size=len(features), hidden_size=64, num_classes=3)
model_attn.eval()

with torch.no_grad():
    # ফরওয়ার্ড পাস
    lstm_out, _ = model_attn.lstm(X_test_t[:1])
    attn_scores = model_attn.attention_weights(lstm_out)
    attn_weights = torch.softmax(attn_scores, dim=1).squeeze(-1)
    
    print(f"অ্যাটেনশন ওয়েট শেপ: {attn_weights.shape}")
    print(f"প্রথম সিকোয়েন্সের অ্যাটেনশন ওয়েটস (প্রথম ১০):")
    print(attn_weights[0, :10].numpy().round(3))
```

## কখন বিডাইরেকশনাল ব্যবহার করবেন?

### সুবিধা
✅ ফরোয়ার্ড + ব্যাকওয়ার্ড কনটেক্সট ক্যাপচার
✅ ফিচার রিপ্রেজেন্টেশন আরও সমৃদ্ধ
✅ NLP টাস্কে (সেন্টিমেন্ট, NER) বেস্ট পারফরম্যান্স
✅ ট্রেন্ড ক্লাসিফিকেশনে ইউজফুল

### অসুবিধা
❌ প্যারামিটার দ্বিগুণ (ধীর ট্রেনিং)
❌ ইনফারেন্স সময় বেশি লাগে
❌ লুক-অ্যাহেড প্রয়োজন (রিয়েল-টাইমে সমস্যা)
❌ টাইম সিরিজ ফোরকাস্টিংয়ে সীমিত ব্যবহার

### ফিন্যান্সে ব্যবহার
```python
# রিয়েল-টাইম ফোরকাস্টিং: ইউনিডাইরেকশনাল ভালো
# ট্রেন্ড ক্লাসিফিকেশন: বিডাইরেকশনাল ভালো
# সেন্টিমেন্ট অ্যানালাইসিস: বিডাইরেকশনাল ব্যবহার করুন
# রিস্ক অ্যানালাইসিস (নন-রিয়েল-টাইম): বিডাইরেকশনাল

print("✅ বিডাইরেকশনাল RNN বোঝা ও ইমপ্লিমেন্ট করা সম্পূর্ণ")
```

## সারাংশ
- বিডাইরেকশনাল RNN দুই দিক থেকে সিকোয়েন্স প্রসেস করে
- ফিচার রিপ্রেজেন্টেশন আরও শক্তিশালী
- ফিন্যান্সে ট্রেন্ড ক্লাসিফিকেশন ও সেন্টিমেন্টে কার্যকর
- প্যারামিটার দ্বিগুণ - কম্পিউটেশন খরচ বেশি
- রিয়েল-টাইম অ্যাপ্লিকেশনে ইউনিডাইরেকশনাল প্রেফারেবল
- অ্যাটেনশনের সাথে কম্বিনেশন আরও শক্তিশালী