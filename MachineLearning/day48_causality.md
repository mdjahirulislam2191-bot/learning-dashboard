# Day 48: কজুয়ালিটি
## Causality in ML

### কজুয়ালিটি (কার্যকারণ) কি?
কজুয়ালিটি হল কারণ এবং প্রভাবের মধ্যে সম্পর্ক। ML-তে, কোরিলেশন ≠ কজুয়েশন। কারণ ML মডেল প্যাটার্ন শিখলেও সেটি কার্যকারণ সম্পর্ক নাও হতে পারে।

### ফাইন্যান্সে কজুয়ালিটি
- **নীতি পরিবর্তনের প্রভাব**: সুদ হার বৃদ্ধির অর্থনীতিতে প্রভাব
- **মার্কেটিং ক্যাম্পেইন ROI**: বিজ্ঞাপন ব্যয় vs বিক্রয়
- **রিস্ক ফ্যাক্টর**: কোন কারণগুলি ডিফল্ট ঝুঁকি বাড়ায়
- **পোর্টফোলিও পারফরম্যান্স**: ট্রেডিং স্ট্র্যাটেজি বনাম মার্কেট

### ফাইন্যান্স উদাহরণ: কজুয়াল ইনফারেন্স
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ফাইন্যান্সিয়াল কজুয়াল ডেটা
np.random.seed(42)
n = 1000

# কনফাউন্ডার: অর্থনৈতিক অবস্থা
economic_health = np.random.randn(n)

# ট্রিটমেন্ট: মার্কেটিং ক্যাম্পেইন (5% গ্রহণ করে)
marketing_campaign = np.random.binomial(1, 0.05 + 0.1 * (economic_health > 0))

# আউটকাম: বিক্রয় (economics + campaign effect + noise)
campaign_effect = 50  # ট্রিটমেন্টের প্রকৃত প্রভাব
sales = 100 + 20 * economic_health + campaign_effect * marketing_campaign + np.random.randn(n) * 30

df = pd.DataFrame({
    'economic_health': economic_health,
    'marketing_campaign': marketing_campaign,
    'sales': sales,
    'customer_satisfaction': 7 + economic_health * 2 + marketing_campaign * 3 + np.random.randn(n)
})

print("📊 Financial Data with Causal Relationships:")
print(df.head())
print(f"\nCampaign participation: {marketing_campaign.mean():.2%}")
print(f"Average sales: {sales.mean():.2f}")
```

### 1. কোরিলেশন ≠ কজুয়েশন
```python
# ============================================
# কোরিলেশন বিশ্লেষণ
# ============================================
print("\n" + "=" * 60)
print("📊 CORRELATION ≠ CAUSATION")
print("=" * 60)

correlation_matrix = df.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix.round(3))

print(f"\nSales ~ Marketing Campaign: r = {correlation_matrix.loc['sales', 'marketing_campaign']:.4f}")
print(f"Sales ~ Economic Health: r = {correlation_matrix.loc['sales', 'economic_health']:.4f}")
print(f"Marketing ~ Economic Health: r = {correlation_matrix.loc['marketing_campaign', 'economic_health']:.4f}")

print("\n⚠️  Problem: Campaign and Economic Health are correlated!")
print("   Economic health is a CONFOUNDER (confounding variable)")
print("   It influences BOTH marketing campaign AND sales")
```

### 2. কজুয়াল ইনফারেন্স: লিনিয়ার রিগ্রেশন
```python
# ============================================
# কজুয়াল ইনফারেন্স - রিগ্রেশন
# ============================================
print("\n" + "=" * 60)
print("🔬 CAUSAL INFERENCE - LINEAR REGRESSION")
print("=" * 60)

# নাইভ মডেল (শুধু campaign)
naive_model = LinearRegression()
naive_model.fit(df[['marketing_campaign']], df['sales'])
naive_effect = naive_model.coef_[0]

print(f"Naive model (without confounders):")
print(f"  Estimated campaign effect: ${naive_effect:.2f}")
print(f"  True effect: ${campaign_effect:.2f}")
print(f"  Bias: ${campaign_effect - naive_effect:.2f}")

# কজুয়াল মডেল (কনফাউন্ডার নিয়ন্ত্রণ)
causal_model = LinearRegression()
causal_model.fit(df[['marketing_campaign', 'economic_health']], df['sales'])
causal_effect = causal_model.coef_[0]

print(f"\nCausal model (with confounders):")
print(f"  Estimated campaign effect: ${causal_effect:.2f}")
print(f"  True effect: ${campaign_effect:.2f}")
print(f"  Bias: ${campaign_effect - causal_effect:.2f}")
print(f"  ✅ Much closer to true effect!")
```

### 3. Propensity Score Matching (PSM)
```python
# ============================================
# Propensity Score Matching
# ============================================
print("\n" + "=" * 60)
print("🎯 PROPENSITY SCORE MATCHING")
print("=" * 60)

# Propensity Score (ট্রিটমেন্টের সম্ভাবনা)
from sklearn.neighbors import NearestNeighbors

# Propensity score estimation
propensity_model = LogisticRegression()
X_confounders = df[['economic_health']]
propensity_model.fit(X_confounders, df['marketing_campaign'])
df['propensity_score'] = propensity_model.predict_proba(X_confounders)[:, 1]

print("\n📊 Propensity Scores:")
print(f"  Control (campaign=0): mean={df[df['marketing_campaign']==0]['propensity_score'].mean():.4f}")
print(f"  Treatment (campaign=1): mean={df[df['marketing_campaign']==1]['propensity_score'].mean():.4f}")

# ম্যাচিং
treated = df[df['marketing_campaign'] == 1]
control = df[df['marketing_campaign'] == 0]

# Nearest neighbor matching on propensity score
nn = NearestNeighbors(n_neighbors=1)
nn.fit(control[['propensity_score']])
distances, indices = nn.kneighbors(treated[['propensity_score']])

# ম্যাচড কন্ট্রোল
matched_controls = control.iloc[indices.flatten()]
matched_outcomes = [
    treated['sales'].values[i] - matched_controls.iloc[i]['sales']
    for i in range(len(treated))
]

ate_psm = np.mean(matched_outcomes)
print(f"\n📊 Propensity Score Matching Results:")
print(f"  ATE (Average Treatment Effect): ${ate_psm:.2f}")
print(f"  True effect: ${campaign_effect:.2f}")
print(f"  Error: ${abs(ate_psm - campaign_effect):.2f}")
```

### 4. Difference-in-Differences (DiD)
```python
# ============================================
# Difference-in-Differences
# ============================================
print("\n" + "=" * 60)
print("📈 DIFFERENCE-IN-DIFFERENCES (DiD)")
print("=" * 60)

# DiD: প্রি-পোস্ট ট্রিটমেন্ট কম্পারিজন
time_periods = pd.DataFrame({
    'time': ['pre'] * n + ['post'] * n,
    'group': np.concatenate([np.random.binomial(1, 0.3, n), 
                              np.random.binomial(1, 0.3, n)]),
    'economic_health': np.concatenate([economic_health, economic_health + np.random.randn(n) * 0.1])
})

# প্রি-পিরিয়ড (কোন ক্যাম্পেইন নাই)
time_periods.loc[time_periods['time'] == 'pre', 'sales'] = (
    100 + 20 * time_periods.loc[time_periods['time'] == 'pre', 'economic_health'] + np.random.randn(n) * 30
)

# পোস্ট-পিরিয়ড (ক্যাম্পেইন এফেক্ট)
time_periods.loc[time_periods['time'] == 'post', 'sales'] = (
    100 + 20 * time_periods.loc[time_periods['time'] == 'post', 'economic_health'] + 
    campaign_effect * time_periods.loc[time_periods['time'] == 'post', 'group'] + 
    np.random.randn(n) * 30
)

# DiD calculation
pre_control = time_periods[(time_periods['time']=='pre') & (time_periods['group']==0)]['sales'].mean()
pre_treatment = time_periods[(time_periods['time']=='pre') & (time_periods['group']==1)]['sales'].mean()
post_control = time_periods[(time_periods['time']=='post') & (time_periods['group']==0)]['sales'].mean()
post_treatment = time_periods[(time_periods['time']=='post') & (time_periods['group']==1)]['sales'].mean()

did_effect = (post_treatment - pre_treatment) - (post_control - pre_control)

print("\n📊 Difference-in-Differences Results:")
print(f"  Pre-treatment Control: {pre_control:.2f}")
print(f"  Pre-treatment Treatment: {pre_treatment:.2f}")
print(f"  Post-treatment Control: {post_control:.2f}")
print(f"  Post-treatment Treatment: {post_treatment:.2f}")
print(f"  DiD Estimate: ${did_effect:.2f}")
print(f"  True Effect: ${campaign_effect:.2f}")
```

### 5. কজুয়াল গ্রাফ (DAG)
```python
# ============================================
# কজুয়াল গ্রাফ (DAG)
# ============================================
print("\n" + "=" * 60)
print("🔗 CAUSAL DAG (Directed Acyclic Graph)")
print("=" * 60)

print("""
📌 Causal Graph for Marketing Campaign:

    Economic Health
      ↗         ↘
    /             \\
Marketing         Sales
Campaign  --------→

📖 Interpretation:
- Economic Health → Marketing Campaign (confounder)
- Economic Health → Sales (confounder)
- Marketing Campaign → Sales (causal effect of interest)

💡 To estimate causal effect:
  ➜ Condition/CONTROL for Economic Health
  ➜ Or use: PSM, DiD, IV, or Randomized Experiment
""")

# DAG-ভিত্তিক ভেরিয়েবল সিলেকশন
print("\n📋 DAG-based Variable Selection:")
print("  ✔ Include: Economic Health (confounder)")
print("  ✔ Include: Marketing Campaign (treatment)")
print("  ✔ Target: Sales (outcome)")
print("  ❌ Exclude: Customer Satisfaction (mediator/ collider)")
```

### 6. র‍্যান্ডমাইজড কন্ট্রোল ট্রায়াল (RCT)
```python
# ============================================
# র‍্যান্ডমাইজড এক্সপেরিমেন্ট (গোল্ড স্ট্যান্ডার্ড)
# ============================================
print("\n" + "=" * 60)
print("🏆 RANDOMIZED CONTROL TRIAL (RCT)")
print("=" * 60)

# RCT: র‍্যান্ডম অ্যাসাইনমেন্ট
n_rct = 500
rct_data = pd.DataFrame({
    'economic_health': np.random.randn(n_rct),
    'group': np.random.binomial(1, 0.5, n_rct)  # র‍্যান্ডম
})

# ট্রিটমেন্ট এফেক্ট (কনফাউন্ডিং নাই)
true_effect_rct = 45
rct_data['sales'] = (
    100 + 20 * rct_data['economic_health'] + 
    true_effect_rct * rct_data['group'] + 
    np.random.randn(n_rct) * 30
)

# RCT বিশ্লেষণ
rct_model = LinearRegression()
rct_model.fit(rct_data[['group']], rct_data['sales'])
rct_effect = rct_model.coef_[0]

print(f"\n📊 RCT Results (Gold Standard):")
print(f"  Group 0 mean: {rct_data[rct_data['group']==0]['sales'].mean():.2f}")
print(f"  Group 1 mean: {rct_data[rct_data['group']==1]['sales'].mean():.2f}")
print(f"  Estimated effect: ${rct_effect:.2f}")
print(f"  True effect: ${true_effect_rct:.2f}")
print(f"  ✅ RCT gives unbiased estimate!")

# কজুয়াল মেথড তুলনা
print("\n📊 Causal Methods Comparison:")
print(f"{'Method':<35} {'Estimate':<12} {'True Effect':<12} {'Error':<10}")
print("-" * 70)
print(f"{'Naive Regression (no confounders)':<35} ${naive_effect:<9.2f} ${campaign_effect:<9.2f} ${abs(naive_effect-campaign_effect):<7.2f}")
print(f"{'Causal Regression (with confounders)':<35} ${causal_effect:<9.2f} ${campaign_effect:<9.2f} ${abs(causal_effect-campaign_effect):<7.2f}")
print(f"{'Propensity Score Matching':<35} ${ate_psm:<9.2f} ${campaign_effect:<9.2f} ${abs(ate_psm-campaign_effect):<7.2f}")
print(f"{'Difference-in-Differences':<35} ${did_effect:<9.2f} ${campaign_effect:<9.2f} ${abs(did_effect-campaign_effect):<7.2f}")
print(f"{'Randomized Control Trial':<35} ${rct_effect:<9.2f} ${true_effect_rct:<9.2f} ${abs(rct_effect-true_effect_rct):<7.2f}")
```

### কজুয়ালিটি বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ CAUSAL INFERENCE BEST PRACTICES")
print("=" * 60)

print("""
📊 Methods Summary:

1️⃣ Randomized Experiments (RCT) - GOLD STANDARD
   - Random assignment eliminates confounding
   - Expensive, sometimes unethical

2️⃣ Regression with Confounders
   - Control for observable confounders
   - Assumes linearity and no unobserved confounders

3️⃣ Propensity Score Matching
   - Match treated/control units on probability of treatment
   - Requires overlap (common support)

4️⃣ Difference-in-Differences
   - Pre-post comparison with control group
   - Requires parallel trends assumption

5️⃣ Instrumental Variables (IV)
   - Uses external instrument (not covered here)
   - For unobserved confounding

6️⃣ Causal Forests / Causal ML
   - ML-based heterogeneous treatment effects
   - Uplift modeling

⚠️ Common Causal Fallacies:
- Confirmation bias (seeing what you expect)
- Omitted variable bias (unobserved confounders)
- Reverse causality (A causes B, but B also causes A)
- Selection bias (non-random sample)
- Simpson's paradox (trend reverses in subgroups)
""")
```

### সারসংক্ষেপ
আজ আমরা কজুয়ালিটি শিখলাম:
- **কোরিলেশন ≠ কজুয়েশন**: কনফাউন্ডারের সমস্যা
- **লিনিয়ার রিগ্রেশন**: কনফাউন্ডার নিয়ন্ত্রণ
- **Propensity Score Matching**: শুধু প্যারালাল ট্রেন্ডস
- **Difference-in-Differences**: প্রি-পোস্ট কম্পারিজন
- **RCT**: গোল্ড স্ট্যান্ডার্ড
- **DAG**: কজুয়াল গ্রাফ মডেলিং

### অনুশীলনী
1. ইন্সট্রুমেন্টাল ভেরিয়েবল (IV) রিগ্রেশন ইমপ্লিমেন্ট করুন
2. কজুয়াল ফরেস্ট (EconML, CausalML) ব্যবহার করুন
3. আপনার ডেটাসেটে DAG তৈরি করুন এবং কজুয়াল পাথ আইডেন্টিফাই করুন
4. সিম্পসন্স প্যারাডক্সের রিয়েল উদাহরণ খুঁজুন এবং বিশ্লেষণ করুন