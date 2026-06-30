# Day 13: র্যান্ডম ফরেস্ট
## Random Forest

### র্যান্ডম ফরেস্ট কি?
র্যান্ডম ফরেস্ট একাধিক ডিসিশন ট্রির এন্সেম্বল। প্রতিটি ট্রি আলাদা ডেটা সাবসেট এবং ফিচার সাবসেটে ট্রেইন হয়, তারপর ভোটিং/এভারেজিং এর মাধ্যমে আউটপুট দেয়।

### কেন র্যান্ডম ফরেস্ট শক্তিশালী?
- Overfitting কমায়
- High-dimensional ডেটা হ্যান্ডেল করে
- Missing Values হ্যান্ডেল করে
- Feature Importance দেয়

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report)
import seaborn as sns

# ফাইন্যান্সিয়াল ফ্রড ডেটা
np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'transaction_amount': np.random.exponential(1000, n),
    'transaction_count': np.random.poisson(5, n),
    'account_age_days': np.random.exponential(500, n),
    'avg_transaction_amount': np.random.exponential(800, n),
    'location_change': np.random.poisson(0.5, n),
    'time_since_last_txn': np.random.exponential(24, n),
    'device_match': np.random.binomial(1, 0.9, n),
    'ip_risk_score': np.random.uniform(0, 10, n)
})

# ফ্রড প্যাটার্ন (উচ্চ অ্যামাউন্ট + কম অ্যাকাউন্ট এজ + IP রিস্ক)
fraud_prob = 1 / (1 + np.exp(-(
    -4 + 
    0.002 * data['transaction_amount'] +
    -2 * data['location_change'] +
    -0.005 * data['account_age_days'] +
    0.3 * data['ip_risk_score']
)))
data['is_fraud'] = (np.random.random(n) < fraud_prob).astype(int)

print("📊 ডেটা ওভারভিউ:")
print(f"Fraud Rate: {data['is_fraud'].mean():.2%}")
print(f"Normal Rate: {1-data['is_fraud'].mean():.2%}")
```

### Random Forest ট্রেইনিং
```python
X = data.drop('is_fraud', axis=1)
y = data['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# বেসিক Random Forest
rf = RandomForestClassifier(
    n_estimators=100,  # ট্রি সংখ্যা
    max_depth=10,      # গভীরতা
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1          # প্যারালাল প্রসেসিং
)
rf.fit(X_train, y_train)
```

### মডেল ইভালুয়েশন
```python
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print("\n📊 Random Forest Performance:")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
```

### Feature Importance
```python
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n📊 Feature Importance:")
print(importance_df.to_string(index=False))

plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Random Forest Feature Importance - ফ্রড ডিটেকশন')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

### n_estimators টিউনিং
```python
n_trees = [10, 50, 100, 200, 500]
scores = []

for n in n_trees:
    rf_temp = RandomForestClassifier(n_estimators=n, max_depth=10, 
                                     min_samples_leaf=4, random_state=42, n_jobs=-1)
    rf_temp.fit(X_train, y_train)
    score = rf_temp.score(X_test, y_test)
    scores.append(score)
    print(f"n_estimators={n:3d}: Test Accuracy={score:.4f}")

plt.figure(figsize=(8, 5))
plt.plot(n_trees, scores, 'bo-')
plt.xlabel('Number of Trees')
plt.ylabel('Test Accuracy')
plt.title('Performance vs Number of Trees')
plt.grid(True)
plt.show()
```

### Grid Search CV
```python
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 4]
}

print("\n🔄 Grid Search চলছে...")
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid=param_grid,
    cv=3,
    scoring='roc_auc',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best CV Score: {grid_search.best_score_:.4f}")
print(f"Test Score: {grid_search.score(X_test, y_test):.4f}")
```

### Random Forest Regressor (স্টক প্রেডিকশন)
```python
np.random.seed(42)
n = 500
dates = pd.date_range('2024-01-01', periods=n, freq='D')
price = 100 + np.cumsum(np.random.randn(n) * 0.3)

df_ts = pd.DataFrame({
    'date': dates,
    'price': price
})
df_ts['day'] = np.arange(n)
df_ts['lag1'] = df_ts['price'].shift(1)
df_ts['lag2'] = df_ts['price'].shift(2)
df_ts['sma5'] = df_ts['price'].rolling(5).mean()
df_ts['sma20'] = df_ts['price'].rolling(20).mean()
df_ts['volatility'] = df_ts['price'].rolling(5).std()
df_ts['return'] = df_ts['price'].pct_change()
df_ts = df_ts.dropna()

features_ts = ['day', 'lag1', 'lag2', 'sma5', 'sma20', 'volatility', 'return']
X_ts = df_ts[features_ts]
y_ts = df_ts['price']

X_train_ts = X_ts[:350]
X_test_ts = X_ts[350:]
y_train_ts = y_ts[:350]
y_test_ts = y_ts[350:]

rf_reg = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
rf_reg.fit(X_train_ts, y_train_ts)
y_pred_ts = rf_reg.predict(X_test_ts)

print(f"\n📈 Stock Price Prediction:")
print(f"R² Score: {rf_reg.score(X_test_ts, y_test_ts):.4f}")
```

### Random Forest Pros & Cons
```python
print("""
✅ Advantages:
- Overfitting-প্রতিরোধী (এন্সেম্বল)
- High-dimensional ডেটা হ্যান্ডেল
- Missing values-tolerant
- Feature importance প্রদান করে
- Non-linear প্যাটার্ন শনাক্ত করে

❌ Disadvantages:
- Computationaly expensive (অনেক ট্রি)
- Large memory প্রয়োজন
- Time series-এ forecast-এর জন্য সতর্ক হতে হবে
- Black box (একক ট্রির মতো interpretable না)
- Imbalanced ডেটায় bias হতে পারে

💡 Tips:
├── n_estimators: 100-1000 (বেশি = ভালো, diminishing returns)
├── max_depth: কন্ট্রোল করে (default=None → full trees)
├── min_samples_leaf: imbalance-এর জন্য বড় মান
└── class_weight='balanced' (imbalanced data)
""")
```

### সারসংক্ষেপ
Random Forest একাধিক ডিসিশন ট্রির সমন্বয়ে গঠিত শক্তিশালী মডেল। Overfitting কমায়, feature importance দেয়, এবং ফাইন্যান্সের বিভিন্ন প্রোবলেম (ফ্রড ডিটেকশন, ক্রেডিট রিস্ক) সমাধানে কার্যকর।