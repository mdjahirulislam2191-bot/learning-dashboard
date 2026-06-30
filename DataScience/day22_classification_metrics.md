# Day 22: ক্লাসিফিকেশন মেট্রিক্স — Precision, Recall, F1
## Classification Metrics: Precision, Recall, F1

### ক্লাসিফিকেশন মেট্রিক্সের গুরুত্ব
শুধু Accuracy দিয়ে ক্লাসিফিকেশন মডেলের পারফরম্যান্স মাপা যথেষ্ট নয়। বিশেষ করে ইমব্যালেন্সড ডেটাসেটে Precision, Recall, F1-Score বেশি নির্ভরযোগ্য।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (precision_score, recall_score, f1_score, fbeta_score,
                             classification_report, confusion_matrix, precision_recall_curve,
                             average_precision_score, matthews_corrcoef)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')
```

### বিস্তারিত মেট্রিক্স ডেফিনেশন:
```python
print("\n=== Precision, Recall, F1 এর বিস্তারিত বর্ণনা ===")

# বিভিন্ন সিনারিও
scenarios = [
    ('পারফেক্ট ক্লাসিফায়ার', np.array([[50, 0], [0, 50]])),
    ('ভালো ক্লাসিফায়ার', np.array([[45, 5], [10, 40]])),
    ('সব পজিটিভ প্রেডিক্ট', np.array([[0, 50], [0, 50]])),
    ('সব নেগেটিভ প্রেডিক্ট', np.array([[50, 0], [50, 0]])),
    ('এলোমেলো', np.array([[30, 20], [25, 25]])),
    ('হাই FP (মিথ্যা অ্যালার্ম বেশি)', np.array([[20, 30], [5, 45]])),
    ('হাই FN (মিস বেশি)', np.array([[45, 5], [40, 10]])),
]

print(f"{'সিনারিও':<25} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Accuracy':<12}")
print("=" * 73)

for name, cm in scenarios:
    tn, fp, fn, tp = cm.ravel()
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    acc = (tp + tn) / (tp + tn + fp + fn)
    print(f"{name:<25} {prec:<12.4f} {rec:<12.4f} {f1:<12.4f} {acc:<12.4f}")
```

### প্র্যাকটিক্যাল উদাহরণ: ফ্রড ডিটেকশন:
```python
print("\n=== প্র্যাকটিক্যাল: ফ্রড ডিটেকশন ===")

np.random.seed(42)
n = 5000

# ইমব্যালেন্সড ডেটা (মাত্র ২% ফ্রড)
data = pd.DataFrame({
    'লেনদেন_পরিমাণ': np.random.lognormal(7, 1.5, n),
    'লেনদেন_সময়': np.random.randint(0, 24, n),
    'অ্যাকাউন্ট_বয়স_দিন': np.random.randint(1, 3650, n),
    'পূর্ববর্তী_লেনদেন': np.random.poisson(5, n),
    'দেশ_পরিবর্তন': np.random.choice([0, 1], n, p=[0.95, 0.05]),
})

# ফ্রড লেবেল (মাত্র ২%)
fraud_prob = 0.02
data['ফ্রড'] = np.random.choice([0, 1], n, p=[1-fraud_prob, fraud_prob])

# কিছু প্যাটার্ন যোগ করা
fraud_mask = data['ফ্রড'] == 1
data.loc[fraud_mask, 'লেনদেন_পরিমাণ'] *= np.random.uniform(2, 5, fraud_mask.sum())
data.loc[fraud_mask, 'লেনদেন_সময়'] = np.random.randint(0, 6, fraud_mask.sum())
data.loc[fraud_mask, 'পূর্ববর্তী_লেনদেন'] = np.random.poisson(1, fraud_mask.sum())

print(f"মোট লেনদেন: {len(data)}")
print(f"ফ্রড লেনদেন: {data['ফ্রড'].sum()} ({data['ফ্রড'].mean()*100:.2f}%)")
print(f"নন-ফ্রড: {(data['ফ্রড']==0).sum()}")

X = data.drop('ফ্রড', axis=1)
y = data['ফ্রড']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# লজিস্টিক রিগ্রেশন
lr = LogisticRegression(class_weight='balanced')
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]

# র্যান্ডম ফরেস্ট
rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
y_prob_rf = rf.predict_proba(X_test_scaled)[:, 1]
```

### Precision, Recall, F1 গণনা:
```python
print("\n=== মডেল তুলনা: Precision, Recall, F1 ===")

models = [
    ('লজিস্টিক রিগ্রেশন', y_pred_lr, y_prob_lr),
    ('র্যান্ডম ফরেস্ট', y_pred_rf, y_prob_rf),
]

for name, y_pred, y_prob in models:
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    f2 = fbeta_score(y_test, y_pred, beta=2)
    f05 = fbeta_score(y_test, y_pred, beta=0.5)
    
    print(f"\n{'='*50}")
    print(f"📊 {name}")
    print(f"{'='*50}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"F0.5-Score:{f05:.4f} (Precision কে বেশি গুরুত্ব দেয়)")
    print(f"F2-Score:  {f2:.4f} (Recall কে বেশি গুরুত্ব দেয়)")
    print(f"MCC:       {matthews_corrcoef(y_test, y_pred):.4f}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['নর্মাল', 'ফ্রড'])}")

# কনফিউশন ম্যাট্রিক্স
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for i, (name, y_pred, _) in enumerate(models):
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                xticklabels=['নর্মাল', 'ফ্রড'],
                yticklabels=['নর্মাল', 'ফ্রড'])
    axes[i].set_title(f'{name}\nPrecision={precision_score(y_test, y_pred):.3f}, Recall={recall_score(y_test, y_pred):.3f}, F1={f1_score(y_test, y_pred):.3f}')
    axes[i].set_xlabel('প্রেডিক্টেড')
    axes[i].set_ylabel('প্রকৃত')

plt.tight_layout()
plt.savefig('classification_metrics_comparison.png')
plt.show()
print("ক্লাসিফিকেশন মেট্রিক্স তুলনা সেভ করা হয়েছে!")
```

### F1-Score বোঝা:
```python
print("\n=== F1-Score বিস্তারিত ===")

# F1 হ'ল Precision ও Recall এর হারমোনিক মিন
precisions = np.linspace(0.1, 1.0, 10)
recalls = np.linspace(0.1, 1.0, 10)
P, R = np.meshgrid(precisions, recalls)
F1 = 2 * (P * R) / (P + R + 1e-10)

# F1 বনাম অ্যারিথমেটিক মিন
print("Precision vs Recall → F1 (হারমোনিক মিন) vs অ্যারিথমেটিক মিন:")
print(f"{'Precision':<12} {'Recall':<12} {'F1':<12} {'অ্যারিথমেটিক মিন':<20}")
print("-" * 56)
for p, r in [(0.9, 0.9), (0.9, 0.5), (0.5, 0.9), (0.5, 0.5), (0.9, 0.1), (1.0, 0.0)]:
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
    am = (p + r) / 2
    print(f"{p:<12.2f} {r:<12.2f} {f1:<12.4f} {am:<20.4f}")

print("\n📌 F1 = 2 * (P*R) / (P+R)")
print("  → হারমোনিক মিন: ছোট ভ্যালুকে বেশি পেনাল্টাইজ করে")
print("  → Precision=0.9, Recall=0.1: F1=0.18 (অ্যারিথমেটিক=0.5)")
print("  → F1 ছোট ভ্যালুটি ধরিয়ে দেয়!")
```

### F-Beta Score:
```python
print("\n=== F-Beta Score ===")

def f_beta(beta, precision, recall):
    """F-Beta Score গণনা"""
    beta_sq = beta ** 2
    return (1 + beta_sq) * (precision * recall) / (beta_sq * precision + recall)

print("F-Beta Score (β নিয়ন্ত্রণ করে Precision vs Recall গুরুত্ব):")
print(f"{'β':<10} {'নাম':<15} {'Precision গুরুত্ব':<20} {'Recall গুরুত্ব':<20}")
print("-" * 65)
betas_info = [(0.5, 'F0.5', '৫ গুণ বেশি', 'সমান'), 
              (1.0, 'F1', 'সমান', 'সমান'),
              (2.0, 'F2', 'সমান', '৫ গুণ বেশি')]

for b, name, p_imp, r_imp in betas_info:
    print(f"{b:<10.1f} {name:<15} {p_imp:<20} {r_imp:<20}")

# উদাহরণ
prec_ex = 0.95
rec_ex = 0.60
print(f"\nউদাহরণ: Precision={prec_ex}, Recall={rec_ex}")
for b, name, _, _ in betas_info:
    fb = f_beta(b, prec_ex, rec_ex)
    print(f"  {name} = {fb:.4f}")
```

### Precision-Recall Trade-off:
```python
print("\n=== Precision-Recall Trade-off ===")

# বিভিন্ন থ্রেশহোল্ডের প্রভাব
thresholds = np.linspace(0.05, 0.95, 50)
precision_th = []
recall_th = []
f1_th = []

for th in thresholds:
    pred = (y_prob_lr >= th).astype(int)
    precision_th.append(precision_score(y_test, pred, zero_division=0))
    recall_th.append(recall_score(y_test, pred, zero_division=0))
    f1_th.append(f1_score(y_test, pred, zero_division=0))

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(thresholds, precision_th, 'b-', linewidth=2, label='Precision')
plt.plot(thresholds, recall_th, 'r-', linewidth=2, label='Recall')
plt.plot(thresholds, f1_th, 'g-', linewidth=2, label='F1')
plt.axvline(0.5, color='gray', linestyle='--', alpha=0.5, label='Default (0.5)')
plt.xlabel('থ্রেশহোল্ড')
plt.ylabel('স্কোর')
plt.title('Precision-Recall Trade-off')
plt.legend()
plt.grid(alpha=0.3)

# Precision vs Recall সরাসরি
plt.subplot(1, 2, 2)
plt.plot(recall_th, precision_th, 'b-', linewidth=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision vs Recall Curve')
plt.grid(alpha=0.3)
# বেস্ট F1 পয়েন্ট চিহ্নিত
best_idx = np.argmax(f1_th)
plt.scatter(recall_th[best_idx], precision_th[best_idx], c='red', s=100, zorder=5, 
            label=f'সেরা F1={f1_th[best_idx]:.3f} (থ্রেশহোল্ড={thresholds[best_idx]:.2f})')
plt.legend()

plt.tight_layout()
plt.savefig('precision_recall_tradeoff.png')
plt.show()
print("Precision-Recall Trade-off গ্রাফ সেভ করা হয়েছে!")

best_th = thresholds[np.argmax(f1_th)]
print(f"\nসেরা থ্রেশহোল্ড (সর্বোচ্চ F1): {best_th:.2f}")
print(f"  Precision: {precision_th[np.argmax(f1_th)]:.4f}")
print(f"  Recall: {recall_th[np.argmax(f1_th)]:.4f}")
print(f"  F1: {f1_th[np.argmax(f1_th)]:.4f}")
```

### Precision-Recall Curve:
```python
print("\n=== Precision-Recall Curve ===")

# দুই মডেলের PR Curve তুলনা
prec_lr, rec_lr, _ = precision_recall_curve(y_test, y_prob_lr)
prec_rf, rec_rf, _ = precision_recall_curve(y_test, y_prob_rf)

ap_lr = average_precision_score(y_test, y_prob_lr)
ap_rf = average_precision_score(y_test, y_prob_rf)

plt.figure(figsize=(10, 6))
plt.plot(rec_lr, prec_lr, 'b-', linewidth=2, label=f'LR (AP={ap_lr:.4f})')
plt.plot(rec_rf, prec_rf, 'r-', linewidth=2, label=f'RF (AP={ap_rf:.4f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve: LR vs RF')
plt.legend(loc='lower left')
plt.grid(alpha=0.3)
plt.savefig('pr_curve_comparison.png')
plt.show()
print("PR Curve তুলনা সেভ করা হয়েছে!")
```

### ক্লাস ইমব্যালেন্স হ্যান্ডলিং:
```python
print("\n=== ক্লাস ইমব্যালেন্স হ্যান্ডলিং ===")

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import f1_score

# বিভিন্ন ক্লাস ওয়েট
weights = [
    ('Default (balanced)', 'balanced'),
    ('No weight', None),
    ('Custom: {0:1, 1:5}', {0: 1, 1: 5}),
    ('Custom: {0:1, 1:10}', {0: 1, 1: 10}),
    ('Custom: {0:1, 1:20}', {0: 1, 1: 20}),
]

print(f"{'ওয়েটিং':<25} {'Precision':<12} {'Recall':<12} {'F1':<12} {'ফ্রড ডিটেক্টেড':<15}")
print("=" * 76)

for name, cw in weights:
    model = LogisticRegression(class_weight=cw, max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    
    prec = precision_score(y_test, pred, zero_division=0)
    rec = recall_score(y_test, pred, zero_division=0)
    f1 = f1_score(y_test, pred, zero_division=0)
    fraud_detected = pred.sum()
    
    print(f"{name:<25} {prec:<12.4f} {rec:<12.4f} {f1:<12.4f} {fraud_detected:<15}")

print("\n📌 ব্যালেন্সড ওয়েট ইমব্যালেন্সড ডেটায় ফ্রড ডিটেকশন বাড়ায়")
print("📌 Precision-Recall Trade-off: একটির সাথে অন্যটির বদল হয়")
```

### মাল্টি-ক্লাস মেট্রিক্স:
```python
print("\n=== মাল্টি-ক্লাস ক্লাসিফিকেশন মেট্রিক্স ===")

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# থ্রি-ক্লাস ডেটা
np.random.seed(42)
y_true_multi = np.random.choice(['লো', 'মিডিয়াম', 'হাই'], 500, p=[0.5, 0.3, 0.2])
y_pred_multi = np.random.choice(['লো', 'মিডিয়াম', 'হাই'], 500, p=[0.4, 0.4, 0.2])

print("মাল্টি-ক্লাস ক্লাসিফিকেশন রিপোর্ট:")
print(classification_report(y_true_multi, y_pred_multi))

# মাইক্রো, ম্যাক্রো, ওয়েটেড
prec_micro, rec_micro, f1_micro, _ = precision_recall_fscore_support(
    y_true_multi, y_pred_multi, average='micro')
prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(
    y_true_multi, y_pred_multi, average='macro')
prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(
    y_true_multi, y_pred_multi, average='weighted')

print(f"\nএভারেজিং মেথডের প্রভাব:")
print(f"{'মেথড':<15} {'Precision':<12} {'Recall':<12} {'F1':<12}")
print("-" * 51)
print(f"{'Micro':<15} {prec_micro:<12.4f} {rec_micro:<12.4f} {f1_micro:<12.4f}")
print(f"{'Macro':<15} {prec_macro:<12.4f} {rec_macro:<12.4f} {f1_macro:<12.4f}")
print(f"{'Weighted':<15} {prec_weighted:<12.4f} {rec_weighted:<12.4f} {f1_weighted:<12.4f}")
```

### MCC (Matthews Correlation Coefficient):
```python
print("\n=== MCC — Matthews Correlation Coefficient ===")

mcc_lr = matthews_corrcoef(y_test, y_pred_lr)
mcc_rf = matthews_corrcoef(y_test, y_pred_rf)

print(f"MCC (LR): {mcc_lr:.4f}")
print(f"MCC (RF): {mcc_rf:.4f}")
print(f"\nMCC = -1 থেকে +1 পর্যন্ত হয়:")
print(f"  +1: পারফেক্ট প্রেডিকশন")
print(f"   0: র্যান্ডম")
print(f"  -1: সম্পূর্ণ ভুল")
print(f"\nইমব্যালেন্সড ডেটায় MCC বেশি নির্ভরযোগ্য!")
```

### মেট্রিক্স সিলেকশন গাইড:
```python
print("\n=== মেট্রিক্স সিলেকশন গাইড ===")

guide = pd.DataFrame({
    'মেট্রিক': ['Precision', 'Recall (Sensitivity)', 'F1-Score', 'F2-Score', 
                'F0.5-Score', 'Specificity', 'MCC'],
    'প্রশ্নের উত্তর দেয়': [
        'পজিটিভ প্রেডিক্ট কতটা নির্ভরযোগ্য?',
        'প্রকৃত পজিটিভের কতটা শনাক্ত করেছি?',
        'Precision ও Recall এর ব্যালেন্স কেমন?',
        'Recall কি বেশি গুরুত্বপূর্ণ?',
        'Precision কি বেশি গুরুত্বপূর্ণ?',
        'নেগেটিভ কতটা সঠিকভাবে শনাক্ত করেছি?',
        'সামগ্রিক কোরিলেশন কেমন?'
    ],
    'উদাহরণ ব্যবহার': [
        'স্প্যাম ফিল্টার (ভালো মেইল যাতে স্প্যাম না হয়)',
        'ক্যান্সার ডিটেকশন (রোগী মিস না করা)',
        'ইমব্যালেন্সড ডেটাসেট',
        'ফ্রড ডিটেকশন (ফ্রড মিস না করা)',
        'প্রোডাক্ট রিকমেন্ডেশন',
        'নেগেটিভ ক্লাসের নির্ভুলতা মাপা',
        'যেকোনো ইমব্যালেন্সড ডেটা'
    ]
})
print(guide.to_string(index=False))
```

### সারাংশ:
```python
print("\n=== সারাংশ ===")

print("""
📊 Precision (নির্ভুলতা):
   TP/(TP+FP) — পজিটিভ প্রেডিকশনের কতটা সঠিক
   স্প্যাম ডিটেকশনে গুরুত্বপূর্ণ (ভালো মেইল যাতে স্প্যাম না হয়)

📊 Recall (সংবেদনশীলতা):
   TP/(TP+FN) — প্রকৃত পজিটিভের কতটা শনাক্ত
   ক্যান্সার ডিটেকশনে গুরুত্বপূর্ণ (রোগী মিস না করা)

📊 F1-Score:
   2×P×R/(P+R) — Precision ও Recall এর হারমোনিক মিন
   ইমব্যালেন্সড ডেটায় Accuracy এর চেয়ে ভালো মেট্রিক

📊 F-Beta:
   Beta>1: Recall বেশি গুরুত্ব (F2)
   Beta<1: Precision বেশি গুরুত্ব (F0.5)

📊 ক্লাস ইমব্যালেন্স:
   Accuracy বিভ্রান্তিকর — Precision, Recall, F1 ব্যবহার করুন
   Class Weight, SMOTE, রিস্যাম্পলিং টেকনিক ব্যবহার করুন
""")
```

### সারাংশ:
- **Precision**: নির্ভুলতা — পজিটিভ প্রেডিকশন কতটা সঠিক
- **Recall**: সংবেদনশীলতা — প্রকৃত পজিটিভ কতটা ধরা পড়েছে
- **F1-Score**: Precision ও Recall এর ব্যালেন্সড মেট্রিক
- **F-Beta**: β দিয়ে Precision/Recall এর গুরুত্ব নিয়ন্ত্রণ
- **MCC**: ইমব্যালেন্সড ডেটার জন্য সবচেয়ে নির্ভরযোগ্য মেট্রিক
- **Trade-off**: Precision বাড়ালে Recall কমে, এবং উল্টোটাও সত্য
- মেট্রিক নির্বাচন ব্যবসায়িক প্রয়োজনের উপর নির্ভর করে