# Day 22: হায়ারারকিক্যাল ক্লাস্টারিং
## Hierarchical Clustering

### হায়ারারকিক্যাল ক্লাস্টারিং কি?
একটি ক্লাস্টারিং কৌশল যা ডেটার মধ্যে একটি ট্রি-মত সম্পর্ক (dendrogram) তৈরি করে। দুটি পদ্ধতি: Agglomerative (bottom-up) এবং Divisive (top-down).

### ফাইন্যান্স উদাহরণ: স্টক ক্লাস্টারিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, cophenet
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# বিভিন্ন স্টক সেক্টরের রিটার্ন ডেটা
np.random.seed(42)
n_days = 252
n_stocks = 20

stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',  # Tech
    'JPM', 'GS', 'BAC', 'WFC', 'MS',            # Banking
    'JNJ', 'PFE', 'MRK', 'ABBV', 'UNH',         # Healthcare  
    'XOM', 'CVX', 'COP', 'SLB', 'EOG'            # Energy
]

stock_returns = pd.DataFrame(index=range(n_days), columns=stocks)

# সেক্টর-ভিত্তিক রিটার্ন
sectors = {
    'tech': stocks[:5], 'banking': stocks[5:10], 
    'healthcare': stocks[10:15], 'energy': stocks[15:20]
}

for sector, sector_stocks in sectors.items():
    sector_return = np.random.randn(n_days) * 0.02 + 0.001
    for stock in sector_stocks:
        stock_returns[stock] = sector_return + np.random.randn(n_days) * 0.005

print("📊 Stock Returns Data:")
print(stock_returns.head())
```

### Agglomerative Clustering
```python
# Correlation-based distance (স্টক ক্লাস্টারিং-এর জন্য ভালো)
corr = stock_returns.corr()
distance_matrix = 1 - corr

# Hierarchical clustering using average linkage
Z = linkage(distance_matrix, method='average')

print("Linkage Matrix Shape:", Z.shape)
print("\n🔄 Clustering Steps:")
print(Z[:5])
```

### Dendrogram
```python
plt.figure(figsize=(14, 7))
dendrogram(Z, labels=stocks, leaf_rotation=90, leaf_font_size=10)
plt.title('Stock Dendrogram - হায়ারারকিক্যাল ক্লাস্টারিং')
plt.xlabel('Stocks')
plt.ylabel('Distance')
plt.axhline(y=0.3, color='r', linestyle='--', label='Cut at 0.3')
plt.legend()
plt.show()
```

### Cluster Assignments
```python
# বিভিন্ন কাট লেভেলে ক্লাস্টার
for k in [2, 3, 4, 5]:
    clusters = fcluster(Z, k, criterion='maxclust')
    cluster_df = pd.DataFrame({'stock': stocks, 'cluster': clusters})
    print(f"\n📋 K={k} Clusters:")
    for c in sorted(cluster_df['cluster'].unique()):
        cluster_stocks = cluster_df[cluster_df['cluster'] == c]['stock'].tolist()
        print(f"  Cluster {c}: {', '.join(cluster_stocks)}")
```

### Linkage Methods তুলনা
```python
methods = ['single', 'complete', 'average', 'ward']

plt.figure(figsize=(16, 10))
for i, method in enumerate(methods):
    plt.subplot(2, 2, i+1)
    Z_method = linkage(distance_matrix, method=method)
    dendrogram(Z_method, labels=stocks, leaf_rotation=90, leaf_font_size=8)
    plt.title(f'{method.capitalize()} Linkage')
plt.tight_layout()
plt.show()

print("📊 Linkage Methods Comparison:")
print("Single → চেইনিং প্রবণ (long clusters)")
print("Complete → কমপ্যাক্ট ক্লাস্টার")
print("Average → ব্যালান্সড (middle ground)")
print("Ward → Variance মিনিমাইজ করে (স্পেশাল)")
```

### Scikit-learn Agglomerative
```python
agg = AgglomerativeClustering(n_clusters=4, linkage='ward')
labels = agg.fit_predict(distance_matrix)

cluster_results = pd.DataFrame({'stock': stocks, 'cluster': labels})
print("\n🏆 Final 4 Clusters:")
for c in sorted(cluster_results['cluster'].unique()):
    stocks_in_cluster = cluster_results[cluster_results['cluster'] == c]['stock'].tolist()
    print(f"  Cluster {c}: {', '.join(stocks_in_cluster)}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- K-ভ্যালু আগে না জানলেও চলে (dendrogram)
- Dendrogram দিয়ে ভিজুয়ালাইজেশন
- Number of clusters flexible
- Non-spherical clusters পায়

❌ Disadvantages:
- O(n³) complexity (বড় ডেটায় ধীর)
- Memory intensive (distance matrix)
- Once merged, cannot undo
- Outliers-এ প্রভাবিত
- Different linkage methods → different results

💡 ফাইন্যান্সে ব্যবহার:
├── স্টক ক্লাস্টারিং (portfolio construction)
├── গ্রাহক সেগমেন্টেশন
├── Asset correlation analysis
└── Market regime identification
""")
```

### সারসংক্ষেপ
হায়ারারকিক্যাল ক্লাস্টারিং ডেটার অন্তর্নিহিত কাঠামো বোঝার জন্য শক্তিশালী টুল। Dendrogram ক্লাস্টার সংখ্যা নির্বাচনে সাহায্য করে। ফাইন্যান্সে স্টক ক্লাস্টারিং এবং পোর্টফোলিও ডাইভার্সিফিকেশনে ব্যবহৃত হয়।