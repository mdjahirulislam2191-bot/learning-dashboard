# Day 32: ডিনয়েজিং অটোএনকোডার 🧹

## ডিনয়েজিং অটোএনকোডার কী?
ডিনয়েজিং অটোএনকোডার (Denoising Autoencoder - DAE) একটি অটোএনকোডার যা intentionally নয়েজি ইনপুট থেকে ক্লিন আউটপুট জেনারেট করতে শেখে।

### কেন ডিনয়েজিং?
- রিয়েল ডেটাতে নয়েজ থাকে
- ডিনয়েজিং শিখলে মডেল আরও রোবাস্ট হয়
- ল্যাটেন্ট রিপ্রেজেন্টেশন আরও মিনিংফুল হয়
- ওভারফিটিং কমে

### DAE vs সাধারণ AE
| বৈশিষ্ট্য | সাধারণ AE | ডিনয়েজিং AE |
|---|---|---|
| ইনপুট | ক্লিন ডেটা | নয়েজি ডেটা |
| টার্গেট | ক্লিন ডেটা | ক্লিন ডেটা |
| লার্নিং | আইডেনটিটি ফাংশন | ডিনয়েজিং ফাংশন |
| রোবাস্টনেস | কম | বেশি |
| ফিচার লার্নিং | বেসিক | অ্যাডভান্সড |

### ফিন্যান্সে ব্যবহার
- নয়েজি মার্কেট ডেটা ক্লিনিং
- ফ্রড ডিটেকশন (ক্রেডিট কার্ড)
- স্টক প্রাইস ডিনয়েজিং
- মিসিং ভ্যালু ইম্পিউটেশন

## DAE আর্কিটেকচার

```
ইনপুট (নয়েজি):    x̃ = x + noise
                        ↓
                   [এনকোডার]
                        ↓
                 ল্যাটেন্ট (z)
                        ↓
                   [ডিকোডার]
                        ↓
আউটপুট (ক্লিন):    x̂ ≈ x

লস: ||x - x̂||²  (ইনপুটের সাথে না, অরিজিনাল ক্লিনের সাথে)
```

## PyTorch DAE ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

class DenoisingAutoencoder(nn.Module):
    """ডিনয়েজিং অটোএনকোডার"""
    def __init__(self, input_dim, encoding_dim=16, dropout_rate=0.3):
        super().__init__()
        
        # এনকোডার
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, encoding_dim),
            nn.ReLU()
        )
        
        # ডিকোডার
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, input_dim),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def add_noise(self, x, noise_factor=0.2):
        """ইনপুটে গাউসিয়ান নয়েজ যোগ"""
        noise = torch.randn_like(x) * noise_factor
        noisy_x = x + noise
        noisy_x = torch.clamp(noisy_x, 0., 1.)  # 0-1 রেঞ্জে ক্লিপ
        return noisy_x
    
    def encode(self, x):
        return self.encoder(x)

# টেস্ট
dae = DenoisingAutoencoder(input_dim=50, encoding_dim=10)
x = torch.randn(16, 50)
x_noisy = dae.add_noise(x, noise_factor=0.3)
reconstructed = dae(x_noisy)
print(f"ক্লিন: {x.shape}, নয়েজি: {x_noisy.shape}, রিকন্সট্রাক্টেড: {reconstructed.shape}")
```

## ফিন্যান্স: স্টক ডেটা ডিনয়েজিং

```python
import pandas as pd

# সিন্থেটিক স্টক ডেটা
np.random.seed(42)
n = 2000
n_features = 20

# ক্লিন ডেটা (ফ্যাক্টর মডেল)
true_factors = np.random.randn(n, 3)
factor_weights = np.random.randn(3, n_features)
clean_data = true_factors @ factor_weights

# নরমালাইজ
clean_data = (clean_data - clean_data.min(axis=0)) / \
             (clean_data.max(axis=0) - clean_data.min(axis=0))

# নয়েজি ডেটা (মার্কেট মাইক্রোস্ট্রাকচার নয়েজ)
noise_factor = 0.15
noisy_data = clean_data + np.random.randn(n, n_features) * noise_factor
noisy_data = np.clip(noisy_data, 0, 1)

print(f"ক্লিন ডেটা: {clean_data.shape}")
print(f"নয়েজি ডেটা: {noisy_data.shape}")
print(f"SNR (Signal-to-Noise): {20*np.log10(np.std(clean_data)/noise_factor):.2f} dB")

# ফিচার করিলেশন দেখুন
print(f"\nক্লিন ফিচার করিলেশন (প্রথম ৫):")
print(np.corrcoef(clean_data[:100, :5].T).round(2))
print(f"\nনয়েজি ফিচার করিলেশন (প্রথম ৫):")
print(np.corrcoef(noisy_data[:100, :5].T).round(2))
```

## DAE ট্রেনিং

```python
# ডেটা প্রিপারেশন
clean_tensor = torch.FloatTensor(clean_data)
noisy_tensor = torch.FloatTensor(noisy_data)

dataset = TensorDataset(noisy_tensor, clean_tensor)  # নয়েজি → ক্লিন
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# মডেল
dae = DenoisingAutoencoder(input_dim=n_features, encoding_dim=8, dropout_rate=0.2)
criterion = nn.MSELoss()
optimizer = optim.Adam(dae.parameters(), lr=0.001)

# ট্রেনিং
epochs = 80
noise_level = 0.2  # ট্রেনিং-এ নয়েজ লেভেল

for epoch in range(epochs):
    total_loss = 0
    
    for batch_noisy, batch_clean in loader:
        # আরও নয়েজ যোগ (DAE ট্রেনিং)
        batch_noisy = dae.add_noise(batch_clean, noise_level)
        
        optimizer.zero_grad()
        reconstructed = dae(batch_noisy)
        loss = criterion(reconstructed, batch_clean)  # ক্লিন টার্গেট
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")

print("✅ DAE ট্রেনিং সম্পূর্ণ!")
```

## ইভালুয়েশন

```python
dae.eval()

# টেস্ট নয়েজি ডেটা
test_noisy = torch.FloatTensor(noisy_data[:200])
test_clean = torch.FloatTensor(clean_data[:200])

with torch.no_grad():
    test_noisy_aug = dae.add_noise(test_clean, noise_factor=0.2)
    denoised = dae(test_noisy_aug)

# পারফরম্যান্স মেট্রিক্স
mse_noisy = nn.MSELoss()(test_noisy_aug, test_clean).item()
mse_denoised = nn.MSELoss()(denoised, test_clean).item()
improvement = (mse_noisy - mse_denoised) / mse_noisy * 100

print(f"{'মেট্রিক':<30} {'মান':<15}")
print("-" * 45)
print(f"{'নয়েজি MSE (ইনপুট)':<30} {mse_noisy:<15.6f}")
print(f"{'ডিনয়েজড MSE (আউটপুট)':<30} {mse_denoised:<15.6f}")
print(f"{'ইমপ্রুভমেন্ট':<30} {improvement:<15.2f}%")

# ভিজুয়ালাইজ
sample_idx = 0
print(f"\nপ্রথম স্যাম্পলের ফিচার রিকন্সট্রাকশন:")
print(f"{'ফিচার':<10} {'ক্লিন':<15} {'নয়েজি':<15} {'ডিনয়েজড':<15}")
print("-" * 55)
for f in range(min(10, n_features)):
    print(f"{f:<10} {test_clean[sample_idx, f]:<15.4f} "
          f"{test_noisy_aug[sample_idx, f]:<15.4f} "
          f"{denoised[sample_idx, f]:<15.4f}")
```

## ডিনয়েজিং কোয়ালিটি অ্যাসেসমেন্ট

```python
def assess_denoising_quality(clean, noisy, denoised):
    """ডিনয়েজিং কোয়ালিটি মেট্রিক্স"""
    clean = clean.numpy()
    noisy = noisy.numpy()
    denoised = denoised.numpy()
    
    # MSE ইমপ্রুভমেন্ট
    mse_noisy = np.mean((noisy - clean) ** 2)
    mse_denoised = np.mean((denoised - clean) ** 2)
    
    # SNR ইমপ্রুভমেন্ট
    signal_power = np.var(clean)
    noise_power_noisy = np.var(noisy - clean)
    noise_power_denoised = np.var(denoised - clean)
    
    snr_noisy = 10 * np.log10(signal_power / (noise_power_noisy + 1e-8))
    snr_denoised = 10 * np.log10(signal_power / (noise_power_denoised + 1e-8))
    
    # 피어슨 কোরিলেশন
    from scipy.stats import pearsonr
    corr_noisy = np.mean([pearsonr(noisy[:, i], clean[:, i])[0] for i in range(clean.shape[1])])
    corr_denoised = np.mean([pearsonr(denoised[:, i], clean[:, i])[0] for i in range(clean.shape[1])])
    
    print(f"{'মেট্রিক':<25} {'নয়েজি':<15} {'ডিনয়েজড':<15}")
    print("-" * 55)
    print(f"{'MSE':<25} {mse_noisy:<15.6f} {mse_denoised:<15.6f}")
    print(f"{'SNR (dB)':<25} {snr_noisy:<15.2f} {snr_denoised:<15.2f}")
    print(f"{'কোরিলেশন':<25} {corr_noisy:<15.4f} {corr_denoised:<15.4f}")
    print(f"{'MSE ইমপ্রুভমেন্ট':<25} {'-':<15} {((mse_noisy-mse_denoised)/mse_noisy*100):<15.2f}%")
    print(f"{'SNR ইমপ্রুভমেন্ট':<25} {'-':<15} {(snr_denoised-snr_noisy):<15.2f} dB")

assess_denoising_quality(test_clean, test_noisy_aug, denoised)
```

## ডিফারেন্ট নয়েজ লেভেলে টেস্ট

```python
# বিভিন্ন নয়েজ লেভেলে DAE টেস্ট
noise_levels = [0.05, 0.1, 0.2, 0.3, 0.5]
results = []

for noise_lvl in noise_levels:
    with torch.no_grad():
        test_noisy = dae.add_noise(test_clean, noise_lvl)
        denoised = dae(test_noisy)
        mse = nn.MSELoss()(denoised, test_clean).item()
        results.append(mse)
        print(f"নয়েজ {noise_lvl:.0%}: ডিনয়েজড MSE = {mse:.6f}")

print(f"\nনয়েজ লেভেল বনাম পারফরম্যান্স:")
for i, lvl in enumerate(noise_levels):
    bar = '█' * int(results[i] * 5000)
    print(f"  {lvl:.0%}: {bar} {results[i]:.6f}")
```

## নয়েজ টাইপের ভ্যারিয়েশন

```python
class NoiseAugmentation:
    """বিভিন্ন ধরণের নয়েজ অগমেন্টেশন"""
    
    @staticmethod
    def gaussian_noise(x, std=0.1):
        """গাউসিয়ান নয়েজ"""
        return x + torch.randn_like(x) * std
    
    @staticmethod
    def salt_pepper_noise(x, prob=0.05):
        """সল্ট-পেপার নয়েজ"""
        mask = torch.rand_like(x) < prob
        noisy = x.clone()
        noisy[mask] = 1 - noisy[mask]  # ফ্লিপ
        return noisy
    
    @staticmethod
    def masking_noise(x, mask_prob=0.1):
        """মাস্কিং নয়েজ (ফিচার ড্রপআউট)"""
        mask = torch.rand_like(x) > mask_prob
        return x * mask.float()
    
    @staticmethod
    def swap_noise(x, swap_prob=0.05):
        """ফিচার সুইপ নয়েজ"""
        noisy = x.clone()
        n = x.size(-1)
        for i in range(len(x)):
            if torch.rand(1) < swap_prob:
                idx = torch.randperm(n)
                noisy[i] = noisy[i, idx]
        return noisy

aug = NoiseAugmentation()

# বিভিন্ন নয়েজ টাইপ দেখুন
sample = torch.FloatTensor(clean_data[:1])
print(f"অরিজিনাল: {sample[0, :5].numpy()}")

noise_types = {
    'গাউসিয়ান': aug.gaussian_noise(sample, 0.2),
    'সল্ট-পেপার': aug.salt_pepper_noise(sample, 0.1),
    'মাস্কিং': aug.masking_noise(sample, 0.2),
}

for name, noisy in noise_types.items():
    similarity = nn.functional.cosine_similarity(sample, noisy).item()
    print(f"{name}: {noisy[0, :5].numpy()} (cosine sim: {similarity:.4f})")
```

## DAE vs সাধারণ AE তুলনা

```python
# তুলনামূলক বিশ্লেষণ
class SimpleAE(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64), nn.ReLU(),
            nn.Linear(64, encoding_dim), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 64), nn.ReLU(),
            nn.Linear(64, input_dim), nn.Sigmoid()
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

# AE ট্রেনিং (ক্লিন ডেটা)
simple_ae = SimpleAE(n_features, 8)
opt_ae = optim.Adam(simple_ae.parameters(), lr=0.001)
criterion = nn.MSELoss()

for epoch in range(50):
    for bx, _ in DataLoader(TensorDataset(clean_tensor, clean_tensor), 64, shuffle=True):
        opt_ae.zero_grad()
        loss = criterion(simple_ae(bx), bx)
        loss.backward()
        opt_ae.step()

# তুলনা
simple_ae.eval()
dae.eval()

with torch.no_grad():
    # সাধারণ AE: নয়েজি ইনপুট → খারাপ আউটপুট
    ae_out = simple_ae(test_noisy_aug)
    ae_mse = criterion(ae_out, test_clean).item()
    
    # DAE: নয়েজি ইনপুট → ভালো আউটপুট
    dae_out = dae(test_noisy_aug)
    dae_mse = criterion(dae_out, test_clean).item()

print(f"{'মডেল':<20} {'নয়েজি ইনপুটে MSE':<20}")
print("-" * 40)
print(f"{'সাধারণ AE':<20} {ae_mse:<20.6f}")
print(f"{'ডিনয়েজিং AE':<20} {dae_mse:<20.6f}")
print(f"{'ইমপ্রুভমেন্ট':<20} {((ae_mse-dae_mse)/ae_mse*100):<19.2f}%")
```

## ফিন্যান্স প্র্যাকটিক্যাল অ্যাপ্লিকেশন

```python
# মিসিং ডেটা ইম্পিউটেশন
def impute_missing_data(model, data_with_missing, missing_mask):
    """অটোএনকোডার দিয়ে মিসিং ডেটা ইম্পিউট"""
    model.eval()
    with torch.no_grad():
        reconstructed = model(data_with_missing)
        # শুধু মিসিং ভ্যালু ইম্পিউট করুন
        imputed = data_with_missing.clone()
        imputed[missing_mask] = reconstructed[missing_mask]
    return imputed

# সিমুলেটেড মিসিং ডেটা
missing_mask = torch.rand_like(clean_tensor[:100]) < 0.1  # 10% মিসিং
data_with_missing = clean_tensor[:100].clone()
data_with_missing[missing_mask] = 0

# ইম্পিউট
imputed = impute_missing_data(dae, data_with_missing, missing_mask)
impute_mse = nn.MSELoss()(imputed[missing_mask], clean_tensor[:100][missing_mask])

print(f"মিসিং ডেটা ইম্পিউটেশন MSE: {impute_mse:.6f}")
print(f"মোট মিসিং ভ্যালু: {missing_mask.sum().item()}")
print("✅ মিসিং ভ্যালু ইম্পিউটেশন সফল!")
```

## সারাংশ
- ডিনয়েজিং অটোএনকোডার intentionally নয়েজি ইনপুট ব্যবহার করে
- ক্লিন আউটপুট পুনরুদ্ধার করতে শেখে
- আরও রোবাস্ট ও মিনিংফুল ল্যাটেন্ট রিপ্রেজেন্টেশন তৈরি করে
- বিভিন্ন নয়েজ টাইপের বিরুদ্ধে কাজ করে
- ফিন্যান্সে ডেটা ক্লিনিং, মিসিং ভ্যালু ইম্পিউটেশন, ফ্রড ডিটেকশনে ব্যবহৃত
- সাধারণ AE-র চেয়ে নয়েজি ডেটাতে অনেক ভালো পারফর্ম করে