# Day 24: PCA (Principal Component Analysis)
## প্রিন্সিপাল কম্পোনেন্ট অ্যানালাইসিস

### PCA কি?
PCA একটি dimensionality reduction কৌশল যা অনেক ফিচারকে কম সংখ্যক "principal components"-এ রূপান্তর করে, যেখানে সর্বোচ্চ variance ধরে রাখা হয়।

### ফাইন্যান্স উদাহরণ: পোর্টফোলিও রিস্ক অ্যানালাইসিস
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# মাল্টিপল স্টক রিটার্ন ডেটা
np.random.seed(42)
n_days = 500
n_stocks = 20

stocks = [f'Stock_{i}' for i in range(n_stocks)]

# ফ্যাক্টর মডেল: 3টি সাধারণ ফ্যাক্টর
market_factor = np.random.randn(n_days) * 0.5
sector_factor = np.random.randn(n_days) * 0.3
momentum_factor = np.random.randn(n_days) * 0.2

returns = pd.DataFrame(index=range(n_days), columns=stocks)
for i, stock in enumerate(stocks):
    # প্রতিটি স্টকে তিন ফ্যাক্টরের কম্বিনেশন
    returns[stock] = (market_factor * 0.6 + 
                      sector_factor * (0.3 if i < 10 else 0.1) +
                      momentum_factor * (0.2 if i % 2 == 0 else 0.1) +
                      np.random.randn(n_days) * 0.2)

print("📊 Stock Returns Shape:", returns.shape)
print("Correlation Matrix Heatmap (first 5 stocks):")
print(returns.iloc[:, :5].corr().round(2))
```

### PCA Implementation
```python
# স্কেলিং
scaler = StandardScaler()
returns_scaled = scaler.fit_transform(returns)

# PCA
pca = PCA()
pca_result = pca.fit_transform(returns_scaled)

# Explained Variance
explained_var = pca.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

print("\n📊 Explained Variance by Component:")
for i, (ev, cv) in enumerate(zip(explained_var[:10], cumulative_var[:10])):
    print(f"PC{i+1:2d}: {ev:.4f} ({cv:.4f} cumulative)")
```

### Scree Plot (কম্পোনেন্ট নির্বাচন)
```python
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.bar(range(1, len(explained_var[:10])+1), explained_var[:10])
plt.plot(range(1, len(explained_var[:10])+1), cumulative_var[:10], 'ro-')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot')
plt.axhline(y=0.1, color='gray', linestyle='--', alpha=0.5)

plt.subplot(1, 2, 2)
plt.plot(range(1, len(explained_var)+1), cumulative_var, 'bo-')
plt.axhline(y=0.8, color='r', linestyle='--', label='80% Variance')
plt.axhline(y=0.9, color='g', linestyle='--', label='90% Variance')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Components Needed')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

n_components_80 = np.argmax(cumulative_var >= 0.8) + 1
n_components_90 = np.argmax(cumulative_var >= 0.9) + 1
print(f"\n🎯 Components for 80% variance: {n_components_80}")
print(f"Components for 90% variance: {n_components_90}")
```

### PCA Components Interpretation
```python
# কম্পোনেন্ট লোডিংস
components_df = pd.DataFrame(
    pca.components_.T,
    index=stocks,
    columns=[f'PC{i+1}' for i in range(n_stocks)]
)

print("\n📋 Top stocks in each component:")
for i in range(3):
    top_positive = components_df[f'PC{i+1}'].nlargest(3)
    top_negative = components_df[f'PC{i+1}'].nsmallest(3)
    print(f"\nPC{i+1}:")
    print(f"  Positive: {', '.join(top_positive.index)}")
    print(f"  Negative: {', '.join(top_negative.index)}")
```

### PCA for Visualization
```python
# 2D ভিজুয়ালাইজেশন
pca_2d = PCA(n_components=2)
returns_2d = pca_2d.fit_transform(returns_scaled)

plt.figure(figsize=(10, 8))
plt.scatter(returns_2d[:, 0], returns_2d[:, 1], alpha=0.6)
plt.xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.1%})')
plt.title('PCA Visualization - স্টক রিটার্নস')
plt.grid(True)
plt.show()

print(f"\n2D PCA captures {pca_2d.explained_variance_ratio_.sum():.1%} of variance")
```

### PCA for Noise Reduction
```python
# শুধু প্রথম 5টি কম্পোনেন্ট ব্যবহার
pca_denoise = PCA(n_components=5)
returns_reduced = pca_denoise.fit_transform(returns_scaled)
returns_denoised = pca_denoise.inverse_transform(returns_reduced)

# Original vs Denoised তুলনা
print("\n🔊 Noise Reduction Example:")
print(f"Original shape: {returns_scaled.shape}")
print(f"Reduced shape: {returns_reduced.shape}")
print(f"Variance preserved: {pca_denoise.explained_variance_ratio_.sum():.2%}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- Dimensionality reduction
- Noise reduction
- Visualization (2D/3D)
- Multicollinearity সমাধান
- Faster training

❌ Disadvantages:
- Interpretability হারায়
- Linear assumption
- Variance-based (label importance নয়)
- Scaling-sensitive
- Outlier-sensitive

💡 Finance Applications:
├── পোর্টফোলিও রিস্ক ফ্যাক্টর অ্যানালাইসিস
├── Asset correlation structure
├── Market regime detection
├── Feature engineering (PCs as features)
└── ডেটা ভিজুয়ালাইজেশন
""")
```

### সারসংক্ষেপ
PCA ডেটাকে কম মাত্রায় রূপান্তর করে variance ধরে রাখে। ফাইন্যান্সে risk factor analysis, portfolio management, এবং visualization-এর জন্য ব্যাপকভাবে ব্যবহৃত হয়। Elbow plot-এ 80-90% variance ধরে রাখা সাধারণত যথেষ্ট।