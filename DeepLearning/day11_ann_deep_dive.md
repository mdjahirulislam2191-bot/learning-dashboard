# Day 11: ANN ডিপ ডাইভ 🧠

## আর্টিফিশিয়াল নিউরাল নেটওয়ার্ক (ANN) বিস্তারিত

ANN হল ডিপ লার্নিং-এর ভিত্তি। এটি ইনপুট, হিডেন ও আউটপুট লেয়ার নিয়ে গঠিত।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## বিভিন্ন আর্কিটেকচার
```python
class ANN_Variants:
    """ANN-এর বিভিন্ন ভ্যারিয়েন্ট"""
    
    @staticmethod
    def shallow(input_size=10, output_size=1):
        """Shallow NN (1 হিডেন লেয়ার)"""
        return nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, output_size)
        )
    
    @staticmethod
    def deep(input_size=10, output_size=1):
        """Deep NN (3+ হিডেন লেয়ার)"""
        return nn.Sequential(
            nn.Linear(input_size, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 16), nn.ReLU(),
            nn.Linear(16, output_size)
        )
    
    @staticmethod
    def wide(input_size=10, output_size=1):
        """Wide NN (প্রশস্ত লেয়ার)"""
        return nn.Sequential(
            nn.Linear(input_size, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, output_size)
        )
    
    @staticmethod
    def custom(input_size, output_size, layer_dims, activation=nn.ReLU):
        """কাস্টম লেয়ার ডাইমেনশন"""
        layers = []
        prev = input_size
        for dim in layer_dims:
            layers.append(nn.Linear(prev, dim))
            layers.append(activation())
            prev = dim
        layers.append(nn.Linear(prev, output_size))
        return nn.Sequential(*layers)

# উদাহরণ
model = ANN_Variants.custom(5, 1, [64, 32, 16], nn.ReLU)
print(f"কাস্টম মডেল:\n{model}")
print(f"প্যারামিটার সংখ্যা: {sum(p.numel() for p in model.parameters())}")
```

## ওয়েট ইনিশিয়ালাইজেশন
```python
class WeightInit:
    """বিভিন্ন ওয়েট ইনিশিয়ালাইজেশন"""
    
    @staticmethod
    def xavier(m):
        """Xavier/Glorot initialization"""
        if isinstance(m, nn.Linear):
            nn.init.xavier_uniform_(m.weight)
            nn.init.zeros_(m.bias)
    
    @staticmethod
    def he(m):
        """He/Kaiming initialization (ReLU-র জন্য)"""
        if isinstance(m, nn.Linear):
            nn.init.kaiming_uniform_(m.weight, nonlinearity='relu')
            nn.init.zeros_(m.bias)
    
    @staticmethod
    def normal(m, mean=0.0, std=0.01):
        """Normal initialization"""
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=mean, std=std)
            nn.init.zeros_(m.bias)

# He initialization দিয়ে মডেল
model = ANN_Variants.deep(5, 1)
model.apply(WeightInit.he)
print("He initialization applied")
```

## ফিন্যান্স: ক্রেডিট রিস্ক মডেলিং
```python
class CreditRiskModel(nn.Module):
    """ক্রেডিট রিস্ক অ্যাসেসমেন্ট ANN"""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(8, 32), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(32, 16), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(16, 8), nn.ReLU(),
            nn.Linear(8, 1), nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.net(x)

# ফিচার: [Income, Debt, Age, Credit_History, Loan_Amount,
#           Employment_Years, DTI_Ratio, Num_Accounts]
sample = torch.randn(10, 8)  # 10 জন ক্লায়েন্ট
model = CreditRiskModel()
risk_scores = model(sample)
print(f"ক্রেডিট রিস্ক স্কোর:\n{risk_scores}")
print(f"ডিফল্ট প্রোবাবিলিটি: {risk_scores.mean().item():.2%}")
```

## Underfitting vs Overfitting
```python
def demonstrate_fitting():
    """আন্ডারফিটিং ও ওভারফিটিং ডেমোনস্ট্রেশন"""
    np.random.seed(42)
    
    # সিন্থেটিক ডেটা
    X = np.linspace(-3, 3, 100).reshape(-1, 1)
    y = np.sin(X) + np.random.randn(100, 1) * 0.1
    
    X_t = torch.FloatTensor(X)
    y_t = torch.FloatTensor(y)
    
    # আন্ডারফিট (খুব ছোট মডেল)
    underfit = nn.Sequential(nn.Linear(1, 2), nn.ReLU(), nn.Linear(2, 1))
    
    # গুড ফিট
    goodfit = nn.Sequential(
        nn.Linear(1, 16), nn.ReLU(),
        nn.Linear(16, 16), nn.ReLU(),
        nn.Linear(16, 1)
    )
    
    # ওভারফিট (খুব বড় মডেল)
    overfit = nn.Sequential(
        nn.Linear(1, 256), nn.ReLU(),
        nn.Linear(256, 256), nn.ReLU(),
        nn.Linear(256, 128), nn.ReLU(),
        nn.Linear(128, 1)
    )
    
    models = {'Underfit': underfit, 'Good': goodfit, 'Overfit': overfit}
    
    for name, model in models.items():
        opt = optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
        
        for _ in range(2000):
            opt.zero_grad()
            loss = criterion(model(X_t), y_t)
            loss.backward()
            opt.step()
        
        pred = model(X_t).detach().numpy()
        print(f"{name}: Loss={loss.item():.4f}, Parameters={sum(p.numel() for p in model.parameters())}")

demonstrate_fitting()
```

## হাইপারপ্যারামিটার সিলেকশন
```python
def suggest_architecture(n_features, n_samples):
    """ডেটার ভিত্তিতে আর্কিটেকচার সাজেস্ট"""
    base_neurons = min(64, n_samples // 10)
    
    if n_features < 5:
        layers = [base_neurons, base_neurons // 2]
    elif n_features < 20:
        layers = [base_neurons * 2, base_neurons, base_neurons // 2]
    else:
        layers = [base_neurons * 4, base_neurons * 2, base_neurons, base_neurons // 2]
    
    return layers

# ফিন্যান্স ডেটার জন্য সাজেশন
n_features = 10  # ১০টি ফিন্যান্সিয়াল ফিচার
n_samples = 5000  # ৫০০০ স্যাম্পল
suggested = suggest_architecture(n_features, n_samples)
print(f"সাজেস্টেড আর্কিটেকচার: {suggested}")
model = ANN_Variants.custom(n_features, 1, suggested)
print(f"টোটাল প্যারামিটার: {sum(p.numel() for p in model.parameters())}")
```

## সারসংক্ষেপ
- Shallow NN: ১ লেয়ার → সহজ কাজ
- Deep NN: ৩+ লেয়ার → জটিল কাজ
- Wide NN: প্রশস্ত লেয়ার → বেশি প্যারামিটার
- Weight initialization: He (ReLU), Xavier (Sigmoid/Tanh)
- Underfit vs Overfit: মডেল সাইজ নিয়ে ব্যালেন্স
- ফিন্যান্স: ক্রেডিট রিস্ক, ফ্রড ডিটেকশন, প্রাইস প্রেডিকশন