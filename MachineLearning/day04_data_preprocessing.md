# Day 04: ডেটা প্রিপ্রসেসিং
## Data Preprocessing

### ডেটা প্রিপ্রসেসিং কেন গুরুত্বপূর্ণ?
ডেটা সায়েন্স এবং ML-এ সাফল্যের ৮০% নির্ভর করে ডেটা প্রিপ্রসেসিং এর উপর। খারাপ ডেটা = খারাপ মডেল।

### মূল স্টেপসমূহ
1. **Missing Values Handling** - অনুপস্থিত মান ব্যবস্থাপনা
2. **Outlier Detection** - আউটলায়ার শনাক্তকরণ
3. **Feature Scaling** - ফিচার স্কেলিং
4. **Encoding** - ক্যাটেগরিক্যাল ডেটা এনকোডিং
5. **Feature Engineering** - নতুন ফিচার তৈরি

### ফাইন্যান্স ডেটা সহ উদাহরণ
```python
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# বাস্তবসম্মত ফাইন্যান্স ডেটা (Missing Values সহ)
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'customer_id': range(1, n+1),
    'age': np.random.randint(22, 70, n),
    'annual_income': np.random.normal(60000, 20000, n),
    'credit_score': np.random.randint(300, 850, n),
    'loan_amount': np.random.exponential(15000, n),
    'loan_term_months': np.random.choice([12, 24, 36, 48, 60], n),
    'default_history': np.random.choice([0, 1], n, p=[0.85, 0.15]),
    'employment_years': np.random.exponential(8, n),
    'debt_to_income': np.random.uniform(0.1, 0.6, n)
})

# ইচ্ছাকৃতভাবে Missing Values যোগ করা
for col in ['annual_income', 'credit_score', 'employment_years', 'debt_to_income']:
    missing_idx = np.random.choice(n, int(n*0.05), replace=False)
    data.loc[missing_idx, col] = np.nan

print("মিসিং ভ্যালু কাউন্ট:")
print(data.isnull().sum())
print(f"\nডেটার আকৃতি: {data.shape}")
```

### 1. Missing Values Handling
```python
# অপশন 1: ড্রপ করা
data_dropped = data.dropna()

# অপশন 2: মিন/মিডিয়ান/মোড দিয়ে পূরণ
imputer_mean = SimpleImputer(strategy='mean')
imputer_median = SimpleImputer(strategy='median')
imputer_mode = SimpleImputer(strategy='most_frequent')

# মিন ইম্পিউটেশন (সংখ্যাসূচক কলামের জন্য)
numeric_cols = ['annual_income', 'credit_score', 'employment_years', 'debt_to_income']
data[numeric_cols] = imputer_mean.fit_transform(data[numeric_cols])

# ফরোয়ার্ড ফিল (টাইম সিরিজের জন্য)
# data['stock_price'].fillna(method='ffill', inplace=True)

print("মিসিং ভ্যালু পূরণের পর:")
print(data.isnull().sum())
```

### 2. Outlier Detection
```python
# IQR পদ্ধতি
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# লোন অ্যামাউন্টে আউটলায়ার চেক
outliers, lb, ub = detect_outliers_iqr(data, 'loan_amount')
print(f"লোন অ্যামাউন্টে আউটলায়ার কাউন্ট: {len(outliers)}")
print(f"Normal Range: {lb:.2f} - {ub:.2f}")

# Z-Score পদ্ধতি
from scipy import stats
z_scores = np.abs(stats.zscore(data['annual_income']))
outliers_z = data[z_scores > 3]
print(f"Z-Score পদ্ধতিতে আউটলায়ার: {len(outliers_z)}")
```

### 3. Feature Scaling
```python
# StandardScaler (Z-score normalization)
scaler_standard = StandardScaler()
data_scaled_standard = scaler_standard.fit_transform(data[numeric_cols])

# MinMaxScaler (0-1 range)
scaler_minmax = MinMaxScaler()
data_scaled_minmax = scaler_minmax.fit_transform(data[numeric_cols])

print("স্ট্যান্ডার্ড স্কেলিং (প্রথম ৫ সারি):")
print(data_scaled_standard[:5])
print(f"\nMean (≈0): {data_scaled_standard[:, 0].mean():.6f}")
print(f"Std (≈1): {data_scaled_standard[:, 0].std():.6f}")
```

### 4. Encoding Categorical Data
```python
# লেবেল এনকোডিং
le = LabelEncoder()
data['loan_term_encoded'] = le.fit_transform(data['loan_term_months'])
print("লোন টার্ম এনকোডিং:")
print(data[['loan_term_months', 'loan_term_encoded']].drop_duplicates().head())

# One-Hot Encoding
loan_term_dummies = pd.get_dummies(data['loan_term_months'], prefix='term')
data = pd.concat([data, loan_term_dummies], axis=1)
print(f"\nOne-Hot Encoding এর পর কলাম সংখ্যা: {data.shape[1]}")
```

### 5. সম্পূর্ণ প্রিপ্রসেসিং পাইপলাইন
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# প্রিপ্রসেসিং পাইপলাইন
numeric_features = ['age', 'annual_income', 'credit_score', 'loan_amount', 
                    'employment_years', 'debt_to_income']
categorical_features = ['loan_term_months']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', 'passthrough')  # বা OneHotEncoder
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

print("প্রিপ্রসেসিং পাইপলাইন প্রস্তুত!")
```

### সারসংক্ষেপ
ডেটা প্রিপ্রসেসিং ML পাইপলাইনের সবচেয়ে গুরুত্বপূর্ণ অংশ। Missing values, outliers, scaling, এবং encoding সঠিকভাবে করা ML মডেলের পারফরম্যান্স significantly উন্নত করে।