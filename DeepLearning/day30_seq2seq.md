# Day 30: Seq2Seq মডেলস 🔄

## Seq2Seq মডেল কী?
Seq2Seq (Sequence-to-Sequence) মডেল একটি এনকোডার-ডিকোডার আর্কিটেকচার যা একটি সিকোয়েন্স ইনপুট নিয়ে অন্য একটি সিকোয়েন্স আউটপুট তৈরি করে।

### অ্যাপ্লিকেশন
- **মেশিন ট্রান্সলেশন**: ইংরেজি → বাংলা
- **টেক্সট সামারি**: লং টেক্সট → শর্ট টেক্সট
- **টাইম সিরিজ ফোরকাস্টিং**: পেস্ট → ফিউচার
- **নিউজ ট্রেডিং সিগন্যাল**: নিউজ → ট্রেড ডিসিশন
- **মাল্টি-স্টেপ স্টক প্রেডিকশন**: ৩০ দিন → পরবর্তী ১৫ দিন

### ইনপুট-আউটপুট ভ্যারিয়েন্ট
| টাইপ | ইনপুট | আউটপুট | উদাহরণ |
|---|---|---|---|
| Many-to-Many | সিকোয়েন্স | সিকোয়েন্স (একই লেন্থ) | NER ট্যাগিং |
| Many-to-One | সিকোয়েন্স | সিঙ্গল | সেন্টিমেন্ট |
| Seq2Seq | সিকোয়েন্স | সিকোয়েন্স (ভিন্ন লেন্থ) | ট্রান্সলেশন, ফোরকাস্টিং |

## PyTorch Seq2Seq ইমপ্লিমেন্টেশন

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")
```

## 1. বেসিক Seq2Seq মডেল

```python
class Seq2Seq(nn.Module):
    """কমপ্লিট Seq2Seq মডেল"""
    def __init__(self, input_size, hidden_size, output_size, 
                 num_layers=2, dropout=0.3):
        super().__init__()
        
        self.encoder = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        self.decoder = nn.LSTM(
            output_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, output_size)
        )
        
        self.num_layers = num_layers
        self.hidden_size = hidden_size
    
    def forward(self, src, trg=None, teacher_forcing_ratio=0.5):
        batch_size = src.shape[0]
        trg_len = trg.shape[1] if trg is not None else 10
        output_size = self.fc[-1].out_features
        
        # এনকোডার
        _, (hidden, cell) = self.encoder(src)
        
        # ডিকোডার ইনপুট (শেষ টাইমস্টেপের শেষ ফিচার)
        decoder_input = src[:, -1:, :output_size]
        
        outputs = torch.zeros(batch_size, trg_len, output_size).to(src.device)
        
        for t in range(trg_len):
            decoder_output, (hidden, cell) = self.decoder(
                decoder_input, (hidden, cell))
            prediction = self.fc(decoder_output)
            outputs[:, t:t+1, :] = prediction
            
            # টিচার ফোর্সিং
            if trg is not None and np.random.random() < teacher_forcing_ratio:
                decoder_input = trg[:, t:t+1, :]
            else:
                decoder_input = prediction
        
        return outputs

# মডেল চেক
model = Seq2Seq(input_size=5, hidden_size=128, output_size=1, num_layers=2)
x = torch.randn(16, 20, 5)
y = model(x)  # ডিফল্ট ১০ স্টেপ
print(f"Seq2Seq আউটপুট: {y.shape}")
```

## 2. ফিন্যান্স: মাল্টি-স্টক প্রাইস ফোরকাস্টিং

```python
# মাল্টি-স্টক সিন্থেটিক ডেটা
np.random.seed(42)
n_stocks = 3
n_days = 2000

stock_prices = []
for i in range(n_stocks):
    ret = np.random.randn(n_days) * 0.02
    price = 100 * np.exp(np.cumsum(ret + 0.0002))
    stock_prices.append(price)

stock_data = np.column_stack(stock_prices)  # (2000, 3)

# নরমালাইজ
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
stock_scaled = scaler.fit_transform(stock_data)

# Seq2Seq ডেটা প্রিপারেশন
def create_seq2seq_data(data, enc_len=30, dec_len=10):
    """Seq2Seq ট্রেনিং ডেটা প্রস্তুত"""
    X, Y = [], []
    for i in range(len(data) - enc_len - dec_len):
        X.append(data[i:i+enc_len])
        Y.append(data[i+enc_len:i+enc_len+dec_len])
    return np.array(X), np.array(Y)

enc_len = 30
dec_len = 10

X_seq, Y_seq = create_seq2seq_data(stock_scaled, enc_len, dec_len)
print(f"Seq2Seq ডেটা:")
print(f"  X (এনকোডার ইনপুট): {X_seq.shape}")
print(f"  Y (ডিকোডার আউটপুট): {Y_seq.shape}")

# ট্রেন/টেস্ট স্প্লিট
split = int(0.8 * len(X_seq))
X_train, X_test = X_seq[:split], X_seq[split:]
Y_train, Y_test = Y_seq[:split], Y_seq[split:]
print(f"  ট্রেন: {X_train.shape}, টেস্ট: {X_test.shape}")
```

## 3. মডেল ট্রেনিং

```python
# মডেল
model = Seq2Seq(input_size=n_stocks, hidden_size=128, 
                output_size=n_stocks, num_layers=2).to(device)

optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-5)
criterion = nn.MSELoss()
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)

# DataLoader
train_loader = DataLoader(
    TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(Y_train)),
    batch_size=32, shuffle=True
)

# ট্রেনিং
epochs = 80
for epoch in range(epochs):
    model.train()
    total_loss = 0
    
    for batch_X, batch_Y in train_loader:
        batch_X, batch_Y = batch_X.to(device), batch_Y.to(device)
        
        optimizer.zero_grad()
        predictions = model(batch_X, batch_Y, teacher_forcing_ratio=0.5)
        loss = criterion(predictions, batch_Y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        
        total_loss += loss.item()
    
    scheduler.step()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.6f}")

print("✅ Seq2Seq ট্রেনিং সম্পূর্ণ!")
```

## 4. ইভালুয়েশন ও প্রেডিকশন

```python
model.eval()
X_test_t = torch.FloatTensor(X_test).to(device)
Y_test_t = torch.FloatTensor(Y_test).to(device)

with torch.no_grad():
    predictions = model(X_test_t, teacher_forcing_ratio=0)
    test_loss = criterion(predictions, Y_test_t)

print(f"✅ টেস্ট MSE: {test_loss:.6f}")

# আনস্কেল
pred_actual = scaler.inverse_transform(
    predictions.cpu().numpy().reshape(-1, n_stocks)).reshape(-1, dec_len, n_stocks)
y_test_actual = scaler.inverse_transform(
    Y_test.reshape(-1, n_stocks)).reshape(-1, dec_len, n_stocks)

# পারফরম্যান্স মেট্রিক্স
for i in range(n_stocks):
    mse = np.mean((pred_actual[:, :, i] - y_test_actual[:, :, i])**2)
    mae = np.mean(np.abs(pred_actual[:, :, i] - y_test_actual[:, :, i]))
    print(f"স্টক {i+1}: MSE={mse:.4f}, MAE={mae:.4f}")

# প্রথম স্যাম্পল ভিজুয়ালাইজ
sample_idx = 0
print(f"\nপ্রথম স্যাম্পল (আগামী {dec_len} দিন):")
for d in range(dec_len):
    print(f"  দিন {d+1}: প্রেডিক্টেড={pred_actual[sample_idx, d]}, "
          f"আসল={y_test_actual[sample_idx, d]}")
```

## 5. বিডাইরেকশনাল Seq2Seq

```python
class BidirectionalSeq2Seq(nn.Module):
    """বিডাইরেকশনাল Seq2Seq"""
    def __init__(self, input_size, hidden_size, output_size, num_layers=2, dropout=0.3):
        super().__init__()
        
        # বিডাইরেকশনাল এনকোডার
        self.encoder = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, bidirectional=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # ডিকোডার (hidden_size*2 থেকে ইনপুট)
        self.decoder = nn.LSTM(
            output_size, hidden_size * 2, num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        self.fc = nn.Linear(hidden_size * 2, output_size)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, src, trg=None, teacher_forcing_ratio=0.5):
        batch = src.shape[0]
        trg_len = trg.shape[1] if trg is not None else 10
        output_size = self.fc.out_features
        
        # এনকোড
        encoder_outputs, (hidden, cell) = self.encoder(src)
        
        # বিডাইরেকশনাল হিডেন → ডিকোডার হিডেন
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1).unsqueeze(0).repeat(
            self.decoder.num_layers, 1, 1)
        cell = torch.cat((cell[-2], cell[-1]), dim=1).unsqueeze(0).repeat(
            self.decoder.num_layers, 1, 1)
        
        decoder_input = src[:, -1:, :output_size]
        outputs = torch.zeros(batch, trg_len, output_size).to(src.device)
        
        for t in range(trg_len):
            decoder_output, (hidden, cell) = self.decoder(
                decoder_input, (hidden, cell))
            prediction = self.fc(self.dropout(decoder_output))
            outputs[:, t:t+1, :] = prediction
            
            if trg is not None and np.random.random() < teacher_forcing_ratio:
                decoder_input = trg[:, t:t+1, :]
            else:
                decoder_input = prediction
        
        return outputs

# টেস্ট
bi_model = BidirectionalSeq2Seq(
    input_size=n_stocks, hidden_size=64, output_size=n_stocks, num_layers=2)
x = torch.randn(16, 30, n_stocks)
y = bi_model(x)
print(f"BiSeq2Seq আউটপুট: {y.shape}")

uni_params = sum(p.numel() for p in model.parameters())
bi_params = sum(p.numel() for p in bi_model.parameters())
print(f"ইউনি প্যারামিটার: {uni_params:,}")
print(f"বাই প্যারামিটার: {bi_params:,}")
```

## 6. Seq2Seq অ্যাটেনশন ভিজুয়ালাইজেশন

```python
class Seq2SeqWithAttention(nn.Module):
    """অ্যাটেনশন সহ Seq2Seq"""
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super().__init__()
        
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers,
                              batch_first=True, bidirectional=True)
        self.decoder = nn.LSTM(output_size, hidden_size * 2, num_layers,
                              batch_first=True)
        
        # অ্যাটেনশন
        self.attn = nn.Linear(hidden_size * 4, 1)
        self.fc = nn.Linear(hidden_size * 4, output_size)
    
    def forward(self, src, trg=None, teacher_forcing_ratio=0.5):
        batch = src.shape[0]
        trg_len = trg.shape[1] if trg is not None else 10
        output_size = self.fc.out_features
        
        encoder_outputs, (hidden, cell) = self.encoder(src)
        
        # হিডেন অ্যাডজাস্ট
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1).unsqueeze(0).repeat(
            self.decoder.num_layers, 1, 1)
        cell = torch.cat((cell[-2], cell[-1]), dim=1).unsqueeze(0).repeat(
            self.decoder.num_layers, 1, 1)
        
        decoder_input = src[:, -1:, :output_size]
        outputs = []
        attentions = []
        
        for t in range(trg_len):
            decoder_output, (hidden, cell) = self.decoder(
                decoder_input, (hidden, cell))
            
            # অ্যাটেনশন
            dec_hidden = decoder_output.repeat(1, encoder_outputs.size(1), 1)
            energy = torch.tanh(torch.cat((encoder_outputs, dec_hidden), dim=2))
            attn_scores = self.attn(energy)
            attn_weights = torch.softmax(attn_scores, dim=1)
            context = torch.sum(attn_weights * encoder_outputs, dim=1, keepdim=True)
            
            combined = torch.cat((decoder_output, context), dim=2)
            prediction = self.fc(combined)
            outputs.append(prediction)
            attentions.append(attn_weights)
            
            if trg is not None and np.random.random() < teacher_forcing_ratio:
                decoder_input = trg[:, t:t+1, :]
            else:
                decoder_input = prediction
        
        return torch.cat(outputs, dim=1), torch.cat(attentions, dim=2)

# টেস্ট
attn_seq2seq = Seq2SeqWithAttention(
    input_size=n_stocks, hidden_size=64, output_size=n_stocks, num_layers=2)
x = torch.randn(8, 30, n_stocks)
out, attn_weights = attn_seq2seq(x)
print(f"অ্যাটেনশন Seq2Seq আউটপুট: {out.shape}")
print(f"অ্যাটেনশন ওয়েটস: {attn_weights.shape}")  # (batch, dec_len, enc_len)
```

## 7. প্রেডিকশন এনসেম্বল

```python
class Seq2SeqEnsemble(nn.Module):
    """একাধিক Seq2Seq মডেলের এনসেম্বল"""
    def __init__(self, models):
        super().__init__()
        self.models = nn.ModuleList(models)
    
    def forward(self, x):
        predictions = []
        for model in self.models:
            pred = model(x)
            predictions.append(pred)
        
        # এভারেজ
        return torch.stack(predictions).mean(dim=0)

# ৩টি মডেলের এনসেম্বল
models = [
    Seq2Seq(input_size=n_stocks, hidden_size=64, output_size=n_stocks, num_layers=1),
    Seq2Seq(input_size=n_stocks, hidden_size=128, output_size=n_stocks, num_layers=2),
    Seq2Seq(input_size=n_stocks, hidden_size=64, output_size=n_stocks, num_layers=3)
]

ensemble = Seq2SeqEnsemble(models)
x = torch.randn(4, 30, n_stocks)
out = ensemble(x)
print(f"এনসেম্বল আউটপুট: {out.shape}")
print("✅ এনসেম্বল প্রেডিকশন: ভ্যারিয়েন্স কমায়, অ্যাকুরেসি বাড়ায়")
```

## Seq2Seq বেস্ট প্র্যাকটিস

### 1. টিচার ফোর্সিং
- শুরুতে হাই রেশিও (0.8-1.0)
- ধীরে ধীরে কমিয়ে 0.0
- আল্টারনেটিভ: সিডিউলড স্যাম্পলিং

### 2. গ্র্যাডিয়েন্ট ক্লিপিং
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### 3. লস ফাংশন
- রিগ্রেশন: MSE, MAE, Huber Loss
- ক্লাসিফিকেশন: CrossEntropy

### 4. ইভালুয়েশন
- ওয়াক-ফরোয়ার্ড ভ্যালিডেশন
- মাল্টি-স্টেপ RMSE
- ডাইরেকশনাল অ্যাকুরেসি

```python
# ওয়াক-ফরোয়ার্ড ইভালুয়েশন
def walk_forward_eval(model, data, enc_len, dec_len, step=10):
    """ওয়াক-ফরোয়ার্ড সিমুলেশন"""
    model.eval()
    all_preds, all_actuals = [], []
    
    for i in range(0, len(data) - enc_len - dec_len, step):
        enc_input = torch.FloatTensor(data[i:i+enc_len]).unsqueeze(0)
        actual = data[i+enc_len:i+enc_len+dec_len]
        
        with torch.no_grad():
            prediction = model(enc_input).squeeze(0).numpy()
        
        all_preds.append(prediction)
        all_actuals.append(actual)
    
    return np.array(all_preds), np.array(all_actuals)

print("✅ ওয়াক-ফরোয়ার্ড ফাংশন ডিফাইন্ড")
```

## সারাংশ
- Seq2Seq এনকোডার + ডিকোডার আর্কিটেকচার
- ভেরিয়েবল-লেন্থ সিকোয়েন্স হ্যান্ডেল করতে পারে
- বিডাইরেকশনাল এনকোডার পারফরম্যান্স উন্নত করে
- অ্যাটেনশন মেকানিজম যোগ করা যায়
- ফিন্যান্সে মাল্টি-স্টেপ ফোরকাস্টিং, পোর্টফোলিও ম্যানেজমেন্ট
- টিচার ফোর্সিং, গ্র্যাডিয়েন্ট ক্লিপিং বেস্ট প্র্যাকটিস