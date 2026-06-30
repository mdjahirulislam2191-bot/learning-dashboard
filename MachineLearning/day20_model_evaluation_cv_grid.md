# Day 20: মডেল ইভালুয়েশন (Cross-Validation, Grid Search)
## Model Evaluation - Cross-Validation & Hyperparameter Tuning

### Cross-Validation কেন গুরুত্বপূর্ণ?
একবার Train/Test Split করলে ভাগ্য ভালো/মন্দ হওয়ার সম্ভাবনা থাকে। Cross-Validation ডেটার একাধিক ভিন্ন ভিন্ন সাবসেটে মডেল টেস্ট করে আরো নির্ভরযোগ্য evaluation দেয়।

### ফাইন্যান্স উদাহরণ: সম্পূর্ণ CV + Grid Search
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import (cross_val_score, KFold, StratifiedKFold,
                                     RepeatedKFold, LeaveOneOut, GridSearchCV,
                                     RandomizedSearchCV, learning_curve,
                                     validation_curve, TimeSeriesSplit)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'feature1': np.random.randn(n),
    'feature2': np.random.randn(n),
    'feature3': np.random.randn(n),
    'feature4': np.random.randn(n),
    'feature5': np.random.randn(n),
    'feature6': np.random.randn(n),
    'feature7': np.random.randn(n),
    'feature8': np.random.randn(n)
})

# লিনিয়ার কম্বিনেশন + নয়েজ
z = (data['feature1'] * 2 + data['feature2'] * 1.5 + data['feature3'] * (-1) +
     data['feature4'] * 0.5 + np.random.randn(n) * 1)
data['target'] = (z > 0).astype(int)

X = data.drop('target', axis=1)
y = data['target']

print(f"Target distribution: {y.value_counts().to_dict()}")
```

### 1. বিভিন্ন CV স্ট্রাটেজি
```python
cv_strategies = {
    'K-Fold (k=5)': KFold(n_splits=5, shuffle=True, random_state=42),
    'K-Fold (k=10)': KFold(n_splits=10, shuffle=True, random_state=42),
    'Stratified K-Fold': StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    'Repeated K-Fold': RepeatedKFold(n_splits=5, n_repeats=3, random_state=42),
}

model = DecisionTreeClassifier(max_depth=5, random_state=42)

print("\n📊 CV Strategy Comparison:")
for name, cv in cv_strategies.items():
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    print(f"{name:25s}: {scores.mean():.4f} (+/- {scores.std()*2:.4f})")
```

### 2. Time Series CV (ফাইন্যান্সের জন্য)
```python
# টাইম সিরিজ ডেটা সিমুলেশন
dates = pd.date_range('2024-01-01', periods=n, freq='D')
data_with_dates = data.copy()
data_with_dates['date'] = dates
data_with_dates = data_with_dates.sort_values('date')

tscv = TimeSeriesSplit(n_splits=5)
ts_scores = cross_val_score(model, data_with_dates[X.columns], 
                            data_with_dates['target'], cv=tscv)

print("\n⏱️ Time Series CV:")
for i, score in enumerate(ts_scores):
    print(f"  Fold {i+1}: {score:.4f}")
print(f"  Mean TS CV: {ts_scores.mean():.4f}")
```

### 3. Grid Search - সম্পূর্ণ টিউনিং
```python
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

print("\n🔄 Grid Search চলছে...")
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid=param_grid,
    cv=3,  # 3-fold CV
    scoring='accuracy',
    n_jobs=-1,
    verbose=0
)
grid_search.fit(X, y)

print(f"\n🏆 Best Parameters:")
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")
print(f"Best CV Score: {grid_search.best_score_:.4f}")
print(f"Test Score: {grid_search.score(X, y):.4f}")

# Grid Search ফলাফল
results_df = pd.DataFrame(grid_search.cv_results_)
print(f"\nTotal combinations tested: {len(results_df)}")
```

### 4. Randomized Search (বড় সার্চ স্পেসের জন্য)
```python
param_dist = {
    'n_estimators': [50, 100, 200, 300, 500],
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10, 15],
    'min_samples_leaf': [1, 2, 4, 6],
    'max_features': ['sqrt', 'log2', None]
}

print("\n🔄 Randomized Search (20 iterations)...")
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_distributions=param_dist,
    n_iter=20,  # শুধু 20 র্যান্ডম কম্বিনেশন
    cv=3,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)
random_search.fit(X, y)

print(f"\n🏆 Best Random Search Params: {random_search.best_params_}")
print(f"Best CV Score: {random_search.best_score_:.4f}")
```

### 5. Learning Curve
```python
train_sizes, train_scores, test_scores = learning_curve(
    RandomForestClassifier(n_estimators=50, random_state=42),
    X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

print("\n📈 Learning Curve:")
for size, train, test in zip(train_sizes, train_mean, test_mean):
    print(f"Train size={size:.0f}: Train={train:.4f}, Test={test:.4f}")
```

### 6. Validation Curve (একটি প্যারামিটার টিউনিং)
```python
param_range = range(1, 20, 2)
train_scores_v, test_scores_v = validation_curve(
    DecisionTreeClassifier(random_state=42),
    X, y,
    param_name='max_depth',
    param_range=param_range,
    cv=5,
    scoring='accuracy'
)

print("\n📊 Validation Curve (max_depth):")
for depth, train_mean, test_mean in zip(
    param_range, 
    np.mean(train_scores_v, axis=1), 
    np.mean(test_scores_v, axis=1)
):
    print(f"max_depth={depth:2d}: Train={train_mean:.4f}, Test={test_mean:.4f}")
```

### Best Practices
```python
print("""
📋 CV & Tuning Best Practices:

1. **CV স্ট্রাটেজি নির্বাচন:**
   ├── সাধারণ: K-Fold (k=5 or 10)
   ├── ইমব্যালেন্সড: Stratified K-Fold
   ├── টাইম সিরিজ: TimeSeriesSplit
   └── ছোট ডেটা: Leave-One-Out / Repeated CV

2. **Grid Search নিয়ম:**
   ├── Broad range → Narrow range (coarse to fine)
   ├── 3-fold CV is usually enough
   ├── Randomized Search for >10 parameters
   └── Scoring metric সঠিকভাবে নির্বাচন

3. **সতর্কতা:**
   ├── NEVER use test data for tuning
   ├── Cross-validation on TRAINING data only
   ├── Feature selection CV-র ভিতরে করতে হবে
   └── Time series-এ future data leakage এড়ান

4. **Overfitting চিহ্নিতকরণ:**
   ├── Train >> Test gap বড় হলে overfit
   ├── Learning curve: train/test converge না হলে
   └── Validation curve: U-shaped test performance
""")
```

### সারসংক্ষেপ
Cross-Validation এবং Hyperparameter Tuning ML পাইপলাইনের অপরিহার্য অংশ। CV মডেলের জেনারেলাইজেশন ক্ষমতার নির্ভরযোগ্য পরিমাপ দেয়, Grid/Randomized Search সেরা প্যারামিটার খুঁজে বের করে। ফাইন্যান্সে TimeSeriesSplit ব্যবহার করা উচিত।