# Day 14: গ্রেডিয়েন্ট বুটিং
## Gradient Boosting

### গ্রেডিয়েন্ট বুটিং কি?
Gradient Boosting sequentially দুর্বল লার্নার (shallow trees) যোগ করে যেখানে প্রতিটি নতুন ট্রি পূর্ববর্তী ট্রির ভুল শুধরে দেয়।

### XGBoost, LightGBM, CatBoost
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import make_classification
import time

# ফাইন্যান্সিয়াল ডেটা
np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'loan_amount': np.random.exponential(20000, n),
    'interest_rate': np.random.uniform(5, 15, n),
    'credit_score': np.random.randint(300, 850, n),
    'debt_ratio': np.random.uniform(0.1, 0.6, n),
    'employment_duration': np.random.exponential(5, n),
    'num_defaults': np.random.poisson(0.3, n),
    'age': np.random.randint(22, 70, n),
    'num_inquiries': np.random.poisson(2, n)
})

# লেবেল: Loan Default
score = (200 + data['credit_score'] * 0.5 - data['debt_ratio'] * 200 
         - data['num_defaults'] * 50 - data['num_inquiries'] * 20
         + np.random.randn(n) * 30)
data['default'] = (score < 400).astype(int)

X = data.drop('default', axis=1)
y = data['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Default Rate: {y.mean():.2%}")
```

### Gradient Boosting Classifier
```python
start = time.time()

gb = GradientBoostingClassifier(
    n_estimators=100,      # বুটিং স্টেপ
    learning_rate=0.1,     # শেখার হার
    max_depth=3,           # প্রতিটি ট্রির গভীরতা
    min_samples_leaf=5,
    subsample=0.8,         # প্রতিটি ট্রির জন্য ডেটা ফ্র্যাকশন
    random_state=42
)
gb.fit(X_train, y_train)

train_time = time.time() - start
y_pred_gb = gb.predict(X_test)
y_prob_gb = gb.predict_proba(X_test)[:, 1]

print(f"\n🏆 Gradient Boosting Results:")
print(f"Training Time: {train_time:.2f}s")
print(f"Accuracy:  {accuracy_score(y_test, y_pred_gb):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob_gb):.4f}")
```

### লার্নিং রেট এবং Estimators
```python
learning_rates = [0.01, 0.05, 0.1, 0.2, 0.5]
results = []

for lr in learning_rates:
    gb_temp = GradientBoostingClassifier(
        n_estimators=200, learning_rate=lr, max_depth=3,
        subsample=0.8, random_state=42
    )
    gb_temp.fit(X_train, y_train)
    test_score = gb_temp.score(X_test, y_test)
    train_score = gb_temp.score(X_train, y_train)
    
    results.append({'lr': lr, 'train': train_score, 'test': test_score})
    print(f"LR={lr:.2f}: Train={train_score:.4f}, Test={test_score:.4f}")

# ওভারফিটিং চেক
print("\n⚠️ Higher learning rate → Faster learning but risk of overfitting")
print("Lower learning rate → Slower but better generalization")
```

### Stage-wise Predictions
```python
# বিভিন্ন স্টেপে মডেল পারফরম্যান্স
staged_scores = []
for i, y_pred_stage in enumerate(gb.staged_predict(X_test)):
    if i % 10 == 0:  # প্রতি 10 স্টেপে চেক
        score = accuracy_score(y_test, y_pred_stage)
        staged_scores.append((i, score))

print("\n🔄 Boosting Stage Performance:")
for stage, score in staged_scores:
    print(f"Stage {stage:3d}: Accuracy={score:.4f}")
```

### Feature Importance
```python
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': gb.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n📊 Feature Importance:")
print(importance_df.to_string(index=False))
```

### লার্নিং রেট এবং n_estimators এর সম্পর্ক
```python
print("""
📐 Learning Rate vs n_estimators:

High LR (0.3-1.0) + Few Trees (10-50):
  → Fast training, risk of overfitting
  → Aggressive learning

Low LR (0.01-0.1) + Many Trees (100-1000):
  → Slower, better generalization
  → Conservative learning

Best Practice: Start with LR=0.1, n_estimators=100
  → Increase n_estimators if underfitting
  → Decrease LR if overfitting
""")
```

### Early Stopping
```python
# validation set-এ মনিটরিং করে ওভারফিটিং থামানো
X_train_sub, X_val, y_train_sub, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42
)

gb_es = GradientBoostingClassifier(
    n_estimators=500,  # বেশি দিলেও early stopping থামাবে
    learning_rate=0.1,
    max_depth=3,
    validation_fraction=0.1,
    n_iter_no_change=10,  # 10 বার কোনো উন্নতি না হলে থাম
    tol=1e-4,
    random_state=42
)
gb_es.fit(X_train, y_train)

print(f"\n🛑 Early Stopping:")
print(f"Trees used: {gb_es.n_estimators_}")
print(f"Best iteration: {gb_es.n_estimators_}")
```

### সারসংক্ষেপ
Gradient Boosting sequentially দুর্বল লার্নার যোগ করে শক্তিশালী মডেল তৈরি করে। Learning rate এবং n_estimators টিউন করা গুরুত্বপূর্ণ। XGBoost, LightGBM, CatBoost এই অ্যালগরিদমের অপ্টিমাইজড ভার্সন।