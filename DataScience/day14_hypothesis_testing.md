# Day 14: হাইপোথিসিস টেস্টিং
## Hypothesis Testing

### হাইপোথিসিস টেস্টিং কী?
হাইপোথিসিস টেস্টিং হলো পরিসংখ্যানের একটি পদ্ধতি যা ডেটার ভিত্তিতে কোনো অনুমান সত্য বা মিথ্যা তা যাচাই করে। ডেটা সায়েন্সে এটি মডেল তুলনা, A/B টেস্টিং এবং সিদ্ধান্ত গ্রহণে ব্যবহৃত হয়।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel, f_oneway, chi2_contingency, norm
import warnings
warnings.filterwarnings('ignore')

# স্যাম্পল ডেটা তৈরি
np.random.seed(42)

# গ্রুপ A (কন্ট্রোল) - পুরাতন ওয়েবসাইট
group_a = np.random.normal(150, 25, 200)  # বিক্রয়

# গ্রুপ B (ট্রিটমেন্ট) - নতুন ওয়েবসাইট
group_b = np.random.normal(160, 25, 200)  # বিক্রয় (১০ বেশি)

print("=== গ্রুপ এ (কন্ট্রোল) ===")
print(f"মিন: {group_a.mean():.2f}, স্টিড: {group_a.std():.2f}")
print(f"সাইজ: {len(group_a)}")

print("\n=== গ্রুপ বি (ট্রিটমেন্ট) ===")
print(f"মিন: {group_b.mean():.2f}, স্টিড: {group_b.std():.2f}")
print(f"সাইজ: {len(group_b)}")
```

### হাইপোথিসিস টেস্টিং এর ধাপসমূহ:

```python
print("\n=== হাইপোথিসিস টেস্টিং স্টেপ ===")

# Null Hypothesis (H₀): গ্রুপ A = গ্রুপ B (কোনো পার্থক্য নেই)
# Alternative Hypothesis (H₁): গ্রুপ A ≠ গ্রুপ B (পার্থক্য আছে)
print("H₀: μA = μB (কোনো পার্থক্য নেই)")
print("H₁: μA ≠ μB (পার্থক্য আছে)")
```

#### ১. টু-স্যাম্পল টি-টেস্ট (Independent T-Test):
```python
print("\n=== টু-স্যাম্পল টি-টেস্ট ===")

t_stat, p_value = ttest_ind(group_a, group_b)
print(f"টি-স্ট্যাটিস্টিক: {t_stat:.4f}")
print(f"পি-ভ্যালু: {p_value:.6f}")

alpha = 0.05
if p_value < alpha:
    print(f"\nপি-ভ্যালু ({p_value:.6f}) < α ({alpha})")
    print("=> H₀ রিজেক্ট! গ্রুপ এ এবং গ্রুপ বি এর মধ্যে পরিসংখ্যানিক পার্থক্য আছে।")
else:
    print(f"\nপি-ভ্যালু ({p_value:.6f}) >= α ({alpha})")
    print("=> H₀ রিজেক্ট করতে ব্যর্থ। পর্যাপ্ত প্রমাণ নেই।")

# কনফিডেন্স ইন্টারভ্যাল
diff = group_b.mean() - group_a.mean()
se = np.sqrt(group_a.var()/len(group_a) + group_b.var()/len(group_b))
ci_low = diff - 1.96 * se
ci_high = diff + 1.96 * se
print(f"\nপার্থক্য: {diff:.2f}")
print(f"৯৫% কনফিডেন্স ইন্টারভ্যাল: ({ci_low:.2f}, {ci_high:.2f})")
```

#### ২. ওয়ান-স্যাম্পল টি-টেস্ট:
```python
print("\n=== ওয়ান-স্যাম্পল টি-টেস্ট ===")

# একটি গ্রুপের মিন নির্দিষ্ট মানের সমান কিনা
# H₀: গ্রুপ A এর মিন = 150
# H₁: গ্রুপ A এর মিন ≠ 150

t_stat_1, p_value_1 = stats.ttest_1samp(group_a, 150)
print(f"H₀: μA = 150")
print(f"টি-স্ট্যাটিস্টিক: {t_stat_1:.4f}")
print(f"পি-ভ্যালু: {p_value_1:.6f}")

if p_value_1 < alpha:
    print(f"=> পি-ভ্যালু < α: H₀ রিজেক্ট! মিন ১৫০ থেকে ভিন্ন।")
else:
    print(f"=> পি-ভ্যালু >= α: H₀ রিজেক্ট করতে ব্যর্থ।")

# অন্যভাবে: মিন ১৫০ কিনা চেক
t_stat_1b, p_value_1b = stats.ttest_1samp(group_a, group_a.mean())
print(f"\nH₀: μA = {group_a.mean():.2f}")
print(f"টি-স্ট্যাটিস্টিক: {t_stat_1b:.4f}")
print(f"পি-ভ্যালু: {p_value_1b:.6f}")
if p_value_1b < alpha:
    print("=> H₀ রিজেক্ট")
else:
    print("=> H₀ অ্যাক্সেপ্ট (কার্যত ১ হওয়ার কথা)")
```

#### ৩. পেয়ারড টি-টেস্ট:
```python
print("\n=== পেয়ারড টি-টেস্ট ===")

# একই ব্যক্তির Before-After পরিমাপ
before = np.random.normal(70, 10, 50)  # Before treatment
after = before + np.random.normal(5, 3, 50)  # After treatment (৫ পয়েন্ট বেড়েছে)

t_stat_p, p_value_p = ttest_rel(before, after)
print(f"Before Mean: {before.mean():.2f}")
print(f"After Mean: {after.mean():.2f}")
print(f"পেয়ারড টি-স্ট্যাটিস্টিক: {t_stat_p:.4f}")
print(f"পি-ভ্যালু: {p_value_p:.6f}")

if p_value_p < alpha:
    print("=> ট্রিটমেন্টের আগে ও পরে পার্থক্য আছে (ট্রিটমেন্ট কার্যকর)!")
else:
    print("=> ট্রিটমেন্ট কার্যকর প্রমাণিত হয়নি।")
```

#### ৪. ANOVA (Analysis of Variance):
```python
print("\n=== ANOVA (তিন বা ততোধিক গ্রুপের তুলনা) ===")

# তিনটি ভিন্ন মার্কেটিং কৌশলের বিক্রয়
strategy_a = np.random.normal(100, 15, 50)
strategy_b = np.random.normal(110, 15, 50)
strategy_c = np.random.normal(95, 15, 50)

f_stat, p_value_anova = f_oneway(strategy_a, strategy_b, strategy_c)
print(f"স্ট্র্যাটেজি A মিন: {strategy_a.mean():.2f}")
print(f"স্ট্র্যাটেজি B মিন: {strategy_b.mean():.2f}")
print(f"স্ট্র্যাটেজি C মিন: {strategy_c.mean():.2f}")
print(f"\nএফ-স্ট্যাটিস্টিক: {f_stat:.4f}")
print(f"পি-ভ্যালু: {p_value_anova:.6f}")

if p_value_anova < alpha:
    print("=> অন্তত একটি স্ট্র্যাটেজি অন্যগুলো থেকে ভিন্ন!")
else:
    print("=> সব স্ট্র্যাটেজির মধ্যে পার্থক্য নেই।")

# পোস্ট-হক টেস্ট (কোন গ্রুপ ভিন্ন?)
from scipy.stats import tukey_hsd
posthoc = tukey_hsd(strategy_a, strategy_b, strategy_c)
print(f"\nপোস্ট-হক (Tukey HSD):")
print(f"A vs B: p={posthoc.pvalue[0,1]:.4f}")
print(f"A vs C: p={posthoc.pvalue[0,2]:.4f}")
print(f"B vs C: p={posthoc.pvalue[1,2]:.4f}")
```

#### ৫. চি-স্কোয়ার টেস্ট (ক্যাটেগোরিকাল ডেটার জন্য):
```python
print("\n=== চি-স্কোয়ার টেস্ট ===")

# কন্টিনজেন্সি টেবিল
data = pd.DataFrame({
    'পুরুষ': [30, 20, 50],
    'মহিলা': [20, 30, 50],
    'মোট': [50, 50, 100]
}, index=['পণ্য_কেনে', 'পণ্য_কেনেনি', 'মোট'])
print(f"ক্রসট্যাব:\n{data}")

# কন্টিনজেন্সি টেবিল
observed = np.array([[30, 20], [20, 30]])
chi2, p_chi, dof, expected = chi2_contingency(observed)

print(f"\nচি-স্কোয়ার: {chi2:.4f}")
print(f"পি-ভ্যালু: {p_chi:.4f}")
print(f"ডিগ্রি অফ ফ্রিডম: {dof}")
print(f"\nএক্সপেক্টেড ফ্রিকোয়েন্সি:\n{expected}")

if p_chi < alpha:
    print("=> লিঙ্গ ও পণ্য কেনার মধ্যে সম্পর্ক আছে!")
else:
    print("=> লিঙ্গ ও পণ্য কেনার মধ্যে কোনো সম্পর্ক নেই।")
```

#### ৬. জেড-টেস্ট (বড় স্যাম্পলের জন্য):
```python
print("\n=== জেড-টেস্ট (বড় স্যাম্পল) ===")

def z_test(sample, pop_mean, pop_std):
    """ওয়ান-স্যাম্পল জেড-টেস্ট"""
    z = (np.mean(sample) - pop_mean) / (pop_std / np.sqrt(len(sample)))
    p = 2 * (1 - norm.cdf(abs(z)))  # টু-টেইলড
    return z, p

# বড় স্যাম্পল
large_sample = np.random.normal(52, 10, 1000)
z_stat, p_z = z_test(large_sample, 50, 10)

print(f"স্যাম্পল মিন: {large_sample.mean():.2f}")
print(f"পপুলেশন মিন (H₀): 50")
print(f"জেড-স্ট্যাটিস্টিক: {z_stat:.4f}")
print(f"পি-ভ্যালু: {p_z:.6f}")

if p_z < alpha:
    print("=> স্যাম্পল মিন পপুলেশন মিন থেকে ভিন্ন!")
else:
    print("=> স্যাম্পল মিন পপুলেশন মিন থেকে ভিন্ন নয়।")
```

#### ৭. টাইপ I ও টাইপ II এরর:
```python
print("\n=== টাইপ I ও টাইপ II এরর ===")

print("টাইপ I এরর (মিথ্যা পজিটিভ): H₀ সত্য থাকলেও রিজেক্ট করা")
print("টাইপ II এরর (মিথ্যা নেগেটিভ): H₀ মিথ্যা থাকলেও রিজেক্ট না করা")
print()
print("α (সিগনিফিকেন্স লেভেল) = টাইপ I এররের প্রোবাবিলিটি")
print("β = টাইপ II এররের প্রোবাবিলিটি")
print("Power = 1 - β (টেস্টের পাওয়ার)")

# পাওয়ার অ্যানালাইসিস
from scipy.stats import nct

def power_analysis(effect_size, sample_size, alpha=0.05):
    """টেস্টের পাওয়ার গণনা"""
    df = 2 * sample_size - 2
    t_crit = stats.t.ppf(1 - alpha/2, df)
    ncp = effect_size * np.sqrt(sample_size / 2)  # নন-সেন্ট্রালিটি প্যারামিটার
    power = 1 - nct.cdf(t_crit, df, ncp) + nct.cdf(-t_crit, df, ncp)
    return power

effect_sizes = [0.2, 0.5, 0.8]  # ছোট, মাঝারি, বড় ইফেক্ট
sample_sizes = [20, 50, 100, 200, 500]

print(f"\nপাওয়ার অ্যানালাইসিস (α={alpha}):")
print(f"{'স্যাম্পল':<10} {'ছোট(0.2)':<15} {'মাঝারি(0.5)':<15} {'বড়(0.8)':<15}")
for n in sample_sizes:
    powers = [power_analysis(es, n) for es in effect_sizes]
    print(f"{n:<10} {powers[0]:<15.3f} {powers[1]:<15.3f} {powers[2]:<15.3f}")
```

### A/B টেস্টিং (প্র্যাকটিক্যাল অ্যাপ্লিকেশন):
```python
print("\n=== A/B টেস্টিং ===")

# ওয়েবসাইট কনভার্সন রেট
np.random.seed(123)
n_visitors = 10000

# কন্ট্রোল গ্রুপ (পুরাতন ডিজাইন)
control = np.random.binomial(1, 0.08, n_visitors)  # 8% কনভার্সন

# ট্রিটমেন্ট গ্রুপ (নতুন ডিজাইন)
treatment = np.random.binomial(1, 0.09, n_visitors)  # 9% কনভার্সন

control_rate = control.mean()
treatment_rate = treatment.mean()
lift = (treatment_rate - control_rate) / control_rate * 100

print(f"কন্ট্রোল কনভার্সন রেট: {control_rate:.4f} ({control_rate*100:.2f}%)")
print(f"ট্রিটমেন্ট কনভার্সন রেট: {treatment_rate:.4f} ({treatment_rate*100:.2f}%)")
print(f"লিফট: {lift:.2f}%")

# Z-test for proportions
from statsmodels.stats.proportion import proportions_ztest
counts = np.array([treatment.sum(), control.sum()])
nobs = np.array([n_visitors, n_visitors])
z_stat_prop, p_prop = proportions_ztest(counts, nobs)

print(f"\nজেড-স্ট্যাটিস্টিক: {z_stat_prop:.4f}")
print(f"পি-ভ্যালু: {p_prop:.6f}")

if p_prop < alpha:
    print(f"=> নতুন ডিজাইন পরিসংখ্যানিকভাবে ভালো! (p={p_prop:.4f})")
else:
    print(f"=> নতুন ডিজাইন পরিসংখ্যানিকভাবে আলাদা নয়। (p={p_prop:.4f})")

# নমুনা আকার নির্ধারণ
from statsmodels.stats.power import TTestIndPower
power_analysis = TTestIndPower()
required_n = power_analysis.solve_power(
    effect_size=0.1,  # ছোট ইফেক্ট
    power=0.8,
    alpha=0.05,
    ratio=1.0
)
print(f"\n৮০% পাওয়ার ও ৫% সিগনিফিকেন্সের জন্য প্রয়োজনীয় স্যাম্পল সাইজ: {int(np.ceil(required_n)):,}")
```

### ভিজুয়ালাইজেশন:
```python
print("\n=== ভিজুয়ালাইজেশন ===")

# ডিস্ট্রিবিউশন প্লট
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.hist(group_a, alpha=0.5, label='গ্রুপ A', bins=20, edgecolor='black')
plt.hist(group_b, alpha=0.5, label='গ্রুপ B', bins=20, edgecolor='black')
plt.axvline(group_a.mean(), color='blue', linestyle='--', linewidth=2)
plt.axvline(group_b.mean(), color='orange', linestyle='--', linewidth=2)
plt.xlabel('মান')
plt.ylabel('ফ্রিকোয়েন্সি')
plt.title('টি-টেস্ট: গ্রুপ A vs B')
plt.legend()

# বক্সপ্লট
plt.subplot(1, 3, 2)
plt.boxplot([group_a, group_b], labels=['গ্রুপ A', 'গ্রুপ B'])
plt.title('বক্সপ্লট: গ্রুপ তুলনা')
plt.ylabel('মান')

# পি-ভ্যালু বনাম আলফা ভিজুয়ালাইজেশন
plt.subplot(1, 3, 3)
x = np.linspace(-4, 4, 1000)
y = stats.t.pdf(x, df=len(group_a)+len(group_b)-2)
plt.plot(x, y, 'b-', label='টি-ডিস্ট্রিবিউশন')
t_crit = stats.t.ppf(1-alpha/2, len(group_a)+len(group_b)-2)
plt.axvline(t_crit, color='r', linestyle='--', label=f'ক্রিটিক্যাল ভ্যালু (±{t_crit:.2f})')
plt.axvline(t_stat, color='g', linestyle='--', label=f'টেস্ট স্ট্যাটিস্টিক ({t_stat:.2f})')
plt.fill_between(x, y, where=(x >= t_crit), color='red', alpha=0.3, label='রিজেকশন অঞ্চল')
plt.fill_between(x, y, where=(x <= -t_crit), color='red', alpha=0.3)
plt.xlabel('টি-ভ্যালু')
plt.ylabel('ডেনসিটি')
plt.title('টি-ডিস্ট্রিবিউশন ও ক্রিটিক্যাল ভ্যালু')
plt.legend()

plt.tight_layout()
plt.savefig('hypothesis_testing.png')
plt.show()
print("ভিজুয়ালাইজেশন সেভ করা হয়েছে!")
```

### কখন কোন টেস্ট ব্যবহার করবেন:
```python
print("\n=== টেস্ট সিলেকশন গাইড ===")

test_guide = pd.DataFrame({
    'টেস্ট': ['ওয়ান-স্যাম্পল টি-টেস্ট', 'টু-স্যাম্পল টি-টেস্ট', 'পেয়ারড টি-টেস্ট', 
              'ANOVA', 'চি-স্কোয়ার', 'জেড-টেস্ট', 'ম্যান-হুইটনি ইউ'],
    'ব্যবহার': ['এক গ্রুপের মিন নির্দিষ্ট মানের সাথে তুলনা', 
                'দুই স্বাধীন গ্রুপের মিন তুলনা',
                'একই গ্রুপের Before-After তুলনা',
                'তিন বা ততোধিক গ্রুপের মিন তুলনা',
                'দুই ক্যাটেগোরিকাল ভ্যারিয়েবলের সম্পর্ক',
                'বড় স্যাম্পলের জন্য মিন/প্রপোরশন টেস্ট',
                'নন-প্যারামেট্রিক টু-গ্রুপ তুলনা'],
    'ডেটা টাইপ': ['নিউমেরিক', 'নিউমেরিক', 'নিউমেরিক (পেয়ারড)',
                   'নিউমেরিক', 'ক্যাটেগোরিকাল', 'নিউমেরিক/বাইনারি',
                   'নিউমেরিক (নরমাল না থাকলে)']
})

print(test_guide.to_string(index=False))
```

### সারাংশ:
- **হাইপোথিসিস টেস্টিং** ডেটা-চালিত সিদ্ধান্ত গ্রহণের মূল হাতিয়ার
- **p-value**: H₀ সত্য হলে এত চরম বা আরও চরম ফলাফল পাওয়ার সম্ভাবনা
- **α (সিগনিফিকেন্স লেভেল)**: সাধারণত 0.05 (৫%)
- **p < α** হলে H₀ রিজেক্ট করি (স্ট্যাটিস্টিকালি সিগনিফিকেন্ট)
- **টাইপ I এরর**: মিথ্যা অ্যালার্ম (False Positive)
- **টাইপ II এরর**: মিস করা (False Negative)
- টেস্ট নির্বাচন ডেটার ধরণ ও প্রশ্নের উপর নির্ভর করে
