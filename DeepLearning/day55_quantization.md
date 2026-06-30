# Day 55: কোয়ান্টাইজেশন — মডেল কম্প্রেশন 🔢⚡

## কোয়ান্টাইজেশন কী?
কোয়ান্টাইজেশন হল নিউরাল নেটওয়ার্কের ওয়েট এবং অ্যাক্টিভেশনকে নিম্ন-প্রিসিশন ফরম্যাটে (যেমন FP32 → INT8) রূপান্তর করা।

### কেন কোয়ান্টাইজেশন?
- **মডেল সাইজ**: 4x ছোট (FP32 = 32-bit → INT8 = 8-bit)
- **স্পিড**: 2-4x ফাস্টার ইনফারেন্স (INT8 অপারেশন)
- **পাওয়ার**: কম এনার্জি কনজাম্পশন (মোবাইল/এজ)
- **মেমরি ব্যান্ডউইথ**: কম মেমরি প্রয়োজন

### কোয়ান্টাইজেশনের ধরন
1. **Post-Training Quantization (PTQ)**: ট্রেনিংয়ের পরে কোয়ান্টাইজ
2. **Quantization-Aware Training (QAT)**: ট্রেনিংয়ের সময় কোয়ান্টাইজেশন সিমুলেট
3. **Dynamic Quantization**: রানটাইমে অ্যাক্টিভেশন কোয়ান্টাইজ
4. **Static Quantization**: ক্যালিব্রেশন ডেটা দিয়ে ফিক্সড স্কেল নির্ধারণ

### ফিন্যান্সে কোয়ান্টাইজেশন
- প্রোডাকশন ট্রেডিং সিস্টেমে লো-লেটেন্সি ইনফারেন্স
- এজ ডিভাইসে মডেল ডিপ্লয়মেন্ট
- হাই-ফ্রিকোয়েন্সি ট্রেডিং (HFT) মডেল
- ক্লাউড কস্ট অপ্টিমাইজেশন

## কোয়ান্টাইজেশন ইমপ্লিমেন্টেশন (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"ব্যবহার করছি: {device}")

np.random.seed(42)
torch.manual_seed(42)
```

## 1. ম্যানুয়াল কোয়ান্টাইজেশন (FP32 → INT8)

```python
class ManualQuantization:
    """ম্যানুয়াল কোয়ান্টাইজেশন ডেমো"""
    
    @staticmethod
    def quantize(tensor, num_bits=8):
        """ফ্লোট টেনসরকে INT এ কোয়ান্টাইজ করুন"""
        qmin = 0
        qmax = 2**num_bits - 1
        
        # মিন-ম্যাক্স স্কেলিং
        min_val = tensor.min()
        max_val = tensor.max()
        
        scale = (max_val - min_val) / (qmax - qmin)
        zero_point = qmin - min_val / scale
        zero_point = torch.round(zero_point).clamp(qmin, qmax)
        
        # কোয়ান্টাইজ
        quantized = torch.round(tensor / scale + zero_point).clamp(qmin, qmax)
        
        return quantized, scale, zero_point
    
    @staticmethod
    def dequantize(quantized, scale, zero_point):
        """INT কে ফ্লোটে ডিকোয়ান্টাইজ করুন"""
        return (quantized - zero_point) * scale
    
    @staticmethod
    def quantization_error(tensor, num_bits=8):
        """কোয়ান্টাইজেশন এরর"""
        quantized, scale, zero_point = ManualQuantization.quantize(tensor, num_bits)
        dequantized = ManualQuantization.dequantize(quantized, scale, zero_point)
        
        mse = F.mse_loss(tensor, dequantized)
        max_error = (tensor - dequantized).abs().max()
        
        return {
            'mse': mse.item(),
            'max_error': max_error.item(),
            'compression': 32 / num_bits,
            'quantized_range': f'{quantized.min().item()}-{quantized.max().item()}'
        }

# ডেমো
print("\n=== ম্যানুয়াল কোয়ান্টাইজেশন ===")
test_tensor = torch.randn(100) * 2 + 0.5  # mean=0.5, std=2
results = ManualQuantization.quantization_error(test_tensor, num_bits=8)
print(f"Original range: {test_tensor.min():.3f} - {test_tensor.max():.3f}")
print(f"MSE: {results['mse']:.6f}")
print(f"Max error: {results['max_error']:.6f}")
print(f"Compression ratio: {results['compression']}x")
print(f"Quantized range: {results['quantized_range']}")
```

## 2. নিউরাল নেটওয়ার্ক মডেল কোয়ান্টাইজেশন

```python
class QuantizableModel(nn.Module):
    """কোয়ান্টাইজেশন-রেডি মডেল"""
    def __init__(self, input_dim=10, hidden_dim=64, num_classes=3):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x

def demonstrate_model_quantization():
    """মডেল কোয়ান্টাইজেশন ডেমো"""
    
    # মডেল তৈরি
    fp32_model = QuantizableModel().to(device)
    
    # ডামি ইনপুট
    dummy_input = torch.randn(100, 10).to(device)
    dummy_labels = torch.randint(0, 3, (100,)).to(device)
    
    # সিম্পল ট্রেনিং
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(fp32_model.parameters(), lr=0.01)
    
    for _ in range(10):
        optimizer.zero_grad()
        outputs = fp32_model(dummy_input)
        loss = criterion(outputs, dummy_labels)
        loss.backward()
        optimizer.step()
    
    # FP32 মডেল স্টেট
    fp32_size = sum(p.numel() * 4 for p in fp32_model.parameters())  # 4 bytes per float32
    print(f"\nFP32 মডেল সাইজ: {fp32_size / 1024:.2f} KB")
    
    # FP32 vs INT8 ওয়েট তুলনা
    print("\nওয়েট কোয়ান্টাইজেশন উদাহরণ (fc1.weight):")
    weight = fp32_model.fc1.weight.data
    
    quantized, scale, zp = ManualQuantization.quantize(weight.cpu(), num_bits=8)
    dequantized = ManualQuantization.dequantize(quantized, scale, zp)
    
    print(f"  FP32: {weight.shape}, range=[{weight.min():.3f}, {weight.max():.3f}]")
    print(f"  INT8: {quantized.shape}, range=[{quantized.min()}, {quantized.max()}]")
    print(f"  MSE: {F.mse_loss(weight.cpu(), dequantized):.6f}")
    print(f"  Scale: {scale.item():.6f}, Zero-point: {zp.item():.0f}")
    
    # INT8 মডেল সাইজ (সিমুলেটেড)
    int8_size = sum(p.numel() * 1 for p in fp32_model.parameters())  # 1 byte per int8
    print(f"\nINT8 মডেল সাইজ: {int8_size / 1024:.2f} KB")
    print(f"কম্প্রেশন রেশিও: {fp32_size / int8_size:.1f}x")
    
    return fp32_model

fp32_model = demonstrate_model_quantization()
```

## 3. PyTorch ডাইনামিক কোয়ান্টাইজেশন

```python
class DynamicQuantizationDemo:
    """PyTorch ডাইনামিক কোয়ান্টাইজেশন ডেমো"""
    
    @staticmethod
    def apply_dynamic_quantization(model):
        """ডাইনামিক কোয়ান্টাইজেশন প্রয়োগ"""
        # শুধু Linear লেয়ার কোয়ান্টাইজ করা
        quantized_model = torch.quantization.quantize_dynamic(
            model.cpu(),
            {nn.Linear},  # কোয়ান্টাইজ করার লেয়ার টাইপ
            dtype=torch.qint8  # টার্গেট ডেটাটাইপ
        )
        
        return quantized_model
    
    @staticmethod
    def compare_models(fp32_model, input_dim=10, n_samples=500):
        """FP32 vs INT8 পারফরম্যান্স তুলনা"""
        
        # ডাইনামিক কোয়ান্টাইজেশন
        int8_model = DynamicQuantizationDemo.apply_dynamic_quantization(fp32_model)
        
        # টেস্ট ইনপুট
        test_input = torch.randn(n_samples, input_dim)
        
        # FP32 ইনফারেন্স
        fp32_model.eval()
        fp32_model.cpu()
        
        import time
        
        # ওয়ার্ম-আপ
        with torch.no_grad():
            for _ in range(10):
                _ = fp32_model(test_input[:10])
                _ = int8_model(test_input[:10])
        
        # FP32 টাইমিং
        fp32_model.cpu()
        start = time.perf_counter()
        with torch.no_grad():
            for i in range(0, n_samples, 10):
                _ = fp32_model(test_input[i:i+10])
        fp32_time = time.perf_counter() - start
        
        # INT8 টাইমিং
        start = time.perf_counter()
        with torch.no_grad():
            for i in range(0, n_samples, 10):
                _ = int8_model(test_input[i:i+10])
        int8_time = time.perf_counter() - start
        
        # মডেল সাইজ
        fp32_size = sum(p.numel() * 4 for p in fp32_model.parameters())
        
        # INT8 সাইজ (PyTorch dynamic quant stores scale/zero-point separately)
        int8_size = 0
        for name, param in int8_model.named_parameters():
            if 'weight' in name:
                int8_size += param.numel() * 1  # INT8
            else:
                int8_size += param.numel() * 4  # FP32 (bias)
        
        print("\n" + "="*50)
        print("FP32 vs INT8 (Dynamic Quantization) তুলনা")
        print("="*50)
        print(f"{'':<15} {'FP32':<15} {'INT8':<15}")
        print(f"{'মডেল সাইজ':<15} {fp32_size/1024:.1f} KB{'':<8} {int8_size/1024:.1f} KB")
        print(f"{'ইনফারেন্স টাইম':<15} {fp32_time:.4f}s{'':<8} {int8_time:.4f}s")
        print(f"{'স্পিডআপ':<15} {'':<15} {fp32_time/int8_time:.1f}x")
        
        # আউটপুট তুলনা
        with torch.no_grad():
            fp32_out = fp32_model(test_input[:10])
            int8_out = int8_model(test_input[:10])
        
        mse = F.mse_loss(fp32_out, int8_out)
        print(f"{'আউটপুট MSE':<15} {mse:.6f}")
        print(f"{'প্রেডিকশন ম্যাচ':<15} {(fp32_out.argmax(1) == int8_out.argmax(1)).sum()}/{10}")
        
        return fp32_time, int8_time, int8_model

# ডেমো
print("\n=== PyTorch ডাইনামিক কোয়ান্টাইজেশন ===")
fp32_t, int8_t, int8_m = DynamicQuantizationDemo.compare_models(fp32_model)
```

## 4. ক্যালিব্রেশন এবং স্ট্যাটিক কোয়ান্টাইজেশন

```python
class StaticQuantizationDemo:
    """স্ট্যাটিক কোয়ান্টাইজেশন (ক্যালিব্রেশন সহ)"""
    
    @staticmethod
    def calibrate_model(model, calib_data):
        """ক্যালিব্রেশন ডেটা দিয়ে স্কেল নির্ধারণ"""
        # সিম্পল মিন-ম্যাক্স ক্যালিব্রেশন
        model.eval()
        
        with torch.no_grad():
            for batch in calib_data:
                _ = model(batch)
        
        return model
    
    @staticmethod
    def quantization_aware_training_concept():
        """QAT কনসেপ্ট"""
        print("""
=== Quantization-Aware Training (QAT) ===

প্রক্রিয়া:
1️⃣ FP32 মডেল ট্রেন করুন
2️⃣ Fake-quantization অপারেটর যোগ করুন
3️⃣ Low-precision সিমুলেট করে ট্রেনিং চালান
4️⃣ Real INT8 মডেলে কনভার্ট করুন

Fake-quantization:
  - ফরওয়ার্ড: INT8 কোয়ান্টাইজ ডিকোয়ান্টাইজ
  - ব্যাকওয়ার্ড: STE (Straight-Through Estimator)
  - গ্রেডিয়েন্ট ফ্লো বজায় থাকে

সুবিধা:
  - PTQ-র চেয়ে ভাল অ্যাকুরেসি (1-3%)
  - বিশেষ করে ছোট মডেলের জন্য এফেক্টিভ
  - অ্যাক্টিভেশন রেঞ্জ শিখতে পারে
""")
    
    @staticmethod
    def compare_quantization_methods():
        """কোয়ান্টাইজেশন মেথড তুলনা"""
        print("""
=== কোয়ান্টাইজেশন মেথড তুলনা ===

মেথড              কম্প্রেশন   অ্যাকুরেসি   কমপ্লেক্সিটি
─────────────────────────────────────────────────────
FP32 (বেসলাইন)      1x        বেস্ট          -
Dynamic Quant.     2-4x       গুড           ইজি
Static Quant.      4x         বেটার         মিড
QAT                4x         বেস্ট          হার্ড (ট্রেনিং লাগে)

PTQ (Post-Training): 
  + কোন ট্রেনিং লাগে না
  - অ্যাকুরেসি কিছুটা ড্রপ

QAT (Quant-Aware):
  + প্রায় FP32 সমান অ্যাকুরেসি
  - ট্রেনিং প্রয়োজন
  - বেশি সময়
""")

StaticQuantizationDemo.quantization_aware_training_concept()
StaticQuantizationDemo.compare_quantization_methods()
```

## 5. ফিন্যান্সিয়াল মডেল কোয়ান্টাইজেশন উদাহরণ

```python
class FinancialModelQuantization:
    """ফিন্যান্সিয়াল মডেলের জন্য কোয়ান্টাইজেশন"""
    
    @staticmethod
    def quantize_trading_model():
        """ট্রেডিং মডেল কোয়ান্টাইজেশন সিমুলেশন"""
        
        # ট্রেডিং মডেল তৈরি
        trading_model = nn.Sequential(
            nn.Linear(20, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3)  # BUY/SELL/HOLD
        )
        
        # ডাইনামিক কোয়ান্টাইজেশন
        quantized_model = torch.quantization.quantize_dynamic(
            trading_model,
            {nn.Linear},
            dtype=torch.qint8
        )
        
        # সাইজ তুলনা
        fp32_params = sum(p.numel() * 4 for p in trading_model.parameters())
        int8_params = 0
        for name, param in quantized_model.named_parameters():
            if 'weight' in name:
                int8_params += param.numel() * 1  # INT8
            else:
                int8_params += param.numel() * 4  # bias
        
        print("\n=== ফিন্যান্সিয়াল মডেল কোয়ান্টাইজেশন ===")
        print(f"মডেল: Linear(20→128→64→3)")
        print(f"FP32 সাইজ: {fp32_params/1024:.2f} KB")
        print(f"INT8 সাইজ: {int8_params/1024:.2f} KB")
        print(f"কম্প্রেশন: {fp32_params/int8_params:.1f}x")
        
        # ইনফারেন্স টাইম (সিমুলেটেড)
        print(f"\nলেটেন্সি (সিমুলেটেড):")
        print(f"FP32: ~2ms (CPU) বা ~0.5ms (GPU)")
        print(f"INT8: ~1ms (CPU) বা ~0.3ms (GPU)")
        print(f"স্পিডআপ: ~2x CPU, ~1.5x GPU")
        
        # ফিন্যান্স ইমপ্যাক্ট
        print(f"\nফিন্যান্স ইমপ্যাক্ট:")
        print(f"  HFT সিস্টেমে 1ms → 0.3ms লেটেন্সি রিডাকশন")
        print(f"  প্রতি দিন 100K ট্রেডে ~70 সেকেন্ড সাশ্রয়")
        print(f"  ক্লাউড কস্ট: ~50-70% কমানো (FP32→INT8)")
        
        return quantized_model

_ = FinancialModelQuantization.quantize_trading_model()
```

## কোয়ান্টাইজেশন বেস্ট প্র্যাকটিস

```python
def quantization_best_practices():
    """কোয়ান্টাইজেশন বেস্ট প্র্যাকটিস"""
    print("""
=== কোয়ান্টাইজেশন বেস্ট প্র্যাকটিস ===

1️⃣ মডেলটি প্রথমে ভালভাবে ট্রেন করুন
   - কোয়ান্টাইজেশন অ্যাকুরেসি লস কমাতে
   - রোবাস্ট মডেল কোয়ান্টাইজেশনে কম ক্ষতিগ্রস্ত হয়

2️⃣ ডাইনামিক কোয়ান্টাইজেশন দিয়ে শুরু করুন
   - সবচেয়ে ইজি, কোন ক্যালিব্রেশন লাগে না
   - Transformer/LSTM মডেলের জন্য ভাল

3️⃣ প্রয়োজন হলে স্ট্যাটিক কোয়ান্টাইজেশন ব্যবহার করুন
   - ক্যালিব্রেশন ডেটা (200-500 স্যাম্পল) প্রয়োজন
   - CNN মডেলের জন্য বেটার

4️⃣ অ্যাকুরেসি ড্রপ চেক করুন
   - <0.5%: নিরাপদ
   - 0.5-2%: গ্রহণযোগ্য (যদি স্পিড বেনিফিট বেশি হয়)
   - >2%: QAT বা কোয়ান্টাইজেশন সংবেদনশীল লেয়ার বাদ দিন

5️⃣ ফিন্যান্স স্পেসিফিক টিপস
   - প্রাইস প্রেডিকশন মডেল: কোয়ান্টাইজেশন সংবেদনশীল
   - ক্লাসিফিকেশন মডেল: কম সংবেদনশীল
   - Ensembled মডেল: কোয়ান্টাইজেশন ভাল কাজ করে
   
6️⃣ হাইব্রিড এপ্রোচ
   - কিছু লেয়ার FP32 রাখুন (প্রথম এবং শেষ)
   - বাকি INT8
   - বেস্ট ব্যালেন্স অফ স্পীড এবং অ্যাকুরেসি
""")

quantization_best_practices()
```

## সারাংশ
- কোয়ান্টাইজেশন FP32 → INT8 কনভার্ট করে মডেল 4x ছোট করে
- Post-Training Quantization (PTQ) সবচেয়ে ইজি
- Quantization-Aware Training (QAT) সর্বোচ্চ অ্যাকুরেসি দেয়
- ডাইনামিক কোয়ান্টাইজেশন NLP মডেলের জন্য ভাল
- স্ট্যাটিক কোয়ান্টাইজেশন CNN-এর জন্য ভাল
- ফিন্যান্স ট্রেডিংয়ে লেটেন্সি 2-3x কমানো যায়
- কোয়ান্টাইজেশন + প্রুনিং একসাথে ব্যবহার করলে 8-10x কম্প্রেশন সম্ভব