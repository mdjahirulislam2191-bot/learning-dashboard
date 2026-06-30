# Day 01: ডিপ লার্নিং এর ওভারভিউ 🧠

## ডিপ লার্নিং কী?
ডিপ লার্নিং (Deep Learning) হল মেশিন লার্নিং-এর একটি শাখা যা কৃত্রিম নিউরাল নেটওয়ার্ক (Artificial Neural Networks) ব্যবহার করে ডেটা থেকে শেখে। এটি মস্তিষ্কের নিউরনের কাজ অনুকরণ করে।

### ডিপ লার্নিং বনাম ট্র্যাডিশনাল মেশিন লার্নিং
- **ট্র্যাডিশনাল ML**: ফিচার ইঞ্জিনিয়ারিং ম্যানুয়ালি করতে হয়, সীমিত জটিলতা
- **ডিপ লার্নিং**: অটোমেটিক ফিচার লার্নিং, উচ্চ জটিলতা, বিপুল ডেটা প্রয়োজন

### ফিন্যান্স ও কোয়ান্টে ডিপ লার্নিং-এর ব্যবহার
1. **স্টক প্রাইস প্রেডিকশন** - LSTM, GRU মডেল
2. **পোর্টফোলিও অপ্টিমাইজেশন** - Reinforcement Learning
3. **অ্যানোমালি ডিটেকশন** - Autoencoders (ফ্রড ডিটেকশন)
4. **সেন্টিমেন্ট অ্যানালাইসিস** - Transformers (সংবাদ ও সোশ্যাল মিডিয়া)
5. **রিস্ক ম্যানেজমেন্ট** - Time Series Forecasting
6. **অ্যালগরিদমিক ট্রেডিং** - Deep Reinforcement Learning

## প্রয়োজনীয় টুলস ও সেটআপ
```bash
pip install torch torchvision torchaudio
pip install tensorflow
pip install numpy pandas matplotlib scikit-learn
pip install yfinance  # ফিন্যান্সিয়াল ডেটার জন্য
pip install ta        # টেকনিক্যাল ইন্ডিকেটর
```

## পাইথন সেটআপ চেক
```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

print(f"NumPy: {np.__version__}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# সিম্পল টেনসর অপারেশন
tensor = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
print(f"Tensor:\n{tensor}")
print(f"Tensor shape: {tensor.shape}")
```

## ডিপ লার্নিং আর্কিটেকচারের ধরণ
1. **ANN (Artificial Neural Network)** - বেসিক নেটওয়ার্ক
2. **CNN (Convolutional Neural Network)** - ইমেজ ও প্যাটার্ন
3. **RNN/LSTM/GRU** - সিকোয়েন্স ও টাইম সিরিজ
4. **Autoencoders** - ডাইমেনশনালিটি রিডাকশন
5. **GANs** - জেনারেটিভ মডেল
6. **Transformers** - NLP ও ট্রান্সফার লার্নিং

## ফিন্যান্সিয়াল ডেটা লোড করা
```python
import yfinance as yf

# Apple স্টক ডেটা ডাউনলোড
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
print(data.head())
print(f"Shape: {data.shape}")
print(f"Columns: {data.columns.tolist()}")
```

## সারসংক্ষেপ
- ডিপ লার্নিং হল মেশিন লার্নিং-এর অত্যাধুনিক শাখা
- ফিন্যান্স ও কোয়ান্টে বহুল ব্যবহার: প্রেডিকশন, অপ্টিমাইজেশন, রিস্ক
- PyTorch, TensorFlow প্রধান ফ্রেমওয়ার্ক
- GPU (CUDA) ব্যবহার করলে ট্রেনিং অনেক দ্রুত হয়