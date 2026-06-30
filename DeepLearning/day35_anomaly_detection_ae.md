# Day 35: অটোএনকোডার দিয়ে অ্যানোমালি ডিটেকশন 🚨

## অ্যানোমালি ডিটেকশন কী?
অ্যানোমালি বা অস্বাভাবিকতা ডিটেকশন হল ডেটাতে অস্বাভাবিক প্যাটার্ন শনাক্ত করা যা সাধারণ প্যাটার্ন থেকে বিচ্যুত।

### অটোএনকোডার দিয়ে কেন?
অটোএনকোডার শুধুমাত্র "নরমাল" ডেটা রিকন্সট্রাক্ট করতে শেখে। অ্যানোমালি থাকলে তা ভালোভাবে রিকন্সট্রাক্ট করতে পারে না → High reconstruction error.

```
নরমাল ডেটা: x → AE → x̂ (লো এরর) ✅
অ্যানোমালি:  x → AE → x̂ (হাই এরর) 🚨
```

### ফিন্যান্সে ব্যবহার
1. **ক্রেডিট কার্ড ফ্রড ডিটেকশন**
2. **মার্কেট ম্যানিপুলেশন ডিটেকশন**
3. **অস্বাভাবিক ট্রেডিং প্যাটার্ন**
4. **ব্রোকার/ক্লায়েন্ট অ্যানোমালি**
5. **ফিন্যান্সিয়াল স্টেটমেন্ট ফ্রড**

## ডেটা জেনারেশন

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# সেটিংস
np.random.seed(42)
torch.manual_seed(42)

N_NORMAL = 5000
N_ANOMALY = 100
N_FEATURES = 30

# নরমাল ডেটা (ফ্যাক্টর মডেল)
true_factors = np.random.randn(N_NORMAL, 3)
W = np.random.randn(3, N_FEATURES)
normal_data = true_factors @ W + np.random.randn(N_NORMAL, N_FEATURES) * 0.1

# অ্যানোমালি ডেটা (ভিন্ন জেনারেটিং প্রসেস)
anomaly_data = np.random.randn(N_ANOMALY, N_FEATURES) * 0.5 + 3  # শিফটেড

# কম্বাইন
X = np.vstack([normal_data, anomaly_data])
y = np.array([0]*N_NORMAL + [1]*N_ANOMALY)  # 0=নরমাল, 1=অ্যানোমালি

# শাফেল
perm = np.random.permutation(len(X))
X, y = X[perm], y[perm]

print(f"মোট ডেটা: {len(X)}")
print(f"  নরমাল: {(y==0).sum()}")
print(f"  অ্যানোমালি: {(y==1).sum()}")
print(f"  অ্যানোমালি রেশিও: {y.mean():.2%}")
print(f"ফিচারের সংখ্যা: {N_FEATURES}")
```

## অ্যানোমালি ডিটেকশন অটোএনকোডার

```python
class AnomalyDetector(nn.Module):
    """অ্যানোমালি ডিটেকশন অটোএনকোডার"""
    def __init__(self, input_dim, encoding_dim=8):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, encoding_dim)
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, input_dim)
        )
    
    def forward(self, x):
        return self.decoder(self.encoder(x))
    
    def reconstruction_error(self, x):
        """প্রতি স্যাম্পলের রিকন্সট্রাকশন MSE"""
        with torch.no_grad():
            recon = self(x)
            error = torch.mean((x - recon) ** 2, dim=1)
        return error.numpy()

# শুধু নরমাল ডেটা দিয়ে ট্রেন
normal_idx = np.where(y[:N_NORMAL] == 0)[0]
X_train = torch.FloatTensor(X[normal_idx])  # ট্রেনিং শুধু নরমাল

scaler = StandardScaler()
X_train_scaled = torch.FloatTensor(scaler.fit_transform(X_train.numpy()))

dataset = TensorDataset(X_train_scaled, X_train_scaled)
loader = DataLoader(dataset, batch_size=128, shuffle=True)

model = AnomalyDetector(input_dim=N_FEATURES, encoding_dim=6)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("মডেল ট্রেনিং (শুধু নরমাল ডেটা):")
epochs = 80
for epoch in range(epochs):
    total_loss = 0
    for bx, _ in loader:
        optimizer.zero_grad()
        recon = model(bx)
        loss = criterion(recon, bx)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 20 == 0:
        print(f"  Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")

print("✅ অ্যানোমালি ডিটেক্টর ট্রেনিং সম্পূর্ণ!")
```

## থ্রেশহোল্ড ডিটেকশন

```python
# ভ্যালিডেশন সেট থেকে থ্রেশহোল্ড নির্ধারণ
model.eval()

# ভ্যালিডেশন (নরমাল ডেটার একটি অংশ)
val_normal = X_train_scaled[:1000]
val_errors = model.reconstruction_error(val_normal)

# থ্রেশহোল্ড (৯৫তম পার্সেন্টাইল)
threshold = np.percentile(val_errors, 95)
print(f"রিকন্সট্রাকশন এরর স্ট্যাটিস্টিক্স (নরমাল ভ্যাল):")
print(f"  মিন: {val_errors.mean():.6f}")
print(f"  স্টাড: {val_errors.std():.6f}")
print(f"  মিডিয়ান: {np.median(val_errors):.6f}")
print(f"  ৯৫তম পার্সেন্টাইল (থ্রেশহোল্ড): {threshold:.6f}")
print(f"  ম্যাক্স: {val_errors.max():.6f}")

# থ্রেশহোল্ড ভিজুয়ালাইজেশন
print(f"\nএরর ডিস্ট্রিবিউশন:")
hist, edges = np.histogram(val_errors, bins=20)
for i in range(len(hist)):
    bar = '█' * (hist[i] // 10)
    print(f"  {edges[i]:.4f}-{edges[i+1]:.4f}: {bar} {hist[i]}")
print(f"  {'─'*30}")
print(f"  থ্রেশহোল্ড: {threshold:.4f}")
```

## টেস্ট সেট ইভালুয়েশন

```python
# টেস্ট ডেটা
X_test = torch.FloatTensor(X[N_NORMAL:])
y_test = y[N_NORMAL:]
X_test_scaled = torch.FloatTensor(scaler.transform(X_test.numpy()))

# এরর
test_errors = model.reconstruction_error(X_test_scaled)

# প্রেডিকশন
y_pred = (test_errors > threshold).astype(int)

# মেট্রিক্স
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accuracy = (y_pred == y_test).mean()

print(f"{'মেট্রিক':<20} {'মান':<15}")
print("-" * 35)
print(f"{'অ্যাকুরেসি':<20} {accuracy:<15.4f}")
print(f"{'প্রিসিশন':<20} {precision:<15.4f}")
print(f"{'রিকল':<20} {recall:<15.4f}")
print(f"{'F1-স্কোর':<20} {f1:<15.4f}")

# কনফিউশন ম্যাট্রিক্স
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nকনফিউশন ম্যাট্রিক্স:")
print(f"{'':<15} {'প্রেডিক্টেড নরমাল':<20} {'প্রেডিক্টেড অ্যানোমালি':<20}")
print(f"{'আসল নরমাল':<15} {cm[0][0]:<20} {cm[0][1]:<20}")
print(f"{'আসল অ্যানোমালি':<15} {cm[1][0]:<20} {cm[1][1]:<20}")

# থ্রেশহোল্ডের প্রভাব
print(f"\nবিভিন্ন থ্রেশহোল্ডে পারফরম্যান্স:")
for p in [80, 85, 90, 95, 99]:
    t = np.percentile(val_errors, p)
    yp = (test_errors > t).astype(int)
    f1_s = f1_score(y_test, yp)
    prec = precision_score(y_test, yp, zero_division=0)
    rec = recall_score(y_test, yp, zero_division=0)
    print(f"  {p}th percentile (thresh={t:.4f}): F1={f1_s:.4f}, "
          f"Prec={prec:.4f}, Rec={rec:.4f}")
```

## রিয়েল-টাইম অ্যানোমালি ডিটেকশন সিমুলেশন

```python
class RealTimeAnomalyDetector:
    """রিয়েল-টাইম অ্যানোমালি ডিটেকশন সিমুলেশন"""
    def __init__(self, model, scaler, threshold, window_size=10):
        self.model = model
        self.scaler = scaler
        self.threshold = threshold
        self.window_size = window_size
        self.history = []
        self.alerts = []
    
    def process(self, sample):
        """নতুন স্যাম্পল প্রসেস"""
        sample_scaled = self.scaler.transform(sample.reshape(1, -1))
        sample_tensor = torch.FloatTensor(sample_scaled)
        
        error = self.model.reconstruction_error(sample_tensor)[0]
        is_anomaly = error > self.threshold
        
        self.history.append(error)
        
        if is_anomaly:
            self.alerts.append({
                'error': error,
                'threshold': self.threshold,
                'severity': (error / self.threshold - 1) * 100
            })
        
        return is_anomaly, error
    
    def get_stats(self):
        if len(self.alerts) == 0:
            return "কোন অ্যালার্ম নেই"
        
        return {
            'total_alerts': len(self.alerts),
            'avg_severity': np.mean([a['severity'] for a in self.alerts]),
            'max_severity': max(a['severity'] for a in self.alerts)
        }

# ডিটেক্টর
detector = RealTimeAnomalyDetector(model, scaler, threshold)

# সিমুলেশন
print("রিয়েল-টাইম অ্যানোমালি ডিটেকশন সিমুলেশন:")
print(f"{'স্টেপ':<10} {'এরর':<15} {'থ্রেশহোল্ড':<15} {'স্ট্যাটাস':<15}")
print("-" * 55)

for i in range(50):
    if i < 40:
        sample = normal_data[i % len(normal_data)]
    else:
        sample = anomaly_data[i - 40]
    
    is_anom, error = detector.process(sample)
    status = "🚨 অ্যানোমালি!" if is_anom else "✅ নরমাল"
    print(f"{i+1:<10} {error:<15.6f} {threshold:<15.6f} {status:<15}")

stats = detector.get_stats()
if isinstance(stats, dict):
    print(f"\n📊 ডিটেকশন স্ট্যাটিস্টিক্স:")
    print(f"  মোট অ্যালার্ম: {stats['total_alerts']}")
    print(f"  গড় সিভিয়ারিটি: {stats['avg_severity']:.2f}%")
    print(f"  সর্বোচ্চ সিভিয়ারিটি: {stats['max_severity']:.2f}%")
```

## অ্যাডভান্সড ফিচার: কনটেক্সচুয়াল অ্যানোমালি

```python
class ContextualAnomalyDetector(nn.Module):
    """কনটেক্সট সহ অ্যানোমালি ডিটেক্টর"""
    def __init__(self, input_dim, context_dim=5, encoding_dim=8):
        super().__init__()
        
        self.context_encoder = nn.Linear(context_dim, 16)
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim + 16, 64),
            nn.ReLU(),
            nn.Linear(64, encoding_dim)
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim + 16, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )
    
    def forward(self, x, context):
        c = torch.relu(self.context_encoder(context))
        
        encoded = self.encoder(torch.cat([x, c], dim=1))
        decoded = self.decoder(torch.cat([encoded, c], dim=1))
        return decoded

# কনটেক্সট উদাহরণ: দিনের সময়, ভলাটিলিটি, ইত্যাদি
context = np.random.randn(len(X), 5)  # সিমুলেটেড কনটেক্সট

print("✅ কনটেক্সচুয়াল অ্যানোমালি ডিটেক্টর ডিফাইন্ড")
print("উদাহরণ: মার্কেট আওয়ার-ভিত্তিক থ্রেশহোল্ড অ্যাডজাস্টমেন্ট")
```

## থ্রেশহোল্ড অ্যাডজাস্টমেন্ট স্ট্র্যাটেজি

```python
def adaptive_threshold(errors, base_percentile=95, window=100):
    """অ্যাডাপ্টিভ থ্রেশহোল্ড"""
    thresholds = []
    for i in range(window, len(errors)):
        recent = errors[i-window:i]
        thresholds.append(np.percentile(recent, base_percentile))
    
    return np.array(thresholds)

# সিমুলেটেড এররস
timestamps = np.arange(1000)
errors = np.random.exponential(0.5, 1000)
errors[500:550] += 2  # অ্যানোমালি পিরিয়ড

adaptive_thresh = adaptive_threshold(errors)
fixed_thresh = np.percentile(errors[:100], 95)

print(f"ফিক্সড থ্রেশহোল্ড: {fixed_thresh:.4f}")
print(f"অ্যাডাপ্টিভ থ্রেশহোল্ড:")
print(f"  মিন: {adaptive_thresh.mean():.4f}")
print(f"  স্টাড: {adaptive_thresh.std():.4f}")
print(f"  রেঞ্জ: [{adaptive_thresh.min():.4f}, {adaptive_thresh.max():.4f}]")
print("✅ অ্যাডাপ্টিভ থ্রেশহোল্ড মার্কেট কন্ডিশনের সাথে খাপ খাইয়ে নেয়")
```

## বেস্ট প্র্যাকটিস

### 1. ডেটা প্রিপ্রসেসিং
- শুধু নরমাল ডেটা দিয়ে ট্রেন করুন
- আউটলায়ার ট্রেনিং সেট থেকে বাদ দিন
- নরমালাইজেশন আবশ্যক

### 2. মডেল সিলেকশন
```python
# Undercomplete AE (এনকোডিং < ইনপুট): স্ট্যান্ডার্ড
# Overcomplete AE (এনকোডিং > ইনপুট): স্পার্সিটি রেগুলারাইজেশন প্রয়োজন
# Denoising AE: নয়েজি ডেটার জন্য
```

### 3. থ্রেশহোল্ড সিলেকশন
- ভ্যালিডেশন সেট থেকে নির্ধারণ
- বিজনেস কস্ট (False Positive vs False Negative)
- সিজনাল/টাইম-ভেরিয়েন্ট থ্রেশহোল্ড

### 4. মনিটরিং
- এরর ডিস্ট্রিবিউশন ট্র্যাক করুন
- ড্রিফট ডিটেক্ট করুন
- পিরিওডিক্যালি রিট্রেন করুন

```python
print("✅ অ্যানোমালি ডিটেকশন সম্পূর্ণ")
print(f"মডেল: {N_FEATURES}D → 6D → {N_FEATURES}D")
print(f"থ্রেশহোল্ড: 95th percentile ({threshold:.6f})")
if 'f1' in dir():
    print(f"টেস্ট F1-স্কোর: {f1:.4f}")
```

## সারাংশ
- অটোএনকোডার অ্যানোমালি ডিটেকশনের জন্য শক্তিশালী টুল
- উচ্চ রিকন্সট্রাকশন এরর → অ্যানোমালি ইনডিকেটর
- শুধু নরমাল ডেটা দিয়ে ট্রেনিং প্রয়োজন
- থ্রেশহোল্ড সিলেকশন ক্রিটিক্যাল
- ফিন্যান্সে ফ্রড, ম্যানিপুলেশন, অস্বাভাবিক ট্রেডিং ডিটেকশনে ব্যবহৃত
- অ্যাডাপ্টিভ থ্রেশহোল্ড মার্কেট কন্ডিশনের সাথে মানিয়ে নেয়