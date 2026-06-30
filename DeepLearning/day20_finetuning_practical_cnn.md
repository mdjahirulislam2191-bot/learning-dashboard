# Day 20: Fine-tuning ও প্র্যাকটিক্যাল CNN 🎯

## Fine-tuning প্র্যাকটিস
ট্রান্সফার লার্নিং-এর পরে মডেলকে নির্দিষ্ট ডেটাসেটে অ্যাডজাস্ট করা।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## সম্পূর্ণ Fine-tuning পাইপলাইন
```python
class FineTuningPipeline:
    """সম্পূর্ণ Fine-tuning পাইপলাইন"""
    
    def __init__(self, model, num_classes):
        self.base_model = model
        self.num_classes = num_classes
        
    def prepare_model(self, freeze_backbone=True):
        """মডেল প্রস্তুত"""
        if freeze_backbone:
            # ব্যাকবোন ফ্রিজ
            for param in self.base_model.parameters():
                param.requires_grad = False
        
        # নতুন ক্লাসিফায়ার হেড
        in_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.num_classes)
        )
        
        return self.base_model.to(device)
    
    def train(self, train_loader, val_loader, epochs=30, lr=0.001):
        """Fine-tuning"""
        model = self.base_model
        criterion = nn.CrossEntropyLoss()
        
        # শুধু ট্রেইনেবল প্যারামিটার আপডেট
        trainable_params = [p for p in model.parameters() if p.requires_grad]
        optimizer = optim.Adam(trainable_params, lr=lr)
        
        history = {'train_loss': [], 'val_acc': []}
        
        for epoch in range(epochs):
            # Train
            model.train()
            total_loss = 0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            # Validation
            model.eval()
            correct = 0
            total = 0
            
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                    outputs = model(batch_X)
                    _, predicted = torch.max(outputs, 1)
                    total += batch_y.size(0)
                    correct += (predicted == batch_y).sum().item()
            
            accuracy = correct / total
            avg_loss = total_loss / len(train_loader)
            
            history['train_loss'].append(avg_loss)
            history['val_acc'].append(accuracy)
            
            if (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch+1}: Loss={avg_loss:.4f}, Val Acc={accuracy:.2%}")
        
        return model, history

# Pipeline তৈরি
# pipeline = FineTuningPipeline(model, num_classes=5)
# model = pipeline.prepare_model(freeze_backbone=True)
# trained_model, history = pipeline.train(train_loader, val_loader)
print("Fine-tuning পাইপলাইন প্রস্তুত")
```

## ফিন্যান্স CNN প্রজেক্ট: স্টক চার্ট ক্লাসিফায়ার
```python
class StockChartFineTuner:
    """স্টক চার্ট প্যাটার্ন ডিটেকশনের জন্য Fine-tuning"""
    
    def __init__(self):
        import torchvision.models as models
        self.model = models.resnet18(pretrained=True)
        
        # গ্রেস্কেল চার্টের জন্য
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        
        # নতুন ক্লাসিফায়ার
        self.model.fc = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 6)  # 6 প্যাটার্ন
        )
        
        self.model = self.model.to(device)
        self.patterns = ['Uptrend', 'Downtrend', 'Sideways', 
                        'Breakout', 'Pullback', 'Volatile']
    
    def generate_training_data(self, n_samples=2000):
        """ট্রেনিং ডেটা জেনারেট"""
        X, y = [], []
        
        for _ in range(n_samples):
            pattern = np.random.randint(0, 6)
            prices = self._generate_pattern(pattern)
            img = self._prices_to_image(prices)
            X.append(img)
            y.append(pattern)
        
        X = np.array(X, dtype=np.float32)
        y = np.array(y)
        
        split = int(0.8 * len(X))
        return (X[:split], y[:split]), (X[split:], y[split:])
    
    def _generate_pattern(self, pattern_type):
        """প্যাটার্ন জেনারেট"""
        n = 64
        x = np.linspace(0, 1, n)
        
        if pattern_type == 0:  # Uptrend
            return 100 + np.cumsum(np.random.randn(n) * 0.5) + 20 * x
        elif pattern_type == 1:  # Downtrend
            return 100 + np.cumsum(np.random.randn(n) * 0.5) - 20 * x
        elif pattern_type == 2:  # Sideways
            return 100 + np.cumsum(np.random.randn(n) * 0.5)
        elif pattern_type == 3:  # Breakout
            prices = 100 + np.cumsum(np.random.randn(n) * 0.3)
            prices[40:] += 10 * np.exp(-np.linspace(0, 2, n-40))
            return prices
        elif pattern_type == 4:  # Pullback
            prices = 100 + np.cumsum(np.random.randn(n) * 0.3) + 20 * x
            prices[30:50] -= 8
            return prices
        else:  # Volatile
            return 100 + np.cumsum(np.random.randn(n) * 2.0)
    
    def _prices_to_image(self, prices, img_size=64):
        """প্রাইস → ইমেজ"""
        prices_norm = (prices - prices.min()) / (prices.max() - prices.min() + 1e-8)
        img = np.zeros((img_size, img_size))
        scaled = (prices_norm * (img_size - 1)).astype(int)
        
        for i in range(min(img_size, len(scaled))):
            img[img_size - 1 - scaled[i], i] = 1.0
        
        return img.reshape(1, img_size, img_size)  # (1, H, W)
    
    def train(self, epochs=30):
        """মডেল ট্রেনিং"""
        (X_tr, y_tr), (X_te, y_te) = self.generate_training_data()
        
        X_tr_t = torch.FloatTensor(X_tr).to(device)
        y_tr_t = torch.LongTensor(y_tr).to(device)
        X_te_t = torch.FloatTensor(X_te).to(device)
        y_te_t = torch.LongTensor(y_te).to(device)
        
        train_loader = DataLoader(
            TensorDataset(X_tr_t, y_tr_t), 
            batch_size=32, shuffle=True
        )
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.0001)
        
        for epoch in range(epochs):
            self.model.train()
            for bX, bY in train_loader:
                optimizer.zero_grad()
                outputs = self.model(bX)
                loss = criterion(outputs, bY)
                loss.backward()
                optimizer.step()
            
            # Test
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(X_te_t)
                _, preds = torch.max(outputs, 1)
                acc = (preds == y_te_t).float().mean()
            
            if (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch+1}: Acc={acc:.2%}")
        
        return self.model

# finetuner = StockChartFineTuner()
# finetuner.train(epochs=30)
print("স্টক চার্ট ফাইন-টিউনার প্রস্তুত")
```

## Fine-tuning Tips
```python
class FineTuningTips:
    """Fine-tuning বেস্ট প্র্যাকটিস"""
    
    @staticmethod
    def get_tips():
        tips = """
🎯 **Fine-tuning Tips for Finance:**

1️⃣ **Learning Rate:**
   - ফিচার এক্সট্র্যাক্টর: lr = 0.001
   - Fine-tune ব্যাকবোন: lr = 0.0001
   - ক্লাসিফায়ার হেড: lr = 0.001 (higher for new layers)

2️⃣ **Layer Freezing Strategy:**
   - প্রথম কয়েক লেয়ার → জেনারেল ফিচার (edges, textures)
   - শেষ লেয়ার → স্পেসিফিক ফিচার (চার্ট প্যাটার্ন)
   - ফিন্যান্স চার্ট ImageNet থেকে আলাদা → বেশি লেয়ার আনফ্রিজ

3️⃣ **Data Augmentation for Charts:**
   - Small rotation (±5°)
   - Scaling (0.9-1.1x)
   - Adding noise
   - Time warp

4️⃣ **Transfer Learning Source:**
   - ImageNet → OK for chart patterns
   - Time-series pretrained → Better for finance
   - Self-supervised → Best if available

5️⃣ **Watch out for:**
   - Catastrophic forgetting (use small LR)
   - Domain shift (chart ≠ natural images)
   - Class imbalance (finance data often imbalanced)
        """
        print(tips)

FineTuningTips.get_tips()
```

## সারসংক্ষেপ
- Fine-tuning = Pretrained মডেল অ্যাডাপ্ট করা
- ব্যাকবোন ফ্রিজ + নতুন হেড → স্টেপ বাই স্টেপ আনফ্রিজ
- ফিন্যান্সে স্টক চার্ট প্যাটার্ন ডিটেকশন
- ছোট LR ব্যবহার (1e-4 or lower)
- Catastrophic forgetting থেকে সাবধান