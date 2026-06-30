# Day 15: প্রজেক্ট - ANN দিয়ে স্টক প্রাইস প্রেডিকশন 📈

## প্রজেক্ট ওভারভিউ
এই প্রজেক্টে আমরা একটি সম্পূর্ণ ANN মডেল তৈরি করব যা রিয়েল স্টক ডেটা ব্যবহার করে প্রাইস প্রেডিক্ট করবে।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime, timedelta

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
```

## ১. ডেটা কালেকশন ও ফিচার ইঞ্জিনিয়ারিং
```python
class StockDataProcessor:
    """স্টক ডেটা প্রসেসর"""
    
    def __init__(self, ticker, start="2018-01-01", end="2024-01-01"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = None
        self.stats = None
    
    def download_data(self):
        """ইয়াহু ফাইন্যান্স থেকে ডেটা ডাউনলোড"""
        self.data = yf.download(self.ticker, start=self.start, end=self.end)
        print(f"{self.ticker}: {len(self.data)} days of data downloaded")
        return self.data
    
    def add_technical_indicators(self):
        """টেকনিক্যাল ইন্ডিকেটর যোগ করা"""
        df = self.data.copy()
        
        # Moving Averages
        for period in [5, 10, 20, 50, 200]:
            df[f'SMA_{period}'] = df['Close'].rolling(period).mean()
            df[f'EMA_{period}'] = df['Close'].ewm(span=period).mean()
        
        # Volatility
        df['Returns'] = df['Close'].pct_change()
        for period in [5, 10, 20]:
            df[f'Volatility_{period}'] = df['Returns'].rolling(period).std()
        
        # RSI
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(20).mean()
        bb_std = df['Close'].rolling(20).std()
        df['BB_Upper'] = df['BB_Middle'] + 2 * bb_std
        df['BB_Lower'] = df['BB_Middle'] - 2 * bb_std
        
        # Volume indicators
        df['Volume_MA'] = df['Volume'].rolling(10).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # Target: Next day's close
        df['Target'] = df['Close'].shift(-1)
        
        self.data = df.dropna()
        print(f"Features added: {len(self.data.columns)} columns")
        return self.data
    
    def prepare_features(self):
        """ফিচার ও টার্গেট সেপারেশন"""
        exclude = ['Target', 'Close']
        feature_cols = [c for c in self.data.columns if c not in exclude 
                       and 'Date' not in c]
        
        X = self.data[feature_cols].values
        y = self.data['Target'].values.reshape(-1, 1)
        
        # Train/Val/Test split (chronological)
        n = len(X)
        train_end = int(0.7 * n)
        val_end = int(0.85 * n)
        
        X_train = X[:train_end]
        y_train = y[:train_end]
        X_val = X[train_end:val_end]
        y_val = y[train_end:val_end]
        X_test = X[val_end:]
        y_test = y[val_end:]
        
        # Normalization
        X_mean, X_std = X_train.mean(axis=0), X_train.std(axis=0)
        y_mean, y_std = y_train.mean(), y_train.std()
        
        X_train = (X_train - X_mean) / (X_std + 1e-8)
        X_val = (X_val - X_mean) / (X_std + 1e-8)
        X_test = (X_test - X_mean) / (X_std + 1e-8)
        y_train = (y_train - y_mean) / (y_std + 1e-8)
        y_val = (y_val - y_mean) / (y_std + 1e-8)
        y_test = (y_test - y_mean) / (y_std + 1e-8)
        
        self.stats = (X_mean, X_std, y_mean, y_std)
        self.feature_cols = feature_cols
        
        print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
```

## ২. ANN মডেল
```python
class StockPriceANN(nn.Module):
    """স্টক প্রাইস প্রেডিকশন ANN"""
    def __init__(self, input_size, hidden_sizes=[128, 64, 32], dropout=0.2):
        super().__init__()
        
        layers = []
        prev = input_size
        
        for hidden in hidden_sizes:
            layers.extend([
                nn.Linear(prev, hidden),
                nn.BatchNorm1d(hidden),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev = hidden
        
        layers.append(nn.Linear(prev, 1))
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)
```

## ৩. ট্রেনিং ফাংশন
```python
class ModelTrainer:
    """মডেল ট্রেনিং ও ইভালুয়েশন"""
    
    def __init__(self, model, device=device):
        self.model = model.to(device)
        self.device = device
        self.history = {'train_loss': [], 'val_loss': []}
    
    def train(self, X_train, y_train, X_val, y_val, epochs=200, lr=0.001):
        X_tr = torch.FloatTensor(X_train).to(self.device)
        y_tr = torch.FloatTensor(y_train).to(self.device)
        X_v = torch.FloatTensor(X_val).to(self.device)
        y_v = torch.FloatTensor(y_val).to(self.device)
        
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=0.001)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, patience=10, factor=0.5, verbose=True
        )
        
        best_val = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            # Train
            self.model.train()
            optimizer.zero_grad()
            train_pred = self.model(X_tr)
            train_loss = criterion(train_pred, y_tr)
            train_loss.backward()
            optimizer.step()
            
            # Validate
            self.model.eval()
            with torch.no_grad():
                val_pred = self.model(X_v)
                val_loss = criterion(val_pred, y_v)
            
            self.history['train_loss'].append(train_loss.item())
            self.history['val_loss'].append(val_loss.item())
            
            scheduler.step(val_loss)
            
            # Early stopping
            if val_loss < best_val:
                best_val = val_loss
                torch.save(self.model.state_dict(), 'best_stock_model.pth')
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= 25:
                    print(f"Early stopping at epoch {epoch}")
                    break
            
            if (epoch + 1) % 25 == 0:
                print(f"Epoch {epoch+1}: Train={train_loss.item():.4f}, Val={val_loss.item():.4f}")
        
        self.model.load_state_dict(torch.load('best_stock_model.pth'))
        return self.model, self.history
    
    def evaluate(self, X_test, y_test, stats):
        X_te = torch.FloatTensor(X_test).to(self.device)
        y_te = torch.FloatTensor(y_test).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(X_te).cpu().numpy()
            actual = y_te.cpu().numpy()
        
        # Denormalize
        _, _, y_mean, y_std = stats
        predictions = predictions * y_std + y_mean
        actual = actual * y_std + y_mean
        
        # Metrics
        mse = mean_squared_error(actual, predictions)
        mae = mean_absolute_error(actual, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(actual, predictions)
        
        # Directional accuracy
        actual_dir = np.sign(np.diff(actual.flatten()))
        pred_dir = np.sign(np.diff(predictions.flatten()))
        dir_acc = np.mean(actual_dir == pred_dir)
        
        print(f"\n📊 {ticker} Performance:")
        print(f"   RMSE: ${rmse:.2f}")
        print(f"   MAE: ${mae:.2f}")
        print(f"   R² Score: {r2:.4f}")
        print(f"   Directional Accuracy: {dir_acc:.2%}")
        
        return {
            'predictions': predictions,
            'actual': actual,
            'metrics': {'mse': mse, 'mae': mae, 'rmse': rmse, 'r2': r2, 'dir_acc': dir_acc}
        }
```

## ৪. ভিজুয়ালাইজেশন
```python
def plot_results(history, results, ticker):
    """ফলাফল ভিজুয়ালাইজেশন"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Loss
    axes[0,0].plot(history['train_loss'], label='Train Loss', alpha=0.7)
    axes[0,0].plot(history['val_loss'], label='Val Loss', alpha=0.7)
    axes[0,0].set_xlabel('Epoch')
    axes[0,0].set_ylabel('Loss')
    axes[0,0].set_title(f'{ticker} Training History')
    axes[0,0].legend()
    axes[0,0].grid(True)
    
    # Predictions vs Actual
    axes[0,1].plot(results['actual'][:100], label='Actual', alpha=0.8)
    axes[0,1].plot(results['predictions'][:100], label='Predicted', alpha=0.8)
    axes[0,1].set_title(f'{ticker} Price Prediction (100 days)')
    axes[0,1].legend()
    axes[0,1].grid(True)
    
    # Scatter
    axes[1,0].scatter(results['actual'], results['predictions'], alpha=0.5, s=10)
    min_val = min(results['actual'].min(), results['predictions'].min())
    max_val = max(results['actual'].max(), results['predictions'].max())
    axes[1,0].plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect')
    axes[1,0].set_xlabel('Actual Price ($)')
    axes[1,0].set_ylabel('Predicted Price ($)')
    axes[1,0].set_title(f'R² = {results["metrics"]["r2"]:.3f}')
    axes[1,0].legend()
    axes[1,0].grid(True)
    
    # Residuals
    residuals = results['actual'] - results['predictions']
    axes[1,1].hist(residuals, bins=50, alpha=0.7, edgecolor='black')
    axes[1,1].axvline(x=0, color='r', linestyle='--')
    axes[1,1].set_xlabel('Prediction Error ($)')
    axes[1,1].set_ylabel('Frequency')
    axes[1,1].set_title(f'Error Distribution (MAE=${results["metrics"]["mae"]:.2f})')
    axes[1,1].grid(True)
    
    plt.tight_layout()
    plt.show()
```

## ৫. প্রধান ফাংশন
```python
def main(ticker="AAPL"):
    """মেইন এক্সিকিউশন ফাংশন"""
    print(f"🚀 {ticker} Stock Price Prediction with ANN\n")
    print("=" * 50)
    
    # ডেটা প্রসেসিং
    processor = StockDataProcessor(ticker)
    processor.download_data()
    processor.add_technical_indicators()
    train_data, val_data, test_data = processor.prepare_features()
    
    X_train, y_train = train_data
    X_val, y_val = val_data
    X_test, y_test = test_data
    
    # মডেল
    model = StockPriceANN(
        input_size=X_train.shape[1],
        hidden_sizes=[128, 64, 32],
        dropout=0.2
    )
    print(f"\nModel parameters: {sum(p.numel() for p in model.parameters())}")
    
    # ট্রেনিং
    trainer = ModelTrainer(model)
    model, history = trainer.train(
        X_train, y_train, X_val, y_val,
        epochs=200, lr=0.001
    )
    
    # ইভালুয়েশন
    results = trainer.evaluate(X_test, y_test, processor.stats)
    
    # প্লট
    plot_results(history, results, ticker)
    
    return model, results

# রান করুন:
# model, results = main("AAPL")
# model, results = main("MSFT")
# model, results = main("GOOGL")

print("প্রজেক্ট প্রস্তুত! main('TICKER') কল করে রান করুন")
```

## চ্যালেঞ্জ
```python
challenges = [
    "🏆 **চ্যালেঞ্জ ১**: বিভিন্ন টিকার ট্রাই করুন (AAPL, MSFT, GOOGL, TSLA)",
    "🏆 **চ্যালেঞ্জ ২**: হাইপারপ্যারামিটার টিউন করুন (layers, neurons, dropout)",
    "🏆 **চ্যালেঞ্জ ৩**: LSTM মডেলের সাথে ANN-এর তুলনা করুন",
    "🏆 **চ্যালেঞ্জ ৪**: ক্লাসিফিকেশন ভার্সন তৈরি করুন (আপ/ডাউন)",
    "🏆 **চ্যালেঞ্জ ৫**: পোর্টফোলিও সিমুলেশন করুন প্রেডিকশনের ভিত্তিতে"
]

for c in challenges:
    print(c)
```

## সারসংক্ষেপ
- সম্পূর্ণ এন্ড-টু-এন্ড স্টক প্রাইস প্রেডিকশন প্রজেক্ট
- টেকনিক্যাল ইন্ডিকেটর + ANN = প্রেডিকশন
- ট্রেনিং, ভ্যালিডেশন, টেস্টিং পাইপলাইন
- RMSE, MAE, R², Directional Accuracy মেট্রিক্স
- রিয়েল মার্কেট ডেটা দিয়ে টেস্টিং