# Day 34: LSTM বেসিক
## LSTM (Long Short-Term Memory) Basics

### LSTM কি?
LSTM হল এক ধরনের Recurrent Neural Network (RNN) যা দীর্ঘমেয়াদী ডিপেন্ডেন্সি মনে রাখতে পারে। এটি টাইম সিরিজ এবং সিকোয়েন্স ডেটার জন্য বিশেষভাবে কার্যকর।

### LSTM এর মূল উপাদান
- **Forget Gate**: কোন তথ্য বাতিল করতে হবে তা নির্ধারণ করে
- **Input Gate**: কোন নতুন তথ্য সংরক্ষণ করতে হবে তা নির্ধারণ করে
- **Cell State**: দীর্ঘমেয়াদী মেমোরি
- **Hidden State**: শর্ট-টার্ম আউটপুট
- **Output Gate**: কোন তথ্য আউটপুট হিসেবে দিতে হবে তা নির্ধারণ করে

### ফাইন্যান্স উদাহরণ: LSTM দিয়ে স্টক প্রাইস ফোরকাস্টিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# TensorFlow/Keras
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    print("✅ TensorFlow/Keras imported successfully")
except ImportError:
    print("Installing TensorFlow...")
    import subprocess
    subprocess.run(['pip', 'install', 'tensorflow'])
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping

# স্টক প্রাইস ডেটা তৈরি
np.random.seed(42)
n = 1000
dates = pd.date_range('2021-01-01', periods=n, freq='D')

# সিন্থেটিক প্রাইস
t = np.arange(n)
price = 100 + np.cumsum(np.random.randn(n) * 0.5) + 0.05 * t + 5 * np.sin(2 * np.pi * t / 30)
price = price - price.min() + 50  # পজিটিভ রাখতে

df = pd.DataFrame({'date': dates, 'price': price})
print(f"Stock price data: {df.shape}")
print(f"Price range: {df['price'].min():.2f} - {df['price'].max():.2f}")

plt.figure(figsize=(15, 5))
plt.plot(df['date'], df['price'], linewidth=0.8)
plt.title('Stock Price Time Series for LSTM')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.grid(True, alpha=0.3)
plt.show()
```

### 1. ডেটা প্রিপ্রসেসিং (সিকোয়েন্স তৈরি)
```python
# স্কেলিং
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df[['price']])

print(f"Scaled data range: {scaled_data.min():.4f} - {scaled_data.max():.4f}")

# সিকোয়েন্স ডেটাসেট তৈরি
def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

SEQ_LENGTH = 60
X, y = create_sequences(scaled_data, SEQ_LENGTH)

# Reshape for LSTM: (samples, time_steps, features)
X = X.reshape(X.shape[0], X.shape[1], 1)

print(f"X shape: {X.shape} (samples, timesteps, features)")
print(f"y shape: {y.shape}")

# ট্রেন/টেস্ট স্প্লিট
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Train: X={X_train.shape}, y={y_train.shape}")
print(f"Test: X={X_test.shape}, y={y_test.shape}")
```

### 2. LSTM মডেল বিল্ডিং
```python
# LSTM মডেল আর্কিটেকচার
model = Sequential([
    LSTM(units=50, return_sequences=True, input_shape=(SEQ_LENGTH, 1)),
    Dropout(0.2),
    LSTM(units=50, return_sequences=True),
    Dropout(0.2),
    LSTM(units=50, return_sequences=False),
    Dropout(0.2),
    Dense(units=25),
    Dense(units=1)
])

# মডেল কম্পাইল
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

print("📊 LSTM Model Architecture:")
model.summary()
```

### 3. মডেল ট্রেইনিং
```python
# আর্লি স্টপিং
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# মডেল ট্রেইন
history = model.fit(
    X_train, y_train,
    batch_size=32,
    epochs=100,
    validation_data=(X_test, y_test),
    callbacks=[early_stop],
    verbose=1
)

print(f"\n✅ Training completed in {len(history.history['loss'])} epochs")
```

### 4. ট্রেইনিং ভিজুয়ালাইজেশন
```python
# Loss এবং MAE প্লট
fig, axes = plt.subplots(1, 2, figsize=(15, 4))

axes[0].plot(history.history['loss'], label='Train Loss', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss (MSE)')
axes[0].set_title('Model Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(history.history['mae'], label='Train MAE', linewidth=2)
axes[1].plot(history.history['val_mae'], label='Validation MAE', linewidth=2)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('MAE')
axes[1].set_title('Model MAE')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 5. প্রেডিকশন এবং ইভালুয়েশন
```python
# প্রেডিকশন
y_pred = model.predict(X_test)

# স্কেল ফিরিয়ে আনা
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
y_pred_inv = scaler.inverse_transform(y_pred)

# ইভালুয়েশন
rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
mae = mean_absolute_error(y_test_inv, y_pred_inv)
mape = np.mean(np.abs((y_test_inv - y_pred_inv) / y_test_inv)) * 100

print(f"\n📊 LSTM Forecast Performance:")
print(f"  RMSE: ${rmse:.4f}")
print(f"  MAE:  ${mae:.4f}")
print(f"  MAPE: {mape:.2f}%")

# ভিজুয়ালাইজেশন
plt.figure(figsize=(15, 6))
plt.plot(y_test_inv, label='Actual Price', linewidth=2)
plt.plot(y_pred_inv, label='LSTM Predicted', linewidth=2, linestyle='--')
plt.title('LSTM - Stock Price Prediction')
plt.xlabel('Time Step')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 6. ফিউচার প্রেডিকশন (মাল্টি-স্টেপ)
```python
# মাল্টি-স্টেপ ফোরকাস্টিং
def predict_future(model, last_sequence, scaler, n_steps=30):
    predictions = []
    current_seq = last_sequence.copy()
    
    for _ in range(n_steps):
        # প্রেডিক্ট
        pred = model.predict(current_seq.reshape(1, SEQ_LENGTH, 1), verbose=0)
        predictions.append(pred[0, 0])
        
        # সিকোয়েন্স আপডেট (shift + new prediction)
        current_seq = np.roll(current_seq, -1)
        current_seq[-1] = pred[0, 0]
    
    # ইনভার্স ট্রান্সফর্ম
    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions)

# শেষ সিকোয়েন্স নেওয়া
last_sequence = scaled_data[-SEQ_LENGTH:, 0]
future_pred = predict_future(model, last_sequence, scaler, n_steps=30)

print("\n🔮 Future 30-day predictions:")
for i, pred in enumerate(future_pred):
    print(f"  Day {i+1}: ${pred[0]:.2f}")

# এক্সটেন্ডেড প্লট
full_predictions = np.vstack([
    scaler.inverse_transform(scaled_data),
    future_pred
])

plt.figure(figsize=(15, 5))
plt.plot(full_predictions[:-30], label='Historical', linewidth=1)
plt.plot(range(len(scaled_data)-1, len(full_predictions)), future_pred, 
         label='Future Prediction', linewidth=2, color='red', linestyle='--')
plt.axvline(x=len(scaled_data)-1, color='green', linestyle=':', alpha=0.7, label='Now')
plt.title('LSTM - Historical + Future Forecast')
plt.xlabel('Time Step')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 7. LSTM হাইপারপ্যারামিটার
```python
print("""
🎛️ LSTM Hyperparameters to Tune:

Architecture:
- Number of LSTM layers: 1-3
- Units per layer: 32, 50, 64, 128
- Dropout rate: 0.1-0.5
- Dense layers after LSTM

Training:
- Sequence length: 30, 60, 90
- Batch size: 16, 32, 64
- Learning rate: 0.001, 0.0001
- Optimizer: adam, rmsprop
- Epochs: 50-200
- Early stopping patience: 5-20

Data:
- Scaling: MinMax, Standard
- Features: OHLCV, technical indicators
- Train/test split: 80/20
""")

# LSTM vs অন্যান্য মডেল
print("""
📊 LSTM vs Traditional Models:
🔵 Advantage: Captures long-term dependencies
🔵 Advantage: Handles complex non-linear patterns
🔵 Disadvantage: Needs more data
🔵 Disadvantage: Computationally expensive
🔵 Disadvantage: Less interpretable
""")
```

### সারসংক্ষেপ
আজ আমরা LSTM বেসিক শিখলাম:
- **LSTM আর্কিটেকচার**: Forget Gate, Input Gate, Output Gate, Cell State
- **সিকোয়েন্স ডেটা**: Time steps, Feature dimension
- **মডেল বিল্ডিং**: Keras Sequential API
- **ইভালুয়েশন**: RMSE, MAE, MAPE
- **ফিউচার ফোরকাস্টিং**: Multi-step prediction

### অনুশীলনী
1. LSTM লেয়ারের সংখ্যা এবং ইউনিট পরিবর্তন করে এক্সপেরিমেন্ট করুন
2. বিভিন্ন সিকোয়েন্স লেংথ (30, 60, 90) নিয়ে টেস্ট করুন
3. মাল্টিপল ফিচার (volume, moving average) যোগ করুন
4. Bidirectional LSTM ব্যবহার করে পারফরম্যান্স তুলনা করুন