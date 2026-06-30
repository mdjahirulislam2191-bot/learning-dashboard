# Day 26: সিকোয়েন্স মডেলস 🔗

## সিকোয়েন্স মডেল কী?
সিকোয়েন্স মডেল এমন ডেটা নিয়ে কাজ করে যেখানে আইটেমগুলোর মধ্যে অর্ডার গুরুত্বপূর্ণ।

### সিকোয়েন্স ডেটার ধরণ
| টাইপ | উদাহরণ | ফিন্যান্স অ্যাপ্লিকেশন |
|---|---|---|
| **Time Series** | প্রাইস, ভলিউম | স্টক প্রেডিকশন, ফোরকাস্টিং |
| **Text** | খবর, রিপোর্ট | সেন্টিমেন্ট অ্যানালাইসিস |
| **Audio** | কনফারেন্স কল | ভয়েস অ্যানালাইসিস |
| **Video** | ট্রেডিং ফ্লোর | প্যাটার্ন রিকগনিশন |

### সিকোয়েন্স প্রকার
1. **Many-to-One**: সিকোয়েন্স → সিঙ্গল আউটপুট (স্টক প্রেডিকশন)
2. **One-to-Many**: সিঙ্গল ইনপুট → সিকোয়েন্স (টেক্সট জেনারেশন)
3. **Many-to-Many**: সিকোয়েন্স → সিকোয়েন্স (ট্রান্সলেশন)
4. **Equal Many-to-Many**: প্রতি ইনপুটে আউটপুট (ভিডিও ফ্রেম)

## PyTorch সিকোয়েন্স ইউটিলিটিস

```python
import torch
import torch.nn as nn
import numpy as np

# PyTorch-এ সিকোয়েন্স মডেলিং টুলস

# 1. PackedSequence (ভেরিয়েবল লেন্থ সিকোয়েন্স)
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pad_sequence

# ভেরিয়েবল লেন্থ ডেটা
sequences = [torch.randn(3, 5), torch.randn(5, 5), torch.randn(2, 5)]
lengths = torch.tensor([3, 5, 2])

# প্যাডিং
padded = pad_sequence(sequences, batch_first=True)
print(f"প্যাডেড সিকোয়েন্স: {padded.shape}")

# প্যাক (efficient processing)
packed = pack_padded_sequence(padded, lengths, batch_first=True, enforce_sorted=False)
print(f"প্যাকড সিকোয়েন্স: {packed}")
```

## সিম্পল সিকোয়েন্স ক্লাসিফিকেশন

```python
class SequenceClassifier(nn.Module):
    """সিকোয়েন্স ক্লাসিফিকেশন মডেল"""
    def __init__(self, input_size, hidden_size, num_classes, num_layers=2):
        super().__init__()
        self.rnn = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, bidirectional=True,
            dropout=0.3 if num_layers > 1 else 0
        )
        self.attention = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
        self.fc = nn.Linear(hidden_size * 2, num_classes)
    
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        
        out, _ = self.rnn(x)
        
        if lengths is not None:
            out, _ = pad_packed_sequence(out, batch_first=True)
        
        # অ্যাটেনশন ওয়েটেড আউটপুট
        attention_weights = self.attention(out)
        attention_weights = torch.softmax(attention_weights, dim=1)
        attended = torch.sum(attention_weights * out, dim=1)
        
        return self.fc(attended)

# টেস্ট
model = SequenceClassifier(input_size=10, hidden_size=64, num_classes=3)
x = torch.randn(16, 20, 10)  # batch=16, seq_len=20, features=10
output = model(x)
print(f"ক্লাসিফিকেশন আউটপুট: {output.shape}")  # (16, 3)
```

## ফিন্যান্স: সেন্টিমেন্ট অ্যানালাইসিস

```python
# সিম্পল টেক্সট → সিকোয়েন্স মডেলিং
class TextToSequence(nn.Module):
    """টেক্সট এমবেডিং + LSTM"""
    def __init__(self, vocab_size, embed_dim=128, hidden_size=256, num_classes=3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_size, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x, lengths=None):
        embedded = self.dropout(self.embedding(x))
        
        if lengths is not None:
            embedded = pack_padded_sequence(embedded, lengths, 
                                           batch_first=True, enforce_sorted=False)
        
        out, (hidden, cell) = self.lstm(embedded)
        
        # বিডাইরেকশনাল হিডেন স্টেট কনক্যাট
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        out = self.fc(self.dropout(hidden))
        return out

# সিমুলেটেড ভোকাবুলারি
vocab_size = 5000
model = TextToSequence(vocab_size=vocab_size, embed_dim=128, hidden_size=256, num_classes=3)

# সিন্থেটিক টেক্সট ডেটা
batch_size, seq_len = 32, 50
x = torch.randint(1, vocab_size, (batch_size, seq_len))
lengths = torch.randint(10, seq_len, (batch_size,))
output = model(x, lengths)
print(f"সেন্টিমেন্ট আউটপুট (3 ক্লাস): {output.shape}")
```

## সিকোয়েন্স-টু-সিকোয়েন্স ফোরকাস্টিং

```python
class Seq2SeqForecaster(nn.Module):
    """মাল্টি-স্টেপ সিকোয়েন্স ফোরকাস্টিং"""
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super().__init__()
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.decoder = nn.LSTM(output_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x, target_len):
        # এনকোডার
        _, (hidden, cell) = self.encoder(x)
        
        # ডিকোডার
        decoder_input = x[:, -1:, :1]  # প্রথম ডিকোডার ইনপুট
        outputs = []
        
        for _ in range(target_len):
            out, (hidden, cell) = self.decoder(decoder_input, (hidden, cell))
            pred = self.fc(out)
            outputs.append(pred)
            decoder_input = pred  # টিচার ফোর্সিং ছাড়া
        
        return torch.cat(outputs, dim=1)

# টেস্ট
seq2seq = Seq2SeqForecaster(input_size=5, hidden_size=128, output_size=1)
x = torch.randn(16, 20, 5)  # batch=16, seq_len=20, features=5
future = seq2seq(x, target_len=10)  # ভবিষ্যত ১০ স্টেপ
print(f"ফোরকাস্ট আউটপুট: {future.shape}")  # (16, 10, 1)
```

## টাইম সিরিজ ফিচার এক্সট্র্যাকশন

```python
class TimeSeriesFeatureExtractor(nn.Module):
    """টাইম সিরিজ থেকে ফিচার এক্সট্র্যাক্ট"""
    def __init__(self, input_size, hidden_size=128):
        super().__init__()
        self.conv1d = nn.Conv1d(input_size, 64, kernel_size=3, padding=1)
        self.conv1d_2 = nn.Conv1d(64, 32, kernel_size=5, padding=2)
        self.lstm = nn.LSTM(32, hidden_size, batch_first=True, bidirectional=True)
        self.pool = nn.AdaptiveAvgPool1d(1)
    
    def forward(self, x):
        # x: (batch, seq_len, features)
        x = x.permute(0, 2, 1)  # (batch, features, seq_len)
        x = torch.relu(self.conv1d(x))
        x = torch.relu(self.conv1d_2(x))
        x = x.permute(0, 2, 1)  # (batch, seq_len, channels)
        
        lstm_out, _ = self.lstm(x)
        pooled = self.pool(lstm_out.permute(0, 2, 1)).squeeze(-1)
        
        return pooled

# টেস্ট
extractor = TimeSeriesFeatureExtractor(input_size=10)
x = torch.randn(16, 50, 10)
features = extractor(x)
print(f"এক্সট্র্যাক্টেড ফিচার: {features.shape}")  # (16, 256)
```

## সিকোয়েন্স ডেটার জন্য ডেটা অগমেন্টেশন

```python
class TimeSeriesAugmentation:
    """টাইম সিরিজ ডেটা অগমেন্টেশন"""
    
    @staticmethod
    def jitter(x, sigma=0.01):
        """গাউসিয়ান নয়েজ যোগ"""
        return x + np.random.normal(0, sigma, x.shape)
    
    @staticmethod
    def scaling(x, sigma=0.1):
        """স্কেলিং অগমেন্টেশন"""
        factor = np.random.normal(1, sigma, (1, x.shape[1]))
        return x * factor
    
    @staticmethod
    def time_warp(x, sigma=0.2):
        """টাইম ওয়ার্পিং"""
        orig_steps = np.arange(x.shape[0])
        random_steps = orig_steps + np.random.normal(0, sigma, x.shape[0])
        random_steps = np.clip(random_steps, 0, x.shape[0]-1)
        
        warped = np.zeros_like(x)
        for i, col in enumerate(range(x.shape[1])):
            warped[:, col] = np.interp(orig_steps, random_steps, x[:, col])
        return warped
    
    @staticmethod
    def magnitude_warp(x, sigma=0.2):
        """ম্যাগনিটিউড ওয়ার্পিং"""
        curve = np.random.normal(1, sigma, x.shape[0])
        curve = np.cumsum(curve)
        curve = curve / curve[-1]  # নরমালাইজ
        return x * curve.reshape(-1, 1)

# ডেমো
x = np.random.randn(100, 5)
aug = TimeSeriesAugmentation()

print(f"অরিজিনাল: {x.shape}")
print(f"জিটার: {aug.jitter(x).shape}")
print(f"স্কেলিং: {aug.scaling(x).shape}")
print(f"টাইম ওয়ার্প: {aug.time_warp(x).shape}")
print(f"ম্যাগনিটিউড ওয়ার্প: {aug.magnitude_warp(x).shape}")
```

## সিকোয়েন্স মডেল ইভালুয়েশন

```python
def sequence_metrics(y_true, y_pred, threshold=0.0):
    """সিকোয়েন্স মডেল ইভালুয়েশন মেট্রিক্স"""
    y_true = np.array(y_true).flatten()
    y_pred = np.array(y_pred).flatten()
    
    # MSE/MAE
    mse = np.mean((y_true - y_pred) ** 2)
    mae = np.mean(np.abs(y_true - y_pred))
    
    # ডাইরেকশনাল অ্যাকুরেসি
    direction_true = np.sign(np.diff(y_true))
    direction_pred = np.sign(np.diff(y_pred))
    directional_acc = np.mean(direction_true == direction_pred) * 100
    
    # স্মুথনেস এরর
    smoothness_true = np.std(np.diff(y_true))
    smoothness_pred = np.std(np.diff(y_pred))
    smoothness_error = abs(smoothness_true - smoothness_pred) / smoothness_true * 100
    
    # ল্যাগ কোরিলেশন
    from scipy.stats import pearsonr
    corr, _ = pearsonr(y_true, y_pred) if len(y_true) > 1 else (0, 1)
    
    return {
        'MSE': mse,
        'RMSE': np.sqrt(mse),
        'MAE': mae,
        'MAPE': np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100,
        'Directional Accuracy': directional_acc,
        'Pearson Correlation': corr,
        'Smoothness Error (%)': smoothness_error
    }

# সিমুলেটেড রেজাল্ট
y_true = np.sin(np.linspace(0, 10, 100)) + 0.1 * np.random.randn(100)
y_pred = np.sin(np.linspace(0.1, 10.1, 100)) + 0.15 * np.random.randn(100)

metrics = sequence_metrics(y_true, y_pred)
print(f"{'মেট্রিক':<30} {'মান':<15}")
print("-" * 45)
for k, v in metrics.items():
    print(f"{k:<30} {v:<15.4f}")
```

## প্র্যাকটিক্যাল টিপস

### সিকোয়েন্স মডেলিং বেস্ট প্র্যাকটিস

1. **ডেটা প্রিপ্রসেসিং**
   - নরমালাইজেশন/স্ট্যান্ডার্ডাইজেশন
   - আউটলায়ার হ্যান্ডলিং
   - মিসিং ভ্যালু ইম্পিউটেশন

2. **আর্কিটেকচার ডিজাইন**
   - স্ট্যাকড LSTM বনাম বিডাইরেকশনাল
   - অ্যাটেনশন মেকানিজম যোগ
   - রেসিডুয়াল কানেকশন

3. **ট্রেনিং স্ট্র্যাটেজি**
   - গ্র্যাডিয়েন্ট ক্লিপিং
   - লার্নিং রেট শিডিউলিং
   - আর্লি স্টপিং

4. **ইভালুয়েশন**
   - ওয়াক-ফরোয়ার্ড ভ্যালিডেশন
   - মাল্টিপল মেট্রিক্স
   - ব্যক্তেস্টিং

```python
# ওয়াক-ফরোয়ার্ড ভ্যালিডেশন
def walk_forward_validation(model_class, X, y, window_size=500, step=100):
    """টাইম সিরিজ ওয়াক-ফরোয়ার্ড ভ্যালিডেশন"""
    n = len(X)
    predictions, actuals = [], []
    
    for start in range(0, n - window_size, step):
        train_end = start + window_size
        test_end = min(train_end + step, n)
        
        X_train, y_train = X[start:train_end], y[start:train_end]
        X_test, y_test = X[train_end:test_end], y[train_end:test_end]
        
        # মডেল ট্রেন ও প্রেডিক্ট
        model = model_class()
        # ... ট্রেনিং ...
        
        # প্রেডিকশন
        pred = model.predict(X_test)
        predictions.extend(pred)
        actuals.extend(y_test)
    
    return np.array(predictions), np.array(actuals)

print("✅ ওয়াক-ফরোয়ার্ড ভ্যালিডেশন প্যাটার্ন ডিফাইন্ড")
```

## সারাংশ
- সিকোয়েন্স মডেল অর্ডারভিত্তিক ডেটার জন্য ডিজাইন করা
- মাল্টিপল আর্কিটেকচার: LSTM, GRU, বিডাইরেকশনাল, Seq2Seq
- ফিন্যান্সে স্টক, সেন্টিমেন্ট, ভলাটিলিটি অ্যানালাইসিস
- ডেটা অগমেন্টেশন পারফরম্যান্স উন্নত করে
- ওয়াক-ফরোয়ার্ড ভ্যালিডেশন টাইম সিরিজের জন্য সবচেয়ে নির্ভরযোগ্য