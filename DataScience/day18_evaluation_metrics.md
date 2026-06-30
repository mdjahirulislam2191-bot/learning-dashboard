# Day 18: ইভালুয়েশন মেট্রিক্স — R², MSE, MAE
## Evaluation Metrics: R², MSE, MAE

### ইভালুয়েশন মেট্রিক্স কী?
রিগ্রেশন মডেলের পারফরম্যান্স বোঝার জন্য বিভিন্ন মেট্রিক্স ব্যবহার করা হয়। এগুলো বলে দেয় মডেলের প্রেডিকশন কতটা নির্ভুল।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             mean_absolute_percentage_error, explained_variance_score)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# বিভিন্ন পরিস্থিতিতে সিমুলেশন
n = 1000
perfect_y = np.random.randn(n)  # পারফেক্ট ডেটা
noisy_y = perfect_y + np.random.normal(0, 2, n)  # নয়জি ডেটা
random_y = np.random.randn(n)  # এলোমেলো ডেটা
perfect_pred = perfect_y  # পারফেক্ট প্রেডিকশন
biased_pred = perfect_y + 0.5  # বায়াসড প্রেডিকশন
noisy_pred = perfect_y + np.random.normal(0, 1, n)  # মোটামুটি প্রেডিকশন
```

### মেজার্স অফ এরর:

#### ১. MAE (Mean Absolute Error):
```python
print("\n=== MAE — Mean Absolute Error ===")

def mae_manual(y_true, y_pred):
    """MAE ম্যানুয়ালি"""
    return np.mean(np.abs(y_true - y_pred))

mae_perfect = mae_manual(perfect_y, perfect_pred)
mae_biased = mae_manual(perfect_y, biased_pred)
mae_noisy = mae_manual(perfect_y, noisy_pred)
mae_random = mae_manual(perfect_y, random_y)

print(f"পারফেক্ট প্রেডিকশন MAE: {mae_perfect:.4f}")
print(f"বায়াসড প্রেডিকশন MAE: {mae_biased:.4f}")
print(f"নয়জি প্রেডিকশন MAE: {mae_noisy:.4f}")
print(f"এলোমেলো প্রেডিকশন MAE: {mae_random:.4f}")

# স্কলার্ন ফাংশন দিয়ে যাচাই
print(f"\nMAE (স্কলার্ন): {mean_absolute_error(perfect_y, noisy_pred):.4f}")
print(f"MAE (ম্যানুয়াল): {mae_manual(perfect_y, noisy_pred):.4f}")
```

#### ২. MSE (Mean Squared Error):
```python
print("\n=== MSE — Mean Squared Error ===")

def mse_manual(y_true, y_pred):
    """MSE ম্যানুয়ালি"""
    return np.mean((y_true - y_pred) ** 2)

mse_perfect = mse_manual(perfect_y, perfect_pred)
mse_biased = mse_manual(perfect_y, biased_pred)
mse_noisy = mse_manual(perfect_y, noisy_pred)
mse_random = mse_manual(perfect_y, random_y)

print(f"পারফেক্ট প্রেডিকশন MSE: {mse_perfect:.4f}")
print(f"বায়াসড প্রেডিকশন MSE: {mse_biased:.4f}")
print(f"নয়জি প্রেডিকশন MSE: {mse_noisy:.4f}")
print(f"এলোমেলো প্রেডিকশন MSE: {mse_random:.4f}")

# MSE বনাম MAE তুলনা
print(f"\nনয়জি ডেটার জন্য:")
print(f"  MAE: {mae_noisy:.4f}")
print(f"  MSE: {mse_noisy:.4f}")
print(f"  RMSE: {np.sqrt(mse_noisy):.4f}")

print(f"\n❌ আউটলায়ার সহ: (MSE বেশি প্রভাবিত)")
y_with_outlier = noisy_pred.copy()
y_with_outlier[0] = 100  # একটা বড় আউটলায়ার
print(f"  MSE (আউটলায়ার সহ): {mse_manual(perfect_y, y_with_outlier):.4f}")
print(f"  MAE (আউটলায়ার সহ): {mae_manual(perfect_y, y_with_outlier):.4f}")
print(f"  → MSE আউটলায়ার দ্বারা বেশি প্রভাবিত হয়!")
```

#### ৩. RMSE (Root Mean Squared Error):
```python
print("\n=== RMSE — Root Mean Squared Error ===")

rmse_perfect = np.sqrt(mse_perfect)
rmse_biased = np.sqrt(mse_biased)
rmse_noisy = np.sqrt(mse_noisy)
rmse_random = np.sqrt(mse_random)

print(f"পারফেক্ট প্রেডিকশন RMSE: {rmse_perfect:.4f}")
print(f"বায়াসড প্রেডিকশন RMSE: {rmse_biased:.4f}")
print(f"নয়জি প্রেডিকশন RMSE: {rmse_noisy:.4f}")
print(f"এলোমেলো প্রেডিকশন RMSE: {rmse_random:.4f}")

print(f"\nRMSE vs MAE:")
print(f"  RMSE: {rmse_noisy:.4f}")
print(f"  MAE: {mae_noisy:.4f}")
print(f"  অনুপাত (RMSE/MAE): {rmse_noisy/mae_noisy:.4f} (১ এর কাছাকাছি হলে কম ভ্যারিয়েন্স)")
```

#### ৪. R² Score (Coefficient of Determination):
```python
print("\n=== R² Score (Coefficient of Determination) ===")

def r2_manual(y_true, y_pred):
    """R² ম্যানুয়ালি"""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

r2_perfect = r2_manual(perfect_y, perfect_pred)
r2_biased = r2_manual(perfect_y, biased_pred)
r2_noisy = r2_manual(perfect_y, noisy_pred)
r2_random = r2_manual(perfect_y, random_y)

print(f"পারফেক্ট প্রেডিকশন R²: {r2_perfect:.4f}")
print(f"বায়াসড প্রেডিকশন R²: {r2_biased:.4f}")
print(f"নয়জি প্রেডিকশন R²: {r2_noisy:.4f}")
print(f"এলোমেলো প্রেডিকশন R²: {r2_random:.4f}")

# স্কলার্ন ফাংশন
print(f"\nR² (স্কলার্ন): {r2_score(perfect_y, noisy_pred):.4f}")
print(f"R² (ম্যানুয়াল): {r2_manual(perfect_y, noisy_pred):.4f}")
```

#### ৫. অ্যাডজাস্টেড R²:
```python
print("\n=== অ্যাডজাস্টেড R² ===")

def adjusted_r2(r2, n, p):
    """অ্যাডজাস্টেড R² (ফিচার সংখ্যার জন্য পেনাল্টি)"""
    return 1 - ((1 - r2) * (n - 1) / (n - p - 1))

# বিভিন্ন সংখ্যক ফিচারের জন্য তুলনা
p_values = [1, 5, 10, 20, 50, 100]
n = 1000

print(f"n={n}, R²=0.85 হলে:")
for p in p_values:
    adj_r2 = adjusted_r2(0.85, n, p)
    print(f"  ফিচার={p:3d}: অ্যাডজাস্টেড R² = {adj_r2:.4f} {'⚠️ ওভারফিট!' if adj_r2 < 0.80 else ''}")
```

#### ৬. MAPE (Mean Absolute Percentage Error):
```python
print("\n=== MAPE — Mean Absolute Percentage Error ===")

def mape_manual(y_true, y_pred):
    """MAPE ম্যানুয়ালি"""
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# নন-জিরো ডেটা দরকার
y_nonzero = np.abs(perfect_y) + 1
pred_nonzero = y_nonzero + np.random.normal(0, 0.5, n)

mape_val = mape_manual(y_nonzero, pred_nonzero)
print(f"MAPE: {mape_val:.2f}%")
print(f"স্কলার্ন MAPE: {mean_absolute_percentage_error(y_nonzero, pred_nonzero)*100:.2f}%")
print(f"(গড়ে প্রেডিকশন {mape_val:.2f}% ভুল)")
```

### বিভিন্ন সিনারিওতে মেট্রিক্স তুলনা:
```python
print("\n=== বিভিন্ন সিনারিওতে মেট্রিক্স তুলনা ===")

scenarios = {
    'পারফেক্ট': (perfect_y, perfect_pred),
    'বায়াসড': (perfect_y, biased_pred),
    'নয়জি': (perfect_y, noisy_pred),
    'এলোমেলো': (perfect_y, random_y),
}

results = []
for name, (true, pred) in scenarios.items():
    mae = mean_absolute_error(true, pred)
    mse = mean_squared_error(true, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(true, pred)
    results.append({'সিনারিও': name, 'MAE': f'{mae:.4f}', 'MSE': f'{mse:.4f}',
                    'RMSE': f'{rmse:.4f}', 'R²': f'{r2:.4f}'})

print(pd.DataFrame(results).to_string(index=False))
```

### রিয়েল-ওয়ার্ল্ড উদাহরণ: হাউস প্রাইস প্রেডিকশন:
```python
print("\n=== রিয়েল-ওয়ার্ল্ড উদাহরণ ===")

# বাস্তব ডেটাসেট
np.random.seed(42)
n = 300

true_price = 50000 + np.random.randn(n) * 50000

# তিনটি ভিন্ন মডেলের প্রেডিকশন
model_a_pred = true_price + np.random.normal(0, 5000, n)  # সঠিক
model_b_pred = true_price + 10000 + np.random.normal(0, 10000, n)  # বায়াসড + ভ্যারিয়েন্স
model_c_pred = true_price + np.random.normal(0, 25000, n)  # হাই ভ্যারিয়েন্স

models = {
    'মডেল A (সঠিক)': model_a_pred,
    'মডেল B (বায়াসড)': model_b_pred,
    'মডেল C (ভ্যারিয়েন্স বেশি)': model_c_pred
}

for name, pred in models.items():
    mae = mean_absolute_error(true_price, pred)
    mse = mean_squared_error(true_price, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(true_price, pred)
    mape = mean_absolute_percentage_error(true_price, pred) * 100
    print(f"\n{name}:")
    print(f"  MAE: {mae:,.2f}")
    print(f"  MSE: {mse:,.2f}")
    print(f"  RMSE: {rmse:,.2f}")
    print(f"  R²: {r2:.4f}")
    print(f"  MAPE: {mape:.2f}%")
```

### মেট্রিক্স ভিজুয়ালাইজেশন:
```python
print("\n=== ভিজুয়ালাইজেশন ===")

plt.figure(figsize=(15, 10))

# ১. পারফেক্ট মডেল
plt.subplot(2, 3, 1)
plt.scatter(true_price, model_a_pred, alpha=0.5)
plt.plot([true_price.min(), true_price.max()], [true_price.min(), true_price.max()], 'r--')
plt.xlabel('প্রকৃত দাম')
plt.ylabel('প্রেডিক্টেড দাম')
plt.title(f'মডেল A (R²={r2_score(true_price, model_a_pred):.3f})')

# ২. বায়াসড মডেল
plt.subplot(2, 3, 2)
plt.scatter(true_price, model_b_pred, alpha=0.5)
plt.plot([true_price.min(), true_price.max()], [true_price.min(), true_price.max()], 'r--')
plt.xlabel('প্রকৃত দাম')
plt.ylabel('প্রেডিক্টেড দাম')
plt.title(f'মডেল B (R²={r2_score(true_price, model_b_pred):.3f})')

# ৩. ভ্যারিয়েন্স বেশি
plt.subplot(2, 3, 3)
plt.scatter(true_price, model_c_pred, alpha=0.5)
plt.plot([true_price.min(), true_price.max()], [true_price.min(), true_price.max()], 'r--')
plt.xlabel('প্রকৃত দাম')
plt.ylabel('প্রেডিক্টেড দাম')
plt.title(f'মডেল C (R²={r2_score(true_price, model_c_pred):.3f})')

# ৪. রেসিডুয়ালস এ
plt.subplot(2, 3, 4)
plt.scatter(model_a_pred, true_price - model_a_pred, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('প্রেডিক্টেড')
plt.ylabel('রেসিডুয়াল')
plt.title('মডেল A রেসিডুয়াল')
plt.ylim(-40000, 40000)

# ৫. রেসিডুয়ালস বি
plt.subplot(2, 3, 5)
plt.scatter(model_b_pred, true_price - model_b_pred, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('প্রেডিক্টেড')
plt.ylabel('রেসিডুয়াল')
plt.title('মডেল B রেসিডুয়াল')
plt.ylim(-40000, 40000)

# ৬. মেট্রিক্স তুলনা
plt.subplot(2, 3, 6)
metrics = ['MAE', 'RMSE', 'R²']
x = np.arange(len(metrics))
width = 0.25
for i, (name, pred) in enumerate(models.items()):
    values = [mean_absolute_error(true_price, pred),
              np.sqrt(mean_squared_error(true_price, pred)),
              r2_score(true_price, pred)]
    if i == 2:  # R² এর জন্য স্কেল
        values[2] = r2_score(true_price, pred)
    plt.bar(x + i*width, values[:3], width, label=name)
plt.xticks(x + width, metrics)
plt.title('মেট্রিক্স তুলনা')
plt.legend()

plt.tight_layout()
plt.savefig('evaluation_metrics.png')
plt.show()
print("মেট্রিক্স ভিজুয়ালাইজেশন সেভ করা হয়েছে!")
```

### মেট্রিক্স সিলেকশন গাইড:
```python
print("\n=== মেট্রিক্স সিলেকশন গাইড ===")

guide = pd.DataFrame({
    'মেট্রিক': ['MAE', 'MSE', 'RMSE', 'R²', 'অ্যাডজাস্টেড R²', 'MAPE'],
    'সূত্র': ['Σ|yi-ŷi|/n', 'Σ(yi-ŷi)²/n', '√MSE', '1-SSres/SStot', '1-(1-R²)(n-1)/(n-p-1)', 'Σ|(yi-ŷi)/yi|×100/n'],
    'ব্যবহার': [
        'ইন্টারপ্রেট করা সহজ, সব ত্রুটিকে সমান গুরুত্ব দেয়',
        'বড় ত্রুটিকে বেশি পেনাল্টাইজ করে, আউটলায়ার সংবেদনশীল',
        'MAE এর মতো ইন্টারপ্রেটেবল, MSE এর মতো বড় ত্রুটিকে পেনাল্টাইজ করে',
        'মডেল কত % ভ্যারিয়েন্স ব্যাখ্যা করে (0-1)',
        'অপ্রয়োজনীয় ফিচারের জন্য পেনাল্টি দেয়',
        'পার্সেন্টেজে ত্রুটি, বিভিন্ন স্কেলের মডেল তুলনার জন্য'
    ],
    'ইউনিট': ['টার্গেট ইউনিট', 'স্কোয়ারড ইউনিট', 'টার্গেট ইউনিট', 'ইউনিটলেস', 'ইউনিটলেস', '%']
})
print(guide.to_string(index=False))
print("\n📌 মনে রাখবেন:")
print("  ➤ R² সবসময় বাড়ে যখন নতুন ফিচার যোগ করি (এমনকি অপ্রয়োজনীয় হলেও)")
print("  ➤ অ্যাডজাস্টেড R² ফিচার সংখ্যার জন্য পেনাল্টি দেয়")
print("  ➤ MSE > MAE (যখন ত্রুটি > ১), কারণ MSE ত্রুটিকে স্কোয়ার করে")
print("  ➤ MAE ≥ RMSE ≥ MSE (সাধারণত)")
print("  ➤ MAPE টার্গেট ভ্যারিয়েবল জিরো হলে ব্যবহার করা যায় না")
```

### রেসিডুয়াল অ্যানালাইসিস:
```python
print("\n=== রেসিডুয়াল অ্যানালাইসিস ===")

residuals = true_price - model_a_pred

print(f"রেসিডুয়ালের পরিসংখ্যান:")
print(f"  মিন: {np.mean(residuals):.4f}")
print(f"  স্টিড: {np.std(residuals):.4f}")
print(f"  স্কিউনেস: {pd.Series(residuals).skew():.4f}")
print(f"  কুরটোসিস: {pd.Series(residuals).kurtosis():.4f}")
print(f"  মিন (এবসোলিউট): {np.mean(np.abs(residuals)):.4f}")
print(f"  ৯৫% রেসিডুয়াল রেঞ্জ: ({np.percentile(residuals, 2.5):.2f}, {np.percentile(residuals, 97.5):.2f})")

# বায়াস চেক
print(f"\nবায়াস চেক:")
print(f"  গড় রেসিডুয়াল: {np.mean(residuals):.4f} (০ এর কাছাকাছি হলে আনবায়াসড)")
bias_threshold = 0.1 * np.std(residuals)
if abs(np.mean(residuals)) < bias_threshold:
    print(f"  ✅ মডেল আনবায়াসড (গড় রেসিডুয়াল {bias_threshold:.4f} এর মধ্যে)")
else:
    print(f"  ⚠️ মডেলে বায়াস থাকতে পারে!")
```

### সারাংশ:
- **MAE**: সহজবোধ্য, সব ত্রুটিকে সমান গুরুত্ব দেয়
- **MSE**: বড় ত্রুটিকে বেশি পেনাল্টাইজ করে (স্কোয়ার করার কারণে)
- **RMSE**: MSE এর মতো কিন্তু আসল ইউনিটে থাকে
- **R²**: মডেলের ব্যাখ্যামূলক ক্ষমতা (০ = খারাপ, ১ = পারফেক্ট)
- **অ্যাডজাস্টেড R²**: ফিচার সংখ্যার জন্য পেনাল্টি দেয়
- **MAPE**: শতাংশে ত্রুটি দেখায়, বিভিন্ন ডেটাসেটের মধ্যে তুলনার জন্য ভালো
- **মেট্রিক নির্বাচন** সমস্যার প্রকৃতির উপর নির্ভর করে — কোন একক মেট্রিক সব পরিস্থিতিতে সেরা নয়
