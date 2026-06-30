# Day 12: ফিচার ইঞ্জিনিয়ারিং
## Feature Engineering

### ফিচার ইঞ্জিনিয়ারিং কী?
ফিচার ইঞ্জিনিয়ারিং হলো কাঁচা ডেটা থেকে মডেলের জন্য উপযুক্ত ফিচার (বৈশিষ্ট্য) তৈরি, রূপান্তর ও নির্বাচনের প্রক্রিয়া। ভালো ফিচার ইঞ্জিনিয়ারিং মডেলের পারফরম্যান্স অনেকাংশে বাড়িয়ে দেয়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
import warnings
warnings.filterwarnings('ignore')

# স্যাম্পল ডেটাসেট তৈরি
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'বয়স': np.random.randint(18, 70, n),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা'], n),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী'], n),
    'শিক্ষাবর্ষ': np.random.randint(0, 20, n),
    'আয়': np.random.normal(50000, 15000, n)
})
print("=== কাঁচা ডেটা ===")
print(df.head())
print(df.info())
```

### ফিচার ইঞ্জিনিয়ারিং টেকনিকসমূহ:

#### ১. মিসিং ভ্যালু হ্যান্ডলিং:
```python
print("\n=== মিসিং ভ্যালু হ্যান্ডলিং ===")
# কিছু মিসিং ভ্যালু যোগ করা
df_missing = df.copy()
df_missing.loc[np.random.choice(n, 50), 'আয়'] = np.nan
df_missing.loc[np.random.choice(n, 30), 'বয়স'] = np.nan

print(f"মিসিং ভ্যালু:\n{df_missing.isnull().sum()}")

# Mean/Median imputation
df_missing['আয়'].fillna(df_missing['আয়'].median(), inplace=True)
df_missing['বয়স'].fillna(df_missing['বয়স'].mean(), inplace=True)
print(f"\nইম্পুটেশনের পর:\n{df_missing.isnull().sum()}")
```

#### ২. এনকোডিং (Encoding):
```python
print("\n=== ক্যাটেগোরিকাল এনকোডিং ===")

# Label Encoding
le = LabelEncoder()
df['লিঙ্গ_এনকোডেড'] = le.fit_transform(df['লিঙ্গ'])
print(f"Label Encoding:\n{dict(zip(le.classes_, le.transform(le.classes_)))}")

# One-Hot Encoding
one_hot = pd.get_dummies(df['শহর'], prefix='শহর')
df_encoded = pd.concat([df, one_hot], axis=1)
print(f"\nOne-Hot Encoding:\n{one_hot.head()}")

# OneHotEncoder with sklearn
ohe = OneHotEncoder(sparse_output=False, drop='first')
city_encoded = ohe.fit_transform(df[['শহর']])
city_df = pd.DataFrame(city_encoded, columns=ohe.get_feature_names_out(['শহর']))
print(f"\nSklearn OneHotEncoder:\n{city_df.head()}")
```

#### ৩. স্কেলিং (Scaling) - নরমালাইজেশন ও স্ট্যান্ডার্ডাইজেশন:
```python
print("\n=== ফিচার স্কেলিং ===")

# StandardScaler (Z-score normalization)
scaler = StandardScaler()
df['আয়_স্ট্যান্ডার্ড'] = scaler.fit_transform(df[['আয়']])

# MinMaxScaler (0 to 1 range)
minmax = MinMaxScaler()
df['আয়_নরমাল'] = minmax.fit_transform(df[['আয়']])

print(f"আয় (অরিজিনাল): মিন={df['আয়'].min():.2f}, ম্যাক্স={df['আয়'].max():.2f}, মিন={df['আয়'].mean():.2f}, স্টিড={df['আয়'].std():.2f}")
print(f"আয় (স্ট্যান্ডার্ড): মিন={df['আয়_স্ট্যান্ডার্ড'].min():.2f}, ম্যাক্স={df['আয়_স্ট্যান্ডার্ড'].max():.2f}, মিন={df['আয়_স্ট্যান্ডার্ড'].mean():.2f}, স্টিড={df['আয়_স্ট্যান্ডার্ড'].std():.2f}")
print(f"আয় (নরমাল): মিন={df['আয়_নরমাল'].min():.2f}, ম্যাক্স={df['আয়_নরমাল'].max():.2f}, মিন={df['আয়_নরমাল'].mean():.2f}, স্টিড={df['আয়_নরমাল'].std():.2f}")
```

#### ৪. ফিচার ক্রিয়েশন (নতুন ফিচার তৈরি):
```python
print("\n=== নতুন ফিচার তৈরি ===")

# বাইনারি ফিচার
df['ইজ_ইয়াং'] = (df['বয়স'] < 30).astype(int)
df['ইজ_সিনিয়র'] = (df['শিক্ষাবর্ষ'] > 10).astype(int)

# ইন্টারঅ্যাকশন ফিচার
df['বয়স_শিক্ষা_ইন্টারঅ্যাকশন'] = df['বয়স'] * df['শিক্ষাবর্ষ']

# অ্যাগ্রিগেট ফিচার
df['বয়স_গ্রুপ'] = pd.cut(df['বয়স'], bins=[0, 25, 35, 50, 100], labels=['তরুণ', 'যুবক', 'মধ্যবয়সী', 'বয়স্ক'])

# পলিনমিয়াল ফিচার
df['শিক্ষাবর্ষ_স্কোয়ার'] = df['শিক্ষাবর্ষ'] ** 2
df['শিক্ষাবর্ষ_কিউব'] = df['শিক্ষাবর্ষ'] ** 3

print(f"নতুন ফিচারসমূহ:\n{df[['বয়স', 'ইজ_ইয়াং', 'ইজ_সিনিয়র', 'বয়স_শিক্ষা_ইন্টারঅ্যাকশন', 'শিক্ষাবর্ষ_স্কোয়ার']].head()}")
print(f"\nবয়স গ্রুপ ডিস্ট্রিবিউশন:\n{df['বয়স_গ্রুপ'].value_counts()}")
```

#### ৫. ফিচার সিলেকশন:
```python
print("\n=== ফিচার সিলেকশন ===")

# SelectKBest - ফিচার র‍্যাঙ্কিং
X = df[['বয়স', 'শিক্ষাবর্ষ', 'আয়']]
y = df['বয়স'] * 0.5 + df['শিক্ষাবর্ষ'] * 0.3 + np.random.normal(0, 5, n)

selector = SelectKBest(score_func=f_regression, k=2)
selector.fit(X, y)

scores = pd.DataFrame({
    'ফিচার': X.columns,
    'স্কোর': selector.scores_,
    'সিলেক্টেড': selector.get_support()
})
print(f"ফিচার স্কোর:\n{scores.sort_values('স্কোর', ascending=False)}")

# Correlation-based selection
corr_matrix = df.select_dtypes(include=[np.number]).corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('ফিচার করিলেশন ম্যাট্রিক্স')
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.show()
print("করিলেশন ম্যাট্রিক্স সেভ করা হয়েছে")
```

#### ৬. বিগিণিং ফিচার (Binning):
```python
print("\n=== বিগিণিং ফিচার ===")

# ইকুয়াল উইডথ বিনিং
df['আয়_রেঞ্জ'] = pd.cut(df['আয়'], bins=5, labels=['খুব কম', 'কম', 'মধ্যম', 'উচ্চ', 'খুব উচ্চ'])
print(f"ইকুয়াল উইডথ বিনিং:\n{df['আয়_রেঞ্জ'].value_counts()}")

# ইকুয়াল ফ্রিকোয়েন্সি বিনিং (কোয়ান্টাইল)
df['আয়_কোয়ান্টাইল'] = pd.qcut(df['আয়'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
print(f"\nইকুয়াল ফ্রিকোয়েন্সি বিনিং:\n{df['আয়_কোয়ান্টাইল'].value_counts()}")
```

#### ৭. লগ ও পাওয়ার ট্রান্সফরমেশন:
```python
print("\n=== ট্রান্সফরমেশন ===")

# লগ ট্রান্সফরমেশন (স্কিউড ডেটার জন্য)
df['আয়_লগ'] = np.log1p(df['আয়'])
print(f"আয় স্কিউনেস: {df['আয়'].skew():.3f}")
print(f"লগ ট্রান্সফর্মড স্কিউনেস: {df['আয়_লগ'].skew():.3f}")

# বক্স-কক্স ট্রান্সফরমেশন
from scipy import stats
boxcox_transformed, lambda_val = stats.boxcox(df['আয়'] - df['আয়'].min() + 1)
df['আয়_বক্সকক্স'] = boxcox_transformed
print(f"বক্স-কক্স ল্যাম্বডা: {lambda_val:.3f}")
print(f"বক্স-কক্স স্কিউনেস: {df['আয়_বক্সকক্স'].skew():.3f}")
```

#### ৮. ডেট এন্ড টাইম ফিচার:
```python
print("\n=== ডেট টাইম ফিচার ===")

# ডেট টাইম ডেটা তৈরি
date_rng = pd.date_range('2024-01-01', periods=100, freq='D')
df_date = pd.DataFrame(date_rng, columns=['তারিখ'])

# ফিচার এক্সট্র্যাকশন
df_date['বছর'] = df_date['তারিখ'].dt.year
df_date['মাস'] = df_date['তারিখ'].dt.month
df_date['দিন'] = df_date['তারিখ'].dt.day
df_date['সপ্তাহের_দিন'] = df_date['তারিখ'].dt.dayofweek  # 0=Monday
df_date['সপ্তাহান্ত'] = (df_date['তারিখ'].dt.dayofweek >= 5).astype(int)
df_date['ত্রৈমাসিক'] = df_date['তারিখ'].dt.quarter
df_date['সপ্তাহ_নং'] = df_date['তারিখ'].dt.isocalendar().week.astype(int)

print(f"ডেট টাইম ফিচার:\n{df_date.head(10)}")
print(f"\nসপ্তাহান্ত বিতরণ:\n{df_date['সপ্তাহান্ত'].value_counts()}")
```

#### ৯. টেক্সট ফিচার (বেসিক):
```python
print("\n=== টেক্সট ফিচার ===")

# স্যাম্পল টেক্সট ডেটা
texts = [
    'ঢাকায় বিক্রি বেড়েছে',
    'চট্টগ্রামে বিক্রি কমেছে',
    'খুলনায় নতুন পণ্য লঞ্চ',
    'রাজশাহীতে আমের ফলন ভালো'
]

# টেক্সট লেংথ ফিচার
df_text = pd.DataFrame({'টেক্সট': texts})
df_text['লেংথ'] = df_text['টেক্সট'].str.len()
df_text['শব্দ_সংখ্যা'] = df_text['টেক্সট'].str.split().str.len()
print(f"টেক্সট ফিচার:\n{df_text}")
```

### ফিচার ইঞ্জিনিয়ারিং পাইপলাইন:
```python
print("\n=== ফিচার ইঞ্জিনিয়ারিং পাইপলাইন ===")

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# পাইপলাইন ডিফাইন
numeric_features = ['বয়স', 'শিক্ষাবর্ষ']
categorical_features = ['লিঙ্গ', 'শহর']

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('cat', categorical_pipeline, categorical_features)
])

# পাইপলাইন ফিট ও ট্রান্সফর্ম
X_transformed = preprocessor.fit_transform(df)
print(f"ট্রান্সফর্মড ডেটা শেপ: {X_transformed.shape}")
print("পাইপলাইন সফলভাবে তৈরি হয়েছে!")
```

### সারাংশ:
- **ফিচার ইঞ্জিনিয়ারিং** ডেটা সায়েন্স প্রজেক্টের সবচেয়ে গুরুত্বপূর্ণ অংশ
- **এনকোডিং** ক্যাটেগোরিকাল ডেটাকে সংখ্যায় রূপান্তর করে
- **স্কেলিং** ফিচারগুলিকে একই রেঞ্জে নিয়ে আসে
- **ফিচার ক্রিয়েশন** নতুন ইনফরমেটিভ ফিচার তৈরি করে
- **ফিচার সিলেকশন** অপ্রয়োজনীয় ফিচার বাদ দেয়
- **পাইপলাইন** সব ধাপ একসাথে অটোমেট করে
