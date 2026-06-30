# Day 29: ক্যাপস্টোন প্রজেক্ট — পার্ট ১: ডেটা প্রিপারেশন ও EDA
## Capstone Project Part 1: Data Preparation & Exploratory Data Analysis

### প্রজেক্ট ওভারভিউ
এটি একটি সম্পূর্ণ ডেটা সায়েন্স ক্যাপস্টোন প্রজেক্টের প্রথম অংশ। আমরা একটি ব্যাংকিং ডেটাসেট নিয়ে কাজ করব — গ্রাহক লোন ডিফল্ট প্রেডিকশন। পার্ট ১-এ আমরা ডেটা প্রিপারেশন, ক্লিনিং ও EDA করব।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')
pd.set_option('display.max_columns', None)

np.random.seed(42)
```

### ক্যাপস্টোন প্রজেক্টের পরিকল্পনা
```python
print("=" * 60)
print("ক্যাপস্টোন প্রজেক্ট: লোন ডিফল্ট প্রেডিকশন")
print("=" * 60)

plan = """
## প্রজেক্ট প্ল্যান (৪ সপ্তাহ)

### পার্ট ১ (Day 29) — ডেটা প্রিপারেশন ও EDA
📌 ডেটাসেট তৈরি/সংগ্রহ
📌 ডেটা ক্লিনিং (মিসিং, আউটলায়ার, ডুপ্লিকেট)
📌 এক্সপ্লোরেটরি ডেটা অ্যানালাইসিস
📌 ফিচার ইঞ্জিনিয়ারিং
📌 ট্রেন-টেস্ট স্প্লিট

### পার্ট ২ (Day 30) — মডেলিং ও ডিপ্লয়মেন্ট
📌 একাধিক মডেল ট্রেনিং (Reg, RF, XGBoost)
📌 হাইপারপ্যারামিটার টিউনিং
📌 মডেল ইভালুয়েশন
📌 ফিচার ইম্পরট্যান্স
📌 বিজনেস রিপোর্ট

## ডেটাসেট: ব্যাংক লোন ডিফল্ট
লক্ষ্য: গ্রাহক লোন ডিফল্ট করবে কিনা (Yes/No) তা পূর্বাভাস করা
"""
print(plan)
```

### স্টেপ ১: ডেটাসেট তৈরি
```python
print("\n=== স্টেপ ১: ডেটাসেট তৈরি ===")

n_customers = 5000

loan_data = pd.DataFrame({
    'গ্রাহক_আইডি': range(1, n_customers + 1),
    'বয়স': np.random.randint(18, 75, n_customers),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা'], n_customers, p=[0.55, 0.45]),
    'বার্ষিক_আয়': np.random.lognormal(11, 0.6, n_customers).astype(int),
    'ক্রেডিট_স্কোর': np.random.randint(300, 850, n_customers),
    'লোন_পরিমাণ': np.random.lognormal(10.5, 0.8, n_customers).astype(int),
    'লোন_মেয়াদ_মাস': np.random.choice([12, 24, 36, 48, 60], n_customers, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
    'সুদের_হার': np.random.uniform(5, 25, n_customers).round(2),
    'বর্তমান_ঋণ_অনুপাত': np.random.uniform(0, 50, n_customers).round(1),
    'কাজের_অভিজ্ঞতা_বছর': np.random.randint(0, 40, n_customers),
    'নিয়োগ_স্থিতি': np.random.choice(['নিযুক্ত', 'স্বনিযুক্ত', 'বেকার'], n_customers, p=[0.7, 0.2, 0.1]),
    'বিবাহিত': np.random.choice(['হ্যাঁ', 'না'], n_customers),
    'নির্ভরশীল_সংখ্যা': np.random.choice([0, 1, 2, 3, 4], n_customers, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
    'আবাসন_স্থিতি': np.random.choice(['নিজস্ব', 'ভাড়া', 'বন্ধক'], n_customers, p=[0.4, 0.35, 0.25]),
    'পূর্ববর্তী_লোন_ডিফল্ট': np.random.choice([0, 1], n_customers, p=[0.85, 0.15]),
    'ক্রেডিট_কার্ড_বয়স_মাস': np.random.randint(0, 240, n_customers),
    'ব্যাংক_অ্যাকাউন্ট_ধরন': np.random.choice(['সেভিংস', 'কারেন্ট', 'উভয়'], n_customers, p=[0.3, 0.3, 0.4]),
    'মাসিক_খরচ': np.random.lognormal(9.5, 0.6, n_customers).astype(int),
    'ইনকাম_টু_লোন_রেশিও': np.random.uniform(0.1, 5, n_customers).round(2),
})

# লোন ডিফল্ট লেবেল তৈরি (টার্গেট ভ্যারিয়েবল)
default_prob = np.zeros(n_customers)
default_prob += (loan_data['ক্রেডিট_স্কোর'] < 600) * 0.25
default_prob += (loan_data['ক্রেডিট_স্কোর'] < 500) * 0.20
default_prob += (loan_data['বর্তমান_ঋণ_অনুপাত'] > 35) * 0.12
default_prob += (loan_data['পূর্ববর্তী_লোন_ডিফল্ট'] == 1) * 0.15
default_prob += (loan_data['ইনকাম_টু_লোন_রেশিও'] < 0.5) * 0.10
default_prob += (loan_data['নিয়োগ_স্থিতি'] == 'বেকার') * 0.15
default_prob += (loan_data['লোন_পরিমাণ'] > 50000) * 0.08
default_prob = np.clip(default_prob, 0.01, 0.90)

loan_data['লোন_ডিফল্ট'] = np.random.binomial(1, default_prob)

# কিছু মিসিং ভ্যালু যোগ করা (রিয়েলিস্টিক)
for col in ['ক্রেডিট_স্কোর', 'বার্ষিক_আয়', 'কাজের_অভিজ্ঞতা_বছর', 'ইনকাম_টু_লোন_রেশিও']:
    missing_idx = np.random.choice(n_customers, size=int(n_customers * 0.03), replace=False)
    loan_data.loc[missing_idx, col] = np.nan

print(f"মোট গ্রাহক: {len(loan_data)}")
print(f"ফিচার সংখ্যা: {len(loan_data.columns)}")
print(f"লোন ডিফল্ট রেট: {loan_data['লোন_ডিফল্ট'].mean()*100:.2f}%")
print(f"\nমিসিং ভ্যালু (প্রতি ফিচার):")
print(loan_data.isnull().sum()[loan_data.isnull().sum() > 0])
print("\nপ্রথম ৫টি রেকর্ড:")
print(loan_data.head())
```

### স্টেপ ২: ডেটা ক্লিনিং
```python
print("\n=== স্টেপ ২: ডেটা ক্লিনিং ===")

# ডুপ্লিকেট চেক
duplicates = loan_data.duplicated(subset=['গ্রাহক_আইডি']).sum()
print(f"ডুপ্লিকেট রেকর্ড: {duplicates}")

# মিসিং ভ্যালু হ্যান্ডলিং
print("\nমিসিং ভ্যালু হ্যান্ডলিং:")

# নিউমেরিক কলাম — মিডিয়ান দিয়ে ফিল
numeric_cols_with_missing = ['ক্রেডিট_স্কোর', 'বার্ষিক_আয়', 'কাজের_অভিজ্ঞতা_বছর', 'ইনকাম_টু_লোন_রেশিও']
imputer = SimpleImputer(strategy='median')
loan_data[numeric_cols_with_missing] = imputer.fit_transform(loan_data[numeric_cols_with_missing])

print("✓ নিউমেরিক কলাম: মিডিয়ান দিয়ে ফিল করা হয়েছে")

# মিসিং ভ্যালু রিমুভড কিনা ভেরিফাই
print(f"মিসিং ভ্যালু অবশিষ্ট: {loan_data.isnull().sum().sum()}")

# ডেটা টাইপ চেক
print("\nডেটা টাইপ:");
print(loan_data.dtypes.value_counts())
```

### স্টেপ ৩: আউটলায়ার ডিটেকশন
```python
print("\n=== স্টেপ ৩: আউটলায়ার ডিটেকশন ও হ্যান্ডলিং ===")

numeric_features = ['বয়স', 'বার্ষিক_আয়', 'ক্রেডিট_স্কোর', 'লোন_পরিমাণ', 
                    'সুদের_হার', 'বর্তমান_ঋণ_অনুপাত', 'ইনকাম_টু_লোন_রেশিও']

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

outlier_counts = {}
for idx, col in enumerate(numeric_features):
    if idx >= len(axes):
        break
    
    # IQR পদ্ধতি
    Q1 = loan_data[col].quantile(0.25)
    Q3 = loan_data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = ((loan_data[col] < lower_bound) | (loan_data[col] > upper_bound)).sum()
    outlier_counts[col] = outliers
    
    # বক্সপ্লট
    axes[idx].boxplot(loan_data[col].dropna(), vert=True, patch_artist=True)
    axes[idx].set_title(f'{col}\n(আউটলায়ার: {outliers})', fontsize=10)
    axes[idx].set_ylabel('মান')

# খালি সাবপ্লট লুকানো
for i in range(len(numeric_features), len(axes)):
    axes[i].set_visible(False)

plt.suptitle('আউটলায়ার ডিটেকশন (IQR Method)', fontsize=14)
plt.tight_layout()
plt.savefig('capstone_outliers.png', dpi=100)
plt.show()

print("আউটলায়ার কাউন্ট (IQR পদ্ধতি):")
for col, count in outlier_counts.items():
    print(f"  {col}: {count} ({count/n_customers*100:.1f}%)")
```

### স্টেপ ৪: ডিপেন্ডেন্ট ভ্যারিয়েবল অ্যানালাইসিস
```python
print("\n=== স্টেপ ৪: লোন ডিফল্ট অ্যানালাইসিস ===")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# টার্গেট ডিস্ট্রিবিউশন
axes[0, 0].bar(['নন-ডিফল্ট (0)', 'ডিফল্ট (1)'], 
               [loan_data['লোন_ডিফল্ট'].value_counts().get(0, 0),
                loan_data['লোন_ডিফল্ট'].value_counts().get(1, 0)],
               color=['steelblue', 'coral'], edgecolor='black')
axes[0, 0].set_title('লোন ডিফল্ট ডিস্ট্রিবিউশন', fontsize=12)
axes[0, 0].set_ylabel('গ্রাহক সংখ্যা')

# ক্রেডিট স্কোর vs ডিফল্ট
axes[0, 1].boxplot([loan_data[loan_data['লোন_ডিফল্ট']==0]['ক্রেডিট_স্কোর'],
                    loan_data[loan_data['লোন_ডিফল্ট']==1]['ক্রেডিট_স্কোর']],
                   labels=['নন-ডিফল্ট', 'ডিফল্ট'])
axes[0, 1].set_title('ক্রেডিট স্কোর vs ডিফল্ট', fontsize=12)
axes[0, 1].set_ylabel('ক্রেডিট স্কোর')

# আয় vs ডিফল্ট
axes[0, 2].boxplot([loan_data[loan_data['লোন_ডিফল্ট']==0]['বার্ষিক_আয়'],
                    loan_data[loan_data['লোন_ডিফল্ট']==1]['বার্ষিক_আয়']],
                   labels=['নন-ডিফল্ট', 'ডিফল্ট'])
axes[0, 2].set_title('বার্ষিক আয় vs ডিফল্ট', fontsize=12)
axes[0, 2].set_ylabel('বার্ষিক আয় ($)')

# ঋণ অনুপাত vs ডিফল্ট
axes[1, 0].boxplot([loan_data[loan_data['লোন_ডিফল্ট']==0]['বর্তমান_ঋণ_অনুপাত'],
                    loan_data[loan_data['লোন_ডিফল্ট']==1]['বর্তমান_ঋণ_অনুপাত']],
                   labels=['নন-ডিফল্ট', 'ডিফল্ট'])
axes[1, 0].set_title('ঋণ অনুপাত vs ডিফল্ট', fontsize=12)
axes[1, 0].set_ylabel('বর্তমান ঋণ অনুপাত (%)')

# ইনকাম টু লোন রেশিও vs ডিফল্ট
axes[1, 1].boxplot([loan_data[loan_data['লোন_ডিফল্ট']==0]['ইনকাম_টু_লোন_রেশিও'],
                    loan_data[loan_data['লোন_ডিফল্ট']==1]['ইনকাম_টু_লোন_রেশিও']],
                   labels=['নন-ডিফল্ট', 'ডিফল্ট'])
axes[1, 1].set_title('আয়-থেকে-লোন অনুপাত vs ডিফল্ট', fontsize=12)
axes[1, 1].set_ylabel('Income/Loan Ratio')

# নিয়োগ স্থিতি vs ডিফল্ট
employment_default = loan_data.groupby('নিয়োগ_স্থিতি')['লোন_ডিফল্ট'].mean()
employment_default.plot(kind='bar', ax=axes[1, 2], color=['steelblue', 'coral', 'green'], edgecolor='black')
axes[1, 2].set_title('নিয়োগ স্থিতি অনুসারে ডিফল্ট রেট', fontsize=12)
axes[1, 2].set_ylabel('ডিফল্ট রেট')
axes[1, 2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('capstone_target_analysis.png', dpi=100)
plt.show()

print("লোন ডিফল্ট বিশ্লেষণ:")
default_rate = loan_data['লোন_ডিফল্ট'].mean()
print(f"সামগ্রিক ডিফল্ট রেট: {default_rate*100:.2f}%")

# উচ্চ-ঝুঁকির গ্রুপ সনাক্তকরণ
high_risk = loan_data[loan_data['ক্রেডিট_স্কোর'] < 600]
print(f"\nক্রেডিট স্কোর < 600 গ্রুপের ডিফল্ট রেট: {high_risk['লোন_ডিফল্ট'].mean()*100:.2f}%")

high_risk2 = loan_data[loan_data['বর্তমান_ঋণ_অনুপাত'] > 35]
print(f"ঋণ অনুপাত > 35% গ্রুপের ডিফল্ট রেট: {high_risk2['লোন_ডিফল্ট'].mean()*100:.2f}%")
```

### স্টেপ ৫: ফিচার ইঞ্জিনিয়ারিং
```python
print("\n=== স্টেপ ৫: ফিচার ইঞ্জিনিয়ারিং ===")

# নতুন ফিচার তৈরি
loan_data['ক্রেডিট_লেভেল'] = pd.cut(loan_data['ক্রেডিট_স্কোর'], 
    bins=[0, 580, 670, 740, 800, 850],
    labels=['খুব_খারাপ', 'খারাপ', 'ভাল', 'খুব_ভাল', 'চমৎকার'])

loan_data['ডিফল্ট_ইতিহাস'] = loan_data['পূর্ববর্তী_লোন_ডিফল্ট']
loan_data['উচ্চ_আয়_ফ্ল্যাগ'] = (loan_data['বার্ষিক_আয়'] > loan_data['বার্ষিক_আয়'].median()).astype(int)
loan_data['উচ্চ_লোন_ফ্ল্যাগ'] = (loan_data['লোন_পরিমাণ'] > loan_data['লোন_পরিমাণ'].median()).astype(int)

# বয়স গ্রুপ
loan_data['বয়স_গ্রুপ'] = pd.cut(loan_data['বয়স'], 
    bins=[0, 25, 35, 50, 65, 100],
    labels=['তরুণ', 'প্রারম্ভিক_প্রাপ্তবয়স্ক', 'মধ্যবয়সী', 'সিনিয়র', 'অবসর'])

# লোন পেমেন্ট প্রতি মাসে
loan_data['মাসিক_কিস্তি'] = loan_data.apply(
    lambda row: np.pmt(row['সুদের_হার']/100/12, row['লোন_মেয়াদ_মাস'], -row['লোন_পরিমাণ']), axis=1
)

# কিস্তি থেকে আয় অনুপাত
loan_data['কিস্তি_থেকে_আয়_অনুপাত'] = loan_data['মাসিক_কিস্তի'] / (loan_data['বার্ষিক_আয়'] / 12)

print("নতুন ফিচার তৈরি করা হয়েছে:")
new_features = ['ক্রেডিট_লেভেল', 'ডিফল্ট_ইতিহাস', 'উচ্চ_আয়_ফ্ল্যাগ', 'উচ্চ_লোন_ফ্ল্যাগ', 
                'বয়স_গ্রুপ', 'মাসিক_কিস্তি', 'কিস্তি_থেকে_আয়_অনুপাত']
for f in new_features:
    print(f"  ✓ {f}")

print("\nক্রেডিট লেভেল ডিস্ট্রিবিউশন:")
print(loan_data['ক্রেডিট_লেভেল'].value_counts())
```

### স্টেপ ৬: কোরিলেশন অ্যানালাইসিস
```python
print("\n=== স্টেপ ৬: কোরিলেশন অ্যানালাইসিস ===")

# এনকোডিং
le = LabelEncoder()
loan_data['লিঙ্গ_এনকোড'] = le.fit_transform(loan_data['লিঙ্গ'])
loan_data['নিয়োগ_এনকোড'] = le.fit_transform(loan_data['নিয়োগ_স্থিতি'])
loan_data['আবাসন_এনকোড'] = le.fit_transform(loan_data['আবাসন_স্থিতি'])
loan_data['বিবাহিত_এনকোড'] = le.fit_transform(loan_data['বিবাহিত'])

# নিউমেরিক ফিচার নির্বাচন
corr_features = ['বয়স', 'বার্ষিক_আয়', 'ক্রেডিট_স্কোর', 'লোন_পরিমাণ', 'লোন_মেয়াদ_মাস',
                 'সুদের_হার', 'বর্তমান_ঋণ_অনুপাত', 'ইনকাম_টু_লোন_রেশিও',
                 'পূর্ববর্তী_লোন_ডিফল্ট', 'নির্ভরশীল_সংখ্যা', 'মাসিক_খরচ',
                 'কিস্তি_থেকে_আয়_অনুপাত', 'লোন_ডিফল্ট']

corr_matrix = loan_data[corr_features].corr()

plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu', center=0, fmt='.2f',
            square=True, linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('ফিচার কোরিলেশন ম্যাট্রিক্স', fontsize=14)
plt.tight_layout()
plt.savefig('capstone_correlation.png', dpi=100)
plt.show()

# টার্গেটের সাথে কোরিলেশন
target_corr = corr_matrix['লোন_ডিফল্ট'].drop('লোন_ডিফল্ট').sort_values(ascending=False)
print("লোন ডিফল্টের সাথে সবচেয়ে বেশি সম্পর্কিত ফিচার:")
for feat, val in target_corr.items():
    print(f"  {feat}: {val:.4f}")
```

### স্টেপ ৭: ফিচার সিলেকশন
```python
print("\n=== স্টেপ ৭: ফিচার সিলেকশন ===")

# মডেলিং-এর জন্য ফিচার প্রস্তুত
model_features = ['বয়স', 'বার্ষিক_আয়', 'ক্রেডিট_স্কোর', 'লোন_পরিমাণ', 
                  'লোন_মেয়াদ_মাস', 'সুদের_হার', 'বর্তমান_ঋণ_অনুপাত', 
                  'ইনকাম_টু_লোন_রেশিও', 'পূর্ববর্তী_লোন_ডিফল্ট',
                  'নির্ভরশীল_সংখ্যা', 'মাসিক_খরচ', 'লিঙ্গ_এনকোড',
                  'নিয়োগ_এনকোড', 'আবাসন_এনকোড', 'বিবাহিত_এনকোড',
                  'কিস্তি_থেকে_আয়_অনুপাত', 'উচ্চ_আয়_ফ্ল্যাগ', 'উচ্চ_লোন_ফ্ল্যাগ']

X = loan_data[model_features]
y = loan_data['লোন_ডিফল্ট']

# মিউচুয়াল ইনফরমেশন ফিচার সিলেকশন
selector = SelectKBest(score_func=mutual_info_classif, k=10)
X_selected = selector.fit_transform(X.fillna(0), y)
selected_indices = selector.get_support(indices=True)
selected_features = [model_features[i] for i in selected_indices]

print("শীর্ষ ১০ ফিচার (Mutual Information):")
for i, feat in enumerate(selected_features, 1):
    print(f"  {i}. {feat}")

# ANOVA F-test
f_selector = SelectKBest(score_func=f_classif, k=10)
f_selector.fit(X.fillna(0), y)
f_scores = pd.DataFrame({
    'ফিচার': model_features,
    'F-স্কোর': f_selector.scores_
}).sort_values('F-স্কোর', ascending=False)

print("\nANOVA F-স্কোর দ্বারা ফিচার র‍্যাঙ্কিং:")
print(f_scores.head(10))
```

### স্টেপ ৮: ট্রেন-টেস্ট স্প্লিট
```python
print("\n=== স্টেপ ৮: ট্রেন-টেস্ট স্প্লিট ===")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"ট্রেনিং সেট: {X_train.shape[0]} নমুনা")
print(f"টেস্ট সেট: {X_test.shape[0]} নমুনা")
print(f"\nট্রেনিং ডিফল্ট রেট: {y_train.mean()*100:.2f}%")
print(f"টেস্ট ডিফল্ট রেট: {y_test.mean()*100:.2f}%")

# স্কেলিং
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ডেটা সেভ করা (পার্ট ২-এর জন্য)
import joblib
joblib.dump((X_train_scaled, X_test_scaled, y_train, y_test, scaler), 
            'capstone_loan_data.pkl')
print("\n✅ প্রসেসড ডেটা 'capstone_loan_data.pkl' ফাইলে সেভ করা হয়েছে")
print("✅ পার্ট ২ (Day 30)-এ এই ডেটা লোড করে মডেলিং করব!")
```

### ইনসাইট রিপোর্ট
```python
print("\n=== পার্ট ১ ইনসাইট রিপোর্ট ===")

insights = """
## 🔍 ডেটা অ্যানালাইসিস থেকে মূল অন্তর্দৃষ্টি

### ১. ডেটা কোয়ালিটি
• ৩% মিসিং ভ্যালু — মিডিয়ান ইম্পুটেশন করা হয়েছে
• আউটলায়ার IQR পদ্ধতিতে সনাক্ত — লোনের পরিমাণে সবচেয়ে বেশি আউটলায়ার
• কোন ডুপ্লিকেট রেকর্ড নেই

### ২. ডিফল্টের মূল ড্রাইভার
🏆 **ক্রেডিট স্কোর** — সবচেয়ে শক্তিশালী প্রেডিক্টর
🏆 **বর্তমান ঋণ অনুপাত** — দ্বিতীয় গুরুত্বপূর্ণ ফ্যাক্টর
🏆 **পূর্ববর্তী ডিফল্ট** — অতীত আচরণ ভবিষ্যতের ইঙ্গিত দেয়

### ৩. উচ্চ-ঝুঁকির গ্রাহক প্রোফাইল
⚠️ ক্রেডিট স্কোর < 600
⚠️ ঋণ অনুপাত > 35%
⚠️ বেকার অবস্থা
⚠️ কম ইনকাম-টু-লোন রেশিও (< 0.5)
⚠️ পূর্ববর্তী লোন ডিফল্টের ইতিহাস

### ৪. নতুন ফিচার থেকে লার্নিং
• কিস্তি-থেকে-আয় অনুপাত ডিফল্টের শক্তিশালী ইন্ডিকেটর
• ক্রেডিট লেভেল ক্যাটেগরি বিভিন্ন গ্রুপের ঝুঁকি বুঝতে সাহায্য করে
• আয় ও লোন ফ্ল্যাগ ডিফল্ট রিস্ক অ্যাসেসমেন্টে সহায়ক
"""
print(insights)
```

### পার্ট ১ সারসংক্ষেপ
```python
print("\n" + "=" * 60)
print("ক্যাপস্টোন পার্ট ১ — সারসংক্ষেপ")
print("=" * 60)

summary = """
## পার্ট ১-এ যা করলাম:

✅ সম্পূর্ণ ডেটা প্রিপারেশন পাইপলাইন:
   1. রিয়েলিস্টিক ব্যাংকিং ডেটাসেট তৈরি
   2. মিসিং ভ্যালু হ্যান্ডলিং (SimpleImputer)
   3. আউটলায়ার ডিটেকশন (Boxplot + IQR)
   4. বিস্তারিত EDA ও টার্গেট অ্যানালাইসিস
   5. ফিচার ইঞ্জিনিয়ারিং (৭টি নতুন ফিচার)
   6. কোরিলেশন অ্যানালাইসিস (Heatmap)
   7. ফিচার সিলেকশন (Mutual Information, ANOVA)
   8. স্ট্র্যাটিফাইড ট্রেন-টেস্ট স্প্লিট
   9. স্কেলিং (StandardScaler)
   10. ডেটা সেভ (পার্ট ২-এর জন্য)

## পার্ট ২ (Day 30)-এ কী হবে:
🔜 একাধিক ML মডেল ট্রেনিং
🔜 হাইপারপ্যারামিটার অপ্টিমাইজেশন
🔜 মডেল ইভালুয়েশন ও তুলনা
🔜 ফিচার ইম্পরট্যান্স অ্যানালাইসিস
🔜 চূড়ান্ত সুপারিশ ও রিপোর্ট
"""
print(summary)
```