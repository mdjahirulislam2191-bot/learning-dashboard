# Day 29: এনকোডার-ডিকোডার আর্কিটেকচার 🔐➡️🔓

## এনকোডার-ডিকোডার কী?
এনকোডার-ডিকোডার আর্কিটেকচার একটি সিকোয়েন্স-টু-সিকোয়েন্স (Seq2Seq) মডেল যা ভেরিয়েবল-লেন্থ ইনপুটকে ভেরিয়েবল-লেন্থ আউটপুটে ম্যাপ করে।

### আর্কিটেকচার ওভারভিউ
```
ইনপুট:       x1 → x2 → x3 → x4    (এনকোডার)
                    ↓
           [কনটেক্সট ভেক্টর]
                    ↓
আউটপুট:      y1 → y2 → y3 → <EOS>  (ডিকোডার)
```

### প্রধান উপাদান
1. **এনকোডার (Encoder)**: ইনপুট সিকোয়েন্স প্রসেস করে কনটেক্সট ভেক্টর তৈরি
2. **কনটেক্সট ভেক্টর (Context Vector)**: সম্পূর্ণ ইনপুটের সারাংশ
3. **ডিকোডার (Decoder)**: কনটেক্সট থেকে আউটপুট জেনারেট

### ফিন্যান্স অ্যাপ্লিকেশন
- **মাল্টি-স্টেপ ফোরকাস্টিং**: একাধিক দিনের প্রাইস প্রেডিকশন
- **পোর্টফোলিও অ্যালোকেশন**: ইনপুট ফিচার → অ্যাসেট ওয়েট
- **রিস্ক ম্যানেজমেন্ট**: মাল্টি-পিরিয়ড রিস্ক ফোরকাস্টিং
- **অ্যালগরিদমিক ট্রেডিং**: মার্কেট ডেটা → ট্রেডিং সিগন্যাল

## সিম্পল এনকোডার-ডিকোডার

```python
import torch
import torch.nn as nn
import numpy as np

class Encoder(nn.Module):
    """এনকোডার: ইনপুট সিকোয়েন্স প্রসেস"""
    def __init__(self, input_size, hidden_size, num_layers=2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
    
    def forward(self, x):
        # x: (batch, seq_len, input_size)
        out, (hidden, cell) = self.lstm(x)
        return hidden, cell  # ডিকোডারকে দেওয়ার জন্য

class Decoder(nn.Module):
    """ডিকোডার: কনটেক্সট থেকে আউটপুট জেনারেট"""
    def __init__(self, output_size, hidden_size, num_layers=2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(output_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x, hidden, cell):
        # x: (batch, 1, output_size) - এক টাইমস্টেপ
        out, (hidden, cell) = self.lstm(x, (hidden, cell))
        pred = self.fc(out)  # (batch, 1, output_size)
        return pred, hidden, cell

class EncoderDecoder(nn.Module):
    """সম্পূর্ণ এনকোডার-ডিকোডার"""
    def __init__(self, encoder, decoder, target_len):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.target_len = target_len
    
    def forward(self, x, target=None, teacher_forcing_ratio=0.5):
        batch = x.size(0)
        output_size = self.decoder.fc.out_features
        
        # এনকোড
        hidden, cell = self.encoder(x)
        
        # ডিকোডার ইনপুট (শেষ ইনপুটের শেষ ফিচার)
        decoder_input = x[:, -1:, :1]  # (batch, 1, 1)
        
        # আউটপুট স্টোর
        outputs = torch.zeros(batch, self.target_len, output_size)
        
        for t in range(self.target_len):
            decoder_output, hidden, cell = self.decoder(
                decoder_input, hidden, cell)
            outputs[:, t:t+1, :] = decoder_output
            
            # টিচার ফোর্সিং
            if target is not None and np.random.random() < teacher_forcing_ratio:
                decoder_input = target[:, t:t+1, :]
            else:
                decoder_input = decoder_output
        
        return outputs

# টেস্ট
encoder = Encoder(input_size=5, hidden_size=128, num_layers=2)
decoder = Decoder(output_size=1, hidden_size=128, num_layers=2)
model = EncoderDecoder(encoder, decoder, target_len=10)

x = torch.randn(16, 20, 5)  # batch=16, seq_len=20, features=5
output = model(x)
print(f"এনকোডার-ডিকোডার আউটপুট: {output.shape}")  # (16, 10, 1)
```

## অ্যাটেনশন সহ এনকোডার-ডিকোডার

```python
class AttentionDecoder(nn.Module):
    """অ্যাটেনশন সহ ডিকোডার"""
    def __init__(self, output_size, hidden_size, num_layers=2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(output_size, hidden_size, num_layers, batch_first=True)
        self.attention = nn.Linear(hidden_size * 2, 1)
        self.fc = nn.Linear(hidden_size * 2, output_size)
    
    def forward(self, x, hidden, cell, encoder_outputs):
        # x: (batch, 1, output_size)
        out, (hidden, cell) = self.lstm(x, (hidden, cell))
        
        # অ্যাটেনশন
        seq_len = encoder_outputs.size(1)
        hidden_expanded = hidden[-1].unsqueeze(1).repeat(1, seq_len, 1)
        
        energy = torch.tanh(encoder_outputs + hidden_expanded)
        attn_weights = torch.softmax(self.attention(energy), dim=1)
        context = torch.sum(attn_weights * encoder_outputs, dim=1, keepdim=True)
        
        # কনটেক্সট + LSTM আউটপুট
        combined = torch.cat((context, out), dim=-1)
        pred = self.fc(combined)
        
        return pred, hidden, cell, attn_weights

class AttnEncoderDecoder(nn.Module):
    """অ্যাটেনশন সহ সম্পূর্ণ এনকোডার-ডিকোডার"""
    def __init__(self, input_size, hidden_size, output_size, 
                 target_len, num_layers=2):
        super().__init__()
        self.target_len = target_len
        
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers, 
                              batch_first=True, bidirectional=True)
        self.decoder = AttentionDecoder(output_size, hidden_size * 2, num_layers)
    
    def forward(self, x):
        encoder_outputs, (hidden, cell) = self.encoder(x)
        
        # এনকোডার বিডাইরেকশনাল → ডিকোডারের জন্য অ্যাডজাস্ট
        hidden = hidden[-2:]  # শেষ লেয়ারের ফরোয়ার্ড + ব্যাকওয়ার্ড
        
        decoder_input = x[:, -1:, :1]
        outputs = []
        
        for _ in range(self.target_len):
            decoder_output, hidden, cell, attn = self.decoder(
                decoder_input, hidden, cell, encoder_outputs)
            outputs.append(decoder_output)
            decoder_input = decoder_output
        
        return torch.cat(outputs, dim=1)

# টেস্ট
attn_model = AttnEncoderDecoder(
    input_size=5, hidden_size=128, output_size=1, target_len=10
)
x = torch.randn(16, 20, 5)
output = attn_model(x)
print(f"অ্যাটেনশন এনকোডার-ডিকোডার আউটপুট: {output.shape}")
```

## ফিন্যান্স: মাল্টি-স্টেপ ফোরকাস্টিং

```python
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

# সিন্থেটিক ডেটা
np.random.seed(42)
n = 2000
seq_len = 20
forecast_horizon = 10
n_features = 3

# ট্রেন্ড + সিজনাল + নয়েজ
t = np.linspace(0, 50, n)
data = np.column_stack([
    100 + 0.5*t + 10*np.sin(0.1*t) + np.random.randn(n) * 2,
    50 + 0.3*t + 5*np.sin(0.15*t) + np.random.randn(n) * 1.5,
    np.random.randn(n) * 0.5  # ভলাটিলিটি
])

# সিকোয়েন্স তৈরি
X, y = [], []
for i in range(n - seq_len - forecast_horizon):
    X.append(data[i:i+seq_len])
    y.append(data[i+seq_len:i+seq_len+forecast_horizon, 0:1])  # শুধু ১ম ফিচার ফোরকাস্ট

X, y = np.array(X), np.array(y)
print(f"X: {X.shape}, y: {y.shape}")

# ট্রেন/টেস্ট
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# মডেল ট্রেনিং
encoder = Encoder(input_size=n_features, hidden_size=128, num_layers=2)
decoder = Decoder(output_size=1, hidden_size=128, num_layers=2)
model = EncoderDecoder(encoder, decoder, target_len=forecast_horizon)

optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# DataLoader
train_dataset = TensorDataset(
    torch.FloatTensor(X_train),
    torch.FloatTensor(y_train)
)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# ট্রেনিং
epochs = 80
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for bx, by in train_loader:
        optimizer.zero_grad()
        predictions = model(bx, by, teacher_forcing_ratio=0.5)
        loss = criterion(predictions, by)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.6f}")

# ইভালুয়েশন
model.eval()
with torch.no_grad():
    X_test_t = torch.FloatTensor(X_test)
    predictions = model(X_test_t, teacher_forcing_ratio=0)
    test_loss = criterion(predictions, torch.FloatTensor(y_test))

print(f"\n✅ টেস্ট MSE: {test_loss:.6f}")
print(f"প্রথম স্যাম্পলের প্রেডিকশন:")
print(f"  প্রেডিক্টেড: {predictions[0, :, 0].numpy()}")
print(f"  আসল:        {y_test[0, :, 0]}")
```

## টিচার ফোর্সিং

```python
class TeacherForcingScheduler:
    """টিচার ফোর্সিং রেশিও শিডিউলার"""
    def __init__(self, initial_ratio=1.0, final_ratio=0.0, decay_epochs=50):
        self.initial = initial_ratio
        self.final = final_ratio
        self.decay = decay_epochs
    
    def get_ratio(self, epoch):
        """কারেন্ট ইপকের জন্য টিচার ফোর্সিং রেশিও"""
        if epoch >= self.decay:
            return self.final
        ratio = self.initial - (self.initial - self.final) * epoch / self.decay
        return ratio

# ডেমো
scheduler = TeacherForcingScheduler(1.0, 0.0, 50)
print("টিচার ফোর্সিং ডিকেয়:")
for epoch in [0, 10, 25, 50, 75]:
    print(f"  Epoch {epoch}: tf_ratio = {scheduler.get_ratio(epoch):.2f}")
```

## এনকোডার-ডিকোডার বেস্ট প্র্যাকটিস

```python
class EnhancedEncoderDecoder(nn.Module):
    """এনহ্যান্সড এনকোডার-ডিকোডার"""
    def __init__(self, input_size, hidden_size, output_size, 
                 target_len, num_layers=2, dropout=0.3):
        super().__init__()
        self.target_len = target_len
        
        # এনকোডার
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers,
                              batch_first=True, dropout=dropout)
        self.encoder_dropout = nn.Dropout(dropout)
        
        # ডিকোডার
        self.decoder = nn.LSTM(output_size, hidden_size, num_layers,
                              batch_first=True, dropout=dropout)
        self.decoder_dropout = nn.Dropout(dropout)
        
        # আউটপুট
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, output_size)
        )
    
    def forward(self, x, teacher_forcing=False, target=None):
        batch = x.size(0)
        
        # এনকোড
        _, (hidden, cell) = self.encoder(x)
        
        # ডিকোড
        decoder_input = x[:, -1:, :self.fc[0].in_features].detach()
        outputs = []
        
        for t in range(self.target_len):
            out, (hidden, cell) = self.decoder(decoder_input, (hidden, cell))
            out = self.decoder_dropout(out)
            pred = self.fc(out)
            outputs.append(pred)
            
            if teacher_forcing and target is not None:
                decoder_input = target[:, t:t+1, :]
            else:
                decoder_input = pred.detach()
        
        return torch.cat(outputs, dim=1)

# টেস্ট
enhanced = EnhancedEncoderDecoder(
    input_size=5, hidden_size=128, output_size=1, 
    target_len=10, num_layers=2, dropout=0.3
)
x = torch.randn(16, 20, 5)
out = enhanced(x)
print(f"এনহ্যান্সড মডেল আউটপুট: {out.shape}")

total_params = sum(p.numel() for p in enhanced.parameters())
print(f"মোট প্যারামিটার: {total_params:,}")
```

## সারাংশ
- এনকোডার-ডিকোডার সিকোয়েন্স-টু-সিকোয়েন্স মডেলের বেস
- এনকোডার ইনপুট কম্প্রেস করে কনটেক্সট ভেক্টরে
- ডিকোডার কনটেক্সট থেকে আউটপুট জেনারেট করে
- অ্যাটেনশন যোগ করলে লং-রেঞ্জ ডিপেন্ডেন্সি ভালো হয়
- টিচার ফোর্সিং ট্রেনিংকে স্টেবল করে
- ফিন্যান্সে মাল্টি-স্টেপ ফোরকাস্টিং, পোর্টফোলিও অপ্টিমাইজেশন