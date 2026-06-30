# Day 51: ResNet — রেসিডুয়াল নেটওয়ার্ক 🏗️🔄

## ResNet কী?
ResNet (Residual Network) গভীর নিউরাল নেটওয়ার্কে গ্রেডিয়েন্ট ভ্যানিশিং সমস্যা সমাধানের জন্য রেসিডুয়াল কানেকশন ব্যবহার করে।

### সমস্যা: ডিগ্রেডেশন ইফেক্ট
গভীর নেটওয়ার্ক → বেশি প্যারামিটার →理论上 ভাল → কিন্তু Actually বেশি লেয়ার যোগ করলে ট্রেনিং এরর বেড়ে যায়

### ResNet-এর সমাধান: রেসিডুয়াল লার্নিং
```
প্লেইন নেট: H(x) = F(x)
ResNet: H(x) = F(x) + x
```
x → F(x) → + → ReLU → আউটপুট
    ↳ শর্টকাট কানেকশন ↳

### ফিন্যান্সে ResNet
- টাইম সিরিজ প্যাটার্ন ডিটেকশন
- মাল্টি-স্কেল ফিচার এক্সট্রাকশন
- হাই-ফ্রিকোয়েন্সি ট্রেডিং ডেটা প্রসেসিং
- রিস্ক ফ্যাক্টর মডেলিং

## ResNet ইমপ্লিমেন্টেশন (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. রেসিডুয়াল ব্লক

```python
class ResidualBlock(nn.Module):
    """বেসিক রেসিডুয়াল ব্লক (ResNet-18/34)"""
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=3, 
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(out_channels)
        self.downsample = downsample
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        # ডাউনস্যাম্পল (যদি শেপ মিল না হয়)
        if self.downsample is not None:
            identity = self.downsample(x)
        
        # রেসিডুয়াল কানেকশন
        out += identity
        out = self.relu(out)
        
        return out

# ডেমো
block = ResidualBlock(64, 64)
x = torch.randn(2, 64, 20)
out = block(x)
print(f"রেসিডুয়াল ব্লক: {x.shape} → {out.shape}")
```

## 2. বটলনেক ব্লক (ResNet-50/101/152)

```python
class BottleneckBlock(nn.Module):
    """Bottleneck রেসিডুয়াল ব্লক (1×1 → 3×3 → 1×1)"""
    expansion = 4
    
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super().__init__()
        width = out_channels  # বটলনেক চ্যানেল
        
        self.conv1 = nn.Conv1d(in_channels, width, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm1d(width)
        self.conv2 = nn.Conv1d(width, width, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(width)
        self.conv3 = nn.Conv1d(width, out_channels * self.expansion, 
                               kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm1d(out_channels * self.expansion)
        self.downsample = downsample
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        
        out = self.conv3(out)
        out = self.bn3(out)
        
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out += identity
        out = self.relu(out)
        
        return out

# ডেমো
bottleneck = BottleneckBlock(64, 64)
x = torch.randn(2, 64, 20)
out = bottleneck(x)
print(f"Bottleneck ব্লক: {x.shape} → {out.shape} (expansion=4)")
```

## 3. সম্পূর্ণ ResNet মডেল (1D — টাইম সিরিজের জন্য)

```python
class ResNet1D(nn.Module):
    """1D ResNet — টাইম সিরিজ এবং ফিন্যান্সিয়াল ডেটার জন্য"""
    def __init__(self, in_channels=1, num_classes=3, 
                 block=ResidualBlock, layers=[2, 2, 2, 2]):
        super().__init__()
        self.in_channels = 64
        
        # ইনপুট কনভোলিউশন
        self.conv1 = nn.Conv1d(in_channels, 64, kernel_size=7, 
                               stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm1d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # রেসিডুয়াল লেয়ারস
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
        
        # ক্লাসিফায়ার
        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(512, num_classes)
    
    def _make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels:
            downsample = nn.Sequential(
                nn.Conv1d(self.in_channels, out_channels, 
                         kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm1d(out_channels)
            )
        
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for _ in range(1, blocks):
            layers.append(block(out_channels, out_channels))
        
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        
        return x

# ডেমো — ResNet-18 (1D)
resnet18 = ResNet1D(in_channels=1, num_classes=3, 
                    block=ResidualBlock, layers=[2, 2, 2, 2]).to(device)
print(f"ResNet-18 (1D):\n{resnet18}")

dummy_input = torch.randn(4, 1, 128).to(device)  # batch=4, 1 চ্যানেল, 128 টাইমস্টেপ
output = resnet18(dummy_input)
print(f"\nইনপুট শেপ: {dummy_input.shape}")
print(f"আউটপুট শেপ: {output.shape}  # [batch, 3 ক্লাস]")
```

## 4. ফিন্যান্সিয়াল টাইম সিরিজ ক্লাসিফিকেশন

```python
class FinancialResNet:
    """ফিন্যান্সিয়াল টাইম সিরিজের জন্য ResNet"""
    def __init__(self, seq_length=128, num_classes=3):
        self.seq_length = seq_length
        self.num_classes = num_classes
        # 3 ক্লাস: আপট্রেন্ড, ডাউনট্রেন্ড, সাইডওয়েজ
        
        self.model = ResNet1D(
            in_channels=1, 
            num_classes=num_classes,
            block=ResidualBlock,
            layers=[2, 2, 2, 2]
        ).to(device)
        
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
    
    def _generate_synthetic_data(self, n_samples=500):
        """সিন্থেটিক টাইম সিরিজ ডেটা তৈরি"""
        X = []
        y = []
        
        for _ in range(n_samples):
            trend = np.random.choice([-1, 0, 1])  # ক্লাস
            noise = np.random.randn(self.seq_length) * 0.1
            drift = np.cumsum(np.random.randn(self.seq_length)) * 0.05
            signal = np.linspace(0, trend, self.seq_length) + noise + drift
            
            X.append(signal)
            y.append(trend + 1)  # 0, 1, 2
        
        X = np.array(X, dtype=np.float32).reshape(-1, 1, self.seq_length)
        y = np.array(y, dtype=np.int64)
        
        return torch.FloatTensor(X), torch.LongTensor(y)
    
    def train(self, epochs=30, batch_size=32):
        """ResNet ট্রেনিং"""
        X, y = self._generate_synthetic_data(500)
        dataset = torch.utils.data.TensorDataset(X, y)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.model.train()
        history = []
        
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
                self.optimizer.step()
                
                epoch_loss += loss.item()
                _, predicted = outputs.max(1)
                total += batch_y.size(0)
                correct += predicted.eq(batch_y).sum().item()
            
            accuracy = 100.0 * correct / total
            history.append(accuracy)
            
            if (epoch + 1) % 10 == 0:
                print(f"এপোক {epoch+1}/{epochs}: "
                      f"লস={epoch_loss/len(loader):.4f}, "
                      f"অ্যাকুরেসি={accuracy:.2f}%")
        
        return history
    
    def predict(self, time_series):
        """টাইম সিরিজের ট্রেন্ড প্রেডিক্ট"""
        self.model.eval()
        with torch.no_grad():
            x = torch.FloatTensor(time_series).reshape(1, 1, -1).to(device)
            outputs = self.model(x)
            probs = F.softmax(outputs, dim=-1)
            pred = outputs.argmax(dim=-1).item()
        
        labels = ['ডাউনট্রেন্ড 📉', 'সাইডওয়েজ ➡️', 'আপট্রেন্ড 📈']
        return {
            'prediction': labels[pred],
            'confidence': float(probs[0][pred]),
            'probabilities': {labels[i]: float(probs[0][i]) for i in range(3)}
        }

# ট্রেনিং
print("\n=== ফিন্যান্সিয়াল ResNet ট্রেনিং ===")
fin_resnet = FinancialResNet(seq_length=64, num_classes=3)
history = fin_resnet.train(epochs=30)

# প্রেডিকশন ডেমো
test_series = np.cumsum(np.random.randn(64)) * 0.1 + np.linspace(0, 1, 64)
result = fin_resnet.predict(test_series)
print(f"\nটেস্ট সিরিজ প্রেডিকশন:")
print(f"প্রেডিকশন: {result['prediction']}")
print(f"কনফিডেন্স: {result['confidence']:.2%}")
```

## 5. ResNet আর্কিটেকচার ভারিয়েন্টস

```python
class ResNetVariants:
    """ResNet আর্কিটেকচারের বিভিন্ন ভারিয়েন্ট"""
    
    @staticmethod
    def resnet_configs():
        """ResNet কনফিগারেশন"""
        configs = {
            'ResNet-18':  {'layers': [2, 2, 2, 2], 'block': 'Basic', 'params': '11M'},
            'ResNet-34':  {'layers': [3, 4, 6, 3], 'block': 'Basic', 'params': '22M'},
            'ResNet-50':  {'layers': [3, 4, 6, 3], 'block': 'Bottleneck', 'params': '26M'},
            'ResNet-101': {'layers': [3, 4, 23, 3], 'block': 'Bottleneck', 'params': '45M'},
            'ResNet-152': {'layers': [3, 8, 36, 3], 'block': 'Bottleneck', 'params': '60M'}
        }
        
        print("=== ResNet কনফিগারেশন ===")
        for name, config in configs.items():
            print(f"{name}: {config['block']} ব্লক, "
                  f"লেয়ার={config['layers']}, "
                  f"প্যারামিটার={config['params']}")
    
    @staticmethod
    def why_residual_works():
        """কেন রেসিডুয়াল কানেকশন কাজ করে"""
        print("""
=== কেন রেসিডুয়াল কানেকশন কাজ করে? ===

1️⃣ গ্রেডিয়েন্ট ফ্লো
   - শর্টকাট কানেকশন গ্রেডিয়েন্টকে সরাসরি প্রবাহিত করতে দেয়
   - dL/dx = dL/dH · (dF/dx + 1) → গ্রেডিয়েন্ট কখনোই শূন্য হয় না

2️⃣ আইডেন্টিটি ম্যাপিং
   - নেটওয়ার্ক F(x) = 0 শিখতে পারে = আইডেন্টিটি ফাংশন
   - নতুন লেয়ার বেসলাইন থেকে ডিভিয়েশন শেখে

3️⃣ এনসেম্বল ইফেক্ট
   - ResNet অনেকগুলো শ্যালো নেটওয়ার্কের এনসেম্বলের মতো
   - ড্রপপাথ: ট্রেনিংয়ের সময় কিছু পাথ ড্রপ হয়

4️⃣ প্রি-কন্ডিশনিং
   - রেসিডুয়াল ম্যাপিং অপ্টিমাইজেশনকে সহজ করে
   - লস ল্যান্ডস্কেপ স্মুথার হয়
""")

ResNetVariants.resnet_configs()
ResNetVariants.why_residual_works()
```

## সারাংশ
- ResNet রেসিডুয়াল কানেকশন দিয়ে গ্রেডিয়েন্ট ভ্যানিশিং সমস্যা সমাধান করে
- H(x) = F(x) + x — আইডেন্টিটি শর্টকাট কানেকশন
- Basic ব্লক (ResNet-18/34) এবং Bottleneck ব্লক (ResNet-50+) রয়েছে
- 152 লেয়ার পর্যন্ত ট্রেন করা সম্ভব
- ফিন্যান্সে টাইম সিরিজ প্যাটার্ন ডিটেকশনে কার্যকর
- Transfer learning এবং ফাইন-টিউনিংয়ে ResNet খুব জনপ্রিয়