# Day 31: অটোএনকোডার (Autoencoder) 🔄

## অটোএনকোডার কী?
অটোএনকোডার একটি আনসুপারভাইজড নিউরাল নেটওয়ার্ক যা ডেটাকে কম্প্রেস করে পুনরায় ডিকোড করতে শেখে। এটি আউটপুটকে ইনপুটের মতো করার চেষ্টা করে।

### আর্কিটেকচার
```
ইনপুট → [এনকোডার] → ল্যাটেন্ট স্পেস → [ডিকোডার] → আউটপুট
  x         f(x)          z               g(z)         x̂
(উচ্চ-মাত্রিক)         (নিম্ন-মাত্রিক)              (পুনর্নির্মিত)
```

### কেন অটোএনকোডার?
1. **ডাইমেনশনালিটি রিডাকশন**: PCA-র মতো কিন্তু নন-লিনিয়ার
2. **ফিচার লার্নিং**: আনসুপারভাইজড ফিচার এক্সট্র্যাকশন
3. **ডিনয়েজিং**: নয়েজি ডেটা ক্লিন করা
4. **অ্যানোমালি ডিটেকশন**: অস্বাভাবিক ডেটা পয়েন্ট খুঁজা
5. **জেনারেশন**: নতুন ডেটা তৈরি (VAE)

### ফিন্যান্স অ্যাপ্লিকেশন
- ফ্রড ডিটেকশন (ক্রেডিট কার্ড)
- মার্কেট অ্যানোমালি ডিটেকশন
- নয়েজি ফিন্যান্সিয়াল ডেটা ক্লিনিং
- ফিচার এক্সট্র্যাকশন (স্টক ফ্যাক্টর)

## সিম্পল অটোএনকোডার

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

class Autoencoder(nn.Module):
    """বেসিক অটোএনকোডার"""
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        
        # এনকোডার
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, encoding_dim),
            nn.ReLU()  # ল্যাটেন্ট স্পেস
        )
        
        # ডিকোডার
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim),
            nn.Sigmoid()  # 0-1 রেঞ্জের জন্য
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def encode(self, x):
        """ল্যাটেন্ট রিপ্রেজেন্টেশন পেতে"""
        return self.encoder(x)

# টেস্ট
autoencoder = Autoencoder(input_dim=50, encoding_dim=10)
x = torch.randn(16, 50)
reconstructed = autoencoder(x)
print(f"ইনপুট শেপ: {x.shape}")
print(f"রিকন্সট্রাক্টেড শেপ: {reconstructed.shape}")
print(f"ল্যাটেন্ট ডাইমেনশন: 10 (কম্প্রেশন রেশিও: 5x)")
```

## সিন্থেটিক ফিন্যান্সিয়াল ডেটা

```python
# ফিন্যান্সিয়াল ফিচার ডেটা
np.random.seed(42)
n_samples = 5000
n_features = 30

# রিয়েলিস্টিক ফিন্যান্সিয়াল ফিচার
financial_data = np.zeros((n_samples, n_features))

# ফ্যাক্টর-বেসড ডেটা
factors = np.random.randn(n_samples, 5)  # ৫টি ল্যাটেন্ট ফ্যাক্টর
factor_loading = np.random.randn(5, n_features)

# ডেটা জেনারেট (ফ্যাক্টর মডেল)
financial_data = factors @ factor_loading
financial_data += np.random.randn(n_samples, n_features) * 0.1  # নয়েজ
financial_data = (financial_data - financial_data.min()) / \
                 (financial_data.max() - financial_data.min())  # 0-1 নরমালাইজ

data_tensor = torch.FloatTensor(financial_data)
dataset = TensorDataset(data_tensor, data_tensor)  # ইনপুট = আউটপুট
loader = DataLoader(dataset, batch_size=64, shuffle=True)

print(f"ফিন্যান্সিয়াল ডেটা: {financial_data.shape}")
print(f"ভ্যালু রেঞ্জ: [{financial_data.min():.4f}, {financial_data.max():.4f}]")
```

## অটোএনকোডার ট্রেনিং

```python
# মডেল
model = Autoencoder(input_dim=n_features, encoding_dim=8)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ট্রেনিং
epochs = 100
loss_history = []

for epoch in range(epochs):
    total_loss = 0
    for batch_x, _ in loader:
        optimizer.zero_grad()
        reconstructed = model(batch_x)
        loss = criterion(reconstructed, batch_x)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    avg_loss = total_loss / len(loader)
    loss_history.append(avg_loss)
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")

# ফাইনাল ইভালুয়েশন
model.eval()
with torch.no_grad():
    test_data = torch.FloatTensor(financial_data[:100])
    reconstructed = model(test_data)
    final_loss = criterion(reconstructed, test_data).item()

print(f"\n✅ ট্রেনিং সম্পূর্ণ! ফাইনাল MSE: {final_loss:.6f}")
print(f"কম্প্রেশন: {n_features} → 8 → {n_features} ({n_features/8:.1f}x)")
```

## অটোএনকোডার ভিজুয়ালাইজেশন

```python
# রিকন্সট্রাকশন ভিজুয়ালাইজ
model.eval()
with torch.no_grad():
    sample = torch.FloatTensor(financial_data[:5])
    recon = model(sample)

print("প্রথম ৫ স্যাম্পলের রিকন্সট্রাকশন:")
print(f"{'ফিচার':<10} {'আসল':<20} {'রিকন্সট্রাক্টেড':<20} {'এরর':<20}")
print("-" * 70)
for f in range(min(10, n_features)):
    orig = sample[0, f].item()
    rec = recon[0, f].item()
    err = abs(orig - rec)
    print(f"{f:<10} {orig:<20.6f} {rec:<20.6f} {err:<20.6f}")

# রিকন্সট্রাকশন এরর ডিস্ট্রিবিউশন
errors = []
for i in range(len(financial_data)):
    with torch.no_grad():
        recon = model(data_tensor[i:i+1])
        err = criterion(recon, data_tensor[i:i+1]).item()
        errors.append(err)

errors = np.array(errors)
print(f"\nএরর স্ট্যাটিস্টিক্স:")
print(f"  মিন: {errors.mean():.6f}")
print(f"  স্টাড: {errors.std():.6f}")
print(f"  ম্যাক্স: {errors.max():.6f}")
print(f"  ৯৫তম পার্সেন্টাইল: {np.percentile(errors, 95):.6f}")
```

## ল্যাটেন্ট স্পেস এক্সপ্লোরেশন

```python
class LatentSpaceExplorer:
    """ল্যাটেন্ট স্পেস অন্বেষণ"""
    def __init__(self, model):
        self.model = model
    
    def encode_data(self, data_loader):
        """সম্পূর্ণ ডেটার ল্যাটেন্ট রিপ্রেজেন্টেশন"""
        self.model.eval()
        latent_codes = []
        
        with torch.no_grad():
            for batch_x, _ in data_loader:
                latent = self.model.encode(batch_x)
                latent_codes.append(latent)
        
        return torch.cat(latent_codes).numpy()
    
    def interpolate(self, x1, x2, steps=10):
        """দুটি ডেটা পয়েন্টের মধ্যে ইন্টারপোলেশন"""
        z1 = self.model.encode(x1.unsqueeze(0))
        z2 = self.model.encode(x2.unsqueeze(0))
        
        alphas = np.linspace(0, 1, steps)
        interpolated = []
        
        for alpha in alphas:
            z = (1 - alpha) * z1 + alpha * z2
            with torch.no_grad():
                recon = self.model.decoder(z)
                interpolated.append(recon)
        
        return torch.cat(interpolated)

explorer = LatentSpaceExplorer(model)
latent_codes = explorer.encode_data(loader)

print(f"ল্যাটেন্ট কোডস শেপ: {latent_codes.shape}")
print(f"ল্যাটেন্ট স্পেস স্ট্যাটিস্টিক্স:")
for i in range(latent_codes.shape[1]):
    print(f"  ডাইমেনশন {i+1}: মিন={latent_codes[:,i].mean():.4f}, "
          f"স্টাড={latent_codes[:,i].std():.4f}")

# ইন্টারপোলেশন
x1 = data_tensor[0]
x2 = data_tensor[50]
interp = explorer.interpolate(x1, x2, steps=5)
print(f"\nইন্টারপোলেশন শেপ: {interp.shape}")
```

## অটোএনকোডারের ভ্যারিয়েন্টস

```python
class SparseAutoencoder(nn.Module):
    """স্পার্স অটোএনকোডার (L1 রেগুলারাইজেশন)"""
    def __init__(self, input_dim, encoding_dim, sparsity_weight=1e-3):
        super().__init__()
        self.sparsity_weight = sparsity_weight
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, encoding_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def get_sparsity_loss(self):
        """L1 স্পারসিটি লস"""
        sparsity_loss = 0
        for name, param in self.encoder.named_parameters():
            if 'weight' in name:
                sparsity_loss += torch.sum(torch.abs(param))
        return self.sparsity_weight * sparsity_loss

class DeepAutoencoder(nn.Module):
    """ডিপ অটোএনকোডার (আরও লেয়ার)"""
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        
        # এনকোডার (স্তরায়িত কম্প্রেশন)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, encoding_dim),
        )
        
        # ডিকোডার (স্তরায়িত এক্সপ্যানশন)
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, input_dim),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.decoder(self.encoder(x))
    
    def encode(self, x):
        return self.encoder(x)

# তুলনা
simple_ae = Autoencoder(30, 8)
deep_ae = DeepAutoencoder(30, 8)
sparse_ae = SparseAutoencoder(30, 8)

print(f"{'মডেল':<20} {'প্যারামিটার':<15}")
print("-" * 35)
print(f"{'সিম্পল AE':<20} {sum(p.numel() for p in simple_ae.parameters()):<15,}")
print(f"{'ডিপ AE':<20} {sum(p.numel() for p in deep_ae.parameters()):<15,}")
print(f"{'স্পার্স AE':<20} {sum(p.numel() for p in sparse_ae.parameters()):<15,}")
```

## অটোএনকোডার হাইপারপ্যারামিটার টিউনিং

```python
# এনকোডিং ডাইমেনশন টিউনিং
encoding_dims = [2, 4, 8, 16, 24]
results = []

for enc_dim in encoding_dims:
    model = Autoencoder(input_dim=n_features, encoding_dim=enc_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    # ২০ ইপক ট্রেইন
    for epoch in range(20):
        for bx, _ in loader:
            optimizer.zero_grad()
            loss = criterion(model(bx), bx)
            loss.backward()
            optimizer.step()
    
    # ইভালুয়েট
    model.eval()
    with torch.no_grad():
        val_loss = criterion(model(data_tensor[:200]), 
                            data_tensor[:200]).item()
    
    compression_ratio = n_features / enc_dim
    results.append((enc_dim, val_loss, compression_ratio))
    print(f"encoding_dim={enc_dim:<3}: Loss={val_loss:.6f}, "
          f"Compression={compression_ratio:.1f}x")

best = min(results, key=lambda r: r[1])
print(f"\n🏆 সেরা এনকোডিং ডাইমেনশন: {best[0]} "
      f"(Loss={best[1]:.6f}, Compression={best[2]:.1f}x)")
```

## প্র্যাকটিক্যাল টিপস

### 1. অ্যাক্টিভেশন ফাংশন
- 0-1 ডেটা: Sigmoid (আউটপুট)
- স্ট্যান্ডার্ড ডেটা: Linear (আউটপুট)

### 2. লস ফাংশন
- MSE (Mean Squared Error): সাধারণত সেরা
- BCE (Binary Cross Entropy): 0-1 ডেটার জন্য

### 3. রেগুলারাইজেশন
- L1 স্পারসিটি: কম ফিচার অ্যাক্টিভেট করতে
- ড্রপআউট: ওভারফিটিং কমাতে
- BatchNorm: ট্রেনিং স্টেবিলাইজ করতে

```python
print("✅ অটোএনকোডার বেসিক সম্পূর্ণ")
print(f"কভার করা হয়েছে: সিম্পল AE, ডিপ AE, স্পার্স AE")
print(f"ফিন্যান্স অ্যাপ্লিকেশন: ফিচার এক্সট্র্যাকশন, অ্যানোমালি ডিটেকশন")
```

## সারাংশ
- অটোএনকোডার আনসুপারভাইজড লার্নিং মডেল
- ইনপুটকে কম্প্রেস করে পুনর্নির্মাণ করতে শেখে
- ডাইমেনশনালিটি রিডাকশন ও ফিচার লার্নিংয়ে ব্যবহৃত
- স্পার্স ও ডিপ ভ্যারিয়েন্ট বিদ্যমান
- ফিন্যান্সে ফ্রড ডিটেকশন, অ্যানোমালি ডিটেকশন, ফিচার এক্সট্র্যাকশন