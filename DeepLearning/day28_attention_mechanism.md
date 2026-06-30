# Day 28: অ্যাটেনশন মেকানিজম 👁️

## অ্যাটেনশন কী?
অ্যাটেনশন মেকানিজম মডেলকে আউটপুট জেনারেট করার সময় ইনপুটের নির্দিষ্ট অংশে ফোকাস করতে দেয়। এটি "মনোযোগ" দেওয়ার মতো কাজ করে।

### কেন অ্যাটেনশন?
- **দীর্ঘ সিকোয়েন্স**: LSTM/GRU দীর্ঘ সিকোয়েন্সে তথ্য হারায়
- **রিলেভ্যান্সি**: সব ইনপুট সমান গুরুত্বপূর্ণ নয়
- **ইন্টারপ্রিটেবিলিটি**: মডেল কী দেখছে তা বোঝা যায়

### অ্যাটেনশনের প্রকার
1. **Bahdanau Attention** (Additive): ছোট সিকোয়েন্সের জন্য ভালো
2. **Luong Attention** (Multiplicative): বড় সিকোয়েন্সের জন্য
3. **Self-Attention**: নিজের সিকোয়েন্সের মধ্যে সম্পর্ক
4. **Multi-Head Attention**: একাধিক পার্সপেক্টিভ থেকে অ্যাটেনশন

## সিম্পল অ্যাটেনশন ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import numpy as np

class BahdanauAttention(nn.Module):
    """Bahdanau অ্যাটেনশন (Additive)"""
    def __init__(self, hidden_size):
        super().__init__()
        self.W1 = nn.Linear(hidden_size, hidden_size)
        self.W2 = nn.Linear(hidden_size, hidden_size)
        self.V = nn.Linear(hidden_size, 1)
    
    def forward(self, decoder_hidden, encoder_outputs):
        # decoder_hidden: (batch, hidden_size)
        # encoder_outputs: (batch, seq_len, hidden_size)
        
        decoder_hidden = decoder_hidden.unsqueeze(1)  # (batch, 1, hidden_size)
        
        # স্কোর স্কিম
        score = self.V(torch.tanh(
            self.W1(decoder_hidden) + self.W2(encoder_outputs)
        ))  # (batch, seq_len, 1)
        
        attention_weights = torch.softmax(score, dim=1)  # (batch, seq_len, 1)
        context = torch.sum(attention_weights * encoder_outputs, dim=1)  # (batch, hidden_size)
        
        return context, attention_weights

class LuongAttention(nn.Module):
    """Luong অ্যাটেনশন (Multiplicative)"""
    def __init__(self, hidden_size):
        super().__init__()
        self.W = nn.Linear(hidden_size, hidden_size, bias=False)
    
    def forward(self, decoder_hidden, encoder_outputs):
        # decoder_hidden: (batch, hidden_size)
        # encoder_outputs: (batch, seq_len, hidden_size)
        
        score = torch.bmm(encoder_outputs, 
                          decoder_hidden.unsqueeze(2))  # (batch, seq_len, 1)
        
        attention_weights = torch.softmax(score, dim=1)
        context = torch.sum(attention_weights * encoder_outputs, dim=1)
        
        return context, attention_weights

# টেস্ট
hidden_size = 256
batch, seq_len = 32, 20

bahdanau = BahdanauAttention(hidden_size)
luong = LuongAttention(hidden_size)

decoder_h = torch.randn(batch, hidden_size)
encoder_out = torch.randn(batch, seq_len, hidden_size)

context_b, attn_b = bahdanau(decoder_h, encoder_out)
context_l, attn_l = luong(decoder_h, encoder_out)

print(f"Bahdanau - কনটেক্সট: {context_b.shape}, অ্যাটেনশন: {attn_b.shape}")
print(f"Luong - কনটেক্সট: {context_l.shape}, অ্যাটেনশন: {attn_l.shape}")
```

## সেল্ফ-অ্যাটেনশন (Transformer-এর মূল)

```python
class SelfAttention(nn.Module):
    """সেল্ফ-অ্যাটেনশন মেকানিজম"""
    def __init__(self, embed_size, heads=1):
        super().__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads
        
        assert embed_size % heads == 0, "embed_size heads দিয়ে বিভাজ্য হতে হবে"
        
        self.queries = nn.Linear(embed_size, embed_size)
        self.keys = nn.Linear(embed_size, embed_size)
        self.values = nn.Linear(embed_size, embed_size)
        self.fc_out = nn.Linear(embed_size, embed_size)
    
    def forward(self, x, mask=None):
        batch, seq_len, embed_size = x.shape
        
        # Q, K, V জেনারেট
        Q = self.queries(x)
        K = self.keys(x)
        V = self.values(x)
        
        # হেডে রিশেপ
        Q = Q.view(batch, seq_len, self.heads, self.head_dim).permute(0, 2, 1, 3)
        K = K.view(batch, seq_len, self.heads, self.head_dim).permute(0, 2, 1, 3)
        V = V.view(batch, seq_len, self.heads, self.head_dim).permute(0, 2, 1, 3)
        
        # অ্যাটেনশন স্কোর
        energy = torch.matmul(Q, K.permute(0, 1, 3, 2)) / (self.head_dim ** 0.5)
        
        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))
        
        attention = torch.softmax(energy, dim=-1)
        
        # কনটেক্সট ভেক্টর
        out = torch.matmul(attention, V)
        out = out.permute(0, 2, 1, 3).contiguous()
        out = out.view(batch, seq_len, embed_size)
        
        return self.fc_out(out), attention

# টেস্ট
self_attn = SelfAttention(embed_size=512, heads=8)
x = torch.randn(16, 50, 512)  # batch=16, seq_len=50, embed=512
out, attn = self_attn(x)
print(f"সেল্ফ-অ্যাটেনশন আউটপুট: {out.shape}")
print(f"অ্যাটেনশন ম্যাট্রিক্স: {attn.shape}")  # (16, 8, 50, 50)
```

## ফিন্যান্স: অ্যাটেনশন সহ টাইম সিরিজ

```python
class LSTMAttention(nn.Module):
    """LSTM + অ্যাটেনশন হাইব্রিড মডেল"""
    def __init__(self, input_size, hidden_size=128, num_layers=2, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, bidirectional=True, dropout=0.3)
        self.attention = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, output_size)
        )
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # (batch, seq_len, hidden*2)
        
        # অ্যাটেনশন
        attn_weights = self.attention(lstm_out)  # (batch, seq_len, 1)
        attn_weights = torch.softmax(attn_weights, dim=1)
        
        # কনটেক্সট ভেক্টর
        context = torch.sum(attn_weights * lstm_out, dim=1)
        
        return self.fc(context), attn_weights

# টেস্ট
model = LSTMAttention(input_size=10, hidden_size=64, output_size=1)
x = torch.randn(32, 30, 10)
output, weights = model(x)
print(f"প্রেডিকশন: {output.shape}")
print(f"অ্যাটেনশন ওয়েটস: {weights.shape}")  # কতোটুকু ফোকাস করছে
```

## অ্যাটেনশন ভিজুয়ালাইজেশন

```python
import matplotlib.pyplot as plt

def visualize_attention(attention_weights, title="অ্যাটেনশন হিটম্যাপ"):
    """অ্যাটেনশন ওয়েট ভিজুয়ালাইজ"""
    plt.figure(figsize=(10, 6))
    
    # সিঙ্গেল স্যাম্পল
    attn = attention_weights[0].squeeze(-1).detach().numpy()  # (seq_len,)
    
    plt.bar(range(len(attn)), attn)
    plt.xlabel('টাইম স্টেপ')
    plt.ylabel('অ্যাটেনশন স্কোর')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()

# সিমুলেটেড অ্যাটেনশন
fake_weights = torch.randn(16, 30, 1)
fake_weights = torch.softmax(fake_weights, dim=1)

print("প্রথম স্যাম্পলের অ্যাটেনশন ডিস্ট্রিবিউশন:")
attn_probs = fake_weights[0].squeeze().numpy()
print(f"মিন: {attn_probs.min():.4f}, ম্যাক্স: {attn_probs.max():.4f}, সাম: {attn_probs.sum():.4f}")

# কোন টাইমস্টেপ সবচেয়ে গুরুত্বপূর্ণ?
most_important = torch.argmax(fake_weights[0])
print(f"সবচেয়ে গুরুত্বপূর্ণ টাইম স্টেপ: {most_important.item()}")
```

## মাল্টি-হেড অ্যাটেনশন

```python
class MultiHeadAttention(nn.Module):
    """মাল্টি-হেড অ্যাটেনশন"""
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.n_heads = n_heads
        self.d_model = d_model
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, query, key, value, mask=None):
        batch = query.shape[0]
        
        # লিনিয়ার ট্রান্সফর্ম + হেডে বিভক্ত
        Q = self.W_q(query).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # অ্যাটেনশন
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.d_k ** 0.5)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attn = torch.softmax(scores, dim=-1)
        context = torch.matmul(attn, V)
        
        # কনক্যাট ও লিনিয়ার
        context = context.transpose(1, 2).contiguous().view(batch, -1, self.d_model)
        return self.W_o(context), attn

# টেস্ট
mha = MultiHeadAttention(d_model=512, n_heads=8)
x = torch.randn(32, 50, 512)
out, attn = mha(x, x, x)  # সেল্ফ-অ্যাটেনশন
print(f"মাল্টি-হেড আউটপুট: {out.shape}")
print(f"অ্যাটেনশন শেপ: {attn.shape}")  # (32, 8, 50, 50)
```

## ফিন্যান্স অ্যাপ্লিকেশন: টেম্পোরাল অ্যাটেনশন

```python
class TemporalAttention(nn.Module):
    """টেম্পোরাল অ্যাটেনশন - সময়ের সাথে গুরুত্ব"""
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.Tanh(),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        
        # টেম্পোরাল অ্যাটেনশন
        scores = self.attention(lstm_out)  # (batch, seq_len, 1)
        weights = torch.softmax(scores, dim=1)
        
        # ওয়েটেড কনটেক্সট
        context = torch.sum(weights * lstm_out, dim=1)
        
        # রিসেন্ট বায়াস চেক
        recent_weight = weights[0, -5:].mean().item()
        early_weight = weights[0, :5].mean().item()
        
        return context, weights, recent_weight, early_weight

# সিমুলেটেড ফিন্যান্স ডেটা
np.random.seed(42)
x = torch.FloatTensor(np.random.randn(10, 30, 5))

temp_attn = TemporalAttention(input_size=5, hidden_size=64)
context, weights, recent, early = temp_attn(x)

print(f"টেম্পোরাল অ্যাটেনশন বিশ্লেষণ:")
print(f"  সাম্প্রতিক (শেষ ৫) গড় অ্যাটেনশন: {recent:.4f}")
print(f"  পুরাতন (প্রথম ৫) গড় অ্যাটেনশন: {early:.4f}")
print(f"  রেশিও (রিসেন্ট/আর্লি): {recent/early:.2f}x")

if recent > early:
    print("  ▶ মডেল সাম্প্রতিক ডেটার উপর বেশি ফোকাস করে")
else:
    print("  ◀ মডেল পুরাতন ডেটার উপর বেশি ফোকাস করে")
```

## অ্যাটেনশনের সুবিধা ও সীমাবদ্ধতা

### সুবিধা
1. **লং-রেঞ্জ ডিপেন্ডেন্সি**: দীর্ঘ সিকোয়েন্সেও তথ্য ধরে রাখে
2. **প্যারালাল প্রসেসিং**: RNN-এর মতো সিকোয়েন্সিয়াল না
3. **ইন্টারপ্রিটেবিলিটি**: অ্যাটেনশন ম্যাপ দেখায় মডেল কী দেখছে
4. **পারফরম্যান্স**: বেশিরভাগ NLP টাস্কে SOTA

### সীমাবদ্ধতা
1. **কম্পিউটেশনাল কস্ট**: O(n²) জটিলতা
2. **পজিশনাল ইনফরমেশন**: অর্ডার বুঝতে পজিশনাল এনকোডিং প্রয়োজন
3. **ছোট ডেটাসেটে ওভারফিটিং**: বহু প্যারামিটার

### কখন ব্যবহার করবেন?
- ট্রান্সফরমার-বেসড মডেল
- Seq2Seq টাস্ক
- টাইম সিরিজে গুরুত্বপূর্ণ ইভেন্ট ডিটেকশন
- ফিন্যান্সে নিউজ সেন্টিমেন্ট অ্যানালাইসিস

```python
print("✅ অ্যাটেনশন মেকানিজম সম্পূর্ণ")
print(f"মোট অ্যাটেনশন ভ্যারিয়েন্ট কভার করা হয়েছে:")
print(f"  - Bahdanau (Additive)")
print(f"  - Luong (Multiplicative)")
print(f"  - Self-Attention")
print(f"  - Multi-Head Attention")
print(f"  - Temporal Attention for Finance")
```

## সারাংশ
- অ্যাটেনশন মডেলকে সবচেয়ে রিলেভেন্ট ইনপুটে ফোকাস করতে দেয়
- Bahdanau ও Luong অ্যাটেনশন সবচেয়ে জনপ্রিয়
- সেল্ফ-অ্যাটেনশন ট্রান্সফরমারের মূল অংশ
- মাল্টি-হেড অ্যাটেনশন একাধিক দৃষ্টিকোণ থেকে বিশ্লেষণ করে
- ফিন্যান্সে টেম্পোরাল প্যাটার্ন ও নিউজ অ্যানালাইসিসে গুরুত্বপূর্ণ