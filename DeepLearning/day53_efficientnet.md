# Day 53: EfficientNet — স্কেলেবল CNN ⚡📈

## EfficientNet কী?
EfficientNet নিউরাল নেটওয়ার্কের স্কেলিং অপ্টিমাইজ করে — ডেপ্থ, উইড্থ, রেজোলিউশন তিনটাই ব্যালেন্সডভাবে বাড়ানো হয়।

### EfficientNet-এর মূল আইডিয়া
Compound Scaling: একসাথে তিনটি ডাইমেনশন স্কেল করা
- **Depth (গভীরতা)**: আরও লেয়ার → কমপ্লেক্স ফিচার
- **Width (প্রস্থ)**: আরও চ্যানেল → ফাইন-গ্রেইন্ড ফিচার
- **Resolution (রেজোলিউশন)**: বড় ইনপুট → ডিটেইলড প্যাটার্ন

### MBConv (Mobile Inverted Bottleneck Conv)
EfficientNet-এর বিল্ডিং ব্লক — ডেপ্থওয়াইজ সেপারেবল কনভোলিউশন + Squeeze-and-Excitation

### ফিন্যান্সে EfficientNet
- এফিশিয়েন্ট টাইম সিরিজ প্রসেসিং
- লো-লেটেন্সি ট্রেডিং মডেল
- এজ ডিভাইসে ডিপ্লয়মেন্ট
- মাল্টি-এসেট ফিচার এক্সট্রাকশন

## EfficientNet ইমপ্লিমেন্টেশন (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import math

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. Squeeze-and-Excitation (SE) ব্লক

```python
class SqueezeExcitation(nn.Module):
    """Squeeze-and-Excitation ব্লক — চ্যানেল অ্যাটেনশন"""
    def __init__(self, in_channels, reduced_dim):
        super().__init__()
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool1d(1),  # Squeeze
            nn.Conv1d(in_channels, reduced_dim, kernel_size=1),
            nn.ReLU(inplace=True),
            nn.Conv1d(reduced_dim, in_channels, kernel_size=1),
            nn.Sigmoid()  # Excitation
        )
    
    def forward(self, x):
        # স্কেল ফ্যাক্টর
        scale = self.se(x)
        return x * scale  # স্কেলড ফিচার

# ডেমো
se_block = SqueezeExcitation(64, 16)
x = torch.randn(2, 64, 20)
out = se_block(x)
print(f"SE ব্লক: {x.shape} → {out.shape}")
print("SE ব্লক গুরুত্বপূর্ণ চ্যানেলকে জোর দেয়")
```

## 2. MBConv ব্লক

```python
class MBConvBlock(nn.Module):
    """Mobile Inverted Bottleneck Convolution (MBConv)"""
    def __init__(self, in_channels, out_channels, kernel_size=3, 
                 stride=1, expand_ratio=6, se_ratio=0.25):
        super().__init__()
        self.use_residual = (stride == 1 and in_channels == out_channels)
        
        # Expansion ফেজ (1×1)
        expanded_channels = in_channels * expand_ratio
        if expand_ratio != 1:
            self.expand = nn.Sequential(
                nn.Conv1d(in_channels, expanded_channels, kernel_size=1, bias=False),
                nn.BatchNorm1d(expanded_channels),
                nn.ReLU6(inplace=True)
            )
        else:
            self.expand = nn.Identity()
        
        # Depthwise কনভোলিউশন
        self.depthwise = nn.Sequential(
            nn.Conv1d(expanded_channels, expanded_channels, kernel_size,
                      stride=stride, padding=kernel_size//2, 
                      groups=expanded_channels, bias=False),
            nn.BatchNorm1d(expanded_channels),
            nn.ReLU6(inplace=True)
        )
        
        # Squeeze-and-Excitation
        reduced_dim = max(1, int(in_channels * se_ratio))
        self.se = SqueezeExcitation(expanded_channels, reduced_dim)
        
        # Projection ফেজ (1×1)
        self.project = nn.Sequential(
            nn.Conv1d(expanded_channels, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm1d(out_channels)
        )
    
    def forward(self, x):
        residual = x
        
        x = self.expand(x)
        x = self.depthwise(x)
        x = self.se(x)
        x = self.project(x)
        
        if self.use_residual:
            x += residual
        
        return x

# ডেমো
mbconv = MBConvBlock(32, 64, kernel_size=3, stride=2, expand_ratio=6)
x = torch.randn(2, 32, 100)
out = mbconv(x)
print(f"MBConv ব্লক: {x.shape} → {out.shape}")
```

## 3. EfficientNet (টাইম সিরিজের জন্য)

```python
class EfficientNet1D(nn.Module):
    """1D EfficientNet — টাইম সিরিজের জন্য"""
    def __init__(self, in_channels=1, num_classes=3, width_mult=1.0, depth_mult=1.0):
        super().__init__()
        
        # বেস কনফিগারেশন: (in, out, k, s, e, se_r)
        # k=kernel, s=stride, e=expand_ratio, se_r=SE ratio
        base_config = [
            # stage 1
            [32, 16, 3, 1, 1, 0.25],
            # stage 2
            [16, 24, 3, 2, 6, 0.25],
            [24, 24, 3, 1, 6, 0.25],
            # stage 3
            [24, 40, 5, 2, 6, 0.25],
            [40, 40, 5, 1, 6, 0.25],
            # stage 4
            [40, 80, 3, 2, 6, 0.25],
            [80, 80, 3, 1, 6, 0.25],
            [80, 80, 3, 1, 6, 0.25],
            # stage 5
            [80, 112, 5, 1, 6, 0.25],
            [112, 112, 5, 1, 6, 0.25],
            [112, 112, 5, 1, 6, 0.25],
            # stage 6
            [112, 192, 5, 2, 6, 0.25],
            [192, 192, 5, 1, 6, 0.25],
            [192, 192, 5, 1, 6, 0.25],
            [192, 192, 5, 1, 6, 0.25],
            # stage 7
            [192, 320, 3, 1, 6, 0.25],
        ]
        
        # ডেপ্থ এবং উইড্থ স্কেলিং
        scaled_config = []
        for cfg in base_config:
            in_ch = self._round_channels(cfg[0], width_mult)
            out_ch = self._round_channels(cfg[1], width_mult)
            scaled_config.append([in_ch, out_ch, cfg[2], cfg[3], cfg[4], cfg[5]])
        
        # স্টেম
        stem_out = self._round_channels(32, width_mult)
        self.stem = nn.Sequential(
            nn.Conv1d(in_channels, stem_out, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm1d(stem_out),
            nn.ReLU6(inplace=True)
        )
        
        # MBConv স্টেজেস
        self.blocks = nn.ModuleList()
        current_in = stem_out
        depth_idx = 0
        
        for i, cfg in enumerate(scaled_config):
            in_ch, out_ch, k, s, e, se_r = cfg
            repeat = max(1, int(math.ceil(depth_mult)))
            actual_repeat = repeat if i > 0 else 1
            
            for j in range(actual_repeat):
                stride = s if j == 0 else 1
                self.blocks.append(MBConvBlock(
                    current_in, out_ch, kernel_size=k,
                    stride=stride, expand_ratio=e, se_ratio=se_r
                ))
                current_in = out_ch
        
        # হেড
        final_out = self._round_channels(1280, width_mult)
        self.head = nn.Sequential(
            nn.Conv1d(current_in, final_out, kernel_size=1, bias=False),
            nn.BatchNorm1d(final_out),
            nn.ReLU6(inplace=True),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(final_out, num_classes)
        )
    
    def _round_channels(self, channels, mult):
        """চ্যানেল সংখ্যা স্কেল করা"""
        if mult == 1.0:
            return channels
        divisor = 8
        new_channels = max(divisor, int(channels * mult + divisor / 2) // divisor * divisor)
        if new_channels < 0.9 * channels * mult:
            new_channels += divisor
        return new_channels
    
    def forward(self, x):
        x = self.stem(x)
        for block in self.blocks:
            x = block(x)
        x = self.head(x)
        return x

# ডেমো
print("\n=== EfficientNet তৈরি ===")
effnet_b0 = EfficientNet1D(in_channels=1, num_classes=3, width_mult=1.0, depth_mult=1.0).to(device)
total_params = sum(p.numel() for p in effnet_b0.parameters())
print(f"EfficientNet-B0 প্যারামিটার: {total_params:,}")

dummy = torch.randn(2, 1, 256).to(device)
out = effnet_b0(dummy)
print(f"ইনপুট: {dummy.shape} → আউটপুট: {out.shape}")
```

## 4. Compound Scaling ডেমো

```python
class CompoundScalingDemo:
    """Compound Scaling ডেমো"""
    
    @staticmethod
    def create_efficientnet_variants():
        """EfficientNet ভারিয়েন্ট বি0-বি7"""
        variants = {
            'B0': (1.0, 1.0, 224),
            'B1': (1.0, 1.1, 240),
            'B2': (1.1, 1.2, 260),
            'B3': (1.2, 1.4, 300),
            'B4': (1.4, 1.8, 380),
            'B5': (1.6, 2.2, 456),
            'B6': (1.8, 2.6, 528),
            'B7': (2.0, 3.1, 600)
        }
        
        print("=== EfficientNet ভারিয়েন্টস ===")
        print(f"{'মডেল':<12} {'Width':<8} {'Depth':<8} {'Params':<12}")
        print("-" * 40)
        
        for name, (w, d, r) in variants.items():
            model = EfficientNet1D(in_channels=1, num_classes=3, 
                                  width_mult=w, depth_mult=d).to(device)
            params = sum(p.numel() for p in model.parameters())
            print(f"EfficientNet-{name:<9} {w:<8.1f} {d:<8.1f} {params:,}")
    
    @staticmethod
    def scaling_formula():
        """Compound Scaling ফর্মুলা"""
        print("""
=== Compound Scaling ফর্মুলা ===

ϕ = compound coefficient (কম্পাউন্ড কোএফিসিয়েন্ট)

depth:    d = α^ϕ      (α=1.2)
width:    w = β^ϕ      (β=1.1)
resolution: r = γ^ϕ    (γ=1.15)

Constraint: α · β² · γ² ≈ 2

ϕ=0 → B0 (বেসলাইন)
ϕ=1 → B1
ϕ=2 → B2
...
ϕ=7 → B7

নোট: ফ্লপস ~2^ϕ বারে বাড়ে
""")

CompoundScalingDemo.create_efficientnet_variants()
CompoundScalingDemo.scaling_formula()
```

## 5. EfficientNet ট্রেডিং সিস্টেম

```python
class EfficientNetTrader:
    """EfficientNet-বেসড ট্রেডিং সিস্টেম"""
    def __init__(self, input_length=256):
        self.input_length = input_length
        self.model = EfficientNet1D(in_channels=1, num_classes=3, 
                                   width_mult=0.5, depth_mult=0.5).to(device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=0.001, weight_decay=1e-4)
        print(f"EfficientNetTrader তৈরি: {sum(p.numel() for p in self.model.parameters()):,} প্যারামিটার")
    
    def _prepare_data(self, prices):
        """প্রাইস ডেটা প্রস্তুত"""
        X, y = [], []
        for i in range(len(prices) - self.input_length - 5):
            seq = prices[i:i+self.input_length]
            future_return = (prices[i+self.input_length+5] - prices[i+self.input_length]) / prices[i+self.input_length]
            
            if future_return > 0.01:
                label = 2  # UP
            elif future_return < -0.01:
                label = 0  # DOWN
            else:
                label = 1  # NEUTRAL
            
            # নরমালাইজেশন
            seq = (seq - np.mean(seq)) / (np.std(seq) + 1e-6)
            X.append(seq)
            y.append(label)
        
        X = np.array(X, dtype=np.float32).reshape(-1, 1, self.input_length)
        y = np.array(y, dtype=np.int64)
        return X, y
    
    def train(self, prices, epochs=50, batch_size=32):
        """ট্রেনিং"""
        X, y = self._prepare_data(prices)
        dataset = torch.utils.data.TensorDataset(
            torch.FloatTensor(X), torch.LongTensor(y)
        )
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.model.train()
        scheduler = optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=epochs)
        
        for epoch in range(epochs):
            epoch_loss = 0
            correct = 0
            total = 0
            
            for batch_X, batch_y in loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()
                
                epoch_loss += loss.item()
                _, predicted = outputs.max(1)
                total += batch_y.size(0)
                correct += predicted.eq(batch_y).sum().item()
            
            scheduler.step()
            
            if (epoch + 1) % 10 == 0:
                acc = 100.0 * correct / total
                lr = self.optimizer.param_groups[0]['lr']
                print(f"এপোক {epoch+1}/{epochs}: লস={epoch_loss/len(loader):.4f}, "
                      f"অ্যাকুরেসি={acc:.2f}%, LR={lr:.6f}")

# ডেমো
print("\n=== EfficientNet ট্রেডিং সিস্টেম ===")
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(1000) * 0.5)

trader = EfficientNetTrader(input_length=128)
trader.train(prices, epochs=30, batch_size=32)

print("\nEfficientNet মডেল ট্রেডিংয়ের জন্য প্রস্তুত!")
print("ইনফারেন্স টাইম: ~2ms (GPU) — লো-লেটেন্সি ট্রেডিংয়ের জন্য উপযুক্ত")
```

## সারাংশ
- EfficientNet compound scaling দিয়ে Depth + Width + Resolution অপ্টিমাইজ করে
- MBConv (Mobile Inverted Bottleneck) এফিশিয়েন্ট বিল্ডিং ব্লক
- Squeeze-and-Excitation চ্যানেল ওয়াইজ অ্যাটেনশন দেয়
- B0-B7 ভারিয়েন্ট বিভিন্ন কম্পিউট বাজেট কভার করে
- ফিন্যান্সে লো-লেটেন্সি এবং এজ ডিপ্লয়মেন্টের জন্য আদর্শ
- একই অ্যাকুরেসিতে 10x ছোট মডেল (তুলনায় ResNet, Inception)