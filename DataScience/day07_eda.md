# Day 07: Exploratory Data Analysis (EDA)
## এক্সপ্লোরেটরি ডেটা অ্যানালাইসিস

### EDA কী?
EDA হল ডেটা বোঝার, প্যাটার্ন খোঁজার এবং হাইপোথিসিস তৈরি করার একটি পদ্ধতি। এটি ডেটা সায়েন্স প্রজেক্টের প্রথম এবং গুরুত্বপূর্ণ ধাপ।

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 6)
sns.set_style('whitegrid')
plt.rcParams['font.size'] = 12
```

### ডেটাসেট তৈরি:
```python
np.random.seed(42)
n = 500

df = pd.DataFrame({
    'আইডি': range(1, n+1),
    'বয়স': np.random.normal(35, 10, n).astype(int).clip(18, 65),
    'বেতন': np.random.normal(60000, 20000, n).astype(int).clip(25000, 150000),
    'অভিজ্ঞতা': np.random.normal(8, 5, n).astype(int).clip(0, 35),
    'শিক্ষা_বছর': np.random.randint(10, 20, n),
    'বিভাগ': np.random.choice(['IT', 'HR', 'Sales', 'Marketing', 'Finance'], n, p=[0.3, 0.15, 0.25, 0.2, 0.1]),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট'], n),
    'পারফরম্যান্স': np.random.uniform(1, 5, n).round(1),
    'প্রজেক্ট_সম্পন্ন': np.random.poisson(5, n),
    'প্রশিক্ষণ_ঘন্টা': np.random.exponential(20, n).astype(int).clip(0, 100)
})

print(f"ডেটাসেট সাইজ: {df.shape}")
print(f"কলাম: {df.columns.tolist()}")
```

### ডেটার প্রাথমিক পরিদর্শন:
```python
print("=== ডেটার আভাস ===")
print(df.head(10))
print(f"\n=== পরিসংখ্যানিক সারাংশ ===")
print(df.describe())
print(f"\n=== ডেটার ধরন ===")
print(df.dtypes)
print(f"\n=== মিসিং ভ্যালু ===")
print(df.isnull().sum())
```

### ইউনিভেরিয়েট অ্যানালাইসিস (একক ভেরিয়েবল):
```python
print("=== ইউনিভেরিয়েট অ্যানালাইসিস ===")

# সংখ্যাত্মক ডেটার জন্য
numerical_cols = ['বয়স', 'বেতন', 'অভিজ্ঞতা', 'শিক্ষা_বছর', 'পারফরম্যান্স', 'প্রজেক্ট_সম্পন্ন']

for col in numerical_cols:
    print(f"\n--- {col} ---")
    print(f"Mean: {df[col].mean():.2f}")
    print(f"Median: {df[col].median():.2f}")
    print(f"Std: {df[col].std():.2f}")
    print(f"Skewness: {df[col].skew():.2f}")
    print(f"Kurtosis: {df[col].kurtosis():.2f}")
    
    # ভিজুয়ালাইজেশন
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # হিস্টোগ্রাম
    axes[0].hist(df[col], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0].axvline(df[col].mean(), color='red', linestyle='--', label=f'Mean: {df[col].mean():.1f}')
    axes[0].axvline(df[col].median(), color='green', linestyle='--', label=f'Median: {df[col].median():.1f}')
    axes[0].set_title(f'{col} - Distribution')
    axes[0].set_xlabel(col)
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    
    # বক্স প্লট
    axes[1].boxplot(df[col], vert=True, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    axes[1].set_title(f'{col} - Box Plot')
    axes[1].set_ylabel(col)
    
    plt.tight_layout()
    plt.show()
```

### ক্যাটেগোরিকাল ভেরিয়েবল অ্যানালাইসিস:
```python
print("=== ক্যাটেগোরিকাল ভেরিয়েবল অ্যানালাইসিস ===")
categorical_cols = ['বিভাগ', 'শহর']

for col in categorical_cols:
    print(f"\n--- {col} ---")
    value_counts = df[col].value_counts()
    percentages = df[col].value_counts(normalize=True) * 100
    
    freq_df = pd.DataFrame({
        'গণনা': value_counts,
        'শতাংশ': percentages.round(1)
    })
    print(freq_df)
    
    # বার প্লট
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    axes[0].bar(value_counts.index, value_counts.values, color='steelblue', edgecolor='black')
    axes[0].set_title(f'{col} - Frequency')
    axes[0].set_xlabel(col)
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)
    
    axes[1].pie(percentages, labels=percentages.index, autopct='%1.1f%%', startangle=90)
    axes[1].set_title(f'{col} - Percentage')
    
    plt.tight_layout()
    plt.show()
```

### বাইভেরিয়েট অ্যানালাইসিস (দুই ভেরিয়েবল):
```python
print("=== বাইভেরিয়েট অ্যানালাইসিস ===")

# সংখ্যাত্মক x সংখ্যাত্মক - Correlation
print("Correlation Matrix:")
numeric_df = df[numerical_cols]
corr_matrix = numeric_df.corr()
print(corr_matrix.round(3))

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

# Scatter plots - key relationships
key_pairs = [('বয়স', 'বেতন'), ('অভিজ্ঞতা', 'বেতন'), ('শিক্ষা_বছর', 'বেতন'), ('পারফরম্যান্স', 'প্রজেক্ট_সম্পন্ন')]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for idx, (x, y) in enumerate(key_pairs):
    row, col = idx // 2, idx % 2
    axes[row, col].scatter(df[x], df[y], alpha=0.5, c='steelblue', edgecolors='white', linewidth=0.5)
    axes[row, col].set_xlabel(x)
    axes[row, col].set_ylabel(y)
    axes[row, col].set_title(f'{x} vs {y}')
    
    # Regression line
    z = np.polyfit(df[x], df[y], 1)
    p = np.poly1d(z)
    axes[row, col].plot(df[x].sort_values(), p(df[x].sort_values()), "r--", alpha=0.8)

plt.tight_layout()
plt.show()
```

### ক্যাটেগোরিকাল x সংখ্যাত্মক অ্যানালাইসিস:
```python
print("=== ক্যাটেগোরিকাল x সংখ্যাত্মক ===")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

plot_data = [
    ('বিভাগ', 'বেতন'), ('বিভাগ', 'পারফরম্যান্স'), ('বিভাগ', 'প্রজেক্ট_সম্পন্ন'),
    ('শহর', 'বেতন'), ('শহর', 'পারফরম্যান্স'), ('শহর', 'প্রজেক্ট_সম্পন্ন')
]

for idx, (cat, num) in enumerate(plot_data):
    df.boxplot(column=num, by=cat, ax=axes[idx], grid=False)
    axes[idx].set_title(f'{num} by {cat}')
    axes[idx].set_xlabel(cat)
    axes[idx].set_ylabel(num)

plt.suptitle('')
plt.tight_layout()
plt.show()

# গ্রুপ পরিসংখ্যান
print("বিভাগ অনুযায়ী গড় বেতন:")
print(df.groupby('বিভাগ')['বেতন'].agg(['mean', 'std', 'count']).round(1))
print("\nশহর অনুযায়ী গড় পারফরম্যান্স:")
print(df.groupby('শহর')['পারফরম্যান্স'].agg(['mean', 'std', 'count']).round(2))
```

### মাল্টিভেরিয়েট অ্যানালাইসিস:
```python
print("=== মাল্টিভেরিয়েট অ্যানালাইসিস ===")

# Pairplot (সব সংখ্যাত্মক ভেরিয়েবলের সম্পর্ক)
sns.pairplot(df[numerical_cols], diag_kind='kde', plot_kws={'alpha': 0.5})
plt.suptitle('Pairplot of Numerical Variables', y=1.02)
plt.show()

# বিভাগ অনুযায়ী বেতন ও বয়সের সম্পর্ক
plt.figure(figsize=(12, 6))
for dept in df['বিভাগ'].unique():
    dept_data = df[df['বিভাগ'] == dept]
    plt.scatter(dept_data['বয়স'], dept_data['বেতন'], 
                label=dept, alpha=0.6, s=dept_data['প্রজেক্ট_সম্পন্ন']*10)
plt.xlabel('বয়স')
plt.ylabel('বেতন')
plt.title('Department-wise Age vs Salary (size = projects completed)')
plt.legend()
plt.tight_layout()
plt.show()
```

### ইনসাইট জেনারেশন:
```python
print("=== কী ইনসাইট ===")

# 1. Highest paid department
dept_salary = df.groupby('বিভাগ')['বেতন'].mean().sort_values(ascending=False)
print(f"1. সর্বোচ্চ গড় বেতনের বিভাগ: {dept_salary.index[0]} ({dept_salary.iloc[0]:,.0f} টাকা)")

# 2. City with best performance
city_perf = df.groupby('শহর')['পারফরম্যান্স'].mean().sort_values(ascending=False)
print(f"2. সর্বোচ্চ পারফরম্যান্সের শহর: {city_perf.index[0]} ({city_perf.iloc[0]:.2f})")

# 3. Correlation insights
corr_pairs = []
for i in range(len(numerical_cols)):
    for j in range(i+1, len(numerical_cols)):
        corr = corr_matrix.iloc[i, j]
        corr_pairs.append((numerical_cols[i], numerical_cols[j], abs(corr)))
corr_pairs.sort(key=lambda x: x[2], reverse=True)
print(f"3. সর্বোচ্চ Correlation: {corr_pairs[0][0]} & {corr_pairs[0][1]} ({corr_pairs[0][2]:.3f})")

# 4. Experience vs Salary trend
exp_bins = pd.cut(df['অভিজ্ঞতা'], bins=5)
exp_salary = df.groupby(exp_bins)['বেতন'].mean()
print(f"4. অভিজ্ঞতা অনুযায়ী বেতন ট্রেন্ড:")
print(exp_salary.round(0).astype(int))

# 5. Training hours effectiveness
training_bins = pd.cut(df['প্রশিক্ষণ_ঘন্টা'], bins=[0, 10, 20, 50, 100], labels=['Low', 'Medium', 'High', 'Very High'])
training_perf = df.groupby(training_bins)['পারফরম্যান্স'].mean()
print(f"\n5. প্রশিক্ষণ ঘন্টা ও পারফরম্যান্স:")
print(training_perf.round(2))
```

### EDA রিপোর্ট জেনারেশন:
```python
def generate_eda_report(df, title="EDA Report"):
    """EDA রিপোর্ট জেনারেটর"""
    print(f"========== {title} ==========")
    print(f"\nমোট সারি: {len(df)}")
    print(f"মোট কলাম: {len(df.columns)}")
    
    print(f"\n--- ডেটা কোয়ালিটি ---")
    print(f"ডুপ্লিকেট: {df.duplicated().sum()}")
    print(f"মিসিং ভ্যালু: {df.isnull().sum().sum()}")
    
    print(f"\n--- কলাম টাইপ ---")
    print(f"Numerical: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"Categorical: {len(df.select_dtypes(include=['object']).columns)}")
    
    print(f"\n--- পরিসংখ্যানিক সারাংশ ---")
    print(df.describe().round(2))
    
    print(f"\n--- টপ ইনসাইট ---")
    return df.describe()

report = generate_eda_report(df, "কর্মী ডেটা EDA রিপোর্ট")
```

### সারসংক্ষেপ:
- ইউনিভেরিয়েট, বাইভেরিয়েট, ও মাল্টিভেরিয়েট অ্যানালাইসিস
- সংখ্যাত্মক ও ক্যাটেগোরিকাল ডেটা ভিজুয়ালাইজেশন
- Correlation অ্যানালাইসিস
- গ্রুপ ভিত্তিক তুলনা
- কী ইনসাইট ও EDA রিপোর্ট জেনারেশন