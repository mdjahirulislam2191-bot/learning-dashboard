# Day 20: ডিসিশন ট্রি
## Decision Trees

### ডিসিশন ট্রি কী?
ডিসিশন ট্রি একটি সুপারভাইজড লার্নিং অ্যালগরিদম যা গাছের মতো স্ট্রাকচার ব্যবহার করে সিদ্ধান্ত নেয়। এটি ক্লাসিফিকেশন ও রিগ্রেশন উভয়ের জন্যই ব্যবহার করা যায়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree, export_text
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ডেটাসেট: লোন অ্যাপ্রুভাল প্রেডিকশন
np.random.seed(42)
n = 500

df = pd.DataFrame({
    'আয়': np.random.lognormal(10.5, 0.6, n).astype(int),
    'ক্রেডিট_স্কোর': np.random.randint(300, 850, n),
    'লোন_পরিমাণ': np.random.lognormal(11, 0.8, n).astype(int),
    'কর্মসংস্থান_বছর': np.random.randint(0, 30, n),
    'ঋণের_ইতিহাস': np.random.choice(['ভালো', 'মধ্যম', 'খারাপ'], n),
    'সম্পত্তির_মূল্য': np.random.lognormal(12, 0.7, n).astype(int),
})

# লজিক: লোন অ্যাপ্রুভাল
df['লোন_অনুমোদিত'] = (
    (df['ক্রেডিট_স্কোর'] >= 650) & 
    (df['কর্মসংস্থান_বছর'] >= 1) & 
    (df['লোন_পরিমাণ'] <= df['আয়'] * 3) &
    (df['ঋণের_ইতিহাস'] != 'খারাপ')
).astype(int)

print("=== লোন ডেটাসেট ===")
print(df.head())
print(f"\nলোন অ্যাপ্রুভাল রেট: {df['লোন_অনুমোদিত'].mean()*100:.2f}%")
print(f"ডেটা শেপ: {df.shape}")
```

### ডিসিশন ট্রি ক্লাসিফায়ার:
```python
print("\n=== ডিসিশন ট্রি ক্লাসিফায়ার ===")

# এনকোডিং
le = LabelEncoder()
df_encoded = df.copy()
df_encoded['ঋণের_ইতিহাস'] = le.fit_transform(df_encoded['ঋণের_ইতিহাস'])

X = df_encoded.drop('লোন_অনুমোদিত', axis=1)
y = df_encoded['লোন_অনুমোদিত']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# বেসিক ডিসিশন ট্রি
dt = DecisionTreeClassifier(random_state=42, max_depth=3)
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"\nক্লাসিফিকেশন রিপোর্ট:")
print(classification_report(y_test, y_pred, target_names=['রিজেক্ট', 'অনুমোদিত']))
```

### ডিসিশন ট্রি ভিজুয়ালাইজেশন:
```python
print("\n=== ডিসিশন ট্রি ভিজুয়ালাইজেশন ===")

plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=X.columns, class_names=['রিজেক্ট', 'অনুমোদিত'], 
          filled=True, rounded=True, fontsize=12)
plt.title('লোন অ্যাপ্রুভাল ডিসিশন ট্রি')
plt.savefig('decision_tree.png', dpi=150, bbox_inches='tight')
plt.show()
print("ডিসিশন ট্রি গ্রাফ সেভ করা হয়েছে!")

# টেক্সট আউটপুট
tree_text = export_text(dt, feature_names=list(X.columns))
print("\nডিসিশন ট্রি (টেক্সট ফর্ম্যাট):")
print(tree_text)
```

### জিনি ইমপিউরিটি বোঝা:
```python
print("\n=== জিনি ইমপিউরিটি ===")

def gini_impurity(classes):
    """জিনি ইমপিউরিটি গণনা"""
    total = len(classes)
    if total == 0:
        return 0
    probabilities = np.bincount(classes) / total
    return 1 - np.sum(probabilities ** 2)

# উদাহরণ
perfect_split = np.array([0, 0, 0, 0])  # সব এক ক্লাস
mixed_split = np.array([0, 0, 1, 1, 1])  # মিশ্রিত
very_mixed = np.array([0, 0, 1, 1, 2, 2, 2])  # আরও মিশ্রিত

print("জিনি ইমপিউরিটি:")
print(f"  পারফেক্ট স্প্লিট (সব ০): {gini_impurity(perfect_split):.4f}")
print(f"  মিক্সড (২:৩ অনুপাত): {gini_impurity(mixed_split):.4f}")
print(f"  আরও মিক্সড (২:২:৩): {gini_impurity(very_mixed):.4f}")

# ফিচার ইম্পরট্যান্স ও জিনি
print(f"\nফিচার ইম্পরট্যান্স (জিনি):")
for i, col in enumerate(X.columns):
    print(f"  {col}: {dt.feature_importances_[i]:.4f}")
```

### ডিসিশন ট্রি প্যারামিটার টিউনিং:
```python
print("\n=== হাইপারপ্যারামিটার টিউনিং ===")

param_grid = {
    'max_depth': [3, 5, 7, 10, 15, None],
    'min_samples_split': [2, 5, 10, 20],
    'min_samples_leaf': [1, 2, 5, 10],
    'max_features': [None, 'sqrt', 'log2']
}

# Grid Search (অল্প কম্বিনেশন)
simple_grid = {
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), 
                           simple_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

print(f"সেরা প্যারামিটার: {grid_search.best_params_}")
print(f"সেরা CV স্কোর: {grid_search.best_score_:.4f}")

# বেস্ট মডেল ইভালুয়েশন
best_dt = grid_search.best_estimator_
y_pred_best = best_dt.predict(X_test)
print(f"টেস্ট Accuracy (টিউনিং পর): {accuracy_score(y_test, y_pred_best):.4f}")
print(f"ইমপ্রুভমেন্ট: {(accuracy_score(y_test, y_pred_best) - accuracy_score(y_test, y_pred))*100:.2f}%")
```

### ওভারফিটিং বনাম আন্ডারফিটিং:
```python
print("\n=== ওভারফিটিং বনাম আন্ডারফিটিং ===")

depths = range(1, 21)
train_scores = []
test_scores = []

for depth in depths:
    dt_temp = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt_temp.fit(X_train, y_train)
    train_scores.append(accuracy_score(y_train, dt_temp.predict(X_train)))
    test_scores.append(accuracy_score(y_test, dt_temp.predict(X_test)))

plt.figure(figsize=(10, 6))
plt.plot(depths, train_scores, 'b-', label='ট্রেন Accuracy', linewidth=2)
plt.plot(depths, test_scores, 'r-', label='টেস্ট Accuracy', linewidth=2)
plt.axvline(x=3, color='g', linestyle='--', label='আন্ডারফিট (max_depth=3)')
plt.axvline(x=7, color='orange', linestyle='--', label='ভালো (max_depth=7)')
plt.axvline(x=15, color='purple', linestyle='--', label='ওভারফিট (max_depth=15)')
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('ডিসিশন ট্রি: ডেপ্থ বনাম Accuracy (ওভারফিটিং)')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('decision_tree_overfitting.png')
plt.show()
print("ওভারফিটিং গ্রাফ সেভ করা হয়েছে!")

print(f"\nওভারফিটিং এনালাইসিস:")
print(f"  max_depth=3: ট্রেন={train_scores[2]:.4f}, টেস্ট={test_scores[2]:.4f} (আন্ডারফিট)")
print(f"  max_depth=7: ট্রেন={train_scores[6]:.4f}, টেস্ট={test_scores[6]:.4f} (ভালো)")
print(f"  max_depth=20: ট্রেন={train_scores[19]:.4f}, টেস্ট={test_scores[19]:.4f} (ওভারফিট)")
```

### প্রুনিং (Cost Complexity Pruning):
```python
print("\n=== কস্ট কমপ্লেক্সিটি প্রুনিং ===")

path = dt.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# বিভিন্ন আলফায় মডেল ট্রেন
train_scores_prune = []
test_scores_prune = []

for alpha in ccp_alphas:
    dt_prune = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)
    dt_prune.fit(X_train, y_train)
    train_scores_prune.append(accuracy_score(y_train, dt_prune.predict(X_train)))
    test_scores_prune.append(accuracy_score(y_test, dt_prune.predict(X_test)))

# সেরা আলফা
best_idx = np.argmax(test_scores_prune)
best_alpha = ccp_alphas[best_idx]
print(f"সেরা ccp_alpha: {best_alpha:.6f}")
print(f"সেরা টেস্ট Accuracy: {test_scores_prune[best_idx]:.4f}")

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(ccp_alphas, train_scores_prune, 'b-', label='ট্রেন', linewidth=2)
plt.plot(ccp_alphas, test_scores_prune, 'r-', label='টেস্ট', linewidth=2)
plt.axvline(best_alpha, color='g', linestyle='--', label=f'সেরা α={best_alpha:.6f}')
plt.xlabel('ccp_alpha')
plt.ylabel('Accuracy')
plt.title('কস্ট কমপ্লেক্সিটি প্রুনিং')
plt.legend()
plt.grid(alpha=0.3)

# ট্রি সাইজ
plt.subplot(1, 2, 2)
tree_sizes = [dt_prune.tree_.node_count for dt_prune in 
              [DecisionTreeClassifier(random_state=42, ccp_alpha=alpha).fit(X_train, y_train) 
               for alpha in ccp_alphas]]
plt.plot(ccp_alphas, tree_sizes, 'b-', linewidth=2)
plt.xlabel('ccp_alpha')
plt.ylabel('নোড সংখ্যা')
plt.title('আলফা বনাম ট্রির আকার')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('pruning.png')
plt.show()
print("প্রুনিং গ্রাফ সেভ করা হয়েছে!")
```

### ডিসিশন ট্রি রিগ্রেশন:
```python
print("\n=== ডিসিশন ট্রি রিগ্রেশন ===")

# রিগ্রেশন ডেটা
np.random.seed(42)
X_reg = np.random.rand(100, 1) * 10
y_reg = np.sin(X_reg).ravel() + np.random.normal(0, 0.1, 100)

reg_tree = DecisionTreeRegressor(max_depth=5, random_state=42)
reg_tree.fit(X_reg, y_reg)

X_grid = np.linspace(0, 10, 100).reshape(-1, 1)
y_grid = reg_tree.predict(X_grid)

plt.figure(figsize=(10, 6))
plt.scatter(X_reg, y_reg, alpha=0.5, label='ডেটা')
plt.plot(X_grid, y_grid, 'r-', linewidth=2, label='ডিসিশন ট্রি রিগ্রেশন')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('ডিসিশন ট্রি রিগ্রেশন')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('decision_tree_regression.png')
plt.show()
print("ডিসিশন ট্রি রিগ্রেশন গ্রাফ সেভ করা হয়েছে!")

print(f"R² Score: {reg_tree.score(X_reg, y_reg):.4f}")
```

### ফিচার ইম্পরট্যান্স:
```python
print("\n=== ফিচার ইম্পরট্যান্স ===")

feat_imp = pd.DataFrame({
    'ফিচার': X.columns,
    'ইম্পরট্যান্স': best_dt.feature_importances_
}).sort_values('ইম্পরট্যান্স', ascending=False)

print("ফিচার ইম্পরট্যান্স (জিনি ইম্পরট্যান্স):")
print(feat_imp.to_string(index=False))

plt.figure(figsize=(10, 5))
plt.barh(feat_imp['ফিচার'], feat_imp['ইম্পরট্যান্স'], color='skyblue', edgecolor='black')
plt.xlabel('ফিচার ইম্পরট্যান্স')
plt.title('ডিসিশন ট্রি: ফিচার ইম্পরট্যান্স')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance_dt.png')
plt.show()
print("ফিচার ইম্পরট্যান্স গ্রাফ সেভ করা হয়েছে!")
```

### এনসেম্বল বেসিস - বুটস্ট্র্যাপ:
```python
print("\n=== বুটস্ট্র্যাপ স্যাম্পলিং ===")

def bootstrap_sample(X, y):
    """বুটস্ট্র্যাপ স্যাম্পল (রিস্যাম্পলিং)"""
    n = len(X)
    indices = np.random.choice(n, n, replace=True)
    return X.iloc[indices], y.iloc[indices]

# বুটস্ট্র্যাপ ট্রি
n_trees = 5
for i in range(n_trees):
    X_boot, y_boot = bootstrap_sample(X_train, y_train)
    tree_boot = DecisionTreeClassifier(max_depth=3, random_state=i)
    tree_boot.fit(X_boot, y_boot)
    acc = tree_boot.score(X_test, y_test)
    print(f"  ট্রি {i+1} (বুটস্ট্র্যাপ): Accuracy = {acc:.4f}")

print("\n💡 এটি র্যান্ডম ফরেস্টের বেসিক আইডিয়া!")
```

### ডিসিশন ট্রির সুবিধা ও অসুবিধা:
```python
print("\n=== ডিসিশন ট্রির সুবিধা ও অসুবিধা ===")

print("""
✅ সুবিধা:
   1. সহজে বোঝা ও ব্যাখ্যা করা যায় (হোয়াইট-বক্স মডেল)
   2. ফিচার স্কেলিং প্রয়োজন হয় না
   3. নন-লিনিয়ার সম্পর্ক ধরতে পারে
   4. ফিচার সিলেকশন বিল্ট-ইন
   5. ক্যাটেগোরিকাল ও নিউমেরিক উভয় ডেটা হ্যান্ডল করতে পারে

❌ অসুবিধা:
   1. ওভারফিটিং প্রবণতা (প্রুনিং ও রেগুলারাইজেশন প্রয়োজন)
   2. ছোট পরিবর্তনে বড় ভ্যারিয়েন্স
   3. বায়াসড ট্রি (কিছু ক্লাসের প্রতি পক্ষপাত)
   4. ডেটার ছোট পরিবর্তনে গাছের স্ট্রাকচার বদলে যেতে পারে
   5. গভীর ট্রি বুঝতে কঠিন

⚡ সমাধান:
   - এনসেম্বল মেথড: র্যান্ডম ফরেস্ট, গ্রেডিয়েন্ট বুস্টিং
   - প্রুনিং (ccp_alpha)
   - ম্যাক্স ডেপ্থ, মিন স্যাম্পলস লিমিট
   - ক্রস-ভ্যালিডেশন
""")
```

### সারাংশ:
- **ডিসিশন ট্রি**: গাছের মতো স্ট্রাকচারে সিদ্ধান্ত নেয়
- **জিনি ইমপিউরিটি/এনট্রপি**: স্প্লিট কোয়ালিটি মাপার পদ্ধতি
- **max_depth**: ট্রির গভীরতা নিয়ন্ত্রণ করে (ওভারফিটিং প্রতিরোধ)
- **প্রুনিং**: অপ্রয়োজনীয় শাখা কেটে ট্রিকে সরল করে
- **ফিচার ইম্পরট্যান্স**: কোন ফিচার কতটা গুরুত্বপূর্ণ তা বলে
- **ক্লাসিফিকেশন ও রিগ্রেশন**: উভয় সমস্যার জন্য ব্যবহার করা যায়
- **এনসেম্বল পদ্ধতির ভিত্তি**: র্যান্ডম ফরেস্ট ও বুস্টিং এর মূল কনসেপ্ট