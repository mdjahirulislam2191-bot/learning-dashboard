# Day 14: আর্লি স্টপিং ও কলব্যাকস ⏱️

## আর্লি স্টপিং কী?
ওভারফিটিং শুরু হওয়ার আগেই ট্রেনিং থামানোর টেকনিক। ভ্যালিডেশন লস কমতে থাকলে চালিয়ে যান, বাড়তে শুরু করলে থামান।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## ১. আর্লি স্টপিং ইমপ্লিমেন্টেশন
```python
class EarlyStopping:
    """আর্লি স্টপিং ইমপ্লিমেন্টেশন"""
    def __init__(self, patience=10, min_delta=0.001, verbose=True):
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        self.counter = 0
        self.best_loss = float('inf')
        self.best_model = None
        self.early_stop = False
    
    def __call__(self, val_loss, model):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.best_model = deepcopy(model.state_dict())
            self.counter = 0
            if self.verbose:
                print(f"✓ New best: {val_loss:.6f}")
        else:
            self.counter += 1
            if self.verbose:
                print(f"✗ No improvement {self.counter}/{self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
                if self.verbose:
                    print(f"🛑 Early stopping triggered!")
    
    def load_best_model(self, model):
        model.load_state_dict(self.best_model)
        return model
```

## ২. সম্পূর্ণ কলব্যাক সিস্টেম
```python
class Callback:
    """কলব্যাক বেস ক্লাস"""
    def on_epoch_end(self, epoch, logs):
        pass
    
    def on_train_end(self, logs):
        pass

class ModelCheckpoint(Callback):
    """সেরা মডেল সেভ করা"""
    def __init__(self, filepath='best_model.pth', monitor='val_loss', mode='min'):
        self.filepath = filepath
        self.monitor = monitor
        self.mode = mode
        self.best = float('inf') if mode == 'min' else -float('inf')
    
    def on_epoch_end(self, epoch, logs):
        current = logs.get(self.monitor)
        if self.mode == 'min' and current < self.best:
            self.best = current
            torch.save(logs['model'].state_dict(), self.filepath)
            print(f"  💾 Model saved (epoch {epoch})")

class LearningRateScheduler(Callback):
    """লার্নিং রেট শিডিউলার"""
    def __init__(self, factor=0.5, patience=5, min_lr=1e-6):
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.counter = 0
        self.best_loss = float('inf')
    
    def on_epoch_end(self, epoch, logs):
        val_loss = logs.get('val_loss')
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                current_lr = logs['optimizer'].param_groups[0]['lr']
                new_lr = max(current_lr * self.factor, self.min_lr)
                logs['optimizer'].param_groups[0]['lr'] = new_lr
                print(f"  📉 LR reduced: {current_lr:.6f} → {new_lr:.6f}")
                self.counter = 0

class History(Callback):
    """ট্রেনিং হিস্ট্রি ট্র্যাকিং"""
    def __init__(self):
        self.history = {'loss': [], 'val_loss': [], 'lr': []}
    
    def on_epoch_end(self, epoch, logs):
        self.history['loss'].append(logs.get('loss'))
        self.history['val_loss'].append(logs.get('val_loss'))
        self.history['lr'].append(logs['optimizer'].param_groups[0]['lr'])

class ProgressBar(Callback):
    """প্রোগ্রেস বার দেখানো"""
    def __init__(self, total_epochs):
        self.total = total_epochs
    
    def on_epoch_end(self, epoch, logs):
        pct = (epoch + 1) / self.total * 100
        bar = '█' * int(pct // 5) + '░' * (20 - int(pct // 5))
        print(f"\rEpoch {epoch+1}/{self.total} [{bar}] {pct:.0f}%", end="")
```

## ৩. ট্রেনিং ইঞ্জিন
```python
class Trainer:
    """কলব্যাক সহ সম্পূর্ণ ট্রেনিং ইঞ্জিন"""
    def __init__(self, model, criterion, optimizer, device=device):
        self.model = model.to(device)
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.callbacks = []
    
    def add_callback(self, callback):
        self.callbacks.append(callback)
    
    def fit(self, X_train, y_train, X_val=None, y_val=None, epochs=100, batch_size=32):
        X_tr = torch.FloatTensor(X_train).to(self.device)
        y_tr = torch.FloatTensor(y_train).to(self.device)
        
        if X_val is not None:
            X_v = torch.FloatTensor(X_val).to(self.device)
            y_v = torch.FloatTensor(y_val).to(self.device)
        
        n_samples = len(X_tr)
        
        for epoch in range(epochs):
            # ট্রেনিং
            self.model.train()
            
            # মিনি-ব্যাচ
            perm = torch.randperm(n_samples)
            epoch_loss = 0
            n_batches = 0
            
            for i in range(0, n_samples, batch_size):
                indices = perm[i:i+batch_size]
                batch_X = X_tr[indices]
                batch_y = y_tr[indices]
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                n_batches += 1
            
            avg_train_loss = epoch_loss / n_batches
            
            # ভ্যালিডেশন
            self.model.eval()
            with torch.no_grad():
                if X_val is not None:
                    val_outputs = self.model(X_v)
                    val_loss = self.criterion(val_outputs, y_v).item()
                else:
                    val_loss = avg_train_loss
            
            # কলব্যাক কল
            logs = {
                'loss': avg_train_loss,
                'val_loss': val_loss,
                'model': self.model,
                'optimizer': self.optimizer,
                'epoch': epoch
            }
            
            for callback in self.callbacks:
                callback.on_epoch_end(epoch, logs)
            
            # আর্লি স্টপিং চেক
            early_stop = [c for c in self.callbacks if isinstance(c, EarlyStopping)]
            if early_stop and early_stop[0].early_stop:
                break
        
        # ট্রেনিং শেষ
        for callback in self.callbacks:
            callback.on_train_end(logs)
        
        return self.model
```

## ৪. ফিন্যান্স: সম্পূর্ণ ট্রেনিং উদাহরণ
```python
import yfinance as yf

def train_stock_model_with_callbacks():
    """কলব্যাক সহ স্টক প্রেডিকশন মডেল ট্রেনিং"""
    
    # ডেটা
    data = yf.download("GOOGL", start="2020-01-01", end="2024-01-01")
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()
    data['Vol'] = data['Close'].pct_change().rolling(5).std()
    data['Target'] = data['Close'].shift(-1)
    data.dropna(inplace=True)
    
    feature_cols = ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA20', 'Vol']
    X = data[feature_cols].values
    y = data['Target'].values.reshape(-1, 1)
    
    # নরমালাইজ
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
    y = (y - y.mean()) / (y.std() + 1e-8)
    
    # স্প্লিট
    split = int(0.8 * len(X))
    X_tr, X_val = X[:split], X[split:]
    y_tr, y_val = y[:split], y[split:]
    
    # মডেল
    model = nn.Sequential(
        nn.Linear(7, 64), nn.ReLU(),
        nn.Linear(64, 32), nn.ReLU(),
        nn.Linear(32, 1)
    )
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # ট্রেইনার ও কলব্যক
    trainer = Trainer(model, criterion, optimizer)
    
    early_stopping = EarlyStopping(patience=15, min_delta=0.0001)
    checkpoint = ModelCheckpoint('best_googl.pth')
    lr_scheduler = LearningRateScheduler(factor=0.5, patience=8)
    history = History()
    progress = ProgressBar(100)
    
    trainer.add_callback(early_stopping)
    trainer.add_callback(checkpoint)
    trainer.add_callback(lr_scheduler)
    trainer.add_callback(history)
    trainer.add_callback(progress)
    
    print("\n🚀 ট্রেনিং শুরু...\n")
    trainer.fit(X_tr, y_tr, X_val, y_val, epochs=100, batch_size=32)
    
    print(f"\n\n✅ সেরা ভ্যালিডেশন লস: {early_stopping.best_loss:.6f}")
    
    # সেরা মডেল লোড
    model = early_stopping.load_best_model(model)
    print("✅ Best model loaded!")
    
    return model, history.history

# model, hist = train_stock_model_with_callbacks()
print("ট্রেনিং ইঞ্জিন প্রস্তুত। train_stock_model_with_callbacks() কল করুন")
```

## কলব্যকের সুবিধা
```python
class CallbackBenefits:
    """কলব্যক ব্যবহারের সুবিধা"""
    
    @staticmethod
    def summary():
        return """
📌 **আর্লি স্টপিং**: 
   - ওভারফিটিং প্রতিরোধ
   - সময় বাঁচায় (অপ্রয়োজনীয় ইটারেশন এড়ায়)
   - অটোমেটিক থামানোর সিদ্ধান্ত

📌 **Model Checkpoint**:
   - সেরা মডেল অটো সেভ
   - ক্র্যাশের পর রিকভারি

📌 **Learning Rate Scheduler**:
   - প্লাটুতে LR কমিয়ে উন্নতি
   - ম্যানুয়াল ইন্ডারভেনশন লাগে না

📌 **History**:
   - লস/মেট্রিক্স ট্র্যাকিং
   - ভিজুয়ালাইজেশন

📌 **ফিন্যান্সে গুরুত্ব**:
   - স্টক প্রাইস প্রেডিকশন ওভারফিট হয়
   - Early stopping + Callbacks = প্রফেশনাল ওয়ার্কফ্লো
        """

print(CallbackBenefits.summary())
```

## সারসংক্ষেপ
- Early Stopping: patience + min_delta দিয়ে ওভারফিট প্রতিরোধ
- Callbacks: ModelCheckpoint, LR Scheduler, History
- ফিন্যান্সে প্রতিটি মডেলে কলব্যাক ব্যবহার করা উচিত
- প্রফেশনাল DL ওয়ার্কফ্লোর অপরিহার্য অংশ