# Day 42: মডেল সিরিয়ালাইজেশন
## Model Serialization

### মডেল সিরিয়ালাইজেশন কি?
মডেল সিরিয়ালাইজেশন হল ট্রেইনড মডেলকে ডিস্কে সেভ করার প্রক্রিয়া যাতে পরে এটি লোড করে প্রেডিকশনের জন্য ব্যবহার করা যায়।

### কেন সিরিয়ালাইজেশন প্রয়োজন?
- **ডিপ্লয়মেন্ট**: প্রোডাকশনে মডেল স্থাপন
- **কোলাবরেশন**: টিমের সাথে মডেল শেয়ার
- **ভার্শনিং**: মডেল ভার্সন ট্র্যাকিং
- **কস্ট সেভিং**: রিট্রেইনিং এড়ানো

### ফাইন্যান্স উদাহরণ: মডেল সেভ এবং লোড
```python
import numpy as np
import pandas as pd
import pickle
import joblib
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# স্টক প্রেডিকশন মডেল
np.random.seed(42)
n = 500
X = np.random.randn(n, 10)
y = X @ np.array([0.5, -0.3, 0.8, 0.2, 0, 1.2, -0.5, 0.1, 0.3, 0]) + np.random.randn(n) * 0.3

feature_names = [f'feature_{i}' for i in range(10)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# মডেল ট্রেইন
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ইভালুয়েশন
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"📊 Model Performance: RMSE={rmse:.4f}, R²={r2:.4f}")
```

### 1. Pickle সিরিয়ালাইজেশন
```python
# ============================================
# pickle দিয়ে মডেল সেভ
# ============================================
print("\n" + "=" * 50)
print("📦 Pickle Serialization")
print("=" * 50)

# সেভ
with open('stock_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model saved with pickle")

# ফাইল সাইজ
file_size = os.path.getsize('stock_model.pkl')
print(f"📏 File size: {file_size/1024:.2f} KB")

# লোড
with open('stock_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# ভেরিফাই
y_pred_loaded = loaded_model.predict(X_test)
load_rmse = np.sqrt(mean_squared_error(y_test, y_pred_loaded))
print(f"✅ Model loaded successfully")
print(f"📊 Loaded model RMSE: {load_rmse:.4f}")

# সেভ টাইম
import time
start = time.time()
for _ in range(1000):
    pickle.dumps(model)
pickle_time = (time.time() - start) / 1000
print(f"⚡ Serialization time: {pickle_time*1000:.2f} ms per save")
```

### 2. Joblib সিরিয়ালাইজেশন
```python
# ============================================
# joblib দিয়ে মডেল সেভ (NumPy arrays এর জন্য ভাল)
# ============================================
print("\n" + "=" * 50)
print("📦 Joblib Serialization")
print("=" * 50)

# সেভ
joblib.dump(model, 'stock_model.joblib')
print("✅ Model saved with joblib")

# ফাইল সাইজ
file_size_joblib = os.path.getsize('stock_model.joblib')
print(f"📏 File size: {file_size_joblib/1024:.2f} KB")

# কম্প্রেশন সহ
joblib.dump(model, 'stock_model_compressed.joblib', compress=3)
file_size_comp = os.path.getsize('stock_model_compressed.joblib')
print(f"📏 Compressed file size: {file_size_comp/1024:.2f} KB")
print(f"📉 Compression ratio: {file_size_joblib/file_size_comp:.2f}x")

# লোড
loaded_joblib = joblib.load('stock_model.joblib')
print("✅ Model loaded with joblib")

# স্পিড টেস্ট
start = time.time()
for _ in range(1000):
    joblib.dump(model, 'temp.joblib')
joblib_time = (time.time() - start) / 1000
print(f"⚡ Joblib serialization time: {joblib_time*1000:.2f} ms per save")
os.remove('temp.joblib')
```

### 3. মডেল + স্কেলার + মেটাডেটা (কমপ্লিট আর্টিফ্যাক্ট)
```python
# ============================================
# কসম্পলিট মডেল আর্টিফ্যাক্ট
# ============================================
print("\n" + "=" * 50)
print("📦 Complete Model Artifact Package")
print("=" * 50)

# স্কেলার
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# মডেল রিট্রেইন (স্কেলড ডেটায়)
model_scaled = RandomForestRegressor(n_estimators=100, random_state=42)
model_scaled.fit(X_train_scaled, y_train)

# ফুল প্যাকেজ
artifact = {
    'model': model_scaled,
    'scaler': scaler,
    'feature_names': feature_names,
    'metadata': {
        'model_type': 'RandomForestRegressor',
        'n_features': 10,
        'n_estimators': 100,
        'rmse': float(rmse),
        'r2_score': float(r2),
        'training_date': datetime.now().isoformat(),
        'python_version': '3.11',
        'sklearn_version': '1.3.0'
    },
    'training_params': {
        'test_size': 0.2,
        'random_state': 42,
        'n_samples': n
    },
    'feature_importance': dict(zip(feature_names, model.feature_importances_))
}

# সেভ
with open('full_stock_artifact.pkl', 'wb') as f:
    pickle.dump(artifact, f)

print(f"✅ Complete artifact saved")
print(f"📏 File size: {os.path.getsize('full_stock_artifact.pkl')/1024:.2f} KB")
print(f"\n📋 Metadata:")
for key, val in artifact['metadata'].items():
    print(f"   {key}: {val}")
```

### 4. JSON মডেল রিপ্রেজেন্টেশন
```python
# ============================================
# JSON এ মডেল কনফিগারেশন
# ============================================
print("\n" + "=" * 50)
print("📦 JSON Model Configuration")
print("=" * 50)

# JSON কনফিগ
model_config = {
    "model_name": "stock_predictor_v1",
    "model_type": "RandomForestRegressor",
    "hyperparameters": {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "random_state": 42
    },
    "features": {
        "names": feature_names,
        "n_features": len(feature_names),
        "feature_importance": {
            str(k): float(v) for k, v in zip(feature_names, model.feature_importances_)
        }
    },
    "performance": {
        "rmse": float(rmse),
        "r2_score": float(r2),
        "test_size": 0.2,
        "n_train_samples": len(X_train),
        "n_test_samples": len(X_test)
    },
    "deployment": {
        "input_format": "JSON array of 10 features",
        "output_format": "float (predicted value)",
        "api_endpoint": "/predict",
        "expected_latency_ms": 50
    },
    "version": "1.0.0",
    "created_at": datetime.now().isoformat()
}

with open('model_config.json', 'w') as f:
    json.dump(model_config, f, indent=2)

print("✅ Model config saved as JSON")
print(json.dumps(model_config, indent=2)[:500] + "...")
```

### 5. মডেল ভার্সনিং
```python
# ============================================
# মডেল ভার্সনিং সিস্টেম
# ============================================
print("\n" + "=" * 50)
print("📦 Model Versioning System")
print("=" * 50)

# মডেল ভার্সন ডিরেক্টরি
os.makedirs('model_registry', exist_ok=True)

def save_model_version(model, scaler, version, metadata):
    """মডেল ভার্সন সেভ ফাংশন"""
    artifact = {
        'model': model,
        'scaler': scaler,
        'metadata': metadata
    }
    
    filename = f'model_registry/model_v{version}.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(artifact, f)
    
    print(f"✅ Model version {version} saved")
    return filename

def load_model_version(version):
    """মডেল ভার্সন লোড ফাংশন"""
    filename = f'model_registry/model_v{version}.pkl'
    with open(filename, 'rb') as f:
        artifact = pickle.load(f)
    print(f"✅ Model version {version} loaded")
    return artifact

# মাল্টিপল ভার্সন সেভ
for v in range(1, 4):
    # বিভিন্ন প্যারামিটার সহ মডেল
    n_est = v * 50
    rf = RandomForestRegressor(n_estimators=n_est, random_state=42)
    rf.fit(X_train, y_train)
    
    save_model_version(rf, None, v, {
        'version': f'v{v}.0',
        'n_estimators': n_est,
        'rmse': float(np.sqrt(mean_squared_error(y_test, rf.predict(X_test)))),
        'date': datetime.now().isoformat()
    })

# ভার্সন তুলনা
print("\n📊 Model Version Comparison:")
for v in range(1, 4):
    art = load_model_version(v)
    print(f"  V{v}: {art['metadata']}")
```

### 6. বড় মডেল হ্যান্ডলিং
```python
# ============================================
# বড় মডেলের জন্য কৌশল
# ============================================
print("\n" + "=" * 50)
print("📦 Large Model Handling")
print("=" * 50)

# 1. মডেল কোয়ান্টাইজেশন
# (শুধুমাত্র ডিপ লার্নিং মডেলের জন্য প্রযোজ্য)
# from tensorflow.keras.models import load_model
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()

print("Large Model Strategies:")
print("""
1️⃣ Compression: joblib.dump(model, 'model.joblib', compress=3)
2️⃣ ONNX Format: Cross-platform, smaller size
3️⃣ TF Lite: For mobile/edge deployment
4️⃣ Model Pruning: Remove unimportant weights
5️⃣ Quantization: Reduce precision (float32 → float16/int8)
6️⃣ Distributed Storage: For models > 100MB
""")

# 2. মেমোরি ম্যাপিং (বড় মডেলের জন্য)
# numpy.memmap ব্যবহার করে বড় অ্যারে হ্যান্ডলিং

# 3. মডেল শার্ডিং
# বড় মডেলকে একাধিক ফাইলে ভাগ করা
print("""
Example: Sharding large models
model_shard_1.pkl, model_shard_2.pkl, ...
""")
```

### সিরিয়ালাইজেশন বেস্ট প্র্যাকটিস
```python
print("""
" + "=" * 60 + "
✅ Serialization Best Practices
" + "=" * 60 + "

📝 Pickle vs Joblib:
- Pickle: Python objects, all types
- Joblib: NumPy arrays, scikit-learn models (faster!)
- Use Joblib for sklearn models

📦 What to Save:
✅ Model parameters (coefficients, weights)
✅ Preprocessing pipeline (scaler, encoder)
✅ Feature names and order
✅ Model metadata (version, date, performance)
✅ Training parameters (for reproducibility)

⚠️ Security:
- Never load pickle files from untrusted sources
- Use JSON for configuration files
- Validate model integrity with checksums
- Sign model artifacts for production

📊 Storage Options:
- Local disk: Development, testing
- S3/GCS/Blob: Cloud storage
- Model Registry: MLflow, DVC, Neptune
- Database: Metadata in DB, model in blobstore
""")
```

### সারসংক্ষেপ
আজ আমরা মডেল সিরিয়ালাইজেশন শিখলাম:
- **Pickle**: স্ট্যান্ডার্ড পাইথন সিরিয়ালাইজেশন
- **Joblib**: NumPy-অপ্টিমাইজড, দ্রুত
- **আর্টিফ্যাক্ট প্যাকেজ**: মডেল + স্কেলার + মেটাডেটা
- **JSON কনফিগ**: হিউম্যান-রিডেবল কনফিগারেশন
- **ভার্সনিং**: মাল্টিপল মডেল ভার্সন ম্যানেজমেন্ট

### অনুশীলনী
1. GB মডেল (1GB+) সিরিয়ালাইজ করার কৌশল ইমপ্লিমেন্ট করুন
2. ONNX ফরম্যাটে মডেল এক্সপোর্ট করুন
3. মডেল চেকসাম এবং ইন্টিগ্রিটি ভেরিফিকেশন যোগ করুন
4. S3/GCS থেকে মডেল লোড করার ফাংশন তৈরি করুন