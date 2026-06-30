# Day 50: এথিক্স ইন ML
## Ethics in Machine Learning

### এথিক্স কেন গুরুত্বপূর্ণ?
মেশিন লার্নিং মডেলের সিদ্ধান্ত মানুষের জীবনে প্রভাব ফেলে। এথিক্যাল এমএল নিশ্চিত করে যে এই প্রভাব ইতিবাচক এবং ন্যায্য।

### এথিক্যাল ইস্যুসমূহ

#### 1. প্রাইভেসি ও ডেটা প্রোটেকশন
```python
import hashlib
import numpy as np
import pandas as pd

class PrivacyPreservingProcessor:
    """প্রাইভেসি-প্রিজারভিং ডেটা প্রসেসর"""
    
    def anonymize(self, df, sensitive_columns):
        """স্পর্শকাতর কলাম এনোনিমাইজ করা"""
        df_copy = df.copy()
        for col in sensitive_columns:
            # হ্যাশিং
            df_copy[col] = df_copy[col].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
            )
        return df_copy
    
    def add_noise(self, df, columns, epsilon=0.1):
        """ডিফারেনশিয়াল প্রাইভেসির জন্য নয়েজ যোগ করা"""
        df_copy = df.copy()
        for col in columns:
            noise = np.random.laplace(0, 1/epsilon, len(df))
            df_copy[col] = df_copy[col] + noise
        return df_copy
    
    def k_anonymize(self, df, quasi_identifiers, k=5):
        """k-anozimity নিশ্চিত করা"""
        # কোয়াসি-আইডেন্টিফায়ার জেনারেলাইজ
        df_copy = df.copy()
        for col in quasi_identifiers:
            if df[col].dtype in ['int64', 'float64']:
                # বিনিং
                bins = len(df) // k
                df_copy[col] = pd.qcut(df[col], q=bins, 
                                       labels=False, duplicates='drop')
        return df_copy

# ব্যবহার
processor = PrivacyPreservingProcessor()
data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 35, 45],
    'salary': [50000, 60000, 70000],
    'diagnosis': [0, 1, 0]
})

anonymized = processor.anonymize(data, ['name'])
print(anonymized)
```

#### 2. ট্রান্সপারেন্সি ও এক্সপ্লেইনেবিলিটি
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.inspection import permutation_importance

class TransparentModel:
    """স্বচ্ছ মডেল ক্লাস"""
    
    def __init__(self):
        self.model = DecisionTreeClassifier(max_depth=3)
        self.feature_importance_ = None
    
    def fit(self, X, y, feature_names):
        self.model.fit(X, y)
        self.feature_names = feature_names
        
        # ফিচার ইম্পরটেন্স
        result = permutation_importance(
            self.model, X, y, n_repeats=10
        )
        self.feature_importance_ = dict(
            zip(feature_names, result.importances_mean)
        )
        
        return self
    
    def explain_prediction(self, x, sample_idx=0):
        """একটি নির্দিষ্ট প্রেডিকশন ব্যাখ্যা করা"""
        tree = self.model.tree_
        feature = tree.feature[0]
        threshold = tree.threshold[0]
        
        explanation = {
            'prediction': self.model.predict([x])[0],
            'probability': self.model.predict_proba([x])[0],
            'decision_path': []
        }
        
        # ডিসিশন পাথ ট্র্যাকিং
        node = 0
        while feature != -2:  # -2 means leaf
            direction = 'left' if x[feature] <= threshold else 'right'
            explanation['decision_path'].append({
                'feature': self.feature_names[feature],
                'value': x[feature],
                'threshold': threshold,
                'direction': direction
            })
            node = tree.children_left[node] if direction == 'left' \
                   else tree.children_right[node]
            feature = tree.feature[node]
            threshold = tree.threshold[node]
        
        return explanation
```

#### 3. অ্যাকাউন্টেবিলিটি
```python
from datetime import datetime
import json

class ModelAccountabilityTracker:
    """মডেল অ্যাকাউন্টেবিলিটি ট্র্যাকার"""
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.predictions_log = []
        self.audit_trail = []
    
    def log_prediction(self, input_data, prediction, user_id):
        """প্রতিটি প্রেডিকশন লগ করা"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'input': input_data,
            'prediction': prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
            'user': user_id
        }
        self.predictions_log.append(log_entry)
        
        # অডিট ট্রেইল
        self.audit_trail.append({
            'action': 'prediction',
            'details': f'User {user_id} made a prediction',
            'timestamp': datetime.now().isoformat()
        })
    
    def get_prediction_history(self, user_id=None, 
                               start_date=None, end_date=None):
        """প্রেডিকশন হিস্টোরি দেখা"""
        history = self.predictions_log
        
        if user_id:
            history = [h for h in history if h['user'] == user_id]
        if start_date:
            history = [h for h in history 
                      if h['timestamp'] >= start_date]
        if end_date:
            history = [h for h in history 
                      if h['timestamp'] <= end_date]
        
        return history
    
    def generate_audit_report(self):
        """অডিট রিপোর্ট জেনারেট করা"""
        return {
            'model': self.model_name,
            'total_predictions': len(self.predictions_log),
            'unique_users': len(set(h['user'] for h in self.predictions_log)),
            'date_range': {
                'start': self.predictions_log[0]['timestamp'] if self.predictions_log else None,
                'end': self.predictions_log[-1]['timestamp'] if self.predictions_log else None
            },
            'audit_actions': len(self.audit_trail)
        }
    
    def save_logs(self, filename='model_logs.json'):
        """লগ ফাইল সেভ করা"""
        with open(filename, 'w') as f:
            json.dump({
                'predictions': self.predictions_log,
                'audit': self.audit_trail
            }, f, indent=2)
```

### এথিক্যাল ফ্রেমওয়ার্ক

#### এফিকিউ (Fairness, Accountability, Transparency, Privacy)
```python
class EthicalMLFramework:
    """এথিক্যাল এমএল ফ্রেমওয়ার্ক"""
    
    def __init__(self):
        self.checks = {
            'fairness': [],
            'accountability': [],
            'transparency': [],
            'privacy': []
        }
    
    def add_fairness_check(self, check_name, check_func):
        self.checks['fairness'].append({
            'name': check_name,
            'function': check_func,
            'passed': None
        })
    
    def add_privacy_check(self, check_name, check_func):
        self.checks['privacy'].append({
            'name': check_name,
            'function': check_func,
            'passed': None
        })
    
    def run_all_checks(self, model, X, y, sensitive_attrs=None):
        """সব এথিক্যাল চেক রান করা"""
        results = {}
        
        for category, checks in self.checks.items():
            category_results = []
            for check in checks:
                try:
                    result = check['function'](model, X, y, sensitive_attrs)
                    check['passed'] = result['passed']
                    category_results.append({
                        'check': check['name'],
                        'passed': result['passed'],
                        'details': result.get('details', '')
                    })
                except Exception as e:
                    category_results.append({
                        'check': check['name'],
                        'passed': False,
                        'details': f'Error: {str(e)}'
                    })
            results[category] = category_results
        
        return results
```

### এথিক্যাল ডিসিশন মেকিং গাইড
1. **স্বচ্ছতা**: মডেল কিভাবে সিদ্ধান্ত নেয় তা ব্যাখ্যা করা
2. **ন্যায্যতা**: সব গ্রুপের জন্য সমান আচরণ
3. **গোপনীয়তা**: ব্যক্তিগত ডেটা সুরক্ষা
4. **দায়িত্ব**: মডেলের ফলাফলের জন্য জবাবদিহি
5. **নিরাপত্তা**: মডেল অ্যাটাক থেকে রক্ষা
6. **নির্ভরযোগ্যতা**: মডেল কনসিস্টেন্ট ফলাফল দিচ্ছে কিনা

### বেস্ট প্র্যাকটিস
- প্রোজেক্টের শুরুতে এথিক্যাল ইমপ্যাক্ট অ্যাসেসমেন্ট করুন
- ডেটা কালেকশনে ইনফর্মড কনসেন্ট নিন
- মডেল ডকুমেন্টেশন তৈরি করুন (Model Cards)
- নিয়মিত এথিক্যাল অডিট করুন
- ডাইভার্স টিম নিয়ে কাজ করুন
- ইউজার ফিডব্যাক নিন এবং তা বিবেচনা করুন