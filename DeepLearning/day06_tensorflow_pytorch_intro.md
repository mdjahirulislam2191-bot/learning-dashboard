# Day 06: TensorFlow ও PyTorch পরিচিতি 🔥

## TensorFlow vs PyTorch

| বৈশিষ্ট্য | TensorFlow | PyTorch |
|-----------|-----------|---------|
| ডেভেলপার | Google | Meta (Facebook) |
| API স্টাইল | ফাংশনাল + Keras | ইম্পারেটিভ (Pythonic) |
| ডিবাগিং | কঠিন | সহজ (Python-native) |
| প্রোডাকশন | ভালো (TF Serving) | TorchScript |
| রিসার্চ | কম জনপ্রিয় | অধিক জনপ্রিয় |

## PyTorch বেসিক
```python
import torch
import torch.nn as nn
import numpy as np

# টেনসর ক্রিয়েশন
scalar = torch.tensor(5.0)
vector = torch.tensor([1.0, 2.0, 3.0])
matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
tensor_3d = torch.randn(2, 3, 4)

print(f"Scalar: {scalar}")
print(f"Vector: {vector}")
print(f"Matrix shape: {matrix.shape}")
print(f"3D Tensor shape: {tensor_3d.shape}")

# NumPy ↔ Tensor
np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)
back_to_np = tensor.numpy()
print(f"NumPy → Tensor: {tensor}")
print(f"Tensor → NumPy: {back_to_np}")

# GPU চেক
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
```

## TensorFlow/Keras বেসিক
```python
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

# টেনসর
tensor = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print(f"Tensor:\n{tensor}")

# ভ্যারিয়েবল
w = tf.Variable(tf.random.normal([3, 2]))
print(f"Variable shape: {w.shape}")
```

## ফিন্যান্সিয়াল ডেটা টেনসরে রূপান্তর
```python
import yfinance as yf
import pandas as pd

def stocks_to_tensor(tickers, start="2023-01-01", end="2024-01-01"):
    """স্টক ডেটা টেনসরে রূপান্তর"""
    data = yf.download(tickers, start=start, end=end)['Close']
    tensor_data = torch.tensor(data.values, dtype=torch.float32)
    return tensor_data, data.columns.tolist()

# উদাহরণ
tickers = ["AAPL", "MSFT", "GOOGL"]
prices_tensor, symbols = stocks_to_tensor(tickers)
print(f"স্টক প্রাইস টেনসর shape: {prices_tensor.shape}")  # [days, stocks]
print(f"প্রথম ৫ দিন:\n{prices_tensor[:5]}")
```

### টেনসর ম্যাথ ফিন্যান্সে
```python
# রিটার্ন ক্যালকুলেশন
returns = torch.diff(prices_tensor, dim=0) / prices_tensor[:-1]
print(f"রিটার্ন shape: {returns.shape}")
print(f"গড় রিটার্ন: {returns.mean(dim=0)}")
print(f"ভোলাটিলিটি (std): {returns.std(dim=0)}")

# কোভেরিয়েন্স ম্যাট্রিক্স
cov_matrix = torch.cov(returns.T)
print(f"কোভেরিয়েন্স ম্যাট্রিক্স:\n{cov_matrix}")

# পোর্টফোলিও ভ্যারিয়েন্স
weights = torch.tensor([0.4, 0.4, 0.2])
portfolio_var = weights.T @ cov_matrix @ weights
print(f"পোর্টফোলিও ভ্যারিয়েন্স: {portfolio_var:.6f}")
```

## অটোগ্র্যাড (Automatic Differentiation)
```python
# গ্রেডিয়েন্ট ট্র্যাকিং
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1

y.backward()  # dy/dx = 2x + 2 = 8
print(f"dy/dx at x=3: {x.grad.item()}")  # 8.0

# ফিন্যান্স: গ্রেডিয়েন্ট দিয়ে অপ্টিমাইজেশন
price = torch.tensor(100.0, requires_grad=True)
# প্রফিট ফাংশন সহজ উদাহরণ
profit = -((price - 105) ** 2)  # maximize near 105
profit.backward()
print(f"অপ্টিমাল প্রাইসের গ্রেডিয়েন্ট: {price.grad.item()}")
```

## কনক্লুশন
- PyTorch: রিসার্চ ও ডেভেলপমেন্টের জন্য জনপ্রিয়
- TensorFlow: প্রোডাকশনের জন্য ভালো
- উভয়ই GPU সাপোর্ট ও অটোগ্র্যাড সমর্থন করে
- আমরা এই কোর্সে PyTorch ব্যবহার করব