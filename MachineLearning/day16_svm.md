# Day 16: SVM (Support Vector Machine)
## সাপোর্ট ভেক্টর মেশিন

### SVM কি?
SVM একটি শক্তিশালী ক্লাসিফিকেশন অ্যালগরিদম যা ক্লাসগুলোর মধ্যে সর্বোচ্চ মার্জিনের হাইপারপ্লেন খুঁজে বের করে। Kernel trick ব্যবহার করে নন-লিনিয়ার ডেটাও ক্লাসিফাই করতে পারে।

### ফাইন্যান্স উদাহরণ: স্টক মার্কেট ট্রেন্ড ক্লাসিফিকেশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC, SVR
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

np.random.seed(42)
n = 1000

# ফাইন্যান্সিয়াল ফিচার
data = pd.DataFrame({
    'rsi': np.random.uniform(20, 80, n),
    'macd': np.random.randn(n) * 2,
    'volume_change': np.random.randn(n) * 5,
    'volatility': np.abs(np.random.randn(n)) * 0.5,
    'price_momentum': np.random.randn(n) * 3
})

# টার্গেট: Market Up (1) or Down (0)
z = (-0.02 * data['rsi'] + 0.3 * data['macd'] + 0.1 * data['volume_change'] 
     - 0.5 * data['volatility'] + 0.2 * data['price_momentum'] + np.random.randn(n) * 0.3)
data['market_up'] = (z > 0).astype(int)

print(f"Market Up Rate: {data['market_up'].mean():.2%}")

X = data.drop('market_up', axis=1)
y = data['market_up']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM-এর জন্য স্কেলিং অপরিহার্য
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### বিভিন্ন Kernel নিয়ে পরীক্ষা
```python
kernels = ['linear', 'rbf', 'poly', 'sigmoid']
results = []

for kernel in kernels:
    svm = SVC(kernel=kernel, probability=True, random_state=42)
    svm.fit(X_train_scaled, y_train)
    y_pred = svm.predict(X_test_scaled)
    y_prob = svm.predict_proba(X_test_scaled)[:, 1]
    
    auc = roc_auc_score(y_test, y_prob)
    results.append({'kernel': kernel, 'accuracy': svm.score(X_test_scaled, y_test), 'auc': auc})

results_df = pd.DataFrame(results)
print("\n📊 Kernel Comparison:")
print(results_df.to_string(index=False))
```

### SVM Hyperparameter Tuning
```python
# Grid Search for SVM
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.1, 0.01],
    'kernel': ['rbf']
}

grid_svm = GridSearchCV(
    SVC(probability=True, random_state=42),
    param_grid=param_grid,
    cv=3,
    scoring='roc_auc',
    n_jobs=-1
)
grid_svm.fit(X_train_scaled, y_train)

print(f"\n🏆 Best Parameters: {grid_svm.best_params_}")
print(f"Best CV AUC: {grid_svm.best_score_:.4f}")
print(f"Test AUC: {roc_auc_score(y_test, grid_svm.predict_proba(X_test_scaled)[:, 1]):.4f}")
```

### SVM Regressor (SVR) - স্টক প্রাইস
```python
np.random.seed(42)
n = 300
days = np.arange(n).reshape(-1, 1)
price = 100 + days.squeeze() * 0.2 + np.random.randn(n) * 3

X_svr = days
y_svr = price

X_train_svr, X_test_svr, y_train_svr, y_test_svr = train_test_split(
    X_svr, y_svr, test_size=0.2, random_state=42
)

# SVR with RBF kernel
svr = SVR(kernel='rbf', C=10, gamma='scale')
svr.fit(X_train_svr, y_train_svr)
y_pred_svr = svr.predict(X_test_svr)

from sklearn.metrics import r2_score, mean_squared_error
print(f"\n📈 SVR Stock Price:")
print(f"R²: {r2_score(y_test_svr, y_pred_svr):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test_svr, y_pred_svr)):.2f}")
```

### SVM Pros & Cons
```python
print("""
✅ Advantages:
- High-dimensional space-এ কার্যকর
- Kernel trick → non-linear প্যাটার্ন
- Decision boundary-এর clear margin
- Overfitting-প্রতিরোধী (regularization)
- Text classification-এ জনপ্রিয়

❌ Disadvantages:
- বড় ডেটাসেটে ধীর
- Kernel এবং hyperparameter টিউনিং জটিল
- Scalability issues (O(n²) or O(n³))
- Imbalanced ডেটায় sensitivity
- Probability calibration প্রয়োজন

💡 Tips:
├── Features scale করুন (StandardScaler)
├── C (regularization) টিউন করুন
│   - Small C: Soft margin (generalization)
│   - Large C: Hard margin (overfitting)
├── Gamma: RBF kernel-এর প্রভাবের পরিধি
└── class_weight='balanced' for imbalance
""")
```

### সারসংক্ষেপ
SVM শক্তিশালী ক্লাসিফিকেশন অ্যালগরিদম যা kernel trick-এর মাধ্যমে non-linear প্যাটার্ন শনাক্ত করে। ফাইন্যান্সে market trend prediction, fraud detection, এবং risk classification-এ ব্যবহৃত হয়।