# Day 13: স্যাম্পলিং টেকনিক
## Sampling Techniques

### স্যাম্পলিং কী?
পপুলেশন থেকে একটি প্রতিনিধিত্বমূলক সাবসেট (স্যাম্পল) নির্বাচনের প্রক্রিয়াকে স্যাম্পলিং বলে। ভালো স্যাম্পলিং নিশ্চিত করে যে আমাদের বিশ্লেষণ ও মডেল পুরো পপুলেশনের জন্য সঠিক হবে।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import random
import warnings
warnings.filterwarnings('ignore')

# বড় পপুলেশন তৈরি (১০০,০০০ রেকর্ড)
np.random.seed(42)
population_size = 100000
population = pd.DataFrame({
    'আইডি': range(1, population_size + 1),
    'বয়স': np.random.normal(35, 12, population_size).astype(int),
    'আয়': np.random.lognormal(10.5, 0.5, population_size).astype(int),
    'শিক্ষাবর্ষ': np.random.poisson(12, population_size),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট'], population_size),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা'], population_size)
})

print("=== পপুলেশন ডেটা ===")
print(f"পপুলেশন সাইজ: {len(population):,}")
print(f"গড় বয়স: {population['বয়স'].mean():.2f}")
print(f"গড় আয়: {population['আয়'].mean():.2f}")
print(f"গড় শিক্ষাবর্ষ: {population['শিক্ষাবর্ষ'].mean():.2f}")
```

### স্যাম্পলিং টেকনিকসমূহ:

#### ১. সিম্পল র্যান্ডম স্যাম্পলিং (SRS):
```python
print("\n=== সিম্পল র্যান্ডম স্যাম্পলিং ===")

sample_size = 1000
srs_sample = population.sample(n=sample_size, random_state=42)

print(f"SRS স্যাম্পল সাইজ: {len(srs_sample)}")
print(f"SRS গড় বয়স: {srs_sample['বয়স'].mean():.2f} (পপুলেশন: {population['বয়স'].mean():.2f})")
print(f"SRS গড় আয়: {srs_sample['আয়'].mean():.2f} (পপুলেশন: {population['আয়'].mean():.2f})")

# মাল্টিপল স্যাম্পল নিয়ে ভ্যারিয়েশন দেখা
means = []
for _ in range(1000):
    s = population.sample(n=100)
    means.append(s['বয়স'].mean())

print(f"\n১০০০ বার ১০০ সাইজের স্যাম্পলের গড় বয়সের ডিস্ট্রিবিউশন:")
print(f"  মিন: {np.mean(means):.2f}")
print(f"  স্টিড: {np.std(means):.2f}")
print(f"  পপুলেশন মিন: {population['বয়স'].mean():.2f}")

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(means, bins=30, edgecolor='black', alpha=0.7)
plt.axvline(population['বয়স'].mean(), color='r', linestyle='--', label='পপুলেশন মিন')
plt.xlabel('স্যাম্পলের গড় বয়স')
plt.ylabel('ফ্রিকোয়েন্সি')
plt.title('স্যাম্পলিং ডিস্ট্রিবিউশন (বয়স)')
plt.legend()
```

#### ২. স্ট্র্যাটিফাইড স্যাম্পলিং:
```python
print("\n=== স্ট্র্যাটিফাইড স্যাম্পলিং ===")

# শহর অনুযায়ী স্ট্র্যাটিফাইড স্যাম্পলিং
stratified_sample = population.groupby('শহר', group_keys=False).apply(
    lambda x: x.sample(frac=0.01, random_state=42)
)

print(f"স্ট্র্যাটিফাইড স্যাম্পল সাইজ: {len(stratified_sample)}")
print(f"\nশহর অনুযায়ী ডিস্ট্রিবিউশন:")
print("পপুলেশন:")
print(population['শহর'].value_counts(normalize=True).sort_index())
print("\nস্ট্র্যাটিফাইড স্যাম্পল:")
print(stratified_sample['শহর'].value_counts(normalize=True).sort_index())

# বয়স গ্রুপ অনুযায়ী স্ট্র্যাটিফিকেশন
population['বয়স_গ্রুপ'] = pd.cut(population['বয়স'], bins=[0, 20, 30, 40, 50, 100], 
                                    labels=['<20', '20-30', '30-40', '40-50', '50+'])

stratified_age = population.groupby('বয়স_গ্রুপ', group_keys=False).apply(
    lambda x: x.sample(frac=0.01, random_state=42)
)

print(f"\nবয়স গ্রুপ অনুযায়ী ডিস্ট্রিবিউশন:")
print("পপুলেশন:")
print(population['বয়স_গ্রুপ'].value_counts(normalize=True).sort_index())
print("\nস্ট্র্যাটিফাইড স্যাম্পল:")
print(stratified_age['বয়স_গ্রুপ'].value_counts(normalize=True).sort_index())
```

#### ৩. ক্লাস্টার স্যাম্পলিং:
```python
print("\n=== ক্লাস্টার স্যাম্পলিং ===")

# শহরগুলোকে ক্লাস্টার হিসেবে ব্যবহার
city_clusters = population.groupby('শহর')
cities = list(population['শহর'].unique())
selected_cities = random.sample(cities, 2)  # ২টি শহর নির্বাচন

cluster_sample = population[population['শহর'].isin(selected_cities)]
print(f"নির্বাচিত শহর: {selected_cities}")
print(f"ক্লাস্টার স্যাম্পল সাইজ: {len(cluster_sample)}")
print(f"ক্লাস্টার স্যাম্পল গড় বয়স: {cluster_sample['বয়স'].mean():.2f}")
print(f"পপুলেশন গড় বয়স: {population['বয়স'].mean():.2f}")

# এলোমেলোভাবে ক্লাস্টার নির্বাচন
all_cluster_means = []
for _ in range(100):
    sel_cities = random.sample(cities, 2)
    samp = population[population['শহর'].isin(sel_cities)]
    all_cluster_means.append(samp['বয়স'].mean())

print(f"\nক্লাস্টার স্যাম্পলিং (২ শহর) গড় বয়সের মিন: {np.mean(all_cluster_means):.2f}")
print(f"ক্লাস্টার স্যাম্পলিং গড় বয়সের স্টিড: {np.std(all_cluster_means):.2f}")
```

#### ৪. সিস্টেমেটিক স্যাম্পলিং:
```python
print("\n=== সিস্টেমেটিক স্যাম্পলিং ===")

def systematic_sample(df, sample_size):
    """সিস্টেমেটিক স্যাম্পলিং ফাংশন"""
    n = len(df)
    k = n // sample_size  # ইন্টারভ্যাল
    start = random.randint(0, k - 1)  # র্যান্ডম স্টার্ট
    indices = list(range(start, n, k))
    return df.iloc[indices]

sys_sample = systematic_sample(population, 1000)
print(f"ইন্টারভ্যাল (k): {len(population) // 1000}")
print(f"সিস্টেমেটিক স্যাম্পল সাইজ: {len(sys_sample)}")
print(f"সিস্টেমেটিক স্যাম্পল গড় বয়স: {sys_sample['বয়স'].mean():.2f}")
print(f"সিস্টেমেটিক স্যাম্পল গড় আয়: {sys_sample['আয়'].mean():.2f}")
```

#### ৫. কনভিনিয়েন্স স্যাম্পলিং:
```python
print("\n=== কনভিনিয়েন্স স্যাম্পলিং ===")

# প্রথম ১০০০ রেকর্ড নেওয়া (সহজলভ্য ডেটা)
conv_sample = population.head(1000)
print(f"কনভিনিয়েন্স স্যাম্পল সাইজ: {len(conv_sample)}")
print(f"কনভিনিয়েন্স স্যাম্পল গড় বয়স: {conv_sample['বয়স'].mean():.2f}")
print(f"পপুলেশন গড় বয়স: {population['বয়স'].mean():.2f}")
print(f"বায়াস: {conv_sample['বয়স'].mean() - population['বয়স'].mean():.2f}")
```

#### ৬. স্যাম্পল সাইজ নির্ধারণ:
```python
print("\n=== স্যাম্পল সাইজ নির্ধারণ ===")

from scipy import stats as scipy_stats

def required_sample_size(population_size, confidence_level, margin_error, p=0.5):
    """
    প্রয়োজনীয় স্যাম্পল সাইজ গণনা
    population_size: পপুলেশন সাইজ
    confidence_level: কনফিডেন্স লেভেল (0.95, 0.99)
    margin_error: মার্জিন অফ এরর (0.05 = 5%)
    p: প্রপোরশন (ডিফল্ট 0.5 = ম্যাক্সিমাম ভ্যারিয়েন্স)
    """
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores[confidence_level]
    
    # কোক্রান ফর্মুলা
    n0 = (z**2 * p * (1-p)) / (margin_error**2)
    n = n0 / (1 + (n0 - 1) / population_size)
    return int(np.ceil(n))

# বিভিন্ন প্যারামিটারের জন্য স্যাম্পল সাইজ
print("বিভিন্ন কনফিডেন্স লেভেলে প্রয়োজনীয় স্যাম্পল সাইজ:")
for cl in [0.90, 0.95, 0.99]:
    for me in [0.03, 0.05, 0.10]:
        n = required_sample_size(population_size, cl, me)
        print(f"  কনফিডেন্স {cl*100:.0f}%, মার্জিন {me*100:.0f}% → স্যাম্পল সাইজ: {n:,}")

print(f"\nপপুলেশন: {population_size:,}")
print(f"৫% মার্জিন, ৯৫% কনফিডেন্সের জন্য স্যাম্পল: {required_sample_size(population_size, 0.95, 0.05):,}")
```

### স্যাম্পলিং বায়াস:
```python
print("\n=== স্যাম্পলিং বায়াস ===")

# আয়ের ভিত্তিতে বায়াস চেক
true_mean_income = population['আয়'].mean()

# SRS এর ত্রুটি
srs_means = [population.sample(500)['আয়'].mean() for _ in range(100)]
srs_error = np.mean([abs(m - true_mean_income) for m in srs_means])

# কনভিনিয়েন্স স্যাম্পলের ত্রুটি
conv_means = [population.head(500)['আয়'].mean() for _ in range(100)]
conv_error = np.mean([abs(m - true_mean_income) for m in conv_means])

print(f"সত্যিকারের গড় আয়: {true_mean_income:.2f}")
print(f"SRS গড় ত্রুটি: {srs_error:.2f}")
print(f"কনভিনিয়েন্স স্যাম্পল গড় ত্রুটি: {conv_error:.2f}")

plt.subplot(1, 2, 2)
plt.boxplot([srs_means, conv_means], labels=['SRS', 'কনভিনিয়েন্স'])
plt.axhline(true_mean_income, color='r', linestyle='--', label='পপুলেশন মিন')
plt.ylabel('গড় আয়')
plt.title('স্যাম্পলিং মেথড কানেকশন')
plt.legend()
plt.tight_layout()
plt.savefig('sampling_comparison.png')
plt.show()
print("গ্রাফ সেভ করা হয়েছে!")
```

### ট্রেন-টেস্ট স্প্লিট (স্যাম্পলিং এর প্রয়োগ):
```python
print("\n=== ট্রেন-টেস্ট স্প্লিট ===")

# সিম্পল র্যান্ডম স্প্লিট
X = population.drop('আয়', axis=1)
y = population['আয়']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"ট্রেন সেট: {len(X_train):,}")
print(f"টেস্ট সেট: {len(X_test):,}")
print(f"ট্রেন গড় আয়: {y_train.mean():.2f}")
print(f"টেস্ট গড় আয়: {y_test.mean():.2f}")

# স্ট্র্যাটিফাইড স্প্লিট
X_train_strat, X_test_strat, y_train_strat, y_test_strat = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=population['শহর']
)

print(f"\nস্ট্র্যাটিফাইড স্প্লিট:")
print("ট্রেনে শহর ডিস্ট্রিবিউশন:")
print(X_train_strat['শহর'].value_counts(normalize=True).sort_index())
print("টেস্টে শহর ডিস্ট্রিবিউশন:")
print(X_test_strat['শহর'].value_counts(normalize=True).sort_index())
```

### কেন ভালো স্যাম্পলিং জরুরি:
```python
print("\n=== ভালো স্যাম্পলিং এর গুরুত্ব ===")

# বিভিন্ন স্যাম্পল সাইজের নির্ভুলতা
sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000]
accuracies = []
true_mean = population['বয়স'].mean()

for size in sample_sizes:
    errors = []
    for _ in range(500):
        sample = population.sample(size)
        errors.append(abs(sample['বয়স'].mean() - true_mean))
    accuracies.append(np.mean(errors))

results = pd.DataFrame({
    'স্যাম্পল_সাইজ': sample_sizes,
    'গড়_ত্রুটি': accuracies
})
print("স্যাম্পল সাইজ বাড়ার সাথে সাথে ত্রুটি কমে:")
print(results.to_string(index=False))
```

### সারাংশ:
- **সিম্পল র্যান্ডম**: সবচেয়ে সহজ ও নিরপেক্ষ
- **স্ট্র্যাটিফাইড**: গ্রুপভিত্তিক প্রতিনিধিত্ব নিশ্চিত করে
- **ক্লাস্টার**: খরচ কম, কিন্তু ভ্যারিয়েন্স বেশি
- **সিস্টেমেটিক**: সহজ বাস্তবায়ন, কিন্তু পিরিয়ডিসিটি থাকলে সমস্যা
- **কনভিনিয়েন্স**: সহজলভ্য, কিন্তু বায়াসড
- ভালো স্যাম্পলিং মডেলের জেনারেলাইজেশন ক্ষমতা বাড়ায়
- স্যাম্পল সাইজ নির্ধারণে কনফিডেন্স ও মার্জিন অব এরর বিবেচনা করুন
