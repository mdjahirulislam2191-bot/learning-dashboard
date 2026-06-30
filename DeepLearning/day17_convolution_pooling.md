# Day 17: কনভোলিউশন ও পুলিং লেয়ার 🔍

## কনভোলিউশন লেয়ার বিস্তারিত

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## কনভোলিউশন প্যারামিটার
```python
class ConvParams:
    """কনভোলিউশন লেয়ার প্যারামিটার এক্সপ্লোরেশন"""
    
    @staticmethod
    def demo_kernel_effects():
        """বিভিন্ন কার্নেলের প্রভাব"""
        # সিম্পল সিগন্যাল
        signal = torch.zeros(1, 1, 32)
        signal[0, 0, 10:20] = 1.0  # square pulse
        
        # বিভিন্ন কার্নেল
        kernels = {
            'Edge Detect': torch.tensor([[-1.0, 0.0, 1.0]]).view(1, 1, -1),
            'Smooth (Mean)': torch.tensor([[0.33, 0.33, 0.33]]).view(1, 1, -1),
            'Sharpen': torch.tensor([[-1.0, 2.0, -1.0]]).view(1, 1, -1),
            'Gaussian': torch.tensor([[0.25, 0.5, 0.25]]).view(1, 1, -1)
        }
        
        results = {}
        for name, kernel in kernels.items():
            conv = nn.Conv1d(1, 1, kernel_size=3, bias=False)
            conv.weight.data = kernel
            output = conv(signal)
            results[name] = output.squeeze().detach().numpy()
            
            print(f"{name}: min={output.min():.2f}, max={output.max():.2f}")
        
        return results

# ConvParams.demo_kernel_effects()
print("কার্নেল ইফেক্টস ডেমো কনফিগার করা হয়েছে")
```

## প্যাডিং ও স্ট্রাইড
```python
def padding_strides_demo():
    """প্যাডিং ও স্ট্রাইড ডেমো"""
    input_length = 10
    kernel_size = 3
    
    # নো প্যাডিং
    conv_no_pad = nn.Conv1d(1, 1, kernel_size=3, padding=0)
    # অউটপুট: 10 - 3 + 1 = 8
    
    # সেম প্যাডিং (ইনপুট = আউটপুট)
    conv_same = nn.Conv1d(1, 1, kernel_size=3, padding=1)
    # অউটপুট: 10 - 3 + 2*1 + 1 = 10
    
    # স্ট্রাইড=২
    conv_stride2 = nn.Conv1d(1, 1, kernel_size=3, stride=2, padding=1)
    # অউটপুট: (10 - 3 + 2) // 2 + 1 = 5
    
    x = torch.randn(1, 1, input_length)
    
    print(f"Input: {x.shape}")
    print(f"Conv (no pad): {conv_no_pad(x).shape}")
    print(f"Conv (same pad): {conv_same(x).shape}")
    print(f"Conv (stride=2): {conv_stride2(x).shape}")

padding_strides_demo()
```

## পুলিং লেয়ার
```python
def pooling_demo():
    """পুলিং লেয়ার ডেমো"""
    # ইনপুট
    x = torch.tensor([[[1.0, 3.0, 2.0, 5.0, 1.0, 4.0]]])
    
    # Max Pooling
    maxpool = nn.MaxPool1d(kernel_size=2)
    print(f"Input: {x.squeeze()}")
    print(f"MaxPool (k=2): {maxpool(x).squeeze()}")
    
    # Average Pooling
    avgpool = nn.AvgPool1d(kernel_size=2)
    print(f"AvgPool (k=2): {avgpool(x).squeeze()}")
    
    # Adaptive Pooling (fixed output size)
    adaptive = nn.AdaptiveAvgPool1d(output_size=3)
    print(f"AdaptiveAvg (out=3): {adaptive(x).squeeze()}")

pooling_demo()
```

## ফিন্যান্সিয়াল টাইম সিরিজ কনভোলিউশন
```python
class FinancialConvNet(nn.Module):
    """ফিন্যান্সিয়াল টাইম সিরিজের জন্য কনভোলিউশন নেট"""
    def __init__(self, seq_len=60, n_features=5):
        super().__init__()
        
        self.conv_block1 = nn.Sequential(
            nn.Conv1d(n_features, 32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        
        self.conv_block2 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        
        self.conv_block3 = nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        
        # Calculate feature size
        self._to_linear = None
        self._get_conv_output((1, n_features, seq_len))
        
        self.fc = nn.Sequential(
            nn.Linear(self._to_linear, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )
    
    def _get_conv_output(self, shape):
        with torch.no_grad():
            x = torch.zeros(shape)
            x = self.conv_block1(x)
            x = self.conv_block2(x)
            x = self.conv_block3(x)
            self._to_linear = x.view(1, -1).size(1)
    
    def forward(self, x):
        # x: (batch, seq, features) → (batch, features, seq)
        x = x.transpose(1, 2)
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# টেস্ট
model = FinancialConvNet(seq_len=60, n_features=5)
test_x = torch.randn(4, 60, 5)
print(f"ConvNet output: {model(test_x).shape}")  # (4, 1)
```

## রিসেপটিভ ফিল্ড
```python
def receptive_field_demo():
    """রিসেপটিভ ফিল্ড বোঝা"""
    print("রিসেপটিভ ফিল্ড: CNN-এর আউটপুট কতটুকু ইনপুট দেখে\n")
    
    layers = [
        ("Conv1 (k=3)", 3, 1, 1),
        ("Pool (k=2)", 3, 2, 2),  
        ("Conv2 (k=3)", 7, 4, 4),
        ("Pool (k=2)", 7, 4, 8),
        ("Conv3 (k=3)", 15, 8, 16),
    ]
    
    for name, rf, jump, start in layers:
        print(f"Layer: {name:15s} → RF={rf}, Jump={jump}")

receptive_field_demo()
```

## সারসংক্ষেপ
| উপাদান | কাজ | ফিন্যান্সে |
|--------|-----|-----------|
| **Conv1D** | টাইম সিরিজ কনভোলিউশন | প্যাটার্ন ডিটেকশন |
| **Padding** | সাইজ কন্ট্রোল | সিকোয়েন্স মেইন্টেন |
| **Stride** | ডাউনস্যাম্পলিং | কম্প্রেশন |
| **MaxPool** | ডোমিনেন্ট ফিচার | নয়েজ রিডাকশন |
| **AvgPool** | স্মুথিং | ট্রেন্ড ক্যাপচার |
| **AdaptivePool** | ফিক্সড আউটপুট | ভেরিয়েবল ইনপুট |