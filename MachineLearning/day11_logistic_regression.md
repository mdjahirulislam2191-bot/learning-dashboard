# Day 11: লজিস্টিক রিগ্রেশন
## Logistic Regression

### লজিস্টিক রিগ্রেশন কি?
বাইনারি ক্লাসিফিকেশনের জন্য ব্যবহৃত হয়। Sigmoid ফাংশন ব্যবহার করে আউটপুটকে 0-1 এর মধ্যে স্কোয়েজ করে।

**Sigmoid:** P(y=1) = 1 / (1 + e^(-z)), যেখানে z = β₀ + β₁x₁ + ...

### ফাইন্যান্স উদাহরণ: ক্রেডিট ডিফল্ট প্রেডিকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, 
                             classification_report, roc_curve)
import seaborn as sns

# ক্রেডিট ডিফল্ট ডেটা
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'credit_utilization': np.random.uniform(0, 1, n),
    'loan_to_income': np.random.uniform(0, 3, n),
    'payment_history': np.random.uniform(0, 10, n),  # 0=poor, 10=excellent
    'credit_age_years': np.random.exponential(10, n),
    'num_late_payments': np.random.poisson(1, n),
    'income_stability': np.random.uniform(0, 1, n)
})

# টার্গেট: ডিফল্ট (0=No, 1=Yes)
z = (-3 + 2*data['credit_utilization'] + 1.5*data['loan_to_income'] 
     - 0.8*data['payment_history'] - 0.3*data['credit_age_years']
     + 0.5*data['num_late_payments'] - 1.5*data['income_stability']
     + np.random.randn(n) * 0.5)

data['default'] = (1 / (1 + np.exp(-z)) > 0.3).astype(int)

print("📊 ডেটা ওভারভিউ:")
print(data.head())
print(f"\nDefault Rate: {data['default'].mean():.2%}")
```

### মডেল ট্রেইনিং
```python
X = data.drop('default', axis=1)
y = data['default']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# লজিস্টিক রিগ্রেশন
model = LogisticRegression(penalty='l2', C=1.0, max_iter=1000)
model.fit(X_train_scaled, y_train)

# কোএফিসিয়েন্টস
coeff_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0],
    'Odds_Ratio': np.exp(model.coef_[0])
}).sort_values('Odds_Ratio', ascending=False)

print("📋 মডেল কোএফিসিয়েন্টস:")
print(coeff_df.to_string(index=False))
```

### Probabilities এবং Threshold
```python
y_prob = model.predict_proba(X_test_scaled)[:, 1]
y_pred = model.predict(X_test_scaled)

print("\n🎯 Probability রেঞ্জ:")
print(f"Min: {y_prob.min():.4f}, Max: {y_prob.max():.4f}")
print(f"Mean: {y_prob.mean():.4f}")

# বিভিন্ন থ্রেশহোল্ড টেস্ট
thresholds = [0.1, 0.2, 0.3, 0.5, 0.7]
for thresh in thresholds:
    preds = (y_prob >= thresh).astype(int)
    print(f"\nThreshold={thresh:.1f}:")
    print(f"  Precision: {precision_score(y_test, preds):.4f}")
    print(f"  Recall:    {recall_score(y_test, preds):.4f}")
    print(f"  F1:        {f1_score(y_test, preds):.4f}")
```

### ROC Curve
```python
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = roc_auc_score(y_test, y_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, 'b-', label=f'ROC (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'r--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - ক্রেডিট ডিফল্ট প্রেডিকশন')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Best threshold
j_scores = tpr - fpr
best_idx = np.argmax(j_scores)
best_threshold = thresholds[best_idx]
print(f"\n🎯 Optimal Threshold (Youden's J): {best_threshold:.4f}")
```

### Model Evaluation
```python
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['No Default', 'Default']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Default', 'Default'],
            yticklabels=['No Default', 'Default'])
plt.title('Confusion Matrix')
plt.show()
```

### সারসংক্ষেপ
লজিস্টিক রিগ্রেশন বাইনারি ক্লাসিফিকেশনের জন্য শক্তিশালী। Probabilities আউটপুট দেয় যা ব্যবসায়িক সিদ্ধান্তের জন্য ব্যবহার করা যায়। ফাইন্যান্সে ক্রেডিট রিস্ক, ফ্রড ডিটেকশন, এবং মার্কেটিং অ্যানালাইসিসে ব্যাপকভাবে ব্যবহৃত হয়।