# Day 04: অ্যাক্টিভেশন ফাংশন (Activation Functions) ⚡

## অ্যাক্টিভেশন ফাংশন কী?
অ্যাক্টিভেশন ফাংশন নিউরনের আউটপুট নির্ধারণ করে। এটি নন-লিনিয়ারিটি যোগ করে, যা ডিপ নেটওয়ার্ককে জটিল প্যাটার্ন শিখতে সাহায্য করে।

## প্রধান অ্যাক্টিভেশন ফাংশন

### 1. Sigmoid (Logistic)
```
σ(x) = 1 / (1 + e^(-x))
রেঞ্জ: (0, 1)
```

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

x = np.linspace(-10, 10, 100)
plt.plot(x, sigmoid(x), label='Sigmoid')
plt.plot(x, sigmoid_derivative(x), label='Derivative', linestyle='--')
plt.legend(), plt.grid(True), plt.title('Sigmoid Activation')
plt.show()

# ফিন্যান্স: সিগময়েড প্রোবাবিলিটি আউটপুট
# যেমন: প্রাইস আপ হওয়ার প্রবাবিলিটি
z = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
probs = sigmoid(z)
print(f"লগিটস: {z}")
print(f"প্রোবাবিলিটিস: {np.round(probs, 4)}")
```

### 2. Tanh (Hyperbolic Tangent)
```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
রেঞ্জ: (-1, 1)
```

```python
def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1 - np.tanh(x)**2

# ফিন্যান্স: ফিচার নরমালাইজেশনের জন্য ভালো
returns = np.array([-0.03, -0.01, 0.0, 0.01, 0.03])
normalized = tanh(returns * 100)  # রিটার্নকে (-1,1) এ ম্যাপ
print(f"রিটার্ন: {returns}")
print(f"Tanh Normalized: {np.round(normalized, 4)}")
```

### 3. ReLU (Rectified Linear Unit)
```
ReLU(x) = max(0, x)
রেঞ্জ: [0, ∞)
```

```python
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

# ফিন্যান্স: ReLU নেগেটিভ প্রাইস পরিবর্তন ফিল্টার করতে পারে
price_changes = np.array([-5.2, -2.1, 0.0, 1.5, 3.8, -0.5])
gains_only = relu(price_changes)
print(f"প্রাইস পরিবর্তন: {price_changes}")
print(f"শুধু গেইন (ReLU): {gains_only}")
```

### 4. Leaky ReLU
```
LeakyReLU(x) = max(αx, x) যেখানে α = 0.01
```

```python
def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

# Dying ReLU সমস্যা সমাধান করে
```

### 5. Softmax (মাল্টি-ক্লাস)
```
softmax(xᵢ) = e^xᵢ / Σ(e^xⱼ)
রেঞ্জ: (0, 1), সাম = 1
```

```python
def softmax(x):
    e_x = np.exp(x - np.max(x))  # numerically stable
    return e_x / e_x.sum()

# ফিন্যান্স: পোর্টফোলিও অ্যালোকেশন
logits = np.array([2.0, 1.0, 0.5, 0.1])  # ৪টি অ্যাসেটের স্কোর
weights = softmax(logits)
assets = ['Stock', 'Bond', 'Gold', 'Cash']
for asset, w in zip(assets, weights):
    print(f"{asset}: {w:.2%}")
print(f"সাম: {weights.sum():.2f}")  # ১.০
```

## পাইথনে সব অ্যাক্টিভেশন ফাংশন
```python
import torch.nn as nn

# PyTorch অ্যাক্টিভেশন
activations = {
    'Sigmoid': nn.Sigmoid(),
    'Tanh': nn.Tanh(),
    'ReLU': nn.ReLU(),
    'LeakyReLU': nn.LeakyReLU(0.01),
    'Softmax': nn.Softmax(dim=0)
}

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
for name, act in activations.items():
    print(f"{name}: {act(x)}")
```

## অ্যাক্টিভেশন ফাংশন তুলনা
```python
import numpy as np

class ActivationComparison:
    @staticmethod
    def all_activations(x):
        return {
            'Sigmoid': 1 / (1 + np.exp(-x)),
            'Tanh': np.tanh(x),
            'ReLU': np.maximum(0, x),
            'Leaky ReLU': np.where(x > 0, x, 0.01 * x),
            'ELU': np.where(x > 0, x, np.exp(x) - 1)
        }
    
    @staticmethod
    def recommend_for_finance(task):
        recommendations = {
            'binary_classification': 'Sigmoid (আউটপুট লেয়ার)',
            'regression': 'Linear (আউটপুট) + ReLU (হিডেন)',
            'multi_class': 'Softmax (আউটপুট)',
            'time_series': 'Tanh বা ReLU',
            'portfolio_weights': 'Softmax'
        }
        return recommendations.get(task, 'ReLU (ডিফল্ট)')

print(ActivationComparison.recommend_for_finance('time_series'))
```

## সারসংক্ষেপ
| ফাংশন | রেঞ্জ | ব্যবহার |
|--------|-------|---------|
| Sigmoid | (0,1) | বাইনারি ক্লাসিফিকেশন আউটপুট |
| Tanh | (-1,1) | RNN, সেন্টারেড ডেটা |
| ReLU | [0,∞) | CNN, ANN (ডিফল্ট) |
| Leaky ReLU | (-∞,∞) | Dying ReLU প্রতিরোধ |
| Softmax | (0,1) | মাল্টি-ক্লাস, পোর্টফোলিও |
| Linear | (-∞,∞) | রিগ্রেশন আউটপুট|

- অ্যাক্টিভেশন ফাংশন নন-লিনিয়ারিটি যোগ করে
- ফিন্যান্সে: সিগময়েড → প্রোবাবিলিটি, Softmax → অ্যাসেট অ্যালোকেশন, ReLU → ফিচার এক্সট্র্যাকশন