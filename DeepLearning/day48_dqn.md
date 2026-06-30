# Day 48: Deep Q-Networks (DQN) 🧠🎮

## DQN কী?
DQN হল Q-Learning + ডিপ নিউরাল নেটওয়ার্ক। বড় স্টেট স্পেসের জন্য Q-টেবিলের পরিবর্তে নিউরাল নেটওয়ার্ক ব্যবহার করা হয়।

### DQN-এর মূল উদ্ভাবন
1. **Experience Replay**: আগের অভিজ্ঞতা সংরক্ষণ করে র্যান্ডম স্যাম্পলিং
2. **Target Network**: স্থিতিশীল ট্রেনিংয়ের জন্য সেপারেট Q-নেটওয়ার্ক
3. **DQN লস**: L = 𝔼[(r + γ·max Q_target(s',a') - Q(s,a))²]

### DQN vs Q-Learning
| Q-Learning | DQN |
|---|---|
| ছোট, ডিসক্রিট স্টেট | বড়, কন্টিনিউয়াস স্টেট |
| Q-টেবিল (মেমরি ইনটেনসিভ) | নিউরাল নেটওয়ার্ক |
| ম্যানুয়াল ফিচার ইঞ্জিনিয়ারিং | অটোমেটিক ফিচার লার্নিং |
| সিম্পল | কম্প্লেক্স (রিপ্লে, টার্গেট নেট) |

### ফিন্যান্সে DQN
- স্টক ট্রেডিং সিগন্যাল জেনারেশন
- পোর্টফোলিও রিব্যালেন্সিং
- অপশন প্রাইসিং ও হেজিং
- ক্রিপ্টো ট্রেডিং বট

## DQN ইমপ্লিমেন্টেশন (PyTorch)

```python
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
random.seed(42)
```

## 1. DQN নিউরাল নেটওয়ার্ক

```python
class DQN(nn.Module):
    """Deep Q-Network নিউরাল নেটওয়ার্ক"""
    def __init__(self, state_dim=4, action_dim=3, hidden_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, x):
        """সব অ্যাকশনের জন্য Q-ভ্যালু রিটার্ন"""
        return self.net(x)
    
    def get_action(self, state, epsilon=0.1):
        """ε-greedy অ্যাকশন সিলেকশন"""
        if np.random.random() < epsilon:
            return np.random.randint(self.net[-1].out_features)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
            q_values = self.forward(state_tensor)
            return q_values.argmax().item()

# ডেমো
dqn = DQN(state_dim=4, action_dim=3, hidden_dim=64).to(device)
dummy_state = np.random.randn(4)
print(f"DQN মডেল:\n{dqn}")
print(f"\nস্টেট {dummy_state} → Q-ভ্যালুস: {dqn(torch.FloatTensor(dummy_state).unsqueeze(0).to(device))}")
```

## 2. Experience Replay বাফার

```python
class ReplayBuffer:
    """Experience Replay বাফার"""
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        """অভিজ্ঞতা সংরক্ষণ"""
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        """র্যান্ডম ব্যাচ স্যাম্পল"""
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        
        return (
            torch.FloatTensor(np.array(states)).to(device),
            torch.LongTensor(actions).unsqueeze(1).to(device),
            torch.FloatTensor(rewards).unsqueeze(1).to(device),
            torch.FloatTensor(np.array(next_states)).to(device),
            torch.FloatTensor(dones).unsqueeze(1).to(device)
        )
    
    def __len__(self):
        return len(self.buffer)

# ডেমো
buffer = ReplayBuffer(capacity=10)
for i in range(5):
    buffer.push(
        np.random.randn(4),  # state
        i % 3,               # action
        np.random.randn(),   # reward
        np.random.randn(4),  # next_state
        False                # done
    )
print(f"বাফারে {len(buffer)} টি অভিজ্ঞতা")
print(f"স্যাম্পল সাইজ: {buffer.sample(3)[0].shape}")
```

## 3. সম্পূর্ণ DQN এজেন্ট

```python
class DQNAgent:
    """সম্পূর্ণ DQN এজেন্ট"""
    def __init__(self, state_dim=4, action_dim=3, hidden_dim=128,
                 lr=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.01,
                 epsilon_decay=0.995, buffer_capacity=10000, batch_size=64,
                 target_update=100):
        
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update
        self.update_count = 0
        
        # নেটওয়ার্কস
        self.q_network = DQN(state_dim, action_dim, hidden_dim).to(device)
        self.target_network = DQN(state_dim, action_dim, hidden_dim).to(device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.memory = ReplayBuffer(buffer_capacity)
        
        print(f"DQN এজেন্ট তৈরি: state={state_dim}, action={action_dim}, hidden={hidden_dim}")
    
    def act(self, state):
        """ε-greedy পলিসি"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
            q_values = self.q_network(state_tensor)
            return q_values.argmax().item()
    
    def remember(self, state, action, reward, next_state, done):
        """অভিজ্ঞতা সংরক্ষণ"""
        self.memory.push(state, action, reward, next_state, done)
    
    def learn(self):
        """DQN ট্রেনিং স্টেপ"""
        if len(self.memory) < self.batch_size:
            return None
        
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        
        # বর্তমান Q-ভ্যালু
        current_q = self.q_network(states).gather(1, actions)
        
        # টার্গেট Q-ভ্যালু (টার্গেট নেটওয়ার্ক)
        with torch.no_grad():
            next_q = self.target_network(next_states).max(1, keepdim=True)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)
        
        # লস
        loss = F.mse_loss(current_q, target_q)
        
        # ব্যাকপ্রপাগেশন
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # টার্গেট নেটওয়ার্ক আপডেট
        self.update_count += 1
        if self.update_count % self.target_update == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Epsilon ডিকে
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        return loss.item()
    
    def save(self, path='dqn_model.pth'):
        """মডেল সেভ"""
        torch.save({
            'q_network': self.q_network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, path)
    
    def load(self, path='dqn_model.pth'):
        """মডেল লোড"""
        checkpoint = torch.load(path, map_location=device)
        self.q_network.load_state_dict(checkpoint['q_network'])
        self.target_network.load_state_dict(checkpoint['target_network'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']

# ডেমো
agent = DQNAgent(state_dim=4, action_dim=3, hidden_dim=64)
print(f"প্রাথমিক ইপসাইলন: {agent.epsilon:.4f}")
```

## 4. ট্রেডিং DQN ট্রেনিং

```python
class TradingDQN:
    """ফিন্যান্সিয়াল ট্রেডিংয়ের জন্য DQN"""
    def __init__(self, prices, state_dim=5):
        self.prices = prices
        self.state_dim = state_dim
        self.action_dim = 3  # HOLD, BUY, SELL
        
        self.agent = DQNAgent(
            state_dim=state_dim,
            action_dim=self.action_dim,
            hidden_dim=128,
            lr=0.001,
            gamma=0.99,
            epsilon=1.0,
            epsilon_decay=0.995,
            buffer_capacity=5000,
            batch_size=32,
            target_update=50
        )
    
    def _get_state(self, idx, balance, holdings):
        """স্টেট ইঞ্জিনিয়ারিং"""
        if idx < 5:
            return np.zeros(self.state_dim, dtype=np.float32)
        
        # প্রাইস ফিচারস
        current_price = self.prices[idx]
        past_prices = self.prices[idx-5:idx]
        price_returns = np.diff(past_prices) / past_prices[:-1]
        
        # ভলাটিলিটি
        volatility = np.std(price_returns) if len(price_returns) > 0 else 0
        
        # মোমেন্টাম
        momentum = (current_price - past_prices[0]) / past_prices[0]
        
        # SMA ইন্ডিকেটর
        sma_20 = np.mean(self.prices[max(0, idx-20):idx+1])
        price_to_sma = (current_price - sma_20) / sma_20
        
        state = np.array([
            balance / 10000,
            holdings / 10,
            price_returns[-1] if len(price_returns) > 0 else 0,
            volatility,
            momentum
        ], dtype=np.float32)
        
        return np.clip(state, -1, 1)
    
    def train(self, episodes=100):
        """DQN ট্রেনিং"""
        rewards = []
        
        for ep in range(episodes):
            balance = 10000
            holdings = 0
            total_reward = 0
            done = False
            idx = 0
            ep_loss = []
            
            state = self._get_state(5, balance, holdings)
            
            while not done and idx < len(self.prices) - 1:
                action = self.agent.act(state)
                price = self.prices[idx]
                
                # অ্যাকশন এক্সিকিউট
                if action == 1:  # BUY
                    if balance >= price:
                        shares = int(balance * 0.5 / price)
                        holdings += shares
                        balance -= shares * price
                
                elif action == 2:  # SELL
                    if holdings > 0:
                        balance += holdings * price
                        holdings = 0
                
                idx += 1
                done = idx >= len(self.prices) - 1
                
                next_state = self._get_state(idx, balance, holdings)
                
                # রিওয়ার্ড
                if done:
                    final_value = balance + holdings * self.prices[-1]
                    reward = (final_value - 10000) / 10000
                else:
                    unrealized_pnl = holdings * (self.prices[idx] - price) / 10000
                    reward = np.clip(unrealized_pnl, -0.1, 0.1)
                
                self.agent.remember(state, action, reward, next_state, done)
                loss = self.agent.learn()
                if loss is not None:
                    ep_loss.append(loss)
                
                total_reward += reward
                state = next_state
            
            rewards.append(total_reward)
            
            if (ep + 1) % 20 == 0:
                avg_reward = np.mean(rewards[-20:])
                avg_loss = np.mean(ep_loss) if ep_loss else 0
                print(f"এপিসোড {ep+1}/{episodes}: "
                      f"রিওয়ার্ড={avg_reward:.4f}, "
                      f"লস={avg_loss:.6f}, "
                      f"ইপসাইলন={self.agent.epsilon:.3f}")
        
        return rewards

# ডেমো
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(500) * 0.5)

print("DQN ট্রেডিং এজেন্ট ট্রেনিং...")
trading_dqn = TradingDQN(prices)
rewards = trading_dqn.train(episodes=60)
print(f"\nট্রেনিং কমপ্লিট! শেষ 10 এপিসোড গড় রিওয়ার্ড: {np.mean(rewards[-10:]):.4f}")
```

## 5. DQN পারফরম্যান্স এভালুয়েশন

```python
def evaluate_dqn(agent, prices, n_trials=10):
    """DQN এজেন্ট এভালুয়েশন"""
    results = []
    
    for trial in range(n_trials):
        balance = 10000
        holdings = 0
        idx = 5
        trades = []
        
        while idx < len(prices) - 1:
            price = prices[idx]
            
            # প্রাইস ফিচারস
            past_prices = prices[idx-5:idx]
            price_returns = np.diff(past_prices) / past_prices[:-1]
            volatility = np.std(price_returns) if len(price_returns) > 0 else 0
            momentum = (price - past_prices[0]) / past_prices[0]
            sma_20 = np.mean(prices[max(0, idx-20):idx+1])
            price_to_sma = (price - sma_20) / sma_20
            
            state = np.array([
                balance / 10000, holdings / 10,
                price_returns[-1] if len(price_returns) > 0 else 0,
                volatility, momentum
            ], dtype=np.float32)
            
            action = agent.act(state)
            
            if action == 1 and balance >= price:
                shares = int(balance * 0.5 / price)
                holdings += shares
                balance -= shares * price
                trades.append(('BUY', price))
            elif action == 2 and holdings > 0:
                balance += holdings * price
                trades.append(('SELL', price))
                holdings = 0
            
            idx += 1
        
        final_value = balance + holdings * prices[-1]
        total_return = (final_value - 10000) / 10000
        sharpe_approx = total_return / (np.std(np.diff(prices))/np.mean(prices)) if len(trades) > 0 else 0
        
        results.append({
            'trial': trial + 1,
            'total_return': total_return,
            'final_value': final_value,
            'total_trades': len(trades),
            'sharpe_approx': sharpe_approx
        })
    
    avg_return = np.mean([r['total_return'] for r in results])
    best_return = max(results, key=lambda x: x['total_return'])
    
    print("=== DQN এভালুয়েশন রেজাল্টস ===")
    print(f"গড় রিটার্ন: {avg_return:.2%}")
    print(f"বেস্ট ট্রায়াল: {best_return['trial']} (রিটার্ন: {best_return['total_return']:.2%})")
    print(f"গড় ট্রেড কাউন্ট: {np.mean([r['total_trades'] for r in results]):.1f}")
    
    return results

print("\nDQN এভালুয়েশন:")
eval_results = evaluate_dqn(trading_dqn.agent, prices, n_trials=3)
```

## সারাংশ
- DQN Q-Learning + ডিপ নিউরাল নেটওয়ার্ক কম্বিনেশন
- Experience Replay ডেটা এফিশিয়েন্সি বাড়ায়
- Target Network ট্রেনিং স্টেবিলিটি দেয়
- কন্টিনিউয়াস স্টেট স্পেসে কাজ করতে পারে
- ফিন্যান্সে ট্রেডিং স্ট্রাটেজি, পোর্টফোলিও অপ্টিমাইজেশনে ব্যবহার হয়
- হাইপারপ্যারামিটার (buffer size, target update frequency) গুরুত্বপূর্ণ