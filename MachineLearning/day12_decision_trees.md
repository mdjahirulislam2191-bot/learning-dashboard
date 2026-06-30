# Day 12: ডিসিশন ট্রি
## Decision Trees

### ডিসিশন ট্রি কি?
ডিসিশন ট্রি একটি সাদৃশ্যপূর্ণ алгоритм যা if-then-else প্রশ্নের মাধ্যমে সিদ্ধান্ত নেয়। এটি নন-লিনিয়ার প্যাটার্ন শনাক্ত করতে পারে।

### ফাইন্যান্স উদাহরণ: ইনভেস্টমেন্ট ডিসিশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns

# ইনভেস্টমেন্ট ডিসিশন ডেটা
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'market_cap_billions': np.random.exponential(10, n),
    'pe_ratio': np.random.normal(15, 8, n),
    'debt_to_equity': np.random.exponential(1, n),
    'revenue_growth': np.random.normal(10, 15, n),
    'profit_margin': np.random.normal(15, 10, n),
    'volatility_30d': np.random.exponential(0.3, n),
    'dividend_yield': np.random.exponential(2, n)
})

# টার্গেট: Buy/Hold/Sell (বাইনারি: Buy বা না)
profit_condition = (data['profit_margin'] > 12).astype(int)
growth_condition = (data['revenue_growth'] > 5).astype(int)
debt_condition = (data['debt_to_equity'] < 1.5).astype(int)

buy_score = profit_condition + growth_condition + debt_condition
data['buy_decision'] = (buy_score >= 2).astype(int)

print("📊 ডেটা ওভারভিউ:")
print(data.head())
print(f"\nBuy Decision Rate: {data['buy_decision'].mean():.2%}")
```

### ডিসিশন ট্রি ট্রেইনিং
```python
X = data.drop('buy_decision', axis=1)
y = data['buy_decision']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# বিভিন্ন ডেপথ ট্রাই
depths = [1, 2, 3, 5, 10, None]  # None = Max depth
for depth in depths:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42)
    tree.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, tree.predict(X_train))
    test_acc = accuracy_score(y_test, tree.predict(X_test))
    print(f"Depth {str(depth):5s}: Train={train_acc:.4f}, Test={test_acc:.4f}", 
          " ⚠️ Overfit" if train_acc > test_acc + 0.1 else "")
```

### Feature Importance
```python
# Optimal depth ট্রি
best_tree = DecisionTreeClassifier(max_depth=4, random_state=42)
best_tree.fit(X_train, y_train)

# ফিচার গুরুত্ব
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': best_tree.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n\n📊 Feature Importance:")
print(importance_df.to_string(index=False))

plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importance - ডিসিশন ট্রি')
plt.gca().invert_yaxis()
plt.show()
```

### ট্রি ভিজুয়ালাইজেশন
```python
plt.figure(figsize=(20, 10))
plot_tree(best_tree, feature_names=X.columns, class_names=['Hold', 'Buy'],
          filled=True, rounded=True, fontsize=10)
plt.title('ইনভেস্টমেন্ট ডিসিশন ট্রি', fontsize=16)
plt.show()
```

### Decision Tree Regressor (স্টক প্রাইস)
```python
# Time series প্রেডিকশন
np.random.seed(42)
n = 500
days = np.arange(n)
price = 100 + np.cumsum(np.random.randn(n) * 0.5)

# ফিচার তৈরি
df = pd.DataFrame({'price': price})
df['lag1'] = df['price'].shift(1)
df['lag2'] = df['price'].shift(2)
df['lag3'] = df['price'].shift(3)
df['sma5'] = df['price'].rolling(5).mean()
df['sma20'] = df['price'].rolling(20).mean()
df['volatility'] = df['price'].rolling(5).std()
df = df.dropna()

X_ts = df.drop('price', axis=1)
y_ts = df['price']

X_train_ts, X_test_ts = X_ts[:350], X_ts[350:]
y_train_ts, y_test_ts = y_ts[:350], y_ts[350:]

tree_reg = DecisionTreeRegressor(max_depth=5, random_state=42)
tree_reg.fit(X_train_ts, y_train_ts)
y_pred_ts = tree_reg.predict(X_test_ts)

print(f"\n📈 Time Series Prediction:")
print(f"R²: {tree_reg.score(X_test_ts, y_test_ts):.4f}")
```

### Hyperparameters
```python
print("""
🎛️ Key Hyperparameters:

max_depth: ট্রির গভীরতা (default=None)
├── ছোট: Underfitting (হাইলি বায়াস)
└── বড়: Overfitting (হাইলি ভ্যারিয়েন্স)

min_samples_split: স্প্লিটের জন্য ন্যূনতম নমুনা
├── বড়: সিম্পলার ট্রি (regularization)
└── ছোট: কমপ্লেক্স ট্রি (overfit)

min_samples_leaf: পাতায় ন্যূনতম নমুনা
├── বড়: স্মুথ প্রেডিকশন
└── ছোট: নয়েজ ক্যাপচার

max_features: বিবেচনার জন্য ফিচার সংখ্যা
├── বড়: সব ফিচার দেখে
└── ছোট: র্যান্ডম নির্বাচন
""")
```

### Pruning (কর্তন)
```python
# Cost complexity pruning
path = best_tree.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

train_scores = []
test_scores = []
for alpha in ccp_alphas:
    tree = DecisionTreeClassifier(max_depth=4, ccp_alpha=alpha, random_state=42)
    tree.fit(X_train, y_train)
    train_scores.append(tree.score(X_train, y_train))
    test_scores.append(tree.score(X_test, y_test))

best_alpha_idx = np.argmax(test_scores)
best_alpha = ccp_alphas[best_alpha_idx]

print(f"\n✂️ Optimal Pruning Alpha: {best_alpha:.4f}")
print(f"Best Test Score: {test_scores[best_alpha_idx]:.4f}")
```

### সারসংক্ষেপ
ডিসিশন ট্রি ইন্টারপ্রেটেবল এবং নন-লিনিয়ার প্যাটার্ন শনাক্ত করতে পারে। তবে এটি overfitting-এর প্রবণ। Pruning, max_depth কন্ট্রোল, এবং এন্সেম্বল মেথড (Random Forest) এই সমস্যা সমাধান করে।