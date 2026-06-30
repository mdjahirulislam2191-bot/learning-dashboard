# Day 05: ব্যাকপ্রোপাগেশন (Backpropagation) 🔄

## ব্যাকপ্রোপাগেশন কী?
ব্যাকপ্রোপাগেশন হল ডিপ লার্নিং-এর মূল অ্যালগরিদম যা নেটওয়ার্ককে শেখায়। এটি চেইন রুল ব্যবহার করে গ্রেডিয়েন্ট ক্যালকুলেট করে এবং ওয়েট আপডেট করে।

### কীভাবে কাজ করে?
```
1. ফরোয়ার্ড পাস: ইনপুট → প্রেডিকশন (ŷ)
2. লস ক্যালকুলেশন: ŷ vs y_true
3. ব্যাকওয়ার্ড পাস: গ্রেডিয়েন্ট ক্যালকুলেশন (চেইন রুল)
4. ওয়েট আপডেট: w = w - η · ∂L/∂w
```

## স্ক্র্যাচ থেকে ব্যাকপ্রোপাগেশন
```python
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, lr=0.01):
        # ওয়েট ইনিশিয়ালাইজেশন
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
        self.lr = lr
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, X):
        # লেয়ার ১
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        # লেয়ার ২ (আউটপুট)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, X, y, output):
        m = X.shape[0]  # স্যাম্পল সংখ্যা
        
        # আউটপুট লেয়ার গ্রেডিয়েন্ট
        dZ2 = output - y  # (ŷ - y)
        dW2 = np.dot(self.a1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        # হিডেন লেয়ার গ্রেডিয়েন্ট (চেইন রুল)
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.sigmoid_derivative(self.a1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # ওয়েট আপডেট (Gradient Descent)
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
    
    def train(self, X, y, epochs):
        losses = []
        for i in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
            loss = np.mean((output - y) ** 2)
            losses.append(loss)
            if i % 100 == 0:
                print(f"Epoch {i}, Loss: {loss:.6f}")
        return losses

# ফিন্যান্সিয়াল ডেটা সিমুলেশন
np.random.seed(42)
# ৫০০ স্যাম্পল, ৩ ফিচার
X = np.random.randn(500, 3)
# y = স্টক আপের প্রবাবিলিটি (০-১)
y = (1 / (1 + np.exp(-(X[:, 0] + 0.5*X[:, 1] - 0.3*X[:, 2] + np.random.randn(500)*0.1)))).reshape(-1, 1)

# মডেল ট্রেনিং
nn = NeuralNetwork(input_size=3, hidden_size=5, output_size=1, lr=0.5)
losses = nn.train(X, y, epochs=1000)

print("\nফাইনাল ওয়েটস W1:", nn.W1)
print("ফাইনাল ওয়েটস W2:", nn.W2)
```

## গ্রেডিয়েন্ট ভিজুয়ালাইজেশন
```python
def compute_gradients_manually(X, y, W1, b1, W2, b2):
    """ম্যানুয়ালি গ্রেডিয়েন্ট ক্যালকুলেশন"""
    # ফরোয়ার্ড
    z1 = np.dot(X, W1) + b1
    a1 = 1 / (1 + np.exp(-z1))
    z2 = np.dot(a1, W2) + b2
    a2 = 1 / (1 + np.exp(-z2))
    
    # MSE লস
    loss = np.mean((a2 - y) ** 2)
    
    # গ্রেডিয়েন্ট
    dL_da2 = 2 * (a2 - y) / len(X)
    da2_dz2 = a2 * (1 - a2)
    dL_dz2 = dL_da2 * da2_dz2
    
    dL_dW2 = np.dot(a1.T, dL_dz2)
    dL_db2 = np.sum(dL_dz2, axis=0)
    
    dL_da1 = np.dot(dL_dz2, W2.T)
    da1_dz1 = a1 * (1 - a1)
    dL_dz1 = dL_da1 * da1_dz1
    
    dL_dW1 = np.dot(X.T, dL_dz1)
    dL_db1 = np.sum(dL_dz1, axis=0)
    
    return loss, dL_dW1, dL_dW2

# টেস্ট
W1_test = np.random.randn(3, 5) * 0.01
b1_test = np.zeros((1, 5))
W2_test = np.random.randn(5, 1) * 0.01
b2_test = np.zeros((1, 1))

loss, grad_W1, grad_W2 = compute_gradients_manually(
    X[:10], y[:10], W1_test, b1_test, W2_test, b2_test
)
print(f"লস: {loss:.6f}")
print(f"dW2 norm: {np.linalg.norm(grad_W2):.6f}")
print(f"dW1 norm: {np.linalg.norm(grad_W1):.6f}")
```

## PyTorch অটোগ্র্যাড (Automated Differentiation)
```python
import torch
import torch.nn as nn
import torch.optim as optim

# PyTorch অটোমেটিক ব্যাকপ্রোপাগেশন
X_t = torch.tensor(X[:5], dtype=torch.float32)
y_t = torch.tensor(y[:5], dtype=torch.float32)

# Requires grad
w = torch.randn(3, 5, requires_grad=True)
b = torch.randn(5, requires_grad=True)
w2 = torch.randn(5, 1, requires_grad=True)
b2 = torch.randn(1, requires_grad=True)

# ফরোয়ার্ড
z1 = torch.mm(X_t, w) + b
a1 = torch.sigmoid(z1)
z2 = torch.mm(a1, w2) + b2
a2 = torch.sigmoid(z2)

loss = torch.mean((a2 - y_t) ** 2)
print(f"লস: {loss.item():.6f}")

# অটোমেটিক গ্রেডিয়েন্ট
loss.backward()
print(f"w.grad shape: {w.grad.shape}")
print(f"w.grad[:3, :3]:\n{w.grad[:3, :3]}")
print(f"বায়াসের গ্রেডিয়েন্ট:\n{b.grad}")
```

## ফিন্যান্স: প্রাইস প্রেডিকশন এরর ব্যাকপ্রোপাগেশন
```python
# স্টক প্রাইস প্রেডিকশনে ব্যাকপ্রোপাগেশন
class StockPriceNN:
    def __init__(self, n_features=5):
        self.nn = NeuralNetwork(n_features, 10, 1, lr=0.01)
    
    def prepare_features(self, df):
        """স্টক ফিচার তৈরি"""
        df['SMA_5'] = df['Close'].rolling(5).mean()
        df['SMA_20'] = df['Close'].rolling(20).mean()
        df['Volatility'] = df['Close'].pct_change().rolling(5).std()
        df['Volume_Change'] = df['Volume'].pct_change()
        df['Return'] = df['Close'].pct_change(5).shift(-5)
        df['Target'] = (df['Return'] > 0).astype(float)
        return df.dropna()
    
    def train_on_stock(self, ticker, start, end):
        import yfinance as yf
        data = yf.download(ticker, start=start, end=end)
        data = self.prepare_features(data)
        
        features = data[['SMA_5', 'SMA_20', 'Volatility', 'Volume_Change', 'Return']].values
        target = data['Target'].values.reshape(-1, 1)
        
        # ট্রেনিং-টেস্ট স্প্লিট
        split = int(len(features) * 0.8)
        X_train, X_test = features[:split], features[split:]
        y_train, y_test = target[:split], target[split:]
        
        self.nn.train(X_train, y_train, epochs=500)
        
        # টেস্ট
        test_pred = self.nn.forward(X_test)
        accuracy = np.mean((test_pred > 0.5) == y_test)
        print(f"টেস্ট অ্যাকুরেসি: {accuracy:.2%}")

# নোট: রিয়েল ডেটা দিয়ে ট্রেন করতে চাইলে আনকমেন্ট করুন
# model = StockPriceNN()
# model.train_on_stock("AAPL", "2020-01-01", "2024-01-01")
```

## সারসংক্ষেপ
- ব্যাকপ্রোপাগেশন: চেইন রুল ব্যবহার করে গ্রেডিয়েন্ট ক্যালকুলেশন
- ফরোয়ার্ড → লস → ব্যাকওয়ার্ড → আপডেট
- PyTorch/TensorFlow অটোমেটিক্যালি ব্যাকপ্রোপাগেশন করে (AutoGrad)
- ফিন্যান্সে প্রেডিকশন এরর ব্যাকপ্রোপাগেট করে মডেল ইম্প্রুভ
- গ্রেডিয়েন্ট ভ্যানিশিং/এক্সপ্লোডিং সমস্যা হতে পারে (Day 09 এ সমাধান)