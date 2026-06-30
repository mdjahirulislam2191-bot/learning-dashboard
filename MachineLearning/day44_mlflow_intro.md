# Day 44: MLflow ইন্ট্রো
## MLflow Introduction

### MLflow কি?
MLflow একটি ওপেন-সোর্স প্ল্যাটফর্ম যা ML লাইফসাইকেল ম্যানেজ করে — এক্সপেরিমেন্ট ট্র্যাকিং, মডেল রেজিস্ট্রি, ডিপ্লয়মেন্ট।

### MLflow কম্পোনেন্ট
- **MLflow Tracking**: এক্সপেরিমেন্ট, প্যারামিটার, মেট্রিক্স লগ
- **MLflow Projects**: রিপ্রোডিউসিবল ML কোড
- **MLflow Models**: মডেল প্যাকেজিং এবং ডিপ্লয়মেন্ট
- **MLflow Model Registry**: মডেল ভার্সন ম্যানেজমেন্ট

### ফাইন্যান্স উদাহরণ: MLflow Tracking
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# MLflow ইনস্টল চেক
try:
    import mlflow
    import mlflow.sklearn
    print("✅ MLflow imported successfully")
    MLFLOW_AVAILABLE = True
except ImportError:
    print("MLflow not installed. Installing...")
    import subprocess
    subprocess.run(['pip', 'install', 'mlflow'], capture_output=True)
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True

# ফাইন্যান্স ডেটা
np.random.seed(42)
n = 1000
X = np.random.randn(n, 20)
true_coef = np.concatenate([np.random.randn(10) * 2, np.zeros(10)])
y = X @ true_coef + np.random.randn(n) * 0.5

feature_names = [f'factor_{i}' for i in range(20)]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 1. MLflow Tracking বেসিক
```python
# ============================================
# MLflow Tracking সেটআপ
# ============================================
print("\n" + "=" * 60)
print("📊 MLFLOW TRACKING")
print("=" * 60)

# এক্সপেরিমেন্ট সেট
mlflow.set_experiment("Stock Return Prediction")

with mlflow.start_run(run_name="RandomForest_Baseline"):
    # প্যারামিটার লগ
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("test_size", 0.2)
    
    # মডেল ট্রেইন
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    # প্রেডিক্ট
    y_pred = rf.predict(X_test)
    
    # মেট্রিক্স লগ
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2_score", r2)
    mlflow.log_metric("cv_score", cross_val_score(rf, X_train, y_train, cv=5).mean())
    
    # মডেল + আর্টিফ্যাক্ট সেভ
    mlflow.sklearn.log_model(rf, "random_forest_model")
    
    # Feature importance লগ (আর্টিফ্যাক্ট হিসেবে)
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf.feature_importances_
    })
    importance.to_csv("feature_importance.csv", index=False)
    mlflow.log_artifact("feature_importance.csv")
    
    print(f"✅ Run completed: RMSE={rmse:.4f}, R²={r2:.4f}")
    print(f"   Run ID: {mlflow.active_run().info.run_id}")
```

### 2. মাল্টিপল রান তুলনা
```python
# ============================================
# মাল্টিপল মডেল তুলনা
# ============================================
print("\n" + "=" * 60)
print("📊 MULTIPLE MODEL COMPARISON")
print("=" * 60)

models_to_try = [
    ("Ridge", Ridge(alpha=1.0)),
    ("Lasso", Lasso(alpha=0.1)),
    ("RandomForest_50", RandomForestRegressor(n_estimators=50, random_state=42)),
    ("RandomForest_100", RandomForestRegressor(n_estimators=100, random_state=42)),
    ("GradientBoosting_50", GradientBoostingRegressor(n_estimators=50, random_state=42)),
    ("GradientBoosting_100", GradientBoostingRegressor(n_estimators=100, random_state=42))
]

for name, model in models_to_try:
    with mlflow.start_run(run_name=name):
        # প্যারামিটার
        mlflow.log_param("model_name", name)
        mlflow.log_param("model_type", type(model).__name__)
        
        if hasattr(model, 'get_params'):
            params = model.get_params()
            for k, v in params.items():
                mlflow.log_param(k, v)
        
        # ট্রেইন
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # মেট্রিক্স
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        cv = cross_val_score(model, X_train, y_train, cv=5).mean()
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("cv_mean", cv)
        
        # মডেল সেভ
        mlflow.sklearn.log_model(model, name)
        
        print(f"✅ {name}: RMSE={rmse:.4f}, R²={r2:.4f}, CV={cv:.4f}")

print("\n📊 To compare runs, run: mlflow ui")
print("   Then open http://localhost:5000 in browser")
```

### 3. MLflow UI এ্যাক্সেস
```python
# ============================================
# MLflow UI এবং কুয়েরি
# ============================================
print("\n" + "=" * 60)
print("🔍 MLFLOW UI & QUERY")
print("=" * 60)

# MLflow UI চালু করার কমান্ড
print("""
📌 Run MLflow UI:
mlflow ui --host 0.0.0.0 --port 5000

📌 Open browser:
http://localhost:5000

📌 Features:
- Compare runs side by side
- Filter by metrics/parameters
- Download artifacts
- View run history
- Compare model performance
""")

# প্রোগ্রামেটিক্যালি রান কুয়েরি
experiment = mlflow.get_experiment_by_name("Stock Return Prediction")
if experiment:
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    print(f"\n📊 Experiment runs ({len(runs)} total):")
    if not runs.empty:
        display_cols = ['run_id', 'metrics.rmse', 'metrics.r2_score', 'params.model_name']
        display_cols = [c for c in display_cols if c in runs.columns]
        print(runs[display_cols].to_string())
```

### 4. MLflow Model Registry
```python
# ============================================
# MLflow মডেল রেজিস্ট্রি
# ============================================
print("\n" + "=" * 60)
print("📦 MLFLOW MODEL REGISTRY")
print("=" * 60)

# বেস্ট মডেল রেজিস্টার
with mlflow.start_run(run_name="Best_Model_Registration"):
    best_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    best_model.fit(X_train, y_train)
    
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    mlflow.log_metric("rmse", rmse)
    mlflow.log_param("model_type", "GradientBoosting")
    
    # মডেল রেজিস্টার (Model Registry এ)
    mlflow.sklearn.log_model(
        best_model,
        "gradient_boosting_model",
        registered_model_name="Stock_Return_Predictor"
    )
    
    print(f"✅ Model registered: Stock_Return_Predictor")
    print(f"   RMSE: {rmse:.4f}")

# রেজিস্টার থেকে মডেল লোড
print("\n📋 To load from Model Registry:")
print("""
import mlflow.pyfunc

# লোড বেস্ট মডেল
model = mlflow.pyfunc.load_model(
    "models:/Stock_Return_Predictor/1"  # version 1
)

# প্রেডিক্ট
predictions = model.predict(X_test)
""")
```

### 5. MLflow Projects
```python
# ============================================
# MLflow Projects
# ============================================
print("\n" + "=" * 60)
print("📁 MLFLOW PROJECTS")
print("=" * 60)

mlflow_project = '''
# MLproject file
name: Stock Prediction

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      n_estimators: {type: int, default: 100}
      max_depth: {type: int, default: 10}
      learning_rate: {type: float, default: 0.1}
    command: "python train.py --n_estimators {n_estimators} --max_depth {max_depth} --learning_rate {learning_rate}"

  evaluate:
    parameters:
      model_uri: {type: string}
    command: "python evaluate.py --model_uri {model_uri}"
'''

print(mlflow_project)

print("""
📌 Run MLflow Project:
mlflow run . -P n_estimators=200 -P max_depth=15

📌 Benefits:
- Reproducible runs
- Parameter tracking
- Environment management
- Shareable projects
""")
```

### MLflow Best Practices
```python
print("\n" + "=" * 60)
print("✅ MLFLOW BEST PRACTICES")
print("=" * 60)

print("""
1️⃣ Experiment Organization
   - One experiment per project
   - Descriptive run names
   - Log all relevant parameters
   - Log multiple metrics

2️⃣ Artifact Management
   - Save model files
   - Save plots (feature importance, learning curves)
   - Save predictions for analysis
   - Save preprocessing pipeline

3️⃣ Model Registry
   - Register production-ready models
   - Use version tags
   - Promote models through stages:
     Staging → Production → Archived
   - Document model changes

4️⃣ Team Collaboration
   - Shared MLflow server
   - Standard experiment naming
   - Use tags for searchability
   - Review runs before registering

5️⃣ Production
   - Deploy from Model Registry
   - Use model versioning
   - Monitor model performance
   - Automate with CI/CD

⚡ Integration:
MLflow + scikit-learn = 🔥
MLflow + TensorFlow/PyTorch = 🔥
MLflow + Docker + Kubernetes = Production ML!
""")
```

### সারসংক্ষেপ
আজ আমরা MLflow শিখলাম:
- **Tracking**: এক্সপেরিমেন্ট, প্যারামিটার, মেট্রিক্স লগ
- **UI**: ওয়েব ইন্টারফেস দিয়ে রান তুলনা
- **Model Registry**: মডেল ভার্সন ম্যানেজমেন্ট
- **Projects**: রিপ্রোডিউসিবল ML পাইপলাইন
- **Best Practices**: প্রোডাকশন-রেডি ML ওয়ার্কফ্লো

### অনুশীলনী
1. আপনার ML প্রজেক্টে MLflow Tracking ইমপ্লিমেন্ট করুন
2. সার্ভার মোডে MLflow UI চালু করুন (mlflow server)
3. Model Registry ব্যবহার করে মডেল প্রমোট করুন (Staging → Production)
4. MLflow Projects ফরম্যাটে আপনার পাইপলাইন তৈরি করুন