# Day 19: এন্সেম্বল মেথড
## Ensemble Methods

### এন্সেম্বল লার্নিং কি?
একাধিক মডেলকে কম্বাইন করে একটি শক্তিশালী মডেল তৈরি করা। "বহু মাথায় বুদ্ধি বেশি" নীতিতে কাজ করে।

### প্রধান এন্সেম্বল টেকনিক
1. **Bagging** - Parallel (Random Forest)
2. **Boosting** - Sequential (XGBoost)
3. **Stacking** - Meta-learner
4. **Voting** - Majority voting

### ফাইন্যান্স উদাহরণ: ক্রেডিট রিস্ক (সমস্ত এন্সেম্বল)
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    VotingClassifier, AdaBoostClassifier, BaggingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'credit_score': np.random.randint(300, 850, n),
    'income': np.random.exponential(50000, n),
    'loan_amount': np.random.exponential(15000, n),
    'debt_ratio': np.random.uniform(0.1, 0.6, n),
    'employment_years': np.random.exponential(8, n),
    'num_late_payments': np.random.poisson(1, n)
})

risk = (data['credit_score'] * 0.3 + data['income']/1000 * 0.2 - 
        data['loan_amount']/1000 * 0.2 - data['debt_ratio'] * 100 +
        data['employment_years'] * 5 - data['num_late_payments'] * 10 +
        np.random.randn(n) * 20)
data['good_credit'] = (risk > np.median(risk)).astype(int)

X = data.drop('good_credit', axis=1)
y = data['good_credit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
```

### 1. Voting Classifier
```python
estimators = [
    ('lr', LogisticRegression(max_iter=1000)),
    ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
    ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42))
]

voting_hard = VotingClassifier(estimators=estimators, voting='hard')
voting_soft = VotingClassifier(estimators=estimators, voting='soft')

voting_hard.fit(X_train_s, y_train)
voting_soft.fit(X_train_s, y_train)

print("📊 Voting Classifier:")
print(f"Hard Voting: {voting_hard.score(X_test_s, y_test):.4f}")
print(f"Soft Voting: {voting_soft.score(X_test_s, y_test):.4f}")
```

### 2. Bagging vs Boosting তুলনা
```python
models = {
    'Single Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Bagging (10 trees)': BaggingClassifier(
        DecisionTreeClassifier(max_depth=5), n_estimators=10, random_state=42),
    'Bagging (50 trees)': BaggingClassifier(
        DecisionTreeClassifier(max_depth=5), n_estimators=50, random_state=42),
    'Random Forest (50)': RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42),
    'AdaBoost (50)': AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=3), n_estimators=50, random_state=42),
    'Gradient Boosting (50)': GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=42)
}

print("\n🏆 Ensemble Methods Comparison:")
for name, model in models.items():
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"{name:30s}: Train={train_acc:.4f}, Test={test_acc:.4f}")
```

### 3. Bagging Details
```python
print("""
🟦 Bagging (Bootstrap Aggregating):

প্রক্রিয়া:
1. Bootstrap samples তৈরি (ডেটা random sampling with replacement)
2. প্রতিটি sample-এ আলাদা মডেল ট্রেইন
3. Majority voting (classification) বা average (regression)

সুবিধা:
├── High variance models-এর variance কমায়
├── Overfitting কমায়
├── Parallelizable (দ্রুত)
└── Out-of-bag (OOB) error estimate

ফাইন্যান্স: Random Forest = Bagging + Decision Trees
""")
```

### 4. Boosting Details
```python
print("""
🟩 Boosting:

প্রক্রিয়া:
1. Sequential training (একটির পর একটি)
2. প্রতিটি নতুন মডেল পুরোনোর ভুল শুধরে
3. Weighted voting (ভালো মডেল বেশি গুরুত্ব পায়)

প্রকার:
├── AdaBoost: ভুল নমুনার ওজন বাড়ায়
├── Gradient Boosting: গ্রেডিয়েন্ট দিয়ে error কমায়
├── XGBoost: Regularized + Parallel version
└── LightGBM: দ্রুত + কম memory

ফাইন্যান্স: High accuracy প্রয়োজন হলে Boosting ব্যবহার করুন
""")
```

### 5. Weighted Ensemble (Custom)
```python
# নিজস্ব ওয়েটেড এন্সেম্বল
lr_pred = LogisticRegression(max_iter=1000).fit(X_train_s, y_train).predict_proba(X_test_s)[:, 1]
rf_pred = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_train, y_train).predict_proba(X_test)[:, 1]
gb_pred = GradientBoostingClassifier(n_estimators=50, random_state=42).fit(X_train, y_train).predict_proba(X_test)[:, 1]

# ওয়েটেড কম্বিনেশন
weights = [0.2, 0.4, 0.4]  # বেশি accuracy এর মডেল বেশি weight
ensemble_pred = (lr_pred * weights[0] + rf_pred * weights[1] + gb_pred * weights[2])
ensemble_class = (ensemble_pred > 0.5).astype(int)

print(f"\n🎯 Custom Weighted Ensemble AUC: {roc_auc_score(y_test, ensemble_pred):.4f}")
```

### Ensemble Size vs Performance
```python
n_estimators_list = [1, 5, 10, 20, 50, 100, 200]
bagging_scores = []
boosting_scores = []

for n in n_estimators_list:
    bag = BaggingClassifier(DecisionTreeClassifier(max_depth=5), 
                            n_estimators=n, random_state=42).fit(X_train, y_train)
    boost = GradientBoostingClassifier(n_estimators=n, max_depth=3, 
                                       random_state=42).fit(X_train, y_train)
    bagging_scores.append(bag.score(X_test, y_test))
    boosting_scores.append(boost.score(X_test, y_test))

print("\n📈 Estimators vs Accuracy:")
print("Estimators | Bagging | Boosting")
print("-" * 35)
for n, b, g in zip(n_estimators_list, bagging_scores, boosting_scores):
    print(f"{n:6d}     | {b:.4f}   | {g:.4f}")
```

### Ensemble Best Practices
```python
print("""
📋 কখন কী ব্যবহার করবেন?

High Variance (Overfitting):
├── Bagging / Random Forest ✅
├── Voting with diverse models
└── Más ডেটা যোগ করুন

High Bias (Underfitting):
├── Boosting ✅
├── কমপ্লেক্স মডেল যোগ করুন
└── ফিচার ইঞ্জিনিয়ারিং

Best Performance:
├── Stacking ✅ (meta-learner)
├── XGBoost / LightGBM
└── Blending (hold-out set)

Speed Priority:
├── Voting (parallel) ✅
├── Random Forest
└── Bagging
""")
```

### সারসংক্ষেপ
এন্সেম্বল মেথড একাধিক মডেল কম্বাইন করে accuracy এবং robustness বাড়ায়। Bagging variance কমায়, Boosting bias কমায়। ফাইন্যান্সে Voting, Stacking, এবং Blending ব্যাপকভাবে ব্যবহৃত হয়।