# Day 58: ক্যাপস্টোন — মডেল ইভালুয়েশন 📊📉

## মডেল ইভালুয়েশন ওভারভিউ
আজ আমরা ক্যাপস্টোন LSTM মডেলের সম্পূর্ণ ইভালুয়েশন করব — শুধু অ্যাকুরেসি নয়, ফিন্যান্সিয়াল মেট্রিক্সও।

### ইভালুয়েশন মেট্রিক্স
1. **ক্লাসিফিকেশন মেট্রিক্স**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
2. **ফিন্যান্সিয়াল মেট্রিক্স**: Sharpe Ratio, Max Drawdown, Win Rate, Profit Factor
3. **রোবাস্টনেস চেক**: Overfitting Detection, Confidence Analysis, Feature Importance

### ফিন্যান্সিয়াল ইভালুয়েশন কেন গুরুত্বপূর্ণ?
- 60% অ্যাকুরেসি ট্রেডিংয়ে লাভজনক হতে পারে (যদি risk:reward ভাল হয়)
- 80% অ্যাকুরেসিও লোকসান দিতে পারে (যদি ডাউনসাইড মিস হয়)
- কনফিডেন্স ক্যালিব্রেশন অত্যন্ত গুরুত্বপূর্ণ

## ইভালুয়েশন পাইপলাইন

```python
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             confusion_matrix, classification_report)
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. মডেল লোড এবং ইনফারেন্স

```python
class ModelInference:
    """মডেল লোড এবং ইনফারেন্স"""
    
    @staticmethod
    def create_mock_model():
        """ডেমো মডেল তৈরি (যদি প্রি-ট্রেইনড না থাকে)"""
        # ডে 57-এর মডেল আর্কিটেকচার
        import torch.nn as nn
        
        class MockLSTM(nn.Module):
            def __init__(self, input_dim=14, hidden_dim=128, num_classes=3):
                super().__init__()
                self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
                self.fc = nn.Linear(hidden_dim, num_classes)
            
            def forward(self, x):
                out, _ = self.lstm(x)
                out = out[:, -1, :]
                return self.fc(out)
        
        model = MockLSTM()
        return model
    
    @staticmethod
    def get_predictions(model, loader, device):
        """সমস্ত ডেটার জন্য প্রেডিকশন"""
        model.eval()
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for X_batch, y_batch in loader:
                X_batch = X_batch.to(device)
                outputs = model(X_batch)
                probs = F.softmax(outputs, dim=1)
                _, preds = outputs.max(1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(y_batch.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        return {
            'predictions': np.array(all_preds),
            'labels': np.array(all_labels),
            'probabilities': np.array(all_probs)
        }

# সিমুলেটেড প্রেডিকশন (ডেমো)
n_samples = 500
np.random.seed(42)
true_labels = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3])

# সিমুলেটেড প্রেডিকশন (60% অ্যাকুরেসি + কিছু প্যাটার্ন)
pred_probs = np.zeros((n_samples, 3))
for i in range(n_samples):
    if np.random.random() < 0.6:
        pred_probs[i, true_labels[i]] = 0.7 + np.random.random() * 0.2
    else:
        wrong = [x for x in range(3) if x != true_labels[i]]
        pred_probs[i, np.random.choice(wrong)] = 0.7 + np.random.random() * 0.2

pred_probs = pred_probs / pred_probs.sum(axis=1, keepdims=True)
predictions = pred_probs.argmax(axis=1)

results = {
    'predictions': predictions,
    'labels': true_labels,
    'probabilities': pred_probs
}

print(f"সিমুলেটেড প্রেডিকশন লোডেড: {n_samples} স্যাম্পল")
print(f"ক্লাস ডিস্ট্রিবিউশন:")
for cls, name in enumerate(['DOWN', 'NEUTRAL', 'UP']):
    print(f"  {name}: ট্রু={sum(results['labels']==cls)}, প্রেড={sum(results['predictions']==cls)}")
```

## 2. ক্লাসিফিকেশন মেট্রিক্স

```python
class ClassificationMetrics:
    """সম্পূর্ণ ক্লাসিফিকেশন ইভালুয়েশন"""
    
    @staticmethod
    def compute_all_metrics(results, class_names=None):
        """সব ক্লাসিফিকেশন মেট্রিক্স"""
        if class_names is None:
            class_names = ['DOWN 📉', 'NEUTRAL ➡️', 'UP 📈']
        
        y_true = results['labels']
        y_pred = results['predictions']
        
        # বেসিক মেট্রিক্স
        accuracy = accuracy_score(y_true, y_pred)
        
        # Precision, Recall, F1
        precision, recall, f1, support = precision_recall_fscore_support(
            y_true, y_pred, average=None, zero_division=0
        )
        
        # ম্যাক্রো/ওয়েটেড F1
        macro_f1 = np.mean(f1)
        weighted_f1 = np.average(f1, weights=support)
        
        print("\n" + "="*50)
        print("📊 ক্লাসিফিকেশন ইভালুয়েশন")
        print("="*50)
        print(f"Accucary: {accuracy:.2%} ({accuracy*100:.1f}%)")
        print(f"Macro F1: {macro_f1:.4f}")
        print(f"Weighted F1: {weighted_f1:.4f}")
        
        print(f"\n{'ক্লাস':<18} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'সাপোর্ট':<8}")
        print("-" * 60)
        for i in range(3):
            print(f"{class_names[i]:<18} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]:<8}")
        
        # কনফিউশন ম্যাট্রিক্স
        cm = confusion_matrix(y_true, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"{'':<12}", end='')
        for name in class_names:
            print(f"{name:<12}", end='')
        print()
        for i in range(3):
            print(f"{class_names[i]:<8}", end='')
            for j in range(3):
                print(f"{cm[i][j]:<12}", end='')
            print()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'macro_f1': macro_f1,
            'weighted_f1': weighted_f1,
            'confusion_matrix': cm,
            'support': support
        }
    
    @staticmethod
    def classification_report_text(results):
        """টেক্সট রিপোর্ট জেনারেট"""
        y_true = results['labels']
        y_pred = results['predictions']
        
        report = classification_report(
            y_true, y_pred,
            target_names=['DOWN 📉', 'NEUTRAL ➡️', 'UP 📈'],
            zero_division=0
        )
        print("\n=== Classification Report ===")
        print(report)

# গণনা
metrics = ClassificationMetrics.compute_all_metrics(results)
ClassificationMetrics.classification_report_text(results)
```

## 3. ফিন্যান্সিয়াল মেট্রিক্স

```python
class FinancialMetrics:
    """ফিন্যান্সিয়াল পারফরম্যান্স মেট্রিক্স"""
    
    @staticmethod
    def simulate_trades(results, initial_capital=10000, trade_size=0.3):
        """প্রেডিকশনের ভিত্তিতে ট্রেডিং সিমুলেশন"""
        y_pred = results['predictions']
        probs = results['probabilities']
        
        balance = initial_capital
        holdings = 0
        trades = []
        equity_curve = [initial_capital]
        
        for i in range(len(y_pred)):
            pred = y_pred[i]
            confidence = probs[i].max()
            
            # শুধু হাই-কনফিডেন্স ট্রেড (কনফিডেন্স > 0.6)
            if confidence < 0.6:
                equity_curve.append(balance + holdings * 100)  # সিম্পল প্রাইস
                continue
            
            if pred == 2:  # UP প্রেডিক্ট → BUY
                if balance > 0 and holdings == 0:
                    invest = balance * trade_size
                    shares = invest / 100  # সিম্পল প্রাইস $100
                    holdings += shares
                    balance -= invest
                    trades.append(('BUY', i, confidence))
            
            elif pred == 0:  # DOWN প্রেডিক্ট → SELL
                if holdings > 0:
                    balance += holdings * 100
                    trades.append(('SELL', i, confidence))
                    holdings = 0
            
            current_value = balance + holdings * 100
            equity_curve.append(current_value)
        
        # ফাইনাল ভ্যালু
        final_value = balance + holdings * 100
        total_return = (final_value - initial_capital) / initial_capital
        
        # ড্রডাউন
        equity = np.array(equity_curve)
        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak
        max_drawdown = drawdown.min()
        
        # শার্প রেশিও
        returns = np.diff(equity) / equity[:-1]
        if np.std(returns) > 0:
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe = 0
        
        # Win Rate
        if len(trades) > 1:
            wins = sum(1 for t in trades if t[0] == 'SELL')
            win_rate = wins / (len(trades) / 2) if len(trades) > 0 else 0
        else:
            win_rate = 0
        
        portfolio = {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'total_trades': len(trades),
            'win_rate': win_rate,
            'equity_curve': equity_curve
        }
        
        return portfolio
    
    @staticmethod
    def print_financial_summary(portfolio):
        """ফিন্যান্সিয়াল সারাংশ প্রিন্ট"""
        print("\n" + "="*50)
        print("💰 ফিন্যান্সিয়াল পারফরম্যান্স সারাংশ")
        print("="*50)
        print(f"প্রাথমিক মূলধন: ${portfolio['initial_capital']:,.2f}")
        print(f"ফাইনাল ভ্যালু: ${portfolio['final_value']:,.2f}")
        print(f"মোট রিটার্ন: {portfolio['total_return']:.2%}")
        print(f"ম্যাক্স ড্রডাউন: {portfolio['max_drawdown']:.2%}")
        print(f"শার্প রেশিও (বার্ষিক): {portfolio['sharpe_ratio']:.2f}")
        print(f"মোট ট্রেড: {portfolio['total_trades']}")
        print(f"উইন রেট: {portfolio['win_rate']:.2%}")
        
        # পারফরম্যান্স রেটিং
        if portfolio['sharpe_ratio'] > 1.0:
            print("📊 পারফরম্যান্স: ⭐⭐⭐ চমৎকার!")
        elif portfolio['sharpe_ratio'] > 0.5:
            print("📊 পারফরম্যান্স: ⭐⭐ ভাল")
        elif portfolio['total_return'] > 0:
            print("📊 পারফরম্যান্স: ⭐ গ্রহণযোগ্য")
        else:
            print("📊 পারফরম্যান্স: ❌ উন্নতি প্রয়োজন")

# ফিন্যান্সিয়াল সিমুলেশন
portfolio = FinancialMetrics.simulate_trades(results)
FinancialMetrics.print_financial_summary(portfolio)
```

## 4. কনফিডেন্স অ্যানালাইসিস

```python
class ConfidenceAnalysis:
    """মডেল কনফিডেন্স এবং ক্যালিব্রেশন অ্যানালাইসিস"""
    
    @staticmethod
    def analyze_confidence(results):
        """কনফিডেন্স অ্যানালাইসিস"""
        probs = results['probabilities']
        preds = results['predictions']
        labels = results['labels']
        
        # কনফিডেন্স বিন
        conf_bins = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        bin_names = ['30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
        
        max_confs = probs.max(axis=1)
        
        print("\n" + "="*50)
        print("🔮 কনফিডেন্স অ্যানালাইসিস")
        print("="*50)
        print(f"{'কনফিডেন্স রেঞ্জ':<18} {'কাউন্ট':<10} {'অ্যাকুরেসি':<12}")
        print("-" * 40)
        
        results_by_conf = {}
        for i, (low, high) in enumerate(zip(conf_bins[:-1], conf_bins[1:])):
            mask = (max_confs >= low) & (max_confs < high)
            if mask.sum() > 0:
                acc = (preds[mask] == labels[mask]).mean()
                results_by_conf[f'{low:.0%}-{high:.0%}'] = {
                    'count': mask.sum(),
                    'accuracy': acc
                }
                print(f"{low:.0%}-{high:.0%:<16} {mask.sum():<10} {acc:.2%}")
        
        # হাই কনফিডেন্স (%) স্ট্যাটস
        high_conf_mask = max_confs >= 0.7
        high_conf_acc = (preds[high_conf_mask] == labels[high_conf_mask]).mean() if high_conf_mask.sum() > 0 else 0
        
        print(f"\nহাই-কনফিডেন্স (≥70%): {high_conf_mask.sum()} স্যাম্পল, অ্যাকুরেসি: {high_conf_acc:.2%}")
        
        low_conf_mask = max_confs < 0.5
        low_conf_acc = (preds[low_conf_mask] == labels[low_conf_mask]).mean() if low_conf_mask.sum() > 0 else 0
        print(f"লো-কনফিডেন্স (<50%): {low_conf_mask.sum()} স্যাম্পল, অ্যাকুরেসি: {low_conf_acc:.2%}")
        
        return results_by_conf
    
    @staticmethod
    def confidence_vs_accuracy_plot():
        """কনফিডেন্স vs অ্যাকুরেসি ছক"""
        print("\n" + "="*50)
        print("📈 কনফিডেন্স বনাম অ্যাকুরেসি এনালাইসিস")
        print("="*50)
        print("একটি ভাল ক্যালিব্রেটেড মডেলে:")
        print("  কনফিডেন্স 50% → অ্যাকুরেসি ~50%")
        print("  কনফিডেন্স 70% → অ্যাকুরেসি ~70%")
        print("  কনফিডেন্স 90% → অ্যাকুরেসি ~90%")
        print("\nযদি অ্যাকুরেসি কনফিডেন্সের চেয়ে কম হয়:")
        print("  → মডেল ওভারকনফিডেন্ট (পুনঃক্যালিব্রেশন প্রয়োজন)")
        print("  → সমাধান: Temperature Scaling বা Platt Scaling")

# কনফিডেন্স অ্যানালাইসিস
conf_analysis = ConfidenceAnalysis.analyze_confidence(results)
ConfidenceAnalysis.confidence_vs_accuracy_plot()
```

## 5. ফিচার ইম্পর্টেন্স এবং মডেল ডিবাগিং

```python
class ModelDebugging:
    """মডেল ডিবাগিং এবং ইন্টারপ্রিটেবিলিটি"""
    
    @staticmethod
    def error_analysis(results):
        """ভুল প্রেডিকশন অ্যানালাইসিস"""
        preds = results['predictions']
        labels = results['labels']
        probs = results['probabilities']
        
        # ভুল প্রেডিকশন খুঁজুন
        errors = preds != labels
        
        print("\n" + "="*50)
        print("🔍 এরর অ্যানালাইসিস")
        print("="*50)
        print(f"মোট ভুল: {errors.sum()} / {len(errors)} ({(errors.sum()/len(errors))*100:.1f}%)")
        
        # এরর ডিস্ট্রিবিউশন
        print(f"\nএরর টাইপ ডিস্ট্রিবিউশন:")
        for true_cls in range(3):
            true_names = ['DOWN', 'NEUTRAL', 'UP']
            mask = labels == true_cls
            if mask.sum() > 0:
                error_mask = errors & mask
                print(f"  ট্রু {true_names[true_cls]}: {error_mask.sum()}/{mask.sum()} ভুল "
                      f"({(error_mask.sum()/mask.sum())*100:.1f}%)")
                
                # কোথায় প্রেডিক্ট করেছে
                if error_mask.sum() > 0:
                    error_preds = preds[error_mask]
                    for pred_cls in range(3):
                        if pred_cls != true_cls:
                            count = (error_preds == pred_cls).sum()
                            if count > 0:
                                print(f"    → {true_names[pred_cls]} বলে ভুল করেছে: {count} বার")
    
    @staticmethod
    def feature_sensitivity_analysis():
        """ফিচার সেনসিটিভিটি অ্যানালাইসিস (কনসেপ্ট)"""
        print("\n" + "="*50)
        print("🧪 ফিচার সেনসিটিভিটি অ্যানালাইসিস")
        print("="*50)
        print("ফিচার ইম্পর্টেন্স টেস্ট করার পদ্ধতি:")
        print("1️⃣ Permutation Importance")
        print("   - একটি ফিচারের ভ্যালু শাফল করুন")
        print("   - অ্যাকুরেসি ড্রপ = ফিচার ইম্পর্টেন্স")
        print()
        print("2️⃣ Gradient-based Importance")
        print("   - ∂출력/∂ইনপুট গ্রেডিয়েন্ট ক্যালকুলেট করুন")
        print("   - গ্রেডিয়েন্ট ম্যাগনিচিউড = ইম্পর্টেন্স")
        print()
        print("3️⃣ Ablation Study")
        print("   - একটি ফিচার সম্পূর্ণ রিমুভ করে মডেল টেস্ট")
        
        # সিম্পল ফিচার ইম্পর্টেন্স ডেমো
        feature_names = [
            'রিটার্ন', 'ভলাটিলিটি', 'RSI', 'MACD', 'BB_position',
            'SMA_10', 'SMA_20', 'SMA_50', 'ATR', 'ভলিউম',
            'মোমেন্টাম', 'হাই-লো', 'ক্লোজ-ওপেন', 'ম্যাকড_হিস্ট'
        ]
        
        # সিমুলেটেড ইম্পর্টেন্স
        importances = np.random.rand(len(feature_names))
        importances = importances / importances.sum()
        
        print(f"\nসিমুলেটেড ফিচার ইম্পর্টেন্স (টপ-5):")
        top5 = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:5]
        for i, (name, imp) in enumerate(top5, 1):
            print(f"  {i}. {name}: {imp:.2%}")

# এরর অ্যানালাইসিস
ModelDebugging.error_analysis(results)
ModelDebugging.feature_sensitivity_analysis()
```

## 6. ফাইনাল রিপোর্ট

```python
class FinalReport:
    """সম্পূর্ণ ইভালুয়েশন রিপোর্ট"""
    
    @staticmethod
    def generate_final_report(metrics, portfolio, conf_analysis):
        """ফাইনাল রিপোর্ট জেনারেট"""
        print("\n\n" + "="*60)
        print("📋 ক্যাপস্টোন LSTM মডেল — ফাইনাল ইভালুয়েশন রিপোর্ট")
        print("="*60)
        
        print("\n✅ ক্লাসিফিকেশন পারফরম্যান্স:")
        print(f"   অ্যাকুরেসি: {metrics['accuracy']:.2%}")
        print(f"   ম্যাক্রো F1: {metrics['macro_f1']:.4f}")
        print(f"   বেস্ট ক্লাস: UP (F1={metrics['f1'][2]:.3f})")
        print(f"   ওয়ার্স্ট ক্লাস: NEUTRAL (F1={metrics['f1'][1]:.3f})")
        
        print("\n💰 ট্রেডিং পারফরম্যান্স:")
        print(f"   রিটার্ন: {portfolio['total_return']:.2%}")
        print(f"   শার্প রেশিও: {portfolio['sharpe_ratio']:.2f}")
        print(f"   ম্যাক্স ড্রডাউন: {portfolio['max_drawdown']:.2%}")
        print(f"   উইন রেট: {portfolio['win_rate']:.2%}")
        
        print("\n🔮 কনফিডেন্স:")
        print(f"   হাই-কনফিডেন্স (≥70%) স্যাম্পল: {sum(1 for c in np.max(results['probabilities'], axis=1) >= 0.7)}")
        print(f"   গড় কনফিডেন্স: {np.max(results['probabilities'], axis=1).mean():.2%}")
        
        print("\n📌 ফাইনাল রেকমেন্ডেশন:")
        if portfolio['sharpe_ratio'] > 1.0 and metrics['accuracy'] > 0.6:
            print("   ✅ মডেল প্রোডাকশনের জন্য প্রস্তুত!")
            print("   ➡️ পরবর্তী ধাপ: RL ট্রেডিং সিস্টেম (Day 59)")
        elif portfolio['total_return'] > 0:
            print("   📊 মডেল গ্রহণযোগ্য, কিন্তু উন্নতি প্রয়োজন")
            print("   ➡️ আরও ডেটা, ফিচার ইঞ্জিনিয়ারিং, হাইপারপ্যারামিটার টিউনিং")
        else:
            print("   ❌ মডেল উন্নতি প্রয়োজন")
            print("   ➡️ মডেল আর্কিটেকচার, ডেটা কোয়ালিটি, ফিচার রিভিউ")
        
        print("\n" + "="*60)
        print("🏁 ডে 58 ইভালুয়েশন সম্পন্ন! ডে 59-এ RL ট্রেডিংয়ের জন্য প্রস্তুত।")
        print("="*60)

# ফাইনাল রিপোর্ট
FinalReport.generate_final_report(metrics, portfolio, conf_analysis)
```

## সারাংশ
- ক্লাসিফিকেশন মেট্রিক্স: Accuracy, Precision, Recall, F1, Confusion Matrix
- ফিন্যান্সিয়াল মেট্রিক্স: Sharpe Ratio, Max Drawdown, Win Rate
- কনফিডেন্স অ্যানালাইসিস: ক্যালিব্রেশন চেক, এরর প্যাটার্ন
- 60%+ অ্যাকুরেসি + ভাল শার্প রেশিও = প্রোডাকশন রেডি
- লো কনফিডেন্স প্রেডিকশন ফিল্টার করলে পারফরম্যান্স বাড়ে
- ফিচার ইম্পর্টেন্স মডেল বুঝতে সাহায্য করে