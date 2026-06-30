# Day 27: ফিচার সিলেকশন
## Feature Selection

### ফিচার সিলেকশন কি?
ফিচার সিলেকশন হল সবচেয়ে প্রাসঙ্গিক ফিচার নির্বাচন করার প্রক্রিয়া যা মডেল পারফরম্যান্স উন্নত করে, ওভারফিটিং কমায়, এবং ট্রেইনিং টাইম হ্রাস করে।

### কেন ফিচার সিলেকশন প্রয়োজন?
- **কার্স অফ ডাইমেনশনালিটি** কমানো
- **ওভারফিটিং** হ্রাস
- **ট্রেইনিং টাইম** উন্নত
- **মডেল ইন্টারপ্রিটেবিলিটি** বাড়ানো

### ফাইন্যান্স উদাহরণ: ফিচার সিলেকশন টেকনিক
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import (SelectKBest, f_regression, 
                                       mutual_info_regression,
                                       RFE, SelectFromModel)
from sklearn.linear_model import LassoCV
import matplotlib.pyplot as plt
import seaborn as sns

# ফাইন্যান্স ডেটা তৈরি
np.random.seed(42)
n = 500
n_features = 50

# 50টি ফিচার, যার মধ্যে 10টি প্রাসঙ্গিক
relevant = 10
noise = n_features - relevant

X = np.zeros((n, n_features))
for i in range(relevant):
    X[:, i] = np.random.randn(n) * (i + 1)

# 10 প্রাসঙ্গিক ফিচারের লিনিয়ার কম্বিনেশন
true_coef = np.array([(i+1) * 0.5 for i in range(relevant)] + [0] * noise)
y = X @ true_coef + np.random.randn(n) * 2

# নয়েজ ফিচার যোগ করা
X[:, relevant:] = np.random.randn(n, noise) * 0.5

feature_names = [f'feature_{i}' for i in range(n_features)]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

print(f"Dataset: {df.shape}")
print(f"True relevant features: {relevant}")
print(f"Total features: {n_features}")
```

### 1. ফিল্টার মেথড - Correlation
```python
# Correlation Matrix
corr_matrix = df.corr()
target_corr = corr_matrix['target'].drop('target').abs().sort_values(descending=True)

print("Top 10 features by correlation:")
print(target_corr.head(10))

# Threshold: |corr| > 0.3
selected_by_corr = target_corr[target_corr > 0.3].index.tolist()
print(f"\nFeatures selected by correlation threshold: {len(selected_by_corr)}")
```

### 2. ফিল্টার মেথড - SelectKBest
```python
X_data = df.drop('target', axis=1)
y_data = df['target']

# F-regression
selector_f = SelectKBest(score_func=f_regression, k=15)
selector_f.fit(X_data, y_data)
f_scores = pd.DataFrame({
    'feature': feature_names,
    'f_score': selector_f.scores_
}).sort_values('f_score', ascending=False)

print("Top 15 features by F-Score:")
print(f_scores.head(15))

# Mutual Information
selector_mi = SelectKBest(score_func=mutual_info_regression, k=15)
selector_mi.fit(X_data, y_data)
mi_scores = pd.DataFrame({
    'feature': feature_names,
    'mi_score': selector_mi.scores_
}).sort_values('mi_score', ascending=False)

print("\nTop 15 features by Mutual Information:")
print(mi_scores.head(15))
```

### 3. র্যাপার মেথড - RFE (Recursive Feature Elimination)
```python
# RFE with Random Forest
rf = RandomForestRegressor(n_estimators=50, random_state=42)
rfe = RFE(estimator=rf, n_features_to_select=15)
rfe.fit(X_data, y_data)

rfe_selected = [f for f, s in zip(feature_names, rfe.support_) if s]
print(f"RFE selected features: {len(rfe_selected)}")
print(f"Top features: {rfe_selected[:5]}")
```

### 4. এমবেডেড মেথড - Lasso & Tree Importance
```python
# LassoCV (L1 Regularization)
lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_data, y_data)

lasso_selected = [f for f, c in zip(feature_names, lasso.coef_) if abs(c) > 0.001]
print(f"Lasso selected features: {len(lasso_selected)}")
print(f"Lasso coefs (first 5): {lasso.coef_[:5]}")

# Random Forest Importance
rf_imp = RandomForestRegressor(n_estimators=100, random_state=42)
rf_imp.fit(X_data, y_data)

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': rf_imp.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 features by RF Importance:")
print(importance_df.head(10))
print(f"\nBottom 10 features by RF Importance:")
print(importance_df.tail(10))
```

### 5. ফিচার সিলেকশনের ইমপ্যাক্ট
```python
from sklearn.metrics import mean_squared_error

# All features
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, 
                                                    test_size=0.2, random_state=42)

rf_all = RandomForestRegressor(n_estimators=50, random_state=42)
rf_all.fit(X_train, y_train)
y_pred_all = rf_all.predict(X_test)
rmse_all = np.sqrt(mean_squared_error(y_test, y_pred_all))

# Selected features (top 15 by MI)
selected_mi = mi_scores.head(15)['feature'].tolist()
X_train_sel = X_train[selected_mi]
X_test_sel = X_test[selected_mi]

rf_sel = RandomForestRegressor(n_estimators=50, random_state=42)
rf_sel.fit(X_train_sel, y_train)
y_pred_sel = rf_sel.predict(X_test_sel)
rmse_sel = np.sqrt(mean_squared_error(y_test, y_pred_sel))

print(f"All features ({X_train.shape[1]}): RMSE = {rmse_all:.4f}")
print(f"Selected features ({len(selected_mi)}): RMSE = {rmse_sel:.4f}")
print(f"Train time improvement: ~{X_train.shape[1] // len(selected_mi)}x faster")
```

### ফিচার সিলেকশন পদ্ধতির তুলনা
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

methods = {}

# All features
lr = LinearRegression()
lr.fit(X_train, y_train)
methods['All'] = r2_score(y_test, lr.predict(X_test))

# By Correlation
X_train_corr = X_train[selected_by_corr[:15]]
X_test_corr = X_test[selected_by_corr[:15]]
lr.fit(X_train_corr, y_train)
methods['Correlation'] = r2_score(y_test, lr.predict(X_test_corr))

# By MI
X_train_mi = X_train[selected_mi]
X_test_mi = X_test[selected_mi]
lr.fit(X_train_mi, y_train)
methods['Mutual_Info'] = r2_score(y_test, lr.predict(X_test_mi))

# By Lasso
lasso_feats = [f for f, c in zip(feature_names, lasso.coef_) if abs(c) > 0.001][:15]
X_train_lasso = X_train[lasso_feats]
X_test_lasso = X_test[lasso_feats]
lr.fit(X_train_lasso, y_train)
methods['Lasso'] = r2_score(y_test, lr.predict(X_test_lasso))

# By RFE
X_train_rfe = X_train[rfe_selected[:15]]
X_test_rfe = X_test[rfe_selected[:15]]
lr.fit(X_train_rfe, y_train)
methods['RFE'] = r2_score(y_test, lr.predict(X_test_rfe))

comparison = pd.DataFrame(list(methods.items()), columns=['Method', 'R² Score'])
print("Feature Selection Methods Comparison:")
print(comparison.sort_values('R² Score', ascending=False))
```

### সারসংক্ষেপ
আজ আমরা ফিচার সিলেকশনের বিভিন্ন পদ্ধতি শিখলাম:
- **ফিল্টার মেথড**: Correlation, F-Score, Mutual Information
- **র্যাপার মেথড**: RFE
- **এমবেডেড মেথড**: Lasso, Tree Importance

### অনুশীলনী
1. আপনার ডেটাসেটে 100টি নয়েজ ফিচার যোগ করুন এবং ফিচার সিলেকশনের পারফরম্যান্স মূল্যায়ন করুন
2. বিভিন্ন থ্রেশহোল্ড ব্যবহার করে ফিচার সিলেকশনের ইমপ্যাক্ট তুলনা করুন
3. ফরওয়ার্ড এবং ব্যাকওয়ার্ড সিলেকশন অ্যালগরিদম ইমপ্লিমেন্ট করুন
4. PCA এবং ফিচার সিলেকশনের পারফরম্যান্স তুলনা করুন
