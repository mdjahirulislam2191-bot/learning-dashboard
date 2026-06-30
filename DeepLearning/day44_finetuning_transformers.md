# Day 44: ট্রান্সফরমার ফাইন-টিউনিং 🔧

## ফাইন-টিউনিং কী?
প্রি-ট্রেইনড ট্রান্সফরমার মডেলকে নির্দিষ্ট ডোমেইন বা টাস্কের জন্য অ্যাডাপ্ট করা।

### ফাইন-টিউনিং স্ট্র্যাটেজি
1. **ফুল ফাইন-টিউনিং**: সব প্যারামিটার আপডেট
2. **হেড অনলি**: শুধু ক্লাসিফায়ার হেড ট্রেন
3. **লেয়ার-ওয়াইজ**: নির্দিষ্ট লেয়ার আনফ্রিজ
4. **LoRA**: লো-র্যাংক অ্যাডাপ্টেশন (প্যারামিটার-এফিশিয়েন্ট)

### ফিন্যান্স স্পেসিফিক ফাইন-টিউনিং
- ফিন্যান্সিয়াল টেক্সট (10-K, 10-Q, নিউজ)
- টাইম সিরিজ প্যাটার্ন
- ভলাটিলিটি প্রেডিকশন
- সেন্টিমেন্ট অ্যানালাইসিস

## ফাইন-টিউনিং ট্রান্সফরমার

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. প্রি-ট্রেইনড এনকোডার লোড

```python
# প্রি-ট্রেইনড মডেল লোড সিমুলেশন
class PretrainedTransformer(nn.Module):
    """প্রি-ট্রেইনড ট্রান্সফরমার এনকোডার"""
    def __init__(self, d_model=128, n_heads=8, num_layers=4):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=512,
            dropout=0.1, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.norm = nn.LayerNorm(d_model)
    
    def forward(self, x):
        return self.norm(self.transformer(x))

# প্রি-ট্রেইনড ওয়েট (সিমুলেটেড)
pretrained = PretrainedTransformer(d_model=128, n_heads=8, num_layers=4)

print(f"প্রি-ট্রেইনড মডেল লোডেড")
print(f"  d_model=128, n_heads=8, num_layers=4")
print(f"  প্যারামিটার: {sum(p.numel() for p in pretrained.parameters()):,}")
```

## 2. ফাইন-টিউনিং সেটআপ

```python
class FinancialTransformer(nn.Module):
    """ফাইন-টিউনড ফিন্যান্স ট্রান্সফরমার"""
    def __init__(self, pretrained_encoder, input_dim=10, 
                 num_classes=3, freeze_encoder=True):
        super().__init__()
        
        self.input_proj = nn.Linear(input_dim, 128)
        
        # প্রি-ট্রেইনড এনকোডার
        self.encoder = pretrained_encoder
        if freeze_encoder:
            for param in self.encoder.parameters():
                param.requires_grad = False
        
        # ফিন্যান্স-স্পেসিফিক হেড
        self.finance_head = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )
    
    def forward(self, x):
        x = self.input_proj(x)
        encoded = self.encoder(x)
        pooled = encoded.mean(dim=1)
        return self.finance_head(pooled)
    
    def unfreeze(self, num_layers=0):
        """নির্দিষ্ট সংখ্যক লেয়ার আনফ্রিজ"""
        if num_layers > 0:
            layers = list(self.encoder.transformer.layers)
            for layer in layers[-num_layers:]:
                for param in layer.parameters():
                    param.requires_grad = True

# মডেল
model = FinancialTransformer(pretrained, input_dim=10, num_classes=3, freeze_encoder=True)

# ফাইন-টিউনেবল প্যারামিটার
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)

print(f"ফাইন-টিউনিং কনফিগ:")
print(f"  ফ্রোজেন প্যারামিটার: {frozen:,}")
print(f"  ট্রেইনেবল প্যারামিটার: {trainable:,}")
print(f"  ট্রেইনেবল রেশিও: {trainable/(trainable+frozen)*100:.2f}%")
```

## 3. সিন্থেটিক ফিন্যান্সিয়াল ডেটা

```python
np.random.seed(42)
n_samples = 2000
seq_len = 30
n_features = 10
n_classes = 3

# ফিন্যান্সিয়াল টাইম সিরিজ ডেটা
X = np.random.randn(n_samples, seq_len, n_features)

# রেজিম-ভিত্তিক লেবেল (বুল/বিয়ার/নিউট্রাল)
trend = X[:, -1, 0] + 0.5 * X[:, -5, 1]
y = np.digitize(trend, bins=[-1, 1])  # 0, 1, 2

# ট্রেন/ভ্যাল/টেস্ট
split1, split2 = int(0.7*n_samples), int(0.85*n_samples)
X_train, X_val, X_test = X[:split1], X[split1:split2], X[split2:]
y_train, y_val, y_test = y[:split1], y[split1:split2], y[split2:]

# DataLoader
train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train)),
    batch_size=32, shuffle=True
)
val_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val)),
    batch_size=32
)

print(f"ডেটা প্রস্তুত:")
print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"  X_val: {X_val.shape}, y_val: {y_val.shape}")
print(f"  X_test: {X_test.shape}, y_test: {y_test.shape}")
```

## 4. ফাইন-টিউনিং ট্রেনিং

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(
    filter(lambda p: p.requires_grad, model.parameters()), 
    lr=1e-4, weight_decay=1e-5
)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)

epochs = 30
best_val_acc = 0

print("\nট্রান্সফরমার ফাইন-টিউনিং শুরু...")
for epoch in range(epochs):
    model.train()
    train_loss = 0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        pred = model(batch_X)
        loss = criterion(pred, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        train_loss += loss.item()
    
    # ভ্যালিডেশন
    model.eval()
    val_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for batch_X, batch_y in val_loader:
            pred = model(batch_X)
            loss = criterion(pred, batch_y)
            val_loss += loss.item()
            _, predicted = torch.max(pred, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
    
    val_acc = correct / total
    scheduler.step()
    
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'best_finetuned.pt')
    
    if (epoch + 1) % 5 == 0:
        print(f"  Epoch {epoch+1}: Train Loss={train_loss/len(train_loader):.4f}, "
              f"Val Acc={val_acc:.4f}")

print(f"\n✅ ফাইন-টিউনিং সম্পূর্ণ!")
print(f"সেরা ভ্যালিডেশন অ্যাকুরেসি: {best_val_acc:.4f}")
```

## 5. ফ্রিজিং স্ট্র্যাটেজি তুলনা

```python
def evaluate_strategy(freeze_strategy, name):
    """একটি ফ্রিজিং স্ট্র্যাটেজি ইভালুয়েট"""
    model = FinancialTransformer(pretrained, input_dim=10, num_classes=3)
    
    if freeze_strategy == 'full':
        # সব ফ্রিজড (শুধু হেড)
        pass
    elif freeze_strategy == 'half':
        # শেষ ২ লেয়ার আনফ্রিজ
        model.unfreeze(num_layers=2)
    elif freeze_strategy == 'none':
        # সব আনফ্রিজ
        for param in model.encoder.parameters():
            param.requires_grad = True
    
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()), 
        lr=1e-4
    )
    
    # সিম্পল ট্রেনিং
    for epoch in range(10):
        model.train()
        for bx, by in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(bx), by)
            loss.backward()
            optimizer.step()
    
    model.eval()
    with torch.no_grad():
        correct = sum((torch.max(model(X_test[:200]), 1)[1] == 
                      torch.LongTensor(y_test[:200])).sum().item())
        acc = correct / 200
    
    return trainable, acc

# তুলনা
strategies = ['full', 'half', 'none']
print(f"\nফ্রিজিং স্ট্র্যাটেজি তুলনা:")
print(f"{'স্ট্র্যাটেজি':<15} {'ট্রেইনেবল':<15} {'অ্যাকুরেসি':<15}")
print("-" * 45)

for strategy in strategies:
    trainable, acc = evaluate_strategy(strategy, strategy)
    print(f"{strategy:<15} {trainable:<15,} {acc:<15.4f}")
```

## 6. LoRA (Low-Rank Adaptation)

```python
class LoRALayer(nn.Module):
    """LoRA অ্যাডাপ্টেশন লেয়ার"""
    def __init__(self, original_layer, rank=8, alpha=16):
        super().__init__()
        self.original = original_layer
        self.rank = rank
        self.alpha = alpha
        
        d_model = original_layer.in_features
        self.lora_down = nn.Linear(d_model, rank, bias=False)
        self.lora_up = nn.Linear(rank, d_model, bias=False)
        
        # অরিজিনাল ফ্রিজ
        for param in self.original.parameters():
            param.requires_grad = False
    
    def forward(self, x):
        # অরিজিনাল + LoRA অ্যাডাপ্টেশন
        original_out = self.original(x)
        lora_out = self.lora_up(self.lora_down(x)) * (self.alpha / self.rank)
        return original_out + lora_out

class LoRAFineTunedModel(nn.Module):
    """LoRA সহ ফাইন-টিউনড মডেল"""
    def __init__(self, pretrained, input_dim=10, num_classes=3, lora_rank=8):
        super().__init__()
        
        self.input_proj = nn.Linear(input_dim, 128)
        self.encoder = pretrained
        
        # LoRA অ্যাডাপ্টেশন (প্রতি লেয়ারে)
        self.lora_layers = nn.ModuleList([
            LoRALayer(nn.Linear(128, 128), rank=lora_rank)
            for _ in range(4)
        ])
        
        self.fc = nn.Linear(128, num_classes)
    
    def forward(self, x):
        x = self.input_proj(x)
        for lora in self.lora_layers:
            x = lora(x)
        return self.fc(x.mean(dim=1))

lora_model = LoRAFineTunedModel(pretrained, input_dim=10, num_classes=3, lora_rank=8)
lora_params = sum(p.numel() for p in lora_model.parameters() if p.requires_grad)
full_params = sum(p.numel() for p in model.parameters())

print(f"\nLoRA ফাইন-টিউনিং:")
print(f"  LoRA ট্রেইনেবল: {lora_params:,}")
print(f"  ফুল ফাইন-টিউনিং ট্রেইনেবল: {full_params:,}")
print(f"  প্যারামিটার সেভিং: {(1 - lora_params/full_params)*100:.1f}%")
```

## ফাইন-টিউনিং বেস্ট প্র্যাকটিস

```python
tips = """
ফাইন-টিউনিং বেস্ট প্র্যাকটিস (ফিন্যান্স):

1. লার্নিং রেট
   - হেড অনলি: 1e-3 to 5e-4
   - ফুল ফাইন-টিউন: 2e-5 to 5e-5
   - LoRA: 1e-4 to 5e-4

2. ডেটা সাইজ
   - ছোট (<1000): হেড অনলি বা LoRA
   - মাঝারি (1000-10000): আংশিক আনফ্রিজ
   - বড় (>10000): ফুল ফাইন-টিউন

3. রেগুলারাইজেশন
   - ওয়েট ডিকেয়: 0.01-0.1
   - ড্রপআউট: 0.1-0.3
   - আর্লি স্টপিং: patience=5

4. ডোমেইন অ্যাডাপ্টেশন
   - ফিন্যান্স স্পেসিফিক প্রি-ট্রেনিং
   - ইন-ডোমেইন ডেটা অগমেন্টেশন
   - ডোমেইন অ্যাডভারসারিয়াল ট্রেনিং
"""

print(tips)
```

## সারাংশ
- ফাইন-টিউনিং প্রি-ট্রেইনড মডেলকে নির্দিষ্ট ডোমেইনে অ্যাডাপ্ট করে
- বিভিন্ন স্ট্র্যাটেজি: ফুল, হেড অনলি, স্তরায়িত, LoRA
- LoRA সবচেয়ে এফিশিয়েন্ট (১% প্যারামিটারেই ~৯০% পারফরম্যান্স)
- ফিন্যান্সে টেক্সট, টাইম সিরিজ, রিস্ক অ্যানালাইসিসে ব্যবহৃত
- লার্নিং রেট ও ডেটা সাইজ অনুযায়ী স্ট্র্যাটেজি সিলেক্ট করুন