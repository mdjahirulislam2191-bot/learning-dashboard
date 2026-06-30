# Day 21: কে-মিনস ক্লাস্টারিং
## K-Means Clustering

### K-Means কি?
K-Means একটি unsupervised learning অ্যালগরিদম যা ডেটাকে K-সংখ্যক ক্লাস্টারে বিভক্ত করে। প্রতিটি ডেটা পয়েন্ট তার নিকটতম ক্লাস্টার সেন্টার (centroid) এর সাথে যুক্ত হয়।

### ফাইন্যান্স উদাহরণ: গ্রাহক সেগমেন্টেশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import seaborn as sns

# ফাইন্যান্সিয়াল কাস্টমার ডেটা
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'annual_income': np.concatenate([
        np.random.normal(30000, 5000, n//3),
        np.random.normal(60000, 8000, n//3),
        np.random.normal(120000, 15000, n//3)
    ]),
    'spending_score': np.concatenate([
        np.random.normal(80, 10, n//3),
        np.random.normal(50, 10, n//3),
        np.random.normal(30, 10, n//3)
    ]),
    'loan_amount': np.concatenate([
        np.random.exponential(5000, n//3),
        np.random.exponential(15000, n//3),
        np.random.exponential(30000, n//3)
    ]),
    'credit_card_usage': np.concatenate([
        np.random.uniform(0.6, 1.0, n//3),
        np.random.uniform(0.3, 0.7, n//3),
        np.random.uniform(0.1, 0.4, n//3)
    ])
})

print("📊 Customer Data:")
print(data.describe())
```

### K-Means মডেল ট্রেইনিং
```python
# স্কেলিং (K-Means-এর জন্য অপরিহার্য)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(data_scaled)

data['segment'] = labels

print("\n📋 সেগমেন্ট সাইজ:")
print(data['segment'].value_counts().sort_index())

# Centroid ইন্টারপ্রেটেশন (আসল স্কেলে)
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
centroid_df = pd.DataFrame(centroids, columns=data.columns[:4])
print("\n📍 Cluster Centers (Original Scale):")
print(centroid_df)
```

### Elbow Method - Best K
```python
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(data_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(data_scaled, labels))

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.axvline(x=3, color='r', linestyle='--', alpha=0.5)

plt.subplot(1, 2, 2)
plt.plot(K_range, silhouettes, 'bo-')
plt.xlabel('K')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score')
plt.axvline(x=3, color='r', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

print(f"\n🎯 Best K (Silhouette): K={K_range[np.argmax(silhouettes)]}, Score={max(silhouettes):.4f}")
```

### Cluster Interpretation
```python
print("\n📊 Segment Profiles:")
for seg in sorted(data['segment'].unique()):
    seg_data = data[data['segment'] == seg]
    print(f"\n   Segment {seg} (n={len(seg_data)}):")
    for col in ['annual_income', 'spending_score', 'loan_amount', 'credit_card_usage']:
        print(f"     {col}: {seg_data[col].mean():.0f}")

# নেমিং সেগমেন্টস
segment_names = {0: 'High Value - Low Risk', 1: 'Medium Value', 2: 'Low Value - High Risk'}
data['segment_name'] = data['segment'].map(segment_names)
print("\n🏷️ Segment Distribution:")
print(data['segment_name'].value_counts())
```

### Evaluation Metrics
```python
print("\n📊 Clustering Metrics:")
print(f"Silhouette Score:        {silhouette_score(data_scaled, labels):.4f}")
print(f"Calinski-Harabasz Score: {calinski_harabasz_score(data_scaled, labels):.4f}")
print(f"Davies-Bouldin Score:    {davies_bouldin_score(data_scaled, labels):.4f}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- Simple and fast
- Large datasets-এ স্কেলেবল
- সহজ interpretability
- Well understood algorithm

❌ Disadvantages:
- K-ভ্যালু আগে নির্ধারণ করতে হয়
- Spherical clusters ধরে নেয়
- Outliers-এ সংবেদনশীল
- Random initialization-এর উপর নির্ভরশীল
- Non-linear data-এ ভালো না

💡 Tips:
├── Scaler ব্যবহার করুন (StandardScaler)
├── n_init=10-25 (বেশি stable)
├── K নির্বাচন: Elbow + Silhouette
├── Outliers আগে হ্যান্ডেল করুন
└── K-means++ initialization (default)
""")
```

### সারসংক্ষেপ
K-Means দ্রুত এবং সহজ ক্লাস্টারিং অ্যালগরিদম। গ্রাহক সেগমেন্টেশন, পোর্টফোলিও ক্লাস্টারিং এবং risk profiling-এ ফাইন্যান্সে ব্যাপকভাবে ব্যবহৃত হয়।