# Day 16: CNN বেসিক 🖼️

## কনভোলিউশনাল নিউরাল নেটওয়ার্ক (CNN)
CNN মূলত ইমেজ ডেটার জন্য ডিজাইন করা হলেও, ফিন্যান্সে 1D CNN টাইম সিরিজের জন্য কার্যকর।

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## কনভোলিউশন অপারেশন
```python
def convolution_demo():
    """কনভোলিউশন অপারেশন বোঝা"""
    # ইনপুট: ১x৫ টেনসর
    signal = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # কার্নেল: ১x৩
    kernel = torch.tensor([0.5, 1.0, 0.5])
    
    # ম্যানুয়াল কনভোলিউশন
    output = []
    for i in range(len(signal) - len(kernel) + 1):
        conv_val = (signal[i:i+3] * kernel).sum()
        output.append(conv_val)
    
    print(f"Signal: {signal}")
    print(f"Kernel: {kernel}")
    print(f"Convolution output: {output}")
    
    # PyTorch Conv1d
    signal_2d = signal.view(1, 1, -1)  # (batch, channels, length)
    conv1d = nn.Conv1d(in_channels=1, out_channels=1, kernel_size=3, bias=False)
    conv1d.weight.data = kernel.view(1, 1, -1)
    
    output_pt = conv1d(signal_2d)
    print(f"PyTorch Conv1d output: {output_pt.squeeze()}")

convolution_demo()
```

## ১D CNN (টাইম সিরিজের জন্য)
```python
class TimeSeriesCNN(nn.Module):
    """1D CNN for Financial Time Series"""
    def __init__(self, input_channels=1, seq_length=20):
        super().__init__()
        
        self.conv_layers = nn.Sequential(
            nn.Conv1d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
            
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
            
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        
        self.fc = nn.Sequential(
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        # x shape: (batch, seq_len) 
        x = x.unsqueeze(1)  # (batch, 1, seq_len)
        x = self.conv_layers(x)
        x = x.squeeze(-1)
        x = self.fc(x)
        return x

# টেস্ট
model = TimeSeriesCNN(seq_length=20)
test_input = torch.randn(8, 20)  # batch=8, seq=20
print(f"Input: {test_input.shape}")
print(f"Output: {model(test_input).shape}")
```

## ২D CNN (ইমেজ ডেটা)
```python
class StockChartCNN(nn.Module):
    """স্টক চার্ট ইমেজ ক্লাসিফিকেশন CNN"""
    def __init__(self, num_classes=2):
        super().__init__()
        
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),  # RGB input
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        
        self.fc = nn.Sequential(
            nn.Linear(64 * 28 * 28, 256),  # 224x224 → 28x28 after 3 poolings
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
```

## ফিন্যান্সে CNN (টেকনিক্যাল প্যাটার্ন ডিটেকশন)
```python
class PatternDetectionCNN(nn.Module):
    """স্টক চার্ট প্যাটার্ন ডিটেকশন (Head & Shoulders, Double Top, etc.)"""
    def __init__(self, input_channels=5):  # OHLCV
        super().__init__()
        
        self.conv1d = nn.Sequential(
            nn.Conv1d(input_channels, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool1d(2),
            
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),
            
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 3)  # 3 patterns: uptrend, downtrend, sideways
        )
    
    def forward(self, x):
        # x: (batch, seq_len, 5) → (batch, 5, seq_len)
        x = x.transpose(1, 2)
        x = self.conv1d(x)
        x = x.squeeze(-1)
        x = self.classifier(x)
        return x

# সিন্থেটিক ট্রেন্ড ডেটা
def generate_trend_data(n_samples=1000, seq_len=50):
    """সিন্থেটিক ট্রেন্ড ডেটা জেনারেশন"""
    X = []
    y = []
    for _ in range(n_samples):
        trend = np.random.choice(['up', 'down', 'sideways'])
        
        if trend == 'up':
            data = np.cumsum(np.random.randn(seq_len) * 0.5) + np.linspace(0, 10, seq_len)
            label = 0
        elif trend == 'down':
            data = np.cumsum(np.random.randn(seq_len) * 0.5) - np.linspace(0, 10, seq_len)
            label = 1
        else:
            data = np.cumsum(np.random.randn(seq_len) * 1.0)
            label = 2
        
        # 5 চ্যানেল সিমুলেট
        multi_channel = np.column_stack([
            data + np.random.randn(seq_len) * 0.1,
            data + np.random.randn(seq_len) * 0.2,
            data + np.random.randn(seq_len) * 0.1,
            data + np.random.randn(seq_len) * 0.3,
            np.random.rand(seq_len) * 1000000  # Volume
        ])
        
        X.append(multi_channel)
        y.append(label)
    
    return np.array(X, dtype=np.float32), np.array(y)

# টেস্ট
X, y = generate_trend_data(100, 50)
print(f"Trend data: X={X.shape}, y={y.shape}")

model = PatternDetectionCNN()
out = model(torch.FloatTensor(X[:4]))
print(f"Pattern prediction: {out.shape}")  # (4, 3)
```

## CNN-এর কী উপাদান?
```python
class CNNComponents:
    """CNN-এর মূল উপাদান"""
    
    @staticmethod
    def show_components():
        components = {
            'Conv1d/2d': '''
                কনভোলিউশন লেয়ার
                - কার্নেল/ফিল্টার দিয়ে কনভোলিউশন
                - লার্নেবল ফিচার ডিটেক্টর
                - ফিন্যান্স: লোকাল প্যাটার্ন ডিটেকশন
            ''',
            'Activation': '''
                ReLU অ্যাক্টিভেশন
                - নন-লিনিয়ারিটি যোগ
                - নেগেটিভ ভ্যালু জিরো করে
            ''',
            'Pooling': '''
                ম্যাক্স/এভারেজ পুলিং
                - ডাইমেনশন কমানো
                - ডোমিনেন্ট ফিচার ধরা
                - ওভারফিটিং কমানো
            ''',
            'Fully Connected': '''
                ফ্ল্যাটেন + ডেন্স লেয়ার
                - ফিচার কম্বাইন
                - ফাইনাল ক্লাসিফিকেশন/রিগ্রেশন
            '''
        }
        
        for name, desc in components.items():
            print(f"📌 {name}:")
            print(desc)
            print("-" * 30)

CNNComponents.show_components()
```

## সারসংক্ষেপ
- CNN = Convolution + Pooling + FC Layers
- 1D CNN: টাইম সিরিজ, 시그নাল প্রসেসিং
- 2D CNN: ইমেজ, স্টক চার্ট প্যাটার্ন
- ফিন্যান্স: প্যাটার্ন ডিটেকশন, ট্রেন্ড ক্লাসিফিকেশন
- CNN অটোমেটিক ফিচার এক্সট্র্যাকশন করে (ফিচার ইঞ্জিনিয়ারিং লাগে না)