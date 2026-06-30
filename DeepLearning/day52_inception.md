# Day 52: Inception Network — গুগলনেট 🌐🧩

## Inception নেটওয়ার্ক কী?
Inception (GoogLeNet) একই লেয়ারে বিভিন্ন সাইজের কনভোলিউশন অপারেশন প্যারালেলভাবে ব্যবহার করে।

### মূল আইডিয়া
একই ইনপুটে 1×1, 3×3, 5×5 কনভোলিউশন + 3×3 ম্যাক্সপুলিং → সব কনক্যাট → পরবর্তী লেয়ার

### Inception মডিউল
```
ইনপুট
  │
  ├── 1×1 Conv ──→ 3×3 Conv ──→
  ├── 1×1 Conv ──→ 5×5 Conv ──→  কনক্যাট → আউটপুট
  ├── 3×3 MaxPool ──→ 1×1 Conv ──→
  └── 1×1 Conv ─────────────────→
```

### ফিন্যান্সে Inception
- মাল্টি-স্কেল টাইম সিরিজ অ্যানালাইসিস
- বিভিন্ন টাইমফ্রেমের প্যাটার্ন ক্যাপচার (দিন, সপ্তাহ, মাস)
- মাল্টি-এসেট ফিচার ইন্টিগ্রেশন
- ক্রস-মার্কেট ফ্যাক্টর অ্যানালাইসিস

## Inception ইমপ্লিমেন্টেশন (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. বেসিক Inception মডিউল

```python
class InceptionModule(nn.Module):
    """Inception মডিউল (1D — টাইম সিরিজের জন্য)"""
    def __init__(self, in_channels, out_1x1, red_3x3, out_3x3, 
                 red_5x5, out_5x5, out_pool):
        super().__init__()
        
        # 1×1 কনভ পাথ
        self.branch1 = nn.Sequential(
            nn.Conv1d(in_channels, out_1x1, kernel_size=1),
            nn.BatchNorm1d(out_1x1),
            nn.ReLU(inplace=True)
        )
        
        # 1×1 → 3×3 কনভ পাথ
        self.branch2 = nn.Sequential(
            nn.Conv1d(in_channels, red_3x3, kernel_size=1),
            nn.BatchNorm1d(red_3x3),
            nn.ReLU(inplace=True),
            nn.Conv1d(red_3x3, out_3x3, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_3x3),
            nn.ReLU(inplace=True)
        )
        
        # 1×1 → 5×5 কনভ পাথ
        self.branch3 = nn.Sequential(
            nn.Conv1d(in_channels, red_5x5, kernel_size=1),
            nn.BatchNorm1d(red_5x5),
            nn.ReLU(inplace=True),
            nn.Conv1d(red_5x5, out_5x5, kernel_size=5, padding=2),
            nn.BatchNorm1d(out_5x5),
            nn.ReLU(inplace=True)
        )
        
        # 3×3 ম্যাক্সপুল → 1×1 কনভ পাথ
        self.branch4 = nn.Sequential(
            nn.MaxPool1d(kernel_size=3, stride=1, padding=1),
            nn.Conv1d(in_channels, out_pool, kernel_size=1),
            nn.BatchNorm1d(out_pool),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        branch1 = self.branch1(x)
        branch2 = self.branch2(x)
        branch3 = self.branch3(x)
        branch4 = self.branch4(x)
        
        # সব ব্রাঞ্চ কনক্যাট (চ্যানেল ডাইমেনশনে)
        outputs = [branch1, branch2, branch3, branch4]
        return torch.cat(outputs, dim=1)

# ডেমো
inception = InceptionModule(
    in_channels=64, 
    out_1x1=32, 
    red_3x3=32, out_3x3=64,
    red_5x5=16, out_5x5=32,
    out_pool=32
)
x = torch.randn(2, 64, 50)
out = inception(x)
total_channels = 32 + 64 + 32 + 32  # = 160
print(f"Inception মডিউল: {x.shape} → {out.shape}")
print(f"আউটপুট চ্যানেল: {out.shape[1]} (32+64+32+32=160)")
```

## 2. সম্পূর্ণ Inception নেটওয়ার্ক (GoogLeNet)

```python
class GoogLeNet1D(nn.Module):
    """1D GoogLeNet — টাইম সিরিজের জন্য"""
    def __init__(self, in_channels=1, num_classes=3):
        super().__init__()
        
        # স্টেম (প্রথম কয়েকটি লেয়ার)
        self.stem = nn.Sequential(
            nn.Conv1d(in_channels, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=3, stride=2, padding=1),
            
            nn.Conv1d(64, 64, kernel_size=1),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.Conv1d(64, 192, kernel_size=3, padding=1),
            nn.BatchNorm1d(192),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        )
        
        # Inception মডিউলস (3a, 3b → পুল → 4a, 4b, 4c, 4d, 4e → পুল → 5a, 5b)
        self.inception3a = InceptionModule(192, 64, 96, 128, 16, 32, 32)
        self.inception3b = InceptionModule(256, 128, 128, 192, 32, 96, 64)
        
        self.pool3 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        self.inception4a = InceptionModule(480, 192, 96, 208, 16, 48, 64)
        self.inception4b = InceptionModule(512, 160, 112, 224, 24, 64, 64)
        self.inception4c = InceptionModule(512, 128, 128, 256, 24, 64, 64)
        self.inception4d = InceptionModule(512, 112, 144, 288, 32, 64, 64)
        self.inception4e = InceptionModule(528, 256, 160, 320, 32, 128, 128)
        
        self.pool4 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        self.inception5a = InceptionModule(832, 256, 160, 320, 32, 128, 128)
        self.inception5b = InceptionModule(832, 384, 192, 384, 48, 128, 128)
        
        # ক্লাসিফায়ার
        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.dropout = nn.Dropout(0.4)
        self.fc = nn.Linear(1024, num_classes)
    
    def forward(self, x):
        x = self.stem(x)
        
        x = self.inception3a(x)
        x = self.inception3b(x)
        x = self.pool3(x)
        
        x = self.inception4a(x)
        x = self.inception4b(x)
        x = self.inception4c(x)
        x = self.inception4d(x)
        x = self.inception4e(x)
        x = self.pool4(x)
        
        x = self.inception5a(x)
        x = self.inception5b(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.dropout(x)
        x = self.fc(x)
        
        return x

# ডেমো
googlenet = GoogLeNet1D(in_channels=1, num_classes=3).to(device)
print(f"GoogLeNet (1D) — মডেল তৈরি হয়েছে")
dummy = torch.randn(2, 1, 256).to(device)
out = googlenet(dummy)
print(f"ইনপুট: {dummy.shape} → আউটপুট: {out.shape}")
```

## 3. মাল্টি-স্কেল টাইম সিরিজ ক্লাসিফিকেশন

```python
class MultiScaleTimeSeriesClassifier:
    """মাল্টি-স্কেল টাইম সিরিজ ক্লাসিফায়ার (Inception বেসড)"""
    def __init__(self, seq_length=256, num_classes=3):
        self.seq_length = seq_length
        self.num_classes = num_classes
        
        self.model = GoogLeNet1D(in_channels=1, num_classes=num_classes).to(device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0005)
    
    def _generate_multi_scale_data(self, n_samples=400):
        """মাল্টি-স্কেল প্যাটার্ন সহ সিন্থেটিক ডেটা"""
        X, y = [], []
        
        for _ in range(n_samples):
            seq = np.zeros(self.seq_length)
            trend_type = np.random.choice([0, 1, 2])  # 0: downtrend, 1: range, 2: uptrend
            
            # শর্ট-টার্ম প্যাটার্ন (দিন)
            short_term = np.random.randn(self.seq_length) * 0.3
            
            # মিড-টার্ম প্যাটার্ন (সপ্তাহ)
            mid_term = np.sin(np.linspace(0, 4*np.pi, self.seq_length)) * 0.5
            
            # লং-টার্ম প্যাটার্ন (মাস/ট্রেন্ড)
            if trend_type == 2:
                long_term = np.linspace(0, 2, self.seq_length)
            elif trend_type == 0:
                long_term = np.linspace(0, -2, self.seq_length)
            else:
                long_term = np.zeros(self.seq_length)
            
            seq = short_term + mid_term + long_term
            X.append(seq)
            y.append(trend_type)
        
        X = np.array(X, dtype=np.float32).reshape(-1, 1, self.seq_length)
        y = np.array(y, dtype=np.int64)
        
        return torch.FloatTensor(X), torch.LongTensor(y)
    
    def train(self, epochs=30, batch_size=16):
        """ট্রেনিং"""
        X, y = self._generate_multi_scale_data()
        dataset = torch.utils.data.TensorDataset(X, y)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.model.train()
        
        for epoch in range(epochs):
            epoch_loss = 0
            correct = 0
            total = 0
            
            for batch_X, batch_y in loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                _, predicted = outputs.max(1)
                total += batch_y.size(0)
                correct += predicted.eq(batch_y).sum().item()
            
            acc = 100.0 * correct / total
            if (epoch + 1) % 10 == 0:
                print(f"এপোক {epoch+1}/{epochs}: লস={epoch_loss/len(loader):.4f}, "
                      f"অ্যাকুরেসি={acc:.2f}%")
    
    def predict_multi_scale(self, time_series):
        """মাল্টি-স্কেল প্রেডিকশন"""
        self.model.eval()
        with torch.no_grad():
            x = torch.FloatTensor(time_series).reshape(1, 1, -1).to(device)
            outputs = self.model(x)
            probs = F.softmax(outputs, dim=-1)
            pred = outputs.argmax(dim=-1).item()
        
        labels = ['ডাউনট্রেন্ড 📉', 'সাইডওয়েজ ➡️', 'আপট্রেন্ড 📈']
        return {
            'prediction': labels[pred],
            'confidence': float(probs[0][pred]),
            'all_probs': {labels[i]: float(probs[0][i]) for i in range(3)}
        }

# ডেমো
print("\n=== মাল্টি-স্কেল Inception ট্রেনিং ===")
classifier = MultiScaleTimeSeriesClassifier(seq_length=256, num_classes=3)
classifier.train(epochs=30)

# টেস্ট
test_seq = np.sin(np.linspace(0, 3*np.pi, 256)) + np.linspace(0, 1.5, 256) + np.random.randn(256)*0.3
result = classifier.predict_multi_scale(test_seq)
print(f"\nমাল্টি-স্কেল প্রেডিকশন: {result['prediction']} (কনফিডেন্স: {result['confidence']:.2%})")
```

## 4. Inception vs প্লেইন CNN

```python
class InceptionVsPlainCNN:
    """Inception vs প্লেইন CNN তুলনা"""
    
    @staticmethod
    def compare_architectures():
        """আর্কিটেকচার তুলনা"""
        print("""
=== Inception vs প্লেইন CNN তুলনা ===

প্লেইন CNN:
  - ক্রমিক কনভোলিউশন (3×3 → 3×3 → 3×3)
  - একক স্কেল ফিচার
  - সীমিত রিসেপটিভ ফিল্ড

Inception নেটওয়ার্ক:
  - প্যারালেল মাল্টি-স্কেল কনভোলিউশন
  - 1×1: পিক্সেল-ওয়াইজ ফিচার
  - 3×3: লোকাল প্যাটার্নস
  - 5×5: বড় রিসেপটিভ ফিল্ড
  - পুলিং: ইমেজ প্রসেসিং (পুলিং ব্রাঞ্চ)
  
প্যারামিটার এফিশিয়েন্সি:
  - Inception-এ 1×1 বটলনেক → প্যারামিটার কমায়
  - উদাহরণ: 192×256 3×3 = 442K প্যারামিটার
  - 1×1(96) + 3×3(256) = 31K + 221K = 252K (43% কম!)
""")
    
    @staticmethod
    def financial_applications():
        """ফিন্যান্স অ্যাপ্লিকেশন"""
        print("""
=== ফিন্যান্সে Inception এর ব্যবহার ===

1️⃣ মাল্টি-টাইমফ্রেম অ্যানালাইসিস
   - 1×1 conv: intraday প্যাটার্ন
   - 3×3 conv: দৈনিক প্যাটার্ন
   - 5×5 conv: সাপ্তাহিক প্যাটার্ন

2️⃣ মাল্টি-এসেট ফিচার ফিউশন
   - বিভিন্ন এসেটের (স্টক, বন্ড, কমোডিটি) ফিচার কম্বাইন
   - ইন্টার-মার্কেট রিলেশনশিপ ক্যাপচার

3️⃣ ক্রস-টাইমফ্রেম সিগন্যাল
   - স্বল্প এবং দীর্ঘমেয়াদী সিগন্যাল একসাথে
   - ট্রেন্ড রিভার্সাল ডিটেকশন
""")

InceptionVsPlainCNN.compare_architectures()
InceptionVsPlainCNN.financial_applications()
```

## 5. অক্সিলিয়ারি ক্লাসিফায়ার

```python
class InceptionAuxiliary(nn.Module):
    """অক্সিলিয়ারি ক্লাসিফায়ার (GoogLeNet-এ ব্যবহৃত)"""
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool1d(4)
        self.conv = nn.Conv1d(in_channels, 128, kernel_size=1)
        self.bn = nn.BatchNorm1d(128)
        self.relu = nn.ReLU(inplace=True)
        self.fc1 = nn.Linear(128 * 4, 1024)
        self.fc2 = nn.Linear(1024, num_classes)
        self.dropout = nn.Dropout(0.7)
    
    def forward(self, x):
        x = self.pool(x)
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

print("\n=== অক্সিলিয়ারি ক্লাসিফায়ার ===")
aux = InceptionAuxiliary(512, 3)
x = torch.randn(2, 512, 20)
out = aux(x)
print(f"অক্সিলিয়ারি আউটপুট: {out.shape}")
print("অক্সিলিয়ারি ক্লাসিফায়ার ট্রেনিংয়ের সময় গ্রেডিয়েন্ট ফ্লো সাহায্য করে")
```

## সারাংশ
- Inception নেটওয়ার্ক মাল্টি-স্কেল ফিচার প্যারালেলভাবে শেখে
- 1×1 বটলনেক প্যারামিটার সংখ্যা drastically কমায়
- GoogLeNet (Inception v1) ILSVRC 2014 জিতেছিল
- অক্সিলিয়ারি ক্লাসিফায়ার গ্রেডিয়েন্ট ভ্যানিশিং কমায়
- ফিন্যান্সে মাল্টি-টাইমফ্রেম অ্যানালাইসিসের জন্য আদর্শ
- পরবর্তী ভারিয়েন্ট: Inception v2/v3 (Batch Normalization + Factorized Convolutions)