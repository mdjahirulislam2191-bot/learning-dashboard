# Day 24: প্রিন্সিপাল কম্পোনেন্ট অ্যানালাইসিস (PCA)
## Principal Component Analysis: Dimensionality Reduction

### PCA কী?
PCA একটি আনসুপারভাইজড ডাইমেনশনালিটি রিডাকশন টেকনিক। এটি উচ্চ-মাত্রিক ডেটাকে কম মাত্রায় রূপান্তর করে, যেখানে ডেটার বেশিরভাগ ভ্যারিয়েন্স বা তথ্য ধরে রাখা হয়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA, SparsePCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris, load_digits, fetch_openml, load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
```

### PCA-এর মূল ধারণা
```python
print("=" * 60)
print("PCA-এর মূল ধারণা")
print("=" * 60)

concepts = [
    "1. ভ্যারিয়েন্স ম্যাক্সিমাইজেশন: প্রথম PC সর্বোচ্চ ভ্যারিয়েন্স ধরে",
    "2. অর্থোগোনাল কম্পোনেন্ট: প্রতিটি PC পূর্ববর্তী PC-এর সাথে লম্ব",
    "3. ইজেনভ্যালু ও ইজেনভেক্টর: কোভ্যারিয়েন্স ম্যাট্রিক্স থেকে গণনা",
    "4. ডাইমেনশনালিটি রিডাকশন: কম গুরুত্বপূর্ণ কম্পোনেন্ট বাদ দেওয়া",
    "5. ফিচার ট্রান্সফর্মেশন: আসল ফিচারকে PC-তে রূপান্তর"
]

for c in concepts:
    print(c)

print("\nPCA স্টেপস:")
print("1. ডেটা স্ট্যান্ডার্ডাইজ করা (গড়=0, ভ্যারিয়েন্স=1)")
print("2. কোভ্যারিয়েন্স ম্যাট্রিক্স গণনা")
print("3. ইজেনভ্যালু ও ইজেনভেক্টর বের করা")
print("4. ইজেনভ্যালু অনুসারে সাজানো")
print("5. K সংখ্যক কম্পোনেন্ট নির্বাচন")
print("6. ডেটা ট্রান্সফর্ম করা")
```

### IRIS ডেটাসেটে PCA প্রয়োগ
```python
print("\n=== IRIS ডেটাসেটে PCA ===")

iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print(f"ডেটা আকৃতি: {X.shape}")
print(f"ফিচার: {feature_names}")
print(f"ক্লাস: {target_names}")

# স্কেলিং
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

print(f"\nPCA-র পর আকৃতি: {X_pca.shape}")
print(f"\nপ্রতিটি PC-র ভ্যারিয়েন্স অনুপাত:")
for i, var in enumerate(pca.explained_variance_ratio_, 1):
    print(f"  PC{i}: {var:.4f} ({var*100:.2f}%)")

print(f"\nক্রমবর্ধমান ভ্যারিয়েন্স:")
cum_var = np.cumsum(pca.explained_variance_ratio_)
for i, cv in enumerate(cum_var, 1):
    print(f"  PC1-{i}: {cv:.4f} ({cv*100:.2f}%)")
```

### ভ্যারিয়েন্স ভিজুয়ালাইজেশন
```python
print("\n=== ভ্যারিয়েন্স ভিজুয়ালাইজেশন ===")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scree Plot
components = np.arange(1, len(pca.explained_variance_ratio_) + 1)
axes[0].bar(components, pca.explained_variance_ratio_, alpha=0.7, color='steelblue')
axes[0].plot(components, pca.explained_variance_ratio_, 'ro-', linewidth=2, markersize=8)
axes[0].set_title('Scree Plot - প্রতিটি PC-র ভ্যারিয়েন্স', fontsize=12)
axes[0].set_xlabel('প্রিন্সিপাল কম্পোনেন্ট')
axes[0].set_ylabel('ভ্যারিয়েন্স অনুপাত')
axes[0].grid(True, alpha=0.3)

# Cumulated Variance
axes[1].bar(components, cum_var, alpha=0.7, color='coral')
axes[1].plot(components, cum_var, 'go-', linewidth=2, markersize=8)
axes[1].axhline(y=0.95, color='red', linestyle='--', alpha=0.7, label='95% ভ্যারিয়েন্স')
axes[1].set_title('ক্রমবর্ধমান ভ্যারিয়েন্স', fontsize=12)
axes[1].set_xlabel('প্রিন্সিপাল কম্পোনেন্টের সংখ্যা')
axes[1].set_ylabel('ক্রমবর্ধমান ভ্যারিয়েন্স')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.savefig('pca_variance.png', dpi=100)
plt.show()
```

### 2D ভিজুয়ালাইজেশন
```python
print("\n=== PCA 2D ভিজুয়ালাইজেশন ===")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# প্রথম দুটি PC
colors = ['navy', 'orange', 'green']
for i, name in enumerate(target_names):
    mask = y == i
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors[i], 
                   label=name, s=50, alpha=0.8, edgecolors='white', linewidth=0.5)
axes[0].set_title('PCA: IRIS ডেটার 2D প্রজেকশন', fontsize=12)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% ভ্যারিয়েন্স)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% ভ্যারিয়েন্স)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# PC2 vs PC3
for i, name in enumerate(target_names):
    mask = y == i
    axes[1].scatter(X_pca[mask, 1], X_pca[mask, 2], c=colors[i],
                   label=name, s=50, alpha=0.8, edgecolors='white', linewidth=0.5)
axes[1].set_title('PCA: PC2 vs PC3', fontsize=12)
axes[1].set_xlabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% ভ্যারিয়েন্স)')
axes[1].set_ylabel(f'PC3 ({pca.explained_variance_ratio_[2]*100:.1f}% ভ্যারিয়েন্স)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('pca_iris_2d.png', dpi=100)
plt.show()

print("PC1-এ সর্বোচ্চ ভ্যারিয়েন্স, তাই ডেটা PC1 অক্ষে সবচেয়ে বেশি ছড়িয়ে আছে!")
```

### ফিচার লোডিং অ্যানালাইসিস
```python
print("\n=== ফিচার লোডিং অ্যানালাইসিস ===")

loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(pca.n_components_)],
    index=feature_names
)
print("ফিচার লোডিং (প্রতিটি PC-তে ফিচারের অবদান):")
print(loadings.round(3))

# হিটম্যাপ
plt.figure(figsize=(10, 6))
sns.heatmap(loadings, annot=True, cmap='RdBu', center=0, 
            xticklabels=[f'PC{i+1}' for i in range(pca.n_components_)],
            yticklabels=feature_names)
plt.title('ফিচার লোডিং হিটম্যাপ', fontsize=14)
plt.tight_layout()
plt.savefig('pca_loadings.png', dpi=100)
plt.show()

print("\nলোডিং ব্যাখ্যা:")
print("• পাপড়ির দৈর্ঘ্য ও প্রস্থ PC1-এ বেশি লোডিং (সবচেয়ে গুরুত্বপূর্ণ)")
print("• সিপালের দৈর্ঘ্য PC2-এ বেশি লোডিং")
```

### ডাইমেনশনালিটি রিডাকশন: 4D → 2D
```python
print("\n=== ডাইমেনশনালিটি রিডাকশন: 4D → 2D ===")

pca_2d = PCA(n_components=2)  # 95% ভ্যারিয়েন্স ধরে রাখতে 2 কম্পোনেন্টই যথেষ্ট
X_pca_2d = pca_2d.fit_transform(X_scaled)

print(f"আসল ডেটা: {X.shape[1]} ডাইমেনশন")
print(f"PCA-র পর: {X_pca_2d.shape[1]} ডাইমেনশন")
print(f"ধরে রাখা ভ্যারিয়েন্স: {sum(pca_2d.explained_variance_ratio_)*100:.2f}%")
print(f"তথ্য হারিয়েছে: {(1 - sum(pca_2d.explained_variance_ratio_))*100:.2f}%")

# 2D তে ক্লাসিফিকেশন
X_train, X_test, y_train, y_test = train_test_split(X_pca_2d, y, test_size=0.3, random_state=42)
clf = LogisticRegression(max_iter=200, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"\nশুধু 2D PC ব্যবহার করে Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# আসল 4D ডেটায় ক্লাসিফিকেশন
X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
clf_orig = LogisticRegression(max_iter=200, random_state=42)
clf_orig.fit(X_train_orig, y_train_orig)
y_pred_orig = clf_orig.predict(X_test_orig)

print(f"আসল 4D ডেটায় Accuracy: {accuracy_score(y_test_orig, y_pred_orig):.4f}")
```

### ডিজিট ডেটাসেটে PCA (উচ্চ-মাত্রিক ডেটা)
```python
print("\n=== ডিজিট ডেটাসেটে PCA ===")

digits = load_digits()
X_digits = digits.data
y_digits = digits.target

print(f"ডিজিট ডেটা আকৃতি: {X_digits.shape}")
print(f"প্রতি ইমেজ: 8×8 = 64 পিক্সেল (64টি ফিচার)")

# স্কেলিং
X_digits_scaled = StandardScaler().fit_transform(X_digits)

# PCA
pca_digits = PCA()
X_digits_pca = pca_digits.fit_transform(X_digits_scaled)

# কতগুলো কম্পোনেন্ট 95% ভ্যারিয়েন্স ধরে রাখে
cum_var_digits = np.cumsum(pca_digits.explained_variance_ratio_)
n_components_95 = np.argmax(cum_var_digits >= 0.95) + 1

print(f"\n95% ভ্যারিয়েন্সের জন্য প্রয়োজনীয় কম্পোনেন্ট: {n_components_95}")
print(f"ডাইমেনশনালিটি রিডাকশন: 64 → {n_components_95}")
print(f"কম্প্রেশন রেশিও: {64/n_components_95:.1f}x")

# ভ্যারিয়েন্স গ্রাফ
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.bar(range(1, 21), pca_digits.explained_variance_ratio_[:20], alpha=0.7)
plt.axvline(x=n_components_95, color='red', linestyle='--', label=f'{n_components_95} কম্পোনেন্ট')
plt.title('প্রথম 20 PC-র ভ্যারিয়েন্স')
plt.xlabel('PC')
plt.ylabel('ভ্যারিয়েন্স অনুপাত')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(cum_var_digits[:40], 'b-', linewidth=2)
plt.axhline(y=0.95, color='red', linestyle='--', label='95% ভ্যারিয়েন্স')
plt.axvline(x=n_components_95, color='green', linestyle='--', label=f'{n_components_95} PC')
plt.title('ক্রমবর্ধমান ভ্যারিয়েন্স')
plt.xlabel('PC সংখ্যা')
plt.ylabel('ক্রমবর্ধমান ভ্যারিয়েন্স')
plt.legend()

plt.tight_layout()
plt.savefig('pca_digits.png', dpi=100)
plt.show()
```

### PCA দিয়ে ডেটা রিকন্সট্রাকশন
```python
print("\n=== PCA দিয়ে ডেটা রিকন্সট্রাকশন ===")

# বিভিন্ন সংখ্যক কম্পোনেন্ট দিয়ে রিকন্সট্রাকশন
n_components_list = [2, 10, 20, 40]
fig, axes = plt.subplots(1, 5, figsize=(20, 4))

# আসল ইমেজ
axes[0].imshow(digits.images[0], cmap='gray')
axes[0].set_title('আসল ইমেজ\n(64 ফিচার)', fontsize=10)
axes[0].axis('off')

for idx, n_comp in enumerate(n_components_list):
    pca_n = PCA(n_components=n_comp)
    X_transformed = pca_n.fit_transform(X_digits_scaled)
    X_reconstructed = pca_n.inverse_transform(X_transformed)
    
    axes[idx + 1].imshow(X_reconstructed[0].reshape(8, 8), cmap='gray')
    axes[idx + 1].set_title(f'{n_comp} PC\n({pca_n.explained_variance_ratio_.sum()*100:.1f}% ভ্যারি.)', fontsize=10)
    axes[idx + 1].axis('off')

plt.suptitle('PCA রিকন্সট্রাকশন: কম্পোনেন্ট সংখ্যার প্রভাব', fontsize=14)
plt.tight_layout()
plt.savefig('pca_reconstruction.png', dpi=100)
plt.show()

print("কম্পোনেন্ট সংখ্যা বাড়ালে রিকন্সট্রাকশন কোয়ালিটি বাড়ে, কিন্তু ডাইমেনশনালিটিও বাড়ে")
```

### PCA + ক্লাসিফিকেশন (ওয়াইন ডেটাসেট)
```python
print("\n=== PCA + ক্লাসিফিকেশন (ওয়াইন ডেটাসেট) ===")

wine = load_wine()
X_wine = wine.data
y_wine = wine.target

print(f"ওয়াইন ডেটা: {X_wine.shape[1]} ফিচার, {len(np.unique(y_wine))} ক্লাস")

# স্কেলিং
X_wine_scaled = StandardScaler().fit_transform(X_wine)

# Full features
rf_full = RandomForestClassifier(n_estimators=100, random_state=42)
scores_full = cross_val_score(rf_full, X_wine_scaled, y_wine, cv=5)
print(f"\nফুল ফিচার ({X_wine.shape[1]}D):")
print(f"  Accuracy: {scores_full.mean():.4f} (+/- {scores_full.std()*2:.4f})")

# PCA (2 components)
pca_wine = PCA(n_components=2)
X_wine_pca = pca_wine.fit_transform(X_wine_scaled)
rf_pca = RandomForestClassifier(n_estimators=100, random_state=42)
scores_pca = cross_val_score(rf_pca, X_wine_pca, y_wine, cv=5)
print(f"\nPCA (2D):")
print(f"  Accuracy: {scores_pca.mean():.4f} (+/- {scores_pca.std()*2:.4f})")
print(f"  ভ্যারিয়েন্স ধরে রেখেছে: {sum(pca_wine.explained_variance_ratio_)*100:.1f}%")

# PCA (enough for 95%)
n_95 = np.argmax(np.cumsum(PCA().fit(X_wine_scaled).explained_variance_ratio_) >= 0.95) + 1
pca_wine_95 = PCA(n_components=n_95)
X_wine_95 = pca_wine_95.fit_transform(X_wine_scaled)
rf_95 = RandomForestClassifier(n_estimators=100, random_state=42)
scores_95 = cross_val_score(rf_95, X_wine_95, y_wine, cv=5)
print(f"\nPCA ({n_95}D for 95%):")
print(f"  Accuracy: {scores_95.mean():.4f} (+/- {scores_95.std()*2:.4f})")

# 2D ভিজুয়ালাইজেশন
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_wine_pca[:, 0], X_wine_pca[:, 1], c=y_wine, cmap='viridis', 
                     s=60, alpha=0.8, edgecolors='white', linewidth=0.5)
plt.colorbar(scatter)
plt.xlabel(f'PC1 ({pca_wine.explained_variance_ratio_[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({pca_wine.explained_variance_ratio_[1]*100:.1f}%)')
plt.title('PCA: ওয়াইন ডেটার 2D প্রজেকশন', fontsize=14)
plt.grid(True, alpha=0.3)
plt.savefig('pca_wine.png', dpi=100)
plt.show()
```

### PCA-র ব্যবহার ও সীমাবদ্ধতা
```python
print("\n=== PCA-র ব্যবহার ও সীমাবদ্ধতা ===")

print("✅ PCA-র ব্যবহার:")
use_cases = [
    "• ডাইমেনশনালিটি রিডাকশন (কম্পিউটেশনাল কস্ট কমানো)",
    "• নয়েজ রিমুভাল (শেষ PC-গুলো সাধারণত নয়েজ)",
    "• ডেটা ভিজুয়ালাইজেশন (2D/3D তে প্রজেকশন)",
    "• মাল্টিকোলিনিয়ারিটি সমাধান",
    "• ফিচার ইঞ্জিনিয়ারিং (নতুন ফিচার তৈরি)",
    "• ওভারফিটিং কমানো",
    "• ইমেজ কম্প্রেশন"
]
print("\n".join(use_cases))

print("\n⚠️ সীমাবদ্ধতা:")
limitations = [
    "• লিনিয়ার ট্রান্সফর্মেশন - নন-লিনিয়ার রিলেশন ধরতে পারে না",
    "• স্কেলিং অত্যাবশ্যক - স্কেলিং ছাড়া ফলাফল ভুল হবে",
    "• ব্যাখ্যা করা কঠিন (PC-গুলো আসল ফিচার নয়)",
    "• আউটলায়ারের প্রতি সংবেদনশীল",
    "• ভ্যারিয়েন্স সর্বোচ্চ করা মানে ক্লাস সেপারেশন নিশ্চিত নয়",
    "• ক্যাটেগরিক্যাল ডেটার জন্য সরাসরি উপযুক্ত নয়"
]
print("\n".join(limitations))

print("\n=== PCA এর বিকল্প ===")
alternatives = [
    "→ t-SNE: উচ্চ-মাত্রিক ডেটার ভিজুয়ালাইজেশনের জন্য",
    "→ UMAP: t-SNE এর চেয়ে দ্রুততর, ভালো গ্লোবাল স্ট্রাকচার ধরে",
    "→ Kernel PCA: নন-লিনিয়ার ডেটার জন্য",
    "→ Sparse PCA: বেশি ব্যাখ্যাযোগ্য কম্পোনেন্ট চাইলে",
    "→ ICA: ইন্ডিপেন্ডেন্ট কম্পোনেন্ট অ্যানালাইসিস"
]
print("\n".join(alternatives))
```

### Incremental PCA (বড় ডেটার জন্য)
```python
print("\n=== Incremental PCA (বড় ডেটাসেট) ===")

# সিন্থেটিক বড় ডেটাসেট
np.random.seed(42)
X_large = np.random.randn(10000, 500)  # 10K নমুনা, 500 ফিচার

print(f"বড় ডেটা আকৃতি: {X_large.shape}")
print("সব ডেটা মেমোরিতে না রেখে ব্যাচে ব্যাচে PCA করা যায়!")

# Incremental PCA
batch_size = 500
ipca = IncrementalPCA(n_components=50)

# ব্যাচে ফিট
for i in range(0, len(X_large), batch_size):
    batch = X_large[i:i+batch_size]
    ipca.partial_fit(batch)

X_large_pca = ipca.transform(X_large)
print(f"Incremental PCA এর পর আকৃতি: {X_large_pca.shape}")
print(f"ধরে রাখা ভ্যারিয়েন্স: {sum(ipca.explained_variance_ratio_)*100:.2f}%")
print(f"মেমোরি বেঞ্চিফিট: পুরো ডেটা মেমোরিতে না রেখেই PCA করা সম্ভব!")
```

### সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("PCA - সারসংক্ষেপ")
print("=" * 60)

summary = """
## PCA-এর মূল পয়েন্ট

✅ PCA ডেটার ডাইমেনশন কমায়, গুরুত্বপূর্ণ তথ্য ধরে রাখে
✅ ফিচারের মধ্যেকার সম্পর্ক ব্যবহার করে নতুন কম্পোনেন্ট তৈরি করে
✅ ডেটা ভিজুয়ালাইজেশন, কম্প্রেশন, নয়েজ রিমুভালে ব্যবহার
✅ কম্পোনেন্ট সংখ্যা নির্বাচনে Scree Plot ও ক্রমবর্ধমান ভ্যারিয়েন্স ব্যবহার
✅ স্কেলিং অত্যাবশ্যক - StandardScaler ব্যবহার বাধ্যতামূলক
✅ PCA-র আগে ট্রেন/টেস্ট স্প্লিট করা উচিত

## প্র্যাকটিক্যাল টিপস
• 95% ভ্যারিয়েন্স ধরে রাখার জন্য যথেষ্ট কম্পোনেন্ট নিন
• PCA ট্রান্সফর্ম শুধু ট্রেনিং ডেটায় ফিট করুন, টেস্ট ডেটায় transform করুন
• ব্যাখ্যার জন্য ফিচার লোডিং দেখুন
• নন-লিনিয়ার ডেটার জন্য Kernel PCA ব্যবহার করুন
• বড় ডেটার জন্য Incremental PCA ব্যবহার করুন
"""
print(summary)
```