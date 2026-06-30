"""
Day 9 — NumPy পরিচিতি (NumPy Introduction)
=============================================
লেখক: Jahirul Islam
বিষয়: NumPy দিয়ে অ্যারে, শেপ, ভেক্টরাইজড অপারেশন, মিন/ম্যাক্স/মিন/std
ফাইন্যান্স উদাহরণ: স্টক প্রাইস পরিসংখ্যান (Stock Price Statistics)

কি শিখবো:
  1. NumPy ইম্পোর্ট ও অ্যারে তৈরি
  2. অ্যারে শেপ, রিশেপ, মাত্রা
  3. ভেক্টরাইজড অপারেশন (দ্রুত গণিত)
  4. পরিসংখ্যান: গড়, মধ্যমা, স্ট্যান্ডার্ড ডেভিয়েশন
  5. ফাইন্যান্সিয়াল ডেটা নিয়ে কাজ
"""

import numpy as np

# ============================================================
# ১. NumPy অ্যারে তৈরি (Creating NumPy Arrays)
# ============================================================

print("=" * 60)
print("১. NumPy অ্যারে তৈরি")
print("=" * 60)

# লিস্ট থেকে অ্যারে
prices = [150.25, 152.10, 149.80, 151.40, 153.00, 148.75, 150.90]
price_array = np.array(prices)
print("স্টক প্রাইস অ্যারে:", price_array)
print("অ্যারের টাইপ:", type(price_array))
print("ডেটা টাইপ:", price_array.dtype)
print()

# ২D অ্যারে — একাধিক স্টকের প্রাইস (দিন × স্টক)
multi_stock = np.array([
    [150.25, 245.10, 89.50],   # দিন ১
    [152.10, 247.00, 88.75],   # দিন ২
    [149.80, 243.90, 90.10],   # দিন ৩
    [151.40, 248.50, 89.90],   # দিন ৪
])
print("মাল্টি-স্টক অ্যারে (দিন × স্টক):")
print(multi_stock)
print("মাত্রা (ndim):", multi_stock.ndim)
print("শেপ (shape):", multi_stock.shape)     # (4, 3) = 4 দিন, 3 টি স্টক
print("মোট এলিমেন্ট (size):", multi_stock.size)
print()

# বিশেষ অ্যারে তৈরি
zeros = np.zeros((3, 4), dtype=int)
print("zeros অ্যারে (3×4):\n", zeros)

ones = np.ones((2, 5))
print("ones অ্যারে (2×5):\n", ones)

# np.arange — রেঞ্জ
days = np.arange(1, 11)          # 1 থেকে 10
print("ট্রেডিং ডেস (arange):", days)

# np.linspace — সমান ব্যবধানে
prices_range = np.linspace(140, 160, 5)   # 140 থেকে 160 পর্যন্ত ৫টি সমান মান
print("সম্ভাব্য প্রাইস রেঞ্জ (linspace):", prices_range)
print()

# ============================================================
# ২. অ্যারে শেপ পরিবর্তন (Reshape & Shape Manipulation)
# ============================================================

print("=" * 60)
print("২. অ্যারে শেপ পরিবর্তন")
print("=" * 60)

data = np.arange(1, 13)          # 1..12
print("অরিজিনাল:", data, "→ শেপ:", data.shape)

# 12 এলিমেন্ট → 3×4 ম্যাট্রিক্সে রূপান্তর
reshaped = data.reshape(3, 4)
print("Reshaped (3×4):\n", reshaped)

# ফ্ল্যাট করুন (যেকোনো মাত্রা → ১D)
flat_again = reshaped.flatten()
print("Flat করা:", flat_again)
print()

# ============================================================
# ৩. ভেক্টরাইজড অপারেশন (Vectorized Operations)
# ============================================================

print("=" * 60)
print("৩. ভেক্টরাইজড অপারেশন (দ্রুত গণিত)")
print("=" * 60)

# স্টক প্রাইসে শতাংশ পরিবর্তন হিসাব
open_price = np.array([150.00, 152.00, 149.00, 151.00, 153.00])
close_price = np.array([152.10, 149.80, 151.40, 153.00, 148.75])

# ভেক্টরাইজড — লুপ লাগে না!
change = close_price - open_price
print("প্রাইস পরিবর্তন:", change)

pct_change = (close_price - open_price) / open_price * 100
print("শতাংশ পরিবর্তন:", np.round(pct_change, 2))

# ব্রডকাস্টিং — পুরো অ্যারেতে একটি সংখ্যা যোগ/গুণ করা
adjusted_prices = open_price + 5.00     # প্রতিটি প্রাইসে ৫ টাকা যোগ
print("অ্যাডজাস্টেড প্রাইস:", adjusted_prices)

# এলিমেন্ট-ওয়াইজ অপারেশন
high = np.array([153.00, 153.50, 150.00, 154.00, 154.50])
low  = np.array([149.00, 148.50, 148.00, 150.00, 147.50])
daily_range = high - low
print("ডেইলি রেঞ্জ (high - low):", daily_range)
print()

# ============================================================
# ৪. পরিসংখ্যান ফাংশন (Statistics — Mean, Median, Std, Min, Max)
# ============================================================

print("=" * 60)
print("৪. স্টক প্রাইস পরিসংখ্যান")
print("=" * 60)

stock_a = np.array([150.25, 152.10, 149.80, 151.40, 153.00, 148.75, 150.90])

mean_price = np.mean(stock_a)
median_price = np.median(stock_a)
std_price = np.std(stock_a)           # রিস্ক/ভোলাটিলিটি
var_price = np.var(stock_a)
min_price = np.min(stock_a)
max_price = np.max(stock_a)
price_range = max_price - min_price

print(f"স্টক A — ৭ দিনের প্রাইস ডেটা")
print(f"  গড় প্রাইস (Mean):          ${mean_price:.2f}")
print(f"  মধ্যমা (Median):           ${median_price:.2f}")
print(f"  স্ট্যান্ডার্ড ডেভিয়েশন:    ${std_price:.4f}  ← রিস্ক/ভোলাটিলিটি")
print(f"  ভ্যারিয়েন্স:               ${var_price:.4f}")
print(f"  সর্বনিম্ন (Min):           ${min_price:.2f}")
print(f"  সর্বোচ্চ (Max):            ${max_price:.2f}")
print(f"  রেঞ্জ:                    ${price_range:.2f}")
print()

# অক্ষ বরাবর পরিসংখ্যান (axis=0 → কলাম, axis=1 → সারি)
print("মাল্টি-স্টক অ্যারের কলাম (স্টক) অনুযায়ী পরিসংখ্যান:")
print(multi_stock)
col_means = np.mean(multi_stock, axis=0)      # প্রতি স্টকের গড়
col_stds  = np.std(multi_stock, axis=0)       # প্রতি স্টকের std
print("প্রতি স্টকের গড় প্রাইস:", np.round(col_means, 2))
print("প্রতি স্টকের ভোলাটিলিটি:", np.round(col_stds, 4))

row_means = np.mean(multi_stock, axis=1)      # প্রতি দিনের গড়
print("প্রতি দিনের গড় প্রাইস:", np.round(row_means, 2))
print()

# ============================================================
# ৫. ফাইন্যান্সিয়াল উদাহরণ: স্টক পোর্টফোলিও রিটার্ন
# ============================================================

print("=" * 60)
print("৫. পোর্টফোলিও রিটার্ন বিশ্লেষণ")
print("=" * 60)

# ধরি, পোর্টফোলিওতে ৩টি স্টক আছে
stock_returns = np.array([0.02, -0.01, 0.03])     # 2%, -1%, 3% ডেইলি রিটার্ন
weights = np.array([0.40, 0.35, 0.25])              # 40%, 35%, 25% ওয়েটেজ

# পোর্টফোলিও রিটার্ন = Σ (weight × return)
portfolio_return = np.sum(weights * stock_returns)
print(f"স্টক রিটার্ন:      {stock_returns}")
print(f"ওয়েটেজ:            {weights}")
print(f"পোর্টফোলিও রিটার্ন: {portfolio_return:.4f} ({portfolio_return*100:.2f}%)")
print()

# একাধিক দিনের রিটার্ন
daily_returns = np.array([
    [0.02, -0.01, 0.03],    # দিন ১
    [0.01,  0.00, 0.02],    # দিন ২
    [-0.01, 0.02, 0.01],    # দিন ৩
])
portfolio_daily = np.dot(daily_returns, weights)  # ম্যাট্রিক্স গুণ
print("ডেইলি পোর্টফোলিও রিটার্ন:")
for i, ret in enumerate(portfolio_daily, 1):
    print(f"  দিন {i}: {ret*100:.2f}%")
print(f"গড় ডেইলি রিটার্ন: {np.mean(portfolio_daily)*100:.2f}%")
print(f"রিটার্নের Std:     {np.std(portfolio_daily)*100:.2f}%  (পোর্টফোলিও রিস্ক)")
print()

# ============================================================
# ৬. অ্যারে স্লাইসিং ও ইনডেক্সিং (Slicing & Indexing)
# ============================================================

print("=" * 60)
print("৬. অ্যারে স্লাইসিং ও ইনডেক্সিং")
print("=" * 60)

prices_5d = np.array([150, 152, 149, 151, 153])
print("সব প্রাইস:", prices_5d)
print("প্রথম ৩ দিন:", prices_5d[:3])        # স্লাইস
print("শেষ ২ দিন:", prices_5d[-2:])
print("২য় থেকে ৪র্থ:", prices_5d[1:4])

# ২D অ্যারে স্লাইসিং
print("\nমাল্টি-স্টক অ্যারে:")
print(multi_stock)
print("প্রথম ২ দিন, সব স্টক:\n", multi_stock[:2, :])
print("সব দিন, প্রথম ২ স্টক:\n", multi_stock[:, :2])
print("২য় থেকে ৩য় দিন, ১ম ও ৩য় স্টক:\n", multi_stock[1:3, [0, 2]])
print()

# ============================================================
# ৭. বুলিয়ান ইনডেক্সিং (Boolean Indexing / Filtering)
# ============================================================

print("=" * 60)
print("৭. বুলিয়ান ইনডেক্সিং (ফিল্টারিং)")
print("=" * 60)

# যে দিনগুলিতে প্রাইস ১৫০-এর উপরে ছিল
above_150 = stock_a[stock_a > 150]
print("১৫০-এর উপরে প্রাইস:", above_150)
print("সংখ্যা:", len(above_150))

# লজিক্যাল অপারেটর (&, |)
between_149_152 = stock_a[(stock_a >= 149) & (stock_a <= 152)]
print("১৪৯-১৫২ রেঞ্জের প্রাইস:", between_149_152)
print()

# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 60)
print("🎯 প্র্যাকটিস টাস্ক")
print("=" * 60)
print("""
টাস্ক ১: ৩টি স্টকের ৫ দিনের প্রাইস নিয়ে 2D অ্যারে তৈরি করুন।
         প্রতিটি স্টকের গড়, মিন, ম্যাক্স, এবং std বের করুন।
         
টাস্ক ২: np.random.normal() ব্যবহার করে ১০০০টি ডেইলি রিটার্ন
         জেনারেট করুন (গড়=0.001, std=0.02)। এদের উপর
         পরিসংখ্যান (mean, std, min, max) বের করুন এবং
         কতগুলি রিটার্ন 0-এর উপরে তা গণনা করুন।
         
টাস্ক ৩: আপনার পোর্টফোলিওতে ৪টি স্টক আছে (ওয়েটেজ: 25% করে)।
         ১০ দিনের ডেইলি রিটার্ন জেনারেট করে পোর্টফোলিও
         রিটার্ন এবং রিস্ক (std) বের করুন।
""")
