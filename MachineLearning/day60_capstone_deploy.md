# Day 60: ক্যাপস্টোন প্রোজেক্ট — মডেল ডিপ্লয়মেন্ট
## Capstone Project: Model Deployment

### প্রোডাকশনে মডেল ডিপ্লয়মেন্ট
আজ আমরা আমাদের সেরা মডেলটি প্রোডাকশন পরিবেশে ডিপ্লয় করব — একটি ফুল-স্ট্যাক ওয়েব অ্যাপ্লিকেশন।

```python
import numpy as np
import pandas as pd
import joblib
import json
import os
from datetime import datetime
```

### ১. মডেল ও প্রিপ্রসেসর লোড

```python
# প্রয়োজনীয় ফাইল লোড
model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_engineer = joblib.load('feature_engineer.pkl')
report = joblib.load('evaluation_report.pkl')

print(f"মডেল: {report['best_model']}")
print(f"টেস্ট R²: {report['test_r2']:.4f}")
print(f"টেস্ট RMSE: {report['test_rmse']:.2f}")

# মডেল ইনফো
def get_model_info(model):
    """মডেল সম্পর্কে তথ্য"""
    info = {
        'model_type': type(model).__name__,
        'parameters': model.get_params(),
        'feature_importances': None,
        'performance': report
    }
    
    # ফিচার ইম্পরটেন্স (যদি থাকে)
    if hasattr(model, 'feature_importances_'):
        info['feature_importances'] = model.feature_importances_.tolist()
    elif hasattr(model, 'coef_'):
        info['feature_importances'] = model.coef_.tolist()
    
    return info

model_info = get_model_info(model)
print("\nমডেল ইনফো:")
print(json.dumps(model_info, indent=2, default=str))
```

### ২. প্রেডিকশন API (Flask)

```python
# app.py — সম্পূর্ণ Flask API
flask_app_code = '''
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime
import logging

# লগিং কনফিগার
logging.basicConfig(
    filename='predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

app = Flask(__name__)

# মডেল লোড
model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_engineer = joblib.load('feature_engineer.pkl')

# মডেল মেটাডাটা
with open('model_metadata.json', 'r') as f:
    model_metadata = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', metadata=model_metadata)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # JSON ডেটা পার্স
        data = request.get_json()
        
        # প্রয়োজনীয় ফিচার চেক
        required_features = [
            'area', 'bedrooms', 'bathrooms', 'age',
            'location_score', 'has_garage', 'has_garden',
            'floor', 'total_floors', 'distance_center'
        ]
        
        missing_features = [f for f in required_features if f not in data]
        if missing_features:
            return jsonify({
                'error': f'মিসিং ফিচার: {missing_features}',
                'status': 'failed'
            }), 400
        
        # ডেটা প্রিপ্রসেস
        input_df = pd.DataFrame([data])
        
        # ফিচার ইঞ্জিনিয়ারিং
        input_processed = feature_engineer.transform(input_df)
        
        # প্রেডিকশন
        prediction = model.predict(input_processed)[0]
        
        # কনফিডেন্স ইন্টারভাল (অ্যাপ্রোক্সিমেট)
        confidence_interval = (
            float(prediction - 2 * 20000),  # RMSE approximation
            float(prediction + 2 * 20000)
        )
        
        # লগিং
        logging.info(f'ইনপুট: {data} -> প্রেডিকশন: {prediction:.2f}')
        
        return jsonify({
            'predicted_price': float(prediction),
            'predicted_price_formatted': f"৳{prediction:,.2f}",
            'confidence_interval': {
                'lower': confidence_interval[0],
                'upper': confidence_interval[1],
                'lower_formatted': f"৳{confidence_interval[0]:,.2f}",
                'upper_formatted': f"৳{confidence_interval[1]:,.2f}"
            },
            'model_used': model_metadata['model_type'],
            'model_accuracy': f"{model_metadata['test_r2']*100:.1f}%",
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """হেলথ চেক এন্ডপয়েন্ট"""
    return jsonify({
        'status': 'healthy',
        'model': model_metadata['model_type'],
        'accuracy': f"{model_metadata['test_r2']*100:.1f}%",
        'last_trained': model_metadata.get('training_date', 'N/A'),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """একাধিক প্রেডিকশন একসাথে"""
    try:
        data = request.get_json()
        inputs = data['inputs']
        
        predictions = []
        for item in inputs:
            input_df = pd.DataFrame([item])
            input_processed = feature_engineer.transform(input_df)
            pred = model.predict(input_processed)[0]
            predictions.append(float(pred))
        
        logging.info(f'ব্যাচ প্রেডিকশন: {len(inputs)} টি অনুরোধ')
        
        return jsonify({
            'predictions': predictions,
            'predictions_formatted': [f"৳{p:,.2f}" for p in predictions],
            'count': len(predictions),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
'''

# API কোড সেভ
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(flask_app_code)
print("✅ Flask API তৈরি করা হয়েছে: app.py")
```

### ৩. HTML টেমপ্লেট

```python
html_template = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>হাউস প্রাইস প্রেডিক্টর</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 700px;
            width: 100%;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        input, select {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn-predict {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 20px;
        }
        .btn-predict:hover {
            transform: translateY(-2px);
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            display: none;
        }
        .result.show { display: block; }
        .result h2 {
            color: #333;
            margin-bottom: 15px;
            text-align: center;
        }
        .price {
            font-size: 36px;
            font-weight: bold;
            color: #28a745;
            text-align: center;
            margin: 15px 0;
        }
        .confidence {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
        .model-info {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
        .error {
            color: #dc3545;
            text-align: center;
            margin-top: 15px;
            display: none;
        }
        .error.show { display: block; }
        .loading {
            text-align: center;
            display: none;
            margin-top: 20px;
        }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 হাউস প্রাইস প্রেডিক্টর</h1>
        <p class="subtitle">আপনার বাড়ির মূল্য নির্ধারণ করুন মেশিন লার্নিং দিয়ে</p>
        
        <form id="predictionForm">
            <div class="form-row">
                <div class="form-group">
                    <label>বাড়ির আয়তন (sqft)</label>
                    <input type="number" id="area" required step="any" value="1500">
                </div>
                <div class="form-group">
                    <label>বেডরুম</label>
                    <input type="number" id="bedrooms" required min="1" max="10" value="3">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>বাথরুম</label>
                    <input type="number" id="bathrooms" required min="1" max="5" value="2">
                </div>
                <div class="form-group">
                    <label>বাড়ির বয়স (বছর)</label>
                    <input type="number" id="age" required min="0" value="10">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>লোকেশন স্কোর (1-10)</label>
                    <input type="number" id="location_score" required min="1" max="10" step="0.1" value="7">
                </div>
                <div class="form-group">
                    <label>সেন্টার থেকে দূরত্ব (km)</label>
                    <input type="number" id="distance_center" required step="0.1" value="5">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>গ্যারেজ</label>
                    <select id="has_garage">
                        <option value="1">হ্যাঁ</option>
                        <option value="0" selected>না</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>বাগান</label>
                    <select id="has_garden">
                        <option value="1">হ্যাঁ</option>
                        <option value="0" selected>না</option>
                    </select>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>ফ্লোর নম্বর</label>
                    <input type="number" id="floor" required min="1" value="2">
                </div>
                <div class="form-group">
                    <label>মোট ফ্লোর</label>
                    <input type="number" id="total_floors" required min="1" value="5">
                </div>
            </div>
            
            <button type="submit" class="btn-predict">🔮 মূল্য নির্ধারণ করুন</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top:10px;color:#666;">প্রেডিকশন করা হচ্ছে...</p>
        </div>
        
        <div class="result" id="result">
            <h2>📊 প্রেডিক্টেড মূল্য</h2>
            <div class="price" id="price">৳0</div>
            <div class="confidence" id="confidence">কনফিডেন্স ইন্টারভাল: ৳0 - ৳0</div>
            <div class="model-info" id="modelInfo"></div>
        </div>
        
        <div class="error" id="error"></div>
    </div>
    
    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            
            loading.classList.add('show');
            result.classList.remove('show');
            error.classList.remove('show');
            
            const data = {
                area: parseFloat(document.getElementById('area').value),
                bedrooms: parseInt(document.getElementById('bedrooms').value),
                bathrooms: parseInt(document.getElementById('bathrooms').value),
                age: parseInt(document.getElementById('age').value),
                location_score: parseFloat(document.getElementById('location_score').value),
                has_garage: parseInt(document.getElementById('has_garage').value),
                has_garden: parseInt(document.getElementById('has_garden').value),
                floor: parseInt(document.getElementById('floor').value),
                total_floors: parseInt(document.getElementById('total_floors').value),
                distance_center: parseFloat(document.getElementById('distance_center').value)
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const resultData = await response.json();
                
                if (resultData.status === 'success') {
                    document.getElementById('price').textContent = resultData.predicted_price_formatted;
                    document.getElementById('confidence').textContent = 
                        `কনফিডেন্স ইন্টারভাল: ${resultData.confidence_interval.lower_formatted} - ${resultData.confidence_interval.upper_formatted}`;
                    document.getElementById('modelInfo').textContent = 
                        `মডেল: ${resultData.model_used} | অ্যাকুরেসি: ${resultData.model_accuracy}`;
                    result.classList.add('show');
                } else {
                    document.getElementById('error').textContent = 'এরর: ' + (resultData.error || 'অজানা ত্রুটি');
                    error.classList.add('show');
                }
            } catch (err) {
                document.getElementById('error').textContent = 'এরর: ' + err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
            }
        });
    </script>
</body>
</html>
'''

# টেমপ্লেট ফোল্ডার তৈরি
os.makedirs('templates', exist_ok=True)

# HTML টেমপ্লেট সেভ
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("✅ HTML টেমপ্লেট তৈরি করা হয়েছে: templates/index.html")
```

### ৪. মডেল মেটাডাটা

```python
# মডেল মেটাডাটা JSON
model_metadata = {
    'model_type': type(model).__name__,
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'test_r2': float(report['test_r2']),
    'test_rmse': float(report['test_rmse']),
    'test_mae': float(report['test_mae']),
    'features': [
        'area', 'bedrooms', 'bathrooms', 'age',
        'location_score', 'has_garage', 'has_garden',
        'floor', 'total_floors', 'distance_center'
    ],
    'description': 'হাউস প্রাইস প্রেডিকশন মডেল — ক্যাপস্টোন প্রোজেক্ট',
    'version': '1.0.0',
    'author': 'Machine Learning Engineer',
    'notes': 'এই মডেলটি বিভিন্ন ফিচারের উপর ভিত্তি করে বাড়ির মূল্য প্রেডিক্ট করে'
}

# মেটাডাটা সেভ
with open('model_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(model_metadata, f, indent=2)

print("✅ মডেল মেটাডাটা তৈরি করা হয়েছে: model_metadata.json")
print(json.dumps(model_metadata, indent=2))
```

### ৫. Docker কনফিগারেশন

```python
# Dockerfile
dockerfile = '''
FROM python:3.9-slim

WORKDIR /app

# প্রয়োজনীয় প্যাকেজ ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# অ্যাপ কোড কপি
COPY . .

# পোর্ট এক্সপোজ
EXPOSE 5000

# অ্যাপ রান
CMD ["python", "app.py"]
'''

# requirements.txt
requirements = '''
flask==2.3.3
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
joblib==1.3.2
gunicorn==21.2.0
'''

# docker-compose.yml
docker_compose = '''
version: '3.8'

services:
  house-price-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./predictions.log:/app/predictions.log
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
'''

# ফাইল সেভ
with open('Dockerfile', 'w') as f:
    f.write(dockerfile)
with open('requirements.txt', 'w') as f:
    f.write(requirements)
with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose)

print("✅ Docker কনফিগারেশন তৈরি করা হয়েছে")
print("   - Dockerfile")
print("   - requirements.txt")
print("   - docker-compose.yml")
```

### ৬. লোকাল টেস্টিং

```python
def test_prediction_api():
    """API লোকালি টেস্ট করা"""
    
    test_input = {
        'area': 1800,
        'bedrooms': 3,
        'bathrooms': 2,
        'age': 5,
        'location_score': 8.5,
        'has_garage': 1,
        'has_garden': 0,
        'floor': 3,
        'total_floors': 8,
        'distance_center': 2.5
    }
    
    # সরাসরি মডেল দিয়ে টেস্ট
    input_df = pd.DataFrame([test_input])
    input_processed = feature_engineer.transform(input_df)
    prediction = model.predict(input_processed)[0]
    
    print("\n=== API টেস্ট ===")
    print(f"ইনপুট:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    print(f"\nপ্রেডিক্টেড মূল্য: ৳{prediction:,.2f}")
    print(f"R² অ্যাকুরেসি: {report['test_r2']*100:.1f}%")
    
    return prediction

test_prediction = test_prediction_api()
```

### ৭. API রেসপন্স টেস্ট

```python
print("\n" + "="*70)
print("📋 API রেসপন্স ফরম্যাট")
print("="*70)

# সিমুলেটেড API রেসপন্স
response = {
    'predicted_price': 325000.00,
    'predicted_price_formatted': '৳325,000.00',
    'confidence_interval': {
        'lower': 285000.00,
        'upper': 365000.00,
        'lower_formatted': '৳285,000.00',
        'upper_formatted': '৳365,000.00'
    },
    'model_used': type(model).__name__,
    'model_accuracy': f"{report['test_r2']*100:.1f}%",
    'timestamp': datetime.now().isoformat(),
    'status': 'success'
}

print(json.dumps(response, indent=2))
```

### ৮. ক্যাপস্টোন প্রোজেক্ট সারাংশ

```python
print("\n" + "="*70)
print("🎉 ক্যাপস্টোন প্রোজেক্ট — সমাপ্তি!")
print("="*70)

print("""
📁 প্রোজেক্ট স্ট্রাকচার:
├── data/
│   ├── X_train.pkl          # ট্রেইন ফিচার
│   ├── X_test.pkl           # টেস্ট ফিচার
│   ├── y_train.pkl          # ট্রেইন টার্গেট
│   └── y_test.pkl           # টেস্ট টার্গেট
├── features/
│   ├── X_train_final.pkl    # ফাইনাল ফিচার
│   ├── X_test_final.pkl     # ফাইনাল ফিচার
│   └── feature_engineer.pkl # ফিচার ইঞ্জিনিয়ার
├── models/
│   ├── best_model.pkl       # সেরা মডেল
│   ├── all_models.pkl       # সব মডেল
│   └── scaler.pkl           # স্কেলার
├── evaluation/
│   ├── evaluation_report.pkl
│   ├── model_metrics.pkl
│   └── feature_scores.pkl
├── deployment/
│   ├── app.py               # Flask API
│   ├── templates/
│   │   └── index.html       # ওয়েব UI
│   ├── model_metadata.json  # মডেল তথ্য
│   ├── Dockerfile           # ডকার কনফিগ
│   ├── docker-compose.yml   # ডকার কম্পোজ
│   └── requirements.txt     # পাইথন ডিপেন্ডেন্সি
└── visuals/
    ├── capstone_*.png        # সব ভিজুয়ালাইজেশন
""")

print("""
✅ কী শিখলাম:
1. ডেটা প্রিপারেশন ও ক্লিনিং
2. ফিচার ইঞ্জিনিয়ারিং (পলিনোমিয়াল, বিনিং, রেশিও)
3. একাধিক মডেল বিল্ডিং (LR, Ridge, Lasso, RF, GBR, XGBoost)
4. হাইপারপ্যারামিটার টিউনিং
5. মডেল ইভালুয়েশন (মেট্রিক্স, রেসিডুয়াল, লার্নিং কার্ভ)
6. মডেল ডিপ্লয়মেন্ট (Flask API + HTML UI + Docker)
""")

print("""
🚀 ডিপ্লয়মেন্ট কমান্ড:
# লোকালি রান
python app.py

# ডকার দিয়ে রান
docker-compose up --build

# API টেস্ট
curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"area":1500,"bedrooms":3,"bathrooms":2,"age":10,"location_score":7,"has_garage":1,"has_garden":0,"floor":2,"total_floors":5,"distance_center":5}'

# হেলথ চেক
curl http://localhost:5000/health
""")
```

### ফাইনাল চেকলিস্ট
- ✅ ডেটা প্রিপারেশন (Day 56)
- ✅ ফিচার ইঞ্জিনিয়ারিং (Day 57)
- ✅ মডেল বিল্ডিং (Day 58)
- ✅ মডেল ইভালুয়েশন (Day 59)
- ✅ মডেল ডিপ্লয়মেন্ট (Day 60)
- ✅ **ক্যাপস্টোন প্রোজেক্ট সম্পন্ন!** 🎉