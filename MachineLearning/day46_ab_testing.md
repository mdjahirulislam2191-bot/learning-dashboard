# Day 46: A/B টেস্টিং
## A/B Testing

### A/B টেস্টিং কি?
A/B টেস্টিং একটি পরিসংখ্যানিক পদ্ধতি যা দুটি বা ততোধিক ভার্সনের পারফরম্যান্স তুলনা করে। ML-তে এটি নতুন মডেল বনাম পুরনো মডেলের পারফরম্যান্স ভ্যালিডেট করতে ব্যবহৃত হয়।

### ফাইন্যান্সে A/B টেস্টিং
- **নতুন ML মডেল vs পুরনো মডেল**: রিস্ক স্কোরিং
- **ফ্রড ডিটেকশন অ্যালগরিদম**: নতুন থ্রেশহোল্ড টেস্টিং
- **ক্রেডিট স্কোরিং মডেল**: নিউ ফিচারের ইমপ্যাক্ট
- **ট্রেডিং স্ট্র্যাটেজি**: নতুন অ্যালগরিদম vs বেসলাইন

### ফাইন্যান্স উদাহরণ: ফ্রড ডিটেকশন A/B টেস্ট
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import seaborn as sns

np.random.seed(42)

# ============================================
# সিমুলেটেড A/B টেস্ট
# ============================================
print("=" * 60)
print("📊 A/B TEST SIMULATION - Fraud Detection")
print("=" * 60)

# বর্তমান মডেল (A - কন্ট্রোল)
# নতুন মডেল (B - ট্রিটমেন্ট)
n_samples = 10000

# কন্ট্রোল গ্রুপ (A): 3% ফ্রড, 92% অ্যাকুরেসি
control_fraud = np.random.binomial(1, 0.03, n_samples)
control_pred = np.where(
    np.random.rand(n_samples) < 0.92,  # 92% accuracy
    control_fraud,
    1 - control_fraud
)

# ট্রিটমেন্ট গ্রুপ (B): 3% ফ্রড, 94% অ্যাকুরেসি (2% উন্নতি)
treatment_fraud = np.random.binomial(1, 0.03, n_samples)
treatment_pred = np.where(
    np.random.rand(n_samples) < 0.94,  # 94% accuracy
    treatment_fraud,
    1 - treatment_fraud
)

# মেট্রিক্স
control_metrics = {
    'accuracy': accuracy_score(control_fraud, control_pred),
    'precision': precision_score(control_fraud, control_pred),
    'recall': recall_score(control_fraud, control_pred),
    'f1': f1_score(control_fraud, control_pred)
}

treatment_metrics = {
    'accuracy': accuracy_score(treatment_fraud, treatment_pred),
    'precision': precision_score(treatment_fraud, treatment_pred),
    'recall': recall_score(treatment_fraud, treatment_pred),
    'f1': f1_score(treatment_fraud, treatment_pred)
}

print("\n📊 Model A (Control) Metrics:")
for k, v in control_metrics.items():
    print(f"  {k}: {v:.4f}")

print("\n📊 Model B (Treatment) Metrics:")
for k, v in treatment_metrics.items():
    print(f"  {k}: {v:.4f}")
```

### 1. স্ট্যাটিস্টিক্যাল সিগনিফিকেন্স টেস্ট
```python
# ============================================
# স্ট্যাটিস্টিক্যাল টেস্টিং
# ============================================
print("\n" + "=" * 60)
print("📊 STATISTICAL SIGNIFICANCE TEST")
print("=" * 60)

def ab_test_metrics(control_outcomes, treatment_outcomes, metric='accuracy'):
    """A/B টেস্ট স্ট্যাটিস্টিক্যাল সিগনিফিকেন্স"""
    
    # প্রপোর্শন টেস্ট
    control_correct = (control_outcomes['actual'] == control_outcomes['predicted']).mean()
    treatment_correct = (treatment_outcomes['actual'] == treatment_outcomes['predicted']).mean()
    
    n_control = len(control_outcomes)
    n_treatment = len(treatment_outcomes)
    
    # জেড-টেস্ট (প্রপোর্শন)
    p_pooled = (control_correct * n_control + treatment_correct * n_treatment) / (n_control + n_treatment)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
    z_stat = (treatment_correct - control_correct) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Lift
    relative_lift = (treatment_correct - control_correct) / control_correct
    
    return {
        'control_rate': control_correct,
        'treatment_rate': treatment_correct,
        'absolute_lift': treatment_correct - control_correct,
        'relative_lift': relative_lift,
        'z_statistic': z_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        '90_ci': (treatment_correct - control_correct - 1.645 * se,
                  treatment_correct - control_correct + 1.645 * se),
        '95_ci': (treatment_correct - control_correct - 1.96 * se,
                  treatment_correct - control_correct + 1.96 * se)
    }

# টেস্ট ডেটা
control_data = {'actual': control_fraud, 'predicted': control_pred}
treatment_data = {'actual': treatment_fraud, 'predicted': treatment_pred}

results = ab_test_metrics(control_data, treatment_data)

print(f"\n📊 A/B Test Results (Accuracy):")
print(f"  Control:    {results['control_rate']:.4f}")
print(f"  Treatment:  {results['treatment_rate']:.4f}")
print(f"  Lift:       {results['absolute_lift']:.4f} ({results['relative_lift']:.2%})")
print(f"  Z-statistic: {results['z_statistic']:.4f}")
print(f"  P-value:     {results['p_value']:.6f}")
print(f"  95% CI:      [{results['95_ci'][0]:.4f}, {results['95_ci'][1]:.4f}]")
print(f"  Significant: {'✅ Yes' if results['significant'] else '❌ No'}")
```

### 2. A/B টেস্ট ডিজাইন
```python
# ============================================
# A/B টেস্ট ডিজাইন এবং নমুনা সাইজ
# ============================================
print("\n" + "=" * 60)
print("📋 A/B TEST DESIGN")
print("=" * 60)

def calculate_sample_size(baseline_rate, minimum_detectable_effect, 
                          alpha=0.05, beta=0.20):
    """প্রয়োজনীয় নমুনা সাইজ ক্যালকুলেট"""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(1 - beta)
    
    p1 = baseline_rate
    p2 = baseline_rate * (1 + minimum_detectable_effect)
    
    p_pooled = (p1 + p2) / 2
    
    n = ((z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) + 
          z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (p2 - p1) ** 2
    
    return int(np.ceil(n))

# উদাহরণ: ফ্রড ডিটেকশনের জন্য নমুনা সাইজ
baseline_fraud_rate = 0.03
mde = 0.20  # 20% improvement detect করতে চাই

n_needed = calculate_sample_size(baseline_fraud_rate, mde)
print(f"\n📊 Sample Size Calculation:")
print(f"  Baseline fraud rate: {baseline_fraud_rate:.1%}")
print(f"  Minimum detectable effect: {mde:.0%}")
print(f"  Required sample per group: {n_needed:,}")
print(f"  Total samples needed: {n_needed * 2:,}")
print(f"  (α=0.05, β=0.20, power=80%)")

# বিভিন্ন MDE এর জন্য নমুনা সাইজ
print("\n\nRequired Samples by MDE:")
for effect in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
    n = calculate_sample_size(baseline_fraud_rate, effect)
    print(f"  MDE {effect:.0%}: {n:,} per group")
```

### 3. র‍্যান্ডমাইজেশন এবং ট্রাফিক স্প্লিট
```python
# ============================================
# র‍্যান্ডমাইজেশন স্ট্র্যাটেজি
# ============================================
print("\n" + "=" * 60)
print("🎲 RANDOMIZATION & TRAFFIC SPLIT")
print("=" * 60)

class ABTestSplitter:
    """A/B টেস্ট ট্রাফিক স্প্লিটার"""
    def __init__(self, treatment_prob=0.5, seed=42):
        self.treatment_prob = treatment_prob
        self.rng = np.random.default_rng(seed)
        self.assignments = {}
    
    def assign_group(self, user_id):
        """ইউজারকে গ্রুপে অ্যাসাইন করুন"""
        if user_id not in self.assignments:
            self.assignments[user_id] = 'B' if self.rng.random() < self.treatment_prob else 'A'
        return self.assignments[user_id]
    
    def get_group_summary(self):
        """গ্রুপ ডিস্ট্রিবিউশন সারাংশ"""
        a_count = sum(1 for v in self.assignments.values() if v == 'A')
        b_count = sum(1 for v in self.assignments.values() if v == 'B')
        total = len(self.assignments)
        return {
            'A': a_count,
            'B': b_count,
            'A_pct': a_count / total * 100,
            'B_pct': b_count / total * 100,
            'total': total
        }

# সিমুলেট
splitter = ABTestSplitter(treatment_prob=0.5)
user_ids = range(10000)
for uid in user_ids:
    splitter.assign_group(uid)

summary = splitter.get_group_summary()
print(f"\n📋 Traffic Split:")
print(f"  Group A (Control):   {summary['A']:>5,} ({summary['A_pct']:.1f}%)")
print(f"  Group B (Treatment): {summary['B']:>5,} ({summary['B_pct']:.1f}%)")
print(f"  Total:               {summary['total']:>5,}")
```

### 4. A/B টেস্ট রিপোর্টিং
```python
# ============================================
# A/B টেস্ট রিপোর্ট
# ============================================
print("\n" + "=" * 60)
print("📋 A/B TEST REPORT")
print("=" * 60)

def generate_ab_report(control_metrics, treatment_metrics, test_results):
    """A/B টেস্ট রিপোর্ট জেনারেট"""
    print("\n" + "=" * 60)
    print("📊 A/B TEST REPORT - Fraud Detection Model")
    print("=" * 60)
    
    print(f"\nHypothesis:")
    print(f"  H₀: Model B accuracy ≤ Model A accuracy (no improvement)")
    print(f"  H₁: Model B accuracy > Model A accuracy (improvement)")
    
    print(f"\n📊 Metrics Comparison:")
    print(f"{'Metric':<15} {'Control (A)':<15} {'Treatment (B)':<15} {'Δ':<10} {'% Change':<10}")
    print("-" * 65)
    
    for metric in control_metrics:
        c_val = control_metrics[metric]
        t_val = treatment_metrics[metric]
        diff = t_val - c_val
        pct = (diff / c_val) * 100
        print(f"{metric:<15} {c_val:<15.4f} {t_val:<15.4f} {diff:<+10.4f} {pct:<+10.2%}")
    
    print(f"\n📊 Statistical Results:")
    print(f"  P-value: {test_results['p_value']:.6f}")
    print(f"  Z-statistic: {test_results['z_statistic']:.4f}")
    print(f"  {test_results['control_rate']:.4f} vs {test_results['treatment_rate']:.4f}")
    print(f"  Absolute Lift: {test_results['absolute_lift']:.4f}")
    print(f"  Relative Lift: {test_results['relative_lift']:.2%}")
    print(f"  95% CI: [{test_results['95_ci'][0]:.4f}, {test_results['95_ci'][1]:.4f}]")
    
    print(f"\n🎯 Conclusion:")
    if test_results['significant']:
        print(f"  ✅ Statistically significant! Deploy Model B.")
        print(f"  Expected improvement: {test_results['relative_lift']:.2%}")
    else:
        print(f"  ❌ Not statistically significant. Keep running test.")
        print(f"  Consider larger sample size or longer test duration.")
    
    print("\n" + "=" * 60)

generate_ab_report(control_metrics, treatment_metrics, results)
```

### A/B টেস্ট বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ A/B TESTING BEST PRACTICES")
print("=" * 60)

print("""
📋 A/B Testing in ML:

1️⃣ Test Design
   - Clear hypothesis (H₀ vs H₁)
   - Determine minimum detectable effect (MDE)
   - Calculate required sample size
   - Random assignment of users/transactions
   - One metric as primary (avoid multiple comparison)

2️⃣ Execution
   - Run test for sufficient duration
   - Avoid peeking (look at results early)
   - Monitor both groups for side effects
   - Document all changes

3️⃣ Analysis
   - Check statistical significance (p < 0.05)
   - Consider practical significance (business impact)
   - Check for Simpson's paradox
   - Validate with holdout set

4️⃣ Common Mistakes
   ❌ Multiple testing without correction
   ❌ Early stopping (peeking)
   ❌ Ignoring novelty effects
   ❌ Unequal sample distribution
   ❌ Not considering business metrics

5️⃣ ML-Specific Considerations
   - Model A/B ≠ feature A/B
   - Shadow deployment (log both model outputs)
   - Gradual rollout (1% → 5% → 50% → 100%)
   - Rollback plan ready
""")
```

### সারসংক্ষেপ
আজ আমরা A/B টেস্টিং শিখলাম:
- **হাইপোথেসিস টেস্টিং**: Z-test, p-value
- **নমুনা সাইজ**: MDE, α, β ক্যালকুলেশন
- **র‍্যান্ডমাইজেশন**: ট্রাফিক স্প্লিট স্ট্র্যাটেজি
- **রিপোর্টিং**: কম্প্রিহেনসিভ A/B টেস্ট রিপোর্ট
- **বেস্ট প্র্যাকটিস**: ML মডেল ডিপ্লয়মেন্টের জন্য

### অনুশীলনী
1. মাল্টি-আর্মড ব্যান্ডিট (MAB) অ্যালগরিদম ইমপ্লিমেন্ট করুন
2. বায়েসিয়ান A/B টেস্টিং ব্যবহার করুন
3. A/B টেস্ট রেজাল্ট মনিটরিং ড্যাশবোর্ড তৈরি করুন
4. গ্রাজুয়াল রোলআউট প্ল্যান ইমপ্লিমেন্ট করুন