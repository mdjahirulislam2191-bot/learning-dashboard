# Day 49: পলিসি গ্রেডিয়েন্টস 📈🎯

## পলিসি গ্রেডিয়েন্টস কী?
পলিসি গ্রেডিয়েন্ট মেথড সরাসরি পলিসি π(a|s) অপ্টিমাইজ করে, Q-ভ্যালু না শিখে।

### ভ্যালু-বেসড vs পলিসি-বেসড
| ভ্যালু-বেসড (DQN) | পলিসি-বেসড |
|---|---|
| Q(s,a) শেখে | সরাসরি π(a|s) শেখে |
| ডিটারমিনিস্টিক পলিসি | স্টোকাস্টিক পলিসি |
| ডিসক্রিট অ্যাকশন | কন্টিনিউয়াস অ্যাকশনও সম্ভব |
| অফ-পলিসি | অন-পলিসি |

### পলিসি গ্রেডিয়েন্ট থিওরেম
∇J(θ) = 𝔼[∇ log π(a|s) · G]

যেখানে G = Σ γᵗ · rₜ (ডিসকাউন্টেড রিটার্ন)

### ফিন্যান্সে পলিসি গ্রেডিয়েন্টস
- কন্টিনিউয়াস ট্রেডিং সাইজ অপ্টিমাইজেশন
- রিয়েল-টাইম পোর্টফোলিও অ্যালোকেশন
- রিস্ক-অ্যাডজাস্টেড ট্রেডিং স্ট্রাটেজি
- মার্কেট মেকিং

## REINFORCE অ্যালগরিদম

```python
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. পলিসি নেটওয়ার্ক

```python
class PolicyNetwork(nn.Module):
    """পলিসি নেটওয়ার্ক (Gaussian Policy for continuous)"""
    def __init__(self, state_dim=4, action_dim=3, hidden_dim=128):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # ডিসক্রিট অ্যাকশনের জন্য
        self.action_head = nn.Linear(hidden_dim, action_dim)
        
        # কন্টিনিউয়াস অ্যাকশনের জন্য (মিউ + লগ স্টিডি)
        self.mu_head = nn.Linear(hidden_dim, action_dim)
        self.log_std = nn.Parameter(torch.zeros(action_dim))
    
    def forward(self, state):
        """লগিট প্রোবাবিলিটি রিটার্ন"""
        x = self.shared(state)
        logits = self.action_head(x)
        return logits
    
    def get_action(self, state, deterministic=False):
        """পলিসি অনুযায়ী অ্যাকশন নিন"""
        with torch.no_grad():
            logits = self.forward(state)
            
            if deterministic:
                return torch.argmax(logits, dim=-1).item()
            
            # স্টোকাস্টিক স্যাম্পলিং
            probs = F.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            
            return action.item(), dist.log_prob(action)

# ডেমো
policy_net = PolicyNetwork(state_dim=4, action_dim=3).to(device)
dummy_state = torch.FloatTensor(np.random.randn(1, 4)).to(device)
action, log_prob = policy_net.get_action(dummy_state)
print(f"পলিসি নেটওয়ার্ক: state→action")
print(f"ইনপুট স্টেট: {dummy_state.cpu().numpy().flatten()}")
print(f"সিলেক্টেড অ্যাকশন: {action}, লগ-প্রব: {log_prob.item():.3f}")
```

## 2. REINFORCE এজেন্ট

```python
class REINFORCEAgent:
    """REINFORCE (Monte Carlo Policy Gradient) এজেন্ট"""
    def __init__(self, state_dim=4, action_dim=3, hidden_dim=128,
                 lr=0.001, gamma=0.99):
        self.gamma = gamma
        self.policy = PolicyNetwork(state_dim, action_dim, hidden_dim).to(device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        
        # এপিসোড বাফার
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
    
    def store_transition(self, state, action, reward, log_prob):
        """এপিসোড ডেটা সংরক্ষণ"""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.log_probs.append(log_prob)
    
    def get_action(self, state):
        """পলিসি অনুযায়ী অ্যাকশন"""
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
            action, log_prob = self.policy.get_action(state_tensor)
            return action, log_prob
    
    def learn(self):
        """REINFORCE আপডেট"""
        if len(self.rewards) == 0:
            return None
        
        # ডিসকাউন্টেড রিটার্ন গণনা
        returns = []
        G = 0
        for r in reversed(self.rewards):
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns).to(device)
        
        # নরমালাইজেশন (ভ্যারিয়েন্স রিডাকশন)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # পলিসি গ্রেডিয়েন্ট আপডেট
        policy_loss = []
        for log_prob, G in zip(self.log_probs, returns):
            policy_loss.append(-log_prob * G)
        
        self.optimizer.zero_grad()
        policy_loss = torch.cat(policy_loss).sum()
        policy_loss.backward()
        self.optimizer.step()
        
        loss_value = policy_loss.item()
        
        # বাফার ক্লিয়ার
        self.clear_buffer()
        
        return loss_value
    
    def clear_buffer(self):
        """এপিসোড বাফার ক্লিয়ার"""
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []

# ডেমো তৈরি
agent = REINFORCEAgent(state_dim=4, action_dim=3)
print(f"REINFORCE এজেন্ট তৈরি: state=4, action=3")
# টেস্ট অ্যাকশন
test_state = np.random.randn(4)
action, log_prob = agent.get_action(test_state)
print(f"টেস্ট অ্যাকশন: {action}")
```

## 3. ট্রেডিং REINFORCE

```python
class TradingREINFORCE:
    """ফিন্যান্সিয়াল ট্রেডিংয়ের জন্য REINFORCE"""
    def __init__(self, prices):
        self.prices = prices
        self.state_dim = 5
        self.action_dim = 3  # HOLD(0), BUY(1), SELL(2)
        
        self.agent = REINFORCEAgent(
            state_dim=self.state_dim,
            action_dim=self.action_dim,
            hidden_dim=64,
            lr=0.001,
            gamma=0.99
        )
    
    def _get_state(self, idx, balance, holdings):
        """স্টেট ইঞ্জিনিয়ারিং"""
        if idx < 5:
            return np.zeros(self.state_dim, dtype=np.float32)
        
        current_price = self.prices[idx]
        past_prices = self.prices[idx-5:idx]
        
        # ফিচারস
        returns = np.diff(past_prices) / (past_prices[:-1] + 1e-6)
        volatility = np.std(returns) if len(returns) > 0 else 0
        momentum = (current_price - past_prices[0]) / (past_prices[0] + 1e-6)
        
        sma_20 = np.mean(self.prices[max(0, idx-20):idx+1])
        price_to_sma = (current_price - sma_20) / (sma_20 + 1e-6)
        
        returns_mean = np.mean(returns) if len(returns) > 0 else 0
        
        state = np.array([
            balance / 10000,
            holdings / 10,
            returns_mean,
            volatility * 10,
            price_to_sma
        ], dtype=np.float32)
        
        return np.clip(state, -3, 3)
    
    def train(self, episodes=200):
        """REINFORCE ট্রেনিং"""
        episode_rewards = []
        episode_losses = []
        
        for ep in range(episodes):
            balance = 10000
            holdings = 0
            idx = 5
            done = False
            total_reward = 0
            
            while not done and idx < len(self.prices) - 1:
                state = self._get_state(idx, balance, holdings)
                action, log_prob = self.agent.get_action(state)
                
                price = self.prices[idx]
                prev_balance = balance
                
                # অ্যাকশন এক্সিকিউট
                if action == 1 and balance >= price:  # BUY
                    shares = int(balance * 0.3 / price)
                    if shares > 0:
                        holdings += shares
                        balance -= shares * price
                
                elif action == 2 and holdings > 0:  # SELL
                    balance += holdings * price
                    holdings = 0
                
                idx += 1
                done = idx >= len(self.prices) - 1
                
                # রিওয়ার্ড
                if done:
                    final_value = balance + holdings * self.prices[-1]
                    reward = (final_value - 10000) / 10000
                else:
                    portfolio_change = (balance - prev_balance) / 10000
                    reward = np.clip(portfolio_change, -0.05, 0.05)
                
                self.agent.store_transition(state, action, reward, log_prob)
                total_reward += reward
            
            # এপিসোড শেষে লার্ন
            loss = self.agent.learn()
            episode_rewards.append(total_reward)
            if loss is not None:
                episode_losses.append(loss)
            
            if (ep + 1) % 40 == 0:
                avg_reward = np.mean(episode_rewards[-40:])
                avg_loss = np.mean(episode_losses[-40:]) if episode_losses else 0
                print(f"এপিসোড {ep+1}/{episodes}: "
                      f"রিওয়ার্ড={avg_reward:.4f}, "
                      f"লস={avg_loss:.4f}")
        
        return episode_rewards

# ডেমো
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(400) * 0.5)

print("=== REINFORCE ট্রেডিং ট্রেনিং ===")
reinforce_trader = TradingREINFORCE(prices)
rewards = reinforce_trader.train(episodes=120)
print(f"\nট্রেনিং সম্পন্ন! শেষ গড় রিওয়ার্ড: {np.mean(rewards[-20:]):.4f}")
```

## 4. পলিসি গ্রেডিয়েন্ট ভ্যারিয়েন্টস

```python
class PolicyGradientVariants:
    """পলিসি গ্রেডিয়েন্টের বিভিন্ন ভ্যারিয়েন্ট"""
    
    @staticmethod
    def reinforce_with_baseline():
        """REINFORCE with baseline (ভ্যারিয়েন্স রিডাকশন)"""
        print("=== REINFORCE with Baseline ===")
        print("∇J = 𝔼[∇log π(a|s) · (G - b(s))]")
        print("b(s) = V(s) (স্টেট-ভ্যালু ফাংশন)")
        print("ভ্যারিয়েন্স কমায়, বায়াস কমায়")
        print()
    
    @staticmethod
    def actor_critic():
        """Actor-Critic মেথড"""
        print("=== Actor-Critic ===")
        print("Actor: π(a|s) — পলিসি নেটওয়ার্ক")
        print("Critic: V(s) or Q(s,a) — ভ্যালু নেটওয়ার্ক")
        print("∇J = 𝔼[∇log π(a|s) · (r + γV(s') - V(s))]")
        print("TD Error এডভান্টেজ হিসেবে কাজ করে")
        print()
    
    @staticmethod
    def ppo():
        """PPO (Proximal Policy Optimization)"""
        print("=== PPO ===")
        print("প্রধান আইডিয়া: পলিসি আপডেট খুব বড় না হওয়া")
        print("Clipped surrogate objective:")
        print("L = min(ratio · A, clip(ratio, 1-ε, 1+ε) · A)")
        print("ratio = π_θ(a|s) / π_θ_old(a|s)")
        print("ট্রেনিং স্টেবল এবং সিম্পল")
        print()
    
    @staticmethod
    def sac():
        """SAC (Soft Actor-Critic)"""
        print("=== SAC ===")
        print("ম্যাক্সিমাম এনট্রপি RL ফ্রেমওয়ার্ক")
        print("এক্সপ্লোরেশন এনকোরেজ করে")
        print("J = Σ 𝔼[r + α·H(π(·|s))]")
        print("α = টেম্পারেচার প্যারামিটার (এনট্রপি ওয়েট)")

variants = PolicyGradientVariants()
variants.reinforce_with_baseline()
variants.actor_critic()
variants.ppo()
variants.sac()
```

## 5. ফিন্যান্সিয়াল পলিসি গ্রেডিয়েন্ট অ্যানালাইসিস

```python
def analyze_policy(policy_net, n_samples=100):
    """পলিসি অ্যানালাইসিস"""
    policy_net.eval()
    
    # বিভিন্ন স্টেটের জন্য পলিসি আউটপুট
    print("=== পলিসি অ্যানালাইসিস ===")
    
    # টেস্ট স্টেট জেনারেট
    test_states = []
    for i in range(5):
        state = np.array([
            np.random.uniform(0.5, 1.5),  # balance ratio
            np.random.uniform(0, 0.5),    # holdings ratio
            np.random.uniform(-0.05, 0.05), # return
            np.random.uniform(0, 0.02),   # volatility
            np.random.uniform(-0.1, 0.1)  # price_to_sma
        ], dtype=np.float32)
        test_states.append(state)
    
    with torch.no_grad():
        for i, state in enumerate(test_states):
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
            logits = policy_net(state_tensor)
            probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
            
            print(f"স্টেট {i+1}: HOLD={probs[0]:.3f}, BUY={probs[1]:.3f}, SELL={probs[2]:.3f}")
            
            # ডিটারমিনিস্টিক অ্যাকশন
            if probs[1] > 0.5:
                print(f"  → BUY সিগন্যাল (কনফিডেন্স: {probs[1]:.1%})")
            elif probs[2] > 0.5:
                print(f"  → SELL সিগন্যাল (কনফিডেন্স: {probs[2]:.1%})")
            else:
                print(f"  → HOLD (বেস্ট: {['HOLD','BUY','SELL'][np.argmax(probs)]})")

# পলিসি অ্যানালাইসিস
analyze_policy(reinforce_trader.agent.policy)
```

## পলিসি গ্রেডিয়েন্টস: গুরুত্বপূর্ণ টিপস

```python
def policy_gradient_tips():
    """পলিসি গ্রেডিয়েন্ট ইমপ্লিমেন্টেশন টিপস"""
    tips = """
🔑 পলিসি গ্রেডিয়েন্ট ইমপ্লিমেন্টেশন টিপস:

1. ব্যাসেলাইন ইউজ করুন
   - G - b(s) ভ্যারিয়েন্স কমায়
   - b(s) = V(s) বা মিন রিটার্ন

2. রিটার্ন নরমালাইজ করুন
   - (G - μ_G) / σ_G
   - ট্রেনিং স্টেবিলিটি বাড়ায়

3. গ্রেডিয়েন্ট ক্লিপিং করুন
   - টু বড় আপডেট প্রিভেন্ট করে
   - max_grad_norm = 0.5 বা 1.0

4. লার্নিং রেট ছোট রাখুন
   - পলিসি গ্রেডিয়েন্ট সেন্সিটিভ
   - 1e-4 থেকে 3e-4 বেস্ট

5. এন্ট্রপি বোনাস যোগ করুন
   - এক্সপ্লোরেশন এনকোরেজ করে
   - β · H(π) লসে যোগ করুন
"""
    print(tips)

policy_gradient_tips()
```

## সারাংশ
- পলিসি গ্রেডিয়েন্ট সরাসরি π(a|s) অপ্টিমাইজ করে
- REINFORCE মন্টে কার্লো মেথড (পূর্ণ এপিসোড লাগে)
- ব্যাসেলাইন ভ্যারিয়েন্স কমায়
- Actor-Critic আরও এফিশিয়েন্ট
- PPO এবং SAC প্র্যাকটিক্যালি বেশি ব্যবহৃত
- ফিন্যান্সে কন্টিনিউয়াস অ্যাকশন স্পেসের জন্য আদর্শ