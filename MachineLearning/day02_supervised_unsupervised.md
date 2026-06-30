# Day 02: Supervised vs Unsupervised Learning
## তত্ত্বাবধায়ক ও অ-তত্ত্বাবধায়ক শিক্ষা

### Supervised Learning (তত্ত্বাবধায়ক শিক্ষা)
Supervised Learning এ আমরা ইনপুট (features) এবং আউটপুট (labels) উভয়ই সরবরাহ করি। মডেলটি ইনপুট থেকে আউটপুট ম্যাপিং শেখে।

**প্রকারভেদ:**
1. **Regression** - ক্রমাগত মান পূর্বাভাস (যেমন: স্টক মূল্য)
2. **Classification** - বিভাগ পূর্বাভাস (যেমন: ফ্রড বা না)

**ফাইন্যান্স উদাহরণ:**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

# Regression উদাহরণ: স্টক মূল্য পূর্বাভাস
np.random.seed(42)
days = 200
X = np.arange(days).reshape(-1, 1)
y = 100 + X.squeeze() * 0.5 + np.random.randn(days) * 5

model_reg = LinearRegression()
model_reg.fit(X, y)
print(f"Regression Coef: {model_reg.coef_[0]:.2f}")
print(f"Intercept: {model_reg.intercept_:.2f}")

# Classification উদাহরণ: ফ্রড ডিটেকশন
n_transactions = 500
transaction_amount = np.random.exponential(1000, n_transactions)
is_fraud = (transaction_amount > 3000).astype(int)  # সরলীকৃত

X_clf = transaction_amount.reshape(-1, 1)
y_clf = is_fraud

model_clf = RandomForestClassifier(n_estimators=10)
model_clf.fit(X_clf, y_clf)
print(f"\nফ্রড ডিটেকশন মডেল তৈরি!")
```

### Unsupervised Learning (অ-তত্ত্বাবধায়ক শিক্ষা)
Unsupervised Learning এ শুধুমাত্র ইনপুট ডেটা থাকে, কোন লেবেল থাকে না। মডেল নিজেই প্যাটার্ন খুঁজে বের করে।

**প্রকারভেদ:**
1. **Clustering** - গ্রুপিং (যেমন: গ্রাহক সেগমেন্টেশন)
2. **Dimensionality Reduction** - মাত্রা হ্রাস (যেমন: PCA)

**ফাইন্যান্স উদাহরণ:**
```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Clustering উদাহরণ: গ্রাহক সেগমেন্টেশন
np.random.seed(42)
n_customers = 300

customer_data = pd.DataFrame({
    'annual_income': np.random.normal(60000, 20000, n_customers),
    'spending_score': np.random.normal(50, 20, n_customers),
    'loan_amount': np.random.exponential(10000, n_customers)
})

kmeans = KMeans(n_clusters=3, random_state=42)
customer_data['segment'] = kmeans.fit_predict(customer_data)

print("গ্রাহক সেগমেন্ট তৈরি:")
print(customer_data['segment'].value_counts())

# PCA উদাহরণ: মাত্রা হ্রাস
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(customer_data[['annual_income', 'spending_score', 'loan_amount']])
print(f"\nPCA এর পর ডেটার আকৃতি: {reduced_data.shape}")
print(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
```

### Supervised vs Unsupervised তুলনা

| বৈশিষ্ট্য | Supervised | Unsupervised |
|-----------|-----------|-------------|
| লেবেল প্রয়োজন | হ্যাঁ | না |
| জটিলতা | বেশি সরল | বেশি জটিল |
| প্রয়োগ | প্রেডিকশন | প্যাটার্ন খোঁজা |
| উদাহরণ | রিগ্রেশন, ক্লাসিফিকেশন | ক্লাস্টারিং, PCA |

### Semi-supervised Learning
একটি হাইব্রিড পদ্ধতি যেখানে অল্প লেবেলযুক্ত এবং প্রচুর লেবেলবিহীন ডেটা ব্যবহার করা হয়।

### ফাইন্যান্সে প্রয়োগ
```python
# পোর্টফোলিও ক্লাস্টারিং (Unsupervised)
np.random.seed(42)
stocks = pd.DataFrame({
    'stock_a': np.random.randn(100) * 0.02,
    'stock_b': np.random.randn(100) * 0.03,
    'stock_c': np.random.randn(100) * 0.015,
    'stock_d': np.random.randn(100) * 0.025
})

# Correlation matrix
corr = stocks.corr()
print("স্টক রিটার্নের Correlation:\n", corr)
```

### সারসংক্ষেপ
Supervised Learning লেবেলযুক্ত ডেটা থেকে শেখে (প্রেডিকশন), Unsupervised Learning লেবেলবিহীন ডেটা থেকে প্যাটার্ন খুঁজে (ইনসাইট)। ফাইন্যান্সে উভয়েরই গুরুত্বপূর্ণ ভূমিকা রয়েছে।