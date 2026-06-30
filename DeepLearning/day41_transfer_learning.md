# Day 41: ট্রান্সফার লার্নিং 🔄

## ট্রান্সফার লার্নিং কী?
প্রি-ট্রেইনড মডেলকে নতুন টাস্কে অ্যাডাপ্ট করা। এটি কম ডেটায় দ্রুত শিখতে সাহায্য করে।

### ফিন্যান্সে ট্রান্সফার লার্নিং
1. **সেন্টিমেন্ট অ্যানালাইসিস**: BERT ফাইন-টিউনিং
2. **ফ্রড ডিটেকশন**: ইমেজ নেট প্রি-ট্রেইনড CNN
3. **টাইম সিরিজ**: স্টক প্রেডিকশনে ট্রান্সফার
4. **ইমেজ-ভিত্তিক ট্রেডিং**: চার্ট প্যাটার্ন রিকগনিশন

## PyTorch ট্রান্সফার লার্নিং

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# প্রি-ট্রেইনড মডেল সিমুলেশন
class PretrainedModel(nn.Module):
    """প্রি-ট্রেইনড বেস মডেল (সিমুলেটেড)"""
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Linear(100, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU()
        )
        self.classifier = nn.Linear(64, 10)
    
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

pretrained = PretrainedModel()

# 1. ফিচার এক্সট্র্যাক্টর (ব্যাকবোন ফ্রিজ)
class FeatureExtractor(nn.Module):
    """ফিচার এক্সট্র্যাক্টর ট্রান্সফার"""
    def __init__(self, pretrained, num_classes=3):
        super().__init__()
        # ফিচার লেয়ার ফ্রিজ
        self.features = pretrained.features
        for param in self.features.parameters():
            param.requires_grad = False
        
        # নতুন ক্লাসিফায়ার হেড
        self.classifier = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes)
        )
    
    def forward(self, x):
        with torch.no_grad():  # ফিচার লেয়ারে গ্র্যাডিয়েন্ট বন্ধ
            x = self.features(x)
        return self.classifier(x)

# 2. ফাইন-টিউনিং (সকল লেয়ার আনফ্রিজ)
class FineTunedModel(nn.Module):
    """ফাইন-টিউনড মডেল"""
    def __init__(self, pretrained, num_classes=3, freeze_ratio=0.5):
        super().__init__()
        self.features = pretrained.features
        self.classifier = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# মডেল সাইজ তুলনা
fe_model = FeatureExtractor(pretrained, num_classes=3)
ft_model = FineTunedModel(pretrained, num_classes=3)

fe_trainable = sum(p.numel() for p in fe_model.parameters() if p.requires_grad)
ft_trainable = sum(p.numel() for p in ft_model.parameters() if p.requires_grad)
total = sum(p.numel() for p in ft_model.parameters())

print(f"ফিচার এক্সট্র্যাক্টর ট্রেইনেবল: {fe_trainable:,}")
print(f"ফাইন-টিউনিং ট্রেইনেবল: {ft_trainable:,}")
print(f"মোট প্যারামিটার: {total:,}")
print(f"ট্রেইনেবল রেশিও: {fe_trainable/total:.1%} vs {ft_trainable/total:.1%}")
```

## ফিন্যান্স: BERT সেন্টিমেন্ট ট্রান্সফার

```python
class FinancialSentimentModel(nn.Module):
    """BERT-স্টাইল সেন্টিমেন্ট মডেল"""
    def __init__(self, vocab_size=10000, embed_dim=128, num_classes=3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=4, dim_feedforward=512),
            num_layers=2
        )
        # প্রি-ট্রেইনড লেয়ার (ফ্রিজড)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.classifier = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        embedded = self.embedding(x).permute(1, 0, 2)  # (seq, batch, embed)
        encoded = self.transformer(embedded)
        encoded = encoded.permute(1, 2, 0)  # (batch, embed, seq)
        pooled = self.pool(encoded).squeeze(-1)
        return self.classifier(pooled)

# সিমুলেটেড ফিন্যান্সিয়াল টেক্সট
print("ফাইন্যান্সিয়াল সেন্টিমেন্ট মডেল:")
print(f"  BERT-স্টাইল ট্রান্সফার লার্নিং")
print(f"  ক্লাসেস: নেগেটিভ, নিউট্রাল, পজিটিভ")
print(f"  ডোমেন: ফিন্যান্সিয়াল নিউজ অ্যানালাইসিস")
```

## ডোমেইন অ্যাডাপ্টেশন

```python
class DomainAdapter(nn.Module):
    """ডোমেইন অ্যাডাপ্টেশন লেয়ার"""
    def __init__(self, input_dim=64, adaptation_dim=32):
        super().__init__()
        self.domain_classifier = nn.Sequential(
            nn.Linear(input_dim, adaptation_dim),
            nn.ReLU(),
            nn.Linear(adaptation_dim, 2)  # 2 ডোমেইন
        )
        self.gradient_reversal = None  # GRL (Gradient Reversal Layer)
    
    def forward(self, features):
        return self.domain_classifier(features)

# সিন্থেটিক ডোমেইন ডেটা
np.random.seed(42)
source_data = np.random.randn(1000, 64) + 0.5  # সোর্স ডোমেইন
target_data = np.random.randn(200, 64) * 1.2    # টার্গেট ডোমেইন (শুধু ২০০)

print(f"ডোমেইন অ্যাডাপ্টেশন:")
print(f"  সোর্স ডোমেইন: {source_data.shape} (প্রচুর ডেটা)")
print(f"  টার্গেট ডোমেইন: {target_data.shape} (সীমিত ডেটা)")
print(f"  গোল: সোর্স থেকে টার্গেটে নলেজ ট্রান্সফার")

# ডোমেইন শিফট মেজার
source_mean = source_data.mean(axis=0)
target_mean = target_data.mean(axis=0)
domain_shift = np.linalg.norm(source_mean - target_mean)
print(f"  ডোমেইন শিফট ম্যাগনিটিউড: {domain_shift:.4f}")
```

## ট্রান্সফার লার্নিং স্ট্র্যাটেজি

```python
class TransferStrategy:
    """ট্রান্সফার লার্নিং স্ট্র্যাটেজি"""
    
    @staticmethod
    def feature_extractor(feature_layer, new_classifier):
        """শুধু ফিচার এক্সট্র্যাকশন"""
        for param in feature_layer.parameters():
            param.requires_grad = False
        return nn.Sequential(feature_layer, new_classifier)
    
    @staticmethod
    def fine_tune(model, freeze_layers=2):
        """ফাইন-টিউন (আংশিক ফ্রিজ)"""
        layers = list(model.children())
        for layer in layers[:freeze_layers]:
            for param in layer.parameters():
                param.requires_grad = False
        return model
    
    @staticmethod
    def gradual_unfreeze(model, epoch, max_epochs):
        """ধীরে ধীরে আনফ্রিজ"""
        layers = list(model.children())
        freeze_until = max(0, len(layers) - 
                          int(epoch / max_epochs * len(layers)))
        for i, layer in enumerate(layers):
            requires_grad = i >= freeze_until
            for param in layer.parameters():
                param.requires_grad = requires_grad
        return model

strategy = TransferStrategy()

# ডেমো: বিভিন্ন স্ট্র্যাটেজি
print(f"\nট্রান্সফার লার্নিং স্ট্র্যাটেজিস:")
print(f"  1. ফিচার এক্সট্র্যাক্টর: শুধু হেড ট্রেন")
print(f"  2. ফাইন-টিউনিং: সব লেয়ার ট্রেন")
print(f"  3. গ্র্যাজুয়াল আনফ্রিজ: ধীরে ধীরে")
print(f"  4. ডোমেইন অ্যাডাপ্টেশন: ডোমেইন শিফট কমানো")
```

## ট্রান্সফার লার্নিং টিপস

```python
tips = """
ফিন্যান্সে ট্রান্সফার লার্নিং টিপস:

1. কত লেয়ার ফ্রিজ করবেন?
   - ছোট ডেটাসেট: বেশিরভাগ ফ্রিজ
   - মাঝারি ডেটাসেট: হাফ ফ্রিজ
   - বড় ডেটাসেট: সামান্য ফ্রিজ

2. লার্নিং রেট
   - ফ্রিজড লেয়ার: N/A
   - আনফ্রিজড লেয়ার: ছোট lr (1e-5 to 1e-4)
   - নতুন হেড: স্বাভাবিক lr (1e-3)

3. কখন ফাইন-টিউন করবেন?
   - টার্গেট ডেটা সোর্সের মতো হলে
   - পর্যাপ্ত লেবেলড ডেটা থাকলে
   - আউট-অফ-ডিস্ট্রিবিউশন ডেটার জন্য

4. প্রি-ট্রেইনড মডেল সোর্স
   - ইমেজ: ImageNet, ResNet
   - NLP: BERT, RoBERTa, FinBERT
   - টাইম সিরিজ: জেনেরিক প্যাটার্ন
"""

print(tips)
```

## সারাংশ
- ট্রান্সফার লার্নিং প্রি-ট্রেইনড মডেলের নলেজ ব্যবহার করে
- ফিচার এক্সট্র্যাক্টর ও ফাইন-টিউনিং দুটি প্রধান পদ্ধতি
- ফিন্যান্সে সেন্টিমেন্ট, ফ্রড, ইমেজ রিকগনিশনে ব্যবহৃত
- ডোমেইন শিফট থাকলে ডোমেইন অ্যাডাপ্টেশন প্রয়োজন
- ডেটার পরিমাণ অনুযায়ী ফ্রিজ/আনফ্রিজ স্ট্র্যাটেজি নির্বাচন