# Day 39: GAN দিয়ে সিন্থেটিক ডেটা জেনারেশন 🤖

## সিন্থেটিক ডেটা কেন?
রিয়েল ওয়ার্ল্ড ডেটা অনেক সময় দুর্লভ, দামি, বা প্রাইভেসি-সংবেদনশীল। GAN বাস্তবসম্মত সিন্থেটিক ডেটা জেনারেট করতে পারে।

### ফিন্যান্সে সিন্থেটিক ডেটার প্রয়োজন
1. **ডেটা প্রাইভেসি**: ক্লায়েন্ট ডেটা শেয়ার করা যায় না
2. **বিরল ইভেন্ট**: মার্কেট ক্র্যাশের মতো বিরল ঘটনার ডেটা কম
3. **ব্যক্তেস্টিং**: পর্যাপ্ত ঐতিহাসিক ডেটা নেই
4. **ডেটা অগমেন্টেশন**: মডেলের জন্য আরও ডেটা প্রয়োজন
5. **রেগুলেটরি কমপ্লায়েন্স**: সিন্থেটিক ডেটা ব্যবহার করে টেস্টিং

### GAN-জেনারেটেড ডেটার গুণাগুণ
| গুণ | বর্ণনা | চেক করার উপায় |
|---|---|---|
| **ফিডেলিটি** | বাস্তবের কাছাকাছি | স্ট্যাটিস্টিক্যাল ম্যাচিং |
| **ডাইভারসিটি** | বিভিন্ন ধরণের ডেটা | মোড কোল্যাপস চেক |
| **প্রাইভেসি** | আসল ডেটা লিক না | Nearest Neighbor Distance |
| **ইউটিলিটি** | ডাউনস্ট্রিম টাস্কে কার্যকর | ট্রেন-টেস্ট পারফরম্যান্স |

## সম্পূর্ণ সিন্থেটিক ডেটা পাইপলাইন

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score, mean_squared_error
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. GAN মডেল ডেফিনিশন

```python
class SyntheticDataGenerator(nn.Module):
    """সিন্থেটিক ডেটা জেনারেটর"""
    def __init__(self, noise_dim=128, output_dim=50):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(noise_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, output_dim)
        )
    
    def forward(self, z):
        return self.model(z)

class SyntheticDataDiscriminator(nn.Module):
    """সিন্থেটিক ডেটা ডিসক্রিমিনেটর"""
    def __init__(self, input_dim=50):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.model(x)

noise_dim = 128
data_dim = 50
```

## 2. রিয়েল ফিন্যান্সিয়াল ডেটা

```python
np.random.seed(42)
N = 10000

# ফিন্যান্সিয়াল ডেটা রিপ্রেজেন্টেশন
# ফিচার: রিটার্ন, ভলাটিলিটি, ভলিউম, স্প্রেড, ইত্যাদি
real_data = np.zeros((N, data_dim))

for i in range(N):
    # ফ্যাক্টর-বেসড মডেল
    factors = np.random.randn(8)
    factor_loading = np.random.randn(8, data_dim) * 0.5
    
    # বেস লাইন
    base = factors @ factor_loading
    
    # নয়েজ
    noise = np.random.randn(data_dim) * 0.15
    
    # অটোকোরিলেশন ইফেক্ট
    if i > 0:
        base += 0.3 * real_data[i-1]
    
    real_data[i] = base + noise

# স্ট্যান্ডার্ডাইজ
real_data = (real_data - real_data.mean(axis=0)) / real_data.std(axis=0)

# ট্রেন/টেস্ট স্প্লিট
real_train, real_test = train_test_split(real_data, test_size=0.2, random_state=42)

real_train_t = torch.FloatTensor(real_train).to(device)
dataset = DataLoader(TensorDataset(real_train_t, real_train_t), 
                     batch_size=128, shuffle=True)

print(f"রিয়েল ডেটা: {real_data.shape}")
print(f"  ট্রেন: {real_train.shape}, টেস্ট: {real_test.shape}")
print(f"  মিন: {real_data.mean():.4f}, স্টাড: {real_data.std():.4f}")
```

## 3. GAN ট্রেনিং

```python
# মডেল
G = SyntheticDataGenerator(noise_dim, data_dim).to(device)
D = SyntheticDataDiscriminator(data_dim).to(device)

criterion = nn.BCELoss()
g_optim = optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optim = optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

# ট্রেনিং
epochs = 100

for epoch in range(epochs):
    for batch_x, _ in dataset:
        batch_size = batch_x.size(0)
        
        real_lbl = torch.ones(batch_size, 1).to(device) * 0.9
        fake_lbl = torch.zeros(batch_size, 1).to(device) + 0.1
        
        # D ট্রেন
        D.zero_grad()
        d_real = criterion(D(batch_x), real_lbl)
        
        z = torch.randn(batch_size, noise_dim).to(device)
        fake = G(z)
        d_fake = criterion(D(fake.detach()), fake_lbl)
        d_loss = d_real + d_fake
        d_loss.backward()
        d_optim.step()
        
        # G ট্রেন
        G.zero_grad()
        z = torch.randn(batch_size, noise_dim).to(device)
        fake = G(z)
        g_loss = criterion(D(fake), real_lbl)
        g_loss.backward()
        g_optim.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{epochs} | D: {d_loss.item():.4f} | G: {g_loss.item():.4f}")

print("✅ GAN ট্রেনিং সম্পূর্ণ!")
```

## 4. সিন্থেটিক ডেটা জেনারেশন

```python
G.eval()

# সিন্থেটিক ডেটা জেনারেট
n_synthetic = 10000
with torch.no_grad():
    z = torch.randn(n_synthetic, noise_dim).to(device)
    synthetic_data = G(z).cpu().numpy()

print(f"সিন্থেটিক ডেটা: {synthetic_data.shape}")
```

## 5. স্ট্যাটিস্টিক্যাল ভ্যালিডেশন

```python
def validate_synthetic_data(real, synthetic):
    """সিন্থেটিক ডেটা ভ্যালিডেশন"""
    
    print("=" * 50)
    print("স্ট্যাটিস্টিক্যাল ভ্যালিডেশন")
    print("=" * 50)
    
    # 1. বেসিক স্ট্যাটিস্টিক্স
    print(f"\n1. বেসিক স্ট্যাটিস্টিক্স:")
    print(f"{'মেট্রিক':<20} {'রিয়েল':<15} {'সিন্থেটিক':<15}")
    print("-" * 50)
    print(f"{'মিন':<20} {real.mean():<15.4f} {synthetic.mean():<15.4f}")
    print(f"{'স্টাড':<20} {real.std():<15.4f} {synthetic.std():<15.4f}")
    print(f"{{'স্কিউ':<20}} {np.mean(real**3):<15.4f} {np.mean(synthetic**3):<15.4f}")
    print(f"{'কার্টোসিস':<20} {np.mean(real**4):<15.4f} {np.mean(synthetic**4):<15.4f}")
    
    # 2. ডিস্ট্রিবিউশন ম্যাচিং (KS টেস্ট)
    from scipy.stats import ks_2samp
    ks_stats = []
    print(f"\n2. KS টেস্ট (প্রথম ১০ ফিচার):")
    for i in range(min(10, data_dim)):
        stat, pval = ks_2samp(real[:, i], synthetic[:, i])
        ks_stats.append(stat)
        print(f"  ফিচার {i+1}: KS={stat:.4f}, p={pval:.4f}", 
              end="")
        if pval > 0.05:
            print(" ✅")
        else:
            print(" ❌")
    print(f"  গড় KS স্ট্যাট: {np.mean(ks_stats):.4f}")
    
    # 3. কোরিলেশন স্ট্রাকচার
    n_check = 10
    corr_real = np.corrcoef(real[:, :n_check].T)
    corr_syn = np.corrcoef(synthetic[:, :n_check].T)
    corr_diff = np.abs(corr_real - corr_syn).mean()
    print(f"\n3. কোরিলেশন স্ট্রাকচার:")
    print(f"  কোরিলেশন ম্যাট্রিক্স ডিফারেন্স: {corr_diff:.4f}")
    
    # 4. কভারিয়েন্স স্ট্রাকচার
    cov_real = np.cov(real, rowvar=False)
    cov_syn = np.cov(synthetic, rowvar=False)
    cov_diff = np.linalg.norm(cov_real - cov_syn) / np.linalg.norm(cov_real)
    print(f"  কভারিয়েন্স ডিফারেন্স (নর্মালাইজড): {cov_diff:.4f}")
    
    return {
        'ks_mean': np.mean(ks_stats),
        'corr_diff': corr_diff,
        'cov_diff': cov_diff
    }

metrics = validate_synthetic_data(real_data, synthetic_data)
```

## 6. ইউটিলিটি টেস্ট

```python
def utility_test(real, synthetic, test_size=0.2):
    """ডাউনস্ট্রিম টাস্কে ইউটিলিটি টেস্ট"""
    n, d = real.shape
    n_syn = synthetic.shape[0]
    
    # সিন্থেটিক টার্গেট (আসল ডেটার কাঠামো থেকে)
    y_real = real[:, 0] + 0.5 * real[:, 1] + np.random.randn(n) * 0.1
    y_syn = synthetic[:, 0] + 0.5 * synthetic[:, 1] + np.random.randn(n_syn) * 0.1
    
    # মডেল 1: শুধু রিয়েল ডেটা দিয়ে ট্রেন
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        real[:, 2:], y_real, test_size=test_size, random_state=42)
    
    lr_real = LinearRegression()
    lr_real.fit(Xr_train, yr_train)
    r2_real = r2_score(yr_test, lr_real.predict(Xr_test))
    
    # মডেল 2: রিয়েল + সিন্থেটিক ডেটা দিয়ে ট্রেন
    X_combined = np.vstack([real[:, 2:], synthetic[:, 2:]])
    y_combined = np.hstack([y_real, y_syn])
    
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_combined, y_combined, test_size=test_size, random_state=42)
    
    lr_combined = LinearRegression()
    lr_combined.fit(Xc_train, yc_train)
    r2_combined = r2_score(yr_test, lr_combined.predict(Xr_test))  # রিয়েল টেস্টে
    
    # মডেল 3: শুধু সিন্থেটিক ডেটা দিয়ে ট্রেন
    Xs_train, Xs_test, ys_train, ys_test = train_test_split(
        synthetic[:, 2:], y_syn, test_size=test_size, random_state=42)
    
    lr_syn = LinearRegression()
    lr_syn.fit(Xs_train, ys_train)
    r2_syn = r2_score(yr_test, lr_syn.predict(Xr_test))  # রিয়েল টেস্টে
    
    print(f"\n4. ইউটিলিটি টেস্ট (রিয়েল টেস্ট ডেটায় R²):")
    print(f"{'ট্রেনিং ডেটা':<25} {'R² স্কোর':<15}")
    print("-" * 40)
    print(f"{'শুধু রিয়েল':<25} {r2_real:<15.4f}")
    print(f"{'রিয়েল + সিন্থেটিক':<25} {r2_combined:<15.4f}")
    print(f"{'শুধু সিন্থেটিক':<25} {r2_syn:<15.4f}")
    
    return {'r2_real': r2_real, 'r2_combined': r2_combined, 'r2_syn': r2_syn}

utility_metrics = utility_test(real_data, synthetic_data)
```

## 7. প্রাইভেসি চেক

```python
def privacy_check(real, synthetic, k=5):
    """প্রাইভেসি মেট্রিক: Nearest Neighbor Distance"""
    from sklearn.neighbors import NearestNeighbors
    
    nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
    nn.fit(real)
    
    distances, indices = nn.kneighbors(synthetic)
    
    print(f"\n5. প্রাইভেসি চেক:")
    print(f"  মিন NN দূরত্ব: {distances.mean():.4f}")
    print(f"  মিন NN দূরত্ব (স্টাড): {distances.std():.4f}")
    
    # ক্লোজেস্ট পয়েন্ট চেক (< 5th percentile)
    threshold = np.percentile(distances, 5)
    privacy_risk = (distances < threshold).mean() * 100
    print(f"  প্রাইভেসি রিস্ক (৫% থ্রেশহোল্ড): {privacy_risk:.2f}%")
    
    if privacy_risk > 10:
        print("  ⚠️  বেশি প্রাইভেসি রিস্ক! মেমরি ওভারফিটিং হতে পারে")
    else:
        print("  ✅ প্রাইভেসি রিস্ক গ্রহণযোগ্য")
    
    return distances.mean()

privacy_dist = privacy_check(real_data, synthetic_data)
```

## 8. মোড কোল্যাপস ডিটেকশন

```python
def detect_mode_collapse(synthetic):
    """মোড কোল্যাপস ডিটেক্ট"""
    variance = synthetic.var(axis=0)
    variance_ratio = variance / variance.max()
    
    low_var_features = (variance_ratio < 0.1).sum()
    collapse_score = low_var_features / len(variance)
    
    if collapse_score > 0.3:
        print(f"\n6. 🚨 মোড কোল্যাপস ডিটেক্টেড! {low_var_features}/{len(variance)} ফিচার কম ভ্যারিয়েন্স")
    else:
        print(f"\n6. ✅ মোড কোল্যাপস নেই: {low_var_features}/{len(variance)} ফিচার কম ভ্যারিয়েন্স")
    
    return collapse_score

collapse_score = detect_mode_collapse(synthetic_data)
```

## 9. সিন্থেটিক ডেটা সেভ

```python
# সিন্থেটিক ডেটা সেভ
import pickle

synthetic_package = {
    'data': synthetic_data,
    'n_samples': n_synthetic,
    'n_features': data_dim,
    'model': 'GAN',
    'validation_metrics': {
        **metrics,
        **utility_metrics,
        'privacy_distance': privacy_dist,
        'collapse_score': collapse_score
    }
}

# Save as pickle
with open('synthetic_financial_data.pkl', 'wb') as f:
    pickle.dump(synthetic_package, f)

# Save as numpy
np.save('synthetic_financial_data.npy', synthetic_data)

print(f"\n✅ সিন্থেটিক ডেটা সেভ করা হয়েছে:")
print(f"  synthetic_financial_data.npy")
print(f"  synthetic_financial_data.pkl")
print(f"  ডেটা সাইজ: {synthetic_data.nbytes / 1024 / 1024:.2f} MB")
```

## সেরা প্র্যাকটিস সমূহ

```python
# সিন্থেটিক ডেটা জেনারেশন গাইডলাইন
guidelines = """
সিন্থেটিক ফিন্যান্সিয়াল ডেটা জেনারেশন গাইডলাইন:

1. ডেটা কোয়ালিটি
   - স্ট্যাটিস্টিক্যাল ম্যাচিং ভেরিফাই করুন
   - কোরিলেশন স্ট্রাকচার চেক করুন
   - টেইল বিহেভিয়ার ম্যাচ করুন

2. প্রাইভেসি
   - Nearest Neighbor Distance চেক করুন
   - মেমরি ওভারফিটিং এড়িয়ে চলুন
   - ডিফারেন্সিয়াল প্রাইভেসি বিবেচনা করুন

3. ইউটিলিটি
   - ডাউনস্ট্রিম টাস্কে ভ্যালিডেট করুন
   - রিয়েল vs সিন্থেটিক ট্রেনিং তুলনা
   - মডেল পারফরম্যান্স মনিটর করুন

4. রেগুলেটরি
   - রেগুলেটরকে জানান (সিন্থেটিক ডেটা ব্যবহার)
   - ডকুমেন্টেশন রাখুন
   - অডিট ট্রেইল বজায় রাখুন
"""

print(guidelines)
```

## সারাংশ
- GAN সিন্থেটিক ফিন্যান্সিয়াল ডেটা জেনারেট করতে পারে
- স্ট্যাটিস্টিক্যাল ম্যাচিং, কোরিলেশন, ইউটিলিটি টেস্ট জরুরি
- প্রাইভেসি ঝুঁকি মূল্যায়ন করা প্রয়োজন
- মোড কোল্যাপস ডিটেক্ট করা গুরুত্বপূর্ণ
- সিন্থেটিক ডেটা ডেটা অগমেন্টেশন, ব্যক্তেস্টিং, প্রাইভেসি-প্রিজারভিং শেয়ারিং-এ ব্যবহার করা যায়
- ডাউনস্ট্রিম টাস্কে ইউটিলিটি টেস্ট করে ভেরিফাই করুন