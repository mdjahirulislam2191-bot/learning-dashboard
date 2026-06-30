# Day 13: রেগুলারাইজেশন (Dropout, BatchNorm, L2) 🛡️

## রেগুলারাইজেশন কেন প্রয়োজন?
ওভারফিটিং প্রতিরোধ করার জন্য রেগুলারাইজেশন ব্যবহার করা হয়। ওভারফিটিং = ট্রেনিং ডেটায় ভালো কিন্তু টেস্ট ডেটায় খারাপ।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## ১. Dropout
Dropout ট্রেনিংয়ের সময় র্যান্ডমলি কিছু নিউরন বন্ধ করে দেয়।

```python
class DropoutDemo(nn.Module):
    """Dropout সহ মডেল"""
    def __init__(self, dropout_rate=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),  # 30% নিউরন বন্ধ
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        return self.net(x)

# Dropout ট্রেনিং বনাম ইভালুয়েশন মোড
model = DropoutDemo(0.5)
x = torch.randn(1, 20)

model.train()
out_train = model(x)
print(f"Train mode output: {out_train}")

model.eval()
out_eval = model(x)
print(f"Eval mode output: {out_eval}")
# Eval mode এ dropout বন্ধ থাকে
```

## ২. Batch Normalization
BatchNorm প্রতিটি মিনি-ব্যাচের আউটপুট নরমালাইজ করে।

```python
class BatchNormDemo(nn.Module):
    """BatchNorm সহ মডেল"""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 64),
            nn.BatchNorm1d(64),  # মিন-০, স্ট্যান্ডার্ড ডেভিয়েশন-১
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        return self.net(x)

# BatchNorm প্যারামিটার
model = BatchNormDemo()
x = torch.randn(32, 20)  # batch_size=32
out = model(x)

# BatchNorm লেয়ারের প্যারামিটার দেখুন
for name, param in model.named_parameters():
    if 'weight' in name or 'bias' in name:
        print(f"{name}: shape={param.shape}")

# BatchNorm ট্র্যাক করে: running_mean, running_var
print(f"\nBatchNorm running_mean: {model.net[1].running_mean}")
print(f"BatchNorm running_var: {model.net[1].running_var}")
```

## ৩. L2 Regularization (Weight Decay)
লার্জ ওয়েট পিনালাইজ করে মডেলকে সিম্পল রাখে।

```python
# L2 রেগুলারাইজেশন সহ ট্রেনিং
model = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 1))

# Weight Decay = L2 রেগুলারাইজেশন
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)
# loss = original_loss + 0.01 * Σ(w²)

# ম্যানুয়াল L2
l2_lambda = 0.01
def l2_penalty(model):
    return l2_lambda * sum(p.pow(2).sum() for p in model.parameters())

# ট্রেনিং লুপে:
# loss = criterion(output, target) + l2_penalty(model)
# loss.backward()
```

## ৪. তুলনা: Regularization Effects
```python
def compare_regularization():
    """বিভিন্ন রেগুলারাইজেশন পদ্ধতি তুলনা"""
    np.random.seed(42)
    torch.manual_seed(42)
    
    # নয়েজি ডেটা (ওভারফিট প্রবণ)
    X = np.random.randn(200, 10)
    y = (np.sin(X[:, 0]) + 0.5 * X[:, 1] + 0.3 * X[:, 2] + 
         np.random.randn(200) * 0.3).reshape(-1, 1)
    
    X_t = torch.FloatTensor(X)
    y_t = torch.FloatTensor(y)
    
    # বিভিন্ন মডেল
    models = {
        'No Regularization': nn.Sequential(
            nn.Linear(10, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        ),
        'Dropout (0.5)': nn.Sequential(
            nn.Linear(10, 128), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(128, 64), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(64, 1)
        ),
        'BatchNorm': nn.Sequential(
            nn.Linear(10, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Linear(64, 1)
        ),
        'L2 (wd=0.01)': nn.Sequential(
            nn.Linear(10, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        )
    }
    
    results = {}
    for name, model in models.items():
        if 'L2' in name:
            opt = optim.Adam(model.parameters(), lr=0.01, weight_decay=0.01)
        else:
            opt = optim.Adam(model.parameters(), lr=0.01)
        
        criterion = nn.MSELoss()
        
        for epoch in range(500):
            model.train()
            opt.zero_grad()
            loss = criterion(model(X_t), y_t)
            loss.backward()
            opt.step()
        
        results[name] = loss.item()
        print(f"{name}: Final Loss = {loss.item():.4f}")
    
    return results

# compare_regularization()
print("রেগুলারাইজেশন তুলনা কনফিগার করা হয়েছে")
```

## ৫. ফিন্যান্সে রেগুলারাইজেশন
```python
class RegularizedStockModel(nn.Module):
    """ফিন্যান্সিয়াল মডেল + সব ধরনের রেগুলারাইজেশন"""
    def __init__(self, input_size=10):
        super().__init__()
        
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(32, 16),
            nn.ReLU(),
            
            nn.Linear(16, 1)
        )
    
    def forward(self, x):
        return self.net(x)

def train_regularized_model():
    """রেগুলারাইজড মডেল ট্রেনিং"""
    import yfinance as yf
    
    data = yf.download("MSFT", start="2020-01-01", end="2024-01-01")
    
    # ফিচার
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()
    data['Vol'] = data['Close'].pct_change().rolling(10).std()
    data['Ret'] = data['Close'].pct_change()
    data.dropna(inplace=True)
    
    X = data[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA20', 'Vol', 'Ret']].values
    y = data['Close'].values.reshape(-1, 1)
    
    # নরমালাইজ
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
    y = (y - y.mean()) / (y.std() + 1e-8)
    
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    
    model = RegularizedStockModel(input_size=8).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10)
    criterion = nn.MSELoss()
    
    # ট্রেনিং সহ ওভারফিটিং চেক
    X_tr_t = torch.FloatTensor(X_tr).to(device)
    y_tr_t = torch.FloatTensor(y_tr).to(device)
    X_te_t = torch.FloatTensor(X_te).to(device)
    y_te_t = torch.FloatTensor(y_te).to(device)
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        loss = criterion(model(X_tr_t), y_tr_t)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 50 == 0:
            model.eval()
            with torch.no_grad():
                val_loss = criterion(model(X_te_t), y_te_t)
            print(f"Epoch {epoch+1}: Train={loss.item():.4f}, Test={val_loss.item():.4f}")
            scheduler.step(val_loss)
    
    return model

print("ট্রেনিং ফাংশন ডিফাইন করা হয়েছে। চালানোর জন্য ফাংশন কল করুন।")
```

## কখন কী ব্যবহার করবেন?
```python
class RegularizationGuide:
    """রেগুলারাইজেশন গাইডলাইন"""
    
    @staticmethod
    def recommend(task):
        recommendations = {
            'small_dataset': ['Dropout (0.5)', 'L2 (0.01)', 'Early Stopping'],
            'large_dataset': ['BatchNorm', 'Dropout (0.2)', 'L2 (0.001)'],
            'time_series': ['Dropout (0.2)', 'BatchNorm', 'Gradient Clipping'],
            'image_data': ['BatchNorm', 'Dropout (0.3)', 'Data Augmentation'],
            'text_data': ['Dropout (0.1)', 'LayerNorm', 'Weight Decay'],
            'finance_data': ['Dropout (0.3)', 'BatchNorm', 'L2 (0.01)']
        }
        return recommendations.get(task, ['Dropout', 'L2'])

guide = RegularizationGuide()
print("ছোট ডেটাসেট:", guide.recommend('small_dataset'))
print("টাইম সিরিজ:", guide.recommend('time_series'))
print("ফিন্যান্স:", guide.recommend('finance_data'))
```

## সারসংক্ষেপ
| পদ্ধতি | কাজ | ফিন্যান্সে ব্যবহার |
|--------|-----|-------------------|
| **Dropout** | নিউরন র্যান্ডম বন্ধ | ওভারফিটিং কমানো |
| **BatchNorm** | আউটপুট নরমালাইজ | দ্রুত কনভার্জেন্স |
| **L2 (Weight Decay)** | বড় ওয়েট পিনালাইজ | জেনারেলাইজেশন |
| **Early Stopping** | ওভারফিট শুরু হলেই থামা | সব মডেলে |
| **Gradient Clipping** | গ্রেডিয়েন্ট ক্যাপ | RNN/LSTM এ |