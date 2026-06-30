# Day 59: ক্যাপস্টোন প্রোজেক্ট — মডেল ইভালুয়েশন
## Capstone Project: Model Evaluation

### ডিটেইলড ইভালুয়েশন
শুধু R² বা RMSE নয় — মডেলের গভীর বিশ্লেষণ এবং বিভিন্ন অ্যাঙ্গেল থেকে মূল্যায়ন।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, median_absolute_error,
    mean_absolute_percentage_error
)
from scipy import stats
import joblib
import warnings
warnings.filterwarnings('ignore')
```

### মডেল ও ডেটা লোড

```python
# সেরা মডেল লোড
best_model = joblib.load('best_model.pkl')
all_models = joblib.load('all_models.pkl')
metrics = joblib.load('model_metrics.pkl')

# ডেটা লোড
X_train = joblib.load('X_train_final.pkl')
X_test = joblib.load('X_test_final.pkl')
y_train = joblib.load('y_train.pkl')
y_test = joblib.load('y_test.pkl')

print(f"মডেল: {metrics[0]['model_name']}")  # সেরা মডেলের নাম
print(f"ট্রেইন শেপ: {X_train.shape}")
print(f"টেস্ট শেপ: {X_test.shape}")

# প্রেডিকশন
y_train_pred = best_model.predict(X_train)
y_test_pred = best_model.predict(X_test)
```

### ১. কম্প্রিহেনসিভ মেট্রিক্স

```python
def comprehensive_evaluation(y_true, y_pred, y_train=None, y_pred_train=None):
    """সম্পূর্ণ ইভালুয়েশন মেট্রিক্স"""
    
    residuals = y_true - y_pred
    
    metrics = {
        # রিগ্রেশন মেট্রিক্স
        'R² (Coefficient of Determination)': r2_score(y_true, y_pred),
        'Adjusted R²': None,  # নিচে ক্যালকুলেটেড
        'RMSE (Root Mean Squared Error)': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MSE (Mean Squared Error)': mean_squared_error(y_true, y_pred),
        'MAE (Mean Absolute Error)': mean_absolute_error(y_true, y_pred),
        'MedAE (Median Absolute Error)': median_absolute_error(y_true, y_pred),
        'MAPE (Mean Absolute Percentage Error)': mean_absolute_percentage_error(y_true, y_pred) * 100,
        'Explained Variance': explained_variance_score(y_true, y_pred),
        
        # রেসিডুয়াল স্ট্যাটিস্টিক্স
        'Mean Residual': np.mean(residuals),
        'Std Residual': np.std(residuals),
        'Skewness of Residuals': stats.skew(residuals),
        'Kurtosis of Residuals': stats.kurtosis(residuals),
    }
    
    # অ্যাডজাস্টেড R²
    if y_train is not None:
        n = len(y_test)
        p = X_test.shape[1]
        r2 = r2_score(y_true, y_pred)
        metrics['Adjusted R²'] = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    
    # ওভারফিটিং মেট্রিক
    if y_train is not None and y_pred_train is not None:
        metrics['Train R²'] = r2_score(y_train, y_pred_train)
        metrics['Overfitting Gap'] = metrics['Train R²'] - metrics['R² (Coefficient of Determination)']
    
    return metrics

eval_metrics = comprehensive_evaluation(y_test, y_test_pred, y_train, y_train_pred)

print("="*60)
print("সম্পূর্ণ মডেল ইভালুয়েশন রিপোর্ট")
print("="*60)
for metric, value in eval_metrics.items():
    if value is not None:
        if 'MAPE' in metric:
            print(f"{metric:45s}: {value:.2f}%")
        else:
            print(f"{metric:45s}: {value:.6f}")
```

### ২. রেসিডুয়াল অ্যানালাইসিস

```python
residuals = y_test - y_test_pred

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# রেসিডুয়াল ডিস্ট্রিবিউশন
axes[0, 0].hist(residuals, bins=40, edgecolor='black', alpha=0.7, density=True)
axes[0, 0].set_xlabel('রেসিডুয়াল')
axes[0, 0].set_ylabel('ডেনসিটি')
axes[0, 0].set_title('রেসিডুয়াল ডিস্ট্রিবিউশন')

# Q-Q প্লট (নর্মালিটি চেক)
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Q-Q প্লট (নর্মালিটি চেক)')

# রেসিডুয়াল vs প্রেডিক্টেড
axes[0, 2].scatter(y_test_pred, residuals, alpha=0.6, s=30)
axes[0, 2].axhline(y=0, color='r', linestyle='--', alpha=0.7)
axes[0, 2].set_xlabel('প্রেডিক্টেড ভ্যালু')
axes[0, 2].set_ylabel('রেসিডুয়াল')
axes[0, 2].set_title('রেসিডুয়াল vs প্রেডিক্টেড')

# অ্যাকচুয়াল vs প্রেডিক্টেড
axes[1, 0].scatter(y_test, y_test_pred, alpha=0.6, s=30)
min_val = min(y_test.min(), y_test_pred.min())
max_val = max(y_test.max(), y_test_pred.max())
axes[1, 0].plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.7)
axes[1, 0].set_xlabel('অ্যাকচুয়াল')
axes[1, 0].set_ylabel('প্রেডিক্টেড')
axes[1, 0].set_title('অ্যাকচুয়াল vs প্রেডিক্টেড')

# রেসিডুয়াল এর হিটম্যাপ (ইনডেক্স অনুযায়ী)
axes[1, 1].scatter(range(len(residuals)), residuals, alpha=0.6, s=20)
axes[1, 1].axhline(y=0, color='r', linestyle='--', alpha=0.7)
axes[1, 1].set_xlabel('ডেটা পয়েন্ট ইনডেক্স')
axes[1, 1].set_ylabel('রেসিডুয়াল')
axes[1, 1].set_title('রেসিডুয়াল vs ইনডেক্স')

# রেসিডুয়াল হিস্টোগ্রাম (কিউমুলেটিভ)
axes[1, 2].hist(residuals, bins=40, cumulative=True, 
                density=True, alpha=0.7, edgecolor='black')
axes[1, 2].set_xlabel('রেসিডুয়াল')
axes[1, 2].set_ylabel('কিউমুলেটিভ প্রোবাবিলিটি')
axes[1, 2].set_title('কিউমুলেটিভ রেসিডুয়াল ডিস্ট্রিবিউশন')

plt.tight_layout()
plt.savefig('capstone_residual_analysis.png', dpi=100)
plt.show()
print("রেসিডুয়াল অ্যানালাইসিস প্লট সেভ করা হয়েছে")
```

### ৩. এরর ডিস্ট্রিবিউশন অ্যানালাইসিস

```python
# পার্সেন্টাইল ভিত্তিক এরর
percentiles = [10, 25, 50, 75, 90, 95, 99]
errors = np.abs(residuals)

print("\n=== পার্সেন্টাইল অনুযায়ী এরর ===")
for p in percentiles:
    print(f"{p}th পার্সেন্টাইল: {np.percentile(errors, p):.2f}")

# এরর থ্রেশহোল্ড
thresholds = [5000, 10000, 20000, 30000, 50000]
print("\n=== থ্রেশহোল্ড অনুযায়ী সঠিক প্রেডিকশন ===")
for th in thresholds:
    within_threshold = (errors <= th).mean() * 100
    print(f"{th:>6,.0f} Tk এর মধ্যে: {within_threshold:.1f}%")

# প্রেডিকশন accuracy (%) — বিভিন্ন টলারেন্সে
print("\n=== বিভিন্ন টলারেন্সে অ্যাকুরেসি ===")
for tol in [0.05, 0.10, 0.15, 0.20, 0.25]:
    accuracy = (errors / y_test <= tol).mean() * 100
    print(f"{tol*100:.0f}% টলারেন্স: {accuracy:.1f}%")
```

### ৪. ক্রস-ভ্যালিডেশন অ্যানালাইসিস

```python
from sklearn.model_selection import cross_validate, KFold

def detailed_cross_validation(model, X, y, cv=10):
    """ডিটেইলড ক্রস-ভ্যালিডেশন"""
    
    scoring = {
        'r2': 'r2',
        'neg_mse': 'neg_mean_squared_error',
        'neg_mae': 'neg_mean_absolute_error',
        'explained_var': 'explained_variance'
    }
    
    cv_results = cross_validate(
        model, X, y,
        cv=KFold(n_splits=cv, shuffle=True, random_state=42),
        scoring=scoring,
        return_train_score=True
    )
    
    print(f"\n=== {cv}-ফোল্ড ক্রস-ভ্যালিডেশন রেজাল্ট ===")
    print(f"{'মেট্রিক':<20} {'ট্রেইন':<12} {'টেস্ট':<12} {'ডিফারেন্স':<12}")
    print("-"*56)
    
    for metric in ['r2', 'neg_mse', 'neg_mae']:
        train_scores = cv_results[f'train_{metric}']
        test_scores = cv_results[f'test_{metric}']
        
        train_mean = np.mean(train_scores)
        test_mean = np.mean(test_scores)
        
        print(f"{metric:<20} {train_mean:>8.4f} +/- {np.std(train_scores):.4f}  "
              f"{test_mean:>8.4f} +/- {np.std(test_scores):.4f}  "
              f"{train_mean - test_mean:>8.4f}")
    
    return cv_results

cv_results = detailed_cross_validation(best_model, X_train, y_train, cv=10)

# প্রতিটি ফোল্ডের R²
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), cv_results['train_r2'], 'bo-', label='Train R²', alpha=0.7)
plt.plot(range(1, 11), cv_results['test_r2'], 'rs-', label='Test R²', alpha=0.7)
plt.axhline(y=np.mean(cv_results['test_r2']), color='g', linestyle='--', 
            label=f'Mean Test R² = {np.mean(cv_results["test_r2"]):.4f}')
plt.xlabel('ফোল্ড নম্বর')
plt.ylabel('R² স্কোর')
plt.title('ক্রস-ভ্যালিডেশন: প্রতি ফোল্ডের R²')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('capstone_cv_folds.png', dpi=100)
plt.show()
print("ক্রস-ভ্যালিডেশন ফোল্ড প্লট সেভ করা হয়েছে")
```

### ৫. লার্নিং কার্ভ

```python
from sklearn.model_selection import learning_curve

def plot_learning_curve(model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)):
    """লার্নিং কার্ভ প্লট"""
    
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=cv, train_sizes=train_sizes,
        scoring='r2', random_state=42
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='ট্রেইন স্কোর', linewidth=2)
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.2, color='blue')
    
    plt.plot(train_sizes, test_mean, 'o-', color='red', label='ক্রস-ভ্যালিডেশন স্কোর', linewidth=2)
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, 
                     alpha=0.2, color='red')
    
    plt.xlabel('ট্রেইনিং ডেটা সাইজ')
    plt.ylabel('R² স্কোর')
    plt.title('লার্নিং কার্ভ')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('capstone_learning_curve.png', dpi=100)
    plt.show()
    print("লার্নিং কার্ভ সেভ করা হয়েছে")

plot_learning_curve(best_model, X_train, y_train)
```

### ৬. এরর অ্যানালাইসিস — সবচেয়ে বড় এরর

```python
# সবচেয়ে বড় এররগুলো
error_df = pd.DataFrame({
    'actual': y_test.values,
    'predicted': y_test_pred,
    'error': residuals,
    'abs_error': np.abs(residuals),
    'pct_error': np.abs(residuals) / y_test.values * 100
})

print("\n=== সবচেয়ে বড় ১০টি এরর ===")
worst_errors = error_df.nlargest(10, 'abs_error')
print(worst_errors.to_string())

print(f"\n=== সবচেয়ে ছোট ১০টি এরর ===")
best_errors = error_df.nsmallest(10, 'abs_error')
print(best_errors.to_string())

# এরর ক্যাটাগরি
error_df['error_category'] = pd.cut(
    error_df['abs_error'],
    bins=[0, 5000, 15000, 30000, 50000, float('inf')],
    labels=['Excellent', 'Good', 'Fair', 'Poor', 'Very Poor']
)

print("\n=== এরর ক্যাটাগরি ডিস্ট্রিবিউশন ===")
print(error_df['error_category'].value_counts().sort_index())

# এরর ক্যাটাগরি পাই চার্ট
plt.figure(figsize=(8, 8))
error_df['error_category'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', startangle=90,
    colors=['green', 'lightgreen', 'yellow', 'orange', 'red']
)
plt.title('এরর ক্যাটাগরি ডিস্ট্রিবিউশন')
plt.ylabel('')
plt.tight_layout()
plt.savefig('capstone_error_categories.png', dpi=100)
plt.show()
print("এরর ক্যাটাগরি চার্ট সেভ করা হয়েছে")
```

### ৭. মডেল স্টেবিলিটি টেস্ট

```python
def stability_test(model, X, y, n_runs=10, test_size=0.2):
    """মডেল স্টেবিলিটি টেস্ট — একাধিক রান"""
    
    from sklearn.model_selection import train_test_split
    
    results = []
    for i in range(n_runs):
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=test_size, random_state=i
        )
        model.fit(X_tr, y_tr)
        y_pred = model.predict(X_te)
        
        results.append({
            'run': i + 1,
            'r2': r2_score(y_te, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_te, y_pred)),
            'mae': mean_absolute_error(y_te, y_pred)
        })
    
    results_df = pd.DataFrame(results)
    
    print("\n=== মডেল স্টেবিলিটি টেস্ট ===")
    print(f"{'রান':<6} {'R²':<10} {'RMSE':<12} {'MAE':<12}")
    print("-"*40)
    for _, row in results_df.iterrows():
        print(f"{row['run']:<6} {row['r2']:<10.4f} {row['rmse']:<12.2f} {row['mae']:<12.2f}")
    
    print("-"*40)
    print(f"{'মিন':<6} {results_df['r2'].min():<10.4f} {results_df['rmse'].min():<12.2f} {results_df['mae'].min():<12.2f}")
    print(f"{'ম্যাক্স':<6} {results_df['r2'].max():<10.4f} {results_df['rmse'].max():<12.2f} {results_df['mae'].max():<12.2f}")
    print(f"{'স্টাড':<6} {results_df['r2'].std():<10.4f} {results_df['rmse'].std():<12.2f} {results_df['mae'].std():<12.2f}")
    
    return results_df

stability_results = stability_test(best_model, pd.concat([X_train, X_test]), 
                                    pd.concat([y_train, y_test]))
```

### ৮. ফাইনাল রিপোর্ট

```python
print("\n" + "="*70)
print("📊 ক্যাপস্টোন প্রোজেক্ট — ফাইনাল মডেল ইভালুয়েশন রিপোর্ট")
print("="*70)

print(f"\n📌 সেরা মডেল: {metrics[0]['model_name']}")
print(f"📌 ট্রেইনিং টাইম: {metrics[0]['train_time']:.2f} সেকেন্ড")

print(f"\n🎯 পারফরমেন্স মেট্রিক্স:")
print(f"   R² (টেস্ট):       {eval_metrics['R² (Coefficient of Determination)']:.4f}")
print(f"   অ্যাডজাস্টেড R²:  {eval_metrics['Adjusted R²']:.4f}")
print(f"   RMSE:             {eval_metrics['RMSE (Root Mean Squared Error)']:.2f}")
print(f"   MAE:              {eval_metrics['MAE (Mean Absolute Error)']:.2f}")
print(f"   MAPE:             {eval_metrics['MAPE (Mean Absolute Percentage Error)']:.2f}%")
print(f"   Expl. Variance:   {eval_metrics['Explained Variance']:.4f}")

print(f"\n📈 ওভারফিটিং:")
print(f"   ট্রেইন R²:        {eval_metrics['Train R²']:.4f}")
print(f"   ওভারফিটিং গ্যাপ:  {eval_metrics['Overfitting Gap']:.4f}")

print(f"\n✅ ভেরডিক্ট: ", end="")
if eval_metrics['R² (Coefficient of Determination)'] >= 0.85:
    print("মডেলটি চমৎকার পারফরমেন্স দেখিয়েছে!")
elif eval_metrics['R² (Coefficient of Determination)'] >= 0.70:
    print("মডেলটি ভালো পারফরমেন্স দেখিয়েছে।")
elif eval_metrics['R² (Coefficient of Determination)'] >= 0.50:
    print("মডেলটি মোটামুটি পারফরমেন্স দেখিয়েছে।")
else:
    print("মডেলটির আরও উন্নতি প্রয়োজন।")

# মডেল ইভালুয়েশন রিপোর্ট সেভ
report = {
    'best_model': metrics[0]['model_name'],
    'test_r2': eval_metrics['R² (Coefficient of Determination)'],
    'test_rmse': eval_metrics['RMSE (Root Mean Squared Error)'],
    'test_mae': eval_metrics['MAE (Mean Absolute Error)'],
    'mape': eval_metrics['MAPE (Mean Absolute Percentage Error)'],
    'overfitting_gap': eval_metrics['Overfitting Gap'],
}

joblib.dump(report, 'evaluation_report.pkl')
print("\nফাইনাল ইভালুয়েশন রিপোর্ট সেভ করা হয়েছে: evaluation_report.pkl")
```

### সারাংশ
- ✅ কম্প্রিহেনসিভ মেট্রিক্স ক্যালকুলেশন
- ✅ রেসিডুয়াল অ্যানালাইসিস (ডিস্ট্রিবিউশন, Q-Q প্লট, হেটারোসকেড্যাস্টিসিটি)
- ✅ ক্রস-ভ্যালিডেশন অ্যানালাইসিস (10-ফোল্ড)
- ✅ লার্নিং কার্ভ অ্যানালাইসিস
- ✅ এরর ডিস্ট্রিবিউশন ও ক্যাটেগোরাইজেশন
- ✅ মডেল স্টেবিলিটি টেস্ট
- ✅ ফাইনাল ইভালুয়েশন রিপোর্ট