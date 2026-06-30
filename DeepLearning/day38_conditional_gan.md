# Day 38: কন্ডিশনাল GAN (Conditional GAN) 🏷️

## কন্ডিশনাল GAN কী?
CGAN হল GAN-এর একটি এক্সটেনশন যেখানে জেনারেটর ও ডিসক্রিমিনেটর উভয়েই অতিরিক্ত তথ্য (কন্ডিশন) গ্রহণ করে। এটি নির্দিষ্ট ধরণের ডেটা জেনারেট করতে পারে।

### cGAN vs সাধারণ GAN
| বৈশিষ্ট্য | GAN | cGAN |
|---|---|---|
| জেনারেটর ইনপুট | z (নয়েজ) | z + c (কন্ডিশন) |
| ডি ইনপুট | x (ডেটা) | x + c (ডেটা + কন্ডিশন) |
| জেনারেশন | র্যান্ডম | কন্ডিশন-কন্ট্রোলড |
| নিয়ন্ত্রণ | নেই | আছে (কন্ডিশন অনুযায়ী) |

### ফিন্যান্সে ব্যবহার
1. **মার্কেট রেজিম-স্পেসিফিক ডেটা জেনারেশন** (বুল/বিয়ার মার্কেট)
2. **ভলাটিলিটি-কন্ডিশনাল ডেটা** (হাই/লো ভোল)
3. **সেক্টর-স্পেসিফিক স্টক ডেটা** (টেক, এনার্জি, ফাইন্যান্স)
4. **রিস্ক প্রোফাইল-বেসড সিন্থেটিক ডেটা**

## PyTorch cGAN ইমপ্লিমেন্টেশন

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

## cGAN মডেল

```python
class ConditionalGenerator(nn.Module):
    """কন্ডিশনাল জেনারেটর"""
    def __init__(self, noise_dim=100, condition_dim=5, output_dim=50):
        super().__init__()
        
        input_dim = noise_dim + condition_dim
        
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, output_dim),
            nn.Tanh()
        )
    
    def forward(self, z, condition):
        # কন্ডিশন কনক্যাট
        x = torch.cat([z, condition], dim=1)
        return self.model(x)

class ConditionalDiscriminator(nn.Module):
    """কন্ডিশনাল ডিসক্রিমিনেটর"""
    def __init__(self, input_dim=50, condition_dim=5):
        super().__init__()
        
        total_dim = input_dim + condition_dim
        
        self.model = nn.Sequential(
            nn.Linear(total_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x, condition):
        # কন্ডিশন কনক্যাট
        x = torch.cat([x, condition], dim=1)
        return self.model(x)

# টেস্ট
noise_dim, cond_dim, data_dim = 100, 5, 50
G_cond = ConditionalGenerator(noise_dim, cond_dim, data_dim).to(device)
D_cond = ConditionalDiscriminator(data_dim, cond_dim).to(device)

z = torch.randn(16, noise_dim).to(device)
c = torch.randn(16, cond_dim).to(device)
x = torch.randn(16, data_dim).to(device)

fake = G_cond(z, c)
validity = D_cond(x, c)

print(f"cGen: {z.shape} + {c.shape} → {fake.shape}")
print(f"cDis: {x.shape} + {c.shape} → {validity.shape}")
```

## ফিন্যান্সিয়াল ডেটা উইথ কন্ডিশন

```python
# ডেটা জেনারেশন
np.random.seed(42)
N = 10000
n_features = 50

# কন্ডিশন: মার্কেট রেজিম (one-hot encoded)
# [বুল মার্কেট, বিয়ার মার্কেট, হাই ভোল, লো ভোল, রেঞ্জ-বাউন্ড]
n_conditions = 5
conditions = np.random.randint(0, 2, size=(N, n_conditions))

# ডেটা জেনারেশন (কন্ডিশন-নির্ভর)
data = np.zeros((N, n_features))

for i in range(N):
    regime = np.argmax(conditions[i])
    
    if regime == 0:  # বুল মার্কেট
        data[i] = np.random.randn(n_features) * 0.5 + 0.5
    elif regime == 1:  # বিয়ার মার্কেট
        data[i] = np.random.randn(n_features) * 0.8 - 0.3
    elif regime == 2:  # হাই ভোল
        data[i] = np.random.randn(n_features) * 2.0
    elif regime == 3:  # লো ভোল
        data[i] = np.random.randn(n_features) * 0.2 + 0.1
    else:  # রেঞ্জ-বাউন্ড
        data[i] = np.random.uniform(-1, 1, n_features)

# নরমালাইজ (-1, 1)
data = data / np.abs(data).max()

print(f"ডেটা: {data.shape}")
print(f"কন্ডিশন: {conditions.shape}")
for i in range(n_conditions):
    n_samples = (conditions[:, i] == 1).sum()
    cond_mean = data[conditions[:, i] == 1].mean()
    print(f"  কন্ডিশন {i}: {n_samples} স্যাম্পল, μ={cond_mean:.4f}")
```

## cGAN ট্রেনিং

```python
# টেন্সর
data_tensor = torch.FloatTensor(data).to(device)
cond_tensor = torch.FloatTensor(conditions).to(device)

dataset = TensorDataset(data_tensor, cond_tensor, data_tensor, cond_tensor)
loader = DataLoader(dataset, batch_size=128, shuffle=True)

# মডেল
G = ConditionalGenerator(noise_dim, n_conditions, n_features).to(device)
D = ConditionalDiscriminator(n_features, n_conditions).to(device)

criterion = nn.BCELoss()
g_optim = optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optim = optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

# ট্রেনিং
epochs = 80
print("cGAN ট্রেনিং শুরু...")
for epoch in range(epochs):
    for batch_x, batch_c, _, _ in loader:
        batch_size = batch_x.size(0)
        
        # লেবেল (স্মুথিং)
        real_lbl = torch.ones(batch_size, 1).to(device) * 0.9
        fake_lbl = torch.zeros(batch_size, 1).to(device) + 0.1
        
        # === D ট্রেন ===
        D.zero_grad()
        
        real_validity = D(batch_x, batch_c)
        d_real_loss = criterion(real_validity, real_lbl)
        
        z = torch.randn(batch_size, noise_dim).to(device)
        fake_data = G(z, batch_c)
        fake_validity = D(fake_data.detach(), batch_c)
        d_fake_loss = criterion(fake_validity, fake_lbl)
        
        d_loss = d_real_loss + d_fake_loss
        d_loss.backward()
        d_optim.step()
        
        # === G ট্রেন ===
        G.zero_grad()
        
        z = torch.randn(batch_size, noise_dim).to(device)
        fake_data = G(z, batch_c)
        fake_validity = D(fake_data, batch_c)
        g_loss = criterion(fake_validity, real_lbl)
        
        g_loss.backward()
        g_optim.step()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs} | D: {d_loss.item():.4f} | G: {g_loss.item():.4f}")

print("✅ cGAN ট্রেনিং সম্পূর্ণ!")
```

## কন্ডিশন-ভিত্তিক ডেটা জেনারেশন

```python
G.eval()

# নির্দিষ্ট কন্ডিশনে ডেটা জেনারেট
with torch.no_grad():
    # বুল মার্কেট ডেটা জেনারেট
    bull_cond = torch.FloatTensor([[1, 0, 0, 0, 0]]).to(device)
    z = torch.randn(500, noise_dim).to(device)
    bull_data = G(z, bull_cond.repeat(500, 1)).cpu().numpy()
    
    # বিয়ার মার্কেট ডেটা জেনারেট
    bear_cond = torch.FloatTensor([[0, 1, 0, 0, 0]]).to(device)
    bear_data = G(z, bear_cond.repeat(500, 1)).cpu().numpy()
    
    # হাই ভোল ডেটা
    high_vol_cond = torch.FloatTensor([[0, 0, 1, 0, 0]]).to(device)
    high_vol_data = G(z, high_vol_cond.repeat(500, 1)).cpu().numpy()

print("কন্ডিশন-নির্দিষ্ট ডেটা জেনারেশন:")
print(f"{'মার্কেট':<20} {'মিন':<15} {'স্টাড':<15}")
print("-" * 50)
print(f"{'বুল':<20} {bull_data.mean():<15.4f} {bull_data.std():<15.4f}")
print(f"{'বিয়ার':<20} {bear_data.mean():<15.4f} {bear_data.std():<15.4f}")
print(f"{'হাই ভোল':<20} {high_vol_data.mean():<15.4f} {high_vol_data.std():<15.4f}")
```

## কন্ডিশন ইন্টিগ্রিটি চেক

```python
# চেক: জেনারেটেড ডেটা কি কন্ডিশনের সাথে সামঞ্জস্যপূর্ণ?
print("কন্ডিশন ইন্টিগ্রিটি চেক:")
print(f"{'কন্ডিশন':<20} {'এক্সপেক্টেড μ':<20} {'একচুয়াল μ':<20}")
print("-" * 60)

# অরিজিনাল ডেটা থেকে এক্সপেক্টেশন
for i in range(n_conditions):
    original_mean = data[conditions[:, i] == 1].mean()
    if i == 0:
        gen_mean = bull_data.mean()
    elif i == 1:
        gen_mean = bear_data.mean()
    elif i == 2:
        gen_mean = high_vol_data.mean()
    else:
        continue
    
    print(f"{'কন্ডিশন '+str(i):<20} {original_mean:<20.4f} {gen_mean:<20.4f}")

# কন্ডিশন রিকগনিশন টেস্ট
from sklearn.linear_model import LogisticRegression

# জেনারেটেড ডেটায় কন্ডিশন প্রেডিক্ট করতে পারি?
X_test = np.vstack([bull_data[:200], bear_data[:200], high_vol_data[:200]])
y_test = np.array([0]*200 + [1]*200 + [2]*200)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_test, y_test)
accuracy = clf.score(X_test, y_test)

print(f"\nকন্ডিশন ক্লাসিফিকেশন অ্যাকুরেসি: {accuracy:.4f}")
print(f"(>0.90 হলে কন্ডিশন ভালোভাবে এনফোর্সড)")
```

## মাল্টি-কন্ডিশন ডেটা জেনারেশন

```python
# কম্বিনেশন কন্ডিশন
def generate_conditioned_data(model, condition_vector, n_samples=100):
    """একটি নির্দিষ্ট কন্ডিশনে ডেটা জেনারেট"""
    model.eval()
    with torch.no_grad():
        cond = torch.FloatTensor(condition_vector).to(device).repeat(n_samples, 1)
        z = torch.randn(n_samples, noise_dim).to(device)
        generated = model(z, cond).cpu().numpy()
    return generated

# বিভিন্ন কন্ডিশনে ডেটা জেনারেট
conditions_to_generate = {
    'বুল + লো ভোল': [1, 0, 0, 1, 0],
    'বিয়ার + হাই ভোল': [0, 1, 1, 0, 0],
    'রেঞ্জ-বাউন্ড': [0, 0, 0, 0, 1],
}

print("মাল্টি-কন্ডিশন ডেটা জেনারেশন:")
for name, cond in conditions_to_generate.items():
    data = generate_conditioned_data(G, cond, n_samples=200)
    print(f"  {name}: μ={data.mean():.4f}, σ={data.std():.4f}")
```

## cGAN অ্যাপ্লিকেশন: ইম্ব্যালেন্সড ডেটা

```python
# ইম্ব্যালেন্সড ক্লাসের জন্য cGAN
# সমস্যা: ফ্রড ডেটা খুবই কম
# সমাধান: cGAN দিয়ে ফ্রড ক্লাসের ডেটা জেনারেট

# সিমুলেটেড ইম্ব্যালেন্সড সিনারিও
n_normal = 5000
n_fraud = 50  # শুধু ১% ফ্রড
n_features = 30

normal_data = np.random.randn(n_normal, n_features) * 0.5
fraud_data = np.random.randn(n_fraud, n_features) * 1.5 + 2  # ভিন্ন প্যাটার্ন

all_data = np.vstack([normal_data, fraud_data])
labels = np.array([0]*n_normal + [1]*n_fraud).reshape(-1, 1)

print(f"ইম্ব্যালেন্সড ডেটা:")
print(f"  নরমাল: {n_normal}")
print(f"  ফ্রড: {n_fraud}")
print(f"  রেশিও: {n_fraud/(n_normal+n_fraud):.2%}")

# cGAN দিয়ে ফ্রড ডেটা জেনারেট করে ব্যালেন্স করা
# (প্র্যাকটিসে কন্ডিশন হিসেবে ক্লাস লেবেল ব্যবহার করা হয়)
print("cGAN ফ্রড ডেটা জেনারেশন করে ক্লাস ব্যালেন্স করতে পারে ✓")
```

## সারাংশ
- cGAN কন্ডিশন ইনপুট নিয়ে নির্দিষ্ট ধরণের ডেটা জেনারেট করে
- জেনারেটর ও ডিসক্রিমিনেটর উভয়েই কন্ডিশন পায়
- ফিন্যান্সে মার্কেট রেজিম-স্পেসিফিক ডেটা, ফ্রড ডিটেকশন ব্যালেন্সিং
- কন্ডিশন ইন্টিগ্রিটি চেক গুরুত্বপূর্ণ
- ইম্ব্যালেন্সড ডেটা সেট ব্যালেন্স করতে ব্যবহার করা যায়
- মাল্টি-কন্ডিশন কম্বিনেশন সম্ভব