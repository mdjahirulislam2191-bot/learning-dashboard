# Day 43: ট্রান্সফরমার (Transformer) 🏗️

## ট্রান্সফরমার কী?
ট্রান্সফরমার একটি আর্কিটেকচার যা শুধুমাত্র অ্যাটেনশন মেকানিজমের উপর ভিত্তি করে তৈরি (No RNN/CNN)। এটি ২০১৭ সালে Google-এর "Attention Is All You Need" পেপারে প্রস্তাবিত।

### ট্রান্সফরমার vs RNN/LSTM
| বৈশিষ্ট্য | RNN/LSTM | ট্রান্সফরমার |
|---|---|---|
| প্রসেসিং | সিকোয়েন্সিয়াল | প্যারালাল |
| অ্যাটেনশন | সহায়ক | মূল মেকানিজম |
| লং-রেঞ্জ | সীমিত | চমৎকার |
| ট্রেনিং টাইম | ধীর | দ্রুত (GPU-তে) |
| প্যারামিটার | কম | বেশি |

### ট্রান্সফরমারের মূল উপাদান
1. **সেল্ফ-অ্যাটেনশন (Multi-Head)**
2. **পজিশনাল এনকোডিং**
3. **ফিড-ফরোয়ার্ড নেটওয়ার্ক**
4. **লেয়ার নরমালাইজেশন**
5. **রেসিডুয়াল কানেকশন**

### ফিন্যান্স অ্যাপ্লিকেশন
- টাইম সিরিজ ফোরকাস্টিং
- ট্রেডিং সিগন্যাল জেনারেশন
- রিস্ক ম্যানেজমেন্ট
- পোর্টফোলিও অপ্টিমাইজেশন
- ফিন্যান্সিয়াল NLP

## PyTorch ট্রান্সফরমার ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math
```

## 1. সেল্ফ-অ্যাটেনশন

```python
class MultiHeadAttention(nn.Module):
    """মাল্টি-হেড অ্যাটেনশন"""
    def __init__(self, d_model=128, n_heads=8, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, query, key, value, mask=None):
        batch = query.size(0)
        
        # লিনিয়ার + হেডে বিভক্ত
        Q = self.W_q(query).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # অ্যাটেনশন স্কোর
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        
        # কনটেক্সট
        context = torch.matmul(attn, V)
        context = context.transpose(1, 2).contiguous().view(batch, -1, self.d_model)
        
        return self.W_o(context)

# টেস্ট
mha = MultiHeadAttention(d_model=128, n_heads=8)
x = torch.randn(16, 20, 128)
out = mha(x, x, x)  # সেল্ফ-অ্যাটেনশন
print(f"মাল্টি-হেড অ্যাটেনশন: {x.shape} → {out.shape}")
```

## 2. পজিশনাল এনকোডিং

```python
class PositionalEncoding(nn.Module):
    """পজিশনাল এনকোডিং (সাইন/কোসাইন)"""
    def __init__(self, d_model=128, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)

# টেস্ট
pe = PositionalEncoding(d_model=128, max_len=100)
x = torch.randn(16, 50, 128)
out = pe(x)
print(f"পজিশনাল এনকোডিং: {x.shape} → {out.shape}")

# সাইন/কোসাইন প্যাটার্ন
pos_pattern = pe.pe[0, :10, :4].numpy()
print(f"\nপ্রথম ৪ ডাইমেনশনের পজিশনাল এনকোডিং (প্রথম ১০ পজিশন):")
print(pos_pattern.round(3))
```

## 3. ট্রান্সফরমার এনকোডার লেয়ার

```python
class TransformerEncoderLayer(nn.Module):
    """ট্রান্সফরমার এনকোডার লেয়ার"""
    def __init__(self, d_model=128, n_heads=8, d_ff=512, dropout=0.1):
        super().__init__()
        
        self.self_attention = MultiHeadAttention(d_model, n_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout2 = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # সেল্ফ-অ্যাটেনশন + রেসিডুয়াল
        attn_out = self.self_attention(x, x, x, mask)
        x = self.norm1(x + self.dropout1(attn_out))
        
        # ফিড-ফরোয়ার্ড + রেসিডুয়াল
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout2(ffn_out))
        
        return x

# টেস্ট
encoder_layer = TransformerEncoderLayer(d_model=128, n_heads=8, d_ff=512)
x = torch.randn(16, 20, 128)
out = encoder_layer(x)
print(f"এনকোডার লেয়ার: {x.shape} → {out.shape}")
```

## 4. কমপ্লিট ট্রান্সফরমার এনকোডার

```python
class TransformerEncoder(nn.Module):
    """সম্পূর্ণ ট্রান্সফরমার এনকোডার"""
    def __init__(self, input_dim=10, d_model=128, n_heads=8, 
                 num_layers=4, d_ff=512, max_len=100, dropout=0.1):
        super().__init__()
        
        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len, dropout)
        
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, n_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # প্রজেক্ট + পজিশনাল এনকোডিং
        x = self.input_proj(x)
        x = self.pos_encoding(x)
        
        # এনকোডার লেয়ার
        for layer in self.layers:
            x = layer(x, mask)
        
        return self.norm(x)

# টেস্ট
encoder = TransformerEncoder(input_dim=5, d_model=128, n_heads=8, num_layers=4)
x = torch.randn(16, 30, 5)  # batch=16, seq_len=30, features=5
out = encoder(x)
print(f"ট্রান্সফরমার এনকোডার: {x.shape} → {out.shape}")
```

## 5. ফিন্যান্স: টাইম সিরিজ ট্রান্সফরমার

```python
class TimeSeriesTransformer(nn.Module):
    """টাইম সিরিজ ফোরকাস্টিং ট্রান্সফরমার"""
    def __init__(self, input_dim=5, d_model=64, n_heads=4, 
                 num_layers=3, output_len=10, dropout=0.1):
        super().__init__()
        
        self.encoder = TransformerEncoder(
            input_dim=input_dim,
            d_model=d_model,
            n_heads=n_heads,
            num_layers=num_layers,
            d_ff=d_model * 4,
            dropout=dropout
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, output_len)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        # গ্লোবাল এভারেজ পুলিং
        pooled = encoded.mean(dim=1)
        output = self.decoder(pooled)
        return output

# টেস্ট
ts_transformer = TimeSeriesTransformer(
    input_dim=5, d_model=64, n_heads=4, num_layers=3, output_len=10
)

x = torch.randn(16, 30, 5)  # batch=16, seq_len=30, features=5
output = ts_transformer(x)
print(f"টাইম সিরিজ ট্রান্সফরমার: {x.shape} → {output.shape}")

total_params = sum(p.numel() for p in ts_transformer.parameters())
print(f"মোট প্যারামিটার: {total_params:,}")
```

## 6. LSTM vs ট্রান্সফরমার বেঞ্চমার্ক

```python
import time

# ট্রেনিং টাইম তুলনা
seq_len = 50
batch = 32
features = 10

lstm = nn.LSTM(features, 64, 2, batch_first=True)
transformer = TimeSeriesTransformer(features, 64, 4, 2, output_len=1)

# ফরোয়ার্ড টাইম
x = torch.randn(batch, seq_len, features)

start = time.time()
for _ in range(100):
    _ = lstm(x)
lstm_time = time.time() - start

start = time.time()
for _ in range(100):
    _ = transformer(x)
transformer_time = time.time() - start

lstm_params = sum(p.numel() for p in lstm.parameters())
transformer_params = sum(p.numel() for p in transformer.parameters())

print(f"\nLSTM vs ট্রান্সফরমার বেঞ্চমার্ক:")
print(f"{'মেট্রিক':<25} {'LSTM':<15} {'ট্রান্সফরমার':<15}")
print("-" * 55)
print(f"{'প্যারামিটার':<25} {lstm_params:<15,} {transformer_params:<15,}")
print(f"{'১০০ ইনফারেন্স টাইম':<25} {lstm_time:<15.4f}s {transformer_time:<15.4f}s")
print(f"{'ইনফারেন্স/সেকেন্ড':<25} {100/lstm_time:<15.0f} {100/transformer_time:<15.0f}")
```

## ট্রান্সফরমার হাইপারপ্যারামিটার গাইড

```python
hyperparams = """
ট্রান্সফরমার হাইপারপ্যারামিটার গাইড (টাইম সিরিজ):

1. d_model (মডেল ডাইমেনশন)
   - ছোট: 32-64 (সিম্পল ডেটা)
   - মাঝারি: 64-128 (ফিন্যান্স)
   - বড়: 256-512 (কমপ্লেক্স ডেটা)

2. n_heads (হেডের সংখ্যা)
   - d_model % n_heads == 0 হওয়া আবশ্যক
   - সাধারণত: 4, 8
   - ছোট ডেটাসেট: 2-4
   - বড় ডেটাসেট: 8-16

3. num_layers (লেয়ারের সংখ্যা)
   - টাইম সিরিজ: 2-4
   - NLP: 6-12 (BERT)
   - বেশি লেয়ার = বেশি ক্ষমতা কিন্তু ওভারফিটিং

4. d_ff (ফিড-ফরোয়ার্ড ডাইমেনশন)
   - সাধারণত: d_model * 4
   - রেঞ্জ: d_model * 2 থেকে d_model * 8

5. dropout
   - ছোট ডেটাসেট: 0.2-0.4
   - বড় ডেটাসেট: 0.1-0.2
"""

print(hyperparams)
```

## সারাংশ
- ট্রান্সফরমার শুধুমাত্র অ্যাটেনশনের উপর ভিত্তি করে
- সেল্ফ-অ্যাটেনশন + পজিশনাল এনকোডিং + FFN মূল কম্পোনেন্ট
- প্যারালাল প্রসেসিং (RNN-এর চেয়ে দ্রুত)
- ফিন্যান্সে টাইম সিরিজ, ট্রেডিং সিগন্যাল, রিস্ক ব্যবস্থাপনায় ব্যবহৃত
- BERT, GPT, Llama সব ট্রান্সফরমার-বেসড
- LSTM-এর তুলনায় ভালো দীর্ঘমেয়াদী ডিপেন্ডেন্সি ক্যাপচার