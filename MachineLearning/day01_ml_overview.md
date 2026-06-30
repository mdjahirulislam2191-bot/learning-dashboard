# Day 01: মেশিন লার্নিং এর ওভারভিউ
## Machine Learning Overview

### মেশিন লার্নিং কি?
মেশিন লার্নিং (ML) হল কৃত্রিম বুদ্ধিমত্তার একটি শাখা যেখানে কম্পিউটারকে ডেটা থেকে শেখানো হয়, স্পষ্টভাবে প্রোগ্রাম না করেই। ML মডেলগুলি প্যাটার্ন শনাক্ত করে এবং সিদ্ধান্ত নেয়।

### কেন ফাইন্যান্স এবং ডেটা অ্যানালিস্টদের জন্য ML গুরুত্বপূর্ণ?
- **ফ্রড ডিটেকশন**: জালিয়াতি লেনদেন শনাক্তকরণ
- **স্টক প্রেডিকশন**: শেয়ার বাজার পূর্বাভাস
- **ক্রেডিট রিস্ক অ্যাসেসমেন্ট**: ঋণ ঝুঁকি মূল্যায়ন
- **কাস্টমার সেগমেন্টেশন**: গ্রাহক বিভাজন
- **পোর্টফোলিও অপ্টিমাইজেশন**: বিনিয়োগ পোর্টফোলিও সর্বোত্তমকরণ

### ML এর প্রকারভেদ
1. **Supervised Learning (পর্যবেক্ষিত শিক্ষা)**: লেবেলযুক্ত ডেটা থেকে শেখে
2. **Unsupervised Learning (অপর্যবেক্ষিত শিক্ষা)**: লেবেলবিহীন ডেটা থেকে শেখে
3. **Reinforcement Learning (পুনর্বহন শিক্ষা)**: পরিবেশের সাথে মিথস্ক্রিয়া করে শেখে

### Python ML Stack
```python
# প্রয়োজনীয় লাইব্রেরি
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("ML Stack প্রস্তুত!")
```

### একটি সাধারণ উদাহরণ: সিউডো-ফাইন্যান্স ডেটা
```python
# ফাইন্যান্স ডেটা জেনারেশন
np.random.seed(42)
n_samples = 1000

# স্টক রিটার্ন এবং ভোলাটিলিটি ডেটা
returns = np.random.randn(n_samples) * 0.02 + 0.001
volume = np.random.randint(100000, 10000000, n_samples)
volatility = np.abs(np.random.randn(n_samples)) * 0.5

data = pd.DataFrame({
    'returns': returns,
    'volume': volume,
    'volatility': volatility
})

print(data.head())
print(f"ডেটার আকৃতি: {data.shape}")
```

### ML প্রজেক্ট লাইফসাইকেল
1. **Problem Definition** - সমস্যা সংজ্ঞায়ন
2. **Data Collection** - ডেটা সংগ্রহ
3. **Data Preprocessing** - ডেটা প্রিপ্রসেসিং
4. **Model Selection** - মডেল নির্বাচন
5. **Training** - প্রশিক্ষণ
6. **Evaluation** - মূল্যায়ন
7. **Deployment** - স্থাপন

### সারসংক্ষেপ
আজ আমরা ML এর বেসিক ধারণা, ফাইন্যান্সে এর প্রয়োগ, এবং Python ML স্ট্যাক সম্পর্কে জানলাম। পরবর্তী ক্লাসে আমরা Supervised এবং Unsupervised Learning নিয়ে বিস্তারিত আলোচনা করব।