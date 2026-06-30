# Day 36: GAN (Generative Adversarial Network) 🎭

## GAN কী?
GAN দুটি নিউরাল নেটওয়ার্কের মধ্যে প্রতিযোগিতার মাধ্যমে শেখে - একটি জেনারেটর (Generator) এবং একটি ডিসক্রিমিনেটর (Discriminator)।

### মৌলিক ধারণা
```
জেনারেটর: নয়েজ → ফেক ডেটা তৈরি করে
    ↕ (প্রতিযোগিতা)
ডিসক্রিমিনেটর: রিয়েল vs ফেক ক্লাসিফাই করে
```

### GAN অ্যানালজি
- **জেনারেটর**: জাল টাকা তৈরি করার চেষ্টা করে
- **ডিসক্রিমিনেটর**: জাল টাকা শনাক্ত করার চেষ্টা করে
- **ফলাফল**: জেনারেটর এত ভালো হয় যে ডিসক্রিমিনেটর আর পার্থক্য করতে পারে না

### ফিন্যান্সে ব্যবহার
1. **সিন্থেটিক মার্কেট ডেটা জেনারেশন**
2. **ডেটা অগমেন্টেশন** (বিরল ইভেন্ট)
3. **রিস্ক সিনারিও জেনারেশন**
4. **পোর্টফোলিও অপ্টিমাইজেশন**
5. **ফ্রড ডিটেকশন ডেটা ব্যালেন্সিং**

## সিম্পল GAN ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset

# ডিভাইস
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## জেনারেটর ও ডিসক্রিমিনেটর

```python
class Generator(nn.Module):
    """জেনারেটর: নয়েজ → ফিন্যান্সিয়াল ডেটা"""
    def __init__(self, noise_dim=100, output_dim=50):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(noise_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, output_dim)
        )
    
    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    """ডিসক্রিমিনেটর: রিয়েল vs ফেক ক্লাসিফাই"""
    def __init__(self, input_dim=50):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
            nn.Sigmoid()  # 0=ফেক, 1=রিয়েল
        )
    
    def forward(self, x):
        return self.model(x)

# টেস্ট
noise_dim = 100
data_dim = 50

G = Generator(noise_dim, data_dim).to(device)
D = Discriminator(data_dim).to(device)

z = torch.randn(16, noise_dim).to(device)
fake_data = G(z)
real_fake = D(fake_data)

print(f"জেনারেটর: নয়েজ {z.shape} → ডেটা {fake_data.shape}")
print(f"ডিসক্রিমিনেটর: {fake_data.shape} → {real_fake.shape}")
print(f"ডি আউটপুট (০=ফেক, ১=রিয়েল): {real_fake[:3].squeeze().detach().cpu().numpy()}")
```

## ফিন্যান্সিয়াল ডেটা তৈরী

```python
# টার্গেট ডেটা ডিস্ট্রিবিউশন
np.random.seed(42)
N = 10000

# ফিন্যান্সিয়াল রিটার্নের মতো ডেটা
# (লেপটোকিউরটিক: ফ্যাট টেল, স্কিউড)
returns = np.random.standard_t(df=4, size=(N, data_dim)) * 0.5
returns = np.clip(returns, -5, 5)

# নরমালাইজ
returns = (returns - returns.mean(axis=0)) / returns.std(axis=0)

real_data = torch.FloatTensor(returns).to(device)
dataset = DataLoader(TensorDataset(real_data, real_data), batch_size=128, shuffle=True)

print(f"রিয়েল ডেটা: {real_data.shape}")
print(f"রিয়েল ডেটা স্ট্যাটিস্টিক্স:")
print(f"  মিন: {returns.mean():.4f}")
print(f"  স্টাড: {returns.std():.4f}")
print(f"  স্কিউ: {np.mean(np.sign(returns**3) * abs(returns**3)):.4f}")
print(f"  কার্টোসিস: {np.mean(returns**4):.4f}")
```

## GAN ট্রেনিং লুপ

```python
# লস ও অপ্টিমাইজার
criterion = nn.BCELoss()
g_optimizer = optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optimizer = optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

# ট্রেনিং
epochs = 5000
g_losses, d_losses = [], []

print("GAN ট্রেনিং শুরু...")
for epoch in range(epochs):
    for batch_idx, (real_batch, _) in enumerate(dataset):
        batch_size = real_batch.size(0)
        
        # লেবেল
        real_labels = torch.ones(batch_size, 1).to(device)
        fake_labels = torch.zeros(batch_size, 1).to(device)
        
        # === ডিসক্রিমিনেটর ট্রেনিং ===
        D.zero_grad()
        
        # রিয়েল ডেটা
        real_output = D(real_batch)
        d_real_loss = criterion(real_output, real_labels)
        
        # ফেক ডেটা
        z = torch.randn(batch_size, noise_dim).to(device)
        fake_data = G(z)
        fake_output = D(fake_data.detach())
        d_fake_loss = criterion(fake_output, fake_labels)
        
        d_loss = d_real_loss + d_fake_loss
        d_loss.backward()
        d_optimizer.step()
        
        # === জেনারেটর ট্রেনিং ===
        G.zero_grad()
        
        z = torch.randn(batch_size, noise_dim).to(device)
        fake_data = G(z)
        fake_output = D(fake_data)
        g_loss = criterion(fake_output, real_labels)  # ডিকে বোকা বানাতে চায়
        
        g_loss.backward()
        g_optimizer.step()
    
    # ট্র্যাকিং
    g_losses.append(g_loss.item())
    d_losses.append(d_loss.item())
    
    if (epoch + 1) % 500 == 0:
        print(f"Epoch [{epoch+1}/{epochs}] | "
              f"D Loss: {d_loss.item():.4f} | "
              f"G Loss: {g_loss.item():.4f}")

print("✅ GAN ট্রেনিং সম্পূর্ণ!")
```

## জেনারেটেড ডেটা ইভালুয়েশন

```python
G.eval()

# নতুন ডেটা জেনারেট
with torch.no_grad():
    z = torch.randn(1000, noise_dim).to(device)
    generated = G(z).cpu().numpy()

# রিয়েল ডেটা
real_np = real_data.cpu().numpy()

# তুলনা
print(f"{'স্ট্যাট':<20} {'রিয়েল ডেটা':<20} {'জেনারেটেড':<20}")
print("-" * 60)
print(f"{'মিন':<20} {real_np.mean():<20.4f} {generated.mean():<20.4f}")
print(f"{'স্টাড':<20} {real_np.std():<20.4f} {generated.std():<20.4f}")
print(f"{'স্কিউ':<20} {np.mean(np.sign(real_np**3)*abs(real_np**3)):<20.4f} "
      f"{np.mean(np.sign(generated**3)*abs(generated**3)):<20.4f}")
print(f"{'কার্টোসিস':<20} {np.mean(real_np**4):<20.4f} "
      f"{np.mean(generated**4):<20.4f}")

# ডিস্ট্রিবিউশন ম্যাচিং
from scipy.stats import ks_2samp

for i in range(min(5, data_dim)):
    stat, pval = ks_2samp(real_np[:, i], generated[:, i])
    print(f"ফিচার {i+1}: KS-stat={stat:.4f}, p-value={pval:.4f}", 
          end="")
    if pval > 0.05:
        print(" ✅ (একই ডিস্ট্রিবিউশন)")
    else:
        print(" ❌ (ভিন্ন ডিস্ট্রিবিউশন)")
```

## কোরিলেশন স্ট্রাকচার চেক

```python
# কোরিলেশন ম্যাট্রিক্স
corr_real = np.corrcoef(real_np[:, :10].T)
corr_gen = np.corrcoef(generated[:, :10].T)

corr_diff = np.abs(corr_real - corr_gen).mean()
print(f"কোরিলেশন ম্যাট্রিক্স ডিফারেন্স: {corr_diff:.4f}")
print("(ছোট মানে ফিচার কোরিলেশন ভালোভাবে ক্যাপচার করা হয়েছে)")

print(f"\nরিয়েল ডেটা কোরিলেশন (প্রথম ৫×৫):")
print(corr_real[:5, :5].round(3))
print(f"\nজেনারেটেড ডেটা কোরিলেশন (প্রথম ৫×৫):")
print(corr_gen[:5, :5].round(3))
```

## GAN লস ভিজুয়ালাইজেশন

```python
# লস প্লট
plt.figure(figsize=(10, 5))
plt.plot(g_losses, label='Generator Loss', alpha=0.7)
plt.plot(d_losses, label='Discriminator Loss', alpha=0.7)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('GAN Training Convergence')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("✅ GAN কনভারজেন্স মনিটরিং কমপ্লিট")
```

## মোড কোল্যাপস ডিটেকশন

```python
def detect_mode_collapse(generated_data, threshold=0.1):
    """মোড কোল্যাপস ডিটেক্ট করুন"""
    variance = np.var(generated_data, axis=0)
    low_variance_features = (variance < threshold * variance.mean()).sum()
    collapse_ratio = low_variance_features / generated_data.shape[1]
    
    if collapse_ratio > 0.3:
        print(f"🚨 মোড কোল্যাপস ডিটেক্টেড! {low_variance_features}/{generated_data.shape[1]} ফিচার কম ভ্যারিয়েন্স")
    else:
        print(f"✅ মোড কোল্যাপস নেই: {low_variance_features}/{generated_data.shape[1]} ফিচার কম ভ্যারিয়েন্স")
    
    return collapse_ratio

# চেক
collapse_ratio = detect_mode_collapse(generated)
print(f"মোড কোল্যাপস রেশিও: {collapse_ratio:.4f}")
```

## GAN হাইপারপ্যারামিটার গাইড

```python
# GAN ট্রেনিং টিপস
tips = {
    "লার্নিং রেট": "0.0002 (Adam-এর জন্য আদর্শ)",
    "Beta1 (Adam)": "0.5 (স্ট্যান্ডার্ড 0.9 না)",
    "Batch Size": "32-128 (ছোট ব্যাচ বেশি স্টেবল)",
    "Noise Dim": "100-256 (পর্যাপ্ত জটিলতা)",
    "LeakyReLU": "Discriminator-এ ভালো (0.2 slope)",
    "Dropout": "Discriminator-এ 0.2-0.5 (অ্যান্টি-মেমোরাইজেশন)",
    "BatchNorm": "Generator-এ অপরিহার্য",
    "Label Smoothing": "রিয়েল লেবেল 0.9, ফেক 0.1 (স্মুদার গ্র্যাডিয়েন্ট)",
    "Gradient Penalty": "WGAN-GP-তে প্রয়োজন"
}

print("GAN হাইপারপ্যারামিটার গাইড:")
for param, tip in tips.items():
    print(f"  {param}: {tip}")

# লেবেল স্মুথিং ডেমো
real_labels_smooth = torch.ones(10, 1) * 0.9
fake_labels_smooth = torch.ones(10, 1) * 0.1
print(f"\nলেবেল স্মুথিং: রিয়েল={real_labels_smooth[0].item()}, "
      f"ফেক={fake_labels_smooth[0].item()}")
```

## সারাংশ
- GAN জেনারেটর ও ডিসক্রিমিনেটরের প্রতিযোগিতার মাধ্যমে শেখে
- জেনারেটর নয়েজ থেকে রিয়েলিস্টিক ডেটা তৈরি করে
- ডিসক্রিমিনেটর রিয়েল-ফেক পার্থক্য করতে শেখে
- জিরো-সাম গেম ➝ ন্যাশ ইকুইলিব্রিয়াম
- ফিন্যান্সে সিন্থেটিক ডেটা, রিস্ক সিনারিও, অগমেন্টেশনে ব্যবহৃত
- মোড কোল্যাপস একটি সাধারণ সমস্যা
- হাইপারপ্যারামিটার টিউনিং গুরুত্বপূর্ণ