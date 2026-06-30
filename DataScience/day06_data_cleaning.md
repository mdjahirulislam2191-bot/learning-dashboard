# Day 06: ডেটা ক্লিনিং
## Data Cleaning

### ডেটা ক্লিনিং কী?
ডেটা ক্লিনিং হলো ডেটাসেট থেকে ত্রুটি, অসঙ্গতি, এবং অপ্রয়োজনীয় ডেটা অপসারণের প্রক্রিয়া। এটি ডেটা সায়েন্সের সবচেয়ে গুরুত্বপূর্ণ ও সময়সাপেক্ষ কাজ।

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

### বাস্তবসম্মত নোংরা ডেটাসেট তৈরি:
```python
np.random.seed(42)
n = 200

df = pd.DataFrame({
    'আইডি': range(1, n+1),
    'নাম': np.random.choice(['আলিফ', 'বর্ণা', 'চন্দন', 'দীপা', None], n, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'বয়স': np.random.choice([18, 25, 30, 35, 40, -5, 150], n, p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.05, 0.05]),
    'বেতন': np.random.choice([25000, 35000, 45000, 55000, 0, -1000, np.nan], n, p=[0.2, 0.2, 0.2, 0.15, 0.1, 0.05, 0.1]),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'ঢাকা ', ' CHITTAGONG', '', 'রাজশাহী'], n),
    'ইমেইল': ['user' + str(i) + '@mail.com' if np.random.random() > 0.15 else 'invalid' for i in range(n)],
    'নিবন্ধন_তারিখ': pd.date_range('2024-01-01', periods=n, freq='D'),
    'স্কোর': np.random.uniform(0, 100, n).round(1)
})

# কিছু intentional duplicate যোগ
df = pd.concat([df, df.iloc[:5]], ignore_index=True)
print(f"মোট সারি: {len(df)}")
print(f"মোট কলাম: {len(df.columns)}")
```

### মিসিং ডেটা হ্যান্ডলিং:
```python
print("=== মিসিং ভ্যালু অ্যানালাইসিস ===")
print(df.isnull().sum())
print(f"\nমোট মিসিং ভ্যালু: {df.isnull().sum().sum()}")

# মিসিং ভ্যালুর ভিজুয়ালাইজেশন
missing_pct = (df.isnull().sum() / len(df)) * 100
print(f"\nমিসিং ভ্যালুর শতাংশ:\n{missing_pct}")

# ড্রপ vs ফিল স্ট্র্যাটেজি
threshold = 0.5  # 50% এর বেশি মিসিং থাকলে কলাম ড্রপ
cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
print(f"\nড্রপ করার মতো কলাম: {cols_to_drop if cols_to_drop else 'কোনটি নেই'}")
```

### আউটলায়ার ডিটেকশন ও হ্যান্ডলিং:
```python
# বয়সে আউটলায়ার চেক
print("=== আউটলায়ার ডিটেকশন ===")
print(f"বয়স পরিসংখ্যান:\n{df['বয়স'].describe()}")

# Z-Score পদ্ধতি
from scipy import stats
z_scores = np.abs(stats.zscore(df['বয়с'].dropna()))
outliers_z = df['বয়স'][z_scores > 3]
print(f"\nZ-Score আউটলায়ার (বয়স): {len(outliers_z)} টি")

# IQR পদ্ধতি
Q1 = df['বয়স'].quantile(0.25)
Q3 = df['বয়স'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_iqr = df[(df['বয়স'] < lower) | (df['বয়স'] > upper)]
print(f"IQR আউটলায়ার (বয়স): {len(outliers_iqr)} টি")

# বেতনে আউটলায়ার
Q1_s = df['বেতন'].quantile(0.25)
Q3_s = df['বেতন'].quantile(0.75)
IQR_s = Q3_s - Q1_s
lower_s = Q1_s - 1.5 * IQR_s
upper_s = Q3_s + 1.5 * IQR_s
salary_outliers = df[(df['বেতন'] < lower_s) | (df['বেতন'] > upper_s)]
print(f"বেতন আউটলায়ার: {len(salary_outliers)} টি")
```

### ডুপ্লিকেট ডেটা হ্যান্ডলিং:
```python
print("=== ডুপ্লিকেট হ্যান্ডলিং ===")
print(f"মোট ডুপ্লিকেট সারি: {df.duplicated().sum()}")

# ডুপ্লিকেট দেখা
dup_rows = df[df.duplicated(keep=False)]
print(f"ডুপ্লিকেট সারি (প্রথম ৫):\n{dup_rows.head()}")

# ডুপ্লিকেট সরানো
df_clean = df.drop_duplicates()
print(f"ডুপ্লিকেট সরানোর পর: {len(df_clean)} সারি")
```

### ডেটা টাইপ কনভার্শন ও ক্লিনিং:
```python
print("=== ডেটা টাইপ ফিক্স ===")
print(df.dtypes)

# বয়স ফিক্স - নেগেটিভ ও অসম্ভব মান
df['বয়স'] = pd.to_numeric(df['বয়স'], errors='coerce')
df.loc[(df['বয়স'] < 0) | (df['বয়স'] > 100), 'বয়স'] = np.nan

# বেতন ফিক্স
df['বেতন'] = pd.to_numeric(df['বেতন'], errors='coerce')
df.loc[df['বেতন'] <= 0, 'বেতন'] = np.nan

print(f"\nটাইপ কনভার্শনের পর:\n{df.dtypes}")
print(f"বয়স রেঞ্জ: {df['বয়স'].min():.0f} - {df['বয়স'].max():.0f}")
print(f"বেতন রেঞ্জ: {df['বেতন'].min():.0f} - {df['বেতন'].max():.0f}")
```

### স্ট্রিং ক্লিনিং:
```python
print("=== স্ট্রিং ক্লিনিং ===")
# শহর ক্লিনিং
print(f"ইউনিক শহর (আগে): {df['শহর'].unique()}")

df['শহর'] = df['শহর'].str.strip().str.title()  # whitespace + capitalization
df['শহর'] = df['শহর'].replace({
    'Chittagong': 'চট্টগ্রাম',
    '': np.nan,
    'Nan': np.nan
})
# Fix any romanized versions
df['শহর'] = df['শহর'].apply(lambda x: 'চট্টগ্রাম' if isinstance(x, str) and x.upper().startswith('CH') else x)

print(f"ইউনিক শহর (পরে): {df['শহর'].dropna().unique()}")

# ইমেইল ভ্যালিডেশন
print(f"\nইমেইল চেক:")
valid_email = df['ইমেইল'].str.contains('@', na=False)
print(f"ভ্যালিড ইমেইল: {valid_email.sum()}")
print(f"ইনভ্যালিড ইমেইল: {(~valid_email).sum()}")
df.loc[~valid_email, 'ইমেইল'] = np.nan
```

### মিসিং ভ্যালু ইমপিউটেশন:
```python
print("=== মিসিং ভ্যালু ইমপিউটেশন ===")
print(f"ইমপিউটেশনের আগে মিসিং:\n{df.isnull().sum()}")

# নাম - মোড দিয়ে পূরণ
df['নাম'].fillna(df['নাম'].mode()[0], inplace=True)

# বয়স - মিডিয়ান দিয়ে পূরণ
df['বয়স'].fillna(df['বয়স'].median(), inplace=True)

# বেতন - গ্রুপ অনুযায়ী মিডিয়ান (এখনো no group, মিডিয়ান দিয়ে)
df['বেতন'].fillna(df['বেতন'].median(), inplace=True)

# শহর - মোড দিয়ে
df['শহর'].fillna(df['শহর'].mode()[0], inplace=True)

print(f"\nইমপিউটেশনের পরে মিসিং:\n{df.isnull().sum()}")
```

### ফিচার ইঞ্জিনিয়ারিং (বেসিক):
```python
print("=== বেসিক ফিচার ইঞ্জিনিয়ারিং ===")
# বয়স গ্রুপ
df['বয়স_গ্রুপ'] = pd.cut(df['বয়স'], 
    bins=[0, 25, 35, 50, 100], 
    labels=['তরুণ', 'যুব', 'মধ্যবয়সী', 'বয়স্ক'])

# বেতন ক্যাটাগরি
df['বেতন_শ্রেণী'] = pd.qcut(df['বেতন'], q=3, labels=['নিম্ন', 'মধ্যম', 'উচ্চ'])

# লগ ট্রান্সফর্ম (স্কিউড ডেটার জন্য)
df['লগ_বেতন'] = np.log1p(df['বেতন'])

print(f"বয়স গ্রুপ:\n{df['বয়স_গ্রুপ'].value_counts()}")
print(f"\nবেতন শ্রেণী:\n{df['বেতন_শ্রেণী'].value_counts()}")
```

### সম্পূর্ণ ক্লিনিং পাইপলাইন:
```python
def clean_pipeline(df):
    """সম্পূর্ণ ডেটা ক্লিনিং পাইপলাইন"""
    df_clean = df.copy()
    
    # 1. ডুপ্লিকেট সরান
    df_clean = df_clean.drop_duplicates()
    
    # 2. স্ট্রিং ক্লিন
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].str.strip().str.title()
    
    # 3. অসম্ভব মান ফিক্স
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        median_val = df_clean[col].median()
        std_val = df_clean[col].std()
        lower = median_val - 3 * std_val
        upper = median_val + 3 * std_val
        df_clean[col] = df_clean[col].clip(lower, upper)
    
    # 4. মিসিং ভ্যালু পূরণ
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)
        else:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    return df_clean

# পাইপলাইন রান
df_final = clean_pipeline(df)
print(f"=== ক্লিনিং পাইপলাইন ফলাফল ===")
print(f"আগে: {len(df)} সারি, {df.isnull().sum().sum()} মিসিং")
print(f"পরে: {len(df_final)} সারি, {df_final.isnull().sum().sum()} মিসিং")
print(f"\nফাইনাল ডেটা:\n{df_final.head()}")
```

### সারসংক্ষেপ:
- মিসিং ডেটা ডিটেকশন ও ইমপিউটেশন
- আউটলায়ার ডিটেকশন (Z-Score, IQR)
- ডুপ্লিকেট হ্যান্ডলিং
- স্ট্রিং ক্লিনিং ও টাইপ কনভার্শন
- অসম্ভব মান ফিক্সিং
- সম্পূর্ণ ডেটা ক্লিনিং পাইপলাইন