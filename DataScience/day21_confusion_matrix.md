# Day 21: কনফিউশন ম্যাট্রিক্স ও ROC
## Confusion Matrix & ROC

### কনফিউশন ম্যাট্রিক্স কী?
কনফিউশন ম্যাট্রিক্স একটি টেবিল যা ক্লাসিফিকেশন মডেলের পারফরম্যান্স সংক্ষেপে দেখায়। এটি প্রকৃত ও প্রেডিক্টেড ভ্যালুর তুলনা করে চারটি ক্যাটেগরিতে ভাগ করে।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, classification_report, roc_curve, auc,
                             roc_auc_score, precision_recall_curve, average_precision_score)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.multiclass import OneVsRestClassifier
import warnings
warnings.filterwarnings('ignore')

# ডেটাসেট তৈরি
np.random.seed(42)
n = 1000

# হেলথ ডেটা: ডায়াবেটিস প্রেডিকশন
df = pd.DataFrame({
    'বয়স': np.random.randint(20, 80, n),
    'বিএমআই': np.random.uniform(18, 40, n),
    'গ্লুকোজ': np.random.normal(120, 30, n),
    'ব্লাডপ্রেসার': np.random.normal(130, 20, n),
    'ইনসুলিন': np.random.normal(80, 40, n),
    'ব্যায়াম_ঘন্টা': np.random.uniform(0, 10, n),
})

# ডায়াবেটিস রিস্ক (সিমুলেটেড)
risk = (-5 + 0.03 * df['বয়স'] + 0.08 * df['বিএমআই'] + 
        0.02 * df['গ্লুকোজ'] + 0.01 * df['ব্লাডপ্রেসर'] - 
        0.3 * df['ব্যায়াম_ঘন্টা'] + np.random.normal(0, 1, n))
prob = 1 / (1 + np.exp(-risk))
df['ডায়াবেটিস'] = np.random.binomial(1, prob)

print("=== ডায়াবেটিস ডেটাসেট ===")
print(f"ডায়াবেটিস রেট: {df['ডায়াবেটিস'].mean()*100:.2f}%")
print(f"মোট: {len(df)}")

X = df.drop('ডায়াবেটিস', axis=1)
y = df['ডায়াবেটيس']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)
y_prob = model.predict_proba(X_test_scaled)[:, 1]
y_pred = model.predict(X_test_scaled)
```

### কনফিউশন ম্যাট্রিক্স বেসিক:
```python
print("\n=== কনফিউশন ম্যাট্রিক্স ===")

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print("কনফিউশন ম্যাট্রিক্স:")
print("=" * 50)
print(f"{'':<20} {'প্রেডিক্টেড':>25}")
print(f"{'':<20} {'না':>10} {'হ্যাঁ':>10}")
print("-" * 50)
print(f"{'প্রকৃত':<10} {'না':>10} {tn:>10} {fp:>10}")
print(f"{'':<10} {'হ্যাঁ':>10} {fn:>10} {tp:>10}")
print("=" * 50)

# ভিজুয়ালাইজেশন
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['না (০)', 'হ্যাঁ (১)'],
            yticklabels=['না (০)', 'হ্যাঁ (১)'])
plt.xlabel('প্রেডিক্টেড')
plt.ylabel('প্রকৃত')
plt.title('কনফিউশন ম্যাট্রিক্স')
plt.savefig('confusion_matrix.png')
plt.show()
print("\nকনফিউশন ম্যাট্রিক্স সেভ করা হয়েছে!")
```

### কনফিউশন ম্যাট্রিক্সের উপাদান:
```python
print("\n=== কনফিউশন ম্যাট্রিক্সের উপাদান ===")

print(f"TP (True Positive): {tp}")
print(f"  → প্রকৃত ১, মডেলও ১ প্রেডিক্ট করেছে ✅")
print(f"TN (True Negative): {tn}")
print(f"  → প্রকৃত ০, মডেলও ০ প্রেডিক্ট করেছে ✅")
print(f"FP (False Positive): {fp}")
print(f"  → প্রকৃত ০, কিন্তু মডেল ১ প্রেডিক্ট করেছে ❌ (মিথ্যা অ্যালার্ম)")
print(f"FN (False Negative): {fn}")
print(f"  → প্রকৃত ১, কিন্তু মডেল ০ প্রেডিক্ট করেছে ❌ (মিস)")
```

### কনফিউশন ম্যাট্রিক্স থেকে মেট্রিক্স:
```python
print("\n=== কনফিউশন ম্যাট্রিক্স থেকে মেট্রিক্স ===")

# Accuracy
accuracy = (tp + tn) / (tp + tn + fp + fn)
print(f"Accuracy: {accuracy:.4f}")
print(f"  → (TP+TN)/(TP+TN+FP+FN) = ({tp}+{tn})/({tp}+{tn}+{fp}+{fn}) = {accuracy:.4f}")

# Precision
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
print(f"\nPrecision: {precision:.4f}")
print(f"  → TP/(TP+FP) = {tp}/({tp}+{fp}) = {precision:.4f}")
print(f"  → 'ডায়াবেটিস' বললে কতবার সঠিক?")

# Recall (Sensitivity)
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
print(f"\nRecall (Sensitivity): {recall:.4f}")
print(f"  → TP/(TP+FN) = {tp}/({tp}+{fn}) = {recall:.4f}")
print(f"  → প্রকৃত ডায়াবেটিস রোগীর কতটুকু চিহ্নিত করেছি?")

# Specificity
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
print(f"\nSpecificity: {specificity:.4f}")
print(f"  → TN/(TN+FP) = {tn}/({tn}+{fp}) = {specificity:.4f}")
print(f"  → সুস্থ ব্যক্তিকে কতটুকু সঠিকভাবে চিহ্নিত করেছি?")

# F1 Score
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
print(f"\nF1 Score: {f1:.4f}")
print(f"  → 2*(P*R)/(P+R) = {f1:.4f}")
print(f"  → Precision ও Recall এর হারমোনিক মিন")
```

### থ্রেশহোল্ড অ্যাডজাস্টমেন্ট:
```python
print("\n=== থ্রেশহোল্ড অ্যাডজাস্টমেন্ট ===")

thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
print(f"{'থ্রেশহোল্ড':<12} {'TP':<6} {'TN':<6} {'FP':<6} {'FN':<6} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1':<10}")
print("-" * 80)

for th in thresholds:
    pred = (y_prob >= th).astype(int)
    cm_t = confusion_matrix(y_test, pred)
    tn_t, fp_t, fn_t, tp_t = cm_t.ravel()
    acc_t = (tp_t + tn_t) / (tp_t + tn_t + fp_t + fn_t)
    prec_t = tp_t / (tp_t + fp_t) if (tp_t + fp_t) > 0 else 0
    rec_t = tp_t / (tp_t + fn_t) if (tp_t + fn_t) > 0 else 0
    f1_t = 2 * prec_t * rec_t / (prec_t + rec_t) if (prec_t + rec_t) > 0 else 0
    print(f"{th:<12.1f} {tp_t:<6} {tn_t:<6} {fp_t:<6} {fn_t:<6} {acc_t:<10.4f} {prec_t:<10.4f} {rec_t:<10.4f} {f1_t:<10.4f}")

print("\n📌 নোট:")
print("  • থ্রেশহোল্ড কমালে Recall বাড়ে, Precision কমে")
print("  • থ্রেশহোল্ড বাড়ালে Precision বাড়ে, Recall কমে")
print("  • ডায়াবেটিসের মতো রোগে Recall বেশি গুরুত্বপূর্ণ (মিস না করার জন্য)")
print("  • স্প্যাম ডিটেকশনে Precision বেশি গুরুত্বপূর্ণ (ভালো মেইল স্প্যাম না হওয়ার জন্য)")
```

### ROC Curve (Receiver Operating Characteristic):
```python
print("\n=== ROC Curve ===")

fpr, tpr, roc_thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

print(f"AUC: {roc_auc:.4f}")
print(f"\nবিভিন্ন থ্রেশহোল্ডে TPR ও FPR:")
print(f"{'থ্রেশহোল্ড':<12} {'FPR':<10} {'TPR (Recall)':<15}")
print("-" * 37)
for i in range(0, len(roc_thresholds), max(1, len(roc_thresholds)//10)):
    print(f"{roc_thresholds[i]:<12.4f} {fpr[i]:<10.4f} {tpr[i]:<15.4f}")

# AUC ইন্টারপ্রিটেশন
print(f"\nAUC ইন্টারপ্রিটেশন:")
if roc_auc >= 0.9:
    print("  🏆 AUC = {:.4f}: অসাধারণ ক্লাসিফায়ার!".format(roc_auc))
elif roc_auc >= 0.8:
    print("  🌟 AUC = {:.4f}: চমৎকার ক্লাসিফায়ার!".format(roc_auc))
elif roc_auc >= 0.7:
    print("  👍 AUC = {:.4f}: ভালো ক্লাসিফায়ার".format(roc_auc))
elif roc_auc >= 0.6:
    print("  🤷 AUC = {:.4f}: মোটামুটি ক্লাসিফায়ার".format(roc_auc))
else:
    print("  ❌ AUC = {:.4f}: দুর্বল ক্লাসিফায়ার".format(roc_auc))

# ROC প্লট
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(fpr, tpr, 'b-', linewidth=2, label=f'ROC Curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'r--', linewidth=2, label='র্যান্ডম (AUC = 0.5)')
plt.fill_between(fpr, tpr, alpha=0.2, color='blue')
plt.xlabel('False Positive Rate (FPR)', fontsize=12)
plt.ylabel('True Positive Rate (TPR)', fontsize=12)
plt.title('ROC Curve', fontsize=14)
plt.legend(loc='lower right')
plt.grid(alpha=0.3)

# বিভিন্ন থ্রেশহোল্ড পয়েন্ট দেখানো
plt.subplot(1, 2, 2)
plt.plot(fpr, tpr, 'b-', linewidth=2)
plt.scatter(fpr[::20], tpr[::20], c='red', s=30, zorder=5)
for i in range(0, len(roc_thresholds), max(1, len(roc_thresholds)//10)):
    plt.annotate(f'{roc_thresholds[i]:.2f}', (fpr[i], tpr[i]), 
                 xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.plot([0, 1], [0, 1], 'r--')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC Curve with Thresholds')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('roc_curve_detailed.png')
plt.show()
print("ROC Curve সেভ করা হয়েছে!")
```

### Precision-Recall Curve:
```python
print("\n=== Precision-Recall Curve ===")

precision_vals, recall_vals, pr_thresholds = precision_recall_curve(y_test, y_prob)
avg_precision = average_precision_score(y_test, y_prob)

print(f"Average Precision: {avg_precision:.4f}")

# PR Curve প্লট
plt.figure(figsize=(10, 6))
plt.plot(recall_vals, precision_vals, 'g-', linewidth=2, label=f'PR Curve (AP = {avg_precision:.4f})')
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision-Recall Curve', fontsize=14)
plt.legend(loc='upper right')
plt.grid(alpha=0.3)
plt.savefig('pr_curve.png')
plt.show()
print("PR Curve সেভ করা হয়েছে!")

print(f"\nPrecision-Recall Curve বিশ্লেষণ:")
print(f"  Average Precision: {avg_precision:.4f}")
print(f"  Precision (থ্রেশহোল্ড ০.৫ এ): {precision:.4f}")
print(f"  Recall (থ্রেশহোল্ড ০.৫ এ): {recall:.4f}")
```

### গেইন ও লিফ্ট চার্ট:
```python
print("\n=== গেইন ও লিফ্ট চার্ট ===")

# প্রোবাবিলিটি অনুযায়ী সাজানো
sorted_indices = np.argsort(y_prob)[::-1]
sorted_y = y_test.values[sorted_indices]
sorted_prob = y_prob[sorted_indices]

# কিউমুলেটিভ গেইন
cumulative_gain = np.cumsum(sorted_y) / np.sum(sorted_y)
baseline = np.arange(1, len(sorted_y) + 1) / len(sorted_y)
lift = cumulative_gain / baseline

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(baseline * 100, cumulative_gain * 100, 'b-', linewidth=2, label='মডেল')
plt.plot([0, 100], [0, 100], 'r--', label='র্যান্ডম')
plt.xlabel('% পপুলেশন')
plt.ylabel('% পজিটিভ ক্যাপচারড')
plt.title('কিউমুলেটিভ গেইন চার্ট')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(baseline * 100, lift, 'b-', linewidth=2)
plt.axhline(y=1, color='r', linestyle='--', label='বেসলাইন')
plt.xlabel('% পপুলেশন')
plt.ylabel('লিফ্ট')
plt.title('লিফ্ট চার্ট')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('gain_lift_chart.png')
plt.show()
print("গেইন ও লিফ্ট চার্ট সেভ করা হয়েছে!")
```

### মাল্টি-ক্লাস কনফিউশন ম্যাট্রিক্স:
```python
print("\n=== মাল্টি-ক্লাস কনফিউশন ম্যাট্রিক্স ===")

# থ্রি-ক্লাস ডেটা
np.random.seed(42)
y_true_3 = np.random.choice([0, 1, 2], size=100)
y_pred_3 = np.random.choice([0, 1, 2], size=100,
                            p=[0.6, 0.3, 0.1])  # কিছু বায়াস

cm_3 = confusion_matrix(y_true_3, y_pred_3)
print("মাল্টি-ক্লাস কনফিউশন ম্যাট্রিক্স:")
print(cm_3)

plt.figure(figsize=(8, 6))
sns.heatmap(cm_3, annot=True, fmt='d', cmap='Greens',
            xticklabels=['ক্লাস ০', 'ক্লাস ১', 'ক্লাস ২'],
            yticklabels=['ক্লাস ০', 'ক্লাস ১', 'ক্লাস ২'])
plt.xlabel('প্রেডিক্টেড')
plt.ylabel('প্রকৃত')
plt.title('মাল্টি-ক্লাস কনফিউশন ম্যাট্রিক্স')
plt.savefig('multiclass_cm.png')
plt.show()
print("মাল্টি-ক্লাস কনফিউশন ম্যাট্রিক্স সেভ করা হয়েছে!")
```

### স্কোরিং এফেক্ট:
```python
print("\n=== ক্লাস ইমব্যালেন্স এফেক্ট ===")

# ইমব্যালেন্সড ডেটা
n_imb = 500
y_imb = np.zeros(n_imb)
y_imb[:50] = 1  # মাত্র ১০% পজিটিভ
pred_all_0 = np.zeros(n_imb)  # সব ০ প্রেডিক্ট
pred_all_1 = np.ones(n_imb)   # সব ১ প্রেডিক্ট

cm_all0 = confusion_matrix(y_imb, pred_all_0)
cm_all1 = confusion_matrix(y_imb, pred_all_1)

print("ইমব্যালেন্সড ডেটা (১০% পজিটিভ):")
print(f"\nসব ০ প্রেডিক্ট করলে:")
print(f"  কনফিউশন ম্যাট্রিক্স:\n{cm_all0}")
print(f"  Accuracy: {accuracy_score(y_imb, pred_all_0):.4f} (ভালো লাগলেও আসলে খারাপ!)")
print(f"  Recall: {cm_all0[1,1]/(cm_all0[1,0]+cm_all0[1,1]):.4f}")

print(f"\nসব ১ প্রেডিক্ট করলে:")
print(f"  কনফিউশন ম্যাট্রিক্স:\n{cm_all1}")
print(f"  Accuracy: {accuracy_score(y_imb, pred_all_1):.4f} (খারাপ)")
print(f"  Recall: {cm_all1[1,1]/(cm_all1[1,0]+cm_all1[1,1]):.4f}")

print(f"\n⚠️ ইমব্যালেন্সড ডেটায় Accuracy বিশ্বাসযোগ্য নয়!")
print(f"  → Precision, Recall, F1, AUC ব্যবহার করুন")
print(f"  → অথবা SMOTE, আন্ডারস্যাম্পলিং টেকনিক ব্যবহার করুন")
```

### সারাংশ:
```python
print("\n=== সারাংশ: কখন কোন মেট্রিক ব্যবহার করবেন ===")

summary = pd.DataFrame({
    'মেট্রিক': ['Accuracy', 'Precision', 'Recall (Sensitivity)', 'Specificity', 
                'F1 Score', 'ROC-AUC', 'PR-AUC'],
    'সূত্র': ['(TP+TN)/Total', 'TP/(TP+FP)', 'TP/(TP+FN)', 'TN/(TN+FP)',
              '2PR/(P+R)', 'ROC এর নিচের ক্ষেত্র', 'PR Curve এর নিচের ক্ষেত্র'],
    'কখন ব্যবহার করবেন': [
        'ব্যালেন্সড ডেটাসেটে',
        'মিথ্যা পজিটিভ এড়াতে চাইলে',
        'মিথ্যা নেগেটিভ এড়াতে চাইলে',
        'নেগেটিভ ক্লাসের সঠিকতা মাপতে',
        'ইমব্যালেন্সড ডেটায়',
        'জেনারেল ক্লাসিফিকেশন পারফরম্যান্স',
        'ইমব্যালেন্সড ডেটায় প্রোবাবিলিটি র‍্যাঙ্কিং'
    ],
    'উদাহরণ': [
        'সাধারণ সমস্যা',
        'স্প্যাম ডিটেকশন',
        'ক্যান্সার ডিটেকশন',
        'নিরাপত্তা সিস্টেম',
        'ফ্রড ডিটেকশন',
        'মডেল তুলনা',
        'রেয়ার ইভেন্ট ডিটেকশন'
    ]
})
print(summary.to_string(index=False))
```

### গুরুত্বপূর্ণ পয়েন্টসমূহ:
```python
print("""
📌 কনফিউশন ম্যাট্রিক্স ও ROC সম্পর্কিত গুরুত্বপূর্ণ তথ্য:

১. কনফিউশন ম্যাট্রিক্সের ৪টি সেল:
   • True Positive (TP): সঠিকভাবে পজিটিভ শনাক্ত
   • True Negative (TN): সঠিকভাবে নেগেটিভ শনাক্ত
   • False Positive (FP): ভুলভাবে পজিটিভ শনাক্ত (টাইপ I এরর)
   • False Negative (FN): ভুলভাবে নেগেটিভ শনাক্ত (টাইপ II এরর)

২. ROC Curve বুঝতে:
   • X-অক্ষ: FPR (FP/FP+TN) — কতটা সুস্থকে অসুস্থ বলছি
   • Y-অক্ষ: TPR (Recall) — কতটা অসুস্থকে সঠিকভাবে শনাক্ত করছি
   • বক্ররেখা যত উপরের দিকে, মডেল তত ভালো

৩. AUC (Area Under Curve):
   • ০.৫: র্যান্ডম (কোনো তথ্য দেয় না)
   • ০.৭-০.৮: গ্রহণযোগ্য
   • ০.৮-০.৯: চমৎকার
   • ০.৯+: অসাধারণ

৪. ইমব্যালেন্সড ডেটার চ্যালেঞ্জ:
   • Accuracy বিভ্রান্তিকর হতে পারে
   • Precision-Recall Curve বেশি নির্ভরযোগ্য
   • F1-Score একটি ভালো ব্যালেন্সড মেট্রিক
""")
```

### সারাংশ:
- **কনফিউশন ম্যাট্রিক্স**: TP, TN, FP, FN — চারটি উপাদান
- **ROC Curve**: বিভিন্ন থ্রেশহোল্ডে TPR vs FPR দেখায়
- **AUC**: মডেলের সার্বিক ক্লাসিফিকেশন ক্ষমতা (0.5-1.0)
- **Precision-Recall Curve**: ইমব্যালেন্সড ডেটার জন্য বেশি নির্ভরযোগ্য
- **থ্রেশহোল্ড**: প্রোবাবিলিটি কাট-অফ পয়েন্ট, প্রয়োজনে পরিবর্তন করা যায়
- **মেট্রিক নির্বাচন**: সমস্যার প্রকৃতি (ক্লাস ব্যালেন্স, কস্ট) অনুযায়ী নির্বাচন করুন