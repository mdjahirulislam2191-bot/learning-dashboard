# Day 05: Train/Test Split এবং Evaluation Basics
## Train/Test Split & Evaluation Fundamentals

### Train/Test Split কেন প্রয়োজন?
মডেলের জেনারেলাইজেশন ক্ষমতা যাচাই করতে আমরা ডেটাকে দুই ভাগে ভাগ করি:
- **Training Set (70-80%)**: মডেল শেখার জন্য
- **Test Set (20-30%)**: মডেল মূল্যায়নের জন্য

### ফাইন্যান্স উদাহরণ: ক্রেডিট রিস্ক মডেল
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# ক্রেডিট রিস্ক ডেটা তৈরি
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'credit_score': np.random.normal(650, 100, n),
    'income': np.random.exponential(50000, n),
    'loan_amount': np.random.exponential(15000, n),
    'employment_years': np.random.exponential(8, n),
    'debt_ratio': np.random.uniform(0.1, 0.5, n),
    'age': np.random.randint(22, 70, n)
})

# Target: ডিফল্ট রিস্ক (1 = default, 0 = no default)
# উচ্চ ঋণ অনুপাত + কম ক্রেডিট স্কোর = বেশি রিস্ক
default_prob = 1 / (1 + np.exp(-(
    -5 + 
    0.005 * (650 - data['credit_score']) + 
    0.00001 * data['loan_amount'] + 
    3 * data['debt_ratio']
)))
data['default'] = (np.random.random(n) < default_prob).astype(int)

print("ডেটা ওভারভিউ:")
print(data.head())
print(f"\nDefault রেট: {data['default'].mean():.2%}")
```

### Train/Test Split করার নিয়ম
```python
# স্ট্যান্ডার্ড 80/20 স্প্লিট
X = data.drop('default', axis=1)
y = data['default']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples ({len(X_train)/n:.0%})")
print(f"Test set: {X_test.shape[0]} samples ({len(X_test)/n:.0%})")
print(f"\nTraining set default rate: {y_train.mean():.2%}")
print(f"Test set default rate: {y_test.mean():.2%}")
```

### Time Series Split (ফাইন্যান্সের জন্য গুরুত্বপূর্ণ)
```python
from sklearn.model_selection import TimeSeriesSplit

# টাইম সিরিজের জন্য স্পেশাল স্প্লিট
dates = pd.date_range('2024-01-01', periods=len(data), freq='D')
data['date'] = dates
data_sorted = data.sort_values('date')

tscv = TimeSeriesSplit(n_splits=5)

print("Time Series Split:")
for i, (train_idx, test_idx) in enumerate(tscv.split(data_sorted)):
    print(f"Fold {i+1}: Train {len(train_idx)}, Test {len(test_idx)}")
```

### Walk-Forward Validation (ফাইন্যান্স স্ট্যান্ডার্ড)
```python
# ফাইন্যান্সে সবচেয়ে জনপ্রিয় পদ্ধতি
def walk_forward_split(data, window_size=600, step_size=200):
    splits = []
    for start in range(0, len(data) - window_size, step_size):
        train_end = start + window_size
        test_end = min(train_end + step_size, len(data))
        splits.append((start, train_end, test_end))
    return splits

wf_splits = walk_forward_split(data)
print(f"Walk-Forward স্প্লিটস: {len(wf_splits)}")
for i, (s, t, e) in enumerate(wf_splits[:3]):
    print(f"  Fold {i+1}: Train {s}-{t}, Test {t}-{e}")
```

### Overfitting এড়ানোর কৌশল
```python
from sklearn.linear_model import Ridge, Lasso

# Overfitting এর উদাহরণ
from sklearn.tree import DecisionTreeRegressor

# গভীর ট্রি (overfit হবে)
tree_deep = DecisionTreeRegressor(max_depth=20, random_state=42)

# অগভীর ট্রি (generalize করবে)
tree_shallow = DecisionTreeRegressor(max_depth=3, random_state=42)

print("Overfitting এড়াতে:")
print("1. Cross-validation ব্যবহার করুন")
print("2. Regularization প্রয়োগ করুন")
print("3. পর্যাপ্ত ডেটা ব্যবহার করুন")
print("4. Feature selection করুন")
```

### Cross-Validation Basics
```python
# K-Fold Cross Validation
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)

model = LogisticRegression(max_iter=1000)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
```

### Model Evaluation Metrics
```python
# মডেল ট্রেইন এবং ইভালুয়েট
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Default', 'Default']))

# ভিজুয়ালাইজেশন
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Default', 'Default'],
            yticklabels=['No Default', 'Default'])
plt.title('Confusion Matrix - ক্রেডিট রিস্ক মডেল')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
```

### Train/Test Split Best Practices
1. **Shuffle করুন** - সময়নির্ভর ডেটা ছাড়া
2. **Stratify করুন** - ইমব্যালেন্সড ডেটার জন্য
3. **Time series এ shuffling করবেন না**
4. **Multiple splits ব্যবহার করুন** (CV)
5. **Test set টি real-world scenario প্রতিফলিত করবে**

### সারসংক্ষেপ
আজ আমরা শিখলাম কীভাবে ডেটাকে Train/Test Split করতে হয়, কেন Time Series Split ফাইন্যান্সের জন্য গুরুত্বপূর্ণ, এবং Overfitting এড়ানোর কৌশল। Evaluation metrics এর মাধ্যমে আমরা মডেলের পারফরম্যান্স মাপতে পারি।