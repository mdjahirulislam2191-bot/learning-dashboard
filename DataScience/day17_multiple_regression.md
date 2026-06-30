# Day 17: মাল্টিপল রিগ্রেশন
## Multiple Regression

### মাল্টিপল রিগ্রেশন কী?
মাল্টিপল রিগ্রেশন লিনিয়ার রিগ্রেশনের এক্সটেনশন যেখানে একাধিক ইন্ডিপেন্ডেন্ট ভ্যারিয়েবল ব্যবহার করে ডিপেন্ডেন্ট ভ্যারিয়েবল প্রেডিক্ট করা হয়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# বাস্তবিক ডেটাসেট: বাড়ির দাম নির্ধারণ
np.random.seed(42)
n = 500

df = pd.DataFrame({
    'বেডরুম': np.random.randint(1, 6, n),
    'বাথরুম': np.random.randint(1, 4, n),
    'স্কয়ার_ফুট': np.random.randint(500, 4000, n),
    'বয়স': np.random.randint(0, 50, n),
    'গ্যারেজ': np.random.randint(0, 3, n),
    'লোকেশন_স্কোর': np.random.uniform(1, 10, n),  # 1-10 স্কোর
    'স্কুল_দূরত্ব_কিমি': np.random.uniform(0.5, 10, n),
    'মার্কেট_দূরত্ব_কিমি': np.random.uniform(0.2, 5, n),
})

# দাম তৈরি (রিয়েলিস্টিক)
df['দাম'] = (
    50000 + 
    150 * df['স্কয়ার_ফুট'] + 
    20000 * df['বেডরুম'] + 
    15000 * df['বাথরুম'] - 
    2000 * df['বয়স'] + 
    10000 * df['গ্যারেজ'] + 
    15000 * df['লোকেশন_স্কোর'] - 
    5000 * df['স্কুল_দূরত্ব_কিমি'] - 
    3000 * df['মার্কেট_দূরত্ব_কিমি'] +
    np.random.normal(0, 30000, n)
)
df['দাম'] = df['দাম'].astype(int)

print("=== মাল্টিপল রিগ্রেশন ডেটাসেট ===")
print(df.head())
print(f"\nডেটা শেপ: {df.shape}")
print(f"\nপরিসংখ্যান:")
print(df.describe())
```

### মাল্টিপল রিগ্রেশন মডেল:
```python
print("\n=== মাল্টিপল রিগ্রেশন মডেল ===")

X = df.drop('দাম', axis=1)
y = df['দাম']

# ট্রেন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"ট্রেন সেট: {X_train.shape}")
print(f"টেস্ট সেট: {X_test.shape}")

# মডেল ট্রেনিং
model = LinearRegression()
model.fit(X_train, y_train)

# কোফিসিয়েন্ট
coef_df = pd.DataFrame({
    'ফিচার': X.columns,
    'কোফিসিয়েন্ট': model.coef_,
    'পরম_প্রভাব': np.abs(model.coef_)
}).sort_values('পরম_প্রভাব', ascending=False)

print(f"\nফিচার কোফিসিয়েন্টসমূহ:")
print(coef_df.to_string(index=False))
print(f"\nইন্টারসেপ্ট: {model.intercept_:.2f}")
print(f"\nসমানীকরণ: দাম = {model.intercept_:.2f} + ...")
for i, f in enumerate(X.columns):
    print(f"  {'+' if model.coef_[i] > 0 else ''}{model.coef_[i]:.2f} × {f}")
```

### মডেল ইভালুয়েশন:
```python
print("\n=== মডেল ইভালুয়েশন ===")

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# ট্রেন সেট
train_r2 = r2_score(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)

# টেস্ট সেট
test_r2 = r2_score(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)

print(f"{'মেট্রিক':<15} {'ট্রেন':<15} {'টেস্ট':<15}")
print("-" * 45)
print(f"{'R²':<15} {train_r2:<15.4f} {test_r2:<15.4f}")
print(f"{'RMSE':<15} {train_rmse:<15.2f} {test_rmse:<15.2f}")
print(f"{'MAE':<15} {train_mae:<15.2f} {test_mae:<15.2f}")
print(f"{'অ্যাডজাস্টেড R²':<15} {1-(1-train_r2)*(n-1)/(n-X.shape[1]-1):.4f}")

# ওভারফিটিং চেক
print(f"\nওভারফিটিং চেক:")
print(f"  R² পার্থক্য (ট্রেন-টেস্ট): {train_r2 - test_r2:.4f}")
```

### মাল্টিকোলিনিয়ারিটি চেক (VIF):
```python
print("\n=== মাল্টিকোলিনিয়ারিটি চেক ===")

# VIF (Variance Inflation Factor)
X_sm = sm.add_constant(X)
vif_data = pd.DataFrame()
vif_data['ফিচার'] = X_sm.columns
vif_data['VIF'] = [variance_inflation_factor(X_sm.values, i) for i in range(X_sm.shape[1])]
print("VIF বিশ্লেষণ (VIF > 10 → মাল্টিকোলিনিয়ারিটি):")
print(vif_data)

# করিলেশন ম্যাট্রিক্স
plt.figure(figsize=(10, 8))
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('ফিচার করিলেশন ম্যাট্রিক্স')
plt.tight_layout()
plt.savefig('correlation_matrix_multiple.png')
plt.show()
print("\nকরিলেশন ম্যাট্রিক্স সেভ করা হয়েছে!")
```

### ফিচার ইম্পরট্যান্স:
```python
print("\n=== ফিচার ইম্পরট্যান্স ===")

# কোফিসিয়েন্টের ভিত্তিতে ইম্পরট্যান্স
coef_df['ফিচার_ইম্পরট্যান্স'] = np.abs(coef_df['কোফিসিয়েন্ট']) / np.abs(coef_df['কোফিসিয়েন্ট']).sum() * 100
print("ফিচার ইম্পরট্যান্স (কোফিসিয়েন্টের ভিত্তিতে):")
print(coef_df[['ফিচার', 'কোফিসিয়েন্ট', 'ফিচার_ইম্পরট্যান্স']].to_string(index=False))

# প্লট
plt.figure(figsize=(10, 5))
plt.barh(coef_df['ফিচার'], coef_df['কোফিসিয়েন্ট'])
plt.xlabel('কোফিসিয়েন্ট ভ্যালু')
plt.title('ফিচার ইম্পরট্যান্স')
plt.axvline(x=0, color='red', linestyle='--')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()
```

### ফরোয়ার্ড/ব্যাকওয়ার্ড ফিচার সিলেকশন:
```python
print("\n=== ফিচার সিলেকশন ===")

from sklearn.feature_selection import SequentialFeatureSelector

# ফরোয়ার্ড সিলেকশন
sfs_forward = SequentialFeatureSelector(
    LinearRegression(), 
    n_features_to_select=5, 
    direction='forward',
    cv=5
)
sfs_forward.fit(X_train, y_train)

print("ফরোয়ার্ড সিলেকশন (৫টি ফিচার):")
selected_features = X.columns[sfs_forward.get_support()].tolist()
print(f"সিলেক্টেড ফিচার: {selected_features}")

# সিলেক্টেড ফিচার দিয়ে মডেল
X_train_sel = X_train[selected_features]
X_test_sel = X_test[selected_features]

model_sel = LinearRegression()
model_sel.fit(X_train_sel, y_train)
y_test_pred_sel = model_sel.predict(X_test_sel)

print(f"\nসিলেক্টেড ফিচার R²: {r2_score(y_test, y_test_pred_sel):.4f}")
print(f"সম্পূর্ণ মডেল R²: {r2_score(y_test, y_test_pred):.4f}")
```

### ইন্টারঅ্যাকশন ইফেক্ট:
```python
print("\n=== ইন্টারঅ্যাকশন ইফেক্ট ===")

# ইন্টারঅ্যাকশন ফিচার: বেডরুম × স্কয়ার_ফুট
df['বেডরুম_স্কয়ার_ইন্টারঅ্যাকশন'] = df['বেডরুম'] * df['স্কয়ার_ফুট']

X_int = df.drop('দাম', axis=1)
y_int = df['দাম']

X_train_int, X_test_int, y_train_int, y_test_int = train_test_split(X_int, y_int, test_size=0.2, random_state=42)

model_int = LinearRegression()
model_int.fit(X_train_int, y_train_int)
y_test_pred_int = model_int.predict(X_test_int)

print(f"ইন্টারঅ্যাকশন ছাড়া R²: {test_r2:.4f}")
print(f"ইন্টারঅ্যাকশন সহ R²: {r2_score(y_test_int, y_test_pred_int):.4f}")
print(f"ইমপ্রুভমেন্ট: {(r2_score(y_test_int, y_test_pred_int) - test_r2) * 100:.2f}%")
```

### স্ট্যাটিস্টিকাল সিগনিফিকেন্স:
```python
print("\n=== স্ট্যাটিস্টিকাল সিগনিফিকেন্স ===")

X_sm = sm.add_constant(X)
sm_model = sm.OLS(y, X_sm).fit()
print(sm_model.summary())

# সিগনিফিকেন্ট ফিচার
p_values = sm_model.pvalues
sig_features = p_values[p_values < 0.05]
print(f"\nস্ট্যাটিস্টিকালি সিগনিফিকেন্ট ফিচার (p < 0.05):")
for feature, p_val in sig_features.items():
    if feature != 'const':
        print(f"  ✅ {feature}: p = {p_val:.6f}")
non_sig = p_values[p_values >= 0.05]
for feature, p_val in non_sig.items():
    if feature != 'const':
        print(f"  ❌ {feature}: p = {p_val:.4f} (সিগনিফিকেন্ট নয়)")
```

### ক্রস-ভ্যালিডেশন:
```python
print("\n=== ক্রস-ভ্যালিডেশন ===")

cv_scores = cross_val_score(LinearRegression(), X, y, cv=10, scoring='r2')
print(f"১০-ফোল্ড ক্রস-ভ্যালিডেশন R²:")
print(f"  প্রতিটি ফোল্ডের স্কোর: {cv_scores}")
print(f"  গড় R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

cv_rmse_scores = -cross_val_score(LinearRegression(), X, y, cv=10, scoring='neg_root_mean_squared_error')
print(f"\n  গড় RMSE: {cv_rmse_scores.mean():.2f} ± {cv_rmse_scores.std():.2f}")
```

### রেসিডুয়াল অ্যানালাইসিস:
```python
print("\n=== রেসিডুয়াল অ্যানালাইসিস ===")

residuals = y_test - y_test_pred

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.scatter(y_test_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('প্রেডিক্টেড দাম')
plt.ylabel('রেসিডুয়াল')
plt.title('রেসিডুয়াল vs প্রেডিক্টেড')

plt.subplot(1, 3, 2)
plt.hist(residuals, bins=20, edgecolor='black', alpha=0.7)
plt.axvline(x=0, color='r', linestyle='--')
plt.xlabel('রেসিডুয়াল')
plt.ylabel('ফ্রিকোয়েন্সি')
plt.title('রেসিডুয়াল ডিস্ট্রিবিউশন')

# QQ প্লট
plt.subplot(1, 3, 3)
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q প্লট')

plt.tight_layout()
plt.savefig('residual_analysis.png')
plt.show()
print("রেসিডুয়াল অ্যানালাইসিস গ্রাফ সেভ করা হয়েছে!")
```

### প্রেডিকশন উদাহরণ:
```python
print("\n=== প্রেডিকশন উদাহরণ ===")

# নতুন বাড়ির বৈশিষ্ট্য
new_houses = pd.DataFrame([
    {'বেডরুম': 3, 'বাথরুম': 2, 'স্কয়ার_ফুট': 1500, 'বয়স': 5, 
     'গ্যারেজ': 1, 'লোকেশন_স্কোর': 8, 'স্কুল_দূরত্ব_কিমি': 1.5, 'মার্কেট_দূরত্ব_কিমি': 0.5},
    {'বেডরুম': 4, 'বাথরুম': 3, 'স্কয়ার_ফুট': 2500, 'বয়স': 2, 
     'গ্যারেজ': 2, 'লোকেশন_স্কোর': 9, 'স্কুল_দূরত্ব_কিমি': 1.0, 'মার্কেট_দূরত্ব_কিমি': 0.3},
    {'বেডরুম': 2, 'বাথরুম': 1, 'স্কয়ার_ফুট': 800, 'বয়স': 25, 
     'গ্যারেজ': 0, 'লোকেশন_স্কোর': 4, 'স্কুল_দূরত্ব_কিমি': 5.0, 'মার্কেট_দূরত্ব_কিমি': 2.5}
])

predicted_prices = model.predict(new_houses)

for i, house in new_houses.iterrows():
    print(f"\nবাড়ি {i+1}: {house['বেডরুম']} বেড, {house['বাথরুম']} বাথ, {house['স্কয়ার_ফুট']} স্কয়ার ফুট")
    print(f"  পূর্বাভাসিত দাম: {predicted_prices[i]:,.2f} টাকা")
```

### মডেল ইন্টারপ্রিটেশন:
```python
print("\n=== মডেল ইন্টারপ্রিটেশন ===")

print("মাল্টিপল রিগ্রেশন ইন্টারপ্রিটেশন:")
print("-" * 50)

# সবচেয়ে শক্তিশালী ফিচার কোফিসিয়েন্ট
top_feature = coef_df.iloc[0]
print(f"➤ '{top_feature['ফিচার']}' সবচেয়ে শক্তিশালী ফিচার")
print(f"  {top_feature['ফিচার']} ১ ইউনিট বাড়লে দাম {top_feature['কোফিসিয়ент']:.2f} টাকা বাড়ে (অন্য ফিচার স্থির থাকলে)")

# বেশি গুরুত্বপূর্ণ নেগেটিভ ফিচার
neg_features = coef_df[coef_df['কোফিসিয়েন্ট'] < 0]
if len(neg_features) > 0:
    print(f"\n➤ নেগেটিভ প্রভাব আছে এমন ফিচার:")
    for _, row in neg_features.iterrows():
        print(f"  {row['ফিচার']}: {row['কোফিসিয়েন্ট']:.2f} (বাড়লে দাম কমে)")

print(f"\n➤ মডেল ব্যাখ্যা করে: {test_r2*100:.2f}% ভ্যারিয়েন্স")
print(f"➤ গড় প্রেডিকশন ত্রুটি: {test_rmse:,.2f} টাকা")
```

### সংক্ষিপ্তকরণ:
```python
print("\n=== সংক্ষিপ্তকরণ ===")

comparison = pd.DataFrame({
    'মেট্রিক': ['R²', 'অ্যাডজাস্টেড R²', 'RMSE', 'MAE', 'ফিচার সংখ্যা'],
    'মান': [f'{test_r2:.4f}', f'{1-(1-train_r2)*(n-1)/(n-X.shape[1]-1):.4f}', 
            f'{test_rmse:,.2f}', f'{test_mae:,.2f}', f'{X.shape[1]}']
})
print(comparison.to_string(index=False))
```

### সারাংশ:
- **মাল্টিপল রিগ্রেশন** একাধিক ফিচার ব্যবহার করে প্রেডিকশন করে
- **কোফিসিয়েন্ট** প্রতিটি ফিচারের আলাদা প্রভাব দেখায় (ceteris paribus)
- **VIF** মাল্টিকোলিনিয়ারিটি চেক করে (VIF > 10 হলে সমস্যা)
- **অ্যাডজাস্টেড R²** বেশি ফিচারের জন্য পেনাল্টি দেয়
- **ক্রস-ভ্যালিডেশন** মডেলের জেনারেলাইজেশন ক্ষমতা যাচাই করে
- ফিচার সিলেকশন, ইন্টারঅ্যাকশন ও পলিনমিয়াল ফিচার মডেল উন্নত করতে পারে
