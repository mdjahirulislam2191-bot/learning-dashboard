# Day 28: মিনি প্রজেক্ট — ক্লাস্টারিং অ্যানালাইসিস
## Mini Project: Clustering Analysis — গ্রাহক সেগমেন্টেশন

### প্রজেক্ট ওভারভিউ
এই প্রজেক্টে আমরা একটি ই-কমার্স কোম্পানির গ্রাহক ডেটা নিয়ে ক্লাস্টারিং অ্যানালাইসিস করব। লক্ষ্য: গ্রাহকদের আচরণ, কেনাকাটার প্যাটার্ন ও ডেমোগ্রাফিক বৈশিষ্ট্যের ভিত্তিতে সেগমেন্টে ভাগ করা।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score, calinski_harabasz_score, 
                             davies_bouldin_score, adjusted_rand_score)
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')

np.random.seed(42)
```

### স্টেপ ১: ডেটাসেট তৈরি
```python
print("=" * 60)
print("প্রজেক্ট: গ্রাহক সেগমেন্টেশন")
print("=" * 60)

print("\n=== স্টেপ ১: ই-কমার্স গ্রাহক ডেটা ===")

n_customers = 1000

ecom_customers = pd.DataFrame({
    'গ্রাহক_আইডি': range(1, n_customers + 1),
    'বয়স': np.random.randint(18, 70, n_customers),
    'বার্ষিক_আয়': np.random.lognormal(10.5, 0.6, n_customers).astype(int),
    'মাসিক_ব্যয়': np.random.lognormal(8, 0.7, n_customers).astype(int),
    'সাইট_ভিজিট_প্রতি_সপ্তাহ': np.random.poisson(5, n_customers),
    'পণ্য_দেখা_প্রতি_ভিজিট': np.random.poisson(8, n_customers),
    'কার্ট_যুক্ত_প্রতি_ভিজিট': np.random.poisson(2, n_customers),
    'পূর্ববর্তী_ক্রয়_গড়_মূল্য': np.random.lognormal(9, 0.8, n_customers).astype(int),
    'ক্রয়_ফ্রিকোয়েন্সি_মাসিক': np.random.exponential(2, n_customers).round(1),
    'রিভিউ_লেখা_মোট': np.random.poisson(3, n_customers),
    'কুপন_ব্যবহার_হার': np.random.uniform(0, 1, n_customers).round(2),
})

# ক্লাস্টার প্যাটার্ন সিমুলেশন
# সেগমেন্ট 1: তরুণ, কম আয়, বেশি সময় ব্যয় করে কিন্তু কম কেনে
mask1 = (ecom_customers['বয়স'] < 30) & (ecom_customers['বার্ষিক_আয়'] < 60000)
ecom_customers.loc[mask1, 'সাইট_ভিজিট_প্রতি_সপ্তাহ'] += np.random.poisson(5, mask1.sum())
ecom_customers.loc[mask1, 'মাসিক_ব্যয়'] *= 0.5

# সেগমেন্ট 2: মধ্যবয়সী, বেশি আয়, বেশি কেনে
mask2 = (ecom_customers['বয়ς'] >= 30) & (ecom_customers['বয়স'] < 50) & (ecom_customers['বার্ষিক_আয়'] > 60000)
ecom_customers.loc[mask2, 'ক্রয়_ফ্রিকোয়েন্সি_মাসিক'] *= 2
ecom_customers.loc[mask2, 'মাসিক_ব্যয়'] *= 1.5
ecom_customers.loc[mask2, 'পূর্ববর্তী_ক্রয়_গড়_মূল্য'] *= 1.3

# সেগমেন্ট 3: সিনিয়র, বেশি আয়, কম ভিজিট কিন্তু বেশি কেনে
mask3 = ecom_customers['বয়স'] >= 50
ecom_customers.loc[mask3, 'পূর্ববর্তী_ক্রয়_গড়_মূল্য'] *= 1.5
ecom_customers.loc[mask3, 'কুপন_ব্যবহার_হার'] *= 0.5

ecom_customers['মাসিক_ব্যয়'] = ecom_customers['মাসিক_ব্যয়'].clip(lower=100)
ecom_customers['পূর্ববর্তী_ক্রয়_গড়_মূল্য'] = ecom_customers['পূর্ববর্তী_ক্রয়_গড়_মূল্য'].clip(lower=50)

print(f"মোট গ্রাহক: {len(ecom_customers)}")
print(f"\nপরিসংখ্যান:")
print(ecom_customers.describe())
print("\nপ্রথম ৫ গ্রাহক:")
print(ecom_customers.head())
```

### স্টেপ ২: EDA — গ্রাহক ডেটা বোঝা
```python
print("\n=== স্টেপ ২: গ্রাহক ডেটা ভিজুয়ালাইজেশন ===")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

axes[0, 0].hist(ecom_customers['বয়স'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 0].set_title('বয়স ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 0].set_xlabel('বয়স')
axes[0, 0].set_ylabel('গ্রাহক সংখ্যা')

axes[0, 1].hist(ecom_customers['বার্ষিক_আয়'], bins=40, edgecolor='black', alpha=0.7, color='green')
axes[0, 1].set_title('বার্ষিক আয় ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 1].set_xlabel('বার্ষিক আয় ($)')

axes[0, 2].hist(ecom_customers['মাসিক_ব্যয়'], bins=40, edgecolor='black', alpha=0.7, color='coral')
axes[0, 2].set_title('মাসিক ব্যয় ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 2].set_xlabel('মাসিক ব্যয় ($)')

axes[1, 0].scatter(ecom_customers['বার্ষিক_আয়'], ecom_customers['মাসিক_ব্যয়'], 
                   alpha=0.5, s=20, c='purple')
axes[1, 0].set_title('আয় vs ব্যয়', fontsize=12)
axes[1, 0].set_xlabel('বার্ষিক আয়')
axes[1, 0].set_ylabel('মাসিক ব্যয়')

axes[1, 1].scatter(ecom_customers['বয়স'], ecom_customers['ক্রয়_ফ্রিকোয়েন্সি_মাসিক'],
                   alpha=0.5, s=20, c='orange')
axes[1, 1].set_title('বয়স vs ক্রয় ফ্রিকোয়েন্সি', fontsize=12)
axes[1, 1].set_xlabel('বয়স')
axes[1, 1].set_ylabel('মাসিক ক্রয় ফ্রিকোয়েন্সি')

axes[1, 2].scatter(ecom_customers['সাইট_ভিজিট_প্রতি_সপ্তাহ'], ecom_customers['মাসিক_ব্যয়'],
                   alpha=0.5, s=20, c='teal')
axes[1, 2].set_title('সাইট ভিজিট vs ব্যয়', fontsize=12)
axes[1, 2].set_xlabel('সাপ্তাহিক ভিজিট')
axes[1, 2].set_ylabel('মাসিক ব্যয়')

plt.tight_layout()
plt.savefig('project_clustering_eda.png', dpi=100)
plt.show()
```

### স্টেপ ৩: ডেটা প্রিপ্রসেসিং
```python
print("\n=== স্টেপ ৩: ডেটা প্রিপ্রসেসিং ===")

# ক্লাস্টারিং-এর জন্য ফিচার নির্বাচন
cluster_features = ['বয়স', 'বার্ষিক_আয়', 'মাসিক_ব্যয়', 'সাইট_ভিজিট_প্রতি_সপ্তাহ', 
                    'পণ্য_দেখা_প্রতি_ভিজিট', 'ক্রয়_ফ্রিকোয়েন্সি_মাসিক', 
                    'পূর্ববর্তী_ক্রয়_গড়_মূল্য', 'কুপন_ব্যবহার_হার']

print("ক্লাস্টারিং ফিচার:")
for f in cluster_features:
    print(f"  • {f}")

X = ecom_customers[cluster_features].copy()

# স্কেলিং
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA রিডাকশন (ভিজুয়ালাইজেশনের জন্য)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"\nPCA ভ্যারিয়েন্স ধরে রেখেছে: {pca.explained_variance_ratio_.sum()*100:.2f}%")
print(f"PC1: {pca.explained_variance_ratio_[0]*100:.1f}%")
print(f"PC2: {pca.explained_variance_ratio_[1]*100:.1f}%")
```

### স্টেপ ৪: এলবো মেথড — সঠিক K নির্বাচন
```python
print("\n=== স্টেপ ৪: এলবো মেথড ও K নির্বাচন ===")

K_range = range(2, 11)
inertias = []
silhouettes = []
calinski_scores = []
davies_scores = []

for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))
    calinski_scores.append(calinski_harabasz_score(X_scaled, labels))
    davies_scores.append(davies_bouldin_score(X_scaled, labels))
    
    print(f"K={k}: Inertia={kmeans.inertia_:.0f}, Silhouette={silhouettes[-1]:.4f}, "
          f"CH={calinski_scores[-1]:.0f}, DB={davies_scores[-1]:.4f}")

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0, 0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_title('এলবো মেথড (Inertia)', fontsize=12)
axes[0, 0].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[0, 0].set_ylabel('Inertia')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(K_range, silhouettes, 'go-', linewidth=2, markersize=8)
axes[0, 1].axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='ভালো = 0.5+')
axes[0, 1].set_title('সিলুয়েট স্কোর', fontsize=12)
axes[0, 1].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[0, 1].set_ylabel('Silhouette Score')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(K_range, calinski_scores, 'mo-', linewidth=2, markersize=8)
axes[1, 0].set_title('Calinski-Harabasz স্কোর', fontsize=12)
axes[1, 0].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[1, 0].set_ylabel('CH Score')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(K_range, davies_scores, 'co-', linewidth=2, markersize=8)
axes[1, 1].set_title('Davies-Bouldin স্কোর (কম = ভালো)', fontsize=12)
axes[1, 1].set_xlabel('K (ক্লাস্টার সংখ্যা)')
axes[1, 1].set_ylabel('DB Score')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('project_k_selection.png', dpi=100)
plt.show()

# Best K
best_k_sil = K_range[np.argmax(silhouettes)]
print(f"\n🏆 সিলুয়েট স্কোর অনুসারে সেরা K: {best_k_sil}")
print(f"🏆 এলবো মেথড অনুসারে সেরা K: 3 বা 4")
```

### স্টেপ ৫: K-Means ক্লাস্টারিং
```python
print("\n=== স্টেপ ৫: K-Means ক্লাস্টারিং (K=4) ===")

k_optimal = 4
kmeans_final = KMeans(n_clusters=k_optimal, init='k-means++', n_init=10, random_state=42)
ecom_customers['ক্লাস্টার_KMeans'] = kmeans_final.fit_predict(X_scaled)

print("ক্লাস্টার ডিস্ট্রিবিউশন:")
print(ecom_customers['ক্লাস্টার_KMeans'].value_counts().sort_index())

# ক্লাস্টার প্রোফাইল
cluster_profile = ecom_customers.groupby('ক্লাস্টার_KMeans')[cluster_features].mean().round(1)
cluster_profile['গ্রাহক_সংখ্যা'] = ecom_customers.groupby('ক্লাস্টার_KMeans').size()
print("\nক্লাস্টার প্রোফাইল (গড় মান):")
print(cluster_profile)

# সেগমেন্ট নামকরণ
segment_names = {
    0: '🟢 ইকোনমি শপার (কম আয়, কম ব্যয়)',
    1: '🔵 বড় ক্রেতা (উচ্চ আয়, বেশি ব্যয়)',
    2: '🟡 ব্রাউজার (অনেক ভিজিট, কম ক্রয়)',
    3: '🟣 প্রিমিয়াম (সিনিয়র, উচ্চ ব্যয়)'
}

print("\nসেগমেন্ট ব্যাখ্যা:")
for cluster, name in segment_names.items():
    count = (ecom_customers['ক্লাস্টার_KMeans'] == cluster).sum()
    print(f"  ক্লাস্টার {cluster}: {name} — {count} গ্রাহক ({count/len(ecom_customers)*100:.1f}%)")
```

### স্টেপ ৬: ক্লাস্টার ভিজুয়ালাইজেশন
```python
print("\n=== স্টেপ ৬: ক্লাস্টার ভিজুয়ালাইজেশন ===")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PCA প্রজেকশন
colors = ['green', 'blue', 'gold', 'purple']
for i in range(k_optimal):
    mask = ecom_customers['ক্লাস্টার_KMeans'] == i
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors[i], 
                   label=segment_names[i].split('(')[0], s=40, alpha=0.7, edgecolors='white', linewidth=0.3)
    # ক্লাস্টার সেন্টার (PCA-তে ট্রান্সফর্মড)
    center_pca = pca.transform(kmeans_final.cluster_centers_[i].reshape(1, -1))
    axes[0].scatter(center_pca[0, 0], center_pca[0, 1], c='red', marker='X', 
                   s=200, edgecolors='black', linewidth=2)

axes[0].set_title('K-Means ক্লাস্টার (PCA প্রজেকশন)', fontsize=14)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

# আয় vs ব্যয়
for i in range(k_optimal):
    mask = ecom_customers['ক্লাস্টার_KMeans'] == i
    axes[1].scatter(ecom_customers.loc[mask, 'বার্ষিক_আয়'], 
                   ecom_customers.loc[mask, 'মাসিক_ব্যয়'],
                   c=colors[i], label=segment_names[i].split('(')[0], 
                   s=40, alpha=0.7, edgecolors='white', linewidth=0.3)

axes[1].set_title('ক্লাস্টার: আয় vs ব্যয়', fontsize=14)
axes[1].set_xlabel('বার্ষিক আয় ($)')
axes[1].set_ylabel('মাসিক ব্যয় ($)')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('project_clusters_visual.png', dpi=100)
plt.show()
```

### স্টেপ ৭: হায়ারার্কিক্যাল ক্লাস্টারিং
```python
print("\n=== স্টেপ ৭: হায়ারার্কিক্যাল ক্লাস্টারিং ===")

# ডেনড্রোগ্রাম
plt.figure(figsize=(14, 7))
Z = linkage(X_scaled[:200], method='ward')  # 200 নমুনা (ভিজুয়ালিটির জন্য)
dn = dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90,
                leaf_font_size=10, show_contracted=True)
plt.title('হায়ারার্কিক্যাল ক্লাস্টারিং ডেনড্রোগ্রাম (Ward Method)', fontsize=14)
plt.xlabel('গ্রাহক')  
plt.ylabel('দূরত্ব')
plt.tight_layout()
plt.savefig('project_dendrogram.png', dpi=100)
plt.show()

# অ্যাগ্লোমেরেটিভ ক্লাস্টারিং
agg_clustering = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
ecom_customers['ক্লাস্টার_Agg'] = agg_clustering.fit_predict(X_scaled)

# K-Means ও Agglomerative-এর তুলনা
from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, completeness_score

ami = adjusted_mutual_info_score(ecom_customers['ক্লাস্টার_KMeans'], ecom_customers['ক্লাস্টার_Agg'])
print(f"K-Means vs Agglomerative ক্লাস্টারিং-এর Adjusted Mutual Info: {ami:.4f}")
print("(1.0 = সম্পূর্ণ একই ক্লাস্টারিং, 0 = র‍্যান্ডম)")
```

### স্টেপ ৮: DBSCAN ক্লাস্টারিং
```python
print("\n=== স্টেপ ৮: DBSCAN ক্লাস্টারিং (আউটলায়ার সনাক্তকরণ) ===")

# eps নির্ধারণ (k-distance গ্রাফ)
neighbors = NearestNeighbors(n_neighbors=5)
neighbors_fit = neighbors.fit(X_scaled)
distances, indices = neighbors_fit.kneighbors(X_scaled)
distances = np.sort(distances[:, -1])

plt.figure(figsize=(10, 5))
plt.plot(distances, 'b-', linewidth=2)
plt.axhline(y=np.percentile(distances, 75), color='red', linestyle='--', 
            label=f'75th percentile = {np.percentile(distances, 75):.3f}')
plt.title('K-Distance গ্রাফ (eps নির্ধারণ)', fontsize=14)
plt.xlabel('পয়েন্ট (সর্টেড)')
plt.ylabel('5th নিকটতম প্রতিবেশীর দূরত্ব')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('project_dbscan_kdist.png', dpi=100)
plt.show()

# DBSCAN
optimal_eps = np.percentile(distances, 75)
dbscan = DBSCAN(eps=optimal_eps, min_samples=5)
ecom_customers['ক্লাস্টার_DBSCAN'] = dbscan.fit_predict(X_scaled)

n_clusters_db = len(set(ecom_customers['ক্লাস্টার_DBSCAN'])) - (1 if -1 in ecom_customers['ক্লাস্টার_DBSCAN'] else 0)
n_noise = (ecom_customers['ক্লাস্টার_DBSCAN'] == -1).sum()

print(f"DBSCAN (eps={optimal_eps:.3f}):")
print(f"  ক্লাস্টার সংখ্যা: {n_clusters_db}")
print(f"  আউটলায়ার (নয়েজ): {n_noise} গ্রাহক ({n_noise/len(ecom_customers)*100:.1f}%)")
```

### স্টেপ ৯: Gaussian Mixture Model (GMM)
```python
print("\n=== স্টেপ ৯: Gaussian Mixture Model ===")

gmm = GaussianMixture(n_components=4, random_state=42, covariance_type='full')
ecom_customers['ক্লাস্টার_GMM'] = gmm.fit_predict(X_scaled)
gmm_probs = gmm.predict_proba(X_scaled)

print("GMM ক্লাস্টার ডিস্ট্রিবিউশন:")
print(ecom_customers['ক্লাস্টার_GMM'].value_counts().sort_index())

# সফ্ট অ্যাসাইনমেন্টের উদাহরণ
print("\nপ্রথম ৫ গ্রাহকের সফ্ট অ্যাসাইনমেন্ট (প্রোবাবিলিটি):")
prob_df = pd.DataFrame(gmm_probs[:5], columns=[f'ক্লাস্টার_{i}' for i in range(4)])
prob_df.index = [f'গ্রাহক_{i+1}' for i in range(5)]
print(prob_df.round(3))
```

### স্টেপ ১০: ক্লাস্টারিং তুলনা ও সেরা মডেল নির্বাচন
```python
print("\n=== স্টেপ ১০: ক্লাস্টারিং মডেল তুলনা ===")

clusterings = {
    'K-Means (K=4)': ecom_customers['ক্লাস্টার_KMeans'],
    'Agglomerative': ecom_customers['ক্লাস্টার_Agg'],
    'DBSCAN': ecom_customers['ক্লাস্টার_DBSCAN'],
    'GMM': ecom_customers['ক্লাস্টার_GMM']
}

comparison = {}
for name, labels in clusterings.items():
    # DBSCAN-এর জন্য শুধু কোর পয়েন্ট
    if name == 'DBSCAN':
        core_mask = labels != -1
        if core_mask.sum() > 0:
            sil = silhouette_score(X_scaled[core_mask], labels[core_mask])
            ch = calinski_harabasz_score(X_scaled[core_mask], labels[core_mask])
            db = davies_bouldin_score(X_scaled[core_mask], labels[core_mask])
        else:
            sil, ch, db = 0, 0, 0
    else:
        sil = silhouette_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    comparison[name] = {'ক্লাস্টার': n_clusters, 'Silhouette': sil, 'CH Score': ch, 'DB Score': db}

comparison_df = pd.DataFrame(comparison).T
print(comparison_df.round(4))

# সেরা মডেল
best_sil = comparison_df['Silhouette'].idxmax()
print(f"\n🏆 সিলুয়েট স্কোর অনুসারে সেরা মডেল: {best_sil}")
```

### বিজনেস ইনসাইটস
```python
print("\n=== বিজনেস ইনসাইটস ===")

insights = """
## গ্রাহক সেগমেন্টেশন থেকে ব্যবসায়িক অন্তর্দৃষ্টি:

### 🟢 ইকোনমি শপার (কম আয়, কম ব্যয়)
• বৈশিষ্ট্য: তরুণ, $৪০K এর কম আয়, কুপন ব্যবহার বেশি
• কৌশল: বাজেট-ফ্রেন্ডলি প্রোডাক্ট দেখানো, কুপন ও ডিসকাউন্ট
• Retention: ইমেল মার্কেটিং, লয়্যালটি পয়েন্ট

### 🔵 বড় ক্রেতা (উচ্চ আয়, বেশি ব্যয়)
• বৈশিষ্ট্য: ৩০-৫০ বছর, $৮০K+ আয়, ঘন ঘন ক্রয়
• কৌশল: প্রিমিয়াম প্রোডাক্ট, VIP সার্ভিস, এক্সক্লুসিভ অফার
• Retention: ব্যক্তিগতকৃত রিকমেন্ডেশন, প্রি-অর্ডার

### 🟡 ব্রাউজার (অনেক ভিজিট, কম ক্রয়)
• বৈশিষ্ট্য: তরুণ, অনেক সময় দেয় কিন্তু কম কেনে
• কৌশল: রিটার্গেটিং অ্যাড, পার্সোনালাইজড রিকমেন্ডেশন
• Retention: আবান্ডনড কার্ট রিমাইন্ডার, সীমিত সময়ের অফার

### 🟣 প্রিমিয়াম (সিনিয়র, উচ্চ ব্যয়)
• বৈশিষ্ট্য: ৫০+ বছর, উচ্চ আয়, দামি পণ্য কেনে
• কৌশল: প্রিমিয়াম সাপোর্ট, কুয়ালিটি প্রোডাক্ট, বিশ্বাসযোগ্যতা
• Retention: ফোন সাপোর্ট, লয়্যালটি প্রোগ্রাম
"""
print(insights)
```

### সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("প্রজেক্ট সারসংক্ষেপ")
print("=" * 60)

summary = """
## এই প্রজেক্ট থেকে যা শিখলাম:

✅ সম্পূর্ণ ক্লাস্টারিং পাইপলাইন:
   1. গ্রাহক ডেটা তৈরি ও ফিচার ইঞ্জিনিয়ারিং
   2. স্কেলিং (StandardScaler) — K-Means-এর জন্য অপরিহার্য
   3. এলবো মেথড, সিলুয়েট, CH, DB স্কোর দিয়ে K নির্বাচন
   4. K-Means, Agglomerative, DBSCAN, GMM — ৪টি অ্যালগরিদম
   5. PCA দিয়ে উচ্চ-মাত্রিক ক্লাস্টার ভিজুয়ালাইজেশন
   6. ক্লাস্টার প্রোফাইলিং ও সেগমেন্ট নামকরণ
   7. বিজনেস ইনসাইট জেনারেশন

✅ বিভিন্ন ক্লাস্টারিং অ্যালগরিদমের তুলনা:
   • K-Means: দ্রুত, গোলাকার ক্লাস্টার, K দিতে হয়
   • Agglomerative: ডেনড্রোগ্রাম দেখতে পাই
   • DBSCAN: ক্লাস্টার সংখ্যা বলে দেয় না, আউটলায়ার ডিটেক্ট
   • GMM: সফ্ট অ্যাসাইনমেন্ট (প্রোবাবিলিটি)

✅ Data Analyst-এর Takeaways:
📌 ক্লাস্টারিং আনসুপারভাইজড — লেবেল লাগে না
📌 একাধিক ক্লাস্টারিং অ্যালগরিদম ট্রাই করা উচিত
📌 ক্লাস্টার ব্যাখ্যা করা সবচেয়ে গুরুত্বপূর্ণ
"""
print(summary)
```