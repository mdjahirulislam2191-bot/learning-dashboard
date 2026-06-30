# Day 18: ইমেজ ক্লাসিফিকেশন 🏷️

## CNN ইমেজ ক্লাসিফিকেশন
ইমেজ ক্লাসিফিকেশন CNN-এর সবচেয়ে জনপ্রিয় অ্যাপ্লিকেশন। ফিন্যান্সে স্টক চার্ট প্যাটার্ন রিকগনিশনে ব্যবহার হয়।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
```

## CNN মডেল (বিখ্যাত আর্কিটেকচার)
```python
class SimpleCNN(nn.Module):
    """সিম্পল CNN for Image Classification"""
    def __init__(self, num_classes=10):
        super().__init__()
        
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 28→14
            
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 14→7
            
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 7→3
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(128 * 3 * 3, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

model = SimpleCNN()
print(model)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

## MNIST ডেটাসেট (সিন্থেটিক উদাহরণ)
```python
# সিন্থেটিক "চার্ট ইমেজ" ডেটাসেট
class SyntheticChartDataset:
    """স্টক চার্টের মতো সিন্থেটিক ইমেজ ডেটা"""
    
    @staticmethod
    def create_sample(pattern='uptrend', img_size=(28, 28)):
        img = np.zeros(img_size)
        x = np.linspace(0, 1, img_size[1])
        
        if pattern == 'uptrend':
            y = 0.3 + 0.4 * x + np.random.randn(img_size[1]) * 0.05
        elif pattern == 'downtrend':
            y = 0.7 - 0.4 * x + np.random.randn(img_size[1]) * 0.05
        elif pattern == 'volatile':
            y = 0.5 + 0.3 * np.sin(10 * x) + np.random.randn(img_size[1]) * 0.05
        elif pattern == 'head_shoulders':
            y = 0.5 + 0.3 * np.sin(3 * x * np.pi) + np.random.randn(img_size[1]) * 0.05
        else:  # sideways
            y = 0.5 + np.random.randn(img_size[1]) * 0.05
        
        # ইমেজে প্লট করা
        y_pixels = np.clip((y * img_size[0]).astype(int), 0, img_size[0]-1)
        for i in range(img_size[1]):
            img[y_pixels[i], i] = 1.0
        
        return img
    
    @staticmethod
    def create_dataset(n_samples=1000):
        patterns = ['uptrend', 'downtrend', 'volatile', 'sideways']
        X, y = [], []
        
        for _ in range(n_samples):
            pattern = np.random.choice(patterns)
            img = SyntheticChartDataset.create_sample(pattern)
            X.append(img)
            y.append(patterns.index(pattern))
        
        X = np.array(X, dtype=np.float32).reshape(-1, 1, 28, 28)
        y = np.array(y)
        
        return X, y, patterns

# ডেটাসেট তৈরি
X, y, patterns = SyntheticChartDataset.create_dataset(500)
print(f"Chart dataset: X={X.shape}, y={y.shape}")
print(f"Classes: {patterns}")

# এক স্যাম্পল ভিজুয়ালাইজ
fig, axes = plt.subplots(2, 4, figsize=(10, 5))
for i, pattern in enumerate(patterns):
    idx = np.where(y == i)[0][0]
    axes[0, i].imshow(X[idx, 0], cmap='gray')
    axes[0, i].set_title(pattern)
    axes[0, i].axis('off')
plt.show()
```

## ট্রেনিং ফাংশন
```python
def train_cnn(model, X_train, y_train, X_test, y_test, epochs=20):
    """CNN ট্রেনিং"""
    X_tr = torch.FloatTensor(X_train)
    y_tr = torch.LongTensor(y_train)
    X_te = torch.FloatTensor(X_test)
    y_te = torch.LongTensor(y_test)
    
    train_loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=32, shuffle=True)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # ইভালুয়েশন
        model.eval()
        X_te_t, y_te_t = X_te.to(device), y_te.to(device)
        with torch.no_grad():
            test_outputs = model(X_te_t)
            _, predicted = torch.max(test_outputs, 1)
            accuracy = (predicted == y_te_t).float().mean()
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}: Loss={total_loss/len(train_loader):.4f}, Acc={accuracy:.2%}")
    
    return model

# ট্রেনিং (বাস্তবায়ন)
# model = SimpleCNN(num_classes=4).to(device)
# train_cnn(model, X_train, y_train, X_test, y_test)
print("CNN মডেল ট্রেনিং কনফিগার করা হয়েছে")
```

## ট্রান্সফার লার্নিং (Pretrained Models)
```python
import torchvision.models as models

class TransferLearningDemo:
    """Pretrained মডেল দিয়ে ট্রান্সফার লার্নিং"""
    
    @staticmethod
    def create_model(num_classes=4):
        # ResNet18 লোড (pretrained on ImageNet)
        model = models.resnet18(pretrained=True)
        
        # ফ্রিজ ফিচার এক্সট্র্যাক্টর
        for param in model.parameters():
            param.requires_grad = False
        
        # নতুন ক্লাসিফায়ার হেড
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
        print(f"ResNet18 with new classifier ({num_classes} classes)")
        return model

# model = TransferLearningDemo.create_model()
print("Transfer Learning: Pretrained weights → Fine-tune on finance data")
```

## ফিন্যান্স: চার্ট প্যাটার্ন ক্লাসিফায়ার
```python
class ChartPatternClassifier:
    """স্টক চার্ট প্যাটার্ন ক্লাসিফিকেশন সিস্টেম"""
    
    def __init__(self):
        self.model = SimpleCNN(num_classes=5)
        self.patterns = ['Bull Flag', 'Bear Flag', 'Double Top', 'Double Bottom', 'Head & Shoulders']
    
    def prepare_chart_data(self, prices, seq_len=28):
        """প্রাইস ডেটা থেকে চার্ট ইমেজ তৈরি"""
        # নরমালাইজ
        prices_norm = (prices - prices.min()) / (prices.max() - prices.min() + 1e-8)
        
        # ইমেজে রূপান্তর
        img = np.zeros((seq_len, seq_len))
        scaled = (prices_norm * (seq_len - 1)).astype(int)
        
        for i in range(min(seq_len, len(scaled))):
            img[seq_len - 1 - scaled[i], i] = 1.0
        
        return img
    
    def predict_pattern(self, price_sequence):
        """প্রাইস সিকোয়েন্স থেকে প্যাটার্ন প্রেডিক্ট"""
        img = self.prepare_chart_data(price_sequence)
        img_tensor = torch.FloatTensor(img).unsqueeze(0).unsqueeze(0)
        
        self.model.eval()
        with torch.no_grad():
            output = self.model(img_tensor)
            probs = torch.softmax(output, dim=1)
            pred_idx = torch.argmax(probs, dim=1).item()
        
        return {
            'pattern': self.patterns[pred_idx],
            'confidence': probs[0, pred_idx].item(),
            'all_probs': {p: probs[0, i].item() for i, p in enumerate(self.patterns)}
        }

# classifier = ChartPatternClassifier()
# test_prices = np.cumsum(np.random.randn(28)) + 100
# result = classifier.predict_pattern(test_prices)
# print(f"Predicted: {result['pattern']} ({result['confidence']:.1%})")
print("চার্ট প্যাটার্ন ক্লাসিফায়ার তৈরি হয়েছে")
```

## সারসংক্ষেপ
- CNN ইমেজ ক্লাসিফিকেশনে অত্যন্ত কার্যকর
- Conv + Pooling + FC = স্ট্যান্ডার্ড আর্কিটেকচার
- Transfer Learning: Pretrained মডেল + Fine-tune
- ফিন্যান্সে: চার্ট প্যাটার্ন রিকগনিশন, স্টক স্ক্রিনিং
- CrossEntropyLoss + Adam = স্ট্যান্ডার্ড ট্রেনিং