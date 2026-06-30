# Day 15: XGBoost
## XGBoost - Extreme Gradient Boosting

### XGBoost কি?
XGBoost হল গ্রেডিয়েন্ট বুটিংয়ের একটি অপ্টিমাইজড ইমপ্লিমেন্টেশন যা speed এবং performance-এর জন্য বিখ্যাত।

### XGBoost-এর বিশেষত্ব
1. **Regularization** - L1/L2 (ওভারফিটিং কমায়)
2. **Parallel Processing** - দ্রুত ট্রেইনিং
3. **Tree Pruning** - নিজে থেকেই প্রুন
4. **Missing Values** - নিজে হ্যান্ডেল
5. **Cross-validation** - বিল্ট-ইন

### ফাইন্যান্স উদাহরণ: ক্রেডিট স্কোরিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report)
import xgboost as xgb
import time

# বড় ফাইন্যান্স ডেটাসেট
np.random.seed(42)
n = 5000

data = pd.DataFrame({
    'age': np.random.randint(20, 70, n),
    'income': np.random.exponential(60000, n),
    'loan_amount': np.random.exponential(15000, n),
    'credit_history_length': np.random.exponential(10, n),
    'num_credit_cards': np.random.randint(0, 10, n),
    'utilization_rate': np.random.uniform(0, 1, n),
    'num_late_payments': np.random.poisson(1, n),
    'dti_ratio': np.random.uniform(0.1, 0.5, n),
    'employment_years': np.random.exponential(8, n),
    'num_inquiries': np.random.poisson(2, n),
    'previous_defaults': np.random.poisson(0.2, n),
    'savings_ratio': np.random.uniform(0, 0.5, n)
})

# ক্রেডিট রিস্ক স্কোর
risk_score = (
    0.3 * (data['credit_history_length'] / 20) +
    0.2 * (1 - data['utilization_rate']) +
    0.15 * (data['income'] / 100000) +
    0.1 * (1 - data['dti_ratio']) +
    0.1 * (1 - data['num_late_payments'] / 10) +
    0.1 * (data['employment_years'] / 20) +
    0.05 * (1 - data['previous_defaults'] / 5)
)
risk_score += np.random.randn(n) * 0.1
data['good_credit'] = (risk_score > 0.5).astype(int)

print(f"Good Credit Rate: {data['good_credit'].mean():.2%}")

X = data.drop('good_credit', axis=1)
y = data['good_credit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### XGBoost ট্রেইনিং
```python
start = time.time()

model = xgb.XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    min_child_weight=1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,  # L1 regularization
    reg_lambda=1.0,  # L2 regularization
    gamma=0,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss',
    early_stopping_rounds=20,
    tree_method='auto'
)

# Evaluation set দিয়ে ট্রেইন
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

train_time = time.time() - start
print(f"⏱️ Training Time: {train_time:.2f}s")
```

### Evaluation
```python
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n📊 XGBoost Performance:")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")
```

### Feature Importance (XGBoost-এ ৩ টাইপ)
```python
# Weight: কতবার ফিচার ট্রি স্প্লিটে ব্যবহৃত হয়েছে
importance_weight = model.get_booster().get_score(importance_type='weight')

# Gain: ফিচার ব্যবহারের গড় ইনফরমেশন গেইন
importance_gain = model.get_booster().get_score(importance_type='gain')

# Cover: ফিচার কতগুলি নমুনাকে কভার করে
importance_cover = model.get_booster().get_score(importance_type='cover')

print("\nFeature Importance (Weight):")
for feat, imp in sorted(importance_weight.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {feat}: {imp}")
```

### Grid Search for XGBoost
```python
# সংক্ষিপ্ত গ্রিড সার্চ
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1],
    'n_estimators': [100, 200],
    'subsample': [0.8, 1.0]
}

print("\n🔄 Grid Search...")
grid_xgb = GridSearchCV(
    xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
    param_grid=param_grid,
    cv=3,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=0
)
grid_xgb.fit(X_train, y_train)

print(f"Best Params: {grid_xgb.best_params_}")
print(f"Best CV Score: {grid_xgb.best_score_:.4f}")
```

### XGBoost Regressor (স্টক প্রাইস)
```python
np.random.seed(42)
n = 1000
price = 100 + np.cumsum(np.random.randn(n) * 0.5)

df = pd.DataFrame({'price': price})
for lag in range(1, 11):
    df[f'lag_{lag}'] = df['price'].shift(lag)
for ma in [5, 10, 20, 50]:
    df[f'sma_{ma}'] = df['price'].rolling(ma).mean()
df['volatility'] = df['price'].rolling(10).std()
df['return'] = df['price'].pct_change()
df = df.dropna()

feature_cols = [c for c in df.columns if c != 'price']
X_ts = df[feature_cols]
y_ts = df['price']

split = int(len(df) * 0.8)
X_train_ts, X_test_ts = X_ts[:split], X_ts[split:]
y_train_ts, y_test_ts = y_ts[:split], y_ts[split:]

xgb_reg = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
xgb_reg.fit(X_train_ts, y_train_ts, eval_set=[(X_test_ts, y_test_ts)], verbose=False)

print(f"\n📈 Stock Price Regression:")
print(f"R²: {xgb_reg.score(X_test_ts, y_test_ts):.4f}")
```

### XGBoost vs Other Models Comparison
```python
print("""
📊 XGBoost vs Others:

             XGBoost    Random Forest    GBM
Speed        ⚡⚡⚡     ⚡⚡           ⚡
Accuracy     🎯🎯🎯     🎯🎯           🎯🎯
Overfitting  Low         Low             Medium
Tuning       Many params Fewer params   Medium
Interpret    SHAP/Imp    Easy            Moderate

🏆 When to use XGBoost:
├── Large datasets (>10K rows)
├── When accuracy is priority
├── Kaggle competitions
├── Imbalanced data
└── Need regularization
""")
```

### সারসংক্ষেপ
XGBoost গ্রেডিয়েন্ট বুটিংয়ের সবচেয়ে শক্তিশালী ইমপ্লিমেন্টেশন। রেগুলারাইজেশন, প্যারালাল প্রসেসিং, এবং বিল্ট-ইন CV ফিচারের কারণে ফাইন্যান্স এবং ডেটা সায়েন্স কম্পিটিশনে ব্যাপকভাবে ব্যবহৃত হয়।