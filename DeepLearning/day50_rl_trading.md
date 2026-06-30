# Day 50: RL ফর ট্রেডিং — প্র্যাকটিক্যাল অ্যাপ্লিকেশন 📊💰

## RL-বেসড ট্রেডিং সিস্টেম
RL ট্রেডিংয়ের জন্য প্রাকটিক্যাল ফ্রেমওয়ার্ক — মার্কেট ডেটা, রিওয়ার্ড ইঞ্জিনিয়ারিং, রিস্ক ম্যানেজমেন্ট।

### RL ট্রেডিং কম্পোনেন্টস
1. **এনভায়রনমেন্ট**: মার্কেট সিমুলেশন (প্রাইস, অর্ডার বুক, ফি)
2. **স্টেট**: টেকনিক্যাল ইন্ডিকেটর + পোর্টফোলিও স্টেট
3. **অ্যাকশন**: BUY/SELL/HOLD বা কন্টিনিউয়াস সাইজ
4. **রিওয়ার্ড**: P&L, Sharpe Ratio, Sortino Ratio
5. **রিস্ক ম্যানেজমেন্ট**: Stop-loss, Position Sizing

### চ্যালেঞ্জেস
- মার্কেট নন-স্টেশনারিটি
- ট্রানজেকশন কস্ট
- স্লিপেজ
- ওভারফিটিং (বিশেষত ব্যাকটেস্টে)
- পার্টিয়ালি অবজার্ভেবল স্টেট

## RL ট্রেডিং ফ্রেমওয়ার্ক

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
random.seed(42)
```

## 1. অ্যাডভান্সড ট্রেডিং এনভায়রনমেন্ট

```python
class AdvancedTradingEnv:
    """অ্যাডভান্সড ট্রেডিং এনভায়রনমেন্ট (ফি, স্লিপেজ, রিস্ক সহ)"""
    def __init__(self, prices, initial_balance=10000, 
                 transaction_fee=0.001, slippage=0.0005,
                 max_position=10, stop_loss=0.02):
        
        self.prices = prices
        self.initial_balance = initial_balance
        self.transaction_fee = transaction_fee
        self.slippage = slippage
        self.max_position = max_position
        self.stop_loss = stop_loss
        
        # ফিচার ক্যালকুলেশন
        self.returns = np.diff(prices) / prices[:-1]
        self.volatility = self._compute_volatility(20)
        self.sma_20 = self._compute_sma(20)
        self.sma_50 = self._compute_sma(50)
        
        self.reset()
    
    def _compute_volatility(self, window):
        """রোলিং ভলাটিলিটি"""
        vol = np.zeros(len(self.prices))
        for i in range(window, len(self.prices)):
            vol[i] = np.std(self.returns[i-window:i])
        return vol
    
    def _compute_sma(self, window):
        """রোলিং সিম্পল মুভিং এভারেজ"""
        sma = np.zeros(len(self.prices))
        for i in range(window, len(self.prices)):
            sma[i] = np.mean(self.prices[i-window:i])
        return sma
    
    def reset(self):
        """এনভায়রনমেন্ট রিসেট"""
        self.balance = self.initial_balance
        self.shares = 0
        self.idx = 50  # ফিচার উইন্ডোর জন্য
        self.entry_price = 0
        self.peak_value = self.initial_balance
        self.total_reward = 0
        self.trades = []
        
        return self._get_state()
    
    def _get_state(self):
        """স্টেট: 8 ডাইমেনশনাল"""
        if self.idx < 50:
            return np.zeros(8, dtype=np.float32)
        
        current_price = self.prices[self.idx]
        
        state = np.array([
            self.balance / self.initial_balance,        # ব্যালেন্স রেশিও
            self.shares / self.max_position,             # পজিশন সাইজ
            self.returns[self.idx-1] if self.idx > 0 else 0,  # লাস্ট রিটার্ন
            self.volatility[self.idx] * 100,              # ভলাটিলিটি
            current_price / self.sma_20[self.idx] - 1,    # SMA20 ডিভিয়েশন
            self.sma_20[self.idx] / self.sma_50[self.idx] - 1 if self.sma_50[self.idx] > 0 else 0,  # SMA ক্রস
            (current_price - self.entry_price) / (self.entry_price + 1e-6) if self.shares > 0 else 0,  # P&L %
            self.idx / len(self.prices)                   # টাইম ডিসকাউন্ট
        ], dtype=np.float32)
        
        return np.clip(state, -3, 3)
    
    def step(self, action):
        """অ্যাকশন নেওয়া
        0: HOLD, 1: BUY 25%, 2: BUY 50%, 3: BUY 100%, 
        4: SELL 25%, 5: SELL 50%, 6: SELL 100%
        """
        current_price = self.prices[self.idx]
        prev_value = self.balance + self.shares * current_price
        
        # অ্যাকশন এক্সিকিউট
        if action >= 1 and action <= 3:  # BUY
            fraction = [0, 0.25, 0.50, 1.0][action]
            cost = self.balance * fraction
            if cost >= current_price and self.shares < self.max_position:
                max_shares = min(int(cost / current_price), 
                               self.max_position - self.shares)
                if max_shares > 0:
                    # ফি ও স্লিপেজ
                    actual_price = current_price * (1 + self.slippage)
                    fee = max_shares * actual_price * self.transaction_fee
                    
                    if cost >= max_shares * actual_price + fee:
                        self.balance -= max_shares * actual_price + fee
                        self.shares += max_shares
                        self.entry_price = current_price if self.shares == max_shares else self.entry_price
                        self.trades.append(('BUY', current_price, max_shares))
        
        elif action >= 4 and action <= 6:  # SELL
            fraction = [0, 0.25, 0.50, 1.0][action-3]
            shares_to_sell = max(1, int(self.shares * fraction))
            if self.shares >= shares_to_sell:
                actual_price = current_price * (1 - self.slippage)
                fee = shares_to_sell * actual_price * self.transaction_fee
                self.balance += shares_to_sell * actual_price - fee
                self.shares -= shares_to_sell
                self.trades.append(('SELL', current_price, shares_to_sell))
                if self.shares == 0:
                    self.entry_price = 0
        
        # নেক্সট স্টেপ
        self.idx += 1
        done = self.idx >= len(self.prices) - 1
        
        # স্টপ-লস চেক
        if self.shares > 0 and self.entry_price > 0:
            unrealized_pnl = (current_price - self.entry_price) / self.entry_price
            if unrealized_pnl < -self.stop_loss:
                # ফোর্সড ক্লোজ (স্টপ-লস)
                self.balance += self.shares * current_price * (1 - self.slippage)
                self.shares = 0
                self.trades.append(('STOP_LOSS', current_price, self.shares))
        
        # রিওয়ার্ড
        current_value = self.balance + self.shares * current_price
        
        if done:
            reward = (current_value - self.initial_balance) / self.initial_balance
        else:
            # ডিফারেনশিয়াল শেপ রেশিও এপ্রোক্সিমেশন
            reward = np.tanh((current_value - prev_value) / prev_value * 100)
        
        self.total_reward += reward
        self.peak_value = max(self.peak_value, current_value)
        
        next_state = self._get_state() if not done else np.zeros(8)
        return next_state, reward, done, {'value': current_value}

# সিম্পল টেস্ট
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(300) * 0.5)
env = AdvancedTradingEnv(prices)
state = env.reset()
print(f"এনভায়রনমেন্ট তৈরি: {len(prices)} প্রাইস পয়েন্ট")
print(f"স্টেট সাইজ: {len(state)}")
print(f"অ্যাকশন সাইজ: 7 (HOLD, BUY 3, SELL 3)")
```

## 2. PPO ট্রেডিং এজেন্ট

```python
class PPOActorCritic(nn.Module):
    """PPO Actor-Critic নেটওয়ার্ক"""
    def __init__(self, state_dim=8, action_dim=7, hidden_dim=128):
        super().__init__()
        
        self.shared = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        self.actor = nn.Linear(hidden_dim, action_dim)
        self.critic = nn.Linear(hidden_dim, 1)
    
    def forward(self, state):
        x = self.shared(state)
        logits = self.actor(x)
        value = self.critic(x)
        return logits, value
    
    def get_action(self, state, deterministic=False):
        with torch.no_grad():
            logits, value = self.forward(state)
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            
            if deterministic:
                action = torch.argmax(probs, dim=-1)
            else:
                action = dist.sample()
            
            log_prob = dist.log_prob(action)
            return action.item(), log_prob.item(), value.item()

class PPOTrader:
    """PPO ট্রেডিং এজেন্ট"""
    def __init__(self, state_dim=8, action_dim=7, lr=3e-4, gamma=0.99,
                 clip_epsilon=0.2, epochs=10, batch_size=64):
        
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.epochs = epochs
        self.batch_size = batch_size
        
        self.policy = PPOActorCritic(state_dim, action_dim).to(device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        
        self.buffer = []  # (state, action, reward, done, log_prob, value)
    
    def get_action(self, state):
        return self.policy.get_action(
            torch.FloatTensor(state).unsqueeze(0).to(device)
        )
    
    def store_transition(self, state, action, reward, done, log_prob, value):
        self.buffer.append((state, action, reward, done, log_prob, value))
    
    def learn(self):
        """PPO আপডেট"""
        if len(self.buffer) < 10:
            return None
        
        states, actions, rewards, dones, log_probs, values = zip(*self.buffer)
        
        # GAE ক্যালকুলেশন
        returns = []
        advantages = []
        G = 0
        adv = 0
        
        for r, d, v in zip(reversed(rewards), reversed(dones), reversed(values)):
            G = r + self.gamma * G * (1 - d)
            returns.insert(0, G)
            
            td_error = r + self.gamma * v * (1 - d) - v
            adv = td_error + self.gamma * 0.95 * adv * (1 - d)
            advantages.insert(0, adv)
        
        returns = torch.FloatTensor(returns).to(device)
        advantages = torch.FloatTensor(advantages).to(device)
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        states = torch.FloatTensor(np.array(states)).to(device)
        actions = torch.LongTensor(actions).to(device)
        old_log_probs = torch.FloatTensor(log_probs).to(device)
        
        total_loss = 0
        
        for _ in range(self.epochs):
            logits, values = self.policy(states)
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            new_log_probs = dist.log_prob(actions)
            entropy = dist.entropy().mean()
            
            # PPO clip
            ratio = torch.exp(new_log_probs - old_log_probs)
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 
                               1 + self.clip_epsilon) * advantages
            actor_loss = -torch.min(surr1, surr2).mean()
            
            critic_loss = F.mse_loss(values.squeeze(), returns)
            
            loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        self.buffer = []
        return total_loss / self.epochs

import torch.nn.functional as F
```

## 3. সম্পূর্ণ ট্রেডিং সিস্টেম ট্রেনিং

```python
class RLTradingSystem:
    """সম্পূর্ণ RL ট্রেডিং সিস্টেম"""
    def __init__(self, prices):
        self.prices = prices
        self.env = AdvancedTradingEnv(prices)
        self.agent = PPOTrader(state_dim=8, action_dim=7)
        self.eval_env = AdvancedTradingEnv(prices.copy())
    
    def train(self, episodes=100):
        """ট্রেনিং"""
        results = []
        
        for ep in range(episodes):
            state = self.env.reset()
            done = False
            total_reward = 0
            
            while not done:
                action, log_prob, value = self.agent.get_action(state)
                next_state, reward, done, info = self.env.step(action)
                
                self.agent.store_transition(
                    state, action, reward, done, log_prob, value
                )
                
                total_reward += reward
                state = next_state
            
            loss = self.agent.learn()
            results.append(total_reward)
            
            if (ep + 1) % 20 == 0:
                avg_reward = np.mean(results[-20:])
                print(f"এপিসোড {ep+1}/{episodes}: "
                      f"গড় রিওয়ার্ড={avg_reward:.4f}, "
                      f"লস={loss:.4f}" if loss else
                      f"গড় রিওয়ার্ড={avg_reward:.4f}")
        
        return results
    
    def evaluate(self):
        """ইভালুয়েশন (ডিটারমিনিস্টিক)"""
        state = self.eval_env.reset()
        done = False
        total_reward = 0
        values = [self.eval_env.initial_balance]
        
        while not done:
            action, _, _ = self.agent.get_action(state, deterministic=True)
            next_state, reward, done, info = self.eval_env.step(action)
            total_reward += reward
            values.append(info['value'])
            state = next_state
        
        print("\n=== ইভালুয়েশন রেজাল্টস ===")
        print(f"ফাইনাল ভ্যালু: ${values[-1]:.2f}")
        print(f"টোটাল রিটার্ন: {(values[-1] - 10000)/10000:.2%}")
        print(f"মোট ট্রেড: {len(self.eval_env.trades)}")
        print(f"ড্রডাউন: {(1 - min(values)/max(values)):.2%}")
        
        # শার্প রেশিও এপ্রক্সিমেশন
        daily_returns = np.diff(values) / values[:-1]
        sharpe = np.mean(daily_returns) / (np.std(daily_returns) + 1e-6) * np.sqrt(252)
        print(f"শার্প রেশিও (এপ্রক্স): {sharpe:.2f}")
        
        return values

# ডেমো
print("\n=== RL ট্রেডিং সিস্টেম ট্রেনিং ===")
system = RLTradingSystem(prices)
rewards = system.train(episodes=60)
values = system.evaluate()
```

## 4. রিস্ক ম্যানেজমেন্ট ফিচারস

```python
class RiskManagement:
    """ট্রেডিং রিস্ক ম্যানেজমেন্ট"""
    
    @staticmethod
    def kelly_criterion(win_prob, win_loss_ratio):
        """Kelly Criterion — অপ্টিমাল পজিশন সাইজ"""
        f = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio
        return max(0, min(f, 0.25))  # 25% ক্যাপ
    
    @staticmethod
    def var(returns, confidence=0.95):
        """Value at Risk"""
        return np.percentile(returns, (1 - confidence) * 100)
    
    @staticmethod
    def cvar(returns, confidence=0.95):
        """Conditional VaR (Expected Shortfall)"""
        var = RiskManagement.var(returns, confidence)
        return returns[returns <= var].mean()
    
    @staticmethod
    def calculate_metrics(equity_curve, risk_free_rate=0.02):
        """পারফরম্যান্স মেট্রিক্স"""
        returns = np.diff(equity_curve) / equity_curve[:-1]
        
        metrics = {
            'total_return': (equity_curve[-1] / equity_curve[0] - 1),
            'volatility': np.std(returns) * np.sqrt(252),
            'sharpe_ratio': (np.mean(returns) - risk_free_rate/252) / (np.std(returns) + 1e-6) * np.sqrt(252),
            'max_drawdown': np.min(equity_curve / np.maximum.accumulate(equity_curve) - 1),
            'win_rate': np.mean(returns > 0),
            'var_95': RiskManagement.var(returns, 0.95),
            'cvar_95': RiskManagement.cvar(returns, 0.95)
        }
        
        return metrics

print("\n=== Risk Management উদাহরণ ===")
metrics = RiskManagement.calculate_metrics(values)
for key, val in metrics.items():
    print(f"{key}: {val:.4f}")
```

## 5. লাইভ ট্রেডিং সিমুলেশন

```python
def live_trading_simulation(agent, prices, window=100):
    """লাইভ ট্রেডিং সিমুলেশন (রিয়েল-টাইম আপডেট)"""
    
    env = AdvancedTradingEnv(prices[:window])
    state = env.reset()
    predictions = []
    
    print("\n=== লাইভ ট্রেডিং সিমুলেশন ===")
    
    for i in range(window, len(prices)):
        # অ্যাকশন নিন
        action, _, _ = agent.get_action(state, deterministic=True)
        next_state, reward, done, info = env.step(action)
        
        predictions.append({
            'price': prices[i],
            'action': ['HOLD', 'BUY25', 'BUY50', 'BUY100', 'SELL25', 'SELL50', 'SELL100'][action],
            'value': info['value']
        })
        
        if (i + 1) % 150 == 0:
            print(f"স্টেপ {i+1}: প্রাইস={prices[i]:.2f}, "
                  f"ভ্যালু=${info['value']:.2f}, "
                  f"অ্যাকশন={predictions[-1]['action']}")
        
        state = next_state
        if done:
            break
    
    final_return = (predictions[-1]['value'] - 10000) / 10000
    print(f"\nসিমুলেশন শেষ: রিটার্ন = {final_return:.2%}")
    
    return predictions

# সিমুলেশন
preds = live_trading_simulation(system.agent, prices)
```

## সারাংশ
- RL ট্রেডিং সিস্টেমে মার্কেট এনভায়রনমেন্ট, স্টেট, অ্যাকশন, রিওয়ার্ড প্রয়োজন
- ট্রানজেকশন ফি, স্লিপেজ, স্টপ-লস রিয়ালিস্টিক সিমুলেশনের জন্য অপরিহার্য
- PPO প্র্যাকটিক্যাল RL ট্রেডিংয়ের জন্য ভাল পছন্দ
- রিস্ক ম্যানেজমেন্ট (Kelly Criterion, VaR, Drawdown) অত্যন্ত গুরুত্বপূর্ণ
- ওভারফিটিং মার্কেট ডেটার সবচেয়ে বড় চ্যালেঞ্জ
- ব্যাকটেস্ট এবং আউট-অফ-স্যাম্পল টেস্টিং অপরিহার্য