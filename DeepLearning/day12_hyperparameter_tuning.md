# Day 12: হাইপারপ্যারামিটার টিউনিং ⚙️

## হাইপারপ্যারামিটার কী?
হাইপারপ্যারামিটার হল মডেলের সেটিংস যা ট্রেনিং-এর আগে সেট করতে হয় (মডেল শিখতে পারেনা)।

### প্রধান হাইপারপ্যারামিটার
1. **Learning Rate (lr)** - কত দ্রুত শিখবে (0.0001 - 0.1)
2. **Batch Size** - একবারে কত স্যাম্পল (16, 32, 64, 128)
3. **Number of Layers** - নেটওয়ার্কের গভীরতা
4. **Neurons per Layer** - প্রতি লেয়ারে নিউরন সংখ্যা
5. **Dropout Rate** - ড্রপআউটের পরিমাণ (0.1 - 0.5)
6. **Optimizer** - SGD, Adam, RMSprop ইত্যাদি
7. **Activation Function** - ReLU, Tanh, Sigmoid
8. **Weight Decay** - L2 রেগুলারাইজেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import itertools
from sklearn.model_selection import ParameterGrid
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## ১. Grid Search
```python
class HyperparameterTuner:
    """Grid Search দিয়ে হাইপারপ্যারামিটার টিউনিং"""
    
    def __init__(self, X_train, y_train, X_val, y_val):
        self.X_tr = torch.FloatTensor(X_train).to(device)
        self.y_tr = torch.FloatTensor(y_train).to(device)
        self.X_val = torch.FloatTensor(X_val).to(device)
        self.y_val = torch.FloatTensor(y_val).to(device)
        self.results = []
    
    def create_model(self, n_layers, n_neurons, dropout_rate):
        """ডাইনামিক মডেল তৈরি"""
        layers = []
        input_dim = self.X_tr.shape[1]
        
        for _ in range(n_layers):
            layers.append(nn.Linear(input_dim, n_neurons))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            input_dim = n_neurons
        
        layers.append(nn.Linear(input_dim, 1))
        return nn.Sequential(*layers).to(device)
    
    def train_and_evaluate(self, params):
        """এক সেট প্যারামিটার দিয়ে ট্রেনিং"""
        model = self.create_model(
            params['n_layers'],
            params['n_neurons'],
            params['dropout']
        )
        
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=params['lr'])
        
        # ট্রেনিং
        for epoch in range(params['epochs']):
            model.train()
            optimizer.zero_grad()
            loss = criterion(model(self.X_tr), self.y_tr)
            loss.backward()
            optimizer.step()
        
        # ইভালুয়েশন
        model.eval()
        with torch.no_grad():
            val_loss = criterion(model(self.X_val), self.y_val)
        
        return val_loss.item()
    
    def grid_search(self, param_grid, epochs=50):
        """সমস্ত কম্বিনেশন টেস্ট"""
        grid = ParameterGrid(param_grid)
        best_loss = float('inf')
        best_params = None
        
        print(f"মোট {len(grid)} টি কম্বিনেশন টেস্ট করা হবে...\n")
        
        for i, params in enumerate(grid):
            params['epochs'] = epochs
            val_loss = self.train_and_evaluate(params)
            
            self.results.append({**params, 'val_loss': val_loss})
            
            if val_loss < best_loss:
                best_loss = val_loss
                best_params = params
            
            print(f"[{i+1}/{len(grid)}] lr={params['lr']}, layers={params['n_layers']}, "
                  f"neurons={params['n_neurons']}, dropout={params['dropout']} → Loss={val_loss:.4f}")
        
        print(f"\n✅ Best: {best_params} → Loss={best_loss:.4f}")
        return best_params

# সিন্থেটিক ডেটা
np.random.seed(42)
X = np.random.randn(1000, 5)
y = np.sum(X[:, :3], axis=1, keepdims=True) + np.random.randn(1000, 1) * 0.1

X_train, X_val = X[:800], X[800:]
y_train, y_val = y[:800], y[800:]

# Grid Search
tuner = HyperparameterTuner(X_train, y_train, X_val, y_val)

param_grid = {
    'lr': [0.001, 0.01],
    'n_layers': [1, 2],
    'n_neurons': [16, 32],
    'dropout': [0.0, 0.2]
}

# best_params = tuner.grid_search(param_grid, epochs=30)
print("Grid Search কনফিগারেশন সেট করা হয়েছে।")
print(f"প্যারামিটার গ্রিড: {param_grid}")
```

## ২. Random Search
```python
import random

class RandomSearch:
    """Random Search হাইপারপ্যারামিটার টিউনিং"""
    
    def __init__(self, n_trials=20):
        self.n_trials = n_trials
    
    def sample_params(self):
        """র্যান্ডম প্যারামিটার স্যাম্পল"""
        return {
            'lr': 10 ** random.uniform(-4, -1),  # 0.0001 - 0.1
            'batch_size': random.choice([16, 32, 64, 128]),
            'n_layers': random.randint(1, 4),
            'n_neurons': random.choice([16, 32, 64, 128, 256]),
            'dropout': random.uniform(0.0, 0.5),
            'weight_decay': 10 ** random.uniform(-5, -2),
            'optimizer': random.choice(['adam', 'sgd'])
        }
    
    def search(self):
        for trial in range(self.n_trials):
            params = self.sample_params()
            print(f"Trial {trial+1}: {params}")
        return self.sample_params()

# rs = RandomSearch(10)
# rs.search()
print("Random Search: র্যান্ডম প্যারামিটার ট্রায়াল করার কনসেপ্ট")
```

## ৩. Learning Rate Finder
```python
def lr_finder(model, X, y, start_lr=1e-7, end_lr=10, num_iter=100):
    """Optimal Learning Rate খোঁজা"""
    lrs = np.logspace(np.log10(start_lr), np.log10(end_lr), num_iter)
    losses = []
    
    X_t = torch.FloatTensor(X).to(device)
    y_t = torch.FloatTensor(y).to(device)
    
    for lr in lrs:
        model_copy = model().__to(device)
        optimizer = optim.SGD(model_copy.parameters(), lr=lr)
        criterion = nn.MSELoss()
        
        optimizer.zero_grad()
        output = model_copy(X_t)
        loss = criterion(output, y_t)
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
    
    # সাজেস্টেড LR = steepest descent পয়েন্ট
    gradients = np.gradient(losses)
    suggested_idx = np.argmin(gradients)
    suggested_lr = lrs[suggested_idx]
    
    print(f"সাজেস্টেড Learning Rate: {suggested_lr:.6f}")
    return suggested_lr

# নোট: লার্জ ডেটাসেটের জন্য lr_finder চালানো উচিত
print("LR Finder: steepest descent পয়েন্ট খুঁজে optimal LR বের করে")
```

## ৪. ফিন্যান্স: হাইপারপ্যারামিটার অপ্টিমাইজেশন
```python
def optimize_for_stock_prediction(ticker="AAPL"):
    """স্টক প্রেডিকশনের জন্য HP টিউনিং"""
    import yfinance as yf
    
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    data['Return'] = data['Close'].pct_change()
    data['SMA_10'] = data['Close'].rolling(10).mean()
    data.dropna(inplace=True)
    
    features = data[['Open', 'High', 'Low', 'Volume', 'Return', 'SMA_10']].values
    targets = data['Close'].shift(-1).dropna().values.reshape(-1, 1)
    
    # অ্যালাইন
    features = features[:len(targets)]
    
    # নরমালাইজ
    f_mean, f_std = features.mean(axis=0), features.std(axis=0)
    t_mean, t_std = targets.mean(), targets.std()
    features = (features - f_mean) / f_std
    targets = (targets - t_mean) / t_std
    
    # স্প্লিট
    split = int(0.8 * len(features))
    X_tr, X_v = features[:split], features[split:]
    y_tr, y_v = targets[:split], targets[split:]
    
    # কুইক টিউনিং (ছোট গ্রিড)
    tuner = HyperparameterTuner(X_tr, y_tr, X_v, y_v)
    quick_grid = {
        'lr': [0.001, 0.01],
        'n_layers': [2, 3],
        'n_neurons': [32, 64],
        'dropout': [0.1, 0.2]
    }
    
    print(f"{ticker} স্টকের জন্য HP টিউনিং...")
    print(f"Grid: {quick_grid}")
    # best = tuner.grid_search(quick_grid, epochs=30)
    
    return {"ticker": ticker, "grid": quick_grid}

# opt = optimize_for_stock_prediction("AAPL")
print("স্টক প্রেডিকশনের জন্য HP অপ্টিমাইজেশন কনফিগার করা হয়েছে")
```

## বেস্ট প্র্যাকটিস
```python
class BestPractices:
    """হাইপারপ্যারামিটার টিউনিং বেস্ট প্র্যাকটিস"""
    
    @staticmethod
    def tips():
        return [
            "1. Learning Rate সবচেয়ে গুরুত্বপূর্ণ HP → LR Finder ব্যবহার করুন",
            "2. Batch Size: পাওয়ার অফ ২ (32, 64, 128) → GPU মেমরি অনুযায়ী",
            "3. Grid → Random → Bayesian Search (ধীর থেকে দ্রুত)",
            "4. ছোট ডেটায় ২-৩ লেয়ার যথেষ্ট, বড় ডেটায় গভীর নেটওয়ার্ক",
            "5. Dropout: 0.2-0.5 (ওভারফিটিং অনুযায়ী)",
            "6. Weight Decay (L2): 1e-5 to 1e-3",
            "7. Validation set এ HP টিউন করুন, TEST SET স্পর্শ করবেন না",
            "8. Cross-validation ফিন্যান্সে time-series CV ব্যবহার করুন",
        ]
    
    @staticmethod
    def fintech_recommendations():
        """ফিন্যান্সিয়াল ML-এর জন্য HP রেকমেন্ডেশন"""
        return {
            'stock_prediction': {'lr': 0.001, 'layers': 2, 'dropout': 0.2},
            'fraud_detection': {'lr': 0.01, 'layers': 3, 'dropout': 0.3},
            'credit_scoring': {'lr': 0.001, 'layers': 2, 'dropout': 0.2},
            'portfolio_optimization': {'lr': 0.0005, 'layers': 3, 'dropout': 0.1},
            'sentiment_analysis': {'lr': 2e-5, 'layers': 4, 'dropout': 0.1}  # Transformer
        }

for tip in BestPractices.tips():
    print(tip)
```

## সারসংক্ষেপ
- **Grid Search**: সব কম্বিনেশন → ধীর কিন্তু নির্ভুল
- **Random Search**: র্যান্ডম স্যাম্পল → দ্রুত
- **Bayesian Search**: স্মার্ট সার্চ (Optuna, Hyperopt)
- **LR Finder**: Optimal LR খোঁজার জন্য
- ফিন্যান্সে Time Series CV ব্যবহার করা জরুরি
- HP টিউনিং মডেল পারফরম্যান্স ২০-৫০% উন্নত করতে পারে