# Day 25: t-SNE
## t-SNE (t-distributed Stochastic Neighbor Embedding)

### t-SNE কি?
t-SNE একটি non-linear dimensionality reduction কৌশল যা হাই-ডাইমেনশনাল ডেটাকে 2D বা 3D-তে ভিজুয়ালাইজ করার জন্য ডিজাইন করা হয়েছে। এটি স্থানীয় কাঠামো সংরক্ষণ করে।

### PCA vs t-SNE
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# ফাইন্যান্সিয়াল ডেটা
np.random.seed(42)
n = 500

# চারটি ভিন্ন ক্লাস তৈরি (বিভিন্ন সেক্টর)
n_per_class = n // 4
classes = ['Tech', 'Banking', 'Healthcare', 'Energy']

data_list = []
for i, cls in enumerate(classes):
    center = np.random.randn(20) * i  # বিভিন্ন সেন্টার
    cls_data = np.random.randn(n_per_class, 20) + center
    df = pd.DataFrame(cls_data, columns=[f'feat_{j}' for j in range(20)])
    df['class'] = cls
    data_list.append(df)

data = pd.concat(data_list, ignore_index=True)
X = data.drop('class', axis=1)
y = data['class']

# স্কেলিং
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Data shape: {X_scaled.shape}")
print(f"Classes: {data['class'].value_counts().to_dict()}")
```

### PCA (2D) ভিজুয়ালাইজেশন
```python
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for cls in classes:
    mask = y == cls
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], label=cls, alpha=0.6, s=30)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title('PCA Visualization')
plt.legend()

plt.subplot(1, 2, 2)
pca_20 = PCA(n_components=20)
pca_20.fit(X_scaled)
cum_var = np.cumsum(pca_20.explained_variance_ratio_)
plt.plot(range(1, 21), cum_var, 'bo-')
plt.axhline(y=0.8, color='r', linestyle='--')
plt.xlabel('Components')
plt.ylabel('Cumulative Variance')
plt.title('PCA Variance Explained')
plt.grid(True)

plt.tight_layout()
plt.show()
```

### t-SNE ভিজুয়ালাইজেশন
```python
print("\n🔄 Computing t-SNE...")
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for cls in classes:
    mask = y == cls
    plt.scatter(X_tsne[mask, 0], X_tsne[mask, 1], label=cls, alpha=0.7, s=30)
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.title('t-SNE Visualization')
plt.legend()
plt.grid(True, alpha=0.3)

# PCA side by side
plt.subplot(1, 2, 2)
for cls in classes:
    mask = y == cls
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], label=cls, alpha=0.6, s=30)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Visualization (same data)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("🎯 t-SNE-এ ক্লাসগুলোর বিচ্ছেদ PCA-র চেয়ে ভালো!")
```

### Perplexity টিউনিং
```python
perplexities = [5, 10, 30, 50, 100]

plt.figure(figsize=(15, 3))
for i, perp in enumerate(perplexities):
    tsne_perp = TSNE(n_components=2, perplexity=perp, random_state=42)
    X_tsne_perp = tsne_perp.fit_transform(X_scaled)
    
    plt.subplot(1, len(perplexities), i+1)
    for cls in classes:
        mask = y == cls
        plt.scatter(X_tsne_perp[mask, 0], X_tsne_perp[mask, 1], 
                   label=cls, alpha=0.7, s=15)
    plt.title(f'Perplexity={perp}')
    plt.xticks([])
    plt.yticks([])
    if i == 0:
        plt.legend()

plt.tight_layout()
plt.show()

print("""
📌 Perplexity:
- ছোট (5-10): Local structure emphasized
- মিডিয়াম (30-50): Balance (recommended)
- বড় (50-100): Global structure emphasized
""")
```

### n_iter প্রভাব
```python
iterations = [250, 500, 1000, 2000]

plt.figure(figsize=(15, 3))
for i, n_iter in enumerate(iterations):
    tsne_iter = TSNE(n_components=2, n_iter=n_iter, random_state=42, verbose=0)
    X_tsne_iter = tsne_iter.fit_transform(X_scaled)
    
    plt.subplot(1, len(iterations), i+1)
    for cls in classes:
        mask = y == cls
        plt.scatter(X_tsne_iter[mask, 0], X_tsne_iter[mask, 1], 
                   label=cls, alpha=0.7, s=15)
    plt.title(f'n_iter={n_iter}')
    plt.xticks([])
    plt.yticks([])

plt.tight_layout()
plt.show()
```

### PCA vs t-SNE Comparison
```python
print("""
📊 PCA vs t-SNE:

PCA:
├── Linear transformation
├── Global structure preserves
├── Deterministic (same result every time)
├── Can be used for preprocessing
├── Faster
└── Interpretable components

t-SNE:
├── Non-linear transformation
├── Local structure preserves
├── Non-deterministic (different each run)
├── Visualization only (can't transform new data)
├── Slower (O(n²))
└── Hard to interpret axes

💡 ফাইন্যান্সে t-SNE ব্যবহার:
├── Market regime visualization
├── গ্রাহক সেগমেন্টেশন ভিজুয়ালাইজেশন
├── Anomaly detection exploration
├── পোর্টফোলিও ক্লাস্টারিং ভিজুয়ালাইজেশন
└── ফ্রড প্যাটার্ন ডিস্কভারি
""")
```

### সারসংক্ষেপ
t-SNE হাই-ডাইমেনশনাল ডেটার non-linear ভিজুয়ালাইজেশনের জন্য সেরা টুল। PCA global variance ধরে রাখে, t-SNE local patterns ভালোভাবে দেখায়। Perplexity একটি গুরুত্বপূর্ণ প্যারামিটার যা ক্লাস্টার সাইজ নিয়ন্ত্রণ করে।