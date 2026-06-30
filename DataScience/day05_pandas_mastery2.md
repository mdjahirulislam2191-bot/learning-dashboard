# Day 05: Pandas মাস্টারি (পর্ব ২) - অ্যাডভান্সড টেকনিক
## Pandas Mastery (Part 2) - Advanced Techniques

### অ্যাডভান্সড ইন্ডেক্সিং:
```python
import pandas as pd
import numpy as np

# MultiIndex DataFrame
arrays = [
    ['ঢাকা', 'ঢাকা', 'চট্টগ্রাম', 'চট্টগ্রাম'],
    ['IT', 'HR', 'IT', 'HR']
]
index = pd.MultiIndex.from_arrays(arrays, names=['শহর', 'বিভাগ'])

df_multi = pd.DataFrame({
    'বেতন': [50000, 45000, 55000, 48000],
    'কর্মী_সংখ্যা': [100, 50, 80, 40]
}, index=index)

print("=== MultiIndex DataFrame ===")
print(df_multi)
print(f"\nঢাকার ডেটা:\n{df_multi.loc['ঢাকা']}")
print(f"\nIT বিভাগের ডেটা:\n{df_multi.xs('IT', level='বিভাগ')}")
```

### টাইম সিরিজ হ্যান্ডলিং:
```python
# ডেটটাইম ইনডেক্স
date_rng = pd.date_range('2024-01-01', periods=30, freq='D')
df_ts = pd.DataFrame(date_rng, columns=['তারিখ'])
df_ts['বিক্রয়'] = np.random.randint(100, 500, 30)
df_ts.set_index('তারিখ', inplace=True)

print("=== টাইম সিরিজ ডেটা ===")
print(df_ts.head(10))

# রিস্যাম্পলিং
weekly = df_ts.resample('W').sum()
monthly = df_ts.resample('M').mean()
print(f"\nসাপ্তাহিক বিক্রয়:\n{weekly}")
print(f"\nমাসিক গড় বিক্রয়:\n{monthly}")

# রোলিং উইন্ডো
df_ts['রোলিং_৭দিন'] = df_ts['বিক্রয়'].rolling(window=7).mean()
df_ts['এক্সপোনেনশিয়াল'] = df_ts['বিক্রয়'].ewm(span=7).mean()
print(f"\nরোলিং অ্যাভারেজ:\n{df_ts.head(10)}")
```

### অ্যাপ্লাই ফাংশন:
```python
df = pd.DataFrame({
    'নাম': ['আলিফ', 'বর্ণা', 'চন্দন', 'দীপা'],
    'বয়স': [25, 30, 28, 35],
    'বেতন': [50000, 60000, 45000, 70000]
})

# Element-wise apply
df['বেতন_শ্রেণী'] = df['বয়স'].apply(lambda x: 'তরুণ' if x < 30 else 'পরিণত')
print("=== Apply ফলাফল ===")
print(df)

# Row-wise apply
def categorize_row(row):
    if row['বেতন'] > 55000:
        return 'উচ্চ বেতন'
    elif row['বেতন'] > 45000:
        return 'মধ্যম বেতন'
    else:
        return 'নিম্ন বেতন'

df['বেতন_শ্রেণী'] = df.apply(categorize_row, axis=1)
print(df)

# Column-wise apply with agg
def salary_range(series):
    return series.max() - series.min()

print(f"\nবেতন রেঞ্জ: {df.apply(salary_range)}")
```

### স্ট্রিং অপারেশন:
```python
df_str = pd.DataFrame({
    'নাম': [' আলিফ ', 'বর্ণা!', 'চন্দন123', 'দীপা_খান'],
    'ইমেইল': ['alif@mail.com', 'BORNA@MAIL.COM', 'chandon@work', 'dipa@company.org'],
    'ফোন': ['০১৭১১১১১১১১', '০১৯২২২২২২২২', '০১৩৩৩৩৩৩৩৩৩', '০১৫৪৪৪৪৪৪৪৪']
})

print("=== স্ট্রিং অপারেশন ===")
df_str['নাম'] = df_str['নাম'].str.strip()  # whitespace remove
df_str['নাম'] = df_str['নাম'].str.replace(r'\d+', '', regex=True)  # digits remove
df_str['নাম'] = df_str['নাম'].str.replace(r'[!_]', '', regex=True)  # special chars remove
df_str['ইমেইল'] = df_str['ইমেইল'].str.lower()  # lowercase

print(df_str)

print(f"\nContains '@mail': {df_str['ইমেইল'].str.contains('@mail')}")
print(f"Start with '০১৭': {df_str['ফোন'].str.startswith('০১৭')}")
print(f"Split 'নাম':\n{df_str['নাম'].str.split(' ')}")
```

### ডেটা টাইপ কনভার্শন:
```python
df_types = pd.DataFrame({
    'আইডি': ['1', '2', '3', '4'],
    'বয়স': ['25.5', '30.2', '28.7', '35.1'],
    'নিবন্ধন': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05'],
    'সক্রিয়': ['True', 'False', 'True', 'True']
})

print("=== টাইপ কনভার্শনের আগে ===")
print(df_types.dtypes)

# টাইপ কনভার্শন
df_types['আইডি'] = pd.to_numeric(df_types['আইডি'])
df_types['বয়স'] = pd.to_numeric(df_types['বয়স'])
df_types['নিবন্ধন'] = pd.to_datetime(df_types['নিবন্ধন'])
df_types['সক্রিয়'] = df_types['সক্রিয়'].map({'True': True, 'False': False})

print("\n=== টাইপ কনভার্শনের পরে ===")
print(df_types.dtypes)
print(df_types)
```

### ডুপ্লিকেট হ্যান্ডলিং:
```python
df_dup = pd.DataFrame({
    'আইডি': [1, 2, 2, 3, 4, 4, 4],
    'নাম': ['আলিফ', 'বর্ণা', 'বর্ণা', 'চন্দন', 'দীপা', 'দীপা', 'দীপা'],
    'বেতন': [50000, 45000, 45000, 55000, 60000, 60000, 60000]
})

print("=== ডুপ্লিকেট ডেটা ===")
print(df_dup)
print(f"\nDuplicate rows: {df_dup.duplicated().sum()}")

# ডুপ্লিকেট সরানো
df_unique = df_dup.drop_duplicates()
print(f"\nডুপ্লিকেট সরানোর পর:\n{df_unique}")

# নির্দিষ্ট কলামে ডুপ্লিকেট চেক
print(f"আইডি তে ডুপ্লিকেট: {df_dup.duplicated(subset=['আইডి']).sum()}")
```

### আউটলায়ার ডিটেকশন:
```python
np.random.seed(42)
df_out = pd.DataFrame({
    'মান': np.random.randn(100) * 10 + 50
})

# কিছু আউটলায়ার যোগ
df_out.loc[0, 'মান'] = 200
df_out.loc[1, 'মান'] = -50
df_out.loc[2, 'মান'] = 250

# IQR পদ্ধতি
Q1 = df_out['মান'].quantile(0.25)
Q3 = df_out['মান'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df_out[(df_out['মান'] < lower_bound) | (df_out['মান'] > upper_bound)]
clean_data = df_out[(df_out['মান'] >= lower_bound) & (df_out['মান'] <= upper_bound)]

print(f"Total: {len(df_out)}")
print(f"Outliers: {len(outliers)}")
print(f"Clean: {len(clean_data)}")
print(f"Lower bound: {lower_bound:.2f}, Upper bound: {upper_bound:.2f}")
print(f"\nOutliers:\n{outliers}")
```

### উইন্ডো ফাংশন:
```python
df_win = pd.DataFrame({
    'গ্রুপ': ['A']*5 + ['B']*5,
    'মান': np.random.randint(1, 100, 10)
}).sort_values('গ্রুপ')

df_win['র্যাংক'] = df_win['মান'].rank(ascending=False)
df_win['গ্রুপ_র্যাংক'] = df_win.groupby('গ্রুপ')['মান'].rank(ascending=False)
df_win['কিউম_সাম'] = df_win.groupby('গ্রুপ')['মান'].cumsum()
df_win['ল্যাগ'] = df_win.groupby('গ্রুপ')['মান'].shift(1)
df_win['ডিফ'] = df_win.groupby('গ্রুপ')['মান'].diff()

print("=== উইন্ডো ফাংশন ===")
print(df_win)
```

### এক্সপোর্ট/ইম্পোর্ট:
```python
# DataFrame সেভ করা
df_export = pd.DataFrame({
    'নাম': ['আলিফ', 'বর্ণা', 'চন্দন'],
    'বয়স': [25, 30, 28],
    'বেতন': [50000, 60000, 45000]
})

# CSV
df_export.to_csv('output.csv', index=False, encoding='utf-8-sig')
df_csv = pd.read_csv('output.csv', encoding='utf-8-sig')
print("CSV থেকে:\n", df_csv)

# Excel (openpyxl প্রয়োজন)
# df_export.to_excel('output.xlsx', index=False)
# df_excel = pd.read_excel('output.xlsx')

# JSON
df_export.to_json('output.json', orient='records', force_ascii=False)
df_json = pd.read_json('output.json')
print("JSON থেকে:\n", df_json)

# Parquet (দ্রুত, ছোট ফাইল)
# df_export.to_parquet('output.parquet')
# df_pq = pd.read_parquet('output.parquet')

# Pickle
df_export.to_pickle('output.pkl')
df_pkl = pd.read_pickle('output.pkl')
print("\nPickle থেকে:\n", df_pkl)
```

### সারসংক্ষেপ:
- MultiIndex ও অ্যাডভান্সড ইন্ডেক্সিং
- টাইম সিরিজ হ্যান্ডলিং ও রিস্যাম্পলিং
- Apply ফাংশন ও ভেক্টরাইজেশন
- স্ট্রিং অপারেশন ও টাইপ কনভার্শন
- ডুপ্লিকেট ও আউটলায়ার হ্যান্ডলিং
- উইন্ডো ফাংশন ও ডেটা এক্সপোর্ট