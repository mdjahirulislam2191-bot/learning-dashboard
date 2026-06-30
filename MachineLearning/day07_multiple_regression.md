# Day 07: মাল্টিপল রিগ্রেশন
## Multiple Regression

### মাল্টিপল রিগ্রেশন কি?
একাধিক স্বাধীন ভেরিয়েবল ব্যবহার করে নির্ভরশীল ভেরিয়েবল পূর্বাভাস করা।

**সমীকরণ:** y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε

### ফাইন্যান্স উদাহরণ: হাউজিং প্রাইস প্রেডিকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import f_regression

# হাউজিং ডেটা (ফাইন্যান্সিয়াল কনটেক্সট)
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'sqft': np.random.normal(1500, 500, n),
    'bedrooms': np.random.randint(1, 6, n),
    'bathrooms': np.random.randint(1, 4, n),
    'age': np.random.randint(0, 50, n),
    'location_score': np.random.uniform(1, 10, n),
    'income_median': np.random.normal(60000, 15000, n),
    'interest_rate': np.random.uniform(3.0, 7.0, n),
    'crime_rate': np.random.uniform(0.1, 5.0, n)
})

# টার্গেট: হাউজিং প্রাইস (বাস্তবসম্মত সম্পর্ক)
data['price'] = (
    50000 +
    data['sqft'] * 150 +
    data['bedrooms'] * 20000 +
    data['bathrooms'] * 15000 -
    data['age'] * 1000 +
    data['location_score'] * 30000 -
    data['crime_rate'] * 8000 +
    np.random.randn(n) * 20000
)

print(data.head())
print(f"\nপ্রাইস রেঞ্জ: ${data['price'].min():.0f} - ${data['price'].max():.0f}")
```

### মাল্টিপল রিগ্রেশন মডেল
```python
# ফিচার এবং টার্গেট
features = ['sqft', 'bedrooms', 'bathrooms', 'age', 'location_score', 
            'income_median', 'interest_rate', 'crime_rate']
X = data[features]
y = data['price']

# স্কেলিং (মাল্টিপল রিগ্রেশনের জন্য গুরুত্বপূর্ণ)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=features)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# মডেল
model = LinearRegression()
model.fit(X_train, y_train)
```

### কোএফিসিয়েন্ট বিশ্লেষণ
```python
# কোএফিসিয়েন্ট এবং P-ভ্যালু
coeff_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_,
    'Abs_Coefficient': np.abs(model.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

print("📊 Feature Importance (Standardized):")
print(coeff_df.to_string(index=False))

# F-statistics
f_stats, p_values = f_regression(X_train, y_train)
print("\n📈 F-Statistics & P-Values:")
for feat, f_stat, p_val in zip(features, f_stats, p_values):
    sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else ''
    print(f"  {feat:15s}: F={f_stat:.2f}, p={p_val:.4f} {sig}")
```

### মডেল ইভালুয়েশন
```python
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
adj_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)

print(f"\n📊 Model Performance:")
print(f"R²:                {r2:.4f}")
print(f"Adjusted R²:       {adj_r2:.4f}")
print(f"RMSE:             ${np.sqrt(mean_squared_error(y_test, y_pred)):,.0f}")
print(f"Mean Price:       ${y_test.mean():,.0f}")
print(f"RMSE/Mean Ratio:   {np.sqrt(mean_squared_error(y_test, y_pred))/y_test.mean():.2%}")
```

### Cross-Validation
```python
cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
print(f"\n🔄 Cross-Validation R² Scores: {cv_scores}")
print(f"Mean CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
```

### Multicolinearity চেক (VIF)
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF গণনা
vif_data = pd.DataFrame()
vif_data['Feature'] = features
vif_data['VIF'] = [variance_inflation_factor(X_scaled.values, i) for i in range(X_scaled.shape[1])]

print("\n🔍 Variance Inflation Factor (VIF):")
print(vif_data)
print("\n⚠️ VIF > 10 → Severe multicolinearity")
```

### ফাইন্যান্সিয়াল ইন্টারপ্রিটেশন
```python
# কোএফিসিয়েন্ট ইন্টারপ্রিটেশন
print("📋 Coefficient Interpretation:")
print("1 স্ট্যান্ডার্ড ডেভিয়েশন পরিবর্তনে প্রাইসের পরিবর্তন:")
for feat, coef in zip(features, model.coef_):
    direction = "📈 বৃদ্ধি" if coef > 0 else "📉 হ্রাস"
    print(f"  {feat:15s}: ${abs(coef):,.0f} ({direction})")
```

### Feature Selection টেকনিক
```python
# Backward Elimination
import statsmodels.api as sm

def backward_elimination(data, target, significance_level=0.05):
    X = data.copy()
    y = target.copy()
    
    while True:
        X_with_const = sm.add_constant(X)
        model = sm.OLS(y, X_with_const).fit()
        p_values = model.pvalues.iloc[1:]  # const বাদে
        
        max_p = p_values.max()
        if max_p > significance_level:
            excluded = p_values.idxmax()
            print(f"Removing {excluded} (p={max_p:.4f})")
            X = X.drop(excluded, axis=1)
        else:
            break
    
    return X.columns.tolist()

selected_features = backward_elimination(data[features], y)
print(f"\n✅ Selected Features: {selected_features}")
```

### সারসংক্ষেপ
মাল্টিপল রিগ্রেশন একাধিক ফিচার ব্যবহার করে প্রেডিকশন করে। ফাইন্যান্সে হাউজিং প্রাইস, স্টক প্রেডিকশন, এবং রিস্ক অ্যানালাইসিসে ব্যবহৃত হয়। VIF, P-ভ্যালু, এবং Adjusted R² গুরুত্বপূর্ণ মেট্রিক্স।