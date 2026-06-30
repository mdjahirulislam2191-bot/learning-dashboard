# Day 27: মিনি প্রজেক্ট — ক্লাসিফিকেশন অ্যানালাইসিস
## Mini Project: Classification Analysis — গ্রাহক চার্ন প্রেডিকশন

### প্রজেক্ট ওভারভিউ
এই প্রজেক্টে আমরা একটি টেলিকম কোম্পানির গ্রাহক চার্ন (Churn) ডেটাসেট নিয়ে ক্লাসিফিকেশন মডেল তৈরি করব। লক্ষ্য: কোন গ্রাহকরা কোম্পানি ছেড়ে যেতে পারেন তা পূর্বাভাস করা।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier, 
                              AdaBoostClassifier, VotingClassifier)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, classification_report,
                             roc_curve, precision_recall_curve, ConfusionMatrixDisplay)
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')

np.random.seed(42)
```

### স্টেপ ১: ডেটাসেট তৈরি
```python
print("=" * 60)
print("প্রজেক্ট: গ্রাহক চার্ন প্রেডিকশন")
print("=" * 60)

print("\n=== স্টেপ ১: টেলিকম চার্ন ডেটাসেট ===")

n_customers = 5000

churn_data = pd.DataFrame({
    'গ্রাহক_আইডি': range(1, n_customers + 1),
    'বয়স': np.random.randint(18, 80, n_customers),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা'], n_customers),
    'চুক্তি_ধরন': np.random.choice(['মাসিক', 'বার্ষিক', 'দ্বিবার্ষিক'], n_customers, p=[0.5, 0.3, 0.2]),
    'মাসিক_বিল': np.random.uniform(30, 150, n_customers).round(2),
    'গ্রাহক_সময়কাল_মাস': np.random.randint(1, 72, n_customers),
    'গ্রাহক_পরিষেবা_কল': np.random.poisson(2, n_customers),
    'পেমেন্ট_বিলম্ব_দিন': np.random.poisson(3, n_customers),
    'ইন্টারনেট_ধরন': np.random.choice(['ফাইবার', 'DSL', 'কোনটি_নয়'], n_customers, p=[0.4, 0.4, 0.2]),
    'অনলাইন_সিকিউরিটি': np.random.choice(['হ্যাঁ', 'না'], n_customers),
    'টেক_সাপোর্ট': np.random.choice(['হ্যাঁ', 'না'], n_customers),
    'কন্ট্রাক্ট_অটোরিনিউ': np.random.choice(['হ্যাঁ', 'না'], n_customers),
})

# চার্ন প্যাটার্ন তৈরি
churn_prob = np.zeros(n_customers)

# মাসিক চুক্তি = বেশি চার্ন রেট
churn_prob += (churn_data['চুক্তি_ধরন'] == 'মাসিক') * 0.25
churn_prob += (churn_data['চুক্তি_ধরন'] == 'বার্ষিক') * 0.10
churn_prob += (churn_data['চুক্তি_ধরন'] == 'দ্বিবার্ষিক') * 0.03

# কম গ্রাহক সময়কাল = বেশি চার্ন
churn_prob += (churn_data['গ্রাহক_সময়কাল_মাস'] < 12) * 0.15

# বেশি বিল = বেশি চার্ন
churn_prob += (churn_data['মাসিক_বিল'] > 100) * 0.10

# বেশি গ্রাহক পরিষেবা কল = বেশি চার্ন
churn_prob += np.minimum(churn_data['গ্রাহক_পরিষেবা_কল'] * 0.05, 0.20)

# পেমেন্ট বিলম্ব = বেশি চার্ন
churn_prob += np.minimum(churn_data['পেমেন্ট_বিলম্ব_দিন'] * 0.03, 0.15)

# সিকিউরিটি না থাকলে = বেশি চার্ন
churn_prob += (churn_data['অনলাইন_সিকিউরিটি'] == 'না') * 0.05

# টেক সাপোর্ট না থাকলে = বেশি চার্ন
churn_prob += (churn_data['টেক_সাপোর্ট'] == 'না') * 0.05

churn_prob = np.clip(churn_prob, 0.01, 0.95)
churn_data['চার্ন'] = np.random.binomial(1, churn_prob)

print(f"মোট গ্রাহক: {len(churn_data)}")
print(f"চার্ন গ্রাহক: {churn_data['চার্ন'].sum()} ({churn_data['চার्न'].mean()*100:.1f}%)")
print(f"নন-চার্ন গ্রাহক: {(1-churn_data['চার্ন']).sum()} ({(1-churn_data['চার্ন'].mean())*100:.1f}%)")
print("\nপ্রথম ৫টি রেকর্ড:")
print(churn_data.head())
```

### স্টেপ ২: EDA — চার্ন অ্যানালাইসিস
```python
print("\n=== স্টেপ ২: এক্সপ্লোরেটরি ডেটা অ্যানালাইসিস ===")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# চার্ন ডিস্ট্রিবিউশন
churn_data['চার্ন'].value_counts().plot(kind='bar', ax=axes[0, 0], color=['steelblue', 'coral'], edgecolor='black')
axes[0, 0].set_title('চার্ন ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 0].set_xticklabels(['নন-চার্ন', 'চার্ন'], rotation=0)
axes[0, 0].set_ylabel('গ্রাহক সংখ্যা')
axes[0, 0].grid(True, alpha=0.3)

# চুক্তি ধরন অনুসারে চার্ন রেট
churn_by_contract = churn_data.groupby('চুক্তি_ধরন')['চার্ন'].mean()
churn_by_contract.plot(kind='bar', ax=axes[0, 1], color='steelblue', edgecolor='black')
axes[0, 1].set_title('চুক্তি ধরন অনুসারে চার্ন রেট', fontsize=12)
axes[0, 1].set_ylabel('চার্ন রেট')
axes[0, 1].set_ylim(0, 0.5)
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].tick_params(axis='x', rotation=45)

# মাসিক বিল vs চার্ন
axes[0, 2].boxplot([churn_data[churn_data['চার্ন']==0]['মাসিক_বিল'],
                    churn_data[churn_data['চার্ন']==1]['মাসিক_বিল']], 
                   labels=['নন-চার্ন', 'চার্ন'])
axes[0, 2].set_title('মাসিক বিল vs চার্ন', fontsize=12)
axes[0, 2].set_ylabel('মাসিক বিল ($)')
axes[0, 2].grid(True, alpha=0.3)

# গ্রাহক সময়কাল vs চার্ন
axes[1, 0].boxplot([churn_data[churn_data['চার্ন']==0]['গ্রাহক_সময়কাল_মাস'],
                    churn_data[churn_data['চার্ন']==1]['গ্রাহক_সময়কাল_মাস']],
                   labels=['নন-চার্ন', 'চার্ন'])
axes[1, 0].set_title('গ্রাহক সময়কাল vs চার্ন', fontsize=12)
axes[1, 0].set_ylabel('সময়কাল (মাস)')
axes[1, 0].grid(True, alpha=0.3)

# গ্রাহক পরিষেবা কল vs চার্ন
axes[1, 1].bar(churn_data[churn_data['চার্ন']==0]['গ্রাহক_পরিষেবা_কল'].value_counts().sort_index().index,
               churn_data[churn_data['চার্ন']==0]['গ্রাহক_পরিষেবা_কল'].value_counts().sort_index().values,
               alpha=0.6, label='নন-চার্ন', color='steelblue')
axes[1, 1].bar(churn_data[churn_data['চার্ন']==1]['গ্রাহক_পরিষেবা_কল'].value_counts().sort_index().index,
               churn_data[churn_data['চার्न']==1]['গ্রাহক_পরিষেবা_কল'].value_counts().sort_index().values,
               alpha=0.6, label='চার্ন', color='coral')
axes[1, 1].set_title('গ্রাহক পরিষেবা কল vs চার্ন', fontsize=12)
axes[1, 1].set_xlabel('কলের সংখ্যা')
axes[1, 1].set_ylabel('গ্রাহক সংখ্যা')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# পেমেন্ট বিলম্ব vs চার্ন
axes[1, 2].bar(churn_data[churn_data['চার্ন']==0]['পেমেন্ট_বিলম্ব_দিন'].value_counts().sort_index().index[:10],
               churn_data[churn_data['চার্ন']==0]['পেমেন্ট_বিলম্ব_দিন'].value_counts().sort_index().values[:10],
               alpha=0.6, label='নন-চার্ন', color='steelblue')
axes[1, 2].bar(churn_data[churn_data['চার্ন']==1]['পেমেন্ট_বিলম্ব_দিন'].value_counts().sort_index().index[:10],
               churn_data[churn_data['চার্ন']==1]['পেমেন্ট_বিলম্ব_দিন'].value_counts().sort_index().values[:10],
               alpha=0.6, label='চার্ন', color='coral')
axes[1, 2].set_title('পেমেন্ট বিলম্ব vs চার্ন', fontsize=12)
axes[1, 2].set_xlabel('বিলম্ব দিন')
axes[1, 2].set_ylabel('গ্রাহক সংখ্যা')
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('project_churn_eda.png', dpi=100)
plt.show()
```

### স্টেপ ৩: ডেটা প্রিপ্রসেসিং
```python
print("\n=== স্টেপ ৩: ডেটা প্রিপ্রসেসিং ===")

# ফিচার এনকোডিং
le_dict = {}
categorical_cols = ['লিঙ্গ', 'চুক্তি_ধরন', 'ইন্টারনেট_ধরন', 
                    'অনলাইন_সিকিউরিটি', 'টেক_সাপোর্ট', 'কন্ট্রাক্ট_অটোরিনিউ']

for col in categorical_cols:
    le = LabelEncoder()
    churn_data[col + '_এনকোড'] = le.fit_transform(churn_data[col])
    le_dict[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    print(f"{col}: {le_dict[col]}")

# ফিচার সিলেকশন
feature_cols = ['বয়স', 'মাসিক_বিল', 'গ্রাহক_সময়কাল_মাস', 'গ্রাহক_পরিষেবা_কল', 'পেমেন্ট_বিলম্ব_দিন']
feature_cols += [col + '_এনকোড' for col in categorical_cols]

X = churn_data[feature_cols]
y = churn_data['চার্ন']

print(f"\nফিচার তালিকা ({len(feature_cols)}টি):")
for f in feature_cols:
    print(f"  - {f}")

# ট্রেন-টেস্ট স্প্লিট (স্ট্র্যাটিফাইড)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"\nট্রেনিং: {X_train.shape} (চার্ন: {y_train.mean()*100:.1f}%)")
print(f"টেস্ট: {X_test.shape} (চার্ন: {y_test.mean()*100:.1f}%)")

# স্কেলিং
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE দিয়ে ইমব্যালেন্স হ্যান্ডলিং
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

print(f"\nSMOTE-র পর ট্রেনিং ডেটা:")
print(f"  নন-চার্ন: {(y_train_resampled == 0).sum()}")
print(f"  চার্ন: {(y_train_resampled == 1).sum()}")
```

### স্টেপ ৪: মডেল ট্রেনিং
```python
print("\n=== স্টেপ ৪: ক্লাসিফিকেশন মডেল ট্রেনিং ===")

classifiers = {
    'Logistic Regression': LogisticRegression(max_iter=200, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=8, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'Naive Bayes': GaussianNB()
}

results = []
for name, clf in classifiers.items():
    clf.fit(X_train_resampled, y_train_resampled)
    y_pred = clf.predict(X_test_scaled)
    y_proba = clf.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    results.append({
        'মডেল': name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1,
        'ROC-AUC': roc_auc
    })
    
    print(f"\n{name}:")
    print(f"  Accuracy: {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall: {rec:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    print(f"  ROC-AUC: {roc_auc:.4f}")
```

### স্টেপ ৫: মডেল তুলনা
```python
print("\n=== স্টেপ ৫: মডেল তুলনা ===")

results_df = pd.DataFrame(results)
results_df.set_index('মডেল', inplace=True)

print("সকল মডেলের তুলনা:")
print(results_df.round(4))

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
results_df[metrics].plot(kind='bar', ax=axes[0], width=0.8, colormap='viridis')
axes[0].set_title('মডেল পারফরম্যান্স তুলনা (সব মেট্রিক্স)', fontsize=12)
axes[0].set_ylabel('স্কোর')
axes[0].set_ylim(0, 1)
axes[0].legend(loc='lower right')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

results_df['ROC-AUC'].plot(kind='bar', ax=axes[1], color='steelblue', edgecolor='black')
axes[1].set_title('ROC-AUC স্কোর তুলনা', fontsize=12)
axes[1].set_ylabel('ROC-AUC')
axes[1].set_ylim(0.5, 1)
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('project_churn_comparison.png', dpi=100)
plt.show()

# সেরা মডেল (F1 বেসিসে)
best_f1 = results_df['F1-Score'].idxmax()
print(f"\n🏆 F1-Score অনুসারে সেরা মডেল: {best_f1} ({results_df.loc[best_f1, 'F1-Score']:.4f})")
```

### স্টেপ ৬: কনফিউশন ম্যাট্রিক্স
```python
print("\n=== স্টেপ ৬: কনফিউশন ম্যাট্রিক্স ===")

# সেরা মডেল দিয়ে
best_clf = RandomForestClassifier(n_estimators=200, random_state=42)
best_clf.fit(X_train_resampled, y_train_resampled)
y_pred_best = best_clf.predict(X_test_scaled)

cm = confusion_matrix(y_test, y_pred_best)
print("কনফিউশন ম্যাট্রিক্স:")
print(f"  TN (True Negative): {cm[0, 0]}")
print(f"  FP (False Positive): {cm[0, 1]}")
print(f"  FN (False Negative): {cm[1, 0]}")
print(f"  TP (True Positive): {cm[1, 1]}")

print(f"\nচার্ন ডিটেকশন রেট (Recall): {cm[1,1]/(cm[1,0]+cm[1,1])*100:.1f}%")
print(f"চার্ন ভুল পূর্বাভাস (False Positive): {cm[0,1]/(cm[0,0]+cm[0,1])*100:.1f}%")

ConfusionMatrixDisplay.from_estimator(best_clf, X_test_scaled, y_test, 
                                       cmap='Blues', values_format='d')
plt.title('কনফিউশন ম্যাট্রিক্স - Random Forest', fontsize=14)
plt.tight_layout()
plt.savefig('project_churn_cm.png', dpi=100)
plt.show()
```

### স্টেপ ৭: ROC Curve ও Precision-Recall Curve
```python
print("\n=== স্টেপ ৭: ROC Curve ও Precision-Recall Curve ===")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ROC Curve
for name, clf in classifiers.items():
    if hasattr(clf, "predict_proba"):
        y_proba = clf.predict_proba(X_test_scaled)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        axes[0].plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})', linewidth=2)

axes[0].plot([0, 1], [0, 1], 'k--', label='র‍্যান্ডম ক্লাসিফায়ার')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve', fontsize=14)
axes[0].legend(loc='lower right')
axes[0].grid(True, alpha=0.3)

# Precision-Recall Curve
for name, clf in classifiers.items():
    if hasattr(clf, "predict_proba"):
        y_proba = clf.predict_proba(X_test_scaled)[:, 1]
        prec, rec, _ = precision_recall_curve(y_test, y_proba)
        axes[1].plot(rec, prec, label=name, linewidth=2)

axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall Curve', fontsize=14)
axes[1].legend(loc='lower left')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('project_churn_curves.png', dpi=100)
plt.show()

print("ROC AUC 1.0 = পারফেক্ট, 0.5 = র‍্যান্ডম")
print("Imbalanced ডেটাসেটে PR Curve বেশি নির্ভরযোগ্য")
```

### স্টেপ ৮: ফিচার ইম্পরট্যান্স
```python
print("\n=== স্টেপ ৮: ফিচার ইম্পরট্যান্স ===")

importances = best_clf.feature_importances_
feature_importance = pd.DataFrame({
    'ফিচার': feature_cols,
    'ইম্পরট্যান্স': importances
}).sort_values('ইম্পরট্যান্স', ascending=False)

print("ফিচার ইম্পরট্যান্স (Random Forest):")
print(feature_importance)

plt.figure(figsize=(12, 6))
sns.barplot(data=feature_importance, x='ইম্পরট্যান্স', y='ফিচার', palette='viridis')
plt.title('ফিচার ইম্পরট্যান্স - চার্ন প্রেডিকশন', fontsize=14)
plt.xlabel('ইম্পরট্যান্স')
plt.tight_layout()
plt.savefig('project_churn_importance.png', dpi=100)
plt.show()

print("\n🔑 শীর্ষ ৩ গুরুত্বপূর্ণ ফিচার:")
for i in range(3):
    feat = feature_importance.iloc[i]
    print(f"  {i+1}. {feat['ফিচার']} ({feat['ইম্পরট্যান্স']:.3f})")
```

### স্টেপ ৯: বিজনেস ইনসাইট
```python
print("\n=== স্টেপ ৯: বিজনেস ইনসাইট ===")

insights = """
## চার্ন অ্যানালাইসিস থেকে ব্যবসায়িক অন্তর্দৃষ্টি:

🔴 **উচ্চ চার্ন ঝুঁকির গ্রাহক বৈশিষ্ট্য:**
• মাসিক চুক্তি ব্যবহারকারী
• ১২ মাসের কম সময়ের গ্রাহক
• মাসিক বিল $১০০ এর বেশি
• বারবার গ্রাহক পরিষেবা কল (৩+)
• পেমেন্ট বিলম্ব বেশি (৫+ দিন)
• অনলাইন সিকিউরিটি ও টেক সাপোর্ট নেই

🟢 **চার্ন কমানোর কৌশল:**
• মাসিক → বার্ষিক চুক্তিতে আপগ্রেড প্রমোশন
• নতুন গ্রাহকদের জন্য ওয়েলকাম বেনিফিট
• হাই-ভ্যালু গ্রাহকদের লয়্যালটি প্রোগ্রাম
• প্রোঅ্যাকটিভ কাস্টমার সার্ভিস
• অটো-রিনিউ রিমাইন্ডার ও ইনসেনটিভ

📊 **মডেল বিজনেস ভ্যালু:**
• Risk স্কোরিং: প্রতিটি গ্রাহকের চার্ন সম্ভাবনা
• টার্গেটেড ইন্টারভেনশন: উচ্চ ঝুঁকির গ্রাহকদের বিশেষ অফার
• কোস্ট সেভিংস: চার্ন প্রতিরোধের ROI বিশ্লেষণ
"""
print(insights)
```

### সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("প্রজেক্ট সারসংক্ষেপ")
print("=" * 60)

summary = """
## এই প্রজেক্ট থেকে যা শিখলাম:

✅ সম্পূর্ণ ক্লাসিফিকেশন পাইপলাইন:
   1. ইমব্যালেন্সড ডেটাসেট তৈরি ও বিশ্লেষণ
   2. স্ট্র্যাটিফাইড ট্রেন-টেস্ট স্প্লিট
   3. SMOTE দিয়ে ইমব্যালেন্স হ্যান্ডলিং
   4. ৮টি ক্লাসিফিকেশন মডেল তুলনা
   5. কনফিউশন ম্যাট্রিক্স বিশ্লেষণ
   6. ROC ও Precision-Recall Curve
   7. ফিচার ইম্পরট্যান্স অ্যানালাইসিস
   8. বিজনেস ইনসাইট জেনারেশন

✅ গুরুত্বপূর্ণ মেট্রিক্স:
   - Precision: মডেল যাদের চার্ন বলেছে, তাদের মধ্যে কতজন সত্যিই চার্ন করবে
   - Recall: প্রকৃত চার্ন গ্রাহকদের মধ্যে মডেল কতজনকে সনাক্ত করতে পেরেছে
   - F1-Score: Precision ও Recall-এর জ্যামিতিক গড়
   - Imbalanced ডেটায় Accuracy কম নির্ভরযোগ্য

✅ Data Analyst-এর Takeaways:
📌 সবসময় Imbalanced ডেটা চেক করুন
📌 SMOTE ওভারস্যাম্পলিং ব্যবহার করুন
📌 Precision-Recall > Accuracy (Imbalanced ডেটায়)
📌 ফিচার ইম্পরট্যান্স বুঝে ইনসাইট জেনারেট করুন
"""
print(summary)
```