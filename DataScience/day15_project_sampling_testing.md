# Day 15: মিনি প্রজেক্ট - স্যাম্পলিং ও হাইপোথিসিস টেস্টিং
## Mini Project: Sampling & Hypothesis Testing

### প্রজেক্ট ওভারভিউ:
এই প্রজেক্টে আমরা একটি ই-কমার্স কোম্পানির ডেটা নিয়ে স্যাম্পলিং টেকনিক ও হাইপোথিসিস টেস্টিং প্রয়োগ করব।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, chi2_contingency, f_oneway
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# সীড সেট করা
np.random.seed(42)

print("=" * 60)
print("প্রজেক্ট: ই-কমার্স ডেটা অ্যানালাইসিস")
print("=" * 60)
```

### স্টেপ ১: ডেটাসেট তৈরি
```python
print("\n=== স্টেপ ১: ডেটাসেট তৈরি ===")

n_customers = 10000

# কাস্টমার ডেটা
customers = pd.DataFrame({
    'কাস্টমার_আইডি': range(1, n_customers + 1),
    'বয়স': np.random.randint(18, 70, n_customers),
    'লিঙ্গ': np.random.choice(['পুরুষ', 'মহিলা', 'অন্যান্য'], n_customers, p=[0.48, 0.48, 0.04]),
    'শহর': np.random.choice(['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট', 'বরিশাল'], n_customers),
    'মাসিক_আয়': np.random.lognormal(10.8, 0.6, n_customers).astype(int),
    'সাইট_ভিজিট': np.random.poisson(8, n_customers),
    'কার্টে_যোগ': np.random.poisson(3, n_customers),
    'পূর্ববর্তী_ক্রয়': np.random.poisson(2, n_customers),
    'সদস্যপদ': np.random.choice(['বেসিক', 'স্ট্যান্ডার্ড', 'প্রিমিয়াম'], n_customers, p=[0.5, 0.3, 0.2])
})

# কিছু লজিকাল সম্পর্ক যোগ করা
customers['কার্টে_যোগ'] = np.minimum(customers['কার্টে_যোগ'], customers['সাইট_ভিজিট'])
customers['পূর্ববর্তী_ক্রয়'] = np.minimum(customers['পূর্ববর্তী_ক্রয়'], customers['কার্টে_যোগ'])

# ক্রয়_সম্ভাবনা (টার্গেট ভ্যারিয়েবল)
purchase_prob = 0.1 + 0.3 * (customers['সদস্যপদ'] == 'প্রিমিয়াম') + \
                0.1 * (customers['পূর্ববর্তী_ক্রয়'] > 2) + \
                0.1 * (customers['সাইট_ভিজিট'] > 10)
purchase_prob = np.clip(purchase_prob, 0, 1)
customers['ক্রয়_করেছে'] = np.random.binomial(1, purchase_prob)

# ক্রয়ের পরিমাণ
customers['ক্রয়_পরিমাণ'] = 0
mask = customers['ক্রয়_করেছে'] == 1
customers.loc[mask, 'ক্রয়_পরিমাণ'] = np.random.lognormal(8, 0.8, mask.sum()).astype(int)

print(f"মোট কাস্টমার: {len(customers):,}")
print(f"ক্রয় করেছে: {customers['ক্রয়_করেছে'].sum():,} ({customers['ক্রয়_করেছে'].mean()*100:.2f}%)")
print(f"গড় ক্রয় পরিমাণ: {customers[customers['ক্রয়_করেছে']==1]['ক্রয়_পরিমাণ'].mean():.2f} টাকা")
print("\nপ্রথম ১০ কাস্টমার:")
print(customers.head(10))
```

### স্টেপ ২: ডেটা এক্সপ্লোরেশন
```python
print("\n=== স্টেপ ২: ডেটা এক্সপ্লোরেশন ===")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# বয়স ডিস্ট্রিবিউশন
axes[0,0].hist(customers['বয়স'], bins=20, edgecolor='black', alpha=0.7)
axes[0,0].set_title('বয়স ডিস্ট্রিবিউশন')
axes[0,0].set_xlabel('বয়স')
axes[0,0].set_ylabel('ফ্রিকোয়েন্সি')

# সদস্যপদ বিতরণ
customers['সদস্যপদ'].value_counts().plot(kind='bar', ax=axes[0,1], edgecolor='black')
axes[0,1].set_title('সদস্যপদ বিতরণ')
axes[0,1].set_xlabel('সদস্যপদ')
axes[0,1].set_ylabel('সংখ্যা')

# শহর ভিত্তিক ক্রয় রেট
city_purchase = customers.groupby('শহর')['ক্রয়_করেছে'].mean().sort_values()
city_purchase.plot(kind='bar', ax=axes[0,2], edgecolor='black', color='green')
axes[0,2].set_title('শহর ভিত্তিক ক্রয় রেট')
axes[0,2].set_xlabel('শহর')
axes[0,2].set_ylabel('ক্রয় রেট')

# বয়স বনাম ক্রয়
axes[1,0].scatter(customers['বয়স'], customers['ক্রয়_পরিমাণ'], alpha=0.3)
axes[1,0].set_title('বয়স বনাম ক্রয় পরিমাণ')
axes[1,0].set_xlabel('বয়স')
axes[1,0].set_ylabel('ক্রয় পরিমাণ')

# সাইট ভিজিট বনাম ক্রয়
axes[1,1].scatter(customers['সাইট_ভিজিট'], customers['ক্রয়_পরিমাণ'], alpha=0.3)
axes[1,1].set_title('সাইট ভিজিট বনাম ক্রয় পরিমাণ')
axes[1,1].set_xlabel('সাইট ভিজিট')
axes[1,1].set_ylabel('ক্রয় পরিমাণ')

# সদস্যপদ ভিত্তিক গড় ক্রয়
membership_purchase = customers[customers['ক্রয়_করেছে']==1].groupby('সদস্যপদ')['ক্রয়_পরিমাণ'].mean()
membership_purchase.plot(kind='bar', ax=axes[1,2], edgecolor='black', color='orange')
axes[1,2].set_title('সদস্যপদ ভিত্তিক গড় ক্রয়')
axes[1,2].set_xlabel('সদস্যপদ')
axes[1,2].set_ylabel('গড় ক্রয় পরিমাণ')

plt.tight_layout()
plt.savefig('project_exploration.png')
plt.show()
print("এক্সপ্লোরেশন গ্রাফ সেভ করা হয়েছে!")

# সারসংখ্যা
print("\n=== শহর ভিত্তিক ক্রয় বিশ্লেষণ ===")
print(customers.groupby('শহর').agg({
    'ক্রয়_করেছে': ['mean', 'sum', 'count'],
    'ক্রয়_পরিমাণ': ['mean', 'median', 'sum']
}).round(2))
```

### স্টেপ ৩: স্যাম্পলিং টেকনিক প্রয়োগ
```python
print("\n=== স্টেপ ৩: স্যাম্পলিং টেকনিক ===")

# ৩.১ সিম্পল র্যান্ডম স্যাম্পলিং
sample_srs = customers.sample(n=500, random_state=42)
print(f"৩.১ SRS স্যাম্পল:")
print(f"  সাইজ: {len(sample_srs)}")
print(f"  ক্রয় রেট: {sample_srs['ক্রয়_করেছে'].mean()*100:.2f}% (পপুলেশন: {customers['ক্রয়_করেছে'].mean()*100:.2f}%)")
print(f"  গড় বয়স: {sample_srs['বয়স'].mean():.1f} (পপুলেশন: {customers['বয়স'].mean():.1f})")

# ৩.২ স্ট্র্যাটিফাইড স্যাম্পলিং (শহর অনুযায়ী)
stratified = customers.groupby('শহর', group_keys=False).apply(
    lambda x: x.sample(frac=0.05, random_state=42)
)
print(f"\n৩.২ স্ট্র্যাটিফাইড স্যাম্পল:")
print(f"  সাইজ: {len(stratified)}")
print(f"  ক্রয় রেট: {stratified['ক্রয়_করেছে'].mean()*100:.2f}%")
print(f"  শহর বিতরণ:")
print(f"    পপুলেশন: {customers['শহর'].value_counts(normalize=True).sort_index().round(3).to_dict()}")
print(f"    স্যাম্পল: {stratified['শহর'].value_counts(normalize=True).sort_index().round(3).to_dict()}")

# ৩.৩ সিস্টেমেটিক স্যাম্পলিং
k = len(customers) // 500
start = np.random.randint(0, k)
systematic = customers.iloc[start::k].head(500)
print(f"\n৩.৩ সিস্টেমেটিক স্যাম্পল (k={k}):")
print(f"  সাইজ: {len(systematic)}")
print(f"  ক্রয় রেট: {systematic['ক্রয়_করেছে'].mean()*100:.2f}%")

# বিভিন্ন স্যাম্পলিং মেথডের তুলনা
print("\n=== স্যাম্পলিং মেথড তুলনা ===")
true_rate = customers['ক্রয়_করেছে'].mean()
methods = []
errors = []

for _ in range(100):
    srs = customers.sample(500)
    methods.append('SRS')
    errors.append(abs(srs['ক্রয়_করেছে'].mean() - true_rate))
    
    start = np.random.randint(0, k)
    sys = customers.iloc[start::k].head(500)
    methods.append('সিস্টেমেটিক')
    errors.append(abs(sys['ক্রয়_করেছে'].mean() - true_rate))

comparison = pd.DataFrame({'মেথড': methods, 'এবসোলিউট এরর': errors})
print(comparison.groupby('মেথড')['এবসোলিউট এরর'].agg(['mean', 'std']).round(4))
```

### স্টেপ ৪: হাইপোথিসিস টেস্টিং
```python
print("\n=== স্টেপ ৪: হাইপোথিসিস টেস্টিং ===")
alpha = 0.05

# ৪.১ প্রিমিয়াম vs বেসিক সদস্যদের ক্রয় রেট তুলনা
premium = customers[customers['সদস্যপদ'] == 'প্রিমিয়াম']['ক্রয়_করেছে']
basic = customers[customers['সদস্যপদ'] == 'বেসিক']['ক্রয়_করেছে']

t_stat, p_val = ttest_ind(premium, basic)
print(f"৪.১ প্রিমিয়াম vs বেসিক ক্রয় রেট:")
print(f"  প্রিমিয়াম ক্রয় রেট: {premium.mean()*100:.2f}%")
print(f"  বেসিক ক্রয় রেট: {basic.mean()*100:.2f}%")
print(f"  টি-স্ট্যাট: {t_stat:.4f}, পি-ভ্যালু: {p_val:.6f}")
print(f"  {'=> উল্লেখযোগ্য পার্থক্য আছে!' if p_val < alpha else '=> উল্লেখযোগ্য পার্থক্য নেই।'}")

# ৪.২ পুরুষ vs মহিলা ক্রয় পরিমাণের তুলনা
male_purchase = customers[(customers['লিঙ্গ'] == 'পুরুষ') & (customers['ক্রয়_করেছে'] == 1)]['ক্রয়_পরিমাণ']
female_purchase = customers[(customers['লিঙ্গ'] == 'মহিলা') & (customers['ক্রয়_করেছে'] == 1)]['ক্রয়_পরিমাণ']

if len(male_purchase) > 0 and len(female_purchase) > 0:
    t_stat2, p_val2 = ttest_ind(male_purchase, female_purchase)
    print(f"\n৪.২ পুরুষ vs মহিলা ক্রয় পরিমাণ:")
    print(f"  পুরুষ: নমুনা={len(male_purchase)}, গড়={male_purchase.mean():.2f}")
    print(f"  মহিলা: নমুনা={len(female_purchase)}, গড়={female_purchase.mean():.2f}")
    print(f"  টি-স্ট্যাট: {t_stat2:.4f}, পি-ভ্যালু: {p_val2:.6f}")
    print(f"  {'=> উল্লেখযোগ্য পার্থক্য আছে!' if p_val2 < alpha else '=> উল্লেখযোগ্য পার্থক্য নেই।'}")

# ৪.৩ ANOVA: তিন সদস্যপদ শ্রেণীর ক্রয় পরিমাণ তুলনা (শুধু যারা কিনেছে)
purchase_data = customers[customers['ক্রয়_করেছে'] == 1]
groups = [purchase_data[purchase_data['সদস্যপদ'] == level]['ক্রয়_পরিমাণ'] 
          for level in ['বেসিক', 'স্ট্যান্ডার্ড', 'প্রিমিয়াম']]

f_stat, p_val3 = f_oneway(*groups)
print(f"\n৪.৩ ANOVA - সদস্যপদ অনুযায়ী ক্রয় পরিমাণ:")
for i, level in enumerate(['বেসিক', 'স্ট্যান্ডার্ড', 'প্রিমিয়াম']):
    print(f"  {level}: মিন={groups[i].mean():.2f}, স্টিড={groups[i].std():.2f}, N={len(groups[i])}")
print(f"  এফ-স্ট্যাট: {f_stat:.4f}, পি-ভ্যালু: {p_val3:.6f}")
print(f"  {'=> অন্তত এক জোড়া গ্রুপের মধ্যে পার্থক্য আছে!' if p_val3 < alpha else '=> কোনো পার্থক্য নেই।'}")

# ৪.৪ চি-স্কোয়ার: লিঙ্গ ও ক্রয়ের মধ্যে সম্পর্ক
contingency = pd.crosstab(customers['লিঙ্গ'], customers['ক্রয়_করেছে'])
chi2, p_chi, dof, expected = chi2_contingency(contingency)
print(f"\n৪.৪ চি-স্কোয়ার - লিঙ্গ ও ক্রয়ের সম্পর্ক:")
print(f"  টেবিল:\n{contingency}")
print(f"  চি-স্কোয়ার: {chi2:.4f}, পি-ভ্যালু: {p_chi:.6f}")
print(f"  {'=> লিঙ্গ ও ক্রয়ের মধ্যে সম্পর্ক আছে!' if p_chi < alpha else '=> কোনো সম্পর্ক নেই।'}")
```

### স্টেপ ৫: A/B টেস্টিং সিমুলেশন
```python
print("\n=== স্টেপ ৫: A/B টেস্টিং সিমুলেশন ===")

# নতুন ফিচার: "২৪ ঘণ্টা ডেলিভারি" ব্যাজ
# H₀: ব্যাজ দেখলে ক্রয় রেট পরিবর্তন হয় না
# H₁: ব্যাজ দেখলে ক্রয় রেট বাড়ে

n_test = 5000
control_cvr = 0.08  # কন্ট্রোল গ্রুপের কনভার্সন (৮%)
treatment_cvr = 0.095  # ট্রিটমেন্ট গ্রুপের কনভার্সন (৯.৫%)

control_group = np.random.binomial(1, control_cvr, n_test)
treatment_group = np.random.binomial(1, treatment_cvr, n_test)

# প্রপোরশন জেড-টেস্ট
from statsmodels.stats.proportion import proportions_ztest
counts = np.array([treatment_group.sum(), control_group.sum()])
nobs = np.array([n_test, n_test])
z_stat_ab, p_ab = proportions_ztest(counts, nobs)

print(f"A/B টেস্ট রেজাল্ট:")
print(f"  কন্ট্রোল CVR: {control_group.mean()*100:.2f}%")
print(f"  ট্রিটমেন্ট CVR: {treatment_group.mean()*100:.2f}%")
print(f"  লিফট: {(treatment_group.mean()/control_group.mean()-1)*100:.2f}%")
print(f"  জেড-স্ট্যাট: {z_stat_ab:.4f}")
print(f"  পি-ভ্যালু: {p_ab:.6f}")
print(f"  {'=> নতুন ফিচার স্ট্যাটিস্টিকালি সিগনিফিকেন্ট!' if p_ab < alpha else '=> নতুন ফিচার স্ট্যাটিস্টিকালি সিগনিফিকেন্ট নয়।'}")

# কনফিডেন্স ইন্টারভ্যাল
from statsmodels.stats.proportion import proportion_confint
ci_control = proportion_confint(control_group.sum(), n_test, alpha=0.05)
ci_treatment = proportion_confint(treatment_group.sum(), n_test, alpha=0.05)
print(f"\n  ৯৫% CI - কন্ট্রোল: ({ci_control[0]*100:.2f}%, {ci_control[1]*100:.2f}%)")
print(f"  ৯৫% CI - ট্রিটমেন্ট: ({ci_treatment[0]*100:.2f}%, {ci_treatment[1]*100:.2f}%)")
```

### স্টেপ ৬: উপসংহার ও রিপোর্ট
```python
print("\n=== স্টেপ ৬: উপসংহার ===")

print("""
প্রজেক্ট সফলভাবে সম্পন্ন! নিচে মূল ফলাফলসমূহ:

১. ডেটা এক্সপ্লোরেশন:
   - {} কাস্টমারের ডেটা বিশ্লেষণ করা হয়েছে
   - {}% কাস্টমার ক্রয় সম্পন্ন করেছেন
   
২. স্যাম্পলিং তুলনা:
   - SRS ও স্ট্র্যাটিফাইড স্যাম্পলিং পপুলেশনের কাছাকাছি ফল দেয়
   - কনভিনিয়েন্স স্যাম্পলিং বায়াসড হতে পারে

৩. হাইপোথিসিস টেস্ট ফলাফল:
   - প্রিমিয়াম সদস্যদের ক্রয় রেট অন্যদের থেকে {} (উল্লেখযোগ্য/উল্লেখযোগ্য নয়)
   - লিঙ্গ ও ক্রয়ের মধ্যে {} (সম্পর্ক আছে/নেই)
   - সদস্যপদ অনুযায়ী ক্রয় পরিমাণে {} (পার্থক্য আছে/নেই)

৪. A/B টেস্টিং:
   - নতুন ফিচার ক্রয় রেট {}% বাড়িয়েছে
   - পরিবর্তনটি {} (স্ট্যাটিস্টিকালি সিগনিফিকেন্ট/নয়)
""".format(
    len(customers),
    round(customers['ক্রয়_করেছে'].mean()*100, 1),
    'উল্লেখযোগ্য' if p_val < alpha else 'উল্লেখযোগ্য নয়',
    'সম্পর্ক আছে' if p_chi < alpha else 'সম্পর্ক নেই',
    'পার্থক্য আছে' if p_val3 < alpha else 'পার্থক্য নেই',
    round((treatment_group.mean()/control_group.mean()-1)*100, 2),
    'স্ট্যাটিস্টিকালি সিগনিফিকেন্ট' if p_ab < alpha else 'স্ট্যাটিস্টিকালি সিগনিফিকেন্ট নয়'
))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.bar(['কন্ট্রোল', 'ট্রিটমেন্ট'], [control_group.mean()*100, treatment_group.mean()*100], 
        color=['red', 'green'], edgecolor='black')
plt.ylabel('কনভার্সন রেট (%)')
plt.title('A/B টেস্ট: কনভার্সন রেট তুলনা')
for i, v in enumerate([control_group.mean()*100, treatment_group.mean()*100]):
    plt.text(i, v + 0.1, f'{v:.2f}%', ha='center', fontweight='bold')

plt.subplot(1, 2, 2)
bars = plt.bar(['SRS', 'স্ট্র্যাটিফাইড', 'সিস্টেমেটিক'], 
               [comparison[comparison['মেথড']=='SRS']['এবসোলিউট এরর'].mean(),
                abs(stratified['ক্রয়_করেছে'].mean() - true_rate),
                comparison[comparison['মেথড']=='সিস্টেমেটিক']['এবসোলিউট এরর'].mean()],
               color=['blue', 'orange', 'green'], edgecolor='black')
plt.ylabel('গড় এবসোলিউট এরর')
plt.title('স্যাম্পলিং মেথড তুলনা')

plt.tight_layout()
plt.savefig('project_summary.png')
plt.show()
print("প্রজেক্ট সামারি গ্রাফ সেভ করা হয়েছে!")
print("\n===== প্রজেক্ট সম্পন্ন =====")
```

### শেখার রিসোর্স:
- **স্যাম্পলিং**: পপুলেশন থেকে প্রতিনিধিত্বমূলক ডেটা নির্বাচনের কৌশল
- **হাইপোথিসিস টেস্টিং**: ডেটা-ভিত্তিক সিদ্ধান্ত গ্রহণের পরিসংখ্যানিক পদ্ধতি
- **A/B টেস্টিং**: প্রোডাক্ট ও মার্কেটিং পরিবর্তনের ইমপ্যাক্ট মাপার জন্য
- **p-value**: ফলাফলের পরিসংখ্যানিক তাৎপর্য মাপার মেট্রিক

এই প্রজেক্টে আমরা শিখলাম কীভাবে বাস্তব ডেটায় স্যাম্পলিং ও হাইপোথিসিস টেস্টিং প্রয়োগ করতে হয় এবং ফলাফল থেকে বিজনেস ইনসাইট বের করতে হয়।
