# Day 30: ইমব্যালেন্সড ডেটা
## Imbalanced Data

### ইমব্যালেন্সড ডেটা কি?
ইমব্যালেন্সড ডেটা হল যখন ক্লাসগুলোর মধ্যে ব্যাপক সংখ্যাগত অসামঞ্জস্য থাকে। যেমন: ফ্রড ডিটেকশনে 99% বৈধ লেনদেন, 1% ফ্রড।

### ফাইন্যান্সে ইমব্যালেন্সড ডেটার উদাহরণ
- **ফ্রড ডিটেকশন**: 99.5% বৈধ, 0.5% ফ্রড
- **লোন ডিফল্ট**: 95% পেমেন্ট, 5% ডিফল্ট
- **স্টক ক্র্যাশ**: 99.9% নরমাল, 0.1% ক্র্যাশ

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, precision_recall_curve,
                             average_precision_score, f1_score)
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline as ImbPipeline
import matplotlib.pyplot as plt
import seaborn as sns

# ফ্রড ডেটা তৈরি
np.random.seed(42)
n_normal = 9500
n_fraud = 500
n_total = n_normal + n_fraud

# নরমাল লেনদেন
normal = pd.DataFrame({
    'amount': np.random.exponential(100, n_normal),
    'time_since_last': np.random.exponential(24, n_normal),
    'distance_from_home': np.random.exponential(10, n_normal),
    'num_transactions_day': np.random.poisson(5, n_normal),
    'merchant_category': np.random.choice([1, 2, 3, 4, 5], n_normal),
    'is_fraud': np.zeros(n_normal)
})

# ফ্রড লেনদেন
fraud = pd.DataFrame({
    'amount': np.random.exponential(500, n_fraud),
    'time_since_last': np.random.exponential(2, n_fraud),
    'distance_from_home': np.random.exponential(100, n_fraud),
    'num_transactions_day': np.random.poisson(15, n_fraud),
    'merchant_category': np.random.choice([1, 3, 5], n_fraud),
    'is_fraud': np.ones(n_fraud)
})

df = pd.concat([normal, fraud], ignore_index=True).sample(frac=1, random_state=42)

print("Dataset Info:")
print(f"Normal transactions: {(df['is_fraud'] == 0).sum():,}")
print(f"Fraud transactions: {(df['is_fraud'] == 1).sum():,}")
print(f"Fraud ratio: {df['is_fraud'].mean():.4%}")

X = df.drop('is_fraud', axis=1)
y = df['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42, stratify=y)

print(f"\nTrain set - Normal: {(y_train == 0).sum()}, Fraud: {(y_train == 1).sum()}")
print(f"Test set - Normal: {(y_test == 0).sum()}, Fraud: {(y_test == 1).sum()}")
```

### 1. ইমব্যালেন্সড ডেটার সমস্যা
```python
# ইমব্যালেন্সড ডেটায় মডেল
rf_imb = RandomForestClassifier(random_state=42)
rf_imb.fit(X_train, y_train)
y_pred_imb = rf_imb.predict(X_test)

print("\n🔴 Imbalanced Model Performance:")
print(f"Accuracy: {(y_pred_imb == y_test).mean():.4f}")  # Misleading!
print(classification_report(y_test, y_pred_imb, 
                           target_names=['Normal', 'Fraud']))

# কনফিউশন ম্যাট্রিক্স
cm = confusion_matrix(y_test, y_pred_imb)
print(f"\nConfusion Matrix:")
print(f"TN: {cm[0,0]:4d}  FP: {cm[0,1]:4d}")
print(f"FN: {cm[1,0]:4d}  TP: {cm[1,1]:4d}")
print(f"Fraud Detection Rate (TPR): {cm[1,1]/(cm[1,0]+cm[1,1]):.4f}")  # Poor!
```

### 2. রিস্যাম্পলিং টেকনিক: Oversampling
```python
# Random Oversampling
ros = RandomOverSampler(random_state=42)
X_ros, y_ros = ros.fit_resample(X_train, y_train)

print("Random Oversampling:")
print(f"  Normal: {(y_ros == 0).sum()}, Fraud: {(y_ros == 1).sum()}")

# SMOTE (Synthetic Minority Over-sampling Technique)
smote = SMOTE(random_state=42)
X_smote, y_smote = smote.fit_resample(X_train, y_train)

print("SMOTE:")
print(f"  Normal: {(y_smote == 0).sum()}, Fraud: {(y_smote == 1).sum()}")

# SMOTE + Tomek Links
smote_tomek = SMOTETomek(random_state=42)
X_st, y_st = smote_tomek.fit_resample(X_train, y_train)

print("SMOTE + Tomek:")
print(f"  Normal: {(y_st == 0).sum()}, Fraud: {(y_st == 1).sum()}")
```

### 3. রিস্যাম্পলিং টেকনিক: Undersampling
```python
# Random Undersampling
rus = RandomUnderSampler(random_state=42)
X_rus, y_rus = rus.fit_resample(X_train, y_train)

print("Random Undersampling:")
print(f"  Normal: {(y_rus == 0).sum()}, Fraud: {(y_rus == 1).sum()}")

# তুলনা
print(f"\nOriginal train set size: {len(X_train):,}")
print(f"After Oversampling (SMOTE): {len(X_smote):,}")
print(f"After Undersampling: {len(X_rus):,}")
```

### 4. মডেল লেভেল টেকনিক: ক্লাস ওয়েট
```python
# ক্লাস ওয়েট ব্যবহার করে মডেল
rf_weighted = RandomForestClassifier(class_weight='balanced', random_state=42)
rf_weighted.fit(X_train, y_train)
y_pred_weighted = rf_weighted.predict(X_test)

print("\n🟢 Class Weighted Model:")
print(classification_report(y_test, y_pred_weighted, 
                           target_names=['Normal', 'Fraud']))

# কাস্টম ওয়েট
fraud_ratio = y_train.mean()
custom_weights = {0: 1, 1: 1/fraud_ratio}
rf_custom = RandomForestClassifier(class_weight=custom_weights, random_state=42)
rf_custom.fit(X_train, y_train)
y_pred_custom = rf_custom.predict(X_test)

print("Custom Weighted Model:")
print(classification_report(y_test, y_pred_custom,
                           target_names=['Normal', 'Fraud']))
```

### 5. ইমব্যালেন্সড পাইপলাইন
```python
# SMOTE + মডেল পাইপলাইন
smote_pipeline = ImbPipeline([
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(random_state=42))
])

smote_pipeline.fit(X_train, y_train)
y_pred_smote = smote_pipeline.predict(X_test)
y_proba_smote = smote_pipeline.predict_proba(X_test)[:, 1]

print("\n🟢 SMOTE Pipeline:")
print(classification_report(y_test, y_pred_smote,
                           target_names=['Normal', 'Fraud']))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba_smote):.4f}")
```

### 6. মডেল তুলনা
```python
models = {
    'Imbalanced': rf_imb,
    'Class Weight': rf_weighted,
    'SMOTE Pipeline': smote_pipeline
}

results = []
for name, model in models.items():
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = model.predict(X_test)
    
    y_pred = model.predict(X_test)
    
    results.append({
        'Model': name,
        'Accuracy': (y_pred == y_test).mean(),
        'ROC-AUC': roc_auc_score(y_test, y_proba),
        'F1-Score': f1_score(y_test, y_pred),
        'Avg Precision': average_precision_score(y_test, y_proba)
    })

comparison = pd.DataFrame(results)
print("\n📊 Model Comparison:")
print(comparison.to_string(index=False))
```

### ইমব্যালেন্সড ডেটার জন্য সঠিক ইভালুয়েশন মেট্রিক
```python
print("""
✅ For Imbalanced Data, use:
- Precision & Recall (not accuracy)
- F1-Score
- ROC-AUC
- Precision-Recall Curve
- Confusion Matrix

❌ Avoid:
- Accuracy (misleading for imbalanced data)
- Without stratified cross-validation
""")
```

### সারসংক্ষেপ
আজ আমরা ইমব্যালেন্সড ডেটা হ্যান্ডলিং শিখলাম:
- **ওভারস্যাম্পলিং**: SMOTE, RandomOverSampler
- **আন্ডারস্যাম্পলিং**: RandomUnderSampler, Tomek Links
- **ক্লাস ওয়েট**: balanced, custom weights
- **সঠিক ইভালুয়েশন**: ROC-AUC, Precision-Recall, F1

### অনুশীলনী
1. বিভিন্ন সাম্পলিং রেশিও নিয়ে এক্সপেরিমেন্ট করুন
2. ক্লাস ওয়েট অ্যাডজাস্ট করে সেরা কম্বিনেশন খুঁজুন
3. ADASYN (Adaptive Synthetic Sampling) ব্যবহার করে দেখুন
4. ইমব্যালেন্সড ডেটার জন্য থ্রেশহোল্ড মুভিং টেকনিক ইমপ্লিমেন্ট করুন
