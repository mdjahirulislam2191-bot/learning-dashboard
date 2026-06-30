# Day 33: ভ্যারিয়েশনাল অটোএনকোডার (VAE) 🎨

## VAE কী?
VAE (Variational Autoencoder) একটি জেনারেটিভ মডেল যা শুধু ডেটা কম্প্রেস নয়, নতুন ডেটাও জেনারেট করতে পারে। এটি ল্যাটেন্ট স্পেসকে একটি প্রোবাবিলিস্টিক ডিস্ট্রিবিউশন হিসেবে মডেল করে।

### VAE vs সাধারণ AE
| বৈশিষ্ট্য | সাধারণ AE | VAE |
|---|---|---|
| ল্যাটেন্ট স্পেস | ডিটারমিনিস্টিক (পয়েন্ট) | প্রোবাবিলিস্টিক (ডিস্ট্রিবিউশন) |
| আউটপুট | ডেটা রিকন্সট্রাকশন | নতুন ডেটা জেনারেশন |
| লস | MSE মাত্র | Reconstruction + KL Divergence |
| ল্যাটেন্ট রেগুলারাইজেশন | নেই | KL Loss (নরমাল ডিস্ট্রিবিউশন) |
| জেনারেটিভ | না | হ্যাঁ |

### ফিন্যান্সে ব্যবহার
- সিন্থেটিক মার্কেট ডেটা জেনারেশন
- ব্যক্তেস্টিং-এর জন্য ডেটা অগমেন্টেশন
- রিস্ক সিনারিও জেনারেশন
- পোর্টফোলিও অপ্টিমাইজেশন

## VAE আর্কিটেকচার

```
ইনপুট x
    ↓
[এনকোডার] → μ এবং σ (ল্যাটেন্ট প্যারামিটার)
    ↓
z = μ + σ * ε  (রিপ্যারামিটারাইজেশন ট্রিক)
    ↓
[ডিকোডার]
    ↓
আউটপুট x̂

লস: reconstruction_loss + KL_divergence
```

## PyTorch VAE ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

class VAE(nn.Module):
    """ভ্যারিয়েশনাল অটোএনকোডার"""
    def __init__(self, input_dim, hidden_dim=256, latent_dim=8):
        super().__init__()
        
        # এনকোডার
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # ল্যাটেন্ট প্যারামিটার
        self.mu_layer = nn.Linear(hidden_dim, latent_dim)
        self.logvar_layer = nn.Linear(hidden_dim, latent_dim)
        
        # ডিকোডার
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()
        )
    
    def encode(self, x):
        h = self.encoder(x)
        mu = self.mu_layer(h)
        logvar = self.logvar_layer(h)
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        """রিপ্যারামিটারাইজেশন ট্রিক"""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z):
        return self.decoder(z)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        reconstruction = self.decode(z)
        return reconstruction, mu, logvar
    
    def loss_function(self, recon_x, x, mu, logvar):
        """VAE লস: Reconstruction + KL Divergence"""
        # Reconstruction loss (BCE or MSE)
        recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
        # recon_loss = F.mse_loss(recon_x, x, reduction='sum')  # MSE alternative
        
        # KL Divergence
        # D_KL(q(z|x) || p(z)) where p(z) ~ N(0, 1)
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        
        return recon_loss + kl_loss, recon_loss, kl_loss
    
    def generate(self, num_samples, device='cpu'):
        """নতুন ডেটা জেনারেট"""
        z = torch.randn(num_samples, self.mu_layer.out_features).to(device)
        samples = self.decode(z)
        return samples

# টেস্ট
vae = VAE(input_dim=50, hidden_dim=256, latent_dim=8)
x = torch.randn(16, 50)
recon, mu, logvar = vae(x)
print(f"ইনপুট: {x.shape} → রিকন্সট্রাক্টেড: {recon.shape}")
print(f"ল্যাটেন্ট μ: {mu.shape}, log(σ²): {logvar.shape}")
```

## সিন্থেটিক ফিন্যান্স ডেটা জেনারেশন

```python
# ফিন্যান্সিয়াল ডেটা (ফ্যাক্টর-বেসড)
np.random.seed(42)
n_samples = 5000
n_features = 50

# ট্রু ফ্যাক্টর স্ট্রাকচার
true_factors = np.random.randn(n_samples, 4)
factor_weights = np.random.randn(4, n_features)
financial_data = true_factors @ factor_weights
financial_data += np.random.randn(n_samples, n_features) * 0.05

# 0-1 নরমালাইজ
financial_data = (financial_data - financial_data.min(axis=0)) / \
                 (financial_data.max(axis=0) - financial_data.min(axis=0))

data_tensor = torch.FloatTensor(financial_data)
dataset = TensorDataset(data_tensor, data_tensor)
loader = DataLoader(dataset, batch_size=128, shuffle=True)

print(f"ফিন্যান্স ডেটা: {financial_data.shape}")
print(f"ট্রু ফ্যাক্টরস: {true_factors.shape}")
```

## VAE ট্রেনিং

```python
# মডেল
vae = VAE(input_dim=n_features, hidden_dim=256, latent_dim=8)
optimizer = optim.Adam(vae.parameters(), lr=1e-3)

# ট্রেনিং
epochs = 100
history = {'total': [], 'recon': [], 'kl': []}

for epoch in range(epochs):
    total_loss = 0
    total_recon = 0
    total_kl = 0
    
    for batch_x, _ in loader:
        optimizer.zero_grad()
        recon_batch, mu, logvar = vae(batch_x)
        loss, recon_loss, kl_loss = vae.loss_function(recon_batch, batch_x, mu, logvar)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        total_recon += recon_loss.item()
        total_kl += kl_loss.item()
    
    avg_loss = total_loss / len(loader.dataset)
    avg_recon = total_recon / len(loader.dataset)
    avg_kl = total_kl / len(loader.dataset)
    
    history['total'].append(avg_loss)
    history['recon'].append(avg_recon)
    history['kl'].append(avg_kl)
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"  Total Loss: {avg_loss:.4f}")
        print(f"  Recon Loss: {avg_recon:.4f}")
        print(f"  KL Loss: {avg_kl:.4f}")

print("\n✅ VAE ট্রেনিং সম্পূর্ণ!")
```

## ল্যাটেন্ট স্পেস ভিজুয়ালাইজেশন

```python
def visualize_latent_space(model, data, labels=None):
    """ল্যাটেন্ট স্পেস 2D প্রজেকশন"""
    model.eval()
    with torch.no_grad():
        mu, logvar = model.encode(data)
        z = model.reparameterize(mu, logvar).numpy()
    
    # PCA to 2D
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    z_2d = pca.fit_transform(z)
    
    print(f"ল্যাটেন্ট স্পেস ভ্যারিয়েন্স ব্যাখ্যা:")
    print(f"  ২টি PCA কম্পোনেন্ট: {pca.explained_variance_ratio_.sum():.2%}")
    
    # ল্যাটেন্ট ডিস্ট্রিবিউশন স্ট্যাটিস্টিক্স
    print(f"\nল্যাটেন্ট ডিস্ট্রিবিউশন চেক:")
    for i in range(min(4, z.shape[1])):
        print(f"  ডাইম {i+1}: μ={z[:,i].mean():.4f}, σ={z[:,i].std():.4f}")
        expected_near_01 = abs(z[:,i].mean()) < 0.2 and abs(z[:,i].std() - 1) < 0.3
        print(f"    {'✅ N(0,1) এর কাছাকাছি' if expected_near_01 else '❌ N(0,1) থেকে দূরে'}")
    
    return z, z_2d

# ভিজুয়ালাইজ
vae.eval()
z, z_2d = visualize_latent_space(vae, data_tensor[:1000])
```

## নতুন ডেটা জেনারেশন

```python
# ল্যাটেন্ট স্পেস থেকে নতুন ডেটা জেনারেট
vae.eval()
num_new_samples = 100

with torch.no_grad():
    generated = vae.generate(num_new_samples)

generated_np = generated.numpy()
print(f"জেনারেটেড ডেটা: {generated_np.shape}")
print(f"ভ্যালু রেঞ্জ: [{generated_np.min():.4f}, {generated_np.max():.4f}]")

# জেনারেটেড ডেটার স্ট্যাটিস্টিক্স
orig_mean = financial_data.mean(axis=0)
gen_mean = generated_np.mean(axis=0)
orig_std = financial_data.std(axis=0)
gen_std = generated_np.std(axis=0)

print(f"\nঅরিজিনাল vs জেনারেটেড তুলনা:")
print(f"{'স্ট্যাট':<15} {'অরিজিনাল':<15} {'জেনারেটেড':<15}")
print("-" * 45)
print(f"{'মিন (গড়)':<15} {orig_mean.mean():<15.4f} {gen_mean.mean():<15.4f}")
print(f"{'স্টাড':<15} {orig_std.mean():<15.4f} {gen_std.mean():<15.4f}")
print(f"{'মিন':<15} {orig_mean.min():<15.4f} {gen_mean.min():<15.4f}")
print(f"{'ম্যাক্স':<15} {orig_mean.max():<15.4f} {gen_mean.max():<15.4f}")

# ফিচার কোরিলেশন তুলনা
corr_orig = np.corrcoef(financial_data[:, :10].T)
corr_gen = np.corrcoef(generated_np[:, :10].T)
corr_diff = np.abs(corr_orig - corr_gen).mean()
print(f"\nকোরিলেশন ম্যাট্রিক্স ডিফারেন্স: {corr_diff:.4f}")
print("(0-র কাছাকাছি হলে ভালো - কোরিলেশন স্ট্রাকচার সংরক্ষিত)")
```

## ইন্টারপোলেশন ও ল্যাটেন্ট ওয়াক

```python
def latent_walk(model, n_steps=10, dim=0, low=-3, high=3):
    """ল্যাটেন্ট স্পেসে ওয়াক"""
    model.eval()
    z = torch.zeros(1, model.mu_layer.out_features)
    
    with torch.no_grad():
        images = []
        for val in np.linspace(low, high, n_steps):
            z[0, dim] = val
            decoded = model.decode(z)
            images.append(decoded)
    
    return torch.cat(images)

def interpolate(model, z1, z2, steps=10):
    """দুটি ল্যাটেন্ট পয়েন্টের মাঝে ইন্টারপোলেট"""
    model.eval()
    alphas = np.linspace(0, 1, steps)
    
    with torch.no_grad():
        interpolated = []
        for alpha in alphas:
            z = (1 - alpha) * z1 + alpha * z2
            decoded = model.decode(z.unsqueeze(0))
            interpolated.append(decoded)
    
    return torch.cat(interpolated)

# ল্যাটেন্ট ওয়াক
walk = latent_walk(vae, n_steps=10, dim=0, low=-3, high=3)
print(f"ল্যাটেন্ট ওয়াক (ডাইম 0): {walk.shape}")
print(f"  লো (-3): {walk[0, :5].detach().numpy()}")
print(f"  হাই (3): {walk[-1, :5].detach().numpy()}")

# ইন্টারপোলেশন
with torch.no_grad():
    z1 = torch.randn(1, vae.mu_layer.out_features)
    z2 = torch.randn(1, vae.mu_layer.out_features)

interp = interpolate(vae, z1[0], z2[0], steps=5)
print(f"\nইন্টারপোলেশন: {interp.shape}")
for i in range(5):
    print(f"  α={i/4:.2f}: ফিচার মিন={interp[i].mean():.4f}")
```

## VAE হাইপারপ্যারামিটার টিউনিং

```python
# ল্যাটেন্ট ডাইমেনশন টিউনিং
latent_dims = [2, 4, 8, 16, 32]
results = []

for latent_dim in latent_dims:
    vae = VAE(input_dim=n_features, hidden_dim=256, latent_dim=latent_dim)
    optimizer = optim.Adam(vae.parameters(), lr=1e-3)
    
    for epoch in range(30):
        total_loss = 0
        for bx, _ in loader:
            optimizer.zero_grad()
            recon, mu, logvar = vae(bx)
            loss, r_loss, kl_loss = vae.loss_function(recon, bx, mu, logvar)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
    
    avg_loss = total_loss / len(loader.dataset)
    
    # জেনারেশন কোয়ালিটি
    with torch.no_grad():
        gen = vae.generate(100)
        gen_corr = np.corrcoef(gen.numpy()[:, :10].T)
        orig_corr = np.corrcoef(financial_data[:100, :10].T)
        corr_sim = 1 - np.abs(gen_corr - orig_corr).mean()
    
    results.append((latent_dim, avg_loss, corr_sim))
    print(f"latent_dim={latent_dim:<3}: Loss={avg_loss:.4f}, CorrSim={corr_sim:.4f}")

best = max(results, key=lambda r: r[2])
print(f"\n🏆 সেরা ল্যাটেন্ট ডাইমেনশন: {best[0]} (CorrSim={best[2]:.4f})")
```

## VAE দিয়ে রিস্ক সিনারিও জেনারেশন

```python
# ক্রাইসিস সিনারিও জেনারেট করতে VAE ব্যবহার
vae.eval()

with torch.no_grad():
    # নরমাল মার্কেট জেনারেট
    z_normal = torch.randn(100, vae.mu_layer.out_features)
    normal_scenarios = vae.decode(z_normal)
    
    # স্ট্রেস সিনারিও (ল্যাটেন্টে শিফট)
    z_stress = torch.randn(100, vae.mu_layer.out_features) + 0.5  # μ=0.5 এ শিফট
    stress_scenarios = vae.decode(z_stress)

normal_mean = normal_scenarios.mean(dim=0)
stress_mean = stress_scenarios.mean(dim=0)
shock = stress_mean - normal_mean

print("VAE রিস্ক সিনারিও অ্যানালাইসিস:")
print(f"  নরমাল সিনারিও গড়: {normal_mean.mean():.4f}")
print(f"  স্ট্রেস সিনারিও গড়: {stress_mean.mean():.4f}")
print(f"  গড় শক: {shock.mean():.4f}")
print(f"  সর্বোচ্চ শক ফিচার: {shock.abs().max():.4f}")
print(f"  ফিচারস এফেক্টেড (>1σ): {(shock.abs() > shock.std()).sum().item()}")

# পোর্টফোলিও ইমপ্যাক্ট
weights = np.ones(n_features) / n_features
normal_portfolio = (normal_scenarios.numpy() @ weights)
stress_portfolio = (stress_scenarios.numpy() @ weights)

print(f"\nপোর্টফোলিও ইমপ্যাক্ট:")
print(f"  নরমাল রিটার্ন: μ={normal_portfolio.mean():.4f}, "
      f"σ={normal_portfolio.std():.4f}")
print(f"  স্ট্রেস রিটার্ন: μ={stress_portfolio.mean():.4f}, "
      f"σ={stress_portfolio.std():.4f}")
print(f"  Expected Shortfall (95%): {np.percentile(stress_portfolio, 5):.4f}")
```

## সারাংশ
- VAE প্রোবাবিলিস্টিক ল্যাটেন্ট স্পেস মডেল করে
- Reconstruction + KL Divergence লস ব্যবহার করে
- নতুন ডেটা জেনারেট করতে পারে (জেনারেটিভ মডেল)
- রিপ্যারামিটারাইজেশন ট্রিক গ্র্যাডিয়েন্ট ফ্লো সক্ষম করে
- ফিন্যান্সে সিন্থেটিক ডেটা, রিস্ক সিনারিও, পোর্টফোলিও অ্যানালাইসিসে ব্যবহৃত
- ল্যাটেন্ট ডাইমেনশন টিউনিং গুরুত্বপূর্ণ হাইপারপ্যারামিটার