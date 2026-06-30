# Day 10: ট্রেনিং লুপ ও ইভালুয়েশন 📊

## সম্পূর্ণ ট্রেনিং পাইপলাইন
```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import yfinance as yf
from datetime import datetime

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
```

## ১. মডেল ডিফাইনিশন
```python
class StockPredictor(nn.Module):
    """স্টক প্রাইস প্রেডিক্টর"""
    def __init__(self, n_features, hidden_dims=[64, 32, 16]):
        super().__init__()
        
        layers = []
        prev_dim = n_features
        
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = h_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)
```

## ২. ডেটা প্রিপ্রসেসিং
```python
def prepare_financial_data(ticker, seq_length=10):
    """ফিন্যান্সিয়াল ডেটা প্রস্তুত"""
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    
    # ফিচার ইঞ্জিনিয়ারিং
    df = data.copy()
    df['Returns'] = df['Close'].pct_change()
    df['SMA_5'] = df['Close'].rolling(5).mean()
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['Volatility'] = df['Returns'].rolling(10).std()
    df['Volume_MA'] = df['Volume'].rolling(10).mean()
    df['High_Low'] = (df['High'] - df['Low']) / df['Close']
    
    # টার্গেট: পরবর্তী দিনের প্রাইস
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()
    
    feature_cols = ['Returns', 'SMA_5', 'SMA_20', 'Volatility', 'Volume_MA', 'High_Low']
    X = df[feature_cols].values
    y = df['Target'].values.reshape(-1, 1)
    
    # নরমালাইজেশন
    X_mean, X_std = X.mean(axis=0), X.std(axis=0)
    y_mean, y_std = y.mean(), y.std()
    
    X = (X - X_mean) / X_std
    y = (y - y_mean) / y_std
    
    return X, y, (X_mean, X_std, y_mean, y_std), feature_cols
```

## ৩. ট্রেনিং ফাংশন
```python
def train_model(model, X_train, y_train, X_val, y_val, epochs=200, lr=0.001):
    """সম্পূর্ণ ট্রেনিং পাইপলাইন"""
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=10, verbose=True
    )
    
    X_tr_t = torch.FloatTensor(X_train).to(device)
    y_tr_t = torch.FloatTensor(y_train).to(device)
    X_val_t = torch.FloatTensor(X_val).to(device)
    y_val_t = torch.FloatTensor(y_val).to(device)
    
    history = {'train_loss': [], 'val_loss': []}
    best_val_loss = float('inf')
    patience_counter = 0
    
    for epoch in range(epochs):
        # ট্রেনিং
        model.train()
        optimizer.zero_grad()
        
        train_pred = model(X_tr_t)
        train_loss = criterion(train_pred, y_tr_t)
        train_loss.backward()
        optimizer.step()
        
        # ভ্যালিডেশন
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val_t)
            val_loss = criterion(val_pred, y_val_t)
        
        history['train_loss'].append(train_loss.item())
        history['val_loss'].append(val_loss.item())
        
        # Scheduler & Early Stopping
        scheduler.step(val_loss)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'best_model.pth')
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= 30:
                print(f"Early stopping at epoch {epoch}")
                break
        
        if (epoch + 1) % 25 == 0:
            print(f"Epoch {epoch+1}: Train Loss={train_loss.item():.4f}, Val Loss={val_loss.item():.4f}")
    
    model.load_state_dict(torch.load('best_model.pth'))
    return model, history
```

## ৪. ইভালুয়েশন ফাংশন
```python
def evaluate_model(model, X_test, y_test, stats, model_name="Model"):
    """মডেল ইভালুয়েশন"""
    model.eval()
    
    X_te_t = torch.FloatTensor(X_test).to(device)
    y_te_t = torch.FloatTensor(y_test).to(device)
    
    with torch.no_grad():
        predictions = model(X_te_t).cpu().numpy()
        actual = y_te_t.cpu().numpy()
    
    # ডিনরমালাইজ
    _, _, y_mean, y_std = stats
    predictions_actual = predictions * y_std + y_mean
    actual_actual = actual * y_std + y_mean
    
    # মেট্রিক্স
    mse = mean_squared_error(actual_actual, predictions_actual)
    mae = mean_absolute_error(actual_actual, predictions_actual)
    rmse = np.sqrt(mse)
    r2 = r2_score(actual_actual, predictions_actual)
    
    # MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((actual_actual - predictions_actual) / actual_actual)) * 100
    
    print(f"\n=== {model_name} Evaluation ===")
    print(f"MSE: ${mse:.4f}")
    print(f"RMSE: ${rmse:.4f}")
    print(f"MAE: ${mae:.4f}")
    print(f"R² Score: {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")
    
    # ডিরেকশনাল অ্যাকুরেসি
    direction_actual = np.sign(np.diff(actual_actual.flatten()))
    direction_pred = np.sign(np.diff(predictions_actual.flatten()))
    dir_acc = np.mean(direction_actual == direction_pred)
    print(f"Directional Accuracy: {dir_acc:.2%}")
    
    return {
        'mse': mse, 'rmse': rmse, 'mae': mae,
        'r2': r2, 'mape': mape, 'dir_acc': dir_acc,
        'predictions': predictions_actual,
        'actual': actual_actual
    }
```

## ৫. ফুল পাইপলাইন এক্সিকিউশন
```python
def full_pipeline(ticker="AAPL"):
    """সম্পূর্ণ ট্রেনিং পাইপলাইন"""
    
    # ডেটা
    X, y, stats, features = prepare_financial_data(ticker)
    print(f"Features: {features}")
    print(f"Data shape: {X.shape}")
    
    # স্প্লিট
    n = len(X)
    train_end = int(0.7 * n)
    val_end = int(0.85 * n)
    
    X_train, y_train = X[:train_end], y[:train_end]
    X_val, y_val = X[train_end:val_end], y[train_end:val_end]
    X_test, y_test = X[val_end:], y[val_end:]
    
    print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # মডেল
    model = StockPredictor(n_features=len(features)).to(device)
    print(f"\nModel:\n{model}")
    
    # ট্রেনিং
    model, history = train_model(
        model, X_train, y_train, X_val, y_val,
        epochs=150, lr=0.001
    )
    
    # ইভালুয়েশন
    results = evaluate_model(model, X_test, y_test, stats, f"{ticker} Predictor")
    
    # প্লট
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # লস
    axes[0].plot(history['train_loss'], label='Train')
    axes[0].plot(history['val_loss'], label='Validation')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training History')
    axes[0].legend()
    axes[0].grid(True)
    
    # প্রেডিকশন
    axes[1].plot(results['actual'][:100], label='Actual', alpha=0.7)
    axes[1].plot(results['predictions'][:100], label='Predicted', alpha=0.7)
    axes[1].set_title(f'{ticker} Price Prediction (first 100 days)')
    axes[1].legend()
    axes[1].grid(True)
    
    # স্ক্যাটার
    axes[2].scatter(results['actual'], results['predictions'], alpha=0.5)
    axes[2].plot([results['actual'].min(), results['actual'].max()],
                 [results['actual'].min(), results['actual'].max()],
                 'r--', label='Perfect')
    axes[2].set_xlabel('Actual Price')
    axes[2].set_ylabel('Predicted Price')
    axes[2].set_title(f'R² = {results["r2"]:.3f}')
    axes[2].legend()
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return model, results

# রান করতে:
# model, results = full_pipeline("AAPL")
```

## মডেল সেভ ও লোড
```python
# সেভ
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'stats': stats,
}, 'stock_model.pth')

# লোড
checkpoint = torch.load('stock_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])
stats = checkpoint['stats']
```

## সারসংক্ষেপ
- সম্পূর্ণ পাইপলাইন: Data → Train → Validate → Test
- Metrics: MSE, RMSE, MAE, R², MAPE, Directional Accuracy
- Early Stopping + Learning Rate Scheduling
- মডেল সেভ/লোড করে প্রোডাকশনে ব্যবহার
- ফিন্যান্সে Directional Accuracy গুরুত্বপূর্ণ (শুধু প্রাইস নয়, দিক)