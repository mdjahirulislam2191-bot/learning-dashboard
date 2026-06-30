# Day 37: অ্যানোমালি ডিটেকশন
## Anomaly Detection

### অ্যানোমালি ডিটেকশন কি?
অ্যানোমালি ডিটেকশন হল অস্বাভাবিক প্যাটার্ন শনাক্ত করার প্রক্রিয়া যা সাধারণ আচরণ থেকে উল্লেখযোগ্যভাবে বিচ্যুত। ফাইন্যান্সে এটি ফ্রড ডিটেকশন এবং রিস্ক ম্যানেজমেন্টের জন্য গুরুত্বপূর্ণ।

### ফাইন্যান্সে অ্যানোমালি ডিটেকশনের ব্যবহার
- **ফ্রড ডিটেকশন**: জালিয়াতি লেনদেন শনাক্তকরণ
- **মার্কেট অ্যানোমালি**: অস্বাভাবিক মার্কেট আচরণ
- **রিস্ক ম্যানেজমেন্ট**: সিস্টেমিক রিস্ক শনাক্তকরণ
- **কোয়ালিটি কন্ট্রোল**: ডেটা ইন্টিগ্রিটি চেক

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns

# ফাইন্যান্সিয়াল লেনদেন ডেটা
np.random.seed(42)
n_normal = 980
n_anomalies = 20
n_total = n_normal + n_anomalies

# নরমাল লেনদেন
normal = pd.DataFrame({
    'amount': np.random.exponential(150, n_normal),
    'frequency': np.random.poisson(5, n_normal),
    'distance': np.random.exponential(10, n_normal),
    'hour': np.random.randint(6, 22, n_normal),
    'amount_std': np.random.rand(n_normal) * 2 + 1
})

# অ্যানোমালি (ফ্রড)
anomalies = pd.DataFrame({
    'amount': np.random.exponential(2000, n_anomalies),
    'frequency': np.random.poisson(20, n_anomalies),
    'distance': np.random.exponential(500, n_anomalies),
    'hour': np.random.choice([2, 3, 4, 23], n_anomalies),
    'amount_std': np.random.rand(n_anomalies) * 5 + 3
})

df = pd.concat([normal, anomalies], ignore_index=True).sample(frac=1, random_state=42)
df['is_anomaly'] = np.where(np.arange(n_total) >= n_normal, 1, 0)

print("📊 Transaction Data:")
print(f"Normal transactions: {n_normal}")
print(f"Anomalies (Fraud): {n_anomalies}")
print(f"Anomaly ratio: {n_anomalies/n_total:.2%}")

X = df.drop(['is_anomaly'], axis=1)
y = df['is_anomaly']

# স্কেলিং
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### 1. Isolation Forest
```python
# Isolation Forest
iso_forest = IsolationForest(contamination=0.02, random_state=42, n_estimators=100)
iso_pred = iso_forest.fit_predict(X_scaled)
iso_pred_binary = [1 if p == -1 else 0 for p in iso_pred]

# ইভালুয়েশন
from sklearn.metrics import classification_report, confusion_matrix

print("\n🔍 Isolation Forest Results:")
print(classification_report(y, iso_pred_binary, target_names=['Normal', 'Anomaly']))

cm = confusion_matrix(y, iso_pred_binary)
print(f"Confusion Matrix:")
print(f"  TN: {cm[0,0]:4d}  FP: {cm[0,1]:4d}")
print(f"  FN: {cm[1,0]:4d}  TP: {cm[1,1]:4d}")
print(f"  Anomaly Detection Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.2%}")
```

### 2. Local Outlier Factor (LOF)
```python
# LOF
lof = LocalOutlierFactor(contamination=0.02, n_neighbors=20)
lof_pred = lof.fit_predict(X_scaled)
lof_pred_binary = [1 if p == -1 else 0 for p in lof_pred]
lof_scores = lof.negative_outlier_factor_

print("\n🔍 LOF Results:")
print(classification_report(y, lof_pred_binary, target_names=['Normal', 'Anomaly']))

cm = confusion_matrix(y, lof_pred_binary)
print(f"  Anomaly Detection Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.2%}")

# LOF স্কোর বিশ্লেষণ
print(f"\nLOF Scores:")
print(f"  Normal (mean): {lof_scores[y == 0].mean():.4f}")
print(f"  Anomaly (mean): {lof_scores[y == 1].mean():.4f}")
```

### 3. One-Class SVM
```python
# One-Class SVM
oc_svm = OneClassSVM(nu=0.02, kernel='rbf', gamma='auto')
oc_svm_pred = oc_svm.fit_predict(X_scaled)
oc_svm_binary = [1 if p == -1 else 0 for p in oc_svm_pred]

print("\n🔍 One-Class SVM Results:")
print(classification_report(y, oc_svm_binary, target_names=['Normal', 'Anomaly']))

cm = confusion_matrix(y, oc_svm_binary)
print(f"  Anomaly Detection Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.2%}")
```

### 4. Elliptic Envelope (মহালানোবিস দূরত্ব)
```python
# Elliptic Envelope
ell_env = EllipticEnvelope(contamination=0.02, random_state=42)
ell_pred = ell_env.fit_predict(X_scaled)
ell_binary = [1 if p == -1 else 0 for p in ell_pred]

print("\n🔍 Elliptic Envelope Results:")
print(classification_report(y, ell_binary, target_names=['Normal', 'Anomaly']))

cm = confusion_matrix(y, ell_binary)
print(f"  Anomaly Detection Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.2%}")
```

### 5. মডেল তুলনা
```python
# সব মডেলের ফলাফল তুলনা
models = {
    'Isolation Forest': iso_pred_binary,
    'LOF': lof_pred_binary,
    'One-Class SVM': oc_svm_binary,
    'Elliptic Envelope': ell_binary
}

print("\n📊 Model Comparison:")
print("-" * 70)
print(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
print("-" * 70)

for name, preds in models.items():
    acc = np.mean(preds == y)
    cm = confusion_matrix(y, preds)
    prec = cm[1,1] / (cm[1,1] + cm[0,1]) if (cm[1,1] + cm[0,1]) > 0 else 0
    rec = cm[1,1] / (cm[1,1] + cm[1,0]) if (cm[1,1] + cm[1,0]) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    
    print(f"{name:<20} {acc:<12.4f} {prec:<12.4f} {rec:<12.4f} {f1:<12.4f}")
```

### 6. ভিজুয়ালাইজেশন (PCA 2D প্রজেকশন)
```python
# PCA ভিজুয়ালাইজেশন
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Isolation Forest স্কোর
iso_scores = iso_forest.score_samples(X_scaled)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# True anomalies
axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='coolwarm', alpha=0.6)
axes[0, 0].set_title('True Anomalies (Red=Anomaly)')
axes[0, 0].set_xlabel('PC1')
axes[0, 0].set_ylabel('PC2')

# Isolation Forest
axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=iso_pred_binary, cmap='coolwarm', alpha=0.6)
axes[0, 1].set_title('Isolation Forest Predictions')
axes[0, 1].set_xlabel('PC1')
axes[0, 1].set_ylabel('PC2')

# LOF
axes[1, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=lof_pred_binary, cmap='coolwarm', alpha=0.6)
axes[1, 0].set_title('LOF Predictions')
axes[1, 0].set_xlabel('PC1')
axes[1, 0].set_ylabel('PC2')

# Isolation Forest Anomaly Scores
scatter = axes[1, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=iso_scores, 
                              cmap='viridis', alpha=0.6)
axes[1, 1].set_title('Isolation Forest - Anomaly Scores')
axes[1, 1].set_xlabel('PC1')
axes[1, 1].set_ylabel('PC2')
plt.colorbar(scatter, ax=axes[1, 1])

plt.tight_layout()
plt.show()
```

### 7. থ্রেশহোল্ড টিউনিং
```python
# সেরা থ্রেশহোল্ড খোঁজা
def find_best_threshold(scores, y_true):
    thresholds = np.linspace(scores.min(), scores.max(), 100)
    best_f1 = 0
    best_th = 0
    
    for th in thresholds:
        preds = (scores < th).astype(int)
        cm = confusion_matrix(y_true, preds)
        
        if cm.shape == (2, 2):
            prec = cm[1,1] / (cm[1,1] + cm[0,1]) if (cm[1,1] + cm[0,1]) > 0 else 0
            rec = cm[1,1] / (cm[1,1] + cm[1,0]) if (cm[1,1] + cm[1,0]) > 0 else 0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            
            if f1 > best_f1:
                best_f1 = f1
                best_th = th
    
    return best_th, best_f1

best_threshold, best_f1 = find_best_threshold(iso_scores, y)
print(f"\n🎯 Best Isolation Forest Threshold: {best_threshold:.4f}")
print(f"   Best F1-Score: {best_f1:.4f}")

# টিউনড থ্রেশহোল্ড দিয়ে
tuned_preds = (iso_scores < best_threshold).astype(int)
print("\n📊 Tuned Model:")
print(classification_report(y, tuned_preds, target_names=['Normal', 'Anomaly']))
```

### অ্যানোমালি ডিটেকশন বেস্ট প্র্যাকটিস
```python
print("""
✅ Anomaly Detection Best Practices:
1️⃣ Know your anomaly ratio (contamination rate)
2️⃣ Use multiple detection methods
3️⃣ Tune threshold for business requirements
4️⃣ Consider feature engineering
5️⃣ Regular model retraining
6️⃣ Use ensemble of detectors

🔑 Key Considerations:
- False positives vs. false negatives trade-off
- Business cost of missing anomalies
- Computational efficiency for real-time detection
- Interpretability of anomaly scores

📊 Method Selection:
- Isolation Forest: Fast, high-dimensional, general purpose
- LOF: Local anomalies, varying densities
- One-Class SVM: Boundary-based, kernel flexible
- Elliptic Envelope: Gaussian assumption, fast
""")
```

### সারসংক্ষেপ
আজ আমরা অ্যানোমালি ডিটেকশন শিখলাম:
- **Isolation Forest**: আইসোলেটিং অ্যানোমালি
- **LOF**: লোকাল ডেনসিটি কম্পারিজন
- **One-Class SVM**: নরমাল ডেটার বাউন্ডারি
- **Elliptic Envelope**: গাউসিয়ান ডিস্ট্রিবিউশন অ্যাসাম্পশন
- **থ্রেশহোল্ড টিউনিং**: F1-অপ্টিমাইজড থ্রেশহোল্ড

### অনুশীলনী
1. রিয়েল-টাইম লেনদেন স্ট্রিমে অ্যানোমালি ডিটেকশন ইমপ্লিমেন্ট করুন
2. বিভিন্ন contamination রেট নিয়ে এক্সপেরিমেন্ট করুন
3. অটোএনকোডার-বেসড অ্যানোমালি ডিটেকশন ইমপ্লিমেন্ট করুন
4. মাল্টি-স্টেজ অ্যানোমালি ডিটেকশন পাইপলাইন তৈরি করুন