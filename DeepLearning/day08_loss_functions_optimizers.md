# Day 08: ট্রেনিং লুপ, লস ফাংশন ও অপ্টিমাইজার 🎯

## ট্রেনিং লুপের উপাদান
```
প্রতি Epoch:
  1. ফরোয়ার্ড পাস → প্রেডিকশন
  2. লস ক্যালকুলেশন
  3. ব্যাকওয়ার্ড পাস (গ্রেডিয়েন্ট)
  4. ওয়েট আপডেট (অপ্টিমাইজার)
```

## PyTorch ট্রেনিং লুপ
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# সিম্পল ডেটা
np.random.seed(42)
X = np.random.randn(500, 5).astype(np.float32)
y = (X[:, 0] + X[:, 1] - X[:, 2] + np.random.randn(500) * 0.1 > 0).astype(np.float32)

X_t = torch.FloatTensor(X).to(device)
y_t = torch.FloatTensor(y).view(-1, 1).to(device)
```

## Loss Functions (লস ফাংশন)

### 1. Mean Squared Error (MSE) - রিগ্রেশন
```python
# MSE = 1/n * Σ(y_true - y_pred)²
def mse_loss(y_pred, y_true):
    return torch.mean((y_pred - y_true) ** 2)

# ফিন্যান্স: প্রাইস প্রেডিকশন
prices_true = torch.tensor([100.0, 102.0, 101.0, 105.0])
prices_pred = torch.tensor([99.5, 101.0, 102.0, 104.0])
print(f"MSE Loss: {mse_loss(prices_pred, prices_true):.4f}")
```

### 2. Binary Cross Entropy (BCE) - বাইনারি ক্লাসিফিকেশন
```python
# BCE = -1/n * Σ[y·log(ŷ) + (1-y)·log(1-ŷ)]
bce = nn.BCELoss()

# ফিন্যান্স: আপ/ডাউন প্রেডিকশন
prob_pred = torch.sigmoid(torch.tensor([0.5, 1.2, -0.8, 2.0]))
actual = torch.tensor([[1.0], [1.0], [0.0], [1.0]])
print(f"BCE Loss: {bce(prob_pred.view(-1,1), actual):.4f}")
```

### 3. Mean Absolute Error (MAE) / L1 Loss
```python
l1_loss = nn.L1Loss()
# MAE ফিন্যান্সে আউটলায়ার-রোবাস্ট
```

## Optimizers (অপ্টিমাইজার)

```python
class CompareOptimizers:
    """বিভিন্ন অপ্টিমাইজার তুলনা"""
    
    @staticmethod
    def test(lr=0.01, epochs=100):
        results = {}
        
        for opt_name in ['SGD', 'Adam', 'RMSprop', 'AdamW']:
            # সিম্পল নেটওয়ার্ক
            model = nn.Sequential(
                nn.Linear(5, 10), nn.ReLU(),
                nn.Linear(10, 1), nn.Sigmoid()
            ).to(device)
            
            if opt_name == 'SGD':
                optimizer = optim.SGD(model.parameters(), lr=lr)
            elif opt_name == 'Adam':
                optimizer = optim.Adam(model.parameters(), lr=lr)
            elif opt_name == 'RMSprop':
                optimizer = optim.RMSprop(model.parameters(), lr=lr)
            elif opt_name == 'AdamW':
                optimizer = optim.AdamW(model.parameters(), lr=lr)
            
            criterion = nn.BCELoss()
            losses = []
            
            for epoch in range(epochs):
                model.train()
                out = model(X_t)
                loss = criterion(out, y_t)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                losses.append(loss.item())
            
            results[opt_name] = losses
        
        return results

# অপ্টিমাইজার তুলনা
results = CompareOptimizers.test(lr=0.01, epochs=200)

for name, losses in results.items():
    print(f"{name}: Final Loss = {losses[-1]:.4f}")

plt.figure(figsize=(10, 6))
for name, losses in results.items():
    plt.plot(losses, label=name)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("অপ্টিমাইজার তুলনা")
plt.legend()
plt.grid(True)
plt.show()
```

## ফিন্যান্স: প্রাইস প্রেডিকশন ট্রেনিং লুপ
```python
import yfinance as yf

class PricePredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 32), nn.ReLU(),
            nn.Linear(32, 16), nn.ReLU(),
            nn.Linear(16, 1)
        )
    
    def forward(self, x):
        return self.net(x)

def prepare_stock_data(ticker="AAPL"):
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    data['SMA_5'] = data['Close'].rolling(5).mean()
    data['SMA_20'] = data['Close'].rolling(20).mean()
    data['Vol'] = data['Close'].pct_change().rolling(5).std()
    data['Mom'] = data['Close'] - data['Close'].shift(5)
    data['Vol_Ratio'] = data['Volume'] / data['Volume'].rolling(5).mean()
    data['Future_Price'] = data['Close'].shift(-5)  # ৫ দিন পরে প্রাইস
    
    data = data.dropna()
    
    features = data[['SMA_5', 'SMA_20', 'Vol', 'Mom', 'Vol_Ratio']].values
    targets = data['Future_Price'].values.reshape(-1, 1)
    
    # নরমালাইজ
    f_mean, f_std = features.mean(axis=0), features.std(axis=0)
    t_mean, t_std = targets.mean(), targets.std()
    features = (features - f_mean) / f_std
    targets = (targets - t_mean) / t_std
    
    return features, targets, (f_mean, f_std, t_mean, t_std)

# ডেটা লোড
features, targets, stats = prepare_stock_data("AAPL")
split = int(0.8 * len(features))

X_tr = torch.FloatTensor(features[:split]).to(device)
y_tr = torch.FloatTensor(targets[:split]).to(device)
X_te = torch.FloatTensor(features[split:]).to(device)
y_te = torch.FloatTensor(targets[split:]).to(device)

# মডেল
model = PricePredictor().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ট্রেনিং
for epoch in range(300):
    model.train()
    pred = model(X_tr)
    loss = criterion(pred, y_tr)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 50 == 0:
        model.eval()
        with torch.no_grad():
            test_loss = criterion(model(X_te), y_te)
        print(f"Epoch {epoch+1}: Train Loss={loss.item():.4f}, Test Loss={test_loss.item():.4f}")

# ফাইনাল ইভালুয়েশন
model.eval()
with torch.no_grad():
    preds = model(X_te).cpu().numpy()
    actuals = y_te.cpu().numpy()
    
    # ডিনরমালাইজ
    _, _, t_mean, t_std = stats
    preds_actual = preds * t_std + t_mean
    actuals_actual = actuals * t_std + t_mean
    
    mae = np.mean(np.abs(preds_actual - actuals_actual))
    print(f"\nMAE (প্রকৃত $): ${mae:.2f}")
```

## Learning Rate Scheduling
```python
# লার্নিং রেট শিডিউলার
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)

# ট্রেনিং লুপে ব্যবহার
for epoch in range(100):
    # ... ট্রেনিং ...
    scheduler.step()  # প্রতি 50 epoch এ LR অর্ধেক
    if epoch % 20 == 0:
        print(f"LR at epoch {epoch}: {optimizer.param_groups[0]['lr']}")
```

## সারসংক্ষেপ
- **Loss Functions**: MSE (রিগ্রেশন), BCE (ক্লাসিফিকেশন), MAE (রোবাস্ট)
- **Optimizers**: SGD (বেসিক), Adam (ফাস্ট), RMSprop (RNN)
- **ট্রেনিং লুপ**: forward → loss → backward → optimizer.step()
- **Learning Rate**: খুব গুরুত্বপূর্ণ হাইপারপ্যারামিটার
- ফিন্যান্সে MSE বেশি ব্যবহৃত হয় প্রাইস প্রেডিকশনের জন্য