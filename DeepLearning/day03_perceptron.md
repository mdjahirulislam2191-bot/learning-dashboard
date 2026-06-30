# Day 03: পারসেপট্রন (Perceptron) 🔬

## পারসেপট্রন কী?
পারসেপট্রন হল সবচেয়ে সহজ কৃত্রিম নিউরন যা ১৯৫৮ সালে Frank Rosenblatt আবিষ্কার করেন। এটি বাইনারি ক্লাসিফিকেশন করে।

### পারসেপট্রন অ্যালগরিদম
```
1. ওয়েট ও বায়াস ইনিশিয়ালাইজ
2. প্রতিটি ট্রেনিং উদাহরণের জন্য:
   a. প্রেডিকশন = sign(Σ(wᵢ·xᵢ) + b)
   b. যদি প্রেডিকশন ≠ টার্গেট:
      wᵢ = wᵢ + η · (target - prediction) · xᵢ
      b = b + η · (target - prediction)
3. কনভার্জেন্স পর্যন্ত পুনরাবৃত্তি
```

## পারসেপট্রন ইমপ্লিমেন্টেশন
```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.loss_history = []
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iters):
            n_errors = 0
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = self._step_function(linear_output)
                
                # আপডেট রুল
                update = self.lr * (y[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update
                n_errors += int(update != 0)
            
            self.loss_history.append(n_errors / n_samples)
            if n_errors == 0:
                break
    
    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return self._step_function(linear_output)
    
    def _step_function(self, x):
        return np.where(x >= 0, 1, 0)

# টেস্ট ডেটা (স্টক আপ/ডাউন প্রেডিকশন সিমুলেশন)
np.random.seed(42)
# ফিচার: ভোলাটিলিটি, P/E, SMA_20, Volume_change
X = np.random.randn(200, 4)
# টার্গেট: ১ = স্টক উপরে যাবে, ০ = নিচে যাবে
y = (X[:, 0] + X[:, 1] - X[:, 2] + np.random.randn(200) * 0.3 > 0).astype(int)

# ট্রেনিং
p = Perceptron(learning_rate=0.01, n_iters=100)
p.fit(X, y)

print(f"লার্নড ওয়েটস: {p.weights}")
print(f"লার্নড বায়াস: {p.bias}")
print(f"অ্যাকুরেসি: {np.mean(p.predict(X) == y):.2%}")
```

## AND/OR Gate পারসেপট্রন
```python
# AND Gate
X_and = np.array([[0,0], [0,1], [1,0], [1,1]])
y_and = np.array([0, 0, 0, 1])

p_and = Perceptron(lr=0.1, n_iters=10)
p_and.fit(X_and, y_and)
print(f"AND Gate: {p_and.predict(X_and)} (expected: {y_and})")

# OR Gate
y_or = np.array([0, 1, 1, 1])
p_or = Perceptron(lr=0.1, n_iters=10)
p_or.fit(X_or, y_or)
print(f"OR Gate: {p_or.predict(X_or)} (expected: {y_or})")
```

## ফিন্যান্সিয়াল অ্যাপ্লিকেশন: বাইনারি মার্কেট প্রেডিকশন
```python
import yfinance as yf

# রিল স্টক ডেটা
ticker = "GOOGL"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

# ফিচার তৈরি
data['Return'] = data['Close'].pct_change()
data['Volatility'] = data['Return'].rolling(5).std()
data['SMA_5'] = data['Close'].rolling(5).mean()
data['Price_SMA_Ratio'] = data['Close'] / data['SMA_5']
data['Target'] = (data['Return'].shift(-1) > 0).astype(int)

data_clean = data.dropna()
features = data_clean[['Volatility', 'Price_SMA_Ratio', 'Return']].values
targets = data_clean['Target'].values

# পারসেপট্রন ট্রেনিং
perc = Perceptron(learning_rate=0.001, n_iters=100)
perc.fit(features, targets)
print(f"মার্কেট প্রেডিকশন অ্যাকুরেসি: {np.mean(perc.predict(features) == targets):.2%}")
print(f"লার্নড ওয়েটস (Volatility, Price/SMA, Return): {perc.weights}")
```

## পারসেপট্রনের সীমাবদ্ধতা
- শুধুমাত্র **লিনিয়ারলি সেপারেবল** ডেটা分類 করতে পারে
- XOR সমস্যা সমাধান করতে পারে না
- স্টেপ ফাংশন ডিফারেনশিয়েবল নয় → ব্যাকপ্রোপাগেশন সম্ভব নয়

```python
# XOR সমস্যা (পারসেপট্রন পারেনা)
X_xor = np.array([[0,0], [0,1], [1,0], [1,1]])
y_xor = np.array([0, 1, 1, 0])

p_xor = Perceptron(lr=0.1, n_iters=100)
p_xor.fit(X_xor, y_xor)
print(f"XOR প্রেডিকশন: {p_xor.predict(X_xor)}")
print(f"XOR Actual:    {y_xor}")
print(f"=> পারসেপট্রন XOR শিখতে পারেনা!")
```

## সারসংক্ষেপ
- পারসেপট্রন = সহজ বাইনারি ক্লাসিফায়ার
- লিনিয়ার ডিসিশন বাউন্ডারি তৈরি করে
- শুধুমাত্র লিনিয়ার সমস্যা সমাধান করতে পারে
- মাল্টি-লেয়ার পারসেপট্রন (MLP) XOR-এর মতো জটিল সমস্যা সমাধান করতে পারে
- ফিন্যান্সে: সিম্পল ডিরেকশনাল প্রেডিকশন, ক্রেডিট স্কোরিং