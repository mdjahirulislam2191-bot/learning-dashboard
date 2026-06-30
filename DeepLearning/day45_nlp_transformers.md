# Day 45: NLP এবং ট্রান্সফরমার 🤖📝

## ট্রান্সফরমার NLP-তে কীভাবে কাজ করে?
ট্রান্সফরমার আর্কিটেকচার NLP-তে বিপ্লব এনেছে। এটি সিকোয়েন্সের সব পজিশনকে একসাথে প্রসেস করতে পারে (প্যারালাল প্রসেসিং)।

### কিওয়ার্ড
- **Self-Attention**: প্রতিটি শব্দ অন্যসব শব্দের সাথে সম্পর্ক বুঝতে পারে
- **Multi-Head Attention**: একাধিক দৃষ্টিকোণ থেকে অ্যাটেনশন
- **Positional Encoding**: শব্দের অবস্থান তথ্য সংরক্ষণ
- **Masked Language Model**: কিছু টোকেন মাস্ক করে প্রেডিক্ট শেখা

### ফিন্যান্সে NLP ট্রান্সফরমারের ব্যবহার
- সেন্টিমেন্ট অ্যানালাইসিস (নিউজ, সোশ্যাল মিডিয়া)
- ফিন্যান্সিয়াল রিপোর্ট পার্সিং (10-K, 10-Q)
- ইভেন্ট-ড্রিভেন ট্রেডিং
- মার্কেট কমেন্টারি জেনারেশন

## HuggingFace ট্রান্সফরমারস সিমুলেশন

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. সেল্ফ-অ্যাটেনশন মেকানিজম

```python
class SelfAttention(nn.Module):
    """সেল্ফ-অ্যাটেনশন মেকানিজম"""
    def __init__(self, d_model=64, n_heads=8):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape
        
        # Q, K, V প্রজেক্ট
        Q = self.W_q(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        
        # স্কেলড ডট-প্রোডাক্ট অ্যাটেনশন
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask == 0, float('-inf'))
        
        attn_probs = F.softmax(attn_scores, dim=-1)
        context = torch.matmul(attn_probs, V)
        
        # কনক্যাট ও প্রজেক্ট
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, -1)
        return self.W_o(context)

# ডেমো
d_model = 64
attn = SelfAttention(d_model=d_model, n_heads=8)
x = torch.randn(2, 10, d_model)  # batch=2, seq_len=10
out = attn(x)
print(f"ইনপুট শেপ: {x.shape}")
print(f"আউটপুট শেপ: {out.shape}")
```

## 2. সম্পূর্ণ ট্রান্সফরমার ব্লক

```python
class TransformerBlock(nn.Module):
    """একটি ট্রান্সফরমার এনকোডার ব্লক"""
    def __init__(self, d_model=64, n_heads=8, d_ff=256, dropout=0.1):
        super().__init__()
        self.attention = SelfAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # মাল্টি-হেড অ্যাটেনশন + রেসিডুয়াল কানেকশন
        attn_out = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN + রেসিডুয়াল কানেকশন
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x

# ডেমো
block = TransformerBlock(d_model=64, n_heads=8)
x = torch.randn(2, 10, 64)
out = block(x)
print(f"ট্রান্সফরমার ব্লক আউটপুট শেপ: {out.shape}")
```

## 3. ফিন্যান্সিয়াল সেন্টিমেন্ট ক্লাসিফিকেশন

```python
class FinancialSentimentModel(nn.Module):
    """ফিন্যান্সিয়াল সেন্টিমেন্ট অ্যানালাইসিসের জন্য ট্রান্সফরমার"""
    def __init__(self, vocab_size=10000, d_model=128, n_heads=8, 
                 num_layers=4, d_ff=512, num_classes=3, max_len=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = self._create_pos_encoding(max_len, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff) 
            for _ in range(num_layers)
        ])
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.classifier = nn.Linear(d_model, num_classes)
        self.dropout = nn.Dropout(0.1)
    
    def _create_pos_encoding(self, max_len, d_model):
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        return pe.unsqueeze(0)
    
    def forward(self, x, mask=None):
        seq_len = x.shape[1]
        x = self.embedding(x) * math.sqrt(self.embedding.embedding_dim)
        x = x + self.pos_encoding[:, :seq_len, :].to(x.device)
        
        for block in self.blocks:
            x = block(x, mask)
        
        # পুলিং (মিন over sequence dim)
        x = x.transpose(1, 2)
        x = self.pool(x).squeeze(-1)
        x = self.dropout(x)
        return self.classifier(x)

# সিমুলেটেড ট্রেনিং
model = FinancialSentimentModel(
    vocab_size=5000, d_model=128, n_heads=8, 
    num_layers=4, num_classes=3
).to(device)

# সিম্পল ডেটা
batch_size, seq_len = 4, 20
dummy_input = torch.randint(0, 5000, (batch_size, seq_len)).to(device)
output = model(dummy_input)
print(f"সেন্টিমেন্ট আউটপুট শেপ: {output.shape}  # [batch, 3] - নেগেটিভ/নিউট্রাল/পজিটিভ")
print(f"সেন্টিমেন্ট লগিটস:\n{output}")
```

## 4. ফিন্যান্সিয়াল টেক্সট এম্বেডিং

```python
def get_financial_embeddings(model, texts_tokenized):
    """ফিন্যান্সিয়াল টেক্সট থেকে এম্বেডিং এক্সট্র্যাক্ট"""
    model.eval()
    with torch.no_grad():
        # সিম্পল ফরওয়ার্ড পাস
        tokens = torch.tensor(texts_tokenized).to(device)
        x = model.embedding(tokens) * math.sqrt(model.embedding.embedding_dim)
        seq_len = tokens.shape[1]
        x = x + model.pos_encoding[:, :seq_len, :].to(device)
        
        for block in model.blocks:
            x = block(x)
        
        # মিন পুলিং
        embeddings = x.mean(dim=1)
    return embeddings.cpu().numpy()

# ডেমো এম্বেডিং
print("\nফিন্যান্সিয়াল টেক্সট এম্বেডিং ডেমো:")
print("টেক্সট: 'মার্কেট টুডে শক্তিশালী আপট্রেন্ড দেখিয়েছে'")
print("এম্বেডিং ভেক্টর: [128-ডাইমেনশনাল রিপ্রেজেন্টেশন]")
```

## 5. ফিন্যান্স NLP পাইপলাইন

```python
class FinancialNLPPipeline:
    """ফিন্যান্সিয়াল NLP পাইপলাইন"""
    def __init__(self, model, tokenizer_vocab):
        self.model = model
        self.vocab = tokenizer_vocab  # সিম্পল ভোকাব ধরে নিচ্ছি
        self.idx_to_label = {0: 'নেগেটিভ 📉', 1: 'নিউট্রাল ➡️', 2: 'পজিটিভ 📈'}
    
    def predict_sentiment(self, text_indices):
        """টেক্সটের সেন্টিমেন্ট প্রেডিক্ট করুন"""
        self.model.eval()
        with torch.no_grad():
            tokens = torch.tensor([text_indices]).to(device)
            logits = self.model(tokens)
            probs = F.softmax(logits, dim=-1)
            pred = logits.argmax(dim=-1).item()
        
        return {
            'sentiment': self.idx_to_label[pred],
            'confidence': probs[0][pred].item(),
            'probabilities': {
                self.idx_to_label[i]: probs[0][i].item() 
                for i in range(3)
            }
        }

# ডেমো
pipeline = FinancialNLPPipeline(model, vocab_size=5000)
demo_input = [12, 45, 67, 890, 234, 56, 78, 901, 345, 67, 
              89, 123, 456, 789, 234, 567, 890, 123, 456, 789]
result = pipeline.predict_sentiment(demo_input[:20])
print(f"\nপ্রেডিক্টেড সেন্টিমেন্ট: {result['sentiment']}")
print(f"কনফিডেন্স: {result['confidence']:.2%}")
```

## সারাংশ
- ট্রান্সফরমার NLP-তে স্টেট-অফ-দি-আর্ট পারফরম্যান্স দেয়
- সেল্ফ-অ্যাটেনশন সব শব্দের সম্পর্ক ক্যাপচার করে
- ফিন্যান্সে NLP ব্যবহার করে সেন্টিমেন্ট অ্যানালাইসিস, নিউজ প্রসেসিং
- HuggingFace ট্রান্সফরমার সহজেই ব্যবহার করা যায়
