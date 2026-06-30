# Day 34: অটোএনকোডার দিয়ে ডাইমেনশনালিটি রিডাকশন 📉

## ডাইমেনশনালিটি রিডাকশন কী?
উচ্চ-মাত্রিক ডেটাকে নিম্ন-মাত্রিক স্পেসে ম্যাপ করা, যেখানে গুরুত্বপূর্ণ তথ্য সংরক্ষিত থাকে।

### কেন প্রয়োজন?
1. **কার্স অফ ডাইমেনশনালিটি**: বেশি ডাইমেনশন = বেশি ডেটা প্রয়োজন
2. **কম্পিউটেশনাল এফিশিয়েন্সি**: কম ডাইমেনশন = দ্রুত প্রসেসিং
3. **ওভারফিটিং কমানো**: কম ফিচার = কম নয়েজ
4. **ভিজুয়ালাইজেশন**: 2D/3D তে ভিজুয়ালাইজ করা যায়
5. **নয়েজ রিডাকশন**: অপ্রাসঙ্গিক ফিচার বাদ দেওয়া

### PCA vs অটোএনকোডার
| বৈশিষ্ট্য | PCA | অটোএনকোডার |
|---|---|---|
| টাইপ | লিনিয়ার | নন-লিনিয়ার |
| ট্রান্সফর্ম | অর্থোগোনাল প্রজেকশন | নিউরাল নেটওয়ার্ক |
| লস | ধরা পড়ে না | নন-লিনিয়ার প্যাটার্ন ক্যাপচার |
| স্কেলেবিলিটি | বড় ডেটায় ধীর | GPU-তে দ্রুত |
| ইন্টারপ্রিটেবিলিটি | বেশি (কম্পোনেন্ট) | কম (ব্ল্যাক বক্স) |

## PCA বেসলাইন

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

# ফিন্যান্সিয়াল ডেটা
np.random.seed(42)
n = 5000
true_dim = 5
n_features = 50

factors = np.random.randn(n, true_dim)
W = np.random.randn(true_dim, n_features)
data = factors @ W + np.random.randn(n, n_features) * 0.1

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# PCA
pca = PCA(n_components=0.95)  # 95% ভ্যারিয়েন্স ধরে
pca_result = pca.fit_transform(data_scaled)

print(f"অরিজিনাল ডাইমেনশন: {n_features}")
print(f"PCA কম্পোনেন্ট (95% ভ্যারিয়েন্স): {pca.n_components_}")
print(f"ব্যাখ্যাত ভ্যারিয়েন্স: {pca.explained_variance_ratio_.cumsum()[-1]:.2%}")
print(f"প্রথম ৫ কম্পোনেন্টের ভ্যারিয়েন্স:")
for i, ratio in enumerate(pca.explained_variance_ratio_[:5]):
    print(f"  PC{i+1}: {ratio:.2%}")
```

## অটোএনকোডার দিয়ে ডাইমেনশনালিটি রিডাকশন

```python
class DimReductionAE(nn.Module):
    """ডাইমেনশনালিটি রিডাকশনের জন্য অটোএনকোডার"""
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        
        # এনকোডার (স্তরায়িত রিডাকশন)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, encoding_dim)
        )
        
        # ডিকোডার
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def encode(self, x):
        return self.encoder(x)

# অটোএনকোডার ট্রেনিং
target_dim = pca.n_components_
ae = DimReductionAE(input_dim=n_features, encoding_dim=target_dim)

data_tensor = torch.FloatTensor(data_scaled)
dataset = TensorDataset(data_tensor, data_tensor)
loader = DataLoader(dataset, batch_size=128, shuffle=True)

criterion = nn.MSELoss()
optimizer = optim.Adam(ae.parameters(), lr=0.001)

print(f"\nঅটোএনকোডার ডাইমেনশন রিডাকশন:")
print(f"  {n_features} → {target_dim} → {n_features}")
print(f"  কম্প্রেশন রেশিও: {n_features/target_dim:.1f}x")

epochs = 80
for epoch in range(epochs):
    total_loss = 0
    for bx, _ in loader:
        optimizer.zero_grad()
        reconstructed = ae(bx)
        loss = criterion(reconstructed, bx)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 20 == 0:
        print(f"  Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")
```

## PCA vs AE রিকন্সট্রাকশন তুলনা

```python
ae.eval()

# PCA রিকন্সট্রাকশন
pca_reconst = pca.inverse_transform(pca_result)

# AE রিকন্সট্রাকশন
with torch.no_grad():
    ae_reconst = ae(data_tensor).numpy()

# MSE তুলনা
pca_mse = np.mean((data_scaled - pca_reconst) ** 2)
ae_mse = np.mean((data_scaled - ae_reconst) ** 2)

print(f"{'মেট্রিক':<25} {'PCA':<15} {'Autoencoder':<15}")
print("-" * 55)
print(f"{'রিকন্সট্রাকশন MSE':<25} {pca_mse:<15.6f} {ae_mse:<15.6f}")
print(f"{'RMSE':<25} {np.sqrt(pca_mse):<15.6f} {np.sqrt(ae_mse):<15.6f}")
print(f"{'ইমপ্রুভমেন্ট':<25} {'-':<15} {((pca_mse-ae_mse)/pca_mse*100):<14.2f}%")

# পার ফিচার MSE
for i in range(min(10, n_features)):
    pca_feat_mse = np.mean((data_scaled[:, i] - pca_reconst[:, i]) ** 2)
    ae_feat_mse = np.mean((data_scaled[:, i] - ae_reconst[:, i]) ** 2)
    print(f"  ফিচার {i:>2}: PCA={pca_feat_mse:.6f}, AE={ae_feat_mse:.6f}", 
          end="")
    if ae_feat_mse < pca_feat_mse:
        print(" ✅")
    else:
        print()
```

## ল্যাটেন্ট ফিচার এক্সট্র্যাকশন

```python
# AE-এক্সট্র্যাক্টেড ফিচার
with torch.no_grad():
    ae_features = ae.encode(data_tensor).numpy()

# PCA কম্পোনেন্ট
pca_features = pca_result

print(f"PCA ফিচার: {pca_features.shape}")
print(f"AE ফিচার: {ae_features.shape}")

# ফিচার কোরিলেশন
corr_pca = np.corrcoef(pca_features[:, :10].T)
corr_ae = np.corrcoef(ae_features[:, :10].T)

print(f"\nPCA ফিচার কোরিলেশন (প্রথম ৫):")
print(corr_pca[:5, :5].round(2))
print(f"\nAE ফিচার কোরিলেশন (প্রথম ৫):")
print(corr_ae[:5, :5].round(2))

# AE ফিচার কি ডিকোরিলেটেড?
mean_abs_corr = np.abs(corr_ae[np.triu_indices_from(corr_ae, k=1)]).mean()
print(f"\nAE ফিচারের গড় এবসুলিউট কোরিলেশন: {mean_abs_corr:.4f}")
print(f"(PCA-র মতো অর্থোগোনাল না, তবে তথ্য ধারণ করে)")
```

## ডাউনস্ট্রিম টাস্কে তুলনা

```python
# রিগ্রেশন টাস্ক: ফিচার → টার্গেট প্রেডিকশন
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# টার্গেট (সিন্থেটিক)
target = factors[:, 0] + 0.5 * factors[:, 1] + np.random.randn(n) * 0.1

# ট্রেন/টেস্ট স্প্লিট
split = int(0.8 * n)

# 1. অরিজিনাল ফিচার
X_train, X_test = data_scaled[:split], data_scaled[split:]
y_train, y_test = target[:split], target[split:]
lr_orig = LinearRegression().fit(X_train, y_train)
orig_r2 = r2_score(y_test, lr_orig.predict(X_test))

# 2. PCA ফিচার
pca_train, pca_test = pca_features[:split], pca_features[split:]
lr_pca = LinearRegression().fit(pca_train, y_train)
pca_r2 = r2_score(y_test, lr_pca.predict(pca_test))

# 3. AE ফিচার
ae_train, ae_test = ae_features[:split], ae_features[split:]
lr_ae = LinearRegression().fit(ae_train, y_train)
ae_r2 = r2_score(y_test, lr_ae.predict(ae_test))

print(f"{'ফিচার সেট':<25} {'R² Score':<15} {'প্যারামিটার':<15}")
print("-" * 55)
print(f"{f'অরিজিনাল ({n_features})':<25} {orig_r2:<15.4f} {n_features:<15}")
print(f"{f'PCA ({target_dim})':<25} {pca_r2:<15.4f} {target_dim:<15}")
print(f"{f'AE ({target_dim})':<25} {ae_r2:<15.4f} {target_dim:<15}")
```

## কম্প্রেশন রেশিও বিশ্লেষণ

```python
# বিভিন্ন এনকোডিং ডাইমেনশনের জন্য রিকন্সট্রাকশন এরর
encoding_dims = [2, 4, 8, 16, 24, 32]
results = []

for enc_dim in encoding_dims:
    model = DimReductionAE(n_features, enc_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(40):
        for bx, _ in loader:
            optimizer.zero_grad()
            loss = criterion(model(bx), bx)
            loss.backward()
            optimizer.step()
    
    model.eval()
    with torch.no_grad():
        loss = criterion(model(data_tensor), data_tensor).item()
    
    compression = n_features / enc_dim
    results.append((enc_dim, loss, compression))
    print(f"enc_dim={enc_dim:<3} (compression={compression:.1f}x): MSE={loss:.6f}")

# এলবো প্লট (স্ক্রি প্লট)
print(f"\nএলবো প্লট (প্রতিটি encoding_dim-এর জন্য MSE):")
for enc_dim, loss, comp in results:
    bar = '█' * int((1-loss) * 200)
    print(f"  {enc_dim:>2} ({comp:.1f}x): {bar} {loss:.6f}")

# সিলেক্ট সেরা কমপ্রেশন (এলবো পয়েন্ট)
losses = [r[1] for r in results]
improvements = [abs(losses[i] - losses[i+1]) for i in range(len(losses)-1)]
elbow_idx = np.argmin(improvements)  # সবচেয়ে কম ইমপ্রুভমেন্ট
print(f"\n🎯 এলবো পয়েন্ট: encoding_dim={results[elbow_idx][0]}")
```

## ভিজুয়ালাইজেশন: PCA vs AE 2D

```python
# 2D রিডাকশন
ae_2d = DimReductionAE(n_features, encoding_dim=2)
optimizer = optim.Adam(ae_2d.parameters(), lr=0.001)

for epoch in range(50):
    for bx, _ in loader:
        optimizer.zero_grad()
        loss = criterion(ae_2d(bx), bx)
        loss.backward()
        optimizer.step()

ae_2d.eval()
with torch.no_grad():
    ae_2d_features = ae_2d.encode(data_tensor).numpy()
pca_2d = PCA(n_components=2).fit_transform(data_scaled)

print(f"PCA 2D: {pca_2d[:5]}")
print(f"AE 2D: {ae_2d_features[:5]}")

# স্প্যাটিয়াল ডিস্ট্রিবিউশন
pca_range = pca_2d.max(axis=0) - pca_2d.min(axis=0)
ae_range = ae_2d_features.max(axis=0) - ae_2d_features.min(axis=0)

print(f"\nPCA স্প্যান: [{pca_2d.min(axis=0)[0]:.2f}, {pca_2d.max(axis=0)[0]:.2f}]")
print(f"AE স্প্যান: [{ae_2d_features.min(axis=0)[0]:.2f}, {ae_2d_features.max(axis=0)[0]:.2f}]")
print(f"PCA vs AE রেঞ্জ রেশিও: {pca_range / ae_range}")
```

## কখন AE ব্যবহার করবেন?

### AE ভালো যখন:
1. নন-লিনিয়ার রিলেশনশিপ আছে
2. ফিচারগুলোর মধ্যে জটিল ইন্টারঅ্যাকশন
3. ডেটা জেনারেশন বা ডিনয়েজিংও প্রয়োজন
4. GPU অ্যাক্সেস আছে

### PCA ভালো যখন:
1. দ্রুত এবং ইন্টারপ্রিটেবল প্রয়োজন
2. লিনিয়ার রিলেশনশিপ যথেষ্ট
3. ছোট ডেটাসেট
4. ফিচার ইন্টারপ্রিটেশন প্রয়োজন

```python
print("✅ ডাইমেনশনালিটি রিডাকশন সম্পূর্ণ")
print(f"PCA vs AE: উভয়ের নিজস্ব সুবিধা আছে, টাস্কের উপর নির্ভর করে")
```

## সারাংশ
- অটোএনকোডার নন-লিনিয়ার ডাইমেনশনালিটি রিডাকশন করে
- PCA-র তুলনায় জটিল প্যাটার্ন ক্যাপচার করতে পারে
- কম্প্রেশন রেশিও এনকোডিং ডাইমেনশনের উপর নির্ভর করে
- ডাউনস্ট্রিম টাস্কে (রিগ্রেশন, ক্লাসিফিকেশন) পারফরম্যান্স উন্নত করে
- এলবো পয়েন্ট এনালাইসিস সেরা এনকোডিং ডাইমেনশন নির্ধারণে সাহায্য করে
- ফিন্যান্সে ফ্যাক্টর মডেল, রিস্ক ম্যানেজমেন্ট, পোর্টফোলিও অ্যানালাইসিসে ব্যবহৃত