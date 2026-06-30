# Day 19: লজিস্টিক রিগ্রেশন
## Logistic Regression

### লজিস্টিক রিগ্রেশন কী?
লজিস্টিক রিগ্রেশন একটি ক্লাসিফিকেশন অ্যালগরিদম যা বাইনারি আউটপুট (০ বা ১, হ্যাঁ বা না) প্রেডিক্ট করে। ��টি লিনিয়ার রিগ্রেশন থেকে ভিন্ন কারণ এটি সিগময়েড ফাংশন ব্যবহার করে প্রোবাবিলিটি আউটপুট দেয়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (accuracy_score, confusion_matrix, classification_report,
                             roc_auc_score, roc_curve, precision_recall_curve)
import warnings
warnings.filterwarnings('ignore')

# স্যাম্পল ডেটাসেট: ক্রেডিট কার্ড ডিফল্ট প্রেডিকশন
np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'বয়স': np.random.randint(18, 70, n),
    'আয়': np.random.lognormal(10.5, 0.6, n).astype(int),
    'ক্রেডিট_স্কোর': np.random.randint(300, 850, n),
    'লোন_পরিমাণ': np.random.lognormal(11, 0.8, n).astype(int),
    'লোন_টু_আয়_রেশিও': np.random.uniform(0.1, 1.5, n),
    'পূর্ববর্তী_ডিফল্ট': np.random.choice([0, 1], n, p=[0.8, 0.2]),
    'অ্যাকাউন্ট_বয়স': np.random.randint(1, 120, n)  # মাসে
})

# ডিফল্ট প্রোবাবিলিটি তৈরি
log_odds = (-3 + 0.02 * (850 - df['ক্রেডিট_স্কোর']) + 
            0.5 * df['লোন_টু_আয়_রেশিও'] + 
            1.5 * df['পূর্ববর্তী_ডিফল্ট'] - 
            0.02 * df['অ্যাকাউন্ট_বয়স'] +
            0.01 * (df['বয়স'] - 30))
prob = 1 / (1 + np.exp(-log_odds))
df['ডিফল্ট'] = np.random.binomial(1, prob)

print("=== ক্রেডিট ডিফল্ট ডেটাসেট ===")
print(df.head())
print(f"\nডিফল্ট রেট: {df['ডিফল্ট'].mean()*100:.2f}%")
print(f"মোট রেকর্ড: {len(df)}")
print(f"\nফিচার তালিকা: {list(df.columns)}")
```

### লজিস্টিক রিগ্রেশন বনাম লিনিয়ার রিগ্রেশন:
```python
print("\n=== লজিস্টিক vs লিনিয়ার রিগ্রেশন ===")

x = np.linspace(-10, 10, 100)

# লিনিয়ার (সীমাহীন আউটপুট)
linear = 2 * x - 3

# লজিস্টিক (সিগময়েড) [০-১ এর মধ্যে]
sigmoid = 1 / (1 + np.exp(-x))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x, linear, 'b-', linewidth=2)
plt.axhline(y=0, color='gray', linestyle='--')
plt.axhline(y=1, color='gray', linestyle='--')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('লিনিয়ার রিগ্রেশন (Y = β₀ + β₁X)')
plt.ylim(-15, 15)
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(x, sigmoid, 'r-', linewidth=2)
plt.axhline(y=0.5, color='gray', linestyle='--', label='থ্রেশহোল্ড (0.5)')
plt.axhline(y=0, color='gray', linestyle='--')
plt.axhline(y=1, color='gray', linestyle='--')
plt.xlabel('X (লগ-অডস)')
plt.ylabel('P(Y=1)')
plt.title('লজিস্টিক রিগ্রেশন (সিগময়েড ফাংশন)')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('logistic_vs_linear.png')
plt.show()
print("লজিস্টিক বনাম লিনিয়ার গ্রাফ সেভ করা হয়েছে!")
```

### মডেল ট্রেনিং:
```python
print("\n=== মডেল ট্রেনিং ===")

X = df.drop('ডিফল্ট', axis=1)
y = df['ডিফল্ট']

# ট্রেন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# স্কেলিং (লজিস্টিক রিগ্রেশনের জন্য গুরুত্বপূর্ণ)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# মডেল ট্রেনিং
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

print(f"ট্রেন সেট: {X_train.shape}")
print(f"টেস্ট সেট: {X_test.shape}")

# কোফিসিয়েন্ট
coef_df = pd.DataFrame({
    'ফিচার': X.columns,
    'কোফিসিয়েন্ট': model.coef_[0],
    'অডস_রেশিও': np.exp(model.coef_[0])
}).sort_values('কোফিসিয়েন্ট', ascending=False)
print(f"\nকোফিসিয়েন্ট ও অডস রেশিও:")
print(coef_df.to_string(index=False))
```

### সিগময়েড ফাংশন ও প্রোবাবিলিটি:
```python
print("\n=== সিগময়েড ফাংশন ===")

def sigmoid(z):
    """সিগময়েড ফাংশন: P(y=1) = 1/(1+e^(-z))"""
    return 1 / (1 + np.exp(-z))

# প্রোবাবিলিটি প্রেডিকশন
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print(f"প্রথম ১০টি টেস্ট নমুনার প্রেডিক্টেড প্রোবাবিলিটি:")
prob_df = pd.DataFrame({
    'প্রকৃত': y_test.values[:10],
    'প্রেডিক্টেড_প্রোব': y_prob[:10],
    'প্রেডিক্টেড_ক্লাস': (y_prob[:10] >= 0.5).astype(int)
})
print(prob_df.to_string(index=False))

# ডিসিশন বাউন্ডারি
print(f"\nডিসিশন বাউন্ডারি: P >= 0.5 → ক্লাস ১ (ডিফল্ট)")
print(f"                   P < 0.5 → ক্লাস ০ (নো ডিফল্ট)")
```

### ক্লাসিফিকেশন থ্রেশহোল্ড:
```python
print("\n=== ক্লাসিফিকেশন থ্রেশহোল্ড ===")

# বিভিন্ন থ্রেশহোল্ডে accuracy
thresholds = np.arange(0.1, 1.0, 0.1)
accuracies = []

for thresh in thresholds:
    pred = (y_prob >= thresh).astype(int)
    acc = accuracy_score(y_test, pred)
    accuracies.append(acc)
    print(f"থ্রেশহোল্ড {thresh:.1f}: Accuracy = {acc:.4f}")

# বেস্ট থ্রেশহোল্ড
best_thresh = thresholds[np.argmax(accuracies)]
print(f"\nসেরা থ্রেশহোল্ড: {best_thresh:.1f} (Accuracy: {max(accuracies):.4f})")
```

### ক্লাসিফিকেশন রিপোর্ট:
```python
print("\n=== ক্লাসিফিকেশন রিপোর্ট ===")

y_pred_default = (y_prob >= 0.5).astype(int)

print("ডিফল্ট থ্রেশহোল্ড (0.5) দিয়ে:");
print(classification_report(y_test, y_pred_default, target_names=['নো ডিফল্ট', 'ডিফল্ট']))

# কনফিউশন ম্যাট্রিক্স
cm = confusion_matrix(y_test, y_pred_default)
print("কনফিউশন ম্যাট্রিক্স:")
print(f"              {'প্রেডিক্টেড নো':<15} {'প্রেডিক্টেড ডিফল্ট'}")
print(f"প্রকৃত নো     {cm[0,0]:<15} {cm[0,1]}")
print(f"প্রকৃত ডিফল্ট {cm[1,0]:<15} {cm[1,1]}")

# মেট্রিক্স
tn, fp, fn, tp = cm.ravel()
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f} (ডিফল্ট প্রেডিক্ট করলে কতবার সঠিক)")
print(f"Recall:    {recall:.4f} (প্রকৃত ডিফল্টের কতটা চিহ্নিত করেছি)")
print(f"F1-Score:  {f1:.4f}")
print(f"\nSpecificity: {tn/(tn+fp):.4f} (প্রকৃত নো-ডিফল্টের কতটা চিহ্নিত করেছি)")
```

### ROC Curve ও AUC:
```python
print("\n=== ROC Curve ও AUC ===")

fpr, tpr, thresholds_roc = roc_curve(y_test, y_prob)
auc = roc_auc_score(y_test, y_prob)

print(f"AUC Score: {auc:.4f}")
print(f"(AUC ০.৫ = র্যান্ডম, ১.০ = পারফেক্ট)")

# AUC ইন্টারপ্রিটেশন
if auc >= 0.9:
    print("📊 অসাধারণ মডেল!")
elif auc >= 0.8:
    print("📊 ভালো মডেল!")
elif auc >= 0.7:
    print("📊 মোটামুটি মডেল")
else:
    print("📊 দুর্বল মডেল")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(fpr, tpr, 'b-', linewidth=2, label=f'ROC Curve (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'r--', label='র্যান্ডম (AUC = 0.5)')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curve')
plt.legend()
plt.grid(alpha=0.3)

# Precision-Recall Curve
plt.subplot(1, 2, 2)
precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_prob)
plt.plot(recall_vals, precision_vals, 'b-', linewidth=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('roc_pr_curves.png')
plt.show()
print("ROC ও PR Curve সেভ করা হয়েছে!")
```

### কোফিসিয়েন্ট ইন্টারপ্রিটেশন:
```python
print("\n=== কোফিসিয়েন্ট ইন্টারপ্রিটেশন ===")

print("কোফিসিয়েন্ট ইন্টারপ্রিটেশন (লগ-অডস স্কেলে):")
for i, feat in enumerate(X.columns):
    coef = model.coef_[0][i]
    odds_ratio = np.exp(coef)
    direction = "বাড়ে" if coef > 0 else "কমে"
    print(f"  {feat}: coef={coef:+.4f}, odds_ratio={odds_ratio:.4f}")
    print(f"    → {feat} ১ ইউনিট বাড়লে ডিফল্টের লগ-অডস {coef:.4f} {direction}")
    print(f"    → ওডস {odds_ratio:.4f} গুণ হয়")

# সবচেয়ে শক্তিশালী ফিচার
abs_coef = np.abs(model.coef_[0])
top_idx = np.argmax(abs_coef)
print(f"\n💡 সবচেয়ে শক্তিশালী ফিচার: {X.columns[top_idx]} (|coef| = {abs_coef[top_idx]:.4f})")
```

### ক্রস-ভ্যালিডেশন:
```python
print("\n=== ক্রস-ভ্যালিডেশন ===")

cv_scores = cross_val_score(LogisticRegression(max_iter=1000), 
                            scaler.fit_transform(X), y, 
                            cv=5, scoring='roc_auc')
print(f"৫-ফোল্ড CV AUC স্কোর:")
print(f"  প্রতিটি ফোল্ড: {cv_scores}")
print(f"  গড় AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

cv_accuracy = cross_val_score(LogisticRegression(max_iter=1000), 
                               scaler.fit_transform(X), y, 
                               cv=5, scoring='accuracy')
print(f"\n৫-ফোল্ড CV Accuracy:")
print(f"  গড় Accuracy: {cv_accuracy.mean():.4f} ± {cv_accuracy.std():.4f}")
```

### লজিস্টিক রিগ্রেশন অ্যাসাম্পশন:
```python
print("\n=== অ্যাসাম্পশন চেক ===")

print("লজিস্টিক রিগ্রেশনের অ্যাসাম্পশন:")
print("""
১. ✅ বাইনারি আউটপুট (০/১)
২. ✅ লিনিয়ারিটি অব লগ-অডস (ফিচার ও লগ-অডসের মধ্যে লিনিয়ার সম্পর্ক)
৩. ❌ নরমালিটি প্রয়োজন নেই
৪. ❌ হোমোসকেডাস্টিসিটি প্রয়োজন নেই
৫. ⚠️ নো মাল্টিকোলিনিয়ারিটি (VIF চেক করা ভালো)
৬. ⚠️ পর্যাপ্ত স্যাম্পল সাইজ
""")
```

### প্রেডিকশন উদাহরণ:
```python
print("\n=== প্রেডিকশন উদাহরণ ===")

# নতুন ক্লায়েন্ট
new_clients = pd.DataFrame([
    {'বয়স': 25, 'আয়': 30000, 'ক্রেডিট_স্কোর': 600, 'লোন_পরিমাণ': 50000,
     'লোন_টু_আয়_রেশিও': 1.67, 'পূর্ববর্তী_ডিফল্ট': 0, 'অ্যাকাউন্ট_বয়স': 12},
    {'বয়স': 45, 'আয়': 80000, 'ক্রেডিট_স্কোর': 750, 'লোন_পরিমাণ': 30000,
     'লোন_টু_আয়_রেশিও': 0.375, 'পূর্ববর্তী_ডিফল্ট': 0, 'অ্যাকাউন্ট_বয়স': 60},
    {'বয়স': 30, 'আয়': 40000, 'ক্রেডিট_স্কোর': 500, 'লোন_পরিমাণ': 60000,
     'লোন_টু_আয়_রেশিও': 1.5, 'পূর্ববর্তী_ডিফল্ট': 1, 'অ্যাকাউন্ট_বয়স': 6}
])

new_clients_scaled = scaler.transform(new_clients)
new_probs = model.predict_proba(new_clients_scaled)[:, 1]
new_preds = model.predict(new_clients_scaled)

for i, client in new_clients.iterrows():
    risk = "উচ্চ ঝুঁকি ⚠️" if new_preds[i] == 1 else "নিম্ন ঝুঁকি ✅"
    print(f"\nক্লায়েন্ট {i+1}: আয়={client['আয়']:,}, স্কোর={client['ক্রেডিট_স্কোর']}, লোন={client['লোন_পরিমাণ']:,}")
    print(f"  ডিফল্ট প্রোবাবিলিটি: {new_probs[i]:.2%}")
    print(f"  সিদ্ধান্ত: {risk}")
```

### একাধিক ক্লাসে লজিস্টিক রিগ্রেশন:
```python
print("\n=== মাল্টিনোমিয়াল লজিস্টিক রিগ্রেশন ===")

# তিনটি ক্লাসের ডেটা
np.random.seed(42)
X_multi = np.random.randn(300, 2)
y_multi = np.random.choice([0, 1, 2], size=300)

model_multi = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model_multi.fit(X_multi, y_multi)

print(f"মাল্টিনোমিয়াল মডেল Accuracy: {model_multi.score(X_multi, y_multi):.4f}")
print(f"ক্লাস সমূহ: {model_multi.classes_}")
print(f"প্রথম ৫ প্রেডিকশন:")
print(pd.DataFrame({
    'প্রকৃত': y_multi[:5],
    'প্রেডিক্টেড': model_multi.predict(X_multi[:5]),
    'প্রোব_ক্লাস০': model_multi.predict_proba(X_multi[:5])[:, 0],
    'প্রোব_ক্লাস১': model_multi.predict_proba(X_multi[:5])[:, 1],
    'প্রোব_ক্লাস২': model_multi.predict_proba(X_multi[:5])[:, 2],
}).round(4))
```

### সারাংশ:
- **লজিস্টিক রিগ্রেশন**: বাইনারি ক্লাসিফিকেশনের জন্য (০/১, হ্যাঁ/না)
- **সিগময়েড ফাংশন**: ০-১ এর মধ্যে প্রোবাবিলিটি আউটপুট দেয়
- **অডস রেশিও**: ফিচারের প্রতি ইউনিট পরিবর্তনে ওডসের পরিবর্তনের অনুপাত
- **ডিসিশন বাউন্ডারি**: সাধারণত ০.৫ (প্রয়োজনে পরিবর্তন করা যায়)
- **AUC**: মডেলের ক্লাসিফিকেশন ক্ষমতার সার্বিক মাপ (০.৫-১.০)
- **পার্থক্য**: লিনিয়ার রিগ্রেশন সংখ্যা প্রেডিক্ট করে, লজিস্টিক রিগ্রেশন প্রোবাবিলিটি প্রেডিক্ট করে