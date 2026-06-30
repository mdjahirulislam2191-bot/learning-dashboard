# Day 41: মডেল ডিপ্লয়মেন্ট
## Model Deployment

### ডিপ্লয়মেন্ট কি?
মডেল ডিপ্লয়মেন্ট হল ট্রেইনড মেশিন লার্নিং মডেলকে প্রোডাকশন পরিবেশে স্থাপন করার প্রক্রিয়া, যাতে এটি রিয়েল-টাইমে প্রেডিকশন দিতে পারে।

### ডিপ্লয়মেন্ট অপশন

#### 1. Flask API (সবচেয়ে সহজ)
```python
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# মডেল লোড
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### 2. FastAPI (আধুনিক ও দ্রুত)
```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('model.pkl')

class InputData(BaseModel):
    features: list[float]

@app.post('/predict')
def predict(data: InputData):
    X = np.array(data.features).reshape(1, -1)
    pred = model.predict(X)
    return {'prediction': pred.tolist()}
```

#### 3. Streamlit (UI সহ)
```python
import streamlit as st
import joblib
import numpy as np

model = joblib.load('model.pkl')

st.title('ML Model Predictor')
st.write('ফিচার ভ্যালু ইনপুট করুন')

features = []
for i in range(4):
    val = st.number_input(f'Feature {i+1}', value=0.0)
    features.append(val)

if st.button('Predict'):
    pred = model.predict([features])
    st.success(f'Prediction: {pred[0]}')
```

### ডিপ্লয়মেন্ট বেস্ট প্র্যাকটিস
1. **ভার্সনিং**: মডেল ভার্সন ট্র্যাক রাখুন
2. **লগিং**: সব রিকোয়েস্ট ও রেসপন্স লগ করুন
3. **মনিটরিং**: মডেল পারফরমেন্স মনিটর করুন
4. **স্কেলিং**: লোড অনুযায়ী স্কেল করুন
5. **সিকিউরিটি**: API প্রোটেক্ট করুন

### সম্পূর্ণ Flask ডিপ্লয়মেন্ট উদাহরণ
```python
# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# লগিং সেটআপ
logging.basicConfig(filename='api.log', level=logging.INFO)

app = Flask(__name__)
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # ফিচার প্রসেসিং
        df = pd.DataFrame([data])
        df_scaled = scaler.transform(df)
        
        # প্রেডিকশন
        pred = model.predict(df_scaled)
        proba = model.predict_proba(df_scaled)
        
        # লগিং
        logging.info(f'{datetime.now()}: {data} -> {pred}')
        
        return jsonify({
            'prediction': int(pred[0]),
            'probability': proba[0].tolist(),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```

### ডিপ্লয়মেন্ট চেকলিস্ট
- [ ] মডেল ট্রেইন ও সেভ করা
- [ ] API তৈরি করা
- [ ] লোকালি টেস্ট করা
- [ ] ডকার ইমেজ বানানো
- [ ] ক্লাউডে ডিপ্লয় করা
- [ ] মনিটরিং সেটআপ করা
- [ ] ডকুমেন্টেশন তৈরি করা