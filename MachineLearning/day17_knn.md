# Day 17: KNN (K-Nearest Neighbors)
## কে-নিয়ারেস্ট নেবারস

### KNN কি?
KNN একটি লেজি লার্নিং অ্যালগরিদম যা নতুন ডেটা পয়েন্টের k-সংখ্যক নিকটতম প্রতিবেশীর ভোটের ভিত্তিতে প্রেডিকশন করে। এটি নন-প্যারামেট্রিক।

### ফাইন্যান্স উদাহরণ: ক্রেডিট রিস্ক - KNN
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

np.random.seed(42)
n = 1500

data = pd.DataFrame({
    'income_to_loan': np.random.uniform(0.5, 5, n),
    'credit_score': np.random.randint(300, 850, n),
    'debt_payments': np.random.exponential(1000, n),
    'age': np.random.randint(22, 70, n),
    'num_loans': np.random.randint(0, 10, n),
    'payment_history': np.random.uniform(0, 10, n)
})

# টার্গেট: Low Risk (1) / High Risk (0)
risk_score = (data['income_to_loan'] * 20 + data['credit_score'] * 0.3 + 
              data['payment_history'] * 5 - data['num_loans'] * 5)
data['low_risk'] = (risk_score > np.median(risk_score)).astype(int)

X = data.drop('low_risk', axis=1)
y = data['low_risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN-এর জন্য স্কেলিং অপরিহার্য
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Low Risk Rate: {y.mean():.2%}")
```

### K-ভ্যালু টিউনিং
```python
k_values = range(1, 51, 2)
k_scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring='accuracy')
    k_scores.append(scores.mean())

best_k = k_values[np.argmax(k_scores)]
print(f"\n🏆 Best K value: {best_k}")
print(f"Best CV Accuracy: {max(k_scores):.4f}")

plt.figure(figsize=(10, 5))
plt.plot(k_values, k_scores, 'bo-')
plt.axvline(x=best_k, color='r', linestyle='--', label=f'Best K={best_k}')
plt.xlabel('K Value')
plt.ylabel('Cross-Validation Accuracy')
plt.title('K vs Accuracy - KNN Performance')
plt.legend()
plt.grid(True)
plt.show()
```

### ওয়েটেড এবং ইউনিফর্ম KNN
```python
knn_uniform = KNeighborsClassifier(n_neighbors=best_k, weights='uniform')
knn_distance = KNeighborsClassifier(n_neighbors=best_k, weights='distance')

knn_uniform.fit(X_train_scaled, y_train)
knn_distance.fit(X_train_scaled, y_train)

print("\n📊 Weight Comparison:")
print(f"Uniform:  {knn_uniform.score(X_test_scaled, y_test):.4f}")
print(f"Distance: {knn_distance.score(X_test_scaled, y_test):.4f}")
```

### Distance Metrics
```python
metrics = ['euclidean', 'manhattan', 'minkowski', 'chebyshev']
for metric in metrics:
    knn = KNeighborsClassifier(n_neighbors=best_k, metric=metric)
    knn.fit(X_train_scaled, y_train)
    score = knn.score(X_test_scaled, y_test)
    print(f"{metric:12s}: {score:.4f}")
```

### Grid Search
```python
param_grid = {
    'n_neighbors': range(1, 31, 2),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'minkowski']
}

grid = GridSearchCV(
    KNeighborsClassifier(),
    param_grid=param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=-1
)
grid.fit(X_train_scaled, y_train)

print(f"\n🏆 Best KNN: {grid.best_params_}")
print(f"Test Accuracy: {grid.score(X_test_scaled, y_test):.4f}")
```

### KNN Regressor - Stock Price
```python
np.random.seed(42)
n = 500
days = np.arange(n).reshape(-1, 1)
price = 100 + np.cumsum(np.random.randn(n) * 0.5)

df_knn = pd.DataFrame({'day': days.squeeze(), 'price': price})
df_knn['lag1'] = df_knn['price'].shift(1)
df_knn['lag2'] = df_knn['price'].shift(2)
df_knn['sma5'] = df_knn['price'].rolling(5).mean()
df_knn['sma20'] = df_knn['price'].rolling(20).mean()
df_knn = df_knn.dropna()

X_knn = df_knn[['day', 'lag1', 'lag2', 'sma5', 'sma20']]
y_knn = df_knn['price']

X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
    X_knn, y_knn, test_size=0.2, random_state=42
)

scaler_knn = StandardScaler()
X_train_knn_s = scaler_knn.fit_transform(X_train_knn)
X_test_knn_s = scaler_knn.transform(X_test_knn)

knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train_knn_s, y_train_knn)

print(f"\n📈 KNN Regressor R²: {knn_reg.score(X_test_knn_s, y_test_knn):.4f}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- Simple and intuitive
- নন-লিনিয়ার প্যাটার্ন শনাক্ত করে
- নন-প্যারামেট্রিক (কোনো assumption নেই)
- মাল্টি-ক্লাস ক্লাসিফিকেশন সহজ

❌ Disadvantages:
- Feature scaling আবশ্যক
- বড় ডেটায় ধীর (O(nd))
- Curse of dimensionality
- ইমব্যালেন্সড ডেটায় bias
- Interpretability কম

💡 Tips:
├── K ছোট = Complex (overfitting)
├── K বড় = Smooth (underfitting)
├── Odd K নির্বাচন (tie break)
├── Scaler ব্যবহার আবশ্যক (StandardScaler)
└── Feature selection গুরুত্বপূর্ণ
""")
```

### সারসংক্ষেপ
KNN সহজ কিন্তু কার্যকর নন-প্যারামেট্রিক অ্যালগরিদম। K-ভ্যালু নির্বাচন এবং ফিচার স্কেলিং গুরুত্বপূর্ণ। ফাইন্যান্সে ক্রেডিট স্কোরিং এবং প্যাটার্ন রিকগনিশনে ব্যবহৃত হয়।