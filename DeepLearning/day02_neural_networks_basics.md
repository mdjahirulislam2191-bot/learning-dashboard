# Day 02: নিউরাল নেটওয়ার্কের বেসিক 🧬

## নিউরাল নেটওয়ার্ক কী?
নিউরাল নেটওয়ার্ক হলো গণিতীয় মডেল যা জৈবিক নিউরনের মতো কাজ করে। এটি ইনপুট নেয়, প্রসেস করে এবং আউটপুট দেয়।

### একক নিউরনের গঠন (Perceptron)
```
ইনপুট → ওয়েট (w) → সাম (Σ) → অ্যাক্টিভেশন ফাংশন (f) → আউটপুট
   x1 ──w1──→
   x2 ──w2──→  [Σ] → [f] → ŷ
   x3 ──w3──→
```

**গাণিতিক রূপ:**  
ŷ = f(Σ(wᵢ · xᵢ) + b)

যেখানে:
- xᵢ = ইনপুট ভ্যালু
- wᵢ = ওয়েট (শিখতে হবে)
- b = বায়াস (শিখতে হবে)
- f = অ্যাক্টিভেশন ফাংশন

## পাইথনে একটি নিউরন ইমপ্লিমেন্টেশন
```python
import numpy as np

class Neuron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size) * 0.01
        self.bias = np.random.randn() * 0.01
    
    def forward(self, inputs):
        """ফরোয়ার্ড পাস"""
        z = np.dot(self.weights, inputs) + self.bias
        return self._sigmoid(z)
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# টেস্ট করা
neuron = Neuron(input_size=3)
inputs = np.array([0.5, 0.8, 0.2])
output = neuron.forward(inputs)
print(f"নিউরন আউটপুট: {output:.4f}")
```

## ফিন্যান্সিয়াল কন্টেক্সট: রিস্ক স্কোরিং
```python
# একটি স্টকের রিস্ক স্কোর ক্যালকুলেশন
# ফিচার: ভোলাটিলিটি, P/E রেশিও, মার্কেট ক্যাপ
class RiskScorer(Neuron):
    def __init__(self):
        super().__init__(input_size=3)
    
    def calculate_risk_score(self, volatility, pe_ratio, log_market_cap):
        features = np.array([volatility, pe_ratio, log_market_cap])
        risk = self.forward(features)
        return risk  # ০ (নিরাপদ) থেকে ১ (উচ্চ ঝুঁকি)

risk_model = RiskScorer()
# উদাহরণ: হাই ভোলাটিলিটি স্টক
score = risk_model.calculate_risk_score(0.45, 35.0, 12.5)
print(f"রিস্ক স্কোর: {score:.3f}")
```

## মাল্টি-লেয়ার নেটওয়ার্ক
```python
class Layer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(output_size, input_size) * 0.01
        self.bias = np.zeros((output_size, 1))
    
    def forward(self, inputs):
        self.inputs = inputs.reshape(-1, 1)
        self.z = np.dot(self.weights, self.inputs) + self.bias
        self.a = self._relu(self.z)
        return self.a
    
    def _relu(self, x):
        return np.maximum(0, x)

# ২-লেয়ার নেটওয়ার্ক
layer1 = Layer(input_size=4, output_size=8)
layer2 = Layer(input_size=8, output_size=1)

sample_input = np.array([0.1, 0.5, 0.3, 0.9])
hidden = layer1.forward(sample_input)
output = layer2.forward(hidden.flatten())
print(f"নেটওয়ার্ক আউটপুট: {output.item():.4f}")
```

## কী পয়েন্টস
- নিউরন = ইনপুট × ওয়েট + বায়াস → অ্যাক্টিভেশন
- লেয়ার = নিউরনের গ্রুপ
- ডিপ নেটওয়ার্ক = একাধিক লেয়ার (গভীর)
- ফিন্যান্সে: রিস্ক স্কোরিং, ক্রেডিট অ্যাসেসমেন্ট
- ওয়েট ও বায়াস ট্রেনিং-এর সময় শিখতে হয়

## এক্সারসাইজ
```python
# আপনার নিজের ৩-ইনপুট নিউরন তৈরি করে বিভিন্ন আউটপুট দেখুন
test_inputs = [
    np.array([0.1, 0.2, 0.3]),
    np.array([0.9, 0.8, 0.7]),
    np.array([0.5, 0.5, 0.5])
]

n = Neuron(3)
for inp in test_inputs:
    print(f"ইনপুট {inp} → আউটপুট {n.forward(inp):.4f}")
```