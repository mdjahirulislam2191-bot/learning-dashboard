# Day 56: ক্যাপস্টোন প্রোজেক্ট — ডেটা প্রিপারেশন
## Capstone Project: Data Preparation

### প্রোজেক্ট ওভারভিউ
আমরা একটি রিয়েল-ওয়ার্ল্ড ডেটাসেট নিয়ে কাজ করব — **হাউস প্রাইস প্রেডিকশন**। এই ক্যাপস্টোন প্রোজেক্টে আমরা একটি এন্ড-টু-এন্ড এমএল পাইপলাইন তৈরি করব।

```python
# প্রয়োজনীয় লাইব্রেরি
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# সেটিংস
plt.style.use('seaborn-v0_8')
sns.set_palette('husl')
```

### ডেটা লোডিং ও এক্সপ্লোরেশন

```python
# সিন্থেটিক ডেটা জেনারেশন (রিয়েল ডেটার মতো)
np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    'area': np.random.normal(1500, 500, n_samples),
    'bedrooms': np.random.randint(1, 6, n_samples),
    'bathrooms': np.random.randint(1, 4, n_samples),
    'age': np.random.randint(0, 50, n_samples),
    'location_score': np.random.uniform(1, 10, n_samples),
    'has_garage': np.random.randint(0, 2, n_samples),
    'has_garden': np.random.randint(0, 2, n_samples),
    'floor': np.random.randint(1, 10, n_samples),
    'total_floors': np.random.randint(1, 15, n_samples),
    'distance_center': np.random.uniform(0.5, 20, n_samples),
})

# প্রাইস জেনারেশন (বাস্তবসম্মত)
data['price'] = (
    50000 + 
    data['area'] * 100 + 
    data['bedrooms'] * 20000 + 
    data['bathrooms'] * 15000 - 
    data['age'] * 1000 + 
    data['location_score'] * 30000 +
    data['has_garage'] * 25000 +
    data['has_garden'] * 15000 +
    np.random.normal(0, 20000, n_samples)
)

print("ডেটাসেট শেপ:", data.shape)
print("\nপ্রথম ৫ সারি:")
print(data.head())

print("\nডেটা ইনফরমেশন:")
print(data.info())

print("\nস্ট্যাটিস্টিক্যাল সামারি:")
print(data.describe())
```

### ডেটা কোয়ালিটি চেক

```python
# মিসিং ভ্যালু চেক
print("মিসিং ভ্যালু:")
print(data.isnull().sum())

# মিসিং ভ্যালু হ্যান্ডলিং (যদি থাকে)
def handle_missing_values(df):
    """মিসিং ভ্যালু হ্যান্ডল করা"""
    df_clean = df.copy()
    
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype in ['int64', 'float64']:
                # নিউমেরিক কলাম -> মিডিয়ান
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
            else:
                # ক্যাটাগোরিকাল কলাম -> মোড
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    return df_clean

# আউটলায়ার ডিটেকশন
def detect_outliers_iqr(df, columns):
    """IQR পদ্ধতিতে আউটলায়ার ডিটেকশন"""
    outliers = {}
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers[col] = df[(df[col] < lower_bound) | 
                          (df[col] > upper_bound)].shape[0]
    
    return outliers

numeric_cols = ['area', 'price', 'age', 'distance_center']
outliers = detect_outliers_iqr(data, numeric_cols)
print("\nআউটলায়ার কাউন্ট:")
for col, count in outliers.items():
    print(f"  {col}: {count}")
```

### ডেটা ভিজুয়ালাইজেশন

```python
# ফিচার ডিস্ট্রিবিউশন
fig, axes = plt.subplots(3, 4, figsize=(16, 12))
axes = axes.ravel()

for idx, col in enumerate(data.columns):
    if idx < 12:
        axes[idx].hist(data[col], bins=30, edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'{col} ডিস্ট্রিবিউশন')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('ফ্রিকোয়েন্সি')

plt.tight_layout()
plt.savefig('capstone_data_distributions.png', dpi=100)
plt.show()
print("ডিস্ট্রিবিউশন প্লট সেভ করা হয়েছে")

# পারস্পরিক সম্পর্ক (Correlation)
plt.figure(figsize=(12, 10))
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', 
            cmap='coolwarm', center=0)
plt.title('ফিচার করিলেশন ম্যাট্রিক্স')
plt.tight_layout()
plt.savefig('capstone_correlation.png', dpi=100)
plt.show()
print("করিলেশন হিটম্যাপ সেভ করা হয়েছে")

# ফিচার vs টার্গেট
fig, axes = plt.subplots(2, 4, figsize=(18, 10))
features = ['area', 'bedrooms', 'bathrooms', 'age', 
            'location_score', 'distance_center', 'has_garage', 'has_garden']

for idx, feature in enumerate(features):
    row = idx // 4
    col = idx % 4
    axes[row, col].scatter(data[feature], data['price'], 
                          alpha=0.6, s=30)
    axes[row, col].set_xlabel(feature)
    axes[row, col].set_ylabel('Price')
    axes[row, col].set_title(f'{feature} vs প্রাইস')

plt.tight_layout()
plt.savefig('capstone_feature_vs_target.png', dpi=100)
plt.show()
print("ফিচার vs টার্গেট প্লট সেভ করা হয়েছে")
```

### ডেটা প্রিপ্রসেসিং

```python
# ফিচার ইঞ্জিনিয়ারিং (বেসিক)
def prepare_features(df):
    """বেসিক ফিচার প্রিপারেশন"""
    df_prep = df.copy()
    
    # নিউমেরিক ফিচার
    numeric_features = ['area', 'age', 'distance_center', 'location_score']
    categorical_features = ['bedrooms', 'bathrooms', 'has_garage', 
                           'has_garden', 'floor', 'total_floors']
    
    # ক্যাটাগোরিকাল ফিচার এনকোডিং
    for col in categorical_features:
        df_prep[col] = df_prep[col].astype('category')
    
    return df_prep, numeric_features, categorical_features

df_processed, num_features, cat_features = prepare_features(data)
print("প্রিপ্রসেসিং পরবর্তী ডেটা:")
print(df_processed.head())
```

### ট্রেইন-টেস্ট স্প্লিট

```python
# ফিচার ও টার্গেট আলাদা করা
X = df_processed.drop('price', axis=1)
y = df_processed['price']

# ট্রেইন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"ট্রেইন সেট: {X_train.shape}")
print(f"টেস্ট সেট: {X_test.shape}")

# স্কেলিং
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[num_features] = scaler.fit_transform(X_train[num_features])
X_test_scaled[num_features] = scaler.transform(X_test[num_features])

print("\nস্কেলিং পরবর্তী ডেটা:")
print(X_train_scaled.describe())

# ডেটা সেভ করা
import joblib
joblib.dump(X_train_scaled, 'X_train.pkl')
joblib.dump(X_test_scaled, 'X_test.pkl')
joblib.dump(y_train, 'y_train.pkl')
joblib.dump(y_test, 'y_test.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\nপ্রিপেয়ারড ডেটা সেভ করা হয়েছে!")
```

### সারাংশ
- ডেটা লোড এবং এক্সপ্লোর করা হয়েছে
- মিসিং ভ্যালু ও আউটলায়ার চেক করা হয়েছে
- ডেটা ভিজুয়ালাইজ করা হয়েছে
- ফিচার প্রিপারেশন করা হয়েছে
- ট্রেইন-টেস্ট স্প্লিট ও স্কেলিং সম্পন্ন হয়েছে
- প্রিপেয়ারড ডেটা সেভ করা হয়েছে