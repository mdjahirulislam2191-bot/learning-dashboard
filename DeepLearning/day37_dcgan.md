# Day 37: DCGAN (Deep Convolutional GAN) 🎨

## DCGAN কী?
DCGAN হল GAN-এর একটি ভ্যারিয়েন্ট যা কনভোলিউশনাল নেটওয়ার্ক ব্যবহার করে। এটি ইমেজ ডেটার জন্য বিশেষভাবে কার্যকর, কিন্তু ফিন্যান্সিয়াল টাইম সিরিজের জন্যও অ্যাডাপ্ট করা যায়।

### DCGAN-এর মূল ধারণা
1. **Conv1D/Conv2D**: কনভোলিউশনাল লেয়ার ব্যবহার
2. **Batch Normalization**: জেনারেটর ও ডিসক্রিমিনেটরে
3. **LeakyReLU**: ডিসক্রিমিনেটরে (ReLU-র পরিবর্তে)
4. **Transposed Convolution**: জেনারেটরে (আপস্যাম্পলিং)
5. **Strided Convolution**: ডিসক্রিমিনেটরে (ডাউনস্যাম্পলিং)

### কেন DCGAN?
- **স্টেবল ট্রেনিং**: GAN-এর চেয়ে বেশি স্টেবল
- **বেটার কোয়ালিটি**: উচ্চ-মানের ডেটা জেনারেশন
- **রিচ রিপ্রেজেন্টেশন**: স্থানিক প্যাটার্ন ক্যাপচার

## PyTorch DCGAN ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1D DCGAN (টাইম সিরিজের জন্য)

```python
class DCGANGenerator1D(nn.Module):
    """1D DCGAN জেনারেটর (টাইম সিরিজ)"""
    def __init__(self, noise_dim=100, seq_len=50, n_features=5):
        super().__init__()
        self.seq_len = seq_len
        self.n_features = n_features
        
        # প্রোজেক্ট & রিশেপ
        self.fc = nn.Linear(noise_dim, 256 * (seq_len // 8))
        
        # ট্রান্সপোজড কনভ১ডি লেয়ার
        self.deconv = nn.Sequential(
            nn.BatchNorm1d(256),
            nn.ReLU(),
            
            nn.ConvTranspose1d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            
            nn.ConvTranspose1d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            
            nn.ConvTranspose1d(64, n_features, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )
    
    def forward(self, z):
        batch = z.size(0)
        out = self.fc(z)
        out = out.view(batch, 256, self.seq_len // 8)
        out = self.deconv(out)
        # আউটপুট: (batch, n_features, seq_len)
        # Permute to (batch, seq_len, n_features) for consistency
        out = out.permute(0, 2, 1)
        return out

class DCGANDiscriminator1D(nn.Module):
    """1D DCGAN ডিসক্রিমিনেটর"""
    def __init__(self, seq_len=50, n_features=5):
        super().__init__()
        
        self.conv = nn.Sequential(
            nn.Conv1d(n_features, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.25),
            
            nn.Conv1d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.25),
            
            nn.Conv1d(128, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.25),
        )
        
        self.fc = nn.Sequential(
            nn.Linear(256 * (seq_len // 8), 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        # x: (batch, seq_len, n_features) → permute to (batch, n_features, seq_len)
        x = x.permute(0, 2, 1)
        features = self.conv(x)
        features = features.view(features.size(0), -1)
        return self.fc(features)

# টেস্ট
G = DCGANGenerator1D(noise_dim=100, seq_len=50, n_features=5).to(device)
D = DCGANDiscriminator1D(seq_len=50, n_features=5).to(device)

z = torch.randn(16, 100).to(device)
fake_seq = G(z)
validity = D(fake_seq)

print(f"DCGAN 1D Test:")
print(f"  নয়েজ: {z.shape}")
print(f"  জেনারেটেড সিকোয়েন্স: {fake_seq.shape}")  # (16, 50, 5)
print(f"  ডি আউটプুট: {validity.shape}")
```

## ফিন্যান্সিয়াল টাইম সিরিজ ডেটা

```python
# মাল্টি-ডাইমেনশনাল টাইম সিরিজ ডেটা
np.random.seed(42)
N = 5000
seq_len = 50
n_features = 5

# ট্রেন্ড + সিজনাল + নয়েজ
t = np.linspace(0, 100, seq_len)
base_data = np.zeros((N, seq_len, n_features))

for i in range(N):
    for f in range(n_features):
        trend = np.random.randn() * 0.01 * t
        seasonal = np.random.randn() * np.sin(2 * np.pi * t / np.random.randint(5, 15))
        noise = np.random.randn(seq_len) * 0.1
        base_data[i, :, f] = trend + seasonal + noise

# নরমালাইজ -1 to 1 (Tanh আউটপুটের জন্য)
data_min = base_data.min()
data_max = base_data.max()
real_data = 2 * (base_data - data_min) / (data_max - data_min) - 1

data_tensor = torch.FloatTensor(real_data).to(device)
dataset = DataLoader(TensorDataset(data_tensor, data_tensor), batch_size=64, shuffle=True)

print(f"টাইম সিরিজ ডেটা: {real_data.shape}")
print(f"ভ্যালু রেঞ্জ: [{real_data.min():.2f}, {real_data.max():.2f}]")
```

## DCGAN ট্রেনিং

```python
# মডেল
G = DCGANGenerator1D(noise_dim=100, seq_len=seq_len, n_features=n_features).to(device)
D = DCGANDiscriminator1D(seq_len=seq_len, n_features=n_features).to(device)

# অপ্টিমাইজার ও লস
criterion = nn.BCELoss()
g_optim = optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optim = optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

# ট্রেনিং
epochs = 100
g_losses, d_losses = [], []

print("DCGAN ট্রেনিং শুরু...")
for epoch in range(epochs):
    for batch_idx, (real_batch, _) in enumerate(dataset):
        batch_size = real_batch.size(0)
        
        # লেবেল (লেবেল স্মুথিং)
        real_labels = torch.ones(batch_size, 1).to(device) * 0.9
        fake_labels = torch.zeros(batch_size, 1).to(device) + 0.1
        
        # === ডিসক্রিমিনেটর ===
        D.zero_grad()
        
        real_output = D(real_batch)
        d_real_loss = criterion(real_output, real_labels)
        
        z = torch.randn(batch_size, 100).to(device)
        fake_batch = G(z)
        fake_output = D(fake_batch.detach())
        d_fake_loss = criterion(fake_output, fake_labels)
        
        d_loss = d_real_loss + d_fake_loss
        d_loss.backward()
        d_optim.step()
        
        # === জেনারেটর ===
        G.zero_grad()
        
        z = torch.randn(batch_size, 100).to(device)
        fake_batch = G(z)
        fake_output = D(fake_batch)
        g_loss = criterion(fake_output, real_labels)
        
        g_loss.backward()
        g_optim.step()
    
    g_losses.append(g_loss.item())
    d_losses.append(d_loss.item())
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}] | D: {d_loss.item():.4f} | G: {g_loss.item():.4f}")

print("✅ DCGAN ট্রেনিং সম্পূর্ণ!")
```

## জেনারেটেড ডেটা ইভালুয়েশন

```python
G.eval()

with torch.no_grad():
    z = torch.randn(500, 100).to(device)
    generated_seqs = G(z).cpu().numpy()

real_np = real_data[:500]

print(f"{'মেট্রিক':<20} {'রিয়েল':<15} {'জেনারেটেড':<15}")
print("-" * 50)
print(f"{'মিন':<20} {real_np.mean():<15.4f} {generated_seqs.mean():<15.4f}")
print(f"{'স্টাড':<20} {real_np.std():<15.4f} {generated_seqs.std():<15.4f}")
print(f"{'স্কিউ':<20} {np.mean(real_np**3):<15.4f} {np.mean(generated_seqs**3):<15.4f}")
print(f"{'কার্টোসিস':<20} {np.mean(real_np**4):<15.4f} {np.mean(generated_seqs**4):<15.4f}")

# অটোকোরিলেশন তুলনা
def autocorr(x, lag=5):
    """অটোকোরিলেশন গণনা"""
    n = len(x)
    mean = np.mean(x)
    var = np.var(x)
    ac = np.zeros(lag)
    for l in range(1, lag+1):
        ac[l-1] = np.mean((x[l:] - mean) * (x[:-l] - mean)) / var
    return ac

# প্রথম ফিচারের অটোকোরিলেশন
real_ac = np.mean([autocorr(real_np[i, :, 0]) for i in range(100)], axis=0)
gen_ac = np.mean([autocorr(generated_seqs[i, :, 0]) for i in range(100)], axis=0)

print(f"\nঅটোকোরিলেশন তুলনা (প্রথম ফিচার):")
print(f"{'ল্যাগ':<10} {'রিয়েল':<15} {'জেনারেটেড':<15}")
for l in range(5):
    print(f"{l+1:<10} {real_ac[l]:<15.4f} {gen_ac[l]:<15.4f}")
```

## টেম্পোরাল ডায়নামিক্স চেক

```python
def temporal_cross_correlation(real, generated):
    """টেম্পোরাল ক্রস-কোরিলেশন"""
    real_diff = np.diff(real, axis=1)
    gen_diff = np.diff(generated, axis=1)
    
    real_corr = np.corrcoef(real_diff[:, :, 0].T)
    gen_corr = np.corrcoef(gen_diff[:, :, 0].T)
    
    return np.abs(real_corr - gen_corr).mean()

temporal_diff = temporal_cross_correlation(real_np, generated_seqs)
print(f"টেম্পোরাল ডায়নামিক্স ডিফারেন্স: {temporal_diff:.4f}")

# ক্রস-ফিচার কোরিলেশন
for f1 in range(n_features):
    for f2 in range(f1+1, n_features):
        real_cc = np.corrcoef(real_np[:, :, f1].flatten(), real_np[:, :, f2].flatten())[0, 1]
        gen_cc = np.corrcoef(generated_seqs[:, :, f1].flatten(), 
                             generated_seqs[:, :, f2].flatten())[0, 1]
        print(f"  ফিচার {f1+1}-{f2+1} কোরিলেশন: রিয়েল={real_cc:.4f}, "
              f"জেন={gen_cc:.4f}, ডিফ={abs(real_cc-gen_cc):.4f}")
```

## 2D DCGAN (ফিন্যান্সিয়াল ইমেজের জন্য)

```python
class DCGANGenerator2D(nn.Module):
    """2D DCGAN জেনারেটর"""
    def __init__(self, noise_dim=100, channels=1, feature_dim=64):
        super().__init__()
        
        self.fc = nn.Linear(noise_dim, feature_dim * 8 * 4 * 4)
        
        self.deconv = nn.Sequential(
            nn.BatchNorm2d(feature_dim * 8),
            nn.ReLU(),
            
            nn.ConvTranspose2d(feature_dim * 8, feature_dim * 4, 
                              kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim * 4),
            nn.ReLU(),
            
            nn.ConvTranspose2d(feature_dim * 4, feature_dim * 2,
                              kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim * 2),
            nn.ReLU(),
            
            nn.ConvTranspose2d(feature_dim * 2, feature_dim,
                              kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim),
            nn.ReLU(),
            
            nn.ConvTranspose2d(feature_dim, channels,
                              kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )
    
    def forward(self, z):
        batch = z.size(0)
        out = self.fc(z)
        out = out.view(batch, -1, 4, 4)
        return self.deconv(out)

class DCGANDiscriminator2D(nn.Module):
    """2D DCGAN ডিসক্রিমিনেটর"""
    def __init__(self, channels=1, feature_dim=64):
        super().__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(channels, feature_dim, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Dropout2d(0.25),
            
            nn.Conv2d(feature_dim, feature_dim * 2, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim * 2),
            nn.LeakyReLU(0.2),
            nn.Dropout2d(0.25),
            
            nn.Conv2d(feature_dim * 2, feature_dim * 4, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim * 4),
            nn.LeakyReLU(0.2),
            nn.Dropout2d(0.25),
            
            nn.Conv2d(feature_dim * 4, feature_dim * 8, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(feature_dim * 8),
            nn.LeakyReLU(0.2),
            nn.Dropout2d(0.25),
            
            nn.Conv2d(feature_dim * 8, 1, kernel_size=4, stride=1, padding=0),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.conv(x).view(-1, 1)

# টেস্ট
G2 = DCGANGenerator2D(noise_dim=100, channels=1).to(device)
D2 = DCGANDiscriminator2D(channels=1).to(device)

z = torch.randn(8, 100).to(device)
img = G2(z)
print(f"\nDCGAN 2D: {z.shape} → {img.shape}")
print(f"ফিন্যান্সিয়াল ইমেজ (64×64) জেনারেট করতে পারে")
```

## DCGAN বেস্ট প্র্যাকটিস

```python
# DCGAN ট্রেনিং টিপস
tips = """
DCGAN স্পেসিফিক টিপস:
1. Strided Convolution ব্যবহার করুন (Pooling নয়)
2. Generator-এ BatchNorm + ReLU
3. Discriminator-এ BatchNorm + LeakyReLU
4. ফুলি কানেক্টেড লেয়ার এড়িয়ে চলুন
5. লার্নিং রেট: 0.0002 (Adam)
6. Beta1: 0.5 (স্ট্যান্ডার্ড 0.9 না)
7. লেবেল স্মুথিং ব্যবহার করুন
8. নয়েজ ডাইমেনশন: 100-128
9. ফিচার ম্যাপ: 64 থেকে শুরু
10. ওয়েট ইনিশিয়ালাইজেশন: N(0, 0.02)
"""

print(tips)

# ওয়েট ইনিশিয়ালাইজেশন ফাংশন
def weights_init(m):
    """DCGAN ওয়েট ইনিশিয়ালাইজেশন"""
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

print("✅ weights_init() ফাংশন ডিফাইন্ড (DCGAN স্ট্যান্ডার্ড)")
```

## সারাংশ
- DCGAN কনভোলিউশনাল লেয়ার ব্যবহার করে GAN-কে উন্নত করে
- 1D DCGAN টাইম সিরিজ/সিকোয়েন্স ডেটার জন্য
- 2D DCGAN ইমেজ ডেটার জন্য (ফিন্যান্সিয়াল চার্ট সহ)
- Strided convolutions, BatchNorm, LeakyReLU মূল কম্পোনেন্ট
- ট্রান্সপোজড কনভোলিউশন জেনারেটরে ব্যবহার
- ফিন্যান্সে সিন্থেটিক টাইম সিরিজ, চার্ট জেনারেশন, ডেটা অগমেন্টেশন