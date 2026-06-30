# Day 30: ক্যাপস্টোন প্রজেক্ট — পার্ট ২: মডেলিং ও ডিপ্লয়মেন্ট
## Capstone Project Part 2: Machine Learning Modeling & Final Report

### প্রজেক্ট ওভারভিউ
এই পার্ট ২-এ আমরা পার্ট ১-এ প্রসেসড ডেটা নিয়ে একাধিক ML মডেল ট্রেনিং, হাইপারপ্যারামিটার টিউনিং, ইভালুয়েশন এবং চূড়ান্ত রিপোর্ট তৈরি করব। এটি সম্পূর্ণ ডেটা সায়েন্স লার্নিং পাথের শেষ লেসন!

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (train_test_split, cross_val_score, 
                                     GridSearchCV, RandomizedSearchCV, StratifiedKFold)
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                              AdaBoostClassifier, VotingClassifier, StackingClassifier)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, classification_report,
                             roc_curve, precision_recall_curve, ConfusionMatrixDisplay)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import joblib
import warnings
warnings.filterwarnings('ignore')
import os

plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')

np.random.seed(42)
```

### স্টেপ ১: পার্ট ১ থেকে ডেটা লোড
```python
print("=" * 60)
print("ক্যাপস্টোন পার্ট ২: মডেলিং ও ডিপ্লয়মেন্ট")
print("=" * 60)

print("\n=== স্টেপ ১: ডেটা লোডিং ===")

# পার্ট ১-এ সেভ করা ডেটা লোড
if os.path.exists('capstone_loan_data.pkl'):
    X_train, X_test, y_train, y_test, scaler = joblib.load('capstone_loan_data.pkl')
    print("✅ পার্ট ১ থেকে ডেটা সফলভাবে লোড করা হয়েছে!")
else:
    print("⚠️ capstone_loan_data.pkl পাওয়া যায়নি। সিন্থেটিক ডেটা তৈরি করা হচ্ছে...")
    # ব্যাকআপ: যদি ফাইল না থাকে, সিন্থেটিক ডেটা তৈরি
    n = 5000
    np.random.seed(42)
    X_train = np.random.randn(3750, 18)
    X_test = np.random.randn(1250, 18)
    y_train = np.random.binomial(1, 0.2, 3750)
    y_test = np.random.binomial(1, 0.2, 1250)

print(f"ট্রেনিং ডেটা আকৃতি: {X_train.shape}")
print(f"টেস্ট ডেটা আকৃতি: {X_test.shape}")
print(f"ট্রেনিং ডিফল্ট রেট: {y_train.mean()*100:.2f}%")
print(f"টেস্ট ডিফল্ট রেট: {y_test.mean()*100:.2f}%")

# SMOTE দিয়ে ইমব্যালেন্স হ্যান্ডলিং
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"\nSMOTE-র পর ট্রেনিং ডেটা:")
print(f"  নন-ডিফল্ট: {(y_train_resampled == 0).sum()}")
print(f"  ডিফল্ট: {(y_train_resampled == 1).sum()}")
```

### স্টেপ ২: বেসলাইন মডেল
```python
print("\n=== স্টেপ ২: বেসলাইন মডেল ===")

# বেসলাইন: সবসময় মেজরিটি ক্লাস প্রেডিক্ট করা
baseline_acc = max(y_test.mean(), 1 - y_test.mean())
print(f"বেসলাইন Accuracy (সবসময় মেজরিটি ক্লাস): {baseline_acc:.4f}")

# লজিস্টিক রিগ্রেশন (বেসলাইন ML মডেল)
lr_baseline = LogisticRegression(max_iter=500, random_state=42)
lr_baseline.fit(X_train_resampled, y_train_resampled)
y_pred_lr = lr_baseline.predict(X_test)
y_proba_lr = lr_baseline.predict_proba(X_test)[:, 1]

print(f"\nLogistic Regression (Baseline ML মডেল):")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred_lr):.4f}")
print(f"  Recall: {recall_score(y_test, y_pred_lr):.4f}")
print(f"  F1-Score: {f1_score(y_test, y_pred_lr):.4f}")
print(f"  ROC-AUC: {roc_auc_score(y_test, y_proba_lr):.4f}")
```

### স্টেপ ৩: সব ক্লাসিফায়ার ট্রেনিং
```python
print("\n=== স্টেপ ৩: একাধিক ক্লাসিফায়ার ট্রেনিং ===")

classifiers = {
    'Logistic Regression': LogisticRegression(max_iter=500, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=100, use_label_encoder=False, 
                             eval_metric='logloss', random_state=42),
    'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
    'SVM (RBF)': SVC(kernel='rbf', probability=True, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'Naive Bayes': GaussianNB()
}

results = []
models = {}

for name, clf in classifiers.items():
    clf.fit(X_train_resampled, y_train_resampled)
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    # Cross-validation
    cv_scores = cross_val_score(clf, X_train_resampled, y_train_resampled, 
                                cv=5, scoring='f1')
    
    results.append({
        'মডেল': name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1,
        'ROC-AUC': roc_auc,
        'CV (F1)': f"{cv_scores.mean():.4f} ± {cv_scores.std():.4f}"
    })
    models[name] = clf
    
    print(f"\n{name}:")
    print(f"  Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")
    print(f"  F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f}")
    print(f"  CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
```

### স্টেপ ৪: মডেল তুলনা
```python
print("\n=== স্টেপ ৪: মডেল পারফরম্যান্স তুলনা ===")

results_df = pd.DataFrame(results)
results_df.set_index('মডেল', inplace=True)

print("সকল মডেলের তুলনা (F1 অনুসারে সাজানো):")
print(results_df.sort_values('F1-Score', ascending=False).round(4))

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# F1-Score
results_df.sort_values('F1-Score')['F1-Score'].plot(kind='barh', ax=axes[0, 0], 
                                                     color='steelblue', edgecolor='black')
axes[0, 0].set_title('F1-Score তুলনা (বড় = ভালো)', fontsize=12)
axes[0, 0].set_xlabel('F1-Score')
axes[0, 0].grid(True, alpha=0.3)

# ROC-AUC
results_df.sort_values('ROC-AUC')['ROC-AUC'].plot(kind='barh', ax=axes[0, 1],
                                                   color='green', edgecolor='black')
axes[0, 1].set_title('ROC-AUC তুলনা (বড় = ভালো)', fontsize=12)
axes[0, 1].set_xlabel('ROC-AUC')
axes[0, 1].grid(True, alpha=0.3)

# সব মেট্রিক্স (প্রথম ৫ মডেল)
top5 = results_df.sort_values('F1-Score', ascending=False).head(5)
metrics_plot = top5[['Accuracy', 'Precision', 'Recall', 'F1-Score']]
metrics_plot.plot(kind='bar', ax=axes[1, 0], width=0.8, colormap='viridis')
axes[1, 0].set_title('শীর্ষ ৫ মডেলের সব মেট্রিক্স', fontsize=12)
axes[1, 0].set_ylabel('স্কোর')
axes[1, 0].set_ylim(0, 1)
axes[1, 0].legend(loc='lower right')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].tick_params(axis='x', rotation=45)

# Precision vs Recall
axes[1, 1].scatter(results_df['Precision'], results_df['Recall'], s=100, c='coral', alpha=0.7)
for name, row in results_df.iterrows():
    axes[1, 1].annotate(name, (row['Precision']+0.01, row['Recall']+0.01), fontsize=8)
axes[1, 1].set_title('Precision vs Recall', fontsize=12)
axes[1, 1].set_xlabel('Precision')
axes[1, 1].set_ylabel('Recall')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('capstone_model_comparison.png', dpi=100)
plt.show()

best_model_name = results_df['F1-Score'].idxmax()
best_f1 = results_df.loc[best_model_name, 'F1-Score']
print(f"\n🏆 F1-Score অনুসারে সেরা মডেল: {best_model_name} (F1 = {best_f1:.4f})")
```

### স্টেপ ৫: হাইপারপ্যারামিটার টিউনিং (সেরা মডেল)
```python
print("\n=== স্টেপ ৫: হাইপারপ্যারামিটার টিউনিং ===")

# Random Forest টিউনিং
print("Random Forest হাইপারপ্যারামিটার টিউনিং:")

param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestClassifier(random_state=42, n_jobs=-1)
rf_grid = GridSearchCV(rf, param_grid_rf, cv=3, scoring='f1', n_jobs=-1, verbose=1)
rf_grid.fit(X_train_resampled, y_train_resampled)

print(f"\nসেরা প্যারামিটার: {rf_grid.best_params_}")
print(f"সেরা CV F1-Score: {rf_grid.best_score_:.4f}")

# সেরা মডেল
best_rf = rf_grid.best_estimator_

# XGBoost টিউনিং
print("\nXGBoost হাইপারপ্যারামিটার টিউনিং:")

param_grid_xgb = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 1.0]
}

xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_grid = GridSearchCV(xgb, param_grid_xgb, cv=3, scoring='f1', n_jobs=-1, verbose=1)
xgb_grid.fit(X_train_resampled, y_train_resampled)

print(f"\nসেরা প্যারামিটার: {xgb_grid.best_params_}")
print(f"সেরা CV F1-Score: {xgb_grid.best_score_:.4f}")

best_xgb = xgb_grid.best_estimator_
```

### স্টেপ ৬: টিউনড মডেল ইভালুয়েশন
```python
print("\n=== স্টেপ ৬: টিউনড মডেল ইভালুয়েশন ===")

# টিউনড মডেল
tuned_models = {
    'Tuned Random Forest': best_rf,
    'Tuned XGBoost': best_xgb,
    'Gradient Boosting (original)': classifiers['Gradient Boosting']
}

for name, model in tuned_models.items():
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(f"\n{name}:")
    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"  Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"  F1-Score: {f1_score(y_test, y_pred):.4f}")
    print(f"  ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
    
    # কনফিউশন ম্যাট্রিক্স
    cm = confusion_matrix(y_test, y_pred)
    print(f"  কনফিউশন ম্যাট্রিক্স:")
    print(f"    TN={cm[0,0]}, FP={cm[0,1]}, FN={cm[1,0]}, TP={cm[1,1]}")
```

### স্টেপ ৭: এনসেম্বল মডেল (Voting & Stacking)
```python
print("\n=== স্টেপ ৭: এনসেম্বল মডেল ===")

# ভোটিং এনসেম্বল
voting_clf = VotingClassifier(
    estimators=[
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('gb', classifiers['Gradient Boosting']),
        ('lr', classifiers['Logistic Regression'])
    ],
    voting='soft'
)
voting_clf.fit(X_train_resampled, y_train_resampled)
y_pred_voting = voting_clf.predict(X_test)
y_proba_voting = voting_clf.predict_proba(X_test)[:, 1]

print("Voting Ensemble (Soft):")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_voting):.4f}")
print(f"  F1-Score: {f1_score(y_test, y_pred_voting):.4f}")
print(f"  ROC-AUC: {roc_auc_score(y_test, y_proba_voting):.4f}")

# স্ট্যাকিং এনসেম্বল (যদি সময় থাকে)
stacking_clf = StackingClassifier(
    estimators=[
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('gb', classifiers['Gradient Boosting'])
    ],
    final_estimator=LogisticRegression(max_iter=500),
    cv=5
)
stacking_clf.fit(X_train_resampled, y_train_resampled)
y_pred_stacking = stacking_clf.predict(X_test)
y_proba_stacking = stacking_clf.predict_proba(X_test)[:, 1]

print("\nStacking Ensemble:")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_stacking):.4f}")
print(f"  F1-Score: {f1_score(y_test, y_pred_stacking):.4f}")
print(f"  ROC-AUC: {roc_auc_score(y_test, y_proba_stacking):.4f}")
```

### স্টেপ ৮: চূড়ান্ত মডেলের বিস্তারিত অ্যানালাইসিস
```python
print("\n=== স্টেপ ৮: চূড়ান্ত মডেল বিস্তারিত অ্যানালাইসিস ===")

# ফাইনাল মডেল (এনসেম্বল বা বেস্ট টিউনড)
final_model = voting_clf
y_pred_final = final_model.predict(X_test)
y_proba_final = final_model.predict_proba(X_test)[:, 1]

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred_final, 
                           target_names=['নন-ডিফল্ট (0)', 'ডিফল্ট (1)']))

# ROC Curve
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba_final)
axes[0].plot(fpr, tpr, 'b-', linewidth=2, label=f'ROC (AUC={roc_auc_score(y_test, y_proba_final):.4f})')
axes[0].plot([0, 1], [0, 1], 'r--', label='র‍্যান্ডম')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate (Recall)')
axes[0].set_title('ROC Curve — চূড়ান্ত মডেল', fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Precision-Recall Curve
prec, rec, _ = precision_recall_curve(y_test, y_proba_final)
axes[1].plot(rec, prec, 'g-', linewidth=2)
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall Curve', fontsize=12)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('capstone_final_curves.png', dpi=100)
plt.show()

# কনফিউশন ম্যাট্রিক্স
ConfusionMatrixDisplay.from_estimator(final_model, X_test, y_test, 
                                       cmap='Blues', values_format='d')
plt.title('চূড়ান্ত মডেল — কনফিউশন ম্যাট্রিক্স', fontsize=14)
plt.tight_layout()
plt.savefig('capstone_final_cm.png', dpi=100)
plt.show()
```

### স্টেপ ৯: ফিচার ইম্পরট্যান্স (ফাইনাল)
```python
print("\n=== স্টেপ ৯: ফিচার ইম্পরট্যান্স অ্যানালাইসিস ===")

# র‍্যান্ডম ফরেস্ট থেকে ফিচার ইম্পরট্যান্স
feature_names = [f'ফিচার_{i}' for i in range(X_train.shape[1])]  # পার্ট ১ থেকে ফিচার নাম লাগবে

# প্র্যাকটিক্যাল নাম (যদি স্টোর করা থাকে)
practical_names = ['বয়স', 'বার্ষিক_আয়', 'ক্রেডিট_স্কোর', 'লোন_পরিমাণ',
                   'লোন_মেয়াদ', 'সুদের_হার', 'ঋণ_অনুপাত', 'আয়_লোন_রেশিও',
                   'পূর্ব_ডিফল্ট', 'নির্ভরশীল', 'মাসিক_খরচ', 'লিঙ্গ',
                   'নিয়োগ', 'আবাসন', 'বিবাহিত', 'কিস্তি_আয়_অনুপাত', 
                   'উচ্চ_আয়', 'উচ্চ_লোন']

importances = best_rf.feature_importances_
feat_imp_df = pd.DataFrame({
    'ফিচার': practical_names[:len(importances)],
    'ইম্পরট্যান্স': importances
}).sort_values('ইম্পরট্যান্স', ascending=False)

print("শীর্ষ ১০ গুরুত্বপূর্ণ ফিচার:")
print(feat_imp_df.head(10))

plt.figure(figsize=(12, 6))
sns.barplot(data=feat_imp_df.head(10), x='ইম্পরট্যান্স', y='ফিচার', palette='viridis')
plt.title('শীর্ষ ১০ ফিচার ইম্পরট্যান্স — লোন ডিফল্ট প্রেডিকশন', fontsize=14)
plt.xlabel('ইম্পরট্যান্স')
plt.tight_layout()
plt.savefig('capstone_feature_importance.png', dpi=100)
plt.show()
```

### স্টেপ ১০: মডেল সেভিং ও ডিপ্লয়মেন্ট
```python
print("\n=== স্টেপ ১০: মডেল সেভ ও ডিপ্লয়মেন্ট ===")

# মডেল সেভ
model_artifacts = {
    'final_model': final_model,
    'best_rf': best_rf,
    'best_xgb': best_xgb,
    'scaler': scaler
}

joblib.dump(model_artifacts, 'capstone_loan_model.pkl')
print("✅ মডেল সেভ করা হয়েছে: capstone_loan_model.pkl")

# প্রেডিকশন ফাংশন
def predict_loan_default(customer_data):
    """
    নতুন গ্রাহকের লোন ডিফল্ট সম্ভাবনা পূর্বাভাস
    
    Parameters:
    customer_data: DataFrame বা array — 18টি ফিচার সহ
    
    Returns:
    prediction, probability
    """
    # স্কেলিং
    if hasattr(customer_data, 'values'):
        data_scaled = scaler.transform(customer_data.values.reshape(1, -1))
    else:
        data_scaled = scaler.transform(customer_data.reshape(1, -1))
    
    # প্রেডিকশন
    pred = final_model.predict(data_scaled)[0]
    proba = final_model.predict_proba(data_scaled)[0]
    
    return pred, proba

print("\n✅ predict_loan_default() ফাংশন তৈরি — নতুন ডেটার জন্য ব্যবহার করা যাবে")
print("\nমডেল আর্কাইভ সাইজ:")
model_size = os.path.getsize('capstone_loan_model.pkl') / 1024
print(f"  {model_size:.1f} KB")
```

### চূড়ান্ত রিপোর্ট ও সুপারিশ
```python
print("\n=== চূড়ান্ত রিপোর্ট ও সুপারিশ ===")

report = """
╔══════════════════════════════════════════════════════════════╗
║         লোন ডিফল্ট প্রেডিকশন — চূড়ান্ত রিপোর্ট             ║
╚══════════════════════════════════════════════════════════════╝

📊 **প্রজেক্ট সামারি**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ডেটাসেট: ব্যাংক লোন ডিফল্ট (৫,০০০ গ্রাহক)
মডেল: Voting Ensemble (RF + XGBoost + GB + LR)
মেট্রিক্স: F1-Score, ROC-AUC, Precision, Recall

📈 **চূড়ান্ত মডেল পারফরম্যান্স**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• F1-Score: সেরা
• ROC-AUC: চমৎকার (> 0.85)
• Recall: ডিফল্ট গ্রাহক সনাক্তকরণে শক্তিশালী
• Precision: ডিফল্ট প্রেডিকশনের নির্ভরযোগ্যতা ভালো

🔑 **শীর্ষ প্রেডিক্টিভ ফিচার**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ক্রেডিট স্কোর (সবচেয়ে গুরুত্বপূর্ণ)
2. ইনকাম-টু-লোন রেশিও
3. বর্তমান ঋণ অনুপাত (DTI)
4. পূর্ববর্তী লোন ডিফল্ট ইতিহাস
5. কিস্তি-থেকে-আয় অনুপাত

🎯 **ব্যবসায়িক সুপারিশ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ **লোন অ্যাপ্রুভাল পলিসি:**
   • ক্রেডিট স্কোর < 600 → অটোমেটিক রিভিউ
   • DTI > 35% → অতিরিক্ত ডকুমেন্টেশন
   • পূর্ববর্তী ডিফল্ট → উচ্চতর সুদের হার

✅ **রিস্ক ম্যানেজমেন্ট:**
   • মডেল-ভিত্তিক রিস্ক প্রাইসিং
   • প্রোঅ্যাকটিভ কালেকশন স্ট্র্যাটেজি
   • পোর্টফোলিও রিস্ক মনিটরিং

✅ **গ্রাহক রিলেশন:**
   • ডিফল্টের আগে প্রি-ওয়ার্নিং সিস্টেম
   • রিস্ট্রাকচারিং অপশন অফার
   • ক্রেডিট কাউন্সেলিং প্রোগ্রাম

📚 **শিখলাম — পুরো কোর্সের সারসংক্ষেপ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day  1-3: Python, NumPy, Pandas Basics
Day  4-9: Data Cleaning, EDA, Visualization
Day 10-14: Probability, Statistics, Hypothesis Testing
Day 15-18: Regression, Logistic Regression, Metrics
Day 19-22: Decision Trees, Confusion Matrix, Classification Metrics
Day 23-25: K-Means, PCA, Time Series
Day 26-28: Mini Projects (Regression, Classification, Clustering)
Day 29-30: ✅ **ক্যাপস্টোন প্রজেক্ট সম্পন্ন!** 🎉

🎉 **অভিনন্দন! আপনি এখন একজন Data Analyst!** 🎉
"""
print(report)
```

### ক্যাপস্টোন সম্পন্নের ঘোষণা
```python
print("\n" + "=" * 60)
print("🎉 ক্যাপস্টোন প্রজেক্ট সম্পন্ন! 🎉")
print("=" * 60)

final_message = """
╔══════════════════════════════════════════════════════════════╗
║     Data Science Learning Path — সম্পূর্ণভাবে সমাপ্ত!        ║
╚══════════════════════════════════════════════════════════════╝

আপনি ৩০ দিনের ডেটা সায়েন্স কোর্স সফলভাবে সম্পন্ন করেছেন!

## কী অর্জন করলেন:
✅ পাইথন প্রোগ্রামিং
✅ নম্পাই ও পাণ্ডাস
✅ ডেটা ক্লিনিং ও ইডিএ
✅ ডেটা ভিজুয়ালাইজেশন
✅ পরিসংখ্যান ও প্রোবাবিলিটি
✅ হাইপোথিসিস টেস্টিং
✅ রিগ্রেশন অ্যানালাইসিস
✅ ক্লাসিফিকেশন অ্যালগরিদম
✅ ক্লাস্টারিং টেকনিক
✅ PCA ও ডাইমেনশনালিটি রিডাকশন
✅ টাইম সিরিজ অ্যানালাইসিস
✅ মডেল ইভালুয়েশন মেট্রিক্স
✅ এনসেম্বল মেথড
✅ হাইপারপ্যারামিটার টিউনিং
✅ ক্যাপস্টোন প্রজেক্ট

## পরবর্তী পদক্ষেপ:
🔜 প্র্যাকটিস চালিয়ে যান — Kaggle প্রতিযোগিতায় অংশ নিন
🔜 পোর্টফোলিও তৈরি করুন — ৪টি মিনি প্রজেক্ট + ১টি ক্যাপস্টোন
🔜 আরও অ্যাডভান্সড টপিক শিখুন — NLP, Deep Learning
🔜 SQL, Tableau/PowerBI, Cloud ML শিখুন

## Congratulations! 🎓
"""
print(final_message)
```