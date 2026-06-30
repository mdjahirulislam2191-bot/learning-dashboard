# Day 07: প্রথম নিউরাল নেটওয়ার্ক তৈরি 🏗️

## প্রথম ANN মডেল
PyTorch দিয়ে একটি সম্পূর্ণ নিউরাল নেটওয়ার্ক তৈরি করা

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# ডিভাইস সেটআপ
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using: {device}")
```

## ১. নেটওয়ার্ক ডিফাইন
```python
class FirstNN(nn.Module):
    """আমাদের প্রথম নিউরাল নেটওয়ার্ক"""
    def __init__(self, input_size=4, hidden_size=10, output_size=1):
        super(FirstNN, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.sigmoid(self.layer2(x))
        return x

model = FirstNN().to(device)
print(model)
```

## ২. ফিন্যান্সিয়াল ডেটা তৈরি
```python
# স্টক মার্কেট ডেটা সিমুলেশন
np.random.seed(42)
n_samples = 1000

# ফিচার: ভোলাটিলিটি, RSI, SMA_ratio, Volume_change
X = np.random.randn(n_samples, 4)
# টার্গেট: প্রাইস আপ (১) বা ডাউন (০)
y = (X[:, 0] * 0.3 + X[:, 1] * 0.2 - X[:, 2] * 0.1 + 
     X[:, 3] * 0.1 + np.random.randn(n_samples) * 0.1 > 0).astype(np.float32)

# ট্রেন-টেস্ট স্প্লিট
split = int(0.8 * n_samples)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# টেনসরে রূপান্তর
X_train_t = torch.FloatTensor(X_train).to(device)
y_train_t = torch.FloatTensor(y_train).view(-1, 1).to(device)
X_test_t = torch.FloatTensor(X_test).to(device)
y_test_t = torch.FloatTensor(y_test).view(-1, 1).to(device)
```

## ৩. ট্রেনিং লুপ
```python
# লস ফাংশন ও অপ্টিমাইজার
criterion = nn.BCELoss()  # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ট্রেনিং
epochs = 500
train_losses = []

for epoch in range(epochs):
    model.train()
    
    # ফরোয়ার্ড
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    
    # ব্যাকওয়ার্ড
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    train_losses.append(loss.item())
    
    if (epoch + 1) % 100 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

# লস ভিজুয়ালাইজ
plt.plot(train_losses)
plt.title("ট্রেনিং লস")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()
```

## ৪. ইভালুয়েশন
```python
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_t)
    test_preds = (test_outputs > 0.5).float()
    accuracy = (test_preds == y_test_t).float().mean()
    
    print(f"টেস্ট অ্যাকুরেসি: {accuracy.item():.2%}")

# কনফিউশন ম্যাট্রিক্স
from sklearn.metrics import confusion_matrix, classification_report

y_true = y_test_t.cpu().numpy()
y_pred = test_preds.cpu().numpy()
cm = confusion_matrix(y_true, y_pred)
print("কনফিউশন ম্যাট্রিক্স:")
print(cm)
print("\nক্লাসিফিকেশন রিপোর্ট:")
print(classification_report(y_true, y_pred, target_names=['Down', 'Up']))
```

## ৫. রিয়েল মার্কেট ডেটা টেস্ট
```python
import yfinance as yf

def train_on_real_data(ticker="AAPL"):
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    
    # টেকনিক্যাল ইন্ডিকেটর
    data['SMA_10'] = data['Close'].rolling(10).mean()
    data['SMA_50'] = data['Close'].rolling(50).mean()
    data['Volatility'] = data['Close'].pct_change().rolling(10).std()
    data['Volume_Ratio'] = data['Volume'] / data['Volume'].rolling(10).mean()
    data['Return'] = data['Close'].pct_change()
    data['Target'] = (data['Return'].shift(-1) > 0).astype(float)
    
    data = data.dropna()
    
    features = data[['SMA_10', 'SMA_50', 'Volatility', 'Volume_Ratio']].values
    targets = data['Target'].values
    
    # স্ট্যান্ডার্ডাইজ
    mean, std = features.mean(axis=0), features.std(axis=0)
    features = (features - mean) / std
    
    # স্প্লিট
    split = int(0.8 * len(features))
    X_tr, X_te = features[:split], features[split:]
    y_tr, y_te = targets[:split], targets[split:]
    
    # টেনসর
    X_tr_t = torch.FloatTensor(X_tr).to(device)
    y_tr_t = torch.FloatTensor(y_tr).view(-1, 1).to(device)
    X_te_t = torch.FloatTensor(X_te).to(device)
    y_te_t = torch.FloatTensor(y_te).view(-1, 1).to(device)
    
    # মডেল
    model = FirstNN(input_size=4, hidden_size=16).to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # ট্রেনিং
    for epoch in range(200):
        model.train()
        out = model(X_tr_t)
        loss = criterion(out, y_tr_t)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # টেস্ট
    model.eval()
    with torch.no_grad():
        preds = (model(X_te_t) > 0.5).float()
        acc = (preds == y_te_t).float().mean()
    
    print(f"{ticker} প্রেডিকশন অ্যাকুরেসি: {acc.item():.2%}")
    return model

# নোট: রিয়েল ডেটা দিয়ে চালাতে চাইলে:
# m = train_on_real_data("AAPL")
```

## সারসংক্ষেপ
- `nn.Module` দিয়ে নেটওয়ার্ক ডিফাইন
- ফরোয়ার্ড মেথড ইমপ্লিমেন্ট
- Loss function + Optimizer সিলেক্ট
- ট্রেনিং লুপ: forward → backward → step
- ইভালুয়েশন: accuracy, confusion matrix
- ফিন্যান্স: BCELoss (binary) বা MSELoss (regression)