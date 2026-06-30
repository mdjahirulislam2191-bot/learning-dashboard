# Day 09: ফিচার ইঞ্জিনিয়ারিং
## Feature Engineering

### ফিচার ইঞ্জিনিয়ারিং কী?
ফিচার ইঞ্জিনিয়ারিং হলো কাঁচা ডেটা থেকে মেশিন লার্নিং মডেলের জন্য উপযোগী ফিচার তৈরি করার প্রক্রিয়া। এটি মডেলের পারফরম্যান্স উল্লেখযোগ্যভাবে উন্নত করতে পারে।

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from datetime import datetime

np.random.seed(42)
```

### ডেটাসেট তৈরি:
```python
n = 1000
df = pd.DataFrame({
    'আইডি': range(1, n+1),
    'নাম': [f'Person_{i}' for i in range(1, n+1)],
    'বয়স': np.random.randint(18, 65, n),
    'লিঙ্গ': np.random.choice(['Male', 'Female'], n),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট', 'বরিশাল'], n),
    'শিক্ষা': np.random.choice(['SSC', 'HSC', 'Bachelor', 'Master', 'PhD'], n, p=[0.1, 0.2, 0.4, 0.2, 0.1]),
    'অভিজ্ঞতা_বছর': np.random.randint(0, 35, n),
    'প্রকল্প_সম্পন্ন': np.random.poisson(5, n),
    'প্রশিক্ষণ_ঘন্টা': np.random.exponential(25, n).astype(int).clip(0, 150),
    'লগইন_দিন': np.random.randint(0, 365, n),
    'ওয়েব_ভিজিট': np.random.poisson(100, n),
    'ইমেইল_ওপেন': np.random.randint(0, 50, n),
    'টার্গেট': np.random.randn(n) + 5  # target variable
})

print(f"Original DF: {df.shape}")
print(df.head())
```

### ১. মিসিং ভ্যালু ইমপিউটেশন (অ্যাডভান্সড):
```python
# কিছু মিসিং ভ্যালু যোগ করা
df_missing = df.copy()
df_missing.loc[::10, 'বয়স'] = np.nan
df_missing.loc[::15, 'শিক্ষা'] = np.nan
df_missing.loc[::8, 'প্রশিক্ষণ_ঘন্টা'] = np.nan

print("=== অ্যাডভান্সড ইমপিউটেশন ===")

# 1. Mean/Median imputation
df['বয়স_median'] = df_missing['বয়স'].fillna(df_missing['বয়স'].median())

# 2. Mode imputation (categorical)
df['শিক্ষা_mode'] = df_missing['শিক্ষা'].fillna(df_missing['শিক্ষা'].mode()[0])

# 3. Group-wise imputation
df['প্রশিক্ষণ_mean_by_edu'] = df_missing.groupby('শিক্ষা')['প্রশিক্ষণ_ঘন্টা'].transform(
    lambda x: x.fillna(x.mean())
)

# 4. Forward fill (time series like)
df['প্রশিক্ষণ_ffill'] = df_missing['প্রশিক্ষণ_ঘন্টা'].ffill()

print("Imputation complete!")
```

### ২. এনকোডিং টেকনিক:
```python
print("=== ক্যাটেগোরিকাল এনকোডিং ===")

# Label Encoding
le = LabelEncoder()
df['লিঙ্গ_encoded'] = le.fit_transform(df['লিঙ্গ'])
print(f"Label Encoded 'লিঙ্গ': {dict(zip(le.classes_, le.transform(le.classes_)))}")

# One-Hot Encoding
df_city = pd.get_dummies(df['শহর'], prefix='শহর', drop_first=True)
df = pd.concat([df, df_city], axis=1)
print(f"\nOne-Hot encoding added {len(df_city.columns)} columns")

# Ordinal Encoding (শিক্ষার জন্য অর্ডার)
education_order = {'SSC': 0, 'HSC': 1, 'Bachelor': 2, 'Master': 3, 'PhD': 4}
df['শিক্ষা_ordinal'] = df['শিক্ষা'].map(education_order)
print(f"\nOrdinal Encoding of Education:\n{df['শিক্ষা_ordinal'].value_counts().sort_index()}")

# Target Encoding (গড় টার্গেট দিয়ে এনকোড)
city_target_mean = df.groupby('শহর')['টার্গেট'].mean()
df['শহর_target_encoded'] = df['শহর'].map(city_target_mean)
print(f"\nTarget Encoding (Mean):\n{city_target_mean}")
```

### ৩. সংখ্যাত্মক ফিচার ট্রান্সফর্মেশন:
```python
print("=== সংখ্যাত্মক ট্রান্সফর্মেশন ===")

# Log Transformation (স্কিউড ডেটার জন্য)
df['লগ_প্রশিক্ষণ'] = np.log1p(df['প্রশিক্ষণ_ঘন্টা'])
df['স্কয়ার_প্রশিক্ষণ'] = np.sqrt(df['প্রশিক্ষণ_ঘন্টा'])

# Binning
df['বয়স_গ্রুপ'] = pd.cut(df['বয়স'], bins=[0, 25, 35, 45, 55, 100], 
                          labels=['তরুণ', 'যুব', 'মধ্যবয়সী', 'পরিণত', 'বয়স্ক'])
df['বয়স_বিন_সংখ্যা'] = pd.cut(df['বয়স'], bins=5, labels=False)

# Interaction Features
df['অভিজ্ঞতা_প্রকল্প'] = df['অভিজ্ঞতা_বছর'] * df['প্রকল্প_সম্পন্ন']
df['বয়স_প্রশিক্ষণ'] = df['বয়স'] * df['প্রশিক্ষণ_ঘন্টা']

# Ratio Features
df['প্রকল্প_প্রতি_বছর'] = df['প্রকল্প_সম্পন্ন'] / (df['অভিজ্ঞতা_বছর'] + 1)
df['প্রশিক্ষণ_ঘন্টা_প্রতি_বছর'] = df['প্রশিক্ষণ_ঘন্টা'] / (df['অভিজ্ঞতা_বছর'] + 1)

# Polynomial Features
df['বয়স_স্কয়ার'] = df['বয়স'] ** 2
df['অভিজ্ঞতা_স্কয়ার'] = df['অভিজ্ঞতা_বছর'] ** 2

print("Transformations complete!")
new_features = ['লগ_প্রশিক্ষণ', 'অভিজ্ঞতা_প্রকল্প', 'প্রকল্প_প্রতি_বছর']
print(f"New features: {new_features}")
```

### ৪. ডেট এন্ড টাইম ফিচার:
```python
print("=== ডেট/টাইম ফিচার ইঞ্জিনিয়ারিং ===")

# ডেট তৈরি
date_rng = pd.date_range('2023-01-01', periods=n, freq='h')
df['তারিখ'] = np.random.choice(date_rng, n)

# ডেট থেকে ফিচার এক্সট্র্যাক্ট
df['বছর'] = df['তারিখ'].dt.year
df['মাস'] = df['তারিখ'].dt.month
df['দিন'] = df['তারিখ'].dt.day
df['ঘন্টা'] = df['তারিখ'].dt.hour
df['দিনের_নাম'] = df['তারিখ'].dt.day_name()
df['সপ্তাহের_দিন'] = df['তারিখ'].dt.weekday  # 0=Monday
df['সপ্তাহান্ত'] = (df['সপ্তাহের_দিন'] >= 5).astype(int)

# সাইক্লিকাল এনকোডিং (মাস ও ঘন্টার জন্য)
df['মাস_sin'] = np.sin(2 * np.pi * df['মাস'] / 12)
df['মাস_cos'] = np.cos(2 * np.pi * df['মাস'] / 12)
df['ঘন্টা_sin'] = np.sin(2 * np.pi * df['ঘন্টা'] / 24)
df['ঘন্টা_cos'] = np.cos(2 * np.pi * df['ঘন্টা'] / 24)

print(f"New date features: {[c for c in df.columns if c.startswith(('বছর', 'মাস', 'দিন', 'ঘন্টা', 'সপ্তাহ'))]}")
```

### ৫. স্কেলিং ও নরমালাইজেশন:
```python
print("=== ফিচার স্কেলিং ===")

# সংখ্যাত্মক ফিচার নির্বাচন
num_features = ['বয়স', 'অভিজ্ঞতা_বছর', 'প্রকল্প_সম্পন্ন', 'প্রশিক্ষণ_ঘন্টা']
X = df[num_features]

# StandardScaler (Z-score normalization)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(X)
df_scaled = pd.DataFrame(df_scaled, columns=[f'{col}_zscore' for col in num_features])
print(f"StandardScaler - Mean: {df_scaled.mean().round(2).tolist()}")
print(f"StandardScaler - Std: {df_scaled.std().round(2).tolist()}")

# MinMaxScaler (0-1 range)
minmax = MinMaxScaler()
df_minmax = minmax.fit_transform(X)
df_minmax = pd.DataFrame(df_minmax, columns=[f'{col}_minmax' for col in num_features])
print(f"MinMaxScaler - Min: {df_minmax.min().round(2).tolist()}")
print(f"MinMaxScaler - Max: {df_minmax.max().round(2).tolist()}")

# RobustScaler (IQR based)
from sklearn.preprocessing import RobustScaler
robust = RobustScaler()
df_robust = robust.fit_transform(X)
df_robust = pd.DataFrame(df_robust, columns=[f'{col}_robust' for col in num_features])

df = pd.concat([df, df_scaled, df_minmax, df_robust], axis=1)
print("Scaling complete!")
```

### ৬. ফিচার সিলেকশন:
```python
print("=== ফিচার সিলেকশন ===")

# Correlation-based selection
feature_cols = ['বয়স', 'অভিজ্ঞতা_বছর', 'প্রকল্প_সম্পন্ন', 'প্রশিক্ষণ_ঘন্টা', 
                'লগইন_দিন', 'ওয়েব_ভিজিট', 'ইমেইল_ওপেন']
corr_with_target = df[feature_cols + ['টার্গেট']].corr()['টার্গেট'].drop('টার্গেট')
print("Correlation with Target:")
print(corr_with_target.sort_values(ascending=False))

# SelectKBest
selector = SelectKBest(score_func=f_regression, k=5)
X_selected = selector.fit_transform(df[feature_cols], df['টার্গেট'])
selected_idx = selector.get_support(indices=True)
selected_features = [feature_cols[i] for i in selected_idx]
print(f"\nTop 5 features (SelectKBest): {selected_features}")
print(f"Scores: {selector.scores_[selected_idx].round(2)}")

# Mutual Information
mi_scores = mutual_info_regression(df[feature_cols], df['টার্গেট'])
mi_features = pd.Series(mi_scores, index=feature_cols).sort_values(ascending=False)
print(f"\nMutual Information Scores:\n{mi_features}")
```

### ৭. টেক্সট ফিচার (বেসিক):
```python
print("=== টেক্সট ফিচার ===")

# নাম থেকে ফিচার
df['নাম_দৈর্ঘ্য'] = df['নাম'].str.len()
df['নামে_আন্ডারস্কোর'] = df['নাম'].str.contains('_').astype(int)

# টেক্সট ফিচার সিমুলেশন
df['ফ্রি_টেক্সট'] = np.random.choice([
    'good experience', 'average work', 'excellent team', 
    'needs improvement', 'outstanding performance'
], n)

# টেক্সট থেকে কীওয়ার্ড
df['has_good'] = df['ফ্রি_টেক্সট'].str.contains('good|excellent|outstanding').astype(int)
df['has_bad'] = df['ফ্রি_টেক্সट'].str.contains('average|needs').astype(int)
df['টেক্সট_দৈর্ঘ্য'] = df['ফ্রি_টেক্সট'].str.len()

print(f"Text features created!")
```

### সম্পূর্ণ ফিচার ইঞ্জিনিয়ারিং পাইপলাইন:
```python
def feature_engineering_pipeline(df, target_col='টার্গেট'):
    """সম্পূর্ণ ফিচার ইঞ্জিনিয়ারিং পাইপলাইন"""
    df_engineered = df.copy()
    
    # 1. Missing value handling
    for col in df_engineered.select_dtypes(include=[np.number]).columns:
        if df_engineered[col].isnull().sum() > 0:
            df_engineered[col].fillna(df_engineered[col].median(), inplace=True)
    
    for col in df_engineered.select_dtypes(include=['object']).columns:
        if df_engineered[col].isnull().sum() > 0:
            df_engineered[col].fillna(df_engineered[col].mode()[0], inplace=True)
    
    # 2. Encode categorical
    for col in df_engineered.select_dtypes(include=['object']).columns:
        if col != target_col and col not in ['তারিখ', 'নাম']:
            if df_engineered[col].nunique() <= 5:
                dummies = pd.get_dummies(df_engineered[col], prefix=col, drop_first=True)
                df_engineered = pd.concat([df_engineered, dummies], axis=1)
    
    # 3. Drop original text columns
    df_engineered.drop(columns=['নাম', 'তারিখ', 'ফ্রি_টেক্সট'], inplace=True, errors='ignore')
    
    # 4. Add interaction features for top numeric columns
    num_cols = df_engineered.select_dtypes(include=[np.number]).columns
    num_cols = [c for c in num_cols if c != target_col][:5]
    
    for i in range(len(num_cols)):
        for j in range(i+1, len(num_cols)):
            col_name = f'{num_cols[i]}_x_{num_cols[j]}'
            df_engineered[col_name] = df_engineered[num_cols[i]] * df_engineered[num_cols[j]]
    
    print(f"Pipeline complete! Shape: {df_engineered.shape}")
    return df_engineered

# পাইপলাইন রান
df_final = feature_engineering_pipeline(df)
print(f"Final shape: {df_final.shape}")
print(f"Features: {df_final.columns.tolist()}")
```

### সারসংক্ষেপ:
- অ্যাডভান্সড ইমপিউটেশন টেকনিক
- ক্যাটেগোরিকাল এনকোডিং (Label, One-Hot, Ordinal, Target)
- সংখ্যাত্মক ট্রান্সফর্মেশন (Log, Binning, Interaction, Polynomial)
- ডেট/টাইম ফিচার ইঞ্জিনিয়ারিং (Cyclical Encoding)
- ফিচার স্কেলিং (Standard, MinMax, Robust)
- ফিচার সিলেকশন (Correlation, SelectKBest, Mutual Information)
- টেক্সট ফিচার ও সম্পূর্ণ পাইপলাইন