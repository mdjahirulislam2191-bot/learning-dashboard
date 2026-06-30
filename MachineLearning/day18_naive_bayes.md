# Day 18: নাইভ বেইস
## Naive Bayes

### নাইভ বেইস কি?
নাইভ বেইস একটি probabilistic ক্লাসিফায়ার যা Bayes' Theorem-এর উপর ভিত্তি করে তৈরি। "Naive" কারণ এটি ধরে নেয় ফিচারগুলো একে অপরের থেকে স্বাধীন।

**Bayes' Theorem:** P(A|B) = P(B|A) * P(A) / P(B)

### ফাইন্যান্স উদাহরণ: ট্রেডিং সিগন্যাল ক্লাসিফিকেশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

# ট্রেডিং সিগন্যাল ডেটা
np.random.seed(42)
n = 2000

data = pd.DataFrame({
    'rsi': np.random.normal(50, 20, n),      # RSI ইন্ডিকেটর
    'macd_signal': np.random.randn(n),         # MACD সিগন্যাল
    'volume_ratio': np.random.exponential(1, n),  # ভলিউম রেশিও
    'price_change_pct': np.random.randn(n) * 2,   # প্রাইস পরিবর্তন
    'volatility_index': np.random.exponential(0.3, n)
})

# ট্রেডিং সিগন্যাল: Buy (1) / Sell (0)
z = (0.3 * (data['rsi'] < 30).astype(float) + 
     0.3 * (data['macd_signal'] > 0).astype(float) +
     0.2 * (data['volume_ratio'] > 1).astype(float) +
     0.2 * (data['price_change_pct'] > 0).astype(float) +
     np.random.randn(n) * 0.2)
data['buy_signal'] = (z > 0.5).astype(int)

print(f"Buy Signal Rate: {data['buy_signal'].mean():.2%}")

X = data.drop('buy_signal', axis=1)
y = data['buy_signal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Gaussian Naive Bayes
```python
gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred_gnb = gnb.predict(X_test)
y_prob_gnb = gnb.predict_proba(X_test)[:, 1]

print("\n📊 Gaussian Naive Bayes:")
print(f"Accuracy: {gnb.score(X_test, y_test):.4f}")
print(f"ROC-AUC:  {roc_auc_score(y_test, y_prob_gnb):.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred_gnb, target_names=['Sell', 'Buy']))
```

### Bernoulli Naive Bayes (বাইনারি ফিচারের জন্য)
```python
# ফিচার বাইনারি করা
data_binary = pd.DataFrame()
data_binary['rsi_low'] = (data['rsi'] < 30).astype(int)
data_binary['rsi_high'] = (data['rsi'] > 70).astype(int)
data_binary['macd_positive'] = (data['macd_signal'] > 0).astype(int)
data_binary['volume_high'] = (data['volume_ratio'] > 1.5).astype(int)
data_binary['price_up'] = (data['price_change_pct'] > 0).astype(int)

X_binary = data_binary
y_binary = data['buy_signal']

X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
    X_binary, y_binary, test_size=0.2, random_state=42
)

bnb = BernoulliNB()
bnb.fit(X_train_bin, y_train_bin)
print(f"\n📊 Bernoulli Naive Bayes Accuracy: {bnb.score(X_test_bin, y_test_bin):.4f}")
```

### Probability বিশ্লেষণ
```python
# ক্লাস প্রায়র এবং ফিচার প্রোবাবিলিটি
print(f"\n📈 Prior Probabilities:")
print(f"P(Sell): {gnb.class_prior_[0]:.4f}")
print(f"P(Buy):  {gnb.class_prior_[1]:.4f}")

print(f"\nFeature Means (by class):")
for i, label in enumerate(['Sell', 'Buy']):
    print(f"\n{label} class means:")
    for feat, mean in zip(X.columns, gnb.theta_[i]):
        print(f"  {feat}: {mean:.4f}")
```

### বিভিন্ন Naive Bayes তুলনা
```python
nb_models = {
    'Gaussian NB': GaussianNB(),
    'Bernoulli NB': BernoulliNB(),
    'Multinomial NB': MultinomialNB()
}

# মাল্টিনমিয়ালের জন্য নন-নেগেটিভ ডেটা
X_pos = np.abs(X)

for name, model in nb_models.items():
    if name == 'Multinomial NB':
        model.fit(X_pos[:len(X_train)], y_train)
        score = model.score(X_pos[len(X_train):], y_test)
    else:
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
    print(f"{name:20s}: {score:.4f}")
```

### Pros & Cons
```python
print("""
✅ Advantages:
- Fast training & prediction (linear time)
- ছোট ডেটায় ভালো কাজ করে
- High-dimensional ডেটা হ্যান্ডেল করে
- Probabilistic আউটপুট দেয়
- সহজ interpretability

❌ Disadvantages:
- Feature independence assumption (naive)
- ফিচার correlation পায় না
- Zero probability problem (Laplace smoothing দিয়ে সমাধান)
- Continuous features-এর জন্য Gaussian assumption
- Imbalanced ডেটায় bias

💡 Applications in Finance:
├── সেন্টিমেন্ট অ্যানালাইসিস (টেক্সট)
├── ফ্রড ডিটেকশন (real-time)
├── স্টক মুভমেন্ট প্রেডিকশন
├── ক্রেডিট স্কোরিং (baseline)
└── Risk classification
""")
```

### সারসংক্ষেপ
Naive Bayes দ্রুত, সহজ, এবং probabilistic ক্লাসিফায়ার। Feature independence assumption সত্ত্বেও অনেক ক্ষেত্রে ভালো কাজ করে। ফাইন্যান্সে text-based sentiment analysis, fraud detection, এবং real-time classification-এর জন্য আদর্শ।