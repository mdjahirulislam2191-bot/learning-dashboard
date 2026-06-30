# Day 23: কে-মিন্স ক্লাস্টারিং (K-Means Clustering)
## K-Means Clustering: An Unsupervised Learning Algorithm

### ক্লাস্টারিং কী?
ক্লাস্টারিং হলো আনসুপারভাইজড লার্নিং টেকনিক, যেখানে ডেটাকে একই রকম বৈশিষ্ট্যের ভিত্তিতে বিভিন্ন গ্রুপ বা ক্লাস্টারে ভাগ করা হয়। K-Means সবচেয়ে জনপ্রিয় ক্লাস্টারিং অ্যালগরিদম।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.datasets import make_blobs, make_moons, load_digits
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
```

### K-Means অ্যালগরিদমের ধাপসমূহ
```python
print("=" * 60)
print("K-Means অ্যালগরিদমের ধাপসমূহ")
print("=" * 60)

steps = [
    "1. K সংখ্যক ক্লাস্টার নির্ধারণ করা",
    "2. প্রতিটি ক্লাস্টারের জন্য র‍্যান্ডম সেন্ট্রয়েড নির্বাচন",
    "3. প্রতিটি পয়েন্টকে নিকটতম সেন্ট্রয়েডে অ্যাসাইন করা",
    "4. প্রতিটি ক্লাস্টারের গড় নিয়ে নতুন সেন্ট্রয়েড নির্ধারণ",
    "5. কনভার্জেন্স না হওয়া পর্যন্ত ৩-৪ ধাপ পুনরাবৃত্তি"
]

for s in steps:
    print(s)

print("\nকনভার্জেন্স শর্ত: সেন্ট্রয়েডের অবস্থান আর পরিবর্তন না হওয়া")
```

### সিন্থেটিক ডেটা তৈরি ও কে-মিন্স প্রয়োগ
```python
print("\n=== সিন্থেটিক ডেটা তৈরি ===")

# বিভিন্ন ধরনের ডেটাসেট তৈরি
n_samples = 1000
centers = 4
cluster_std = 1.5

X_blob, y_blob = make_blobs(n_samples=n_samples, centers=centers, 
                            cluster_std=cluster_std, random_state=42)

print(f"ডেটা আকৃতি: {X_blob.shape}")
print(f"প্রকৃত ক্লাস্টার সংখ্যা: {len(np.unique(y_blob))}")

# মুন ডেটাসেট (অ-রৈখিক)
X_moon, y_moon = make_moons(n_samples=n_samples, noise=0.08, random_state=42)

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(X_blob[:, 0], X_blob[:, 1], c=y_blob, cmap='viridis', s=30, alpha=0.7)
axes[0].set_title('ব্লব ডেটাসেট (ভালো ক্লাস্টারিং এর জন্য উপযোগী)', fontsize=12)
axes[0].set_xlabel('ফিচার ১')
axes[0].set_ylabel('ফিচার ২')

axes[1].scatter(X_moon[:, 0], X_moon[:, 1], c=y_moon, cmap='viridis', s=30, alpha=0.7)
axes[1].set_title('মুন ডেটাসেট (K-Means এর জন্য চ্যালেঞ্জিং)', fontsize=12)
axes[1].set_xlabel('ফিচার ১')
axes[1].set_ylabel('ফিচার ২')

plt.tight_layout()
plt.savefig('kmeans_datasets.png', dpi=100)
plt.show()
```

### K-Means মডেল ট্রেনিং
```python
print("\n=== K-Means মডেল ট্রেনিং ===")

# ব্লব ডেটাসেটে K-Means
k = 4
kmeans_blob = KMeans(n_clusters=k, init='k-means++', n_init=10, 
                     max_iter=300, random_state=42)
y_blob_pred = kmeans_blob.fit_predict(X_blob)

# মুন ডেটাসেটে K-Means (এখানে কাজ করবে না ভালোভাবে)
kmeans_moon = KMeans(n_clusters=2, init='k-means++', n_init=10, 
                     max_iter=300, random_state=42)
y_moon_pred = kmeans_moon.fit_predict(X_moon)

print("ব্লব ডেটা: ক্লাস্টারিং সম্পন্ন")
print(f"ইনারশিয়া (Inertia): {kmeans_blob.inertia_:.2f}")
print(f"পুনরাবৃত্তি (Iterations): {kmeans_blob.n_iter_}")
print(f"\nমুন ডেটা: ক্লাস্টারিং সম্পন্ন")
print(f"ইনারশিয়া: {kmeans_moon.inertia_:.2f}")

# ফলাফল ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(X_blob[:, 0], X_blob[:, 1], c=y_blob_pred, cmap='viridis', s=30, alpha=0.7)
axes[0].scatter(kmeans_blob.cluster_centers_[:, 0], kmeans_blob.cluster_centers_[:, 1],
                c='red', marker='X', s=200, linewidths=2, edgecolors='white', label='সেন্ট্রয়েড')
axes[0].set_title('K-Means → ব্লব ডেটা', fontsize=12)
axes[0].legend()

axes[1].scatter(X_moon[:, 0], X_moon[:, 1], c=y_moon_pred, cmap='viridis', s=30, alpha=0.7)
axes[1].scatter(kmeans_moon.cluster_centers_[:, 0], kmeans_moon.cluster_centers_[:, 1],
                c='red', marker='X', s=200, linewidths=2, edgecolors='white', label='সেন্ট্রয়েড')
axes[1].set_title('K-Means → মুন ডেটা (ভুল ক্লাস্টারিং)', fontsize=12)
axes[1].legend()

plt.tight_layout()
plt.savefig('kmeans_results.png', dpi=100)
plt.show()
```

### সঠিক K মান নির্বাচন: এলবো মেথড
```python
print("\n=== এলবো মেথড (Elbow Method) ===")

inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    kmeans.fit(X_blob)
    inertias.append(kmeans.inertia_)
    sil_score = silhouette_score(X_blob, kmeans.labels_)
    silhouettes.append(sil_score)
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.4f}")

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].axvline(x=4, color='red', linestyle='--', alpha=0.7, label='সঠিক K=4')
axes[0].set_title('এলবো মেথড', fontsize=12)
axes[0].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[0].set_ylabel('ইনারশিয়া')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

axes[1].plot(K_range, silhouettes, 'go-', linewidth=2, markersize=8)
axes[1].axvline(x=4, color='red', linestyle='--', alpha=0.7, label='সঠিক K=4')
axes[1].set_title('সিলুয়েট স্কোর', fontsize=12)
axes[1].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[1].set_ylabel('সিলুয়েট স্কোর')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.savefig('elbow_method.png', dpi=100)
plt.show()

print("\nএলবো মেথড: ইনর্শিয়ার গ্রাফে যেখানে 'হাঁটু' এর মতো বাঁক দেখা যায়, সেটাই সঠিক K")
print("সিলুয়েট স্কোর: ১ এর কাছাকাছি ভাল, -১ এর কাছাকাছি খারাপ")
```

### সিলুয়েট অ্যানালাইসিস
```python
print("\n=== সিলুয়েট অ্যানালাইসিস ===")
from sklearn.metrics import silhouette_samples

kmeans_opt = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
labels = kmeans_opt.fit_predict(X_blob)
silhouette_vals = silhouette_samples(X_blob, labels)

print(f"গড় সিলুয়েট স্কোর: {silhouette_score(X_blob, labels):.4f}")

# ক্লাস্টারভিত্তিক সিলুয়েট
for i in range(4):
    cluster_sil = silhouette_vals[labels == i]
    print(f"ক্লাস্টার {i}: {len(cluster_sil)} পয়েন্ট, গড় সিলুয়েট = {cluster_sil.mean():.4f}")
```

### ডেটা প্রিপ্রসেসিং: স্কেলিং এর গুরুত্ব
```python
print("\n=== স্কেলিং এর গুরুত্ব ===")

# আনস্কেলড ডেটা
np.random.seed(42)
X_unscaled = np.column_stack([
    np.random.normal(50, 10, 300),   # বড় স্কেল
    np.random.normal(5, 1, 300)       # ছোট স্কেল
])

# K-Meins আনস্কেলড ডেটায়
kmeans_unscaled = KMeans(n_clusters=3, random_state=42)
labels_unscaled = kmeans_unscaled.fit_predict(X_unscaled)

# স্কেলিং
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_unscaled)
kmeans_scaled = KMeans(n_clusters=3, random_state=42)
labels_scaled = kmeans_scaled.fit_predict(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(X_unscaled[:, 0], X_unscaled[:, 1], c=labels_unscaled, cmap='viridis', s=30, alpha=0.7)
axes[0].set_title('আনস্কেলড ডেটা - ক্লাস্টারিং', fontsize=12)
axes[0].set_xlabel('ফিচার ১ (বড় স্কেল)')
axes[0].set_ylabel('ফিচার ২ (ছোট স্কেল)')

axes[1].scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels_scaled, cmap='viridis', s=30, alpha=0.7)
axes[1].set_title('স্কেলড ডেটা - সঠিক ক্লাস্টারিং', fontsize=12)
axes[1].set_xlabel('ফিচার ১ (স্ট্যান্ডার্ডাইজড)')
axes[1].set_ylabel('ফিচার ২ (স্ট্যান্ডার্ডাইজড)')

plt.tight_layout()
plt.savefig('scaling_importance.png', dpi=100)
plt.show()

print("K-Means-এ স্কেলিং অত্যন্ত গুরুত্বপ���র্ণ - বড় স্কেলের ফিচার বেশি প্রভাব ফেলে!")
```

### ই-কমার্স কাস্টমার সেগমেন্টেশন (প্র্যাকটিক্যাল উদাহরণ)
```python
print("\n=== ই-কমার্স কাস্টমার সেগমেন্টেশন ===")

np.random.seed(42)
n_customers = 500

customers = pd.DataFrame({
    'customer_id': range(1, n_customers + 1),
    'annual_income': np.random.normal(60000, 20000, n_customers),
    'spending_score': np.random.normal(50, 25, n_customers),
    'age': np.random.randint(18, 70, n_customers),
    'purchase_frequency': np.random.poisson(5, n_customers)
})

# কিছু ক্লাস্টার প্যাটার্ন যোগ করা
# গ্রুপ ১: উচ্চ আয়, উচ্চ ব্যয়
mask1 = (customers['annual_income'] > 75000) & (customers.index < 200)
customers.loc[mask1, 'spending_score'] += np.random.normal(30, 10, mask1.sum())
customers.loc[mask1, 'purchase_frequency'] += np.random.poisson(3, mask1.sum())

# গ্রুপ ২: কম আয়, উচ্চ ব্যয় (তরুণ)
mask2 = (customers['age'] < 30) & (customers['annual_income'] < 50000)
customers.loc[mask2, 'spending_score'] += np.random.normal(20, 8, mask2.sum())

print("কাস্টমার ডেটার প্রথম ৫ সারি:")
print(customers.head())
print(f"\nমোট কাস্টমার: {len(customers)}")

# ফিচার নির্বাচন ও স্কেলিং
features = ['annual_income', 'spending_score', 'age', 'purchase_frequency']
X_customers = customers[features]
scaler = StandardScaler()
X_customers_scaled = scaler.fit_transform(X_customers)

# সঠিক K নির্বাচন
inertias = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_customers_scaled)
    inertias.append(km.inertia_)

# K=4 নিয়ে ক্লাস্টারিং
kmeans_customers = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
customers['segment'] = kmeans_customers.fit_predict(X_customers_scaled)

print("\n=== সেগমেন্ট অ্যানালাইসিস ===")
segment_stats = customers.groupby('segment')[features].mean().round(1)
segment_stats['কাস্টমার_সংখ্যা'] = customers.groupby('segment').size()
print(segment_stats)

# সেগমেন্ট ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

scatter1 = axes[0].scatter(customers['annual_income'], customers['spending_score'],
                          c=customers['segment'], cmap='viridis', s=30, alpha=0.7)
axes[0].set_title('কাস্টমার সেগমেন্ট: আয় vs ব্যয় স্কোর', fontsize=12)
axes[0].set_xlabel('বার্ষিক আয়')
axes[0].set_ylabel('ব্যয় স্কোর')
plt.colorbar(scatter1, ax=axes[0])

scatter2 = axes[1].scatter(customers['age'], customers['spending_score'],
                          c=customers['segment'], cmap='viridis', s=30, alpha=0.7)
axes[1].set_title('কাস্টমার সেগমেন্ট: বয়স vs ব্যয় স্কোর', fontsize=12)
axes[1].set_xlabel('বয়স')
axes[1].set_ylabel('ব্যয় স্কোর')
plt.colorbar(scatter2, ax=axes[1])

plt.tight_layout()
plt.savefig('customer_segmentation.png', dpi=100)
plt.show()

print("\n=== সেগমেন্ট ব্যাখ্যা ===")
for seg in range(4):
    seg_data = customers[customers['segment'] == seg]
    print(f"\nসেগমেন্ট {seg} ({len(seg_data)} কাস্টমার):")
    print(f"  গড় আয়: ${seg_data['annual_income'].mean():.0f}")
    print(f"  গড় ব্যয়: {seg_data['spending_score'].mean():.1f}")
    print(f"  গড় বয়স: {seg_data['age'].mean():.1f}")
```

### K-Means এর সীমাবদ্ধতা
```python
print("\n=== K-Means এর সীমাবদ্ধতা ===")

limitations = [
    "1. K-এর মান আগে থেকে জানতে হয় (হাইপারপ্যারামিটার)",
    "2. আউটলায়ারের প্রতি সংবেদনশীল",
    "3. শুধুমাত্র গোলাকার ক্লাস্টার সনাক্ত করতে পারে",
    "4. ইরেগুলার শেপের ক্লাস্টারের জন্য উপযুক্ত নয়",
    "5. স্থানীয় অপটিমামে আটকে যেতে পারে",
    "6. বড় ডেটাসেটের জন্য ধীর হতে পারে",
    "7. ক্যাটেগরিক্যাল ডেটার জন্য সরাসরি ব্যবহারযোগ্য নয়"
]
print("\n".join(limitations))

print("\n=== সমাধান ===")
solutions = [
    "→ K-means++ initialization: উন্নত সেন্ট্রয়েড সিলেকশন",
    "→ MiniBatch K-means: বড় ডেটার জন্য দ্রুততর ভার্সন",
    "→ DBSCAN: ইরেগুলার শেপের ক্লাস্টারের জন্য",
    "→ Gaussian Mixture Models: সফ্ট ক্লাস্টারিং এর জন্য",
    "→ Hierarchical Clustering: ডেনড্রোগ্রাম ভিত্তিক ক্লাস্টারিং"
]
print("\n".join(solutions))
```

### MiniBatch K-Means (বড় ডেটার জন্য)
```python
print("\n=== MiniBatch K-Means ===")

# বড় ডেটাসেট তৈরি
X_large, _ = make_blobs(n_samples=50000, centers=5, random_state=42)

# স্ট্যান্ডার্ড K-Means
import time
start = time.time()
kmeans_standard = KMeans(n_clusters=5, init='k-means++', n_init=3, random_state=42)
kmeans_standard.fit(X_large)
std_time = time.time() - start

# MiniBatch K-Means
start = time.time()
kmeans_mini = MiniBatchKMeans(n_clusters=5, init='k-means++', n_init=3, 
                              batch_size=100, random_state=42)
kmeans_mini.fit(X_large)
mini_time = time.time() - start

print(f"স্ট্যান্ডার্ড K-Means সময়: {std_time:.2f} সেকেন্ড")
print(f"MiniBatch K-Means সময়: {mini_time:.2f} সেকেন্ড")
print(f"স্পিডআপ: {std_time/mini_time:.1f}x")
print(f"ইনারশিয়া তুলনা:")
print(f"  স্ট্যান্ডার্ড: {kmeans_standard.inertia_:.2f}")
print(f"  MiniBatch: {kmeans_mini.inertia_:.2f}")
```

### সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("K-Means ক্লাস্টারিং - সারসংক্ষেপ")
print("=" * 60)

summary = """
## K-Means-এর মূল পয়েন্ট

✅ K-Means সহজ ও দ্রুত ক্লাস্টারিং অ্যালগরিদম
✅ আনসুপারভাইজড লার্নিং - লেবেল লাগে না
✅ কাস্টমার সেগমেন্টেশন, ইমেজ কম্প্রেশন, মার্কেট অ্যানালাইসিসে ব্যবহার
✅ এলবো মেথড ও সিলুয়েট স্কোর দিয়ে K নির্বাচন
✅ স্কেলিং অত্যন্ত গুরুত্বপূর্ণ
✅ k-means++ initialization ব্যবহার করা উচিত
✅ বড় ডেটার জন্য MiniBatch K-Means ব্যবহার করা ভাল

## কখন K-Means ব্যবহার করবেন?
✓ ক্লাস্টার সংখ্যা আগে থেকে অনুমান করতে পারলে
✓ ডেটা গোলাকার ক্লাস্টারে বিভক্ত হলে
✓ দ্রুত ক্লাস্টারিং প্রয়োজন হলে
✓ বড় ডেটাসেট নিয়ে কাজ করলে

## কখন ব্যবহার করবেন না?
✗ ক্লাস্টার সংখ্যা অনুমান করা কঠিন হলে
✗ ডেটার শেপ জটিল হলে (অ-গোলাকার)
✗ অনেক আউটলায়ার থাকলে
✗ ক্যাটেগরিক্যাল ডেটা হলে
"""
print(summary)
```