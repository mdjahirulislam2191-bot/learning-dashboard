# Day 45: মডেল মনিটরিং
## Model Monitoring

### মডেল মনিটরিং কি?
মডেল মনিটরিং হল প্রোডাকশনে ML মডেলের পারফরম্যান্স ট্র্যাক করার প্রক্রিয়া। মডেল সময়ের সাথে সাথে পারফরম্যান্স হারাতে পারে (মডেল ড্রিফট), তাই নিয়মিত মনিটরিং প্রয়োজন।

### ফাইন্যান্সে মডেল মনিটরিং কেন গুরুত্বপূর্ণ?
- **মডেল ড্রিফট**: মার্কেট কন্ডিশন পরিবর্তন হলে মডেল কম কার্যকর হয়
- **কমপ্লায়েন্স**: রেগুলেটরি রিপোর্টিং প্রয়োজন
- **ফাইন্যান্সিয়াল ইমপ্যাক্ট**: খারাপ মডেল বড় আর্থিক ক্ষতি করতে পারে
- **ফ্রড ডিটেকশন**: ফ্রড প্যাটার্ন পরিবর্তন হলে মডেল আপডেট প্রয়োজন

### ফাইন্যান্স উদাহরণ: মডেল মনিটরিং সিস্টেম
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# স্টার্টিং মডেল (প্রোডাকশনে থাকা মডেল)
np.random.seed(42)
n_initial = 1000

X_init = pd.DataFrame({
    'amount': np.random.exponential(200, n_initial),
    'frequency': np.random.poisson(5, n_initial),
    'hour': np.random.randint(0, 24, n_initial),
    'distance': np.random.exponential(20, n_initial),
    'is_weekend': np.random.binomial(1, 0.3, n_initial)
})

# 3% ফ্রড রেট
y_init = np.random.binomial(1, 0.03, n_initial)

X_train_init, X_test_init, y_train_init, y_test_init = train_test_split(
    X_init, y_init, test_size=0.2, random_state=42
)

# প্রোডাকশন মডেল
production_model = RandomForestClassifier(n_estimators=100, random_state=42)
production_model.fit(X_train_init, y_train_init)

# বেসলাইন পারফরম্যান্স
y_pred_init = production_model.predict(X_test_init)
baseline_metrics = {
    'accuracy': accuracy_score(y_test_init, y_pred_init),
    'precision': precision_score(y_test_init, y_pred_init),
    'recall': recall_score(y_test_init, y_pred_init),
    'f1': f1_score(y_test_init, y_pred_init)
}

print("📊 Production Model Baseline Performance:")
for metric, value in baseline_metrics.items():
    print(f"  {metric}: {value:.4f}")
```

### 1. ড্রিফট সিমুলেশন (মার্কেট চেঞ্জ)
```python
# ============================================
# ড্রিফট সিমুলেশন
# ============================================
print("\n" + "=" * 60)
print("🔄 MODEL DRIFT SIMULATION")
print("=" * 60)

# সময়ের সাথে ডেটা পরিবর্তন (ড্রিফট)
time_periods = 12  # মাস
months = []
metrics_history = []

for month in range(time_periods):
    # ড্রিফট: ফ্রড প্যাটার্ন পরিবর্তন হচ্ছে
    drift_factor = month / time_periods
    
    # ফ্রড রেট বাড়ছে
    fraud_rate = 0.03 + drift_factor * 0.07  # 3% → 10%
    
    # লেনদেনের প্যাটার্ন পরিবর্তন
    n_monthly = 500
    X_month = pd.DataFrame({
        'amount': np.random.exponential(200 * (1 + drift_factor), n_monthly),
        'frequency': np.random.poisson(5 + drift_factor * 5, n_monthly),
        'hour': np.random.randint(0, 24, n_monthly),
        'distance': np.random.exponential(20 * (1 + drift_factor * 2), n_monthly),
        'is_weekend': np.random.binomial(1, 0.3, n_monthly)
    })
    y_month = np.random.binomial(1, fraud_rate, n_monthly)
    
    # প্রোডাকশন মডেল দিয়ে প্রেডিক্ট
    y_pred_month = production_model.predict(X_month)
    
    # মেট্রিক্স গণনা
    metrics = {
        'month': month + 1,
        'fraud_rate': fraud_rate,
        'accuracy': accuracy_score(y_month, y_pred_month),
        'precision': precision_score(y_month, y_pred_month, zero_division=0),
        'recall': recall_score(y_month, y_pred_month, zero_division=0),
        'f1': f1_score(y_month, y_pred_month, zero_division=0),
        'data_drift_score': np.random.uniform(0.1, 0.3 + drift_factor * 0.5)
    }
    
    months.append(month + 1)
    metrics_history.append(metrics)
    
    print(f"Month {month+1:2d}: Fraud={fraud_rate:.2%}, Acc={metrics['accuracy']:.4f}, "
          f"Prec={metrics['precision']:.4f}, Rec={metrics['recall']:.4f}, "
          f"F1={metrics['f1']:.4f}")

metrics_df = pd.DataFrame(metrics_history)
```

### 2. মেট্রিক্স ভিজুয়ালাইজেশন
```python
# ============================================
# মেট্রিক্স ট্রেন্ড ভিজুয়ালাইজেশন
# ============================================
print("\n" + "=" * 60)
print("📈 METRICS TREND VISUALIZATION")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Accuracy
axes[0, 0].plot(metrics_df['month'], metrics_df['accuracy'], 'b-o', linewidth=2)
axes[0, 0].axhline(y=baseline_metrics['accuracy'], color='g', linestyle='--', 
                   label=f"Baseline: {baseline_metrics['accuracy']:.4f}")
axes[0, 0].axhline(y=baseline_metrics['accuracy'] * 0.9, color='r', linestyle=':', 
                   label='Alert Threshold (90%)')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_title('Model Accuracy Over Time')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Precision & Recall
axes[0, 1].plot(metrics_df['month'], metrics_df['precision'], 'r-s', linewidth=2, label='Precision')
axes[0, 1].plot(metrics_df['month'], metrics_df['recall'], 'g-^', linewidth=2, label='Recall')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Score')
axes[0, 1].set_title('Precision & Recall Over Time')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# F1 Score
axes[1, 0].plot(metrics_df['month'], metrics_df['f1'], 'm-o', linewidth=2)
axes[1, 0].axhline(y=baseline_metrics['f1'] * 0.9, color='r', linestyle=':', 
                   label='Alert Threshold (90%)')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('F1 Score')
axes[1, 0].set_title('F1 Score Over Time')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Fraud Rate
axes[1, 1].plot(metrics_df['month'], metrics_df['fraud_rate'], 'c-D', linewidth=2)
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Fraud Rate')
axes[1, 1].set_title('Actual Fraud Rate Over Time')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 3. অ্যালার্ম সিস্টেম
```python
# ============================================
# অ্যালার্ম সিস্টেম
# ============================================
print("\n" + "=" * 60)
print("🔔 MONITORING ALERT SYSTEM")
print("=" * 60)

class ModelMonitor:
    def __init__(self, baseline_metrics, thresholds=None):
        self.baseline = baseline_metrics
        self.thresholds = thresholds or {
            'accuracy': 0.90,  # baseline এর 90%
            'precision': 0.85,
            'recall': 0.85,
            'f1': 0.85,
            'data_drift': 0.3
        }
        self.alerts = []
    
    def check_metrics(self, current_metrics, month):
        """মেট্রিক্স চেক এবং অ্যালার্ট জেনারেট"""
        alerts_triggered = []
        
        for metric in ['accuracy', 'precision', 'recall', 'f1']:
            if metric in current_metrics and metric in self.baseline:
                baseline_val = self.baseline[metric]
                current_val = current_metrics[metric]
                threshold = baseline_val * self.thresholds.get(metric, 0.9)
                
                if current_val < threshold:
                    degradation = (1 - current_val / baseline_val) * 100
                    alert = {
                        'month': month,
                        'metric': metric,
                        'baseline': baseline_val,
                        'current': current_val,
                        'threshold': threshold,
                        'degradation_pct': degradation,
                        'severity': 'HIGH' if degradation > 20 else 'MEDIUM' if degradation > 10 else 'LOW'
                    }
                    alerts_triggered.append(alert)
                    self.alerts.append(alert)
        
        return alerts_triggered
    
    def get_alert_summary(self):
        """সতর্কতা সারাংশ"""
        if not self.alerts:
            return "✅ No alerts triggered - Model is healthy!"
        
        df = pd.DataFrame(self.alerts)
        summary = df.groupby('severity').size().to_dict()
        
        text = "🔔 Alert Summary:\n"
        for severity, count in sorted(summary.items()):
            text += f"  {severity}: {count} alerts\n"
        text += f"  Total: {len(self.alerts)} alerts"
        
        return text

# মনিটর তৈরি
monitor = ModelMonitor(baseline_metrics)

print("\n🔍 Checking each month...")
for row in metrics_history:
    alerts = monitor.check_metrics(row, row['month'])
    if alerts:
        for alert in alerts:
            print(f"⚠️  Month {alert['month']}: {alert['metric']} degraded by "
                  f"{alert['degradation_pct']:.1f}% [{alert['severity']}]")

print(f"\n{monitor.get_alert_summary()}")
```

### 4. ডেটা ড্রিফট ডিটেকশন
```python
# ============================================
# ডেটা ড্রিফট ডিটেকশন
# ============================================
print("\n" + "=" * 60)
print("📊 DATA DRIFT DETECTION")
print("=" * 60)

from scipy.stats import ks_2samp, wasserstein_distance

def detect_data_drift(reference_data, current_data, threshold=0.05):
    """ডেটা ড্রিফট ডিটেক্ট করুন"""
    drift_results = {}
    for col in reference_data.columns:
        if reference_data[col].dtype in ['float64', 'int64']:
            # KS Test
            ks_stat, ks_pval = ks_2samp(reference_data[col], current_data[col])
            
            drift_results[col] = {
                'ks_statistic': ks_stat,
                'ks_p_value': ks_pval,
                'drift_detected': ks_pval < threshold,
                'wasserstein_dist': wasserstein_distance(reference_data[col], current_data[col]),
                'ref_mean': reference_data[col].mean(),
                'cur_mean': current_data[col].mean(),
                'ref_std': reference_data[col].std(),
                'cur_std': current_data[col].std()
            }
    
    return drift_results

# রেফারেন্স ডেটা (initial training data)
reference = X_init

# বর্তমান ডেটা (ড্রিফটেড)
current = pd.DataFrame({
    'amount': np.random.exponential(300, 500),  # ড্রিফটেড
    'frequency': np.random.poisson(8, 500),
    'hour': np.random.randint(0, 24, 500),
    'distance': np.random.exponential(50, 500),
    'is_weekend': np.random.binomial(1, 0.4, 500)
})

print("🔍 Data Drift Analysis:")
drift_results = detect_data_drift(reference, current)

for col, results in drift_results.items():
    drift_status = "🔴 DRIFT" if results['drift_detected'] else "🟢 OK"
    print(f"\n  Feature: {col}")
    print(f"    {drift_status} | KS p-value: {results['ks_p_value']:.6f}")
    print(f"    Reference: μ={results['ref_mean']:.2f}, σ={results['ref_std']:.2f}")
    print(f"    Current:   μ={results['cur_mean']:.2f}, σ={results['cur_std']:.2f}")
```

### 5. রিট্রেইনিং ডিসিশন
```python
# ============================================
# রিট্রেইনিং সিদ্ধান্ত
# ============================================
print("\n" + "=" * 60)
print("🔄 RETRAINING DECISION SYSTEM")
print("=" * 60)

def should_retrain(metrics_history, alert_count, drift_count, 
                   metric_threshold=0.1, alert_threshold=3):
    """মডেল রিট্রেইন করা উচিত কিনা তা নির্ধারণ"""
    reasons = []
    
    # মেট্রিক্স ডিগ্রেডেশন চেক
    first_metrics = metrics_history[0]
    last_metrics = metrics_history[-1]
    
    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        degradation = (1 - last_metrics.get(metric, 0) / (first_metrics.get(metric, 1) + 1e-8))
        if degradation > metric_threshold:
            reasons.append(f"{metric} degraded by {degradation:.2%}")
    
    # অ্যালার্ট কাউন্ট চেক
    if alert_count >= alert_threshold:
        reasons.append(f"{alert_count} alerts triggered")
    
    # ড্রিফট চেক
    if drift_count > 0:
        reasons.append(f"{drift_count} features drifted")
    
    if reasons:
        print("🔴 RETRAINING RECOMMENDED:")
        for reason in reasons:
            print(f"  - {reason}")
        return True
    else:
        print("🟢 Model is healthy. No retraining needed.")
        return False

# রিট্রেইন সিদ্ধান্ত নিন
total_alerts = len(monitor.alerts)
total_drifted = sum(1 for r in drift_results.values() if r['drift_detected'])

print(f"\n📊 Assessment:")
print(f"  Total alerts: {total_alerts}")
print(f"  Drifted features: {total_drifted}/{len(drift_results)}")

should_retrain(metrics_history, total_alerts, total_drifted)
```

### মডেল মনিটরিং বেস্ট প্র্যাকটিস
```python
print("\n" + "=" * 60)
print("✅ MODEL MONITORING BEST PRACTICES")
print("=" * 60)

print("""
1️⃣ What to Monitor:
   - Model metrics (accuracy, precision, recall, F1, AUC)
   - Data drift (feature distributions)
   - Concept drift (target relationships)
   - Prediction distribution
   - System metrics (latency, throughput, memory)

2️⃣ Alert Thresholds:
   - Metric degradation > 10% → WARNING
   - Metric degradation > 20% → CRITICAL
   - Data drift p-value < 0.05 → INVESTIGATE
   - Accuracy < 90% baseline → ALERT

3️⃣ Monitoring Tools:
   - Prometheus + Grafana (metrics, alerts)
   - ELK Stack (logs, predictions)
   - MLflow (model metrics)
   - Evidently AI (data drift)
   - WhyLabs (full ML monitoring)

4️⃣ Retraining Strategy:
   - Time-based (weekly/monthly retraining)
   - Performance-based (alert triggered)
   - Rolling retraining (incremental)
   - Shadow deployment (A/B test new model)

5️⃣ Governance:
   - Log all predictions
   - Store model versions
   - Track data lineage
   - Document model changes
   - Audit trails for compliance
""")
```

### সারসংক্ষেপ
আজ আমরা মডেল মনিটরিং শিখলাম:
- **মেট্রিক্স ট্র্যাকিং**: সময়ের সাথে পারফরম্যান্স মনিটর
- **ড্রিফট ডিটেকশন**: KS Test দিয়ে ডেটা ড্রিফট
- **অ্যালার্ম সিস্টেম**: থ্রেশহোল্ড-বেসড অ্যালার্ট
- **রিট্রেইনিং**: কখন মডেল রিট্রেইন করতে হবে
- **ভিজুয়ালাইজেশন**: মেট্রিক্স ট্রেন্ড ভিজুয়ালাইজেশন

### অনুশীলনী
1. রিয়েল-টাইম মনিটরিং ড্যাশবোর্ড তৈরি করুন (Flask + Chart.js)
2. Evidently AI লাইব্রেরি ব্যবহার করে ডেটা ড্রিফট ডিটেক্ট করুন
3. অটোমেটিক রিট্রেইনিং পাইপলাইন তৈরি করুন
4. প্রোমেথিউস + গ্রাফানা দিয়ে ML মেট্রিক্স মনিটর করুন