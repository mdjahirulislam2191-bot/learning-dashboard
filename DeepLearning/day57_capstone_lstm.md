# Day 57: ক্যাপস্টোন — LSTM মডেল 🧠📈

## LSTM মডেল ক্যাপস্টোন
আজ আমরা ক্যাপস্টোন প্রজেক্টের জন্য LSTM মডেল তৈরি করব — স্টক প্রাইস ট্রেন্ড প্রেডিকশন।

### মডেল আর্কিটেকচার
```
ইনপুট (seq=30, features=14)
  │
  ▼
LSTM Layer 1 (hidden=128, bidirectional=True)
  │
  ▼
Dropout (0.3)
  │
  ▼
LSTM Layer 2 (hidden=64)
  │
  ▼
Dropout (0.3)
  │
  ▼
Fully Connected (64 → 32 → 3 classes)
  │
  ▼
Softmax → DOWN / NEUTRAL / UP
```

### ট্রেনিং সেটআপ
- Loss: CrossEntropyLoss
- Optimizer: AdamW (lr=0.001, weight_decay=1e-4)
- Scheduler: ReduceLROnPlateau
- Early Stopping (patience=10)
- Batch Size: 32

## LSTM মডেল ইমপ্লিমেন্টেশন (PyTorch)

```python
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. LSTM মডেল আর্কিটেকচার

```python
class LSTMModel(nn.Module):
    """ক্যাপস্টোন LSTM মডেল — স্টক ট্রেন্ড ক্লাসিফিকেশন"""
    def __init__(self, input_dim=14, hidden_dim=128, num_layers=2,
                 num_classes=3, dropout=0.3, bidirectional=True):
        super().__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.directions = 2 if bidirectional else 1
        
        # LSTM লেয়ারস
        self.lstm1 = nn.LSTM(
            input_dim, hidden_dim, num_layers=1,
            batch_first=True, bidirectional=bidirectional,
            dropout=0
        )
        
        lstm2_input = hidden_dim * self.directions
        self.lstm2 = nn.LSTM(
            lstm2_input, hidden_dim, num_layers=1,
            batch_first=True, bidirectional=False,
            dropout=0
        )
        
        # ড্রপআউট
        self.dropout = nn.Dropout(dropout)
        
        # ব্যাচ নরমালাইজেশন
        self.bn1 = nn.LayerNorm(hidden_dim * self.directions)
        self.bn2 = nn.LayerNorm(hidden_dim)
        
        # ক্লাসিফায়ার হেড
        self.fc1 = nn.Linear(hidden_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, num_classes)
        
        # অ্যাটেনশন
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim * self.directions, 1),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        # x shape: (batch, seq_len, features)
        
        # LSTM 1 (bidirectional)
        lstm1_out, (h_n1, c_n1) = self.lstm1(x)
        lstm1_out = self.bn1(lstm1_out)
        lstm1_out = self.dropout(lstm1_out)
        
        # LSTM 2 (unidirectional)
        lstm2_out, (h_n2, c_n2) = self.lstm2(lstm1_out)
        lstm2_out = self.bn2(lstm2_out)
        
        # অ্যাটেনশন মেকানিজম (লাস্ট হিডেন স্টেটে ফোকাস)
        attn_weights = self.attention(lstm2_out)
        context = torch.sum(attn_weights * lstm2_out, dim=1)
        
        # ক্লাসিফায়ার
        x = F.relu(self.fc1(context))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x
    
    def get_features(self, x):
        """এম্বেডিং এক্সট্র্যাক্ট (প্রেডিকশনের জন্য)"""
        with torch.no_grad():
            lstm1_out, _ = self.lstm1(x)
            lstm2_out, _ = self.lstm2(lstm1_out)
            features = torch.mean(lstm2_out, dim=1)
        return features

# মডেল তৈরি
model = LSTMModel(
    input_dim=14, hidden_dim=128, num_layers=2,
    num_classes=3, dropout=0.3, bidirectional=True
).to(device)

total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"মডেল প্যারামিটার: {total_params:,}")
print(f"ট্রেনেবল: {trainable_params:,}")
print(f"মডেল:\n{model}")
```

## 2. সিন্থেটিক ডেটা জেনারেট করুন (ডে 56 থেকে ছাড়া)

```python
def generate_mock_data(n_samples=600, seq_length=30, n_features=14, n_classes=3):
    """মক ডেটা জেনারেট (যদি ডে 56 ডেটা না থাকে)"""
    np.random.seed(42)
    
    X = np.random.randn(n_samples, seq_length, n_features).astype(np.float32)
    
    # কিছু প্যাটার্ন যোগ করুন
    for i in range(n_samples):
        trend = np.random.choice([-1, 0, 1])
        X[i, :, 0] += np.linspace(0, trend * 0.5, seq_length)  # রিটার্ন ফিচারে ট্রেন্ড
    
    # টার্গেট জেনারেট
    y = np.zeros(n_samples, dtype=np.int64)
    for i in range(n_samples):
        # লাস্ট কয়েক স্টেপের ভিত্তিতে ক্লাস নির্ধারণ
        last_returns = X[i, -5:, 0]
        avg_return = np.mean(last_returns)
        if avg_return > 0.15:
            y[i] = 2  # UP
        elif avg_return < -0.15:
            y[i] = 0  # DOWN
        else:
            y[i] = 1  # NEUTRAL
    
    return torch.FloatTensor(X), torch.LongTensor(y)

class MockDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# ট্রেন/ভ্যাল/টেস্ট স্প্লিট
X, y = generate_mock_data(n_samples=800, seq_length=30, n_features=14)
n_train, n_val, n_test = 500, 100, 200

train_dataset = MockDataset(X[:n_train], y[:n_train])
val_dataset = MockDataset(X[n_train:n_train+n_val], y[n_train:n_train+n_val])
test_dataset = MockDataset(X[-n_test:], y[-n_test:])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

print("=== ডেটা লোডেড ===")
print(f"ট্রেন: {len(train_dataset)}, ভ্যাল: {len(val_dataset)}, টেস্ট: {len(test_dataset)}")
sample_X, sample_y = next(iter(train_loader))
print(f"ব্যাচ শেপ: X={sample_X.shape}, y={sample_y.shape}")
```

## 3. ট্রেনিং ফাংশন

```python
class ModelTrainer:
    """কমপ্লিট ট্রেনিং পাইপলাইন"""
    def __init__(self, model, device):
        self.model = model.to(device)
        self.device = device
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(
            model.parameters(), lr=0.001, weight_decay=1e-4
        )
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=5, verbose=True
        )
        self.best_val_loss = float('inf')
        self.patience = 10
        self.patience_counter = 0
    
    def train_epoch(self, loader):
        """এক এপোক ট্রেন"""
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for X_batch, y_batch in loader:
            X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(X_batch)
            loss = self.criterion(outputs, y_batch)
            loss.backward()
            
            # গ্রেডিয়েন্ট ক্লিপিং
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += y_batch.size(0)
            correct += predicted.eq(y_batch).sum().item()
        
        return total_loss / len(loader), 100.0 * correct / total
    
    def validate(self, loader):
        """ভ্যালিডেশন"""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for X_batch, y_batch in loader:
                X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
                outputs = self.model(X_batch)
                loss = self.criterion(outputs, y_batch)
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += y_batch.size(0)
                correct += predicted.eq(y_batch).sum().item()
        
        return total_loss / len(loader), 100.0 * correct / total
    
    def train(self, train_loader, val_loader, epochs=100):
        """সম্পূর্ণ ট্রেনিং"""
        history = {
            'train_loss': [], 'train_acc': [],
            'val_loss': [], 'val_acc': []
        }
        
        print("\n=== LSTM মডেল ট্রেনিং শুরু ===")
        print(f"{'এপোক':<6} {'ট্রেন লস':<12} {'ট্রেন অ্যাক':<12} {'ভ্যাল লস':<12} {'ভ্যাল অ্যাক':<12} {'LR':<10}")
        print("-" * 55)
        
        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)
            
            history['train_loss'].append(train_loss)
            history['train_acc'].append(train_acc)
            history['val_loss'].append(val_loss)
            history['val_acc'].append(val_acc)
            
            self.scheduler.step(val_loss)
            current_lr = self.optimizer.param_groups[0]['lr']
            
            # Early stopping চেক
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                # বেস্ট মডেল সেভ
                torch.save(self.model.state_dict(), 'best_lstm_model.pth')
            else:
                self.patience_counter += 1
            
            if (epoch + 1) % 10 == 0 or epoch == 0:
                print(f"{epoch+1:<6} {train_loss:<12.4f} {train_acc:<12.2f} {val_loss:<12.4f} {val_acc:<12.2f} {current_lr:<10.6f}")
            
            if self.patience_counter >= self.patience:
                print(f"⏹️ Early stopping at epoch {epoch+1}")
                break
        
        print(f"\n✅ ট্রেনিং সম্পন্ন! বেস্ট ভ্যাল লস: {self.best_val_loss:.4f}")
        
        # বেস্ট মডেল লোড
        self.model.load_state_dict(torch.load('best_lstm_model.pth'))
        
        return history

# ট্রেনিং
trainer = ModelTrainer(model, device)
history = trainer.train(train_loader, val_loader, epochs=50)
```

## 4. অ্যানালাইসিস এবং ভিজুয়ালাইজেশন

```python
class TrainingVisualizer:
    """ট্রেনিং ভিজুয়ালাইজেশন"""
    
    @staticmethod
    def plot_history(history):
        """লস এবং অ্যাকুরেসি প্লট"""
        epochs = range(1, len(history['train_loss']) + 1)
        
        print("\n=== ট্রেনিং ফলাফল ===")
        print(f"বেস্ট ভ্যাল অ্যাকুরেসি: {max(history['val_acc']):.2f}%")
        print(f"ফাইনাল ট্রেন অ্যাকুরেসি: {history['train_acc'][-1]:.2f}%")
        print(f"ফাইনাল ভ্যাল অ্যাকুরেসি: {history['val_acc'][-1]:.2f}%")
        
        # ওভারফিটিং চেক
        train_val_gap = np.array(history['train_acc']) - np.array(history['val_acc'])
        avg_gap = np.mean(train_val_gap[-10:])
        if avg_gap > 10:
            print("⚠️ সম্ভাব্য ওভারফিটিং (ট্রেন-ভ্যাল গ্যাপ > 10%)")
        elif avg_gap < 3:
            print("✅ গুড — ওভারফিটিং নগণ্য")
        else:
            print("📊 গ্রহণযোগ্য — কিছু ওভারফিটিং কিন্তু ঠিক আছে")
        
        return {
            'best_val_acc': max(history['val_acc']),
            'final_val_acc': history['val_acc'][-1],
            'train_val_gap': avg_gap
        }

# ভিজুয়ালাইজ
visualizer = TrainingVisualizer()
metrics = visualizer.plot_history(history)
```

## 5. মডেল টেস্টিং

```python
class ModelTester:
    """মডেল টেস্টিং এবং ইভালুয়েশন"""
    
    def __init__(self, model, device):
        self.model = model.to(device)
        self.device = device
        self.model.eval()
    
    def test(self, test_loader):
        """টেস্ট সেট ইভালুয়েশন"""
        correct = 0
        total = 0
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
                outputs = self.model(X_batch)
                
                probs = F.softmax(outputs, dim=1)
                _, predicted = outputs.max(1)
                
                total += y_batch.size(0)
                correct += predicted.eq(y_batch).sum().item()
                
                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(y_batch.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        accuracy = 100.0 * correct / total
        
        print("\n=== মডেল টেস্ট রেজাল্টস ===")
        print(f"টেস্ট অ্যাকুরেসি: {accuracy:.2f}%")
        print(f"টেস্ট স্যাম্পল: {total}")
        
        # ক্লাস-ওয়াইজ অ্যাকুরেসি
        classes = ['DOWN 📉', 'NEUTRAL ➡️', 'UP 📈']
        print("\nপার ক্লাস অ্যাকুরেসি:")
        for i in range(3):
            mask = np.array(all_labels) == i
            if mask.sum() > 0:
                class_acc = (np.array(all_preds)[mask] == i).mean() * 100
                print(f"  {classes[i]}: {class_acc:.1f}% ({mask.sum()} স্যাম্পল)")
        
        return {
            'accuracy': accuracy,
            'predictions': all_preds,
            'labels': all_labels,
            'probabilities': all_probs
        }

# টেস্টিং
tester = ModelTester(model, device)
test_results = tester.test(test_loader)
```

## 6. প্রেডিকশন ডেমো

```python
def predict_trend(model, sequence, device):
    """একটি সিকোয়েন্সের জন্য ট্রেন্ড প্রেডিক্ট"""
    model.eval()
    
    with torch.no_grad():
        x = torch.FloatTensor(sequence).unsqueeze(0).to(device)  # (1, seq, features)
        outputs = model(x)
        probs = F.softmax(outputs, dim=1)
        pred = outputs.argmax(dim=1).item()
    
    labels = {0: 'ডাউনট্রেন্ড 📉', 1: 'সাইডওয়েজ ➡️', 2: 'আপট্রেন্ড 📈'}
    conf = probs[0][pred].item()
    
    print(f"\n=== প্রেডিকশন ফলাফল ===")
    print(f"প্রেডিক্টেড ট্রেন্ড: {labels[pred]}")
    print(f"কনফিডেন্স: {conf:.2%}")
    print(f"সম্ভাবনা:")
    for i in range(3):
        print(f"  {labels[i]}: {probs[0][i].item():.2%}")
    
    return pred, conf

# ডেমো প্রেডিকশন
sample_seq, _ = next(iter(test_loader))
demo_seq = sample_seq[0].cpu().numpy()
print("\n🔮 ডেমো প্রেডিকশন:")
predict_trend(model, demo_seq, device)
```

## সারাংশ
- LSTM মডেল তৈরি: 2-লেয়ার LSTM + অ্যাটেনশন + ক্লাসিফায়ার
- Bidirectional LSTM টেম্পোরাল কনটেক্সট ক্যাপচার করে
- অ্যাটেনশন মেকানিজম গুরুত্বপূর্ণ টাইমস্টেপে ফোকাস করে
- AdamW + ReduceLROnPlateau + Early Stopping ব্যবহার
- সিন্থেটিক ডেটা দিয়ে ডেমো ট্রেনিং সম্পন্ন (Day 56 থেকে রিয়েল ডেটা দিয়ে পুনরায় ট্রেন)
- মডেল 3 ক্লাস: DOWN / NEUTRAL / UP প্রেডিক্ট করে