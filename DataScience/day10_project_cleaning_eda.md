# Day 10: প্রোজেক্ট - এন্ড-টু-এন্ড ডেটা ক্লিনিং ও ইডিএ
## Project: End-to-End Data Cleaning & EDA

### প্রকল্প overview
আজ আমরা একটি সম্পূর্ণ ডেটা সায়েন্স প্রজেক্ট করব - কাঁচা ডেটা থেকে শুরু করে ক্লিনিং, ইডিএ এবং ইনসাইট জেনারেশন পর্যন্ত।

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 6)
sns.set_style('whitegrid')
plt.rcParams['font.size'] = 12
```

### ধাপ ১: ডেটা জেনারেশন ও লোডিং
```python
# একটি বাস্তবসম্মত ই-কমার্স ডেটাসেট তৈরি
np.random.seed(42)
n = 1000

# গ্রাহক ডেটা
customers = pd.DataFrame({
    'গ্রাহক_আইডি': range(1001, 1001+n),
    'নাম': [f'গ্রাহক_{i}' for i in range(1, n+1)],
    'বয়স': np.random.randint(18, 70, n).astype(float),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা', 'অন্যান্য'], n, p=[0.48, 0.48, 0.04]),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট', 'বরিশাল', 'রংপুর', 'ময়মনসিংহ'], n),
    'নিবন্ধন_তারিখ': pd.to_datetime(np.random.choice(pd.date_range('2020-01-01', '2024-06-01'), n))
})

# লেনদেন ডেটা
transactions = pd.DataFrame({
    'লেনদেন_আইডি': range(2001, 2001+n),
    'গ্রাহক_আইডি': np.random.choice(customers['গ্রাহক_আইডি'], n),
    'পণ্য_বিভাগ': np.random.choice(['ইলেকট্রনিক্স', 'ফ্যাশন', 'খাদ্য', 'বই', 'হোম', 'স্পোর্টস'], n, 
                                   p=[0.25, 0.2, 0.15, 0.1, 0.2, 0.1]),
    'পরিমাণ': np.random.poisson(2, n).clip(1, 10),
    'মূল্য': np.round(np.random.uniform(100, 50000, n), 0),
    'ডিসকাউন্ট': np.random.choice([0, 5, 10, 15, 20, 25, 30], n, p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]),
    'লেনদেন_তারিখ': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2024-06-01'), n)),
    'পেমেন্ট_পদ্ধতি': np.random.choice(['বিকাশ', 'নগদ', 'ক্রেডিট', 'ডেবিট', 'ক্যাশ অন'], n,
                                        p=[0.3, 0.25, 0.2, 0.15, 0.1])
})

# কিছু intentional missing value যোগ
customers.loc[::15, 'বয়স'] = np.nan
customers.loc[::25, 'শহর'] = np.nan
transactions.loc[::20, 'পরিমাণ'] = np.nan
transactions.loc[::30, 'মূল্য'] = -1  # নেগেটিভ ভ্যালু

# কিছু ডুপ্লিকেট
customers = pd.concat([customers, customers.iloc[:10]], ignore_index=True)

print(f"গ্রাহক ডেটা: {customers.shape}")
print(f"লেনদেন ডেটা: {transactions.shape}")
print("\nগ্রাহক ডেটার প্রথম ৫টি সারি:")
print(customers.head())
print("\nলেনদেন ডেটার প্রথম ৫টি সারি:")
print(transactions.head())
```

### ধাপ ২: ডেটা ক্লিনিং
```python
print("========== ডেটা ক্লিনিং শুরু ==========")

def clean_customer_data(df):
    """গ্রাহক ডেটা ক্লিনিং"""
    df = df.copy()
    
    print("১. ডুপ্লিকেট অপসারণ...")
    before = len(df)
    df = df.drop_duplicates()
    print(f"   অপসারিত: {before - len(df)} টি ডুপ্লিকেট")
    
    print("২. বয়স ফিল্টারিং...")
    initial_missing = df['বয়স'].isnull().sum()
    df.loc[(df['বয়স'] < 18) | (df['বয়স'] > 70), 'বয়স'] = np.nan
    df['বয়স'].fillna(df['বয়স'].median(), inplace=True)
    print(f"   ইমপিউটেড: {initial_missing} টি মিসিং")
    
    print("৩. শহর ক্লিনিং...")
    df['শহর'] = df['শহর'].str.strip().str.title()
    df['শহর'].fillna('ঢাকা', inplace=True)
    
    print("৪. লিঙ্গ ক্লিনিং...")
    df['লিঙ্গ'] = df['লিঙ্গ'].str.strip()
    df['লিঙ্গ'].fillna('অন্যান্য', inplace=True)
    
    print("৫. ডেট টাইপ কনভার্শন...")
    df['বয়স'] = df['বয়স'].astype(int)
    
    return df

def clean_transaction_data(df):
    """লেনদেন ডেটা ক্লিনিং"""
    df = df.copy()
    
    print("\n৬. নেগেটিভ মূল্য ফিক্সিং...")
    neg_mask = df['মূল্য'] < 0
    print(f"   পজিটিভে রূপান্তরিত: {neg_mask.sum()} টি")
    df.loc[neg_mask, 'মূল্য'] = df.loc[neg_mask, 'মূল্য'].abs()
    
    print("৭. পরিমাণ মিসিং ইমপিউট...")
    df['পরিমাণ'].fillna(1, inplace=True)
    df['পরিমাণ'] = df['পরিমাণ'].astype(int)
    
    print("৮. মোট মূল্য গণনা...")
    df['মোট_মূল্য'] = df['পরিমাণ'] * df['মূল্য'] * (1 - df['ডিসকাউন্ট'] / 100)
    df['মোট_মূল্য'] = df['মোট_মূল্য'].round(2)
    
    print("৯. আউটলায়ার ডিটেকশন...")
    Q1 = df['মোট_মূল্য'].quantile(0.25)
    Q3 = df['মোট_মূল্য'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df['মোট_মূল্য'] < lower) | (df['মোট_মূল্য'] > upper)]
    print(f"   আউটলায়ার (মোট_মূল্য): {len(outliers)} টি ({len(outliers)/len(df)*100:.1f}%)")
    
    return df

# ডেটা ক্লিনিং রান
customers = clean_customer_data(customers)
transactions = clean_transaction_data(transactions)
print("\n✅ ডেটা ক্লিনিং সম্পন্ন!")
print(f"গ্রাহক: {customers.shape}, লেনদেন: {transactions.shape}")
```

### ধাপ ৩: ডেটা মার্জিং
```python
print("========== ডেটা মার্জিং ==========")
# গ্রাহক ও লেনদেন ডেটা যোগ করা
df = pd.merge(transactions, customers, on='গ্রাহক_আইডি', how='left')
print(f"মার্জড ডেটা: {df.shape}")
print(f"\nকলাম: {df.columns.tolist()}")
print("\nডেটা টাইপ:")
print(df.dtypes)
print(f"\nমিসিং ভ্যালু:\n{df.isnull().sum()}")
```

### ধাপ ৪: Exploratory Data Analysis
```python
print("========== Exploratory Data Analysis ==========")

# 1. ইউনিভেরিয়েট অ্যানালাইসিস
print("\n--- ইউনিভেরিয়েট অ্যানালাইসিস ---")
print("বেসিক পরিসংখ্যান:")
print(df[['মোট_মূল্য', 'পরিমাণ', 'ডিসকাউন্ট', 'বয়স']].describe())

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Total Revenue Distribution
sns.histplot(df['মোট_মূল্য'], bins=50, kde=True, ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('মোট মূল্য বিতরণ')
axes[0, 0].axvline(df['মোট_মূল্য'].mean(), color='red', linestyle='--', label='Mean')
axes[0, 0].legend()

# Discount Distribution
sns.countplot(x='ডিসকাউন্ট', data=df, ax=axes[0, 1], palette='Set2')
axes[0, 1].set_title('ডিসকাউন্ট বিতরণ')

# Age Distribution
sns.histplot(df['বয়স'], bins=30, kde=True, ax=axes[0, 2], color='green')
axes[0, 2].set_title('গ্রাহক বয়স বিতরণ')

# Category Distribution
df['পণ্য_বিভাগ'].value_counts().plot(kind='bar', ax=axes[1, 0], color='orange', edgecolor='black')
axes[1, 0].set_title('পণ্য বিভাগ অনুযায়ী বিক্রয়')
axes[1, 0].tick_params(axis='x', rotation=45)

# City Distribution
df['শহর'].value_counts().plot(kind='bar', ax=axes[1, 1], color='purple', edgecolor='black')
axes[1, 1].set_title('শহর অনুযায়ী গ্রাহক')

# Payment Method
df['পেমেন্ট_পদ্ধতি'].value_counts().plot(kind='bar', ax=axes[1, 2], color='teal', edgecolor='black')
axes[1, 2].set_title('পেমেন্ট পদ্ধতি')
axes[1, 2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

### ধাপ ৫: বাইভেরিয়েট ও মাল্টিভেরিয়েট অ্যানালাইসিস
```python
print("\n--- বাইভেরিয়েট অ্যানালাইসিস ---")

# Correlation Matrix
num_cols = ['মোট_মূল্য', 'পরিমাণ', 'মূল্য', 'ডিসকাউন্ট', 'বয়স']
corr_matrix = df[num_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, fmt='.2f')
plt.title('ফিচার কোরিলেশন ম্যাট্রিক্স')
plt.tight_layout()
plt.show()

# Category-wise Analysis
print("\nপণ্য বিভাগ অনুযায়ী বিশ্লেষণ:")
category_analysis = df.groupby('পণ্য_বিভাগ').agg({
    'মোট_মূল্য': ['sum', 'mean', 'count'],
    'ডিসকাউন্ট': 'mean',
    'গ্রাহক_আইডি': 'nunique'
}).round(2)
print(category_analysis)

# City-wise Revenue
print("\nশহর অনুযায়ী রাজস্ব:")
city_revenue = df.groupby('শহর')['মোট_মূল্য'].sum().sort_values(ascending=False)
print(city_revenue)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Revenue by Category
df.boxplot(column='মোট_মূল্য', by='পণ্য_বিভাগ', ax=axes[0, 0])
axes[0, 0].set_title('বিভাগ অনুযায়ী মূল্য বিতরণ')
axes[0, 0].tick_params(axis='x', rotation=45)

# Revenue by Age Group
age_bins = pd.cut(df['বয়স'], bins=[18, 25, 35, 45, 55, 70], 
                  labels=['18-25', '26-35', '36-45', '46-55', '56-70'])
age_revenue = df.groupby(age_bins)['মোট_মূল্য'].mean()
age_revenue.plot(kind='bar', ax=axes[0, 1], color='coral', edgecolor='black')
axes[0, 1].set_title('বয়স গ্রুপ অনুযায়ী গড় মূল্য')
axes[0, 1].set_xlabel('বয়স গ্রুপ')
axes[0, 1].tick_params(axis='x', rotation=45)

# Payment Method vs Revenue
df.boxplot(column='মোট_মূল্য', by='পেমেন্ট_পদ্ধতি', ax=axes[1, 0])
axes[1, 0].set_title('পেমেন্ট পদ্ধতি অনুযায়ী মূল্য')
axes[1, 0].tick_params(axis='x', rotation=45)

# Discount Impact
sns.scatterplot(x='ডিসকাউন্ট', y='মোট_মূল্য', data=df, ax=axes[1, 1], alpha=0.3)
axes[1, 1].set_title('ডিসকাউন্ট বনাম মোট মূল্য')
sns.regplot(x='ডিসকাউন্ট', y='মোট_মূল্য', data=df, scatter=False, ax=axes[1, 1], color='red')

plt.suptitle('')
plt.tight_layout()
plt.show()
```

### ধাপ ৬: টাইম সিরিজ অ্যানালাইসিস
```python
print("\n--- টাইম সিরিজ অ্যানালাইসিস ---")

# লেনদেন তারিখ থেকে ফিচার
df['লেনদেন_বছর'] = df['লেনদেন_তারিখ'].dt.year
df['লেনদেন_মাস'] = df['লেনদেন_তারিখ'].dt.month
df['লেনদেন_দিন'] = df['লেনদেন_তারিখ'].dt.day
df['লেনদেন_দিনের_নাম'] = df['লেনদেন_তারিখ'].dt.day_name()
df['লেনদেন_সপ্তাহান্ত'] = (df['লেনদেন_তারিখ'].dt.weekday >= 5).astype(int)

# মাসিক বিক্রয়
monthly_sales = df.groupby(['লেনদেন_বছর', 'লেনদেন_মাস'])['মোট_মূল্য'].sum().reset_index()
monthly_sales['তারিখ'] = pd.to_datetime(monthly_sales[['লেনদেন_বছর', 'লেনদেন_মাস']].assign(day=1))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Monthly Trend
axes[0].plot(monthly_sales['তারিখ'], monthly_sales['মোট_মূল্য'], 'o-', color='steelblue', linewidth=2)
axes[0].set_title('মাসিক বিক্রয় ট্রেন্ড')
axes[0].set_xlabel('তারিখ')
axes[0].set_ylabel('মোট বিক্রয়')
axes[0].grid(True, alpha=0.3)

# Day of week analysis
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_sales = df.groupby('লেনদেন_দিনের_নাম')['মোট_মূল্য'].mean().reindex(day_order)
day_sales.plot(kind='bar', ax=axes[1], color='steelblue', edgecolor='black')
axes[1].set_title('সপ্তাহের দিন অনুযায়ী গড় বিক্রয়')
axes[1].set_xlabel('দিন')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

print("\nসপ্তাহান্তে বনাম সপ্তাহের দিনে বিক্রয়:")
print(df.groupby('লেনদেন_সপ্তাহান্ত')['মোট_মূল্য'].describe())
```

### ধাপ ৭: ইনসাইট ও সিদ্ধান্ত
```python
print("========== কী ইনসাইট ও সুপারিশ ==========")

# 1. Top revenue category
top_cat = df.groupby('পণ্য_বিভাগ')['মোট_মূল্য'].sum().idxmax()
print(f"1. সর্বোচ্চ রাজস্ব উৎপন্ন বিভাগ: {top_cat}")

# 2. Best city
best_city = df.groupby('শহর')['মোট_মূল্য'].sum().idxmax()
print(f"2. সর্বোচ্চ রাজস্বের শহর: {best_city}")

# 3. Average basket value
avg_basket = df['মোট_মূল্য'].mean()
print(f"3. গড় বাস্কেট ভ্যালু: {avg_basket:,.2f} টাকা")

# 4. Most common payment
top_payment = df['পেমেন্ট_পদ্ধতি'].mode()[0]
print(f"4. সবচেয়ে জনপ্রিয় পেমেন্ট পদ্ধতি: {top_payment}")

# 5. Customer age group with highest spending
top_age_group = age_revenue.idxmax()
print(f"5. সর্বোচ্চ ব্যয়কারী বয়স গ্রুপ: {top_age_group}")

# 6. Discount effectiveness
discount_effectiveness = df.groupby('ডিসকাউন্ট')['মোট_মূল্য'].mean()
best_discount = discount_effectiveness.idxmax()
print(f"6. সর্বোচ্চ গড় বিক্রয়ের ডিসকাউন্ট: {best_discount}%")

# 7. Weekend vs weekday
weekday_rev = df.groupby('লেনদেন_সপ্তাহান্ত')['মোট_মূল্য'].mean()
print(f"7. সপ্তাহান্তে গড় বিক্রয়: {weekday_rev[1]:,.2f}")
print(f"   সপ্তাহের দিনে গড় বিক্রয়: {weekday_rev[0]:,.2f}")
```

### ধাপ ৮: ফাইনাল রিপোর্ট
```python
print("\n" + "="*60)
print("📊 ই-কমার্স ডেটা অ্যানালাইসিস - ফাইনাল রিপোর্ট")
print("="*60)

print(f"""
📌 ডেটাসেট তথ্য:
   - মোট গ্রাহক: {customers['গ্রাহক_আইডি'].nunique()}
   - মোট লেনদেন: {len(transactions)}
   - সময়কাল: {transactions['লেনদেন_তারিখ'].min().date()} থেকে {transactions['লেনদেন_তারিখ'].max().date()}

📌 রাজস্ব বিশ্লেষণ:
   - মোট রাজস্ব: {df['মোট_মূল্য'].sum():,.2f} টাকা
   - গড় লেনদেন: {df['মোট_মূল্য'].mean():,.2f} টাকা
   - সর্বোচ্চ লেনদেন: {df['মোট_মূল্য'].max():,.2f} টাকা
   - সর্বনিম্ন লেনদেন: {df['মোট_মূল্য'].min():,.2f} টাকা

📌 গ্রাহক বিশ্লেষণ:
   - গড় বয়স: {df['বয়স'].mean():.1f} বছর
   - সবচেয়ে সক্রিয় শহর: {df['শহর'].value_counts().idxmax()}
   - জনপ্রিয় পেমেন্ট: {df['পেমেন্ট_পদ্ধতি'].value_counts().idxmax()}

📌 টপ সুপারিশ:
   1. {top_cat} বিভাগে ফোকাস বাড়ান
   2. {best_city} শহরে মার্কেটিং বাড়ান
   3. {best_discount}% ডিসকাউন্ট অফার চালিয়ে যান
   4. সপ্তাহান্তে স্পেশাল অফার দিন
""")
```

### সারসংক্ষেপ:
- সম্পূর্ণ এন্ড-টু-এন্ড ডেটা সায়েন্স প্রজেক্ট
- ডেটা ক্লিনিং ও প্রিপ্রসেসিং
- Exploratory Data Analysis (EDA)
- ডেটা ভিজুয়ালাইজেশন
- বিজনেস ইনসাইট জেনারেশন
- অ্যাকশনেবল সুপারিশ