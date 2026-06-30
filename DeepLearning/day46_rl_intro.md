# Day 46: রিইনফোর্সমেন্ট লার্নিং পরিচিতি 🎮🤖

## রিইনফোর্সমেন্ট লার্নিং (RL) কী?
RL হল মেশিন লার্নিংয়ের একটি শাখা যেখানে এজেন্ট পরিবেশের সাথে ইন্টারঅ্যাক্ট করে পুরস্কার ম্যাক্সিমাইজ করতে শেখে।

### মূল ধারণা
- **Agent (এজেন্ট)**: সিদ্ধান্ত গ্রহণকারী
- **Environment (পরিবেশ)**: এজেন্ট যেখানে কাজ করে
- **State (অবস্থা)**: পরিবেশের বর্তমান পরিস্থিতি
- **Action (অ্যাকশন)**: এজেন্ট যা করতে পারে
- **Reward (পুরস্কার)**: ফিডব্যাক সিগন্যাল
- **Policy (পলিসি)**: স্টেট → অ্যাকশন ম্যাপিং

### RL vs সুপারভাইজড লার্নিং
| সুপারভাইজড | RL |
|---|---|
| লেবেলযুক্ত ডেটা | এক্সপ্লোরেশন থেকে শেখে |
| ইমিডিয়েট ফিডব্যাক | ডিলেড রিওয়ার্ড |
| আইড ইন্ডিপেন্ডেন্ট স্যাম্পল | টাইম-ডিপেন্ডেন্ট সিকোয়েন্স |

### ফিন্যান্সে RL-এর ব্যবহার
- ট্রেডিং স্ট্রাটেজি অপ্টিমাইজেশন
- পোর্টফোলিও ম্যানেজমেন্ট
- মার্কেট মেকিং
- রিস্ক ম্যানেজমেন্ট

## RL ফ্রেমওয়ার্ক

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

# সীড সেট করা
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)
```

## 1. এনভায়রনমেন্ট সিমুলেশন

```python
class TradingEnvironment:
    """সিম্পল ট্রেডিং এনভায়রনমেন্ট"""
    def __init__(self, prices, initial_balance=10000, max_steps=100):
        self.prices = prices
        self.initial_balance = initial_balance
        self.max_steps = max_steps
        self.reset()
    
    def reset(self):
        """এনভায়রনমেন্ট রিসেট"""
        self.balance = self.initial_balance
        self.shares = 0
        self.step_count = 0
        self.total_reward = 0
        self.current_price_idx = 0
        return self._get_state()
    
    def _get_state(self):
        """বর্তমান স্টেট রিটার্ন"""
        return np.array([
            self.balance / self.initial_balance,
            self.shares / 10,
            self.prices[self.current_price_idx] / np.mean(self.prices),
            self.step_count / self.max_steps
        ], dtype=np.float32)
    
    def step(self, action):
        """অ্যাকশন নেওয়া
        0: HOLD, 1: BUY, 2: SELL
        """
        price = self.prices[self.current_price_idx]
        
        if action == 1:  # BUY
            max_shares = int(self.balance / price)
            if max_shares > 0:
                self.shares += max_shares
                self.balance -= max_shares * price
        
        elif action == 2:  # SELL
            if self.shares > 0:
                self.balance += self.shares * price
                self.shares = 0
        
        # নেক্সট স্টেপ
        self.step_count += 1
        self.current_price_idx += 1
        done = self.step_count >= self.max_steps or self.current_price_idx >= len(self.prices) - 1
        
        # রিওয়ার্ড ক্যালকুলেশন
        if done:
            # ফাইনাল পোর্টফোলিও ভ্যালু
            final_value = self.balance + self.shares * self.prices[self.current_price_idx]
            reward = (final_value - self.initial_balance) / self.initial_balance
        else:
            reward = 0  # ইন্টারমিডিয়েট রিওয়ার্ড
        
        next_state = self._get_state() if not done else np.zeros(4)
        return next_state, reward, done

# সিম্পল প্রাইস ডেটা
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(200) * 0.5)
env = TradingEnvironment(prices)
print(f"এনভায়রনমেন্ট তৈরি হয়েছে: {len(prices)} প্রাইস পয়েন্ট")
print(f"স্টেট স্পেস: {env._get_state().shape}")
print(f"অ্যাকশন স্পেস: 3 (HOLD/BUY/SELL)")
```

## 2. র্যান্ডম পলিসি বেসলাইন

```python
def random_policy(env, episodes=10):
    """র্যান্ডম পলিসি বেসলাইন"""
    total_rewards = []
    
    for ep in range(episodes):
        state = env.reset()
        done = False
        ep_reward = 0
        
        while not done:
            action = np.random.randint(0, 3)
            next_state, reward, done = env.step(action)
            ep_reward += reward
            state = next_state
        
        total_rewards.append(ep_reward)
        if ep < 3 or ep == episodes - 1:
            print(f"এপিসোড {ep+1}: টোটাল রিওয়ার্ড = {ep_reward:.4f}")
    
    print(f"\nর্যান্ডম পলিসি গড় রিওয়ার্ড: {np.mean(total_rewards):.4f} ± {np.std(total_rewards):.4f}")
    return total_rewards

random_rewards = random_policy(env, episodes=10)
```

## 3. RL টার্মিনোলজি

```python
class RLConcepts:
    """RL গুরুত্বপূর্ণ কনসেপ্টস"""
    
    @staticmethod
    def markov_decision_process():
        """MDP (Markov Decision Process)"""
        return """
MDP ফর্মালিজম:
- S: স্টেট স্পেস
- A: অ্যাকশন স্পেস
- P(s'|s,a): ট্রানজিশন প্রোবাবিলিটি
- R(s,a): রিওয়ার্ড ফাংশন
- γ (gamma): ডিসকাউন্ট ফ্যাক্টর (0 ≤ γ ≤ 1)
"""
    
    @staticmethod
    def bellman_equation():
        """বেলম্যান ইকুয়েশন"""
        return """
বেলম্যান ইকুয়েশন:
V(s) = maxₐ [R(s,a) + γ · Σ P(s'|s,a) · V(s')]

Q(s,a) = R(s,a) + γ · Σ P(s'|s,a) · maxₐ' Q(s',a')
"""
    
    @staticmethod
    def exploration_vs_exploitation():
        """এক্সপ্লোরেশন vs এক্সপ্লয়েটেশন"""
        return """
এক্সপ্লোরেশন vs এক্সপ্লয়েটেশন:
- Exploration: নতুন অ্যাকশন ট্রাই করে (আনসার্টেইন)
- Exploitation: পরিচিত ভাল অ্যাকশন ইউজ করে (অপ্টিমাল)
- Epsilon-Greedy: ε প্রবাবিলিটিতে এক্সপ্লোর, (1-ε) তে এক্সপ্লয়েট
"""

concepts = RLConcepts()
print("=== RL কনসেপ্টস ===")
print(concepts.markov_decision_process())
print(concepts.bellman_equation())
print(concepts.exploration_vs_exploitation())
```

## 4. RL ট্রেনিং লুপ

```python
def rl_training_loop(env, policy_func, episodes=100, epsilon=0.1):
    """RL ট্রেনিং লুপ সিমুলেশন"""
    rewards_history = []
    epsilon_start = epsilon
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        steps = 0
        
        while not done:
            # Epsilon-greedy পলিসি
            if np.random.random() < epsilon:
                action = np.random.randint(0, 3)  # এক্সপ্লোর
            else:
                action = policy_func(state)  # এক্সপ্লয়েট
            
            next_state, reward, done = env.step(action)
            total_reward += reward
            state = next_state
            steps += 1
        
        rewards_history.append(total_reward)
        
        # Epsilon ডিকে (এক্সপ্লোরেশন কমানো)
        epsilon = max(0.01, epsilon * 0.995)
        
        if (episode + 1) % 20 == 0:
            avg_reward = np.mean(rewards_history[-20:])
            print(f"এপিসোড {episode+1}/{episodes}: "
                  f"গড় রিওয়ার্ড = {avg_reward:.4f}, "
                  f"স্টেপস = {steps}, "
                  f"ইপসাইলন = {epsilon:.3f}")
    
    return rewards_history

# সিম্পল পলিসি: বাই-এন্ড-হোল্ড স্ট্রাটেজি
def buy_and_hold_policy(state):
    """শুধু বাই করুন"""
    return 1  # BUY

# সিম্পল পলিসি: মিন-রিভার্সন
def mean_reversion_policy(state):
    """প্রাইস যদি গড়ের নিচে তাহলে বাই"""
    price_ratio = state[2]  # current_price / mean_price
    if price_ratio < 1:
        return 1  # BUY
    else:
        return 0  # HOLD

print("\n=== RL ট্রেনিং লুপ (Buy & Hold) ===")
bh_rewards = rl_training_loop(env, buy_and_hold_policy, episodes=100)

print("\n=== RL ট্রেনিং লুপ (Mean Reversion) ===")
mr_rewards = rl_training_loop(env, mean_reversion_policy, episodes=100)
```

## 5. RL পাইপলাইন ভিজুয়ালাইজেশন

```python
def visualize_rl_pipeline():
    """RL পাইপলাইন ভিজুয়ালাইজেশন"""
    return """
=== RL পাইপলাইন ===

┌─────────────────┐     ┌──────────┐     ┌─────────────────┐
│   Environment   │────▶│   State  │────▶│     Agent      │
│  (Market Data)  │     │   (s)    │     │  (Policy π)    │
└─────────────────┘     └──────────┘     └─────────────────┘
        △                                      │
        │                                      │
        │              ┌──────────┐            │
        └──────────────│  Reward  │◀───────────┘
                       │    r     │
                       └──────────┘

কম্পোনেন্টস:
1️⃣   State: বর্তমান মার্কেট কন্ডিশন (প্রাইস, ভলিউম, ইন্ডিকেটর)
2️⃣   Agent: নিউরাল নেটওয়ার্ক (পলিসি নেটওয়ার্ক)
3️⃣   Action: BUY/SELL/HOLD সিদ্ধান্ত
4️⃣   Reward: P&L, Sharpe Ratio, বা অন্যান্য মেট্রিক
5️⃣   Environment: মার্কেট সিমুলেশন বা রিয়েল ডেটা
"""

print(visualize_rl_pipeline())
```

## সারাংশ
- RL-এ এজেন্ট পরিবেশ থেকে শেখে পুরস্কার ম্যাক্সিমাইজ করে
- MDP ফর্মালিজম RL সমস্যা মডেল করে
- Exploration vs Exploitation একটি মূল চ্যালেঞ্জ
- ফিন্যান্সে RL ট্রেডিং, পোর্টফোলিও, রিস্ক ম্যানেজমেন্টে ব্যবহৃত হয়
- বেলম্যান ইকুয়েশন RL অপ্টিমাইজেশনের ভিত্তি