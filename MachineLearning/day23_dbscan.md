# Day 23: DBSCAN
## DBSCAN - Density-Based Spatial Clustering

### DBSCAN কি?
DBSCAN একটি density-based ক্লাস্টারিং অ্যালগরিদম যা ক্লাস্টারগুলোকে উচ্চ-ঘনত্বের এলাকা হিসেবে চিহ্নিত করে। Outliers (noise) আলাদাভাবে সনাক্ত করে।

**প্যারামিটার:**
- **eps (ε)**: পয়েন্টের আশেপাশের রেডিয়াস
- **min_samples**: কোর পয়েন্ট হতে ন্যূনতম পয়েন্ট সংখ্যা

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
import seaborn as sns

# ফাইন্যান্সিয়াল ট্রানজ্যাকশন ডেটা
np.random.seed(42)
n_normal = 400
n_anomaly = 20

# Normal transactions
normal = pd.DataFrame({
    'amount': np.random.normal(500, 200, n_normal),
    'frequency': np.random.normal(10, 5, n_normal),
    'location_change': np.random.normal(0, 1, n_normal),
    'time_anomaly': np.random.normal(0, 1, n_normal)
})

# Anomalous transactions (ফ্রড)
anomaly = pd.DataFrame({
    'amount': np.random.normal(3000, 1000, n_anomaly),
    'frequency': np.random.normal(50, 20, n_anomaly),
    'location_change': np.random.normal(5, 2, n_anomaly),
    'time_anomaly': np.random.normal(3, 2, n_anomaly)
})

data = pd.concat([normal, anomaly], ignore_index=True)
true_labels = np.array([0]*n_normal + [1]*n_anomaly)  # 1=anomaly

print(f"Normal: {n_normal}, Fraud: {n_anomaly}")
print(f"Total: {len(data)}")

# স্কেলিং
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)
```

### Optimal eps Finding (k-distance গ্রাফ)
```python
# k-distance গ্রাফ
neighbors = NearestNeighbors(n_neighbors=5)
neighbors_fit = neighbors.fit(data_scaled)
distances, indices = neighbors_fit.kneighbors(data_scaled)
distances = np.sort(distances[:, -1])

plt.figure(figsize=(10, 5))
plt.plot(distances)
plt.xlabel('Data Points (sorted)')
plt.ylabel('5th Nearest Neighbor Distance')
plt.title('K-Distance Graph - Optimal eps')
plt.axhline(y=0.5, color='r', linestyle='--', label='eps=0.5')
plt.axhline(y=0.8, color='g', linestyle='--', label='eps=0.8')
plt.axhline(y=1.0, color='orange', linestyle='--', label='eps=1.0')
plt.legend()
plt.grid(True)
plt.show()

# Recommended eps = elbow point
print("📌 Elbow point ~ distance where sharp increase begins")
```

### DBSCAN বিভিন্ন প্যারামিটার নিয়ে
```python
def run_dbscan(data, eps, min_samples):
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(data)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    return labels, n_clusters, n_noise

print("\n📊 DBSCAN বিভিন্ন প্যারামিটার:")
for eps in [0.3, 0.5, 0.8, 1.0, 1.5]:
    for min_samp in [3, 5, 10]:
        labels, n_clusters, n_noise = run_dbscan(data_scaled, eps, min_samp)
        if n_clusters > 0:
            sil = silhouette_score(data_scaled[labels != -1], 
                                   labels[labels != -1])
        else:
            sil = 0
        print(f"eps={eps:.1f}, min_samples={min_samp:2d}: "
              f"clusters={n_clusters}, noise={n_noise}, "
              f"silhouette={sil:.4f}")
```

### Best Model
```python
best_db = DBSCAN(eps=0.8, min_samples=5)
best_labels = best_db.fit_predict(data_scaled)

data['cluster'] = best_labels
data['is_anomaly'] = (best_labels == -1)

print(f"\n🏆 Best DBSCAN Result:")
print(f"Clusters found: {len(set(best_labels)) - (1 if -1 in best_labels else 0)}")
print(f"Noise points (fraud detected): {sum(best_labels == -1)}")
print(f"Actual fraud: {sum(true_labels)}")
print(f"Correctly identified: {sum((best_labels == -1) & (true_labels == 1))}")

# ক্লাস্টার প্রোফাইল
print("\n📋 Cluster Profiles:")
for cluster_id in sorted(set(best_labels)):
    cluster_data = data[data['cluster'] == cluster_id]
    name = "Fraud" if cluster_id == -1 else f"Cluster {cluster_id}"
    print(f"\n{name} (n={len(cluster_data)}):")
    for col in ['amount', 'frequency', 'location_change']:
        print(f"  {col}: mean={cluster_data[col].mean():.1f}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- K-ভ্যালু জানার প্রয়োজন নেই
- Arbitrary shaped clusters
- Outliers automatic detection
- Robust to outliers
- Density-based (not distance-based)

❌ Disadvantages:
- Varying density → problems
- High dimensions → curse of dimensionality
- eps + min_samples টিউনিং challenging
- Not deterministic (border points)
- Large datasets-এ memory intensive

💡 Finance Applications:
├── ফ্রড ডিটেকশন (উচ্চ মানের)
├── Market anomaly detection
├── ট্রেডিং প্যাটার্ন রিকগনিশন
├── গ্রাহক অস্বাভাবিক আচরণ শনাক্তকরণ
└── Risk management
""")
```

### সারসংক্ষেপ
DBSCAN density-based ক্লাস্টারিং যা arbitrary shapes এবং outliers হ্যান্ডেল করতে পারে। ফাইন্যান্সে ফ্রড ডিটেকশন এবং anomaly detection-এর জন্য অত্যন্ত কার্যকর। eps এবং min_samples সঠিকভাবে টিউন করা গুরুত্বপূর্ণ।