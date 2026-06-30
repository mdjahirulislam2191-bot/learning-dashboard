# Day 04: Pandas মাস্টারি (পর্ব ১)
## Pandas Mastery (Part 1)

### Pandas কী?
Pandas হলো পাইথনের সবচেয়ে জনপ্রিয় ডেটা ম্যানিপুলেশন লাইব্রেরি। এটি DataFrame ও Series নামক ডেটা স্ট্রাকচার সরবরাহ করে।

```python
import pandas as pd
import numpy as np

print(f"Pandas ভার্সন: {pd.__version__}")
```

### Series তৈরি ও ম্যানিপুলেশন:
```python
# Series তৈরি
s1 = pd.Series([1, 2, 3, 4, 5])
s2 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
s3 = pd.Series({'a': 1, 'b': 2, 'c': 3})
s4 = pd.Series(np.random.randn(5), name='random_values')

print(f"Series 1:\n{s1}\n")
print(f"Series with index:\n{s2}\n")
print(f"Series from dict:\n{s3}\n")
print(f"Series with name:\n{s4}\n")

# Series অপারেশন
print(f"Mean: {s2.mean():.2f}")
print(f"Sum: {s2.sum()}")
print(f"Std: {s2.std():.2f}")
print(f"Value Counts:\n{s4.value_counts(bins=3)}")

# Series ম্যাপিং
s = pd.Series(['ঢাকা', 'চট্টগ্রাম', 'খুলনা'])
mapped = s.map({'ঢাকা': 'Dhaka', 'চট্টগ্রাম': 'Chittagong', 'খুলনা': 'Khulna'})
print(f"Mapped: {mapped}")
```

### DataFrame তৈরি:
```python
# বিভিন্ন উপায়ে DataFrame তৈরি
# 1. Dictionary থেকে
df1 = pd.DataFrame({
    'নাম': ['আলিফ', 'বর্ণা', 'চন্দন'],
    'বয়স': [25, 30, 28],
    'বেতন': [50000, 60000, 45000]
})

# 2. NumPy array থেকে
df2 = pd.DataFrame(
    np.random.randn(4, 3),
    columns=['A', 'B', 'C'],
    index=['রো1', 'রো2', 'রো3', 'রো4']
)

# 3. CSV/Excel থেকে (সিমুলেটেড)
data = {
    'তারিখ': pd.date_range('2024-01-01', periods=5, freq='D'),
    'প্রোডাক্ট': ['A', 'B', 'C', 'D', 'E'],
    'বিক্রয়': np.random.randint(100, 1000, 5),
    'লাভ': np.random.uniform(10, 50, 5).round(2)
}
df3 = pd.DataFrame(data)

print("=== DataFrame 1 ===")
print(df1)
print(f"\n=== DataFrame 2 ===")
print(df2)
print(f"\n=== DataFrame 3 (টাইম সিরিজ) ===")
print(df3)
```

### DataFrame এক্সপ্লোরেশন:
```python
# বড় ডেটাসেট তৈরি
np.random.seed(42)
n = 100
df = pd.DataFrame({
    'আইডি': range(1, n+1),
    'বয়স': np.random.randint(18, 65, n),
    'বেতন': np.random.randint(25000, 120000, n),
    'অভিজ্ঞতা': np.random.randint(0, 30, n),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট'], n),
    'বিভাগ': np.random.choice(['IT', 'HR', 'Sales', 'Marketing', 'Finance'], n)
})

print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data Types:\n{df.dtypes}")
print(f"\nHead (প্রথম ৫):\n{df.head()}")
print(f"\nTail (শেষ ৫):\n{df.tail()}")
print(f"\nInfo:\n{df.info()}")
print(f"\nDescribe:\n{df.describe()}")
```

### ডেটা সিলেকশন ও ফিল্টারিং:
```python
print("=== কলাম সিলেকশন ===")
print(f"একটি কলাম:\n{df['নাম'] if 'নাম' in df.columns else df['বয়с']['head']}")  
# Let's use numeric columns
print(f"বয়স কলাম (প্রথম ৫):\n{df['বয়স'].head()}")
print(f"\nএকাধিক কলাম:\n{df[['নাম', 'বয়স', 'বেতন']].head() if 'নাম' in df.columns else df[['বয়স', 'বেতন']].head()}")

print("\n=== রো সিলেকশন ===")
print(f"loc (label-based):\n{df.loc[0:5, ['বয়স', 'বেতন']]}")
print(f"\niloc (position-based):\n{df.iloc[0:5, 0:3]}")

print("\n=== ফিল্টারিং ===")
young = df[df['বয়স'] < 30]
high_salary = df[df['বেতন'] > 80000]
it_dept = df[df['বিভাগ'] == 'IT']
complex_filter = df[(df['বয়স'] > 30) & (df['বেতন'] > 50000)]

print(f"তরুণ কর্মী (<30): {len(young)} জন")
print(f"উচ্চ বেতন (>80k): {len(high_salary)} জন")
print(f"IT বিভাগ: {len(it_dept)} জন")
print(f"কমপ্লেক্স ফিল্টার: {len(complex_filter)} জন")
```

### নাল ভ্যালু হ্যান্ডলিং:
```python
# নাল ভ্যালুযুক্ত ডেটা
df_nan = df.copy()
df_nan.loc[::10, 'বেতন'] = np.nan
df_nan.loc[::15, 'বয়স'] = np.nan

print(f"Missing values:\n{df_nan.isnull().sum()}")
print(f"\nTotal missing: {df_nan.isnull().sum().sum()}")

# নাল ভ্যালু অপসারণ
df_drop = df_nan.dropna()
print(f"\nAfter dropna: {len(df_drop)} rows")

# নাল ভ্যালু পূরণ
df_fill = df_nan.fillna({
    'বেতন': df_nan['বেতন'].mean(),
    'বয়স': df_nan['বয়স'].median()
})
print(f"After fillna:\n{df_fill.isnull().sum()}")

# Forward/Backward fill
df_ffill = df_nan.ffill()
df_bfill = df_nan.bfill()
print(f"Forward fill missing: {df_ffill.isnull().sum().sum()}")
print(f"Backward fill missing: {df_bfill.isnull().sum().sum()}")
```

### গ্রুপিং ও এগ্রিগেশন:
```python
print("=== গ্রুপ অপারেশন ===")
# শহর অনুযায়ী গ্রুপ
city_group = df.groupby('শহর')
print(f"শহর অনুযায়ী গড় বেতন:\n{city_group['বেতন'].mean().round(0).astype(int)}")

# বিভাগ অনুযায়ী এগ্রিগেশন
dept_agg = df.groupby('বিভাগ').agg({
    'বেতন': ['mean', 'std', 'min', 'max'],
    'বয়স': 'mean',
    'আইডি': 'count'
}).round(1)
print(f"\nবিভাগ অনুযায়ী পরিসংখ্যান:\n{dept_agg}")

# মাল্টিপল গ্রুপ
multi_group = df.groupby(['শহর', 'বিভাগ'])['বেতন'].mean().round(0).astype(int)
print(f"\nশহর ও বিভাগ অনুযায়ী:\n{multi_group}")
```

### মার্জিং ও জয়েনিং:
```python
# দুইটি DataFrame যোগ করা
df_left = pd.DataFrame({
    'আইডি': [1, 2, 3, 4],
    'নাম': ['আলিফ', 'বর্ণা', 'চন্দন', 'দীপা'],
    'বিভাগ': ['IT', 'HR', 'IT', 'Sales']
})

df_right = pd.DataFrame({
    'আইডি': [1, 2, 3, 5],
    'বেতন': [50000, 45000, 60000, 55000],
    'শহর': ['ঢাকা', 'চট্টগ্রাম', 'ঢাকা', 'খুলনা']
})

print("=== Inner Join ===")
inner = pd.merge(df_left, df_right, on='আইডি', how='inner')
print(inner)

print("\n=== Left Join ===")
left = pd.merge(df_left, df_right, on='আইডি', how='left')
print(left)

print("\n=== Outer Join ===")
outer = pd.merge(df_left, df_right, on='আইডি', how='outer')
print(outer)

# Concat
df_concat = pd.concat([df_left, df_right[['আইডি', 'বেতন']]], axis=1)
print(f"\nConcat:\n{df_concat}")
```

### পিভট টেবিল:
```python
print("=== Pivot Table ===")
pivot = pd.pivot_table(
    df,
    values='বেতন',
    index='শহর',
    columns='বিভাগ',
    aggfunc='mean',
    fill_value=0
).round(0).astype(int)
print(pivot)

# Crosstab
ct = pd.crosstab(df['শহর'], df['বিভাগ'])
print(f"\nCrosstab:\n{ct}")
```

### সারসংক্ষেপ:
- Series ও DataFrame তৈরি
- ডেটা এক্সপ্লোরেশন ও পরিসংখ্যান
- ডেটা সিলেকশন, ফিল্টারিং
- নাল ভ্যালু হ্যান্ডলিং
- গ্রুপিং ও এগ্রিগেশন
- মার্জিং, জয়েনিং, পিভট টেবিল