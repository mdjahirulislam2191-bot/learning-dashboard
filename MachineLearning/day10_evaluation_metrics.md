# Day 10: ইভালুয়েশন মেট্রিক্স
## Evaluation Metrics

### Regression Evaluation Metrics
রিগ্রেশন মডেলের পারফরম্যান্স পরিমাপের জন্য বিভিন্ন মেট্রিক্স ব্যবহার করা হয়।

### ফাইন্যান্স উদাহরণ: স্টক প্রাইস প্রেডিকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error, explained_variance_score
)

# স্টক প্রাইস ডেটা
np.random.seed(42)
n = 500
true_price = 100 + np.cumsum(np.random.randn(n) * 0.5)
predicted_price = true_price + np.random.randn(n) * 2  # মডেল প্রেডিকশন

# কিছু মিস্যালাইনমেন্ট
predicted_price[100:150] += np.random.randn(50) * 5  # কিছু বেশি ভুল

# Actual vs Predicted
y_true = true_price[200:]
y_pred = predicted_price[200:]
```

### সমস্ত Regression Metrics
```python
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred) * 100
r2 = r2_score(y_true, y_pred)
evs = explained_variance_score(y_true, y_pred)

print("📊 Regression Evaluation Metrics:")
print(f"{'Metric':25s} {'Value':>12s}")
print("-" * 37)
print(f"{'MSE':25s} {mse:>12.2f}")
print(f"{'RMSE':25s} {rmse:>12.2f}")
print(f"{'MAE':25s} {mae:>12.2f}")
print(f"{'MAPE':25s} {mape:>12.1%}")
print(f"{'R² Score':25s} {r2:>12.4f}")
print(f"{'Explained Variance':25s} {evs:>12.4f}")
```

### ফাইন্যান্স-স্পেসিফিক মেট্রিক্স
```python
# Sharp Ratio (রিস্ক-অ্যাডজাস্টেড রিটার্ন)
def sharpe_ratio(returns, risk_free_rate=0.02):
    excess_returns = returns - risk_free_rate/252
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# Directional Accuracy (ঠিক দিক পূর্বাভাস)
def directional_accuracy(y_true, y_pred):
    true_direction = np.sign(np.diff(y_true))
    pred_direction = np.sign(np.diff(y_pred))
    # লেংথ ম্যাচ করা
    min_len = min(len(true_direction), len(pred_direction))
    return np.mean(true_direction[:min_len] == pred_direction[:min_len])

# Profit Factor (মুনাফা ফ্যাক্টর)
def profit_factor(y_true, y_pred, threshold=0):
    # ট্রেড সিগন্যাল: প্রেডিক্টেড > থ্রেশহোল্ড
    signals = y_pred > threshold
    returns = np.diff(np.concatenate([[y_true[0]], y_true]))
    trade_returns = returns * signals[:len(returns)]
    
    gross_profit = trade_returns[trade_returns > 0].sum()
    gross_loss = abs(trade_returns[trade_returns < 0].sum())
    
    return gross_profit / gross_loss if gross_loss > 0 else np.inf

print("\n📈 Finance-Specific Metrics:")
print(f"Directional Accuracy:  {directional_accuracy(y_true, y_pred):.2%}")
print(f"Profit Factor:         {profit_factor(y_true, y_pred):.4f}")

# ট্রেডিং সিমুলেশন
daily_returns = np.diff(np.concatenate([[y_true[0]], y_true]))
trades = tp_returns = daily_returns * (np.sign(np.diff(np.concatenate([[y_pred[0]], y_pred]))) > 0)[:len(daily_returns)]

print(f"Sharpe Ratio (annual): {sharpe_ratio(trades):.4f}")
print(f"Total Trades:           {np.sum(np.sign(np.diff(np.concatenate([[y_pred[0]], y_pred]))) != 0)}")
```

### Classification Metrics (বাইনারি)
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    log_loss, matthews_corrcoef
)

# ফ্রড ডিটেকশন সিমুলেশন
np.random.seed(42)
n = 1000
y_true_clf = np.random.binomial(1, 0.1, n)  # 10% ফ্রড
y_prob_clf = 0.1 + y_true_clf * 0.6 + np.random.randn(n) * 0.2
y_prob_clf = np.clip(y_prob_clf, 0, 1)
y_pred_clf = (y_prob_clf > 0.3).astype(int)

print("\n\n📊 Classification Metrics:")
print(f"{'Metric':25s} {'Value':>10s}")
print("-" * 35)
print(f"{'Accuracy':25s} {accuracy_score(y_true_clf, y_pred_clf):>10.4f}")
print(f"{'Precision':25s} {precision_score(y_true_clf, y_pred_clf):>10.4f}")
print(f"{'Recall':25s} {recall_score(y_true_clf, y_pred_clf):>10.4f}")
print(f"{'F1 Score':25s} {f1_score(y_true_clf, y_pred_clf):>10.4f}")
print(f"{'ROC AUC':25s} {roc_auc_score(y_true_clf, y_prob_clf):>10.4f}")
print(f"{'Log Loss':25s} {log_loss(y_true_clf, y_prob_clf):>10.4f}")
print(f"{'Matthews Corr':25s} {matthews_corrcoef(y_true_clf, y_pred_clf):>10.4f}")

print("\nConfusion Matrix:")
cm = confusion_matrix(y_true_clf, y_pred_clf)
print(pd.DataFrame(cm, index=['Actual Neg', 'Actual Pos'], 
                   columns=['Pred Neg', 'Pred Pos']))
```

### Confusion Matrix বুঝুন
```python
TN, FP, FN, TP = cm.ravel()
print(f"""
Confusion Matrix Breakdown:
                          Predicted
                    No Fraud    Fraud
Actual No Fraud     {TN:5d} (TN)  {FP:5d} (FP)
Actual Fraud        {FN:5d} (FN)  {TP:5d} (TP)

মেট্রিক্স:
- Accuracy:  {(TP+TN)/(TP+TN+FP+FN):.4f} (সঠিক পূর্বাভাসের হার)
- Precision: {TP/(TP+FP):.4f} (ফ্রড বললে কতটা সঠিক)
- Recall:    {TP/(TP+FN):.4f} (প্রকৃত ফ্রডের কতটা ধরতে পেরেছি)
- F1:        {2*TP/(2*TP+FP+FN):.4f} (Precision + Recall এর হারমোনিক মিন)
""")
```

### ROC Curve এবং AUC
```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_true_clf, y_prob_clf)
roc_auc = auc(fpr, tpr)

# J-statistic (Youden's Index) দিয়ে Best Threshold
j_scores = tpr - fpr
best_idx = np.argmax(j_scores)
best_threshold = thresholds[best_idx]

print(f"\n🎯 Optimal Threshold (Youden's J): {best_threshold:.4f}")
print(f"   Sensitivity (TPR): {tpr[best_idx]:.4f}")
print(f"   Specificity (TNR): {1-fpr[best_idx]:.4f}")
print(f"   AUC: {roc_auc:.4f}")
```

### Regression Metrics Visualization
```python
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
residuals = y_true - y_pred
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')

plt.subplot(1, 2, 2)
plt.hist(residuals, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Residual Error')
plt.ylabel('Frequency')
plt.title(f'Residual Distribution\nMean={residuals.mean():.2f}, Std={residuals.std():.2f}')
plt.axvline(x=0, color='r', linestyle='--')

plt.tight_layout()
plt.show()
```

### মেট্রিক্স নির্বাচনের নির্দেশিকা
```python
print("""
📋 Metric Selection Guide:

Regression:
├── MSE/RMSE: বড় এরর পেনালাইজ করতে (outlier sensitive)
├── MAE: সব এরর সমান ওজন (robust)
├── MAPE: শতাংশে ভুল বুঝতে (ব্যাখ্যাযোগ্য)
├── R²: মডেল কতটা variance explain করে
└── Directional Accuracy: ট্রেডিং সিগন্যালের জন্য

Classification (Imbalanced):
├── Precision: FP কমানো জরুরি হলে (Spam filter)
├── Recall: FN কমানো জরুরি হলে (Fraud detection)
├── F1: Precision-Recall ব্যালেন্স
├── ROC-AUC: ওভারঅল পারফরম্যান্স
└── Matthews Correlation: ইমব্যালেন্সড ক্লাসের জন্য

Finance Specific:
├── Sharpe Ratio: রিস্ক-অ্যাডজাস্টেড রিটার্ন
├── Profit Factor: উইন/লস রেশিও
└── Maximum Drawdown: সবচেয়ে বড় লোকসান
""")
```

### সারসংক্ষেপ
Evaluation metrics মডেলের পারফরম্যান্স বুঝতে সাহায্য করে। এক মেট্রিক্সে ভালো মানে সব মেট্রিক্সে ভালো নয়। ফাইন্যান্সের প্রেক্ষাপটে সঠিক মেট্রিক্স নির্বাচন করা গুরুত্বপূর্ণ - যেমন ফ্রড ডিটেকশনে Recall বেশি গুরুত্বপূর্ণ।