# Day 54: মডেল প্রুনিং — মডেল কম্প্রেশন ✂️📉

## মডেল প্রুনিং কী?
প্রুনিং হল নিউরাল নেটওয়ার্ক থেকে অপ্রয়োজনীয় ওয়েট বা নিউরন সরিয়ে ফেলা — মডেল সাইজ কমানো এবং ইনফারেন্স স্পিড বাড়ানো।

### প্রুনিংয়ের ধরন
1. **Weight Pruning**: ছোট ওয়েট (≈0) সরানো
2. **Neuron/Unit Pruning**: সম্পূর্ণ নিউরন সরানো
3. **Structured Pruning**: সম্পূর্ণ চ্যানেল/লেয়ার সরানো
4. **Unstructured Pruning**: র‍্যান্ডম ওয়েট সরানো (স্পার্স ম্যাট্রিক্স)

### প্রুনিং প্রক্রিয়া
```
ট্রেন →  প্রুন →  ফাইন-টিউন  (Iterative)
  ↑_______________________|
```

### ফিন্যান্সে প্রুনিং
- প্রোডাকশনে মডেল ডিপ্লয়মেন্টের জন্য মডেল সাইজ কমানো
- রিয়েল-টাইম ট্রেডিং সিস্টেমে লেটেন্সি কমানো
- এজ ডিভাইসে ডিপ্লয়মেন্ট (মোবাইল, IoT)
- কস্ট সেভিং (GPU/CPU খরচ কমানো)

## প্রুনিং ইমপ্লিমেন্টেশন (PyTorch)

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

## 1. সিম্পল নেটওয়ার্ক (প্রুনিংয়ের জন্য)

```python
class SimpleNet(nn.Module):
    """প্রুনিং ডেমোর জন্য সিম্পল নেটওয়ার্ক"""
    def __init__(self, input_dim=10, hidden_dim=64, num_classes=3):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = SimpleNet().to(device)
print(f"মডেল তৈরি: {sum(p.numel() for p in model.parameters()):,} প্যারামিটার")
print(model)
```

## 2. বেসিক ওয়েট প্রুনিং

```python
class BasicPruning:
    """বেসিক ম্যাগনিচিউড-বেসড প্রুনিং"""
    
    @staticmethod
    def magnitude_prune(model, prune_percent=30):
        """ম্যাগনিচিউড-বেসড প্রুনিং (ছোট ওয়েট সরান)"""
        pruned_model = type(model)().to(device)
        pruned_model.load_state_dict(model.state_dict())
        
        total_params = 0
        pruned_params = 0
        masks = {}
        
        for name, param in pruned_model.named_parameters():
            if 'weight' in name and param.dim() >= 2:
                total_params += param.numel()
                
                # থ্রেশহোল্ড নির্ধারণ (abs value percentile)
                threshold = np.percentile(param.abs().cpu().detach().numpy(), prune_percent)
                
                # মাস্ক তৈরি
                mask = (param.abs() > threshold).float()
                masks[name] = mask
                
                # প্রুনিং
                param.data *= mask
                pruned_params += (1 - mask).sum().item()
                
                print(f"  {name}: pruned {pruned_params}/{total_params} "
                      f"({100*pruned_params/total_params:.1f}%)")
        
        print(f"\nমোট প্রুনড: {100*pruned_params/total_params:.1f}% ({pruned_params:,}/{total_params:,})")
        return pruned_model, masks
    
    @staticmethod
    def count_zero_weights(model):
        """জিরো ওয়েট কাউন্ট"""
        total = 0
        zeros = 0
        for param in model.parameters():
            if param.dim() >= 2:
                total += param.numel()
                zeros += (param == 0).sum().item()
        return zeros, total, 100 * zeros / total if total > 0 else 0

# ডেমো
print("\n=== ওয়েট প্রুনিং ডেমো ===")
pruned_model, masks = BasicPruning.magnitude_prune(model, prune_percent=40)
zeros, total, pct = BasicPruning.count_zero_weights(pruned_model)
print(f"\nপ্রুনিংয়ের পর জিরো ওয়েট: {zeros}/{total} ({pct:.1f}%)")
```

## 3. স্ট্রাকচার্ড চ্যানেল প্রুনিং

```python
class StructuredPruning:
    """স্ট্রাকচার্ড চ্যানেল/নিউরন প্রুনিং"""
    
    @staticmethod
    def neuron_prune(model, prune_percent=30):
        """L1-norm ভিত্তিক নিউরন প্রুনিং"""
        pruned_model = type(model)().to(device)
        pruned_model.load_state_dict(model.state_dict())
        
        for name, param in pruned_model.named_parameters():
            if 'weight' in name and param.dim() == 2:  # Linear layers
                # L1-norm অফ আউটপুট নিউরন
                l1_norms = torch.norm(param.data, p=1, dim=0)
                
                # সবচেয়ে ছোট নিউরন প্রুন
                threshold = np.percentile(l1_norms.cpu().numpy(), prune_percent)
                mask = (l1_norms > threshold).float()
                
                # মাস্ক প্রয়োগ (সম্পূর্ণ নিউরন জিরো)
                param.data *= mask.unsqueeze(0)
                
                n_pruned = (1 - mask).sum().item()
                print(f"  {name}: {n_pruned} নিউরন প্রুনড (মোট {param.shape[1]})")
        
        return pruned_model
    
    @staticmethod
    def l1_channel_prune(model, prune_percent=30):
        """L1-norm চ্যানেল প্রুনিং (Conv layers)"""
        pruned_model = type(model)().to(device)
        pruned_model.load_state_dict(model.state_dict())
        
        for name, param in pruned_model.named_parameters():
            if 'weight' in name and param.dim() == 3:  # Conv1d
                # প্রতিটি আউটপুট চ্যানেলের L1-norm
                l1_norms = torch.norm(param.data.view(param.shape[0], -1), p=1, dim=1)
                
                threshold = np.percentile(l1_norms.cpu().numpy(), prune_percent)
                mask = (l1_norms > threshold).float()
                
                # মাস্ক প্রয়োগ
                param.data *= mask.view(-1, 1, 1)
                
                n_pruned = (1 - mask).sum().item()
                print(f"  {name}: {n_pruned} চ্যানেল প্রুনড (মোট {param.shape[0]})")
        
        return pruned_model

# ডেমো
print("\n=== স্ট্রাকচার্ড প্রুনিং ডেমো ===")
sp_model = StructuredPruning.neuron_prune(model, prune_percent=30)
```

## 4. পোস্ট-প্রুনিং ফাইন-টিউনিং

```python
class PruningPipeline:
    """সম্পূর্ণ প্রুনিং পাইপলাইন (ট্রেন → প্রুন → ফাইন-টিউন)"""
    
    def __init__(self, model_class, input_dim=10, hidden_dim=64, num_classes=3):
        self.model_class = model_class
        self.num_classes = num_classes
        self.input_dim = input_dim
        
        self.model = model_class(input_dim, hidden_dim, num_classes).to(device)
        self.criterion = nn.CrossEntropyLoss()
    
    def train(self, epochs=30):
        """মডেল ট্রেন"""
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        
        # সিন্থেটিক ডেটা
        X = torch.randn(500, self.input_dim).to(device)
        y = torch.randint(0, self.num_classes, (500,)).to(device)
        
        self.model.train()
        initial_params = sum(p.numel() for p in self.model.parameters())
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X)
            loss = self.criterion(outputs, y)
            loss.backward()
            optimizer.step()
        
        accuracy = self._evaluate(X, y)
        params = sum(p.numel() for p in self.model.parameters())
        print(f"প্রি-প্রুন অ্যাকুরেসি: {accuracy:.2f}%, প্যারামিটার: {params:,}")
        return accuracy
    
    def _evaluate(self, X, y):
        """এভালুয়েশন"""
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(X)
            _, predicted = outputs.max(1)
            correct = predicted.eq(y).sum().item()
        return 100.0 * correct / len(y)
    
    def prune_and_finetune(self, prune_percent=30, finetune_epochs=10):
        """প্রুন + ফাইন-টিউন"""
        # প্রুনিং আগে অ্যাকুরেসি
        X = torch.randn(500, self.input_dim).to(device)
        y = torch.randint(0, self.num_classes, (500,)).to(device)
        pre_acc = self._evaluate(X, y)
        
        # ম্যাগনিচিউড প্রুনিং
        masked_model, masks = BasicPruning.magnitude_prune(self.model, prune_percent)
        post_prune_acc = self._evaluate(masked_model, X, y) if hasattr(self, '_evaluate') else 0
        
        print(f"\nপ্রুনিং ইফেক্ট:")
        print(f"  আগে: {pre_acc:.2f}%")
        print(f"  প্রুনিং পর: {post_prune_acc:.2f}%")
        
        # ফাইন-টিউনিং
        optimizer = optim.Adam(masked_model.parameters(), lr=0.001)
        
        for epoch in range(finetune_epochs):
            optimizer.zero_grad()
            outputs = masked_model(X)
            loss = self.criterion(outputs, y)
            
            # মাস্কযুক্ত ওয়েট আপডেট না করা
            loss.backward()
            
            # মাস্ক পুনরায় প্রয়োগ (প্রুনড ওয়েট জিরো রাখা)
            with torch.no_grad():
                for name, param in masked_model.named_parameters():
                    if name in masks:
                        param.grad *= masks[name]
            
            optimizer.step()
            
            # প্রুনড ওয়েট জিরো রাখা
            with torch.no_grad():
                for name, param in masked_model.named_parameters():
                    if name in masks:
                        param.data *= masks[name]
        
        final_acc = self._evaluate(X, y)
        zeros, total, pct = BasicPruning.count_zero_weights(masked_model)
        
        print(f"  ফাইন-টিউন পর: {final_acc:.2f}%")
        print(f"  স্পারসিটি: {pct:.1f}% ({zeros:,}/{total:,})")
        
        return masked_model, final_acc

# ডেমো
print("\n=== প্রুনিং পাইপলাইন ===")
pipeline = PruningPipeline(SimpleNet, input_dim=10, hidden_dim=64, num_classes=3)
pipeline.train(epochs=20)
pipeline.prune_and_finetune(prune_percent=50, finetune_epochs=10)
```

## 5. লটারি টিকেট হাইপোথিসিস

```python
class LotteryTicketDemo:
    """লটারি টিকেট হাইপোথিসিস ডেমো"""
    
    @staticmethod
    def lottery_ticket_concept():
        """লটারি টিকেট হাইপোথিসিস ব্যাখ্যা"""
        print("""
=== লটারি টিকেট হাইপোথিসিস (LTH) ===

সাবওয়ার্ক: একটি র‍্যান্ডমলি ইনিশিয়ালাইজড নেটওয়ার্কে
একটি সাবনেটওয়ার্ক থাকে যা নিজে থেকেই ট্রেনিং করলে
বড় নেটওয়ার্কের সমান বা ভাল পারফরম্যান্স দেয়।

প্রক্রিয়া:
1️⃣ র‍্যান্ডম ইনিশিয়ালাইজেশন (সংরক্ষণ করুন)
2️⃣ ট্রেন করুন
3️⃣ প্রুন করুন (যেমন 50% ছোট ওয়েট)
4️⃣ বাকি ওয়েট রিসেট করুন (ইনিশিয়াল ভ্যালুতে)
5️⃣ পুনরায় ট্রেন করুন

রেজাল্ট: প্রুনড নেটওয়ার্ক ফুল নেটওয়ার্কের সমান ভাল!
""")
    
    @staticmethod
    def iterative_pruning_vs_one_shot():
        """Iterative vs One-shot প্রুনিং"""
        print("""
=== Iterative vs One-shot প্রুনিং ===

One-shot Pruning (একবারে):
  - একবারে 50-90% ওয়েট প্রুন
  - সমস্যা: বড় অ্যাকুরেসি ড্রপ
  - দ্রুত

Iterative Pruning (পুনরাবৃত্তি):
  - প্রতি ইটারেশনে 10-20% প্রুন
  - প্রতিবার ফাইন-টিউন
  - বেশি এফেক্টিভ (উচ্চ স্পারসিটি)
  - বেশি সময় লাগে

স্ট্রাটেজি:
  Train → Prune (10%) → Fine-tune → 
  Prune (10%) → Fine-tune → ... 
  → Target sparsity reached
""")

LotteryTicketDemo.lottery_ticket_concept()
LotteryTicketDemo.iterative_pruning_vs_one_shot()
```

## প্রুনিং বেস্ট প্র্যাকটিস

```python
def pruning_best_practices():
    """প্রুনিং বেস্ট প্র্যাকটিস"""
    print("""
=== প্রুনিং বেস্ট প্র্যাকটিস ===

1️⃣ শুরুতে বেশি প্রুন করবেন না
   - স্ট্রাকচার্ড প্রুনিং: 10-20% → ফাইন-টিউন → আরও
   - আনস্ট্রাকচার্ড প্রুনিং: 50% পর্যন্ত ঠিক আছে

2️⃣ ফাইন-টিউনিং অত্যাবশ্যক
   - প্রুনিংয়ের পর ছোট LR দিয়ে ফাইন-টিউন
   - 10-20 এপোক যথেষ্ট

3️⃣ গুরুত্বপূর্ণ লেয়ার কম প্রুন করুন
   - প্রথম এবং শেষ লেয়ার কম প্রুন
   - মিডল লেয়ার বেশি প্রুন করা যায়

4️⃣ টার্গেট স্পারসিটি নির্ধারণ
   - 50-80%: নিরাপদ (ছোট অ্যাকুরেসি ড্রপ)
   - 90%+: অ্যাগ্রেসিভ (ফাইন-টিউনিং প্রয়োজন)

5️⃣ হার্ডওয়্যার সুবিধা
   - স্ট্রাকচার্ড প্রুনিং: GPU/CPU এ্যাক্সিলারেশন
   - আনস্ট্রাকচার্ড প্রুনিং: স্পার্স ম্যাট্রিক্স অপারেশন দরকার

6️⃣ ফিন্যান্স ইউজ কেস
   - লো-লেটেন্সি ট্রেডিং: 2-3x স্পিডআপ
   - মোবাইল ট্রেডিং অ্যাপ: 5-10x মডেল সাইজ রিডাকশন
   - ক্লাউড কস্ট: 50-80% কম্পিউট কমানো
""")

pruning_best_practices()
```

## সারাংশ
- প্রুনিং অপ্রয়োজনীয় ওয়েট/নিউরন সরিয়ে মডেল কম্প্রেস করে
- ম্যাগনিচিউড-বেসড প্রুনিং সবচেয়ে সিম্পল এবং এফেক্টিভ
- স্ট্রাকচার্ড প্রুনিং হার্ডওয়্যার ফ্রেন্ডলি (স্পিডআপ দেয়)
- প্রুনিংয়ের পর ফাইন-টিউনিং অপরিহার্য
- লটারি টিকেট হাইপোথিসিস দেখায় ছোট নেটওয়ার্কও ভাল হতে পারে
- Iterative pruning (10-20% প্রতি রাউন্ড) best practice
- ফিন্যান্সে লেটেন্সি এবং কস্ট কমানোর জন্য প্রুনিং গুরুত্বপূর্ণ