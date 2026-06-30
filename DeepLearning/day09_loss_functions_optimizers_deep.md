# Day 09: Loss Functions & Optimizers Deep Dive 🎯

## Loss Functions বিস্তারিত

### Classification Losses
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# ১. Binary Cross Entropy (BCE)
bce = nn.BCELoss()
bce_logits = nn.BCEWithLogitsLoss()  # numerically stable

# উদাহরণ
logits = torch.tensor([[2.5], [-1.3], [0.1], [-0.7]])
labels = torch.tensor([[1.0], [0.0], [1.0], [0.0]])

# BCEWithLogitsLoss (recommended)
loss_logits = bce_logits(logits, labels)
print(f"BCEWithLogitsLoss: {loss_logits.item():.4f}")

# ২. Categorical Cross Entropy (মাল্টি-ক্লাস)
ce_loss = nn.CrossEntropyLoss()

# ফিন্যান্স: ৩টি অ্যাসেট ক্লাস (Stock, Bond, Commodity)
logits_3class = torch.tensor([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0]])
labels_3class = torch.tensor([0, 1])  # Stock, Bond
print(f"CrossEntropyLoss: {ce_loss(logits_3class, labels_3class):.4f}")
```

### Regression Losses
```python
# ৩. MSE Loss (L2)
mse = nn.MSELoss()

# ৪. MAE Loss (L1)
l1 = nn.L1Loss()

# ৫. Huber Loss (MSE + MAE হাইব্রিড)
huber = nn.HuberLoss(delta=1.0)

# ফিন্যান্স: আউটলায়ারের প্রভাব কমানো
true_prices = torch.tensor([100.0, 102.0, 101.0, 98.0, 500.0])  # 500 = outlier
pred_prices = torch.tensor([101.0, 103.0, 100.0, 99.0, 105.0])

print(f"MSE: {mse(pred_prices, true_prices):.2f}")
print(f"MAE: {l1(pred_prices, true_prices):.2f}")
print(f"Huber: {huber(pred_prices, true_prices):.2f}")
# MAE আউটলায়ারে কম প্রভাবিত হয়
```

## Optimizers বিস্তারিত

### 1. SGD (Stochastic Gradient Descent)
```python
class SGDManual:
    """ম্যানুয়াল SGD ইমপ্লিমেন্টেশন"""
    def __init__(self, params, lr=0.01):
        self.params = list(params)
        self.lr = lr
    
    def step(self):
        for param in self.params:
            if param.grad is not None:
                param.data -= self.lr * param.grad.data
    
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()
```

### 2. SGD with Momentum
```python
# Momentum = পূর্বের গ্রেডিয়েন্ট দিক ধরে রাখা
# v = β·v_prev + η·∇L
# w = w - v

# SGD+Momentum
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

### 3. Adam (Adaptive Moment Estimation)
```python
# Adam = Momentum + RMSprop
# β₁ = 0.9 (momentum decay)
# β₂ = 0.999 (RMSprop decay)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
```

## অপ্টিমাইজার কনভার্জেন্স তুলনা
```python
import matplotlib.pyplot as plt

def train_with_optimizer(model_class, opt_name, lr=0.01):
    """একটি অপ্টিমাইজার দিয়ে ট্রেনিং"""
    model = model_class().to(device)
    
    optimizers_dict = {
        'SGD': optim.SGD(model.parameters(), lr=lr),
        'SGD_Momentum': optim.SGD(model.parameters(), lr=lr, momentum=0.9),
        'Adam': optim.Adam(model.parameters(), lr=lr),
        'RMSprop': optim.RMSprop(model.parameters(), lr=lr),
        'AdamW': optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    }
    
    optimizer = optimizers_dict[opt_name]
    criterion = nn.MSELoss()
    losses = []
    
    for _ in range(500):
        model.train()
        out = model(torch.randn(32, 5).to(device))
        target = torch.randn(32, 1).to(device)
        loss = criterion(out, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    
    return losses

# নোট: ফুল ট্রেনিং চালাতে সময় লাগতে পারে
# উপরের ফাংশনটি কনসেপ্ট বুঝতে সাহায্য করবে
```

## ফিন্যান্স-নির্দিষ্ট লস ফাংশন
```python
class FinancialLosses:
    """ফিন্যান্সিয়াল টাস্কের জন্য কাস্টম লস"""
    
    @staticmethod
    def sharpe_ratio_loss(returns, risk_free=0.02):
        """Sharpe Ratio ম্যাক্সিমাইজ করা (নেগেটিভ লস)"""
        mean_return = returns.mean()
        std_return = returns.std() + 1e-8
        sharpe = (mean_return - risk_free) / std_return
        return -sharpe  # minimize negative Sharpe = maximize Sharpe
    
    @staticmethod
    def portfolio_variance_loss(weights, cov_matrix, target_return, returns):
        """পোর্টফোলিও ভ্যারিয়েন্স মিনিমাইজ"""
        port_return = (weights * returns.mean()).sum()
        port_var = weights @ cov_matrix @ weights
        return_loss = (port_return - target_return) ** 2
        return port_var + return_loss  # ট্রেড-অফ
    
    @staticmethod
    def directional_accuracy_loss(pred, target):
        """ডিরেকশনাল অ্যাকুরেসি (আপ/ডাউন)"""
        pred_dir = torch.sign(pred)
        target_dir = torch.sign(target)
        wrong_direction = (pred_dir != target_dir).float().mean()
        return wrong_direction

# উদাহরণ
fin_loss = FinancialLosses()

# Directional loss
pred_returns = torch.tensor([0.02, -0.01, 0.03, -0.02])
actual_returns = torch.tensor([0.01, -0.02, 0.04, 0.01])
print(f"Directional Error: {fin_loss.directional_accuracy_loss(pred_returns, actual_returns):.2%}")
```

## Weight Decay (L2 Regularization)
```python
# L2 রেগুলারাইজেশন = λ * Σ(w²)
# AdamW: Adam + Decoupled Weight Decay
model = nn.Linear(10, 1)
optimizer_adamw = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# ফিন্যান্স: ওভারফিটিং কমানোর জন্য গুরুত্বপূর্ণ
print("Weight Decay ওভারফিটিং কমায় ও জেনারেলাইজেশন বাড়ায়")
```

## Gradient Clipping
```python
# গ্রেডিয়েন্ট এক্সপ্লোডিং প্রতিরোধ
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# ট্রেনিং লুপে ব্যবহার
for epoch in range(epochs):
    loss = criterion(model(X), y)
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
```

## সারসংক্ষেপ
| অপ্টিমাইজার | গতি | স্থিতিশীলতা | ফিন্যান্সে ব্যবহার |
|-------------|-----|-------------|-------------------|
| SGD | ধীর | ভালো | বেসিক মডেল |
| SGD+Momentum | মাঝারি | ভালো | স্ট্যান্ডার্ড |
| Adam | দ্রুত | চমৎকার | **ডিফল্ট** |
| RMSprop | দ্রুত | ভালো | RNN/LSTM |
| AdamW | দ্রুত | চমৎকার | +Regularization |

- Loss function টাস্ক অনুযায়ী সিলেক্ট করুন
- Adam অধিকাংশ ক্ষেত্রেই ডিফল্ট চয়েজ
- Weight decay ও gradient clipping গুরুত্বপূর্ণ
- ফিন্যান্সে কাস্টম লস ফাংশন তৈরি করা যায় (Sharpe Ratio, etc.)