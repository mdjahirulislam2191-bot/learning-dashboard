# Day 42: BERT ইন্ট্রোডাকশন 🤗

## BERT কী?
BERT (Bidirectional Encoder Representations from Transformers) হল Google-এর NLP মডেল যা ট্রান্সফরমার আর্কিটেকচারের উপর ভিত্তি করে তৈরি।

### BERT-এর বৈশিষ্ট্য
1. **বিডাইরেকশনাল**: বাম ও ডান উভয় দিকের কনটেক্সট বুঝতে পারে
2. **প্রি-ট্রেইনড**: বিশাল টেক্সট কর্পাসে প্রি-ট্রেইনড
3. **ফাইন-টিউনেবল**: নির্দিষ্ট টাস্কে অ্যাডাপ্ট করা যায়
4. **MLM (Masked Language Modeling)**: ট্রেনিং টেকনিক

### ফিন্যান্স অ্যাপ্লিকেশন
- ফিন্যান্সিয়াল সেন্টিমেন্ট অ্যানালাইসিস
- নিউজ-ভিত্তিক ট্রেডিং সিগন্যাল
- ইয়ারনিংগ কল ট্রান্সক্রিপ্ট অ্যানালাইসিস
- রেগুলেটরি ফাইলিং অ্যানালাইসিস (10-K, 10-Q)
- ফিন্যান্সিয়াল QA সিস্টেম

## BERT আর্কিটেকচার ওভারভিউ

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# BERT আর্কিটেকচার সিমুলেশন
class MiniBERT(nn.Module):
    """মিনি BERT মডেল (শিক্ষামূলক)"""
    def __init__(self, vocab_size=1000, d_model=128, nhead=4, 
                 num_layers=4, max_len=128):
        super().__init__()
        
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=512,
            dropout=0.1, batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # MLM হেড
        self.mlm_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
            nn.Linear(d_model, vocab_size)
        )
        
        # পুলার (CLS টোকেন)
        self.pooler = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.Tanh()
        )
    
    def forward(self, input_ids, attention_mask=None):
        batch, seq_len = input_ids.shape
        
        # এম্বেডিং
        token_emb = self.token_embedding(input_ids)
        positions = torch.arange(seq_len).unsqueeze(0).to(input_ids.device)
        pos_emb = self.position_embedding(positions)
        
        x = token_emb + pos_emb
        
        # এনকোডার
        if attention_mask is not None:
            # (batch, seq_len) → (batch*nhead, seq_len) জন্য
            mask = attention_mask.float().masked_fill(
                attention_mask == 0, float('-inf')).masked_fill(
                attention_mask == 1, float(0))
            mask = mask.unsqueeze(1).unsqueeze(2)
            x = self.encoder(x, mask=mask)
        else:
            x = self.encoder(x)
        
        # CLS আউটপুট (প্রথম টোকেন)
        cls_output = self.pooler(x[:, 0, :])
        
        return cls_output, x

# টেস্ট
model = MiniBERT(vocab_size=1000, d_model=128)
x = torch.randint(0, 1000, (4, 32))  # batch=4, seq_len=32
cls_out, seq_out = model(x)
print(f"ইনপুট: {x.shape}")
print(f"CLS আউটপুট: {cls_out.shape}")
print(f"সিকোয়েন্স আউটপুট: {seq_out.shape}")

total_params = sum(p.numel() for p in model.parameters())
print(f"মোট প্যারামিটার: {total_params:,}")
print(f"(রিয়েল BERT-base: 110M প্যারামিটার)")
```

## ফিন্যান্স সেন্টিমেন্টে HuggingFace BERT

```python
# HuggingFace ট্রান্সফরমার ব্যবহার (সিমুলেটেড)
# ইনস্টল: pip install transformers

print("HuggingFace Transformers সেটআপ:")
print("-" * 40)
print("  from transformers import BertTokenizer, BertForSequenceClassification")
print("  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')")
print("  model = BertForSequenceClassification.from_pretrained(")
print("      'bert-base-uncased', num_labels=3)")

# সিমুলেটেড টোকেনাইজেশন
tokenizer_vocab = {
    'মার্কেট': 1001, 'স্টক': 1002, 'বেড়ে': 2001, 'কমেছে': 2002,
    'লাভ': 3001, 'ক্ষতি': 3002, 'নিউট্রাল': 3003, 'গ্রোথ': 4001
}

sample_texts = [
    "মার্কেট বেড়েছে, লাভ হয়েছে",
    "স্টক কমেছে, ক্ষতি হয়েছে",
    "মার্কেট নিউট্রাল অবস্থায় আছে"
]

print(f"\nস্যাম্পল টেক্সট:")
for text in sample_texts:
    print(f"  '{text}'")

# HuggingFace পাইপলাইন সিমুলেশন
class SentimentPipeline:
    """সেন্টিমেন্ট পাইপলাইন"""
    def __init__(self):
        self.labels = ['নেগেটিভ', 'নিউট্রাল', 'পজিটিভ']
    
    def predict(self, texts):
        for text in texts:
            score = self._analyze(text)
            label_idx = np.argmax(score)
            print(f"  '{text}' → {self.labels[label_idx]} "
                  f"(confidence: {score[label_idx]:.2f})")
    
    def _analyze(self, text):
        # সিমুলেটেড বিশ্লেষণ
        if 'ক্ষতি' in text or 'কমেছে' in text:
            return [0.85, 0.10, 0.05]
        elif 'লাভ' in text or 'বেড়েছে' in text:
            return [0.05, 0.10, 0.85]
        else:
            return [0.10, 0.80, 0.10]

pipeline = SentimentPipeline()
pipeline.predict(sample_texts)
```

## ফাইন-টিউনিং BERT

```python
# BERT ফাইন-টিউনিং সিমুলেশন
class BertFineTuner:
    """BERT ফাইন-টিউনিং পাইপলাইন"""
    def __init__(self, num_labels=3, learning_rate=2e-5):
        self.num_labels = num_labels
        self.learning_rate = learning_rate
        
        print(f"BERT ফাইন-টিউনিং কনফিগ:")
        print(f"  num_labels: {num_labels}")
        print(f"  learning_rate: {learning_rate}")
        print(f"  optimizer: AdamW")
        print(f"  scheduler: Linear warmup")
        print(f"  batch_size: 16")
        print(f"  epochs: 3")
    
    def prepare_data(self, texts, labels):
        """ডেটা প্রস্তুত"""
        print(f"\nডেটা প্রস্তুত:")
        print(f"  টেক্সট: {len(texts)}")
        print(f"  লেবেল: {len(set(labels))} ক্লাস")
        
    def train(self, train_texts, train_labels, val_texts, val_labels):
        """ট্রেনিং"""
        print(f"\nট্রেনিং শুরু (সিমুলেটেড):")
        for epoch in range(3):
            train_loss = np.random.uniform(0.1, 0.5) * (0.5 ** epoch)
            val_acc = 0.7 + 0.1 * epoch
            print(f"  Epoch {epoch+1}: train_loss={train_loss:.4f}, "
                  f"val_acc={val_acc:.4f}")
        print("✅ BERT ফাইন-টিউনিং সম্পূর্ণ!")

# ফিন্যান্সিয়াল সেন্টিমেন্ট ডেটা
train_texts = [
    "কোম্পানির মুনাফা ২০% বৃদ্ধি পেয়েছে",
    "বাজার অস্থির, বিনিয়োগকারীরা সতর্ক",
    "সরকার নতুন নীতি ঘোষণা করেছে",
]
train_labels = ['পজিটিভ', 'নিউট্রাল', 'নিউট্রাল']

tuner = BertFineTuner(num_labels=3)
tuner.prepare_data(train_texts, train_labels)
tuner.train(train_texts, train_labels, train_texts, train_labels)
```

## ফিন্যান্সিয়াল টেক্সট প্রিপ্রসেসিং

```python
class FinancialTextPreprocessor:
    """ফিন্যান্সিয়াল টেক্সট প্রিপ্রসেসর"""
    def __init__(self, max_len=128):
        self.max_len = max_len
        self.special_tokens = {
            '[CLS]': 101, '[SEP]': 102, '[PAD]': 0, '[MASK]': 103
        }
    
    def clean_text(self, text):
        """ফিন্যান্সিয়াল টেক্সট ক্লিনিং"""
        import re
        # ডলার সিম্বল
        text = re.sub(r'\$[\d,]+(\.\d+)?', '[PRICE]', text)
        # পার্সেন্টেজ
        text = re.sub(r'\d+\.?\d*%', '[PERCENT]', text)
        # নাম্বার
        text = re.sub(r'\d+\.?\d*', '[NUM]', text)
        return text
    
    def tokenize(self, text):
        """সিম্পল টোকেনাইজেশন"""
        cleaned = self.clean_text(text)
        tokens = cleaned.lower().split()
        tokens = ['[CLS]'] + tokens[:self.max_len-2] + ['[SEP]']
        return tokens

processor = FinancialTextPreprocessor()

# ডেমো
sample = "Apple এর স্টক প্রাইস $154.32 এ ট্রেড করছে, যা গতকাল থেকে 2.5% বেশি"
cleaned = processor.clean_text(sample)
tokens = processor.tokenize(sample)

print(f"অরিজিনাল: '{sample}'")
print(f"ক্লিনড: '{cleaned}'")
print(f"টোকেনস: {tokens}")
print(f"টোকেন কাউন্ট: {len(tokens)}")
```

## BERT ইনফারেন্স অপ্টিমাইজেশন

```python
class BertInferenceOptimizer:
    """BERT ইনফারেন্স অপ্টিমাইজেশন"""
    def __init__(self):
        self.techniques = {
            'কোয়ান্টাইজেশন': 'FP32 → INT8, 4x স্পিডআপ',
            'প্রুনিং': 'অপ্রয়োজনীয় ওয়েট রিমুভ',
            'ডিস্টিলেশন': 'বড় মডেল থেকে ছোট মডেল',
            'অনিক্স': 'ক্রস-প্ল্যাটফর্ম অপ্টিমাইজেশন',
            'ফ্ল্যাশ অ্যাটেনশন': 'মেমরি-এফিশিয়েন্ট অ্যাটেনশন'
        }
    
    def optimize(self, model, technique='কোয়ান্টাইজেশন'):
        print(f"BERT ইনফারেন্স অপ্টিমাইজেশন:")
        print(f"  টেকনিক: {technique}")
        print(f"  বিবরণ: {self.techniques[technique]}")
        print(f"  মডেল সাইজ কমানো: ~75%")
        print(f"  স্পিডআপ: ~2-4x")

opt = BertInferenceOptimizer()
opt.optimize(None, 'কোয়ান্টাইজেশন')

print(f"\nরিয়েল-টাইম ট্রেডিংয়ে BERT:")
print(f"  ১০০০ নিউজ প্রসেসিং: ~৫০০ms (FP32) → ~১৫০ms (INT8)")
print(f"  ট্রেডিং সিগন্যাল জেনারেশন: {200}ms এর নিচে")
```

## সারাংশ
- BERT বিডাইরেকশনাল ট্রান্সফরমার ব্যবহার করে
- MLM (Masked Language Modeling) দিয়ে প্রি-ট্রেইনড
- ফিন্যান্সে সেন্টিমেন্ট, নিউজ অ্যানালাইসিস, QA-তে ব্যবহৃত
- HuggingFace লাইব্রেরি BERT ব্যবহার সহজ করে
- ফাইন-টিউনিং নির্দিষ্ট ফিন্যান্স টাস্কের জন্য অ্যাডাপ্টেশন
- ইনফারেন্স অপ্টিমাইজেশন (কোয়ান্টাইজেশন) রিয়েল-টাইম ট্রেডিংয়ের জন্য জরুরি