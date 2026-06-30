# Day 56: ক্যাপস্টোন প্রজেক্ট — ডেটা প্রিপারেশন 🏗️📊

## ক্যাপস্টোন প্রজেক্ট ওভারভিউ
আমরা একটি সম্পূর্ণ ডিপ লার্নিং ফিন্যান্স প্রজেক্ট তৈরি করব: **LSTM-বেসড স্টক প্রাইস প্রেডিকশন + RL ট্রেডিং সিস্টেম**।

### প্রজেক্ট আর্কিটেকচার
```
ডেটা প্রিপ → LSTM মডেল → ইভালুয়েশন → RL ট্রেডিং → পোর্টফোলিও অপ্টিমাইজেশন
Day 56         Day 57        Day 58         Day 59           Day 60
```

### আজকের লক্ষ্য (Day 56)
1. মার্কেট ডেটা সিমুলেট/জেনারেট করা
2. ফিচার ইঞ্জিনিয়ারিং (টেকনিক্যাল ইন্ডিকেটর)
3. ট্রেন/ভ্যালিডেশন/টেস্ট স্প্লিট
4. ডেটা নরমালাইজেশন এবং সিকোয়েন্স তৈরি
5. PyTorch DataLoader প্রস্তুত

## ডেটা প্রিপারেশন পাইপলাইন

```python
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. ফিন্যান্সিয়াল ডেটা সিমুলেশন

```python
class MarketDataSimulator:
    """রিয়ালিস্টিক মার্কেট ডেটা সিমুলেটর"""
    def __init__(self, n_days=1000, start_price=100.0, 
                 volatility=0.02, drift=0.0001):
        self.n_days = n_days
        self.start_price = start_price
        self.volatility = volatility
        self.drift = drift
    
    def simulate(self):
        """GMB (Geometric Brownian Motion) দিয়ে প্রাইস সিমুলেট"""
        dt = 1/252  # দৈনিক টাইমস্টেপ
        returns = np.random.normal(
            self.drift * dt, 
            self.volatility * np.sqrt(dt), 
            self.n_days
        )
        
        # প্রাইস সিরিজ
        prices = self.start_price * np.exp(np.cumsum(returns))
        
        # ভলিউম সিমুলেট (প্রাইসের সাথে সম্পর্কিত)
        volume = 1000000 + np.random.randn(self.n_days) * 200000
        volume = np.abs(volume) + 100000
        
        # হাই-লো প্রাইস
        high = prices * (1 + np.abs(np.random.randn(self.n_days)) * 0.015)
        low = prices * (1 - np.abs(np.random.randn(self.n_days)) * 0.015)
        
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=self.n_days, freq='B'),
            'open': prices * (1 + np.random.randn(self.n_days) * 0.002),
            'high': high,
            'low': low,
            'close': prices,
            'volume': volume
        })
        
        return df
    
    def load_real_data(self, ticker='AAPL', start='2020-01-01', end='2024-01-01'):
        """(সিমুলেটেড) রিয়েল ডেটা লোড — প্র্যাকটিসের জন্য"""
        print(f"রিয়েল ডেটা: {ticker} ({start} to {end})")
        print("⚠️ NOTE: API কী ছাড়া রিয়েল ডেটা লোড করা সম্ভব নয়।")
        print("সিমুলেটেড ডেটা ব্যবহার করা হবে।")
        return self.simulate()

# ডেটা জেনারেট
print("=== মার্কেট ডেটা জেনারেশন ===")
simulator = MarketDataSimulator(n_days=1000)
df = simulator.simulate()
print(f"ডেটা শেপ: {df.shape}")
print(df.head())
print(f"\nপ্রাইস রেঞ্জ: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
```

## 2. টেকনিক্যাল ইন্ডিকেটর

```python
class TechnicalIndicators:
    """টেকনিক্যাল ইন্ডিকেটর ফিচার ইঞ্জিনিয়ারিং"""
    
    @staticmethod
    def add_all_indicators(df):
        """সব ইন্ডিকেটর যোগ করুন"""
        df = df.copy()
        
        # প্রাইস-বেসড ফিচার
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        df['high_low_ratio'] = (df['high'] - df['low']) / df['close']
        df['close_open_ratio'] = (df['close'] - df['open']) / df['open']
        
        # মুভিং এভারেজেস
        for period in [5, 10, 20, 50, 200]:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
            df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        
        # প্রাইস থেকে SMA অনুপাত
        for period in [10, 20, 50]:
            df[f'price_to_sma_{period}'] = df['close'] / df[f'sma_{period}'] - 1
        
        # RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df['rsi_14'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # বোলিঞ্জার ব্যান্ডস
        sma_20 = df['close'].rolling(window=20).mean()
        std_20 = df['close'].rolling(window=20).std()
        df['bb_upper'] = sma_20 + 2 * std_20
        df['bb_lower'] = sma_20 - 2 * std_20
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'] + 1e-10)
        
        # ATR (Average True Range)
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr_14'] = tr.rolling(window=14).mean()
        
        # ভলিউম ইন্ডিকেটর
        df['volume_sma_5'] = df['volume'].rolling(window=5).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_5']
        
        # টার্গেট: ভবিষ্যৎ রিটার্ন
        df['target_5d'] = df['close'].shift(-5) / df['close'] - 1
        df['target_1d'] = df['close'].shift(-1) / df['close'] - 1
        
        # ক্লাসিফিকেশন টার্গেট
        df['target_class'] = 0  # 0: DOWN, 1: NEUTRAL, 2: UP
        df.loc[df['target_5d'] > 0.02, 'target_class'] = 2
        df.loc[df['target_5d'] < -0.02, 'target_class'] = 0
        df.loc[(df['target_5d'] >= -0.02) & (df['target_5d'] <= 0.02), 'target_class'] = 1
        
        return df

# ইন্ডিকেটর যোগ
print("\n=== টেকনিক্যাল ইন্ডিকেটর ===")
df = TechnicalIndicators.add_all_indicators(df)
print(f"ফিচার কাউন্ট: {len(df.columns)}")
print(f"কলাম: \n{sorted(list(df.columns))}")
print(f"\nNaN মান: {df.isnull().sum().sum()}")
```

## 3. ডেটা ক্লিনিং এবং নরমালাইজেশন

```python
class DataPreprocessor:
    """ডেটা ক্লিনিং এবং নরমালাইজেশন"""
    
    def __init__(self):
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.feature_columns = None
    
    def clean_data(self, df, drop_na=True):
        """ডেটা ক্লিন"""
        df = df.copy()
        
        # NaN হ্যান্ডেল (ড্রপ বা ফরওয়ার্ড ফিল)
        if drop_na:
            # প্রথম ২০০ রো (সব ইন্ডিকেটরের জন্য উইন্ডো লাগে)
            df = df.iloc[200:].reset_index(drop=True)
        
        # ইনফিনিটি রিমুভ
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna()
        
        return df
    
    def select_features(self, df):
        """ফিচার সিলেক্ট"""
        # কোর ফিচার কলাম
        feature_cols = [
            'returns', 'log_returns', 'high_low_ratio', 'close_open_ratio',
            'price_to_sma_10', 'price_to_sma_20', 'price_to_sma_50',
            'rsi_14', 'macd', 'macd_signal', 'macd_hist',
            'bb_position', 'atr_14', 'volume_ratio'
        ]
        
        self.feature_columns = feature_cols
        return df[feature_cols]
    
    def normalize(self, X_train, X_val, X_test, y_train=None, y_val=None, y_test=None):
        """ফিচার নরমালাইজেশন"""
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        X_val_scaled = self.scaler_X.transform(X_val)
        X_test_scaled = self.scaler_X.transform(X_test)
        
        result = (X_train_scaled, X_val_scaled, X_test_scaled)
        
        if y_train is not None:
            y_train_scaled = self.scaler_y.fit_transform(y_train.reshape(-1, 1))
            y_val_scaled = self.scaler_y.transform(y_val.reshape(-1, 1))
            y_test_scaled = self.scaler_y.transform(y_test.reshape(-1, 1))
            result = (X_train_scaled, X_val_scaled, X_test_scaled,
                     y_train_scaled, y_val_scaled, y_test_scaled)
        
        return result

# ক্লিন এবং সিলেক্ট
print("\n=== ডেটা প্রিপ্রসেসিং ===")
preprocessor = DataPreprocessor()
df_clean = preprocessor.clean_data(df)
print(f"ক্লিন ডেটা: {df_clean.shape}")

X = preprocessor.select_features(df_clean)
y_reg = df_clean['target_5d'].values  # রিগ্রেশন টার্গেট
y_cls = df_clean['target_class'].values  # ক্লাসিফিকেশন টার্গেট

print(f"ফিচার ম্যাট্রিক্স: {X.shape}")
print(f"রিগ্রেশন টার্গেট: {y_reg.shape}")
print(f"ক্লাসিফিকেশন টার্গেট: {y_cls.shape}")
print(f"টার্গেট ডিস্ট্রিবিউশন: DOWN={sum(y_cls==0)}, NEUTRAL={sum(y_cls==1)}, UP={sum(y_cls==2)}")
```

## 4. সিকোয়েন্স ডেটাসেট তৈরি

```python
class TimeSeriesDataset(Dataset):
    """টাইম সিরিজ সিকোয়েন্স ডেটাসেট"""
    def __init__(self, X, y, seq_length=30, target_type='regression'):
        self.X = torch.FloatTensor(X)
        self.seq_length = seq_length
        self.target_type = target_type
        
        if target_type == 'regression':
            self.y = torch.FloatTensor(y)
        else:  # classification
            self.y = torch.LongTensor(y)
    
    def __len__(self):
        return len(self.X) - self.seq_length
    
    def __getitem__(self, idx):
        X_seq = self.X[idx:idx + self.seq_length]
        
        if self.target_type == 'regression':
            y_target = self.y[idx + self.seq_length]
        else:
            y_target = self.y[idx + self.seq_length]
        
        return X_seq, y_target

def create_sequences(X, y, seq_length=30, test_size=0.2, val_size=0.1):
    """সিকোয়েন্স তৈরি এবং ট্রেন/ভ্যাল/টেস্ট স্প্লিট"""
    
    # টাইম-অর্ডার সংরক্ষণ করে স্প্লিট
    n = len(X)
    n_test = int(n * test_size)
    n_val = int(n * val_size)
    n_train = n - n_test - n_val
    
    X_train, y_train = X[:n_train], y[:n_train]
    X_val, y_val = X[n_train:n_train+n_val], y[n_train:n_train+n_val]
    X_test, y_test = X[-n_test:], y[-n_test:]
    
    print(f"\n=== ডেটা স্প্লিট ===")
    print(f"ট্রেন: {len(X_train)} ({(len(X_train)/n)*100:.0f}%)")
    print(f"ভ্যালিডেশন: {len(X_val)} ({(len(X_val)/n)*100:.0f}%)")
    print(f"টেস্ট: {len(X_test)} ({(len(X_test)/n)*100:.0f}%)")
    
    # ডেটাসেট তৈরি
    train_dataset = TimeSeriesDataset(X_train, y_train, seq_length, 'classification')
    val_dataset = TimeSeriesDataset(X_val, y_val, seq_length, 'classification')
    test_dataset = TimeSeriesDataset(X_test, y_test, seq_length, 'classification')
    
    # DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    print(f"\nসিকোয়েন্স ডেটাসেট (seq_length={seq_length}):")
    print(f"ট্রেন ব্যাচ: {len(train_loader)}")
    print(f"ভ্যাল ব্যাচ: {len(val_loader)}")
    print(f"টেস্ট ব্যাচ: {len(test_loader)}")
    
    return train_loader, val_loader, test_loader, (X_train, y_train)

# ডেটা রেডি
print("\n=== সিকোয়েন্স ডেটাসেট তৈরি ===")
train_loader, val_loader, test_loader, _ = create_sequences(
    X.values, y_cls, seq_length=30
)

# ডেটা স্যাম্পল চেক
sample_X, sample_y = next(iter(train_loader))
print(f"\nস্যাম্পল ব্যাচ:")
print(f"  X শেপ: {sample_X.shape} [batch, seq_len, features]")
print(f"  y শেপ: {sample_y.shape} [batch]")
print(f"  y ভ্যালুস: {sample_y[:10].numpy()}")
```

## 5. ডেটা সংরক্ষণ

```python
def save_prepared_data(train_loader, val_loader, test_loader, 
                       preprocessor, feature_cols, filepath='capstone_data.pt'):
    """প্রিপেয়ারড ডেটা সেভ করুন (পরবর্তী দিনের জন্য)"""
    
    # ডেটা এক্সট্র্যাক্ট
    train_data = []
    for X, y in train_loader:
        train_data.append((X.cpu(), y.cpu()))
    
    val_data = []
    for X, y in val_loader:
        val_data.append((X.cpu(), y.cpu()))
    
    test_data = []
    for X, y in test_loader:
        test_data.append((X.cpu(), y.cpu()))
    
    data_package = {
        'train_data': train_data,
        'val_data': val_data,
        'test_data': test_data,
        'feature_columns': feature_cols,
        'scaler_X': preprocessor.scaler_X,
        'seq_length': 30,
        'n_features': len(feature_cols),
        'n_classes': 3
    }
    
    torch.save(data_package, filepath)
    print(f"\n✅ ডেটা সেভ করা হয়েছে: {filepath}")
    print(f"   ফিচার: {data_package['n_features']}")
    print(f"   ক্লাস: {data_package['n_classes']}")
    print(f"   সিকোয়েন্স লেন্থ: {data_package['seq_length']}")

# ডেটা সেভ
save_prepared_data(train_loader, val_loader, test_loader, 
                   preprocessor, X.columns.tolist())
```

## সারাংশ
- ক্যাপস্টোন প্রজেক্ট শুরু হয়েছে — LSTM + RL ট্রেডিং সিস্টেম
- মার্কেট ডেটা সিমুলেট/জেনারেট করা হয়েছে (OHLCV)
- টেকনিক্যাল ইন্ডিকেটর যোগ করা হয়েছে (RSI, MACD, BB, SMA, ATR)
- ডেটা ক্লিন, নরমালাইজ, এবং সিকোয়েন্স ফরম্যাটে রূপান্তর
- PyTorch DataLoader প্রস্তুত (train/val/test)
- ডেটা সেভ করা হয়েছে (পরবর্তী দিনে ব্যবহারের জন্য)