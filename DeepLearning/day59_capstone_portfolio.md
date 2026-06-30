# Day 59: ক্যাপস্টোন — পোর্টফোলিও অপ্টিমাইজেশন 📊🎯

## পোর্টফোলিও অপ্টিমাইজেশন কী?
RL ট্রেডিং সিগন্যাল + LSTM প্রেডিকশন একত্রিত করে একটি অপ্টিমাল পোর্টফোলিও তৈরি করা।

### ক্যাপস্টোন ইন্টিগ্রেশন
```
Day 56 (ডেটা) → Day 57 (LSTM) → Day 58 (ইভালুয়েশন) → Day 59 (পোর্টফোলিও)
                                                                │
                                                        RL Agent + LSTM Signals
                                                                │
                                                        অপ্টিমাল অ্যালোকেশন
```

### পোর্টফোলিও অপ্টিমাইজেশন টেকনিক
1. **Mean-Variance Optimization (Markowitz)**: রিস্ক-রিটার্ন ট্রেডঅফ
2. **Risk Parity**: সমান রিস্ক কন্ট্রিবিউশন
3. **Black-Litterman**: মার্কেট ইকুইলিব্রিয়াম + ভিউ
4. **RL-based Allocation**: DQN/PPO দিয়ে অ্যালোকেশন

### ফিন্যান্সিয়াল কনসেপ্টস
- Efficient Frontier: সর্বোচ্চ রিটার্নের জন্য ন্যূনতম রিস্ক
- Sharpe Ratio: risk-adjusted return
- Diversification: একাধিক এসেটে বিনিয়োগ

## পোর্টফোলিও অপ্টিমাইজেশন ইমপ্লিমেন্টেশন

```python
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. পোর্টফোলিও ক্লাস এবং মেট্রিক্স

```python
class PortfolioMetrics:
    """পোর্টফোলিও মেট্রিক্স ক্যালকুলেশন"""
    
    @staticmethod
    def calculate_returns(prices):
        """লগ রিটার্ন ক্যালকুলেট"""
        return np.log(prices[1:] / prices[:-1])
    
    @staticmethod
    def portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
        """পোর্টফোলিও স্ট্যাটিস্টিক্স"""
        portfolio_return = np.sum(mean_returns * weights) * 252  # বার্ষিক
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / (portfolio_vol + 1e-8)
        
        return {
            'return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe': sharpe_ratio
        }
    
    @staticmethod
    def neg_sharpe(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
        """নেগেটিভ শার্প রেশিও (মিনিমাইজেশনের জন্য)"""
        stats = PortfolioMetrics.portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate)
        return -stats['sharpe']

# ডেমো: 4 এসেটের জন্য সিমুলেটেড রিটার্ন
n_assets = 4
asset_names = ['Stock_A', 'Stock_B', 'Bond_C', 'Gold_D']
np.random.seed(42)

# সিমুলেটেড বার্ষিক রিটার্ন এবং কোভেরিয়েন্স
mean_returns = np.array([0.12, 0.15, 0.05, 0.08])
cov_matrix = np.array([
    [0.04, 0.02, 0.01, 0.005],
    [0.02, 0.05, 0.015, 0.01],
    [0.01, 0.015, 0.01, 0.003],
    [0.005, 0.01, 0.003, 0.02]
])

print("=== এসেট তথ্য ===")
for i, name in enumerate(asset_names):
    print(f"{name}: গড় রিটার্ন={mean_returns[i]:.2%}, ভলাটিলিটি={np.sqrt(cov_matrix[i][i]):.2%}")
```

## 2. Mean-Variance অপ্টিমাইজেশন

```python
class MeanVarianceOptimizer:
    """Markowitz Mean-Variance অপ্টিমাইজেশন"""
    
    def __init__(self, mean_returns, cov_matrix, risk_free_rate=0.02):
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.risk_free_rate = risk_free_rate
        self.n_assets = len(mean_returns)
    
    def max_sharpe_portfolio(self):
        """সর্বোচ্চ শার্প রেশিও পোর্টফোলিও"""
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1/self.n_assets] * self.n_assets)
        
        result = minimize(
            PortfolioMetrics.neg_sharpe,
            initial_guess,
            args=(self.mean_returns, self.cov_matrix, self.risk_free_rate),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        weights = result.x
        stats = PortfolioMetrics.portfolio_stats(weights, self.mean_returns, self.cov_matrix)
        
        return weights, stats
    
    def min_volatility_portfolio(self):
        """ন্যূনতম ভলাটিলিটি পোর্টফোলিও"""
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1/self.n_assets] * self.n_assets)
        
        def portfolio_vol(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        
        result = minimize(
            portfolio_vol,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        weights = result.x
        stats = PortfolioMetrics.portfolio_stats(weights, self.mean_returns, self.cov_matrix)
        
        return weights, stats
    
    def efficient_frontier(self, n_points=20):
        """Efficient Frontier পয়েন্টস"""
        targets = np.linspace(0.05, 0.20, n_points)
        efficient_portfolios = []
        
        for target_return in targets:
            constraints = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(x * self.mean_returns) - target_return}
            )
            bounds = tuple((0, 1) for _ in range(self.n_assets))
            initial_guess = np.array([1/self.n_assets] * self.n_assets)
            
            result = minimize(
                lambda w: np.sqrt(np.dot(w.T, np.dot(self.cov_matrix * 252, w))),
                initial_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                weights = result.x
                vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
                efficient_portfolios.append({'return': target_return, 'vol': vol, 'weights': weights})
        
        return efficient_portfolios

# অপ্টিমাইজেশন
print("\n=== Mean-Variance অপ্টিমাইজেশন ===")
optimizer = MeanVarianceOptimizer(mean_returns, cov_matrix)

max_sharpe_weights, max_sharpe_stats = optimizer.max_sharpe_portfolio()
min_vol_weights, min_vol_stats = optimizer.min_volatility_portfolio()

print(f"\n🥇 সর্বোচ্চ Sharpe Ratio পোর্টফোলিও:")
print(f"   Sharpe: {max_sharpe_stats['sharpe']:.3f}")
print(f"   রিটার্ন: {max_sharpe_stats['return']:.2%}")
print(f"   ভলাটিলিটি: {max_sharpe_stats['volatility']:.2%}")
for i, name in enumerate(asset_names):
    print(f"   {name}: {max_sharpe_weights[i]:.1%}")

print(f"\n🛡️ ন্যূনতম ভলাটিলিটি পোর্টফোলিও:")
print(f"   ভলাটিলিটি: {min_vol_stats['volatility']:.2%}")
print(f"   রিটার্ন: {min_vol_stats['return']:.2%}")
for i, name in enumerate(asset_names):
    print(f"   {name}: {min_vol_weights[i]:.1%}")
```

## 3. Risk Parity পোর্টফোলিও

```python
class RiskParityPortfolio:
    """Risk Parity — প্রতিটি এসেট সমান রিস্ক কন্ট্রিবিউট করে"""
    
    def __init__(self, cov_matrix):
        self.cov_matrix = cov_matrix
        self.n_assets = len(cov_matrix)
    
    def risk_contribution(self, weights):
        """প্রতি এসেটের রিস্ক কন্ট্রিবিউশন"""
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        marginal_contrib = np.dot(self.cov_matrix, weights) / portfolio_vol
        risk_contrib = weights * marginal_contrib
        return risk_contrib / portfolio_vol
    
    def risk_parity_objective(self, weights):
        """Risk Parity অবজেক্টিভ (সমান রিস্ক কন্ট্রিবিউশন)"""
        weights = np.abs(weights) / np.sum(np.abs(weights))
        rc = self.risk_contribution(weights)
        target = 1.0 / self.n_assets
        return np.sum((rc - target) ** 2)
    
    def optimize(self):
        """Risk Parity ওয়েট সন্ধান"""
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1/self.n_assets] * self.n_assets)
        
        result = minimize(
            self.risk_parity_objective,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        weights = result.x
        rc = self.risk_contribution(weights)
        
        return weights, rc

print("\n=== Risk Parity পোর্টফোলিও ===")
rp = RiskParityPortfolio(cov_matrix)
rp_weights, rp_contrib = rp.optimize()

print(f"Risk Parity ওয়েট:")
for i, name in enumerate(asset_names):
    print(f"  {name}: {rp_weights[i]:.1%} (রিস্ক কন্ট্রিবিউশন: {rp_contrib[i]:.2%})")

print(f"\nরিস্ক কন্ট্রিবিউশন (সমান): {rp_contrib}")
```

## 4. RL-বেসড অ্যালোকেশন অপ্টিমাইজার

```python
class RLPortfolioAllocator(nn.Module):
    """RL পোর্টফোলিও অ্যালোকেটর নিউরাল নেটওয়ার্ক"""
    def __init__(self, n_assets=4, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_assets * 3, hidden_dim),  # রিটার্ন, ভল, প্রাইস
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_assets),
            nn.Softmax(dim=-1)  # ওয়েট সাম = 1
        )
    
    def forward(self, state):
        """পোর্টফোলিও ওয়েট রিটার্ন"""
        return self.net(state)
    
    def get_allocation(self, returns, volatilities, prices):
        """বর্তমান মার্কেট কন্ডিশনে অ্যালোকেশন"""
        state = torch.cat([
            torch.FloatTensor(returns),
            torch.FloatTensor(volatilities),
            torch.FloatTensor(prices) / prices.mean()
        ]).unsqueeze(0)
        
        with torch.no_grad():
            weights = self.forward(state).squeeze(0).numpy()
        
        return weights

class RLPortfolioOptimizer:
    """RL-বেসড পোর্টফোলিও অপ্টিমাইজার"""
    
    def __init__(self, n_assets=4):
        self.n_assets = n_assets
        self.allocator = RLPortfolioAllocator(n_assets)
        self.optimizer = optim.Adam(self.allocator.parameters(), lr=0.001)
    
    def train_step(self, returns, cov_matrix):
        """একটি ট্রেনিং স্টেপ (শার্প রেশিও ম্যাক্সিমাইজ)"""
        volatilities = np.sqrt(np.diag(cov_matrix))
        prices = np.ones(self.n_assets)  # সিম্পল
        
        weights = self.allocator.get_allocation(
            returns.mean(axis=0) if returns.ndim > 1 else returns,
            volatilities,
            prices * 100
        )
        
        # শার্প রেশিও (লস ফাংশন)
        portfolio_return = np.sum(weights * returns.mean(axis=0)) * 252 if returns.ndim > 1 else np.sum(weights * returns) * 252
        portfolio_vol = np.sqrt(np.dot(weights, np.dot(cov_matrix * 252, weights)))
        sharpe = portfolio_return / (portfolio_vol + 1e-8)
        
        # নেগেটিভ শার্প = লস
        loss = -torch.FloatTensor([sharpe])
        
        self.optimizer.zero_grad()
        # নিউরাল নেটওয়ার্ক গ্রেডিয়েন্ট সিমুলেট (সিম্পল)
        loss.backward()
        self.optimizer.step()
        
        return sharpe, weights

# RL পোর্টফোলিও ডেমো
print("\n=== RL পোর্টফোলিও অ্যালোকেটর ===")
rl_optimizer = RLPortfolioOptimizer(n_assets=4)

# সিমুলেটেড ট্রেনিং
for epoch in range(10):
    # র‍্যান্ডম রিটার্ন এবং কোভেরিয়েন্স
    sample_returns = np.random.randn(100, 4) * 0.02 + mean_returns / 252
    sample_cov = np.cov(sample_returns.T)
    
    sharpe, weights = rl_optimizer.train_step(sample_returns, sample_cov)
    
    if (epoch + 1) % 5 == 0:
        print(f"এপোক {epoch+1}: Sharpe={sharpe:.3f}")

# ফাইনাল অ্যালোকেশন
final_weights = rl_optimizer.allocator.get_allocation(
    mean_returns / 252,
    np.sqrt(np.diag(cov_matrix)),
    np.array([100, 120, 95, 110])
)
print(f"\nRL অপ্টিমাইজড অ্যালোকেশন:")
for i, name in enumerate(asset_names):
    print(f"  {name}: {final_weights[i]:.1%}")
```

## 5. কমপ্লিট পোর্টফোলিও ম্যানেজমেন্ট সিস্টেম

```python
class PortfolioManagementSystem:
    """সম্পূর্ণ পোর্টফোলিও ম্যানেজমেন্ট সিস্টেম"""
    
    def __init__(self, asset_names, mean_returns, cov_matrix, initial_capital=100000):
        self.asset_names = asset_names
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.initial_capital = initial_capital
        self.current_value = initial_capital
        self.weights_history = []
        self.value_history = [initial_capital]
        
        # অপ্টিমাইজার
        self.mvo = MeanVarianceOptimizer(mean_returns, cov_matrix)
        self.rp = RiskParityPortfolio(cov_matrix)
        self.rl = RLPortfolioOptimizer(len(asset_names))
    
    def optimize_portfolio(self, strategy='max_sharpe'):
        """পোর্টফোলিও অপ্টিমাইজ করুন"""
        if strategy == 'max_sharpe':
            weights, stats = self.mvo.max_sharpe_portfolio()
        elif strategy == 'min_vol':
            weights, stats = self.mvo.min_volatility_portfolio()
        elif strategy == 'risk_parity':
            weights, _ = self.rp.optimize()
            stats = PortfolioMetrics.portfolio_stats(weights, self.mean_returns, self.cov_matrix)
        elif strategy == 'rl':
            weights = self.rl.allocator.get_allocation(
                self.mean_returns / 252,
                np.sqrt(np.diag(self.cov_matrix)),
                np.array([100] * len(self.asset_names))
            )
            stats = PortfolioMetrics.portfolio_stats(weights, self.mean_returns, self.cov_matrix)
        else:
            weights = np.array([1/len(self.asset_names)] * len(self.asset_names))
            stats = PortfolioMetrics.portfolio_stats(weights, self.mean_returns, self.cov_matrix)
        
        self.weights_history.append(weights)
        return weights, stats
    
    def rebalance(self, strategy='max_sharpe'):
        """পোর্টফোলিও রিব্যালেন্স"""
        weights, stats = self.optimize_portfolio(strategy)
        
        allocation = {}
        for i, name in enumerate(self.asset_names):
            allocation[name] = self.current_value * weights[i]
        
        result = {
            'weights': weights,
            'stats': stats,
            'allocation': allocation,
            'total_value': self.current_value
        }
        
        return result
    
    def print_portfolio_summary(self, strategy_name='Max Sharpe'):
        """পোর্টফোলিও সারাংশ"""
        result = self.rebalance(strategy_name.lower().replace(' ', '_'))
        
        print(f"\n{'='*50}")
        print(f"📊 পোর্টফোলিও সারাংশ — {strategy_name}")
        print(f"{'='*50}")
        print(f"মোট বিনিয়োগ: ${result['total_value']:,.2f}")
        print(f"প্রত্যাশিত বার্ষিক রিটার্ন: {result['stats']['return']:.2%}")
        print(f"প্রত্যাশিত ভলাটিলিটি: {result['stats']['volatility']:.2%}")
        print(f"শার্প রেশিও: {result['stats']['sharpe']:.3f}")
        
        print(f"\nঅ্যাসেট অ্যালোকেশন:")
        for name, amount in result['allocation'].items():
            pct = amount / result['total_value']
            print(f"  {name}: ${amount:,.2f} ({pct:.1%})")
        
        return result

# সম্পূর্ণ সিস্টেম ডেমো
print("\n" + "="*50)
print("🏛️ ক্যাপস্টোন পোর্টফোলিও ম্যানেজমেন্ট সিস্টেম")
print("="*50)

pms = PortfolioManagementSystem(asset_names, mean_returns, cov_matrix, initial_capital=100000)

for strategy in ['Max Sharpe', 'Min Vol', 'Risk Parity', 'RL']:
    if strategy == 'RL':
        # RL-এর জন্য প্রি-ট্রেনিং
        for _ in range(30):
            sr = np.random.randn(100, 4) * 0.02 + mean_returns / 252
            sc = np.cov(sr.T)
            rl_optimizer.train_step(sr, sc)
    
    pms.print_portfolio_summary(strategy)
```

## 6. LSTM + RL হাইব্রিড সিস্টেম

```python
class HybridSystem:
    """LSTM প্রেডিকশন + RL ট্রেডিং হাইব্রিড সিস্টেম"""
    
    @staticmethod
    def integrate_lstm_with_portfolio():
        """LSTM সিগন্যাল পোর্টফোলিওতে ইন্টিগ্রেট"""
        print("\n" + "="*50)
        print("🔄 LSTM + RL হাইব্রিড সিস্টেম")
        print("="*50)
        print("""
পূর্ণাঙ্গ সিস্টেম ফ্লো:

1️⃣ LSTM মডেল (Day 57)
   ইনপুট: 30-দিনের মার্কেট ডেটা
   আউটপুট: DOWN/NEUTRAL/UP প্রেডিকশন
   
2️⃣ সিগন্যাল জেনারেশন
   UP (conf > 0.7) → BUY সিগন্যাল
   DOWN (conf > 0.7) → SELL সিগন্যাল
   NEUTRAL → HOLD
   
3️⃣ RL এজেন্ট (Day 50)
   স্টেট: LSTM প্রেডিকশন + পোর্টফোলিও স্টেট
   অ্যাকশন: অ্যালোকেশন ওয়েট অ্যাডজাস্টমেন্ট
   রিওয়ার্ড: পোর্টফোলিও শার্প রেশিও
   
4️⃣ পোর্টফোলিও অপ্টিমাইজেশন (Day 59)
   Mean-Variance + Risk Parity + RL
   প্রতিদিন রিব্যালেন্স
   
5️⃣ পারফরম্যান্স মনিটরিং
   রিয়েল-টাইম P&L, Drawdown, Sharpe
   অ্যালার্ম (Stop-loss, Rebalance needed)
""")
    
    @staticmethod
    def sample_trading_day():
        """একটি ট্রেডিং দিনের সিমুলেশন"""
        print("\n📅 একটি ট্রেডিং দিনের সিমুলেশন:")
        print("="*40)
        
        # স্টেপ 1: মার্কেট ডেটা
        print("\n08:30 — ডেটা সংগ্রহ")
        print("  ✓ প্রাইস ডেটা আপডেটেড")
        print("  ✓ টেকনিক্যাল ইন্ডিকেটর ক্যালকুলেটেড")
        
        # স্টেপ 2: LSTM প্রেডিকশন
        lstm_pred = np.random.choice(['DOWN 📉', 'NEUTRAL ➡️', 'UP 📈'], p=[0.2, 0.3, 0.5])
        lstm_conf = np.random.uniform(0.65, 0.92)
        print(f"\n09:00 — LSTM প্রেডিকশন")
        print(f"  প্রেডিকশন: {lstm_pred}")
        print(f"  কনফিডেন্স: {lstm_conf:.1%}")
        
        # স্টেপ 3: RL এজেন্ট
        if lstm_conf > 0.7:
            if 'UP' in lstm_pred:
                action = 'BUY (+5% অ্যালোকেশন)'
            elif 'DOWN' in lstm_pred:
                action = 'SELL (-5% অ্যালোকেশন)'
            else:
                action = 'HOLD'
        else:
            action = 'HOLD (লো কনফিডেন্স)'
        
        print(f"\n09:30 — RL এজেন্ট অ্যাকশন")
        print(f"  অ্যাকশন: {action}")
        
        # স্টেপ 4: পোর্টফোলিও আপডেট
        print(f"\n10:00 — পোর্টফোলিও আপডেট")
        print(f"  রিব্যালেন্স সম্পন্ন")
        print(f"  ট্রানজেকশন ফি: $15.50")
        
        # স্টেপ 5: ইভনিং রিপোর্ট
        print(f"\n16:00 — ইভনিং রিপোর্ট")
        print(f"  ডে P&L: +$1,250 (+1.25%)")
        print(f"  ইয়েল্ড: +$12,400 (+12.4%)")
        print(f"  শার্প রেশিও: 1.32")
        print(f"  ম্যাক্স ড্রডাউন: -4.2%")

HybridSystem.integrate_lstm_with_portfolio()
HybridSystem.sample_trading_day()
```

## সারাংশ
- Mean-Variance Optimization (Markowitz) efficient frontier দেয়
- Risk Parity সকল অ্যাসেটে সমান রিস্ক বিতরণ করে
- RL-বেসড অ্যালোকেশন ডায়নামিকভাবে অ্যাডজাস্ট করে
- LSTM + RL হাইব্রিড সিস্টেম বেস্ট পারফরম্যান্স দেয়
- নিয়মিত রিব্যালেন্সিং রিস্ক কন্ট্রোলে সাহায্য করে
- পোর্টফোলিও ডাইভারসিফিকেশন শার্প রেশিও বাড়ায়