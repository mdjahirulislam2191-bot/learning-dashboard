# Day 49: ফেয়ারনেস ইন ML
## Fairness in Machine Learning

### ফেয়ারনেস কি?
মেশিন লার্নিং মডেলে ফেয়ারনেস হল নিশ্চিত করা যে মডেলের সিদ্ধান্ত কোনো নির্দিষ্ট গ্রুপ বা ব্যক্তির প্রতি পক্ষপাতিত্ব (bias) না দেখায়।

### বায়াসের উৎস
1. **ডেটা বায়াস**: ট্রেনিং ডেটা যদি ভারসাম্যহীন হয়
2. **লেবেল বায়াস**: লেবেল যদি পক্ষপাতদুষ্ট হয়
3. **ফিচার বায়াস**: ফিচার যদি স্পর্শকাতর তথ্য ধারণ করে
4. **অ্যালগরিদমিক বায়াস**: অ্যালগরিদমের ডিজাইনজনিত

### ফেয়ারনেস মেট্রিক্স

```python
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

def demographic_parity(y_true, y_pred, sensitive_attr):
    """
    Demographic Parity: প্রত্যেক গ্রুপের পজিটিভ রেট সমান হওয়া উচিত
    """
    groups = np.unique(sensitive_attr)
    rates = {}
    for group in groups:
        mask = sensitive_attr == group
        rates[group] = y_pred[mask].mean()
    return rates

def equal_opportunity(y_true, y_pred, sensitive_attr):
    """
    Equal Opportunity: প্রত্যেক গ্রুপের True Positive Rate সমান হওয়া উচিত
    """
    groups = np.unique(sensitive_attr)
    tpr = {}
    for group in groups:
        mask = (sensitive_attr == group) & (y_true == 1)
        if mask.sum() > 0:
            tpr[group] = (y_pred[mask] == 1).mean()
        else:
            tpr[group] = 0
    return tpr

def equalized_odds(y_true, y_pred, sensitive_attr):
    """
    Equalized Odds: সকল গ্রুপের TPR এবং FPR সমান হওয়া উচিত
    """
    groups = np.unique(sensitive_attr)
    metrics = {}
    for group in groups:
        mask = sensitive_attr == group
        tn, fp, fn, tp = confusion_matrix(
            y_true[mask], y_pred[mask]
        ).ravel()
        metrics[group] = {
            'tpr': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'fpr': fp / (fp + tn) if (fp + tn) > 0 else 0
        }
    return metrics
```

### ফেয়ারনেস চেক করার উদাহরণ

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# সিমুলেটেড ডেটা
np.random.seed(42)
n_samples = 1000

# স্পর্শকাতর অ্যাট্রিবিউট (যেমন: লিঙ্গ)
sensitive = np.random.binomial(1, 0.5, n_samples)

# কিছু বায়াসড ফিচার
X = np.column_stack([
    np.random.randn(n_samples),  # ফিচার 1
    sensitive * 0.3 + np.random.randn(n_samples) * 0.7,  # ফিচার 2
])
y = (X[:, 0] + X[:, 1] + np.random.randn(n_samples) * 0.5 > 0).astype(int)

# ট্রেইন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test, sens_train, sens_test = train_test_split(
    X, y, sensitive, test_size=0.3, random_state=42
)

# মডেল ট্রেইন
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ফেয়ারনেস চেক
print("Demographic Parity:")
dp = demographic_parity(y_test, y_pred, sens_test)
for group, rate in dp.items():
    print(f"  Group {group}: {rate:.3f}")

print("\nEqual Opportunity:")
eo = equal_opportunity(y_test, y_pred, sens_test)
for group, tpr in eo.items():
    print(f"  Group {group} TPR: {tpr:.3f}")

print("\nEqualized Odds:")
eo_metrics = equalized_odds(y_test, y_pred, sens_test)
for group, m in eo_metrics.items():
    print(f"  Group {group}: TPR={m['tpr']:.3f}, FPR={m['fpr']:.3f}")
```

### ফেয়ারনেস ইমপ্রুভ করার টেকনিক

#### 1. প্রি-প্রসেসিং (ডেটা লেভেল)
```python
from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing

# রিওয়েটিং: গ্রুপগুলোর গুরুত্ব সমান করা
def reweight_data(X, y, sensitive_attr):
    """ডেটা রিওয়েটিং করে ফেয়ারনেস উন্নত করা"""
    weights = np.ones(len(y))
    for group in np.unique(sensitive_attr):
        mask = sensitive_attr == group
        group_frac = mask.mean()
        positive_frac = (y[mask] == 1).mean()
        # ওয়েট ক্যালকুলেশন
        weights[mask] = 1.0 / (group_frac * positive_frac)
    return weights
```

#### 2. ইন-প্রসেসিং (মডেল লেভেল)
```python
from sklearn.linear_model import LogisticRegression

class FairLogisticRegression:
    """ফেয়ারনেস কনস্ট্রেইন্ট সহ লজিস্টিক রিগ্রেশন"""
    def __init__(self, lambda_fairness=0.1):
        self.lambda_fairness = lambda_fairness
        self.model = LogisticRegression()
    
    def fit(self, X, y, sensitive_attr):
        self.model.fit(X, y)
        # ফেয়ারনেস লস অ্যাড করা
        preds = self.model.predict(X)
        dp_diff = self._demographic_parity_diff(preds, sensitive_attr)
        return dp_diff
    
    def _demographic_parity_diff(self, preds, sensitive_attr):
        groups = np.unique(sensitive_attr)
        rates = [preds[sensitive_attr == g].mean() 
                 for g in groups]
        return max(rates) - min(rates)
```

#### 3. পোস্ট-প্রসেসিং (আউটপুট লেভেল)
```python
def reject_option_based_classification(y_prob, sensitive_attr, 
                                      threshold=0.5, 
                                      rejection_region=0.1):
    """সন্দেহজনক প্রেডিকশন রিজেক্ট করা"""
    predictions = np.copy(y_prob)
    
    # রিজেকশন রিজিয়ন
    uncertain = (y_prob > threshold - rejection_region) & \
                (y_prob < threshold + rejection_region)
    
    predictions[uncertain] = -1  # রিজেক্টেড
    predictions[~uncertain] = (y_prob[~uncertain] > threshold).astype(int)
    
    return predictions
```

### গুরুত্বপূর্ণ পয়েন্ট
1. ফেয়ারনেস এক-আকার-সব-এর-জন্য-উপযোগী নয়
2. ট্রেড-অফ: ফেয়ারনেস বনাম অ্যাকুরেসি
3. ডোমেন অনুযায়ী ফেয়ারনেস সংজ্ঞা পরিবর্তিত হয়
4. নিয়মিত অডিটিং প্রয়োজন
5. ট্রান্সপারেন্সি গুরুত্বপূর্ণ

### বেস্ট প্র্যাকটিস
- ডেটা কালেকশনে বৈচিত্র্য নিশ্চিত করুন
- স্পর্শকাতর ফিচার চিহ্নিত করুন
- ফেয়ারনেস মেট্রিক্স নিয়মিত মনিটর করুন
- মডেল ডিসিশন ডকুমেন্ট করুন
- স্টেকহোল্ডারদের সাথে আলোচনা করুন