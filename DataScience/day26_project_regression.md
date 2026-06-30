# Day 26: মিনি প্রজেক্ট — রিগ্রেশন অ্যানালাইসিস
## Mini Project: Regression Analysis — হাউজ প্রাইস প্রেডিকশন

### প্রজেক্ট ওভারভিউ
এই প্রজেক্টে আমরা একটি রিয়েল এস্টেট ডেটাসেট নিয়ে লিনিয়ার ও মাল্টিপল রিগ্রেশন মডেল তৈরি করব। লক্ষ্য: বাড়ির বিভিন্ন বৈশিষ্ট্য ব্যবহার করে দাম পূর্বাভাস করা।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             explained_variance_score, mean_absolute_percentage_error)
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')

np.random.seed(42)
```

### স্টেপ ১: ডেটাসেট তৈরি
```python
print("=" * 60)
print("প্রজেক্ট: হাউজ প্রাইস প্রেডিকশন")
print("=" * 60)

print("\n=== স্টেপ ১: ডেটাসেট তৈরি ===")

n_houses = 2000

houses = pd.DataFrame({
    'বাড়ি_আইডি': range(1, n_houses + 1),
    'বর্গফুট': np.random.normal(1800, 600, n_houses).astype(int),
    'বেডরুম': np.random.randint(1, 6, n_houses),
    'বাথরুম': np.random.randint(1, 4, n_houses),
    'বয়স_বছর': np.random.randint(0, 50, n_houses),
    'তলা': np.random.randint(1, 4, n_houses),
    'গ্যারেজ': np.random.choice([0, 1, 2], n_houses, p=[0.3, 0.5, 0.2]),
    'অবস্থান': np.random.choice(['উত্তর', 'দক্ষিণ', 'পূর্ব', 'পশ্চিম', 'মধ্য'], n_houses),
    'স্কোর': np.random.uniform(1, 10, n_houses).round(1)
})

# ফিচার ইঞ্জিনিয়ারিং
houses['মোট_রুম'] = houses['বেডরুম'] + houses['বাথরুম']
houses['বর্গফুট_প্রতি_রুম'] = houses['বর্গফুট'] / houses['মোট_রুম']

# প্রাইস তৈরি (লিনিয়ার রিলেশনশিপ + নয়েজ)
base_price = 50000
price_per_sqft = 200
bedroom_value = 25000
bathroom_value = 15000
age_depreciation = -1000
garage_value = 15000
location_values = {'উত্তর': 20000, 'দক্ষিণ': -10000, 'পূর্ব': 15000, 'পশ্চিম': -5000, 'মধ্য': 30000}

houses['মূল্য'] = (
    base_price +
    houses['বর্গফুট'] * price_per_sqft +
    houses['বেডরুম'] * bedroom_value +
    houses['বাথরুম'] * bathroom_value +
    houses['বয়স_বছর'] * age_depreciation +
    houses['গ্যারেজ'] * garage_value +
    houses['অবস্থান'].map(location_values) +
    houses['স্কোর'] * 5000 +
    np.random.normal(0, 30000, n_houses)
)

houses['মূল্য'] = houses['মূল্য'].clip(lower=50000).astype(int)

print(f"মোট বাড়ি: {len(houses)}")
print(f"ফিচার সংখ্যা: {len(houses.columns)}")
print("\nপ্রথম ৫টি রেকর্ড:")
print(houses.head())
print(f"\nমূল্যের পরিসংখ্যান:\n{houses['মূল্য'].describe()}")
```

### স্টেপ ২: এক্সপ্লোরেটরি ডেটা অ্যানালাইসিস (EDA)
```python
print("\n=== স্টেপ ২: এক্সপ্লোরেটরি ডেটা অ্যানালাইসিস ===")

# মূল্য ডিস্ট্রিবিউশন
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

axes[0, 0].hist(houses['মূল्य'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 0].axvline(houses['মূল্য'].mean(), color='red', linestyle='--', label=f"গড়: ${houses['মূল্য'].mean():.0f}")
axes[0, 0].set_title('মূল্য ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 0].set_xlabel('মূল্য ($)')
axes[0, 0].set_ylabel('ফ্রিকোয়েন্সি')
axes[0, 0].legend()

# বর্গফুট vs মূল্য
axes[0, 1].scatter(houses['বর্গফুট'], houses['মূল্য'], alpha=0.5, s=20, c='green')
axes[0, 1].set_title('বর্গফুট vs মূল্য', fontsize=12)
axes[0, 1].set_xlabel('বর্গফুট')
axes[0, 1].set_ylabel('মূল্য')

# বেডরুম vs মূল্য
houses.boxplot(column='মূল্য', by='বেডরুম', ax=axes[0, 2])
axes[0, 2].set_title('বেডরুম সংখ্যা vs মূল্য', fontsize=12)
axes[0, 2].set_xlabel('বেডরুম')
axes[0, 2].set_ylabel('মূল্য')

# অবস্থান vs মূল্য
houses.boxplot(column='মূল্য', by='অবস্থান', ax=axes[1, 0])
axes[1, 0].set_title('অবস্থান vs মূল্য', fontsize=12)
axes[1, 0].set_xlabel('অবস্থান')
axes[1, 0].set_ylabel('মূল্য')
axes[1, 0].tick_params(axis='x', rotation=45)

# বয়স vs মূল্য
axes[1, 1].scatter(houses['বয়স_বছর'], houses['মূল্য'], alpha=0.5, s=20, c='coral')
axes[1, 1].set_title('বয়স vs মূল্য', fontsize=12)
axes[1, 1].set_xlabel('বয়স (বছর)')
axes[1, 1].set_ylabel('মূল্য')

# স্কোর vs মূল্য
axes[1, 2].scatter(houses['স্কোর'], houses['মূল্য'], alpha=0.5, s=20, c='purple')
axes[1, 2].set_title('স্কোর vs মূল্য', fontsize=12)
axes[1, 2].set_xlabel('স্কোর')
axes[1, 2].set_ylabel('মূল্য')

plt.suptitle('EDA: হাউজ প্রাইস ডেটা ভিজুয়ালাইজেশন', fontsize=14)
plt.tight_layout()
plt.savefig('project_regression_eda.png', dpi=100)
plt.show()
```

### স্টেপ ৩: কোরিলেশন অ্যানালাইসিস
```python
print("\n=== স্টেপ ৩: কোরিলেশন অ্যানালাইসিস ===")

# এনকোডিং
houses_encoded = houses.copy()
le = LabelEncoder()
houses_encoded['অবস্থান_এনকোড'] = le.fit_transform(houses['অবস্থান'])

# নিউমেরিক ফিচার নির্বাচন
numeric_cols = ['বর্গফুট', 'বেডরুম', 'বাথরুম', 'বয়স_বছর', 'তলা', 'গ্যারেজ', 
                'স্কোর', 'মোট_রুম', 'বর্গফুট_প্রতি_রুম', 'অবস্থান_এনকোড', 'মূল্য']

corr_matrix = houses_encoded[numeric_cols].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu', center=0, 
            fmt='.2f', square=True, linewidths=0.5)
plt.title('ফিচার কোরিলেশন ম্যাট্রিক্স', fontsize=14)
plt.tight_layout()
plt.savefig('project_regression_corr.png', dpi=100)
plt.show()

# মূল্যের সাথে কোরিলেশন
print("মূল্যের সাথে ফিচার কোরিলেশন:")
price_corr = corr_matrix['মূল্য'].drop('মূল্য').sort_values(ascending=False)
for feat, corr_val in price_corr.items():
    strength = 'শক্তিশালী' if abs(corr_val) > 0.5 else 'মধ্যম' if abs(corr_val) > 0.3 else 'দুর্বল'
    print(f"  {feat}: {corr_val:.3f} ({strength})")
```

### স্টেপ ৪: ডেটা প্রিপ্রসেসিং
```python
print("\n=== স্টেপ ৪: ডেটা প্রিপ্রসেসিং ===")

# ফিচার ও টার্গেট
feature_cols = ['বর্গফুট', 'বেডরুম', 'বাথরুম', 'বয়স_বছর', 'তলা', 'গ্যারেজ', 'স্কোর']
X = houses[feature_cols]
y = houses['মূল্য']

# ট্রেন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"ট্রেনিং সেট: {X_train.shape}")
print(f"টেস্ট সেট: {X_test.shape}")

# স্কেলিং
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nস্কেলিংয়ের পর ট্রেন ডেটা পরিসংখ্যান:")
print(f"  গড়: {X_train_scaled.mean(axis=0).round(4)}")
print(f"  স্ট্যান্ডার্ড ডিভিয়েশন: {X_train_scaled.std(axis=0).round(4)}")
```

### স্টেপ ৫: মডেল বিল্ডিং ও ট্রেনিং
```python
print("\n=== স্টেপ ৫: মডেল বিল্ডিং ও ট্রেনিং ===")

models = {
    'লিনিয়ার রিগ্রেশন': LinearRegression(),
    'Ridge রিগ্রেশন': Ridge(alpha=1.0, random_state=42),
    'Lasso রিগ্রেশন': Lasso(alpha=1.0, random_state=42),
    'ElasticNet': ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    
    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2, 'MAPE': mape}
    
    print(f"\n{name}:")
    print(f"  MAE: ${mae:,.0f}")
    print(f"  RMSE: ${rmse:,.0f}")
    print(f"  R²: {r2:.4f}")
    print(f"  MAPE: {mape:.2%}")
```

### স্টেপ ৬: মডেল ইভালুয়েশন তুলনা
```python
print("\n=== স্টেপ ৬: মডেল ইভালুয়েশন তুলনা ===")

results_df = pd.DataFrame(results).T
print("মডেল তুলনা টেবিল:")
print(results_df.round(2))

# ভিজুয়ালাইজেশন
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# R² তুলনা
results_df['R2'].plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title('R² স্কোর তুলনা', fontsize=12)
axes[0].set_ylabel('R²')
axes[0].set_ylim(0, 1)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# RMSE তুলনা
results_df['RMSE'].plot(kind='bar', ax=axes[1], color='coral', edgecolor='black')
axes[1].set_title('RMSE তুলনা (কম = ভালো)', fontsize=12)
axes[1].set_ylabel('RMSE ($)')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('project_regression_comparison.png', dpi=100)
plt.show()

# সেরা মডেল
best_model_name = results_df['R2'].idxmax()
best_r2 = results_df.loc[best_model_name, 'R2']
print(f"\n🏆 সেরা মডেল: {best_model_name} (R² = {best_r2:.4f})")
```

### স্টেপ ৭: এনসেম্বল মডেল
```python
print("\n=== স্টেপ ৭: এনসেম্বল মডেল ===")

ensemble_models = {
    'Decision Tree': DecisionTreeRegressor(max_depth=10, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

for name, model in ensemble_models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"{name}:")
    print(f"  R²: {r2:.4f}")
    print(f"  RMSE: ${rmse:,.0f}")
```

### স্টেপ ৮: বেস্ট মডেলের বিস্তারিত অ্যানালাইসিস
```python
print("\n=== স্টেপ ৮: বেস্ট মডেলের বিস্তারিত অ্যানালাইসিস ===")

# Random Forest সেরা মডেল
best_model = RandomForestRegressor(n_estimators=100, random_state=42)
best_model.fit(X_train_scaled, y_train)
y_pred_best = best_model.predict(X_test_scaled)

# রেসিডুয়াল অ্যানালাইসিস
residuals = y_test - y_pred_best

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Actual vs Predicted
axes[0, 0].scatter(y_test, y_pred_best, alpha=0.5, s=30, c='steelblue')
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                'r--', linewidth=2, label='পারফেক্ট ফিট')
axes[0, 0].set_title('আসল vs পূর্বাভাসিত মূল্য', fontsize=12)
axes[0, 0].set_xlabel('আসল মূল্য ($)')
axes[0, 0].set_ylabel('পূর্বাভাসিত মূল্য ($)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# রেসিডুয়াল ডিস্ট্রিবিউশন
axes[0, 1].hist(residuals, bins=40, edgecolor='black', alpha=0.7, color='coral')
axes[0, 1].axvline(0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_title('রেসিডুয়াল ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 1].set_xlabel('রেসিডুয়াল ($)')
axes[0, 1].set_ylabel('ফ্রিকোয়েন্সি')

# রেসিডুয়াল vs প্রেডিক্টেড
axes[1, 0].scatter(y_pred_best, residuals, alpha=0.5, s=30, c='green')
axes[1, 0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_title('রেসিডুয়াল vs প্রেডিক্টেড', fontsize=12)
axes[1, 0].set_xlabel('পূর্বাভাসিত মূল্য ($)')
axes[1, 0].set_ylabel('রেসিডুয়াল ($)')
axes[1, 0].grid(True, alpha=0.3)

# ফিচার ইম্পরট্যান্স
importances = best_model.feature_importances_
indices = np.argsort(importances)[::-1]
axes[1, 1].barh(range(len(indices)), importances[indices], color='steelblue', edgecolor='black')
axes[1, 1].set_yticks(range(len(indices)))
axes[1, 1].set_yticklabels([feature_cols[i] for i in indices])
axes[1, 1].set_title('ফিচার ইম্পরট্যান্স', fontsize=12)
axes[1, 1].set_xlabel('ইম্পরট্যান্স')

plt.tight_layout()
plt.savefig('project_regression_analysis.png', dpi=100)
plt.show()
```

### স্টেপ ৯: নতুন ডেটা প্রেডিকশন
```python
print("\n=== স্টেপ ৯: নতুন ডেটা প্রেডিকশন ===")

new_houses = pd.DataFrame({
    'বর্গফুট': [1500, 2200, 1800],
    'বেডরুম': [2, 4, 3],
    'বাথরুম': [1, 3, 2],
    'বয়স_বছর': [5, 15, 25],
    'তলা': [1, 2, 1],
    'গ্যারেজ': [1, 2, 1],
    'স্কোর': [7.5, 8.2, 6.0]
})

new_houses_scaled = scaler.transform(new_houses)
predictions = best_model.predict(new_houses_scaled)

print("নতুন বাড়ির দাম পূর্বাভাস:")
for i, row in new_houses.iterrows():
    print(f"\nবাড়ি {i+1}:")
    print(f"  বর্গফুট: {row['বর্গফুট']}")
    print(f"  বেডরুম: {row['বেডরুম']}, বাথরুম: {row['বাথরুম']}")
    print(f"  বয়স: {row['বয়স_বছর']} বছর")
    print(f"  📌 পূর্বাভাসিত মূল্য: ${predictions[i]:,.0f}")
```

### সারসংক্ষেপ ও শেখার পয়েন্ট
```python
print("\n" + "=" * 60)
print("প্রজেক্ট সারসংক্ষেপ")
print("=" * 60)

summary = """
## এই প্রজেক্ট থেকে যা শিখলাম:

✅ সম্পূর্ণ রিগ্রেশন পাইপলাইন:
   1. ডেটাসেট তৈরি ও ফিচার ইঞ্জিনিয়ারিং
   2. EDA ও কোরিলেশন অ্যানালাইসিস
   3. ডেটা প্রিপ্রসেসিং ও স্কেলিং
   4. একাধিক মডেল ট্রেনিং ও তুলনা
   5. রেসিডুয়াল অ্যানালাইসিস
   6. ফিচার ইম্পরট্যান্স অ্যানালাইসিস

✅ বেস্ট মডেল: Random Forest Regressor
   - এনসেম্বল মডেল ওভারফিটিং কমায়
   - নন-লিনিয়ার রিলেশনশিপ ধরতে পারে
   - ফিচার ইম্পরট্যান্স প্রদান করে

✅ R² মেট্রিক ব্যাখ্যা:
   - 1.0 = পারফেক্ট প্রেডিকশন
   - 0.0 = গড় ভ্যালু প্রেডিক্ট করার সমান
   - নেগেটিভ = খুব খারাপ মডেল

## Data Analyst-এর জন্য Takeaways:
📌 সবসময় একাধিক মডেল ট্রাই করুন
📌 ফিচার ইঞ্জিনিয়ারিং মডেলের চেয়েও গুরুত্বপূর্ণ
📌 রেসিডুয়াল চেক করা অত্যাবশ্যক
📌 স্কেলিং রিগ্রেশনের জন্য গুরুত্বপূর্ণ
📌 মডেল ইন্টারপ্রিটেবিলিটি vs পারফরম্যান্স - ট্রেডঅফ
"""
print(summary)
```