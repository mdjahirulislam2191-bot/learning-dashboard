# Day 11: প্রোবাবিলিটি রিভিউ
## Probability Review

### প্রোবাবিলিটি কী?
প্রোবাবিলিটি বা সম্ভাবনা গণিতের একটি শাখা যা অনিশ্চিত ঘটনার গাণিতিক বিশ্লেষণ করে। ডেটা সায়েন্সে প্রোবাবিলিটি মডেলিং, প্রেডিকশন এবং সিদ্ধান্ত গ্রহণের ভিত্তি।

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from itertools import permutations, combinations
import warnings
warnings.filterwarnings('ignore')
```

### মৌলিক প্রোবাবিলিটি কনসেপ্ট:
```python
print("=== মৌলিক প্রোবাবিলিটি কনসেপ্ট ===")

# স্যাম্পল স্পেস
coin = ['H', 'T']
dice = [1, 2, 3, 4, 5, 6]

# Probability of events
def prob(event, sample_space):
    """ইভেন্টের প্রোবাবিলিটি গণনা"""
    return len(event) / len(sample_space)

# Coin toss: P(H) = 1/2
p_head = len([x for x in coin if x == 'H']) / len(coin)
print(f"P(Head) = {p_head}")

# Dice: P(even) = 3/6 = 0.5
even = [x for x in dice if x % 2 == 0]
p_even = prob(even, dice)
print(f"P(Even) = {p_even}")

# Dice: P(>4) = 2/6 = 1/3
gt4 = [x for x in dice if x > 4]
p_gt4 = prob(gt4, dice)
print(f"P(>4) = {p_gt4}")
```

### অ্যাডিশন ও মাল্টিপ্লিকেশন রুল:
```python
print("\n=== প্রোবাবিলিটি রুলস ===")

# Addition Rule: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
# Dice example: P(even ∪ >4)
A = set([2, 4, 6])  # even
B = set([5, 6])     # >4
p_union = len(A | B) / 6
print(f"P(Even ∪ >4) = {p_union}")
print(f"P(Even) + P(>4) - P(Even ∩ >4) = {len(A)/6 + len(B)/6 - len(A & B)/6}")

# Multiplication Rule (Independent): P(A ∩ B) = P(A) * P(B)
# Two coins: P(H, H)
p_two_heads = (1/2) * (1/2)
print(f"\nP(H, H) for 2 coins = {p_two_heads}")

# Conditional Probability: P(A|B) = P(A ∩ B) / P(B)
# P(6 | even) = P(6 ∩ even) / P(even) = (1/6) / (3/6) = 1/3
p_6_given_even = (1/6) / (3/6)
print(f"\nP(6 | Even) = {p_6_given_even:.4f}")
```

### বিন্যাস ও সমাবেশ (Permutation & Combination):
```python
print("\n=== বিন্যাস ও সমাবেশ ===")

items = ['A', 'B', 'C', 'D']

# Permutation (ক্রম গুরুত্বপূর্ণ): nPr = n!/(n-r)!
def permutation(n, r):
    return np.math.factorial(n) / np.math.factorial(n - r)

# Combination (ক্রম গুরুত্বহীন): nCr = n!/(r! * (n-r)!)
def combination(n, r):
    return np.math.factorial(n) / (np.math.factorial(r) * np.math.factorial(n - r))

print(f"P(4,2) = {permutation(4, 2):.0f}")
print(f"C(4,2) = {combination(4, 2):.0f}")

# Python built-in
print(f"\nPermutations of {items[:3]}: {list(permutations(items[:3], 2))}")
print(f"Combinations of {items[:3]}: {list(combinations(items[:3], 2))}")

# ব্যবহারিক উদাহরণ: লটারি
total_combos = combination(49, 6)
print(f"\nলটারি জেতার সম্ভাবনা (6/49): 1 in {total_combos:,.0f}")
print(f"Probability: {1/total_combos:.10f}")
```

### ডিসক্রিট প্রোবাবিলিটি ডিস্ট্রিবিউশন:
```python
print("\n=== ডিসক্রিট ডিস্ট্রিবিউশন ===")

# 1. Bernoulli Distribution (একটি ট্রায়াল)
p = 0.7
bernoulli = stats.bernoulli(p)
x = [0, 1]
probabilities = bernoulli.pmf(x)
print(f"Bernoulli(p={p}): P(0)={probabilities[0]:.2f}, P(1)={probabilities[1]:.2f}")

# 2. Binomial Distribution (n টি ট্রায়াল)
n, p = 10, 0.5
binomial = stats.binom(n, p)
x = np.arange(0, n+1)
probs = binomial.pmf(x)

print(f"\nBinomial(n={n}, p={p})")
print(f"P(5 heads) = {binomial.pmf(5):.4f}")
print(f"P(≥8 heads) = {1 - binomial.cdf(7):.4f}")
print(f"Mean = {binomial.mean():.2f}, Var = {binomial.var():.2f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(x, probs, alpha=0.7, color='steelblue', edgecolor='black')
axes[0].set_title(f'Binomial Distribution (n={n}, p={p})')
axes[0].set_xlabel('Number of Successes')
axes[0].set_ylabel('Probability')

# 3. Poisson Distribution
lam = 3
poisson = stats.poisson(lam)
x = np.arange(0, 12)
probs_p = poisson.pmf(x)

axes[1].bar(x, probs_p, alpha=0.7, color='green', edgecolor='black')
axes[1].set_title(f'Poisson Distribution (λ={lam})')
axes[1].set_xlabel('Number of Events')
axes[1].set_ylabel('Probability')

plt.tight_layout()
plt.show()

print(f"\nPoisson(λ={lam}): P(0)={poisson.pmf(0):.4f}")
print(f"P(≥5) = {1 - poisson.cdf(4):.4f}")
```

### কন্টিনিউয়াস প্রোবাবিলিটি ডিস্ট্রিবিউশন:
```python
print("\n=== কন্টিনিউয়াস ডিস্ট্রিবিউশন ===")

# 1. Normal Distribution
mu, sigma = 0, 1
normal = stats.norm(mu, sigma)
x = np.linspace(-4, 4, 100)
pdf = normal.pdf(x)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(x, pdf, 'b-', linewidth=2)
axes[0].fill_between(x, pdf, alpha=0.3, color='steelblue')
axes[0].set_title(f'Standard Normal (μ={mu}, σ={sigma})')
axes[0].set_xlabel('X')
axes[0].set_ylabel('PDF')

# Shade different std dev regions
x_fill = np.linspace(-1, 1, 100)
axes[0].fill_between(x_fill, normal.pdf(x_fill), alpha=0.3, color='red', label='±1σ (68%)')
axes[0].legend()

print(f"Normal(0,1):")
print(f"P(-1 < Z < 1) = {normal.cdf(1) - normal.cdf(-1):.4f}")
print(f"P(-2 < Z < 2) = {normal.cdf(2) - normal.cdf(-2):.4f}")
print(f"P(-3 < Z < 3) = {normal.cdf(3) - normal.cdf(-3):.4f}")

# 2. Exponential Distribution
lam = 0.5
exponential = stats.expon(scale=1/lam)
x = np.linspace(0, 10, 100)
pdf_e = exponential.pdf(x)

axes[1].plot(x, pdf_e, 'r-', linewidth=2)
axes[1].fill_between(x, pdf_e, alpha=0.3, color='red')
axes[1].set_title(f'Exponential Distribution (λ={lam})')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('PDF')

plt.tight_layout()
plt.show()

print(f"\nExponential(λ={lam}):")
print(f"P(X < 2) = {exponential.cdf(2):.4f}")
print(f"P(X > 3) = {1 - exponential.cdf(3):.4f}")
```

### কেন্দ্রীয় সীমা তত্ত্ব (CLT):
```python
print("\n=== কেন্দ্রীয় সীমা তত্ত্ব (Central Limit Theorem) ===")

# CLT ডেমোনস্ট্রেশন
np.random.seed(42)
population = np.random.exponential(scale=2, size=10000)  # skewed distribution
print(f"Population mean: {population.mean():.3f}")
print(f"Population std: {population.std():.3f}")

# বিভিন্ন স্যাম্পল সাইজ দিয়ে স্যাম্পলিং ডিস্ট্রিবিউশন
sample_sizes = [5, 30, 100]
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for idx, n in enumerate(sample_sizes):
    sample_means = [np.random.choice(population, n).mean() for _ in range(1000)]
    axes[idx].hist(sample_means, bins=30, alpha=0.7, color='steelblue', edgecolor='black', density=True)
    axes[idx].axvline(np.mean(sample_means), color='red', linestyle='--', label=f'Mean={np.mean(sample_means):.3f}')
    axes[idx].set_title(f'Sample Size n={n}\nStd={np.std(sample_means):.3f}')
    axes[idx].set_xlabel('Sample Mean')
    axes[idx].set_ylabel('Density')
    axes[idx].legend()

plt.suptitle('Central Limit Theorem Demonstration', y=1.05)
plt.tight_layout()
plt.show()

print("\nCLT পর্যবেক্ষণ:")
print("- n=5: ডিস্ট্রিবিউশন এখনও স্কিউড")
print("- n=30: প্রায় নরমাল (CLT কার্যকর)")
print("- n=100: ক্লিয়ারলি নরমাল ডিস্ট্রিবিউশন")
```

### বায়েস থিওরেম (ভূমিকা):
```python
print("\n=== বায়েস থিওরেম ===")

# বাস্তব উদাহরণ: মেডিকেল টেস্ট
# রোগের প্রাদুর্ভাব: 1%
# টেস্ট সেনসিটিভিটি: 99% (যদি রোগ থাকে, 99% পজিটিভ)
# টেস্ট স্পেসিফিসিটি: 95% (যদি রোগ না থাকে, 95% নেগেটিভ)

P_disease = 0.01       # Prior: P(D)
P_no_disease = 0.99    # P(¬D)
P_pos_given_disease = 0.99    # Sensitivity: P(+|D)
P_pos_given_no_disease = 0.05  # False positive: P(+|¬D)

# P(+) = P(+|D)*P(D) + P(+|¬D)*P(¬D)
P_positive = P_pos_given_disease * P_disease + P_pos_given_no_disease * P_no_disease

# P(D|+) = P(+|D)*P(D) / P(+)
P_disease_given_positive = (P_pos_given_disease * P_disease) / P_positive

print(f"বায়েস থিওরেম - মেডিকেল টেস্ট উদাহরণ:")
print(f"রোগের প্রাদুর্ভাব: {P_disease*100}%")
print(f"টেস্ট সেনসিটিভিটি: {P_pos_given_disease*100}%")
print(f"টেস্ট স্পেসিফিসিটি: {(1-P_pos_given_no_disease)*100}%")
print(f"\nপজিটিভ টেস্টের পর রোগ হওয়ার সম্ভাবনা: {P_disease_given_positive*100:.2f}%")
print(f"অর্থাৎ, পজিটিভ টেস্টের পরও মাত্র {P_disease_given_positive*100:.2f}% সম্ভাবনা রোগের!")
```

### মন্টে কার্লো সিমুলেশন:
```python
print("\n=== মন্টে কার্লো সিমুলেশন ===")

# Pi গণনা মন্টে কার্লো পদ্ধতিতে
np.random.seed(42)
n_simulations = [100, 1000, 10000, 100000]

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for idx, n in enumerate(n_simulations):
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    inside = (x**2 + y**2) <= 1
    pi_estimate = 4 * inside.sum() / n
    
    axes[idx].scatter(x[inside], y[inside], s=1, alpha=0.5, color='green', label='Inside')
    axes[idx].scatter(x[~inside], y[~inside], s=1, alpha=0.5, color='red', label='Outside')
    axes[idx].set_title(f'n={n}: π ≈ {pi_estimate:.4f}')
    axes[idx].set_aspect('equal')
    axes[idx].legend(markerscale=5)

plt.suptitle('Monte Carlo Pi Estimation', fontsize=14)
plt.tight_layout()
plt.show()

# Final estimate with large sample
n = 1000000
x = np.random.uniform(-1, 1, n)
y = np.random.uniform(-1, 1, n)
inside = (x**2 + y**2) <= 1
pi_final = 4 * inside.sum() / n
print(f"Final π estimate (n=1,000,000): {pi_final:.6f}")
print(f"Actual π: {np.pi:.6f}")
print(f"Error: {abs(pi_final - np.pi):.6f}")
```

### সারসংক্ষেপ:
- প্রোবাবিলিটি মৌলিক কনসেপ্ট (Addition, Multiplication, Conditional)
- বিন্যাস ও সমাবেশ (Permutation & Combination)
- ডিসক্রিট ডিস্ট্রিবিউশন (Bernoulli, Binomial, Poisson)
- কন্টিনিউয়াস ডিস্ট্রিবিউশন (Normal, Exponential)
- কেন্দ্রীয় সীমা তত্ত্ব (CLT)
- বায়েস থিওরেম
- মন্টে কার্লো সিমুলেশন