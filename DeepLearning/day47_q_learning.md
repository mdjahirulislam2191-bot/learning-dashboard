# Day 47: Q-Learning — ভ্যালু-বেসড RL 🎯

## Q-Learning কী?
Q-Learning একটি মডেল-ফ্রি RL অ্যালগরিদম যা Q(s,a) ফাংশন শেখে — একটি স্টেটে একটি অ্যাকশন নেওয়ার প্রত্যাশিত রিওয়ার্ড।

### Q(s,a) ফাংশন
- **Q(s,a)**: স্টেট s-এ অ্যাকশন a নেওয়ার ভ্যালু
- **কিউ-টেবিল**: সব (স্টেট, অ্যাকশন) পেয়ারের Q-ভ্যালু সংরক্ষণ
- **বেলম্যান আপডেট**: Q(s,a) ← Q(s,a) + α[r + γ·maxₐ'Q(s',a') - Q(s,a)]

### Q-Learning অ্যালগরিদম
```
1. Q-টেবিল ইনিশিয়ালাইজ (সব Q(s,a)=0)
2. প্রতিটি এপিসোডের জন্য:
   a. স্টেট s দেখুন
   b. ε-greedy পলিসি দিয়ে অ্যাকশন a নিন
   c. রিওয়ার্ড r এবং নেক্সট স্টেট s' দেখুন
   d. Q(s,a) আপডেট: Q(s,a) += α[r + γ·max Q(s',:) - Q(s,a)]
   e. s = s' (পরবর্তী স্টেপ)
```

### ফিন্যান্স অ্যাপ্লিকেশন
- ডিসক্রিটাইজড মার্কেট স্টেটে ট্রেডিং
- পোর্টফোলিও অ্যালোকেশন
- অর্ডার এক্সিকিউশন অপ্টিমাইজেশন

## Q-Learning ইমপ্লিমেন্টেশন

```python
import numpy as np
import torch
import random
from collections import deque

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
random.seed(42)
```

## 1. সিম্পল Q-Learning এজেন্ট

```python
class QLearningAgent:
    """টেবিল-বেসড Q-Learning এজেন্ট"""
    def __init__(self, n_states=10, n_actions=3, 
                 learning_rate=0.1, gamma=0.95, epsilon=1.0,
                 epsilon_min=0.01, epsilon_decay=0.995):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        
        # Q-টেবিল: states × actions
        self.q_table = np.zeros((n_states, n_actions))
        
        print(f"Q-টেবিল তৈরি: {n_states} স্টেট × {n_actions} অ্যাকশন")
    
    def get_action(self, state):
        """ε-greedy পলিসি দিয়ে অ্যাকশন সিলেক্ট"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state, done):
        """Q-ভ্যালু আপডেট (বেলম্যান ইকুয়েশন)"""
        best_next_q = 0 if done else np.max(self.q_table[next_state])
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - self.q_table[state][action]
        
        # Q(s,a) আপডেট
        self.q_table[state][action] += self.lr * td_error
        
        return td_error
    
    def decay_epsilon(self):
        """এক্সপ্লোরেশন কমানো"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

# ডেমো
agent = QLearningAgent(n_states=10, n_actions=3)
print(f"প্রাথমিক Q-টেবিল:\n{agent.q_table}")
```

## 2. সিম্পল গ্রিড-ওয়ার্ল্ড এনভায়রনমেন্ট

```python
class GridWorld:
    """সিম্পল গ্রিড-ওয়ার্ল্ড এনভায়রনমেন্ট"""
    def __init__(self, size=3):
        self.size = size
        self.n_states = size * size
        self.n_actions = 4  # UP, DOWN, LEFT, RIGHT
        self.goal_state = size * size - 1  (self.size - 1, self.size - 1)
        self.reset()
    
    def reset(self):
        self.state = 0  # শুরু (0,0)
        self.steps = 0
        return self.state
    
    def step(self, action):
        row = self.state // self.size
        col = self.state % self.size
        
        # অ্যাকশন এক্সিকিউট
        if action == 0: row = max(0, row - 1)      # UP
        elif action == 1: row = min(self.size-1, row + 1)  # DOWN
        elif action == 2: col = max(0, col - 1)      # LEFT
        elif action == 3: col = min(self.size-1, col + 1)  # RIGHT
        
        new_state = row * self.size + col
        self.state = new_state
        self.steps += 1
        
        # রিওয়ার্ড
        if new_state == self.goal_state:
            reward = 10
            done = True
        else:
            reward = -1
            done = self.steps >= 20  # ম্যাক্স স্টেপ
        
        return new_state, reward, done

# গ্রিড-ওয়ার্ল্ড টেস্ট
grid = GridWorld(size=4)
print(f"গ্রিড ওয়ার্ল্ড: {grid.size}×{grid.size}")
print(f"স্টেটস: 0-{grid.n_states-1}, গোল: {grid.goal_state}")
print(f"অ্যাকশনস: 0(UP), 1(DOWN), 2(LEFT), 3(RIGHT)")
```

## 3. ট্রেডিং Q-Learning

```python
class TradingQLearning:
    """ফিন্যান্সিয়াল ট্রেডিংয়ের জন্য Q-Learning"""
    def __init__(self, prices, n_price_bins=10, initial_balance=10000):
        self.prices = prices
        self.n_price_bins = n_price_bins
        self.initial_balance = initial_balance
        
        # স্টেট ডিসক্রিটাইজেশন
        self.price_min = min(prices)
        self.price_max = max(prices)
        self.price_bins = np.linspace(self.price_min, self.price_max, n_price_bins)
        
        # স্টেট স্পেস: [প্রাইস_বিন, হোল্ডিংস_বিন]
        self.n_states = n_price_bins * 3  # 0, 1, 2+ শেয়ার
        self.n_actions = 3  # HOLD(0), BUY(1), SELL(2)
        
        self.q_agent = QLearningAgent(
            n_states=self.n_states, 
            n_actions=self.n_actions,
            learning_rate=0.01,
            gamma=0.99,
            epsilon=1.0
        )
    
    def _state_to_idx(self, price_idx, holdings):
        """স্টেটকে ইনডেক্সে রূপান্তর"""
        price_bin = np.digitize(self.prices[price_idx], self.price_bins) - 1
        price_bin = min(price_bin, self.n_price_bins - 1)
        holdings_bin = min(holdings, 2)  # 0, 1, 2+
        return price_bin + holdings_bin * self.n_price_bins
    
    def train(self, episodes=500):
        """Q-Learning ট্রেনিং"""
        rewards_history = []
        
        for ep in range(episodes):
            balance = self.initial_balance
            holdings = 0
            price_idx = 0
            total_reward = 0
            done = False
            
            while not done:
                state = self._state_to_idx(price_idx, holdings)
                action = self.q_agent.get_action(state)
                
                price = self.prices[price_idx]
                
                # অ্যাকশন এক্সিকিউট
                if action == 1:  # BUY
                    can_buy = balance >= price
                    if can_buy:
                        shares_to_buy = int(balance / price)
                        holdings += shares_to_buy
                        balance -= shares_to_buy * price
                
                elif action == 2:  # SELL
                    if holdings > 0:
                        balance += holdings * price
                        holdings = 0
                
                # নেক্সট স্টেট প্রস্তুত
                price_idx += 1
                done = price_idx >= len(self.prices) - 1
                
                # রিওয়ার্ড
                if done:
                    final_value = balance + holdings * self.prices[-1]
                    reward = (final_value - self.initial_balance) / self.initial_balance
                else:
                    next_price = self.prices[price_idx]
                    reward = 0.001 * (next_price - price) / price * holdings
                
                next_state = self._state_to_idx(min(price_idx, len(self.prices)-1), holdings)
                self.q_agent.update(state, action, reward, next_state, done)
                total_reward += reward
            
            self.q_agent.decay_epsilon()
            rewards_history.append(total_reward)
            
            if (ep + 1) % 100 == 0:
                avg_reward = np.mean(rewards_history[-100:])
                print(f"এপিসোড {ep+1}/{episodes}: "
                      f"গড় রিওয়ার্ড = {avg_reward:.4f}, "
                      f"ইপসাইলন = {self.q_agent.epsilon:.3f}")
        
        return rewards_history
    
    def test(self):
        """শিখা পলিসি টেস্ট"""
        balance = self.initial_balance
        holdings = 0
        trades = []
        
        for price_idx in range(len(self.prices) - 1):
            state = self._state_to_idx(price_idx, holdings)
            action = np.argmax(self.q_agent.q_table[state])
            
            price = self.prices[price_idx]
            
            if action == 1 and balance >= price:  # BUY
                shares = int(balance / price)
                holdings += shares
                balance -= shares * price
                trades.append(('BUY', price_idx, price, shares))
            
            elif action == 2 and holdings > 0:  # SELL
                balance += holdings * price
                trades.append(('SELL', price_idx, price, holdings))
                holdings = 0
        
        # ফাইনাল ভ্যালু
        final_value = balance + holdings * self.prices[-1]
        total_return = (final_value - self.initial_balance) / self.initial_balance
        
        return {
            'initial_balance': self.initial_balance,
            'final_value': final_value,
            'total_return': total_return,
            'total_trades': len(trades),
            'trades': trades[:5]  # প্রথম ৫ ট্রেড
        }

# ডেমো
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(300) * 0.5)

trading_agent = TradingQLearning(prices)
print("Q-Learning ট্রেডিং এজেন্ট ট্রেনিং শুরু...")
rewards = trading_agent.train(episodes=200)

print("\nটেস্টিং ফলাফল:")
results = trading_agent.test()
print(f"প্রাথমিক ব্যালেন্স: ${results['initial_balance']:.2f}")
print(f"ফাইনাল ভ্যালু: ${results['final_value']:.2f}")
print(f"মোট রিটার্ন: {results['total_return']:.2%}")
print(f"মোট ট্রেড: {results['total_trades']}")
```

## 4. মাল্টি-স্টেট Q-Learning অ্যানালাইসিস

```python
class QLearningAnalysis:
    """Q-Learning পারফরম্যান্স অ্যানালাইসিস"""
    
    @staticmethod
    def analyze_q_table(q_table, state_labels=None, action_labels=None):
        """Q-টেবিল অ্যানালাইসিস"""
        if action_labels is None:
            action_labels = ['HOLD', 'BUY', 'SELL']
        
        print("=== Q-টেবিল অ্যানালাইসিস ===")
        print(f"শেপ: {q_table.shape}")
        print("\nবেস্ট অ্যাকশন পার স্টেট:")
        
        for s in range(min(q_table.shape[0], 10)):
            best_action = np.argmax(q_table[s])
            best_value = q_table[s][best_action]
            state_name = state_labels[s] if state_labels else f"State {s}"
            print(f"  {state_name}: {action_labels[best_action]} (Q={best_value:.3f})")
        
        print(f"\nগড় Q-ভ্যালু: {np.mean(q_table):.4f}")
        print(f"ম্যাক্স Q-ভ্যালু: {np.max(q_table):.4f}")
        print(f"মিন Q-ভ্যালু: {np.min(q_table):.4f}")
    
    @staticmethod
    def convergence_analysis(rewards, window=50):
        """কনভারজেন্স অ্যানালাইসিস"""
        if len(rewards) < window:
            return
        
        smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
        
        print("=== কনভারজেন্স অ্যানালাইসিস ===")
        print(f"প্রথম {window} এপিসোড গড়: {np.mean(rewards[:window]):.4f}")
        print(f"শেষ {window} এপিসোড গড়: {np.mean(rewards[-window:]):.4f}")
        print(f"ইমপ্রুভমেন্ট: {(np.mean(rewards[-window:]) - np.mean(rewards[:window])):.4f}")
        
        stable = np.std(rewards[-window:])
        print(f"শেষ {window} এপিসোড স্ট্যান্ডার্ড ডেভিয়েশন: {stable:.4f}")
        if stable < 0.1:
            print("✅ মডেল কনভার্জড (লো ভ্যারিয়েন্স)")
        else:
            print("⚠️ মডেল এখনও কনভার্জ করেনি")

# অ্যানালাইসিস চালান
QLearningAnalysis.analyze_q_table(trading_agent.q_agent.q_table)
print()
QLearningAnalysis.convergence_analysis(rewards)
```

## 5. Q-Learning প্যারামিটার টিউনিং

```python
def tune_q_learning(prices, lr_values, gamma_values, episodes=100):
    """হাইপারপ্যারামিটার টিউনিং"""
    best_reward = -float('inf')
    best_params = {}
    
    for lr in lr_values:
        for gamma in gamma_values:
            agent = TradingQLearning(prices)
            agent.q_agent.lr = lr
            agent.q_agent.gamma = gamma
            
            rewards = agent.train(episodes=episodes)
            avg_reward = np.mean(rewards[-50:])
            
            print(f"lr={lr:.2f}, γ={gamma:.2f}: শেষ 50 গড় রিওয়ার্ড = {avg_reward:.4f}")
            
            if avg_reward > best_reward:
                best_reward = avg_reward
                best_params = {'lr': lr, 'gamma': gamma}
    
    print(f"\n✅ বেস্ট প্যারামিটারস: {best_params} (গড় রিওয়ার্ড = {best_reward:.4f})")
    return best_params

# সিম্পল টিউনিং
print("হাইপারপ্যারামিটার টিউনিং:")
print("=" * 40)
tune_q_learning(prices[:100], 
                lr_values=[0.01], 
                gamma_values=[0.9, 0.99], 
                episodes=50)
```

## সারাংশ
- Q-Learning মডেল-ফ্রি RL অ্যালগরিদম
- Q-টেবিলে (স্টেট, অ্যাকশন) ভ্যালু সংরক্ষণ করে
- বেলম্যান ইকুয়েশন দিয়ে Q-ভ্যালু আপডেট করে
- ε-greedy পলিসি এক্সপ্লোরেশন-এক্সপ্লয়েটেশন ব্যালেন্স করে
- ফিন্যান্সে ডিসক্রিটাইজড স্টেট স্পেসে ট্রেডিং শেখা যায়
- লার্নিং রেট (α) এবং ডিসকাউন্ট ফ্যাক্টর (γ) গুরুত্বপূর্ণ হাইপারপ্যারামিটার