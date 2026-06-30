# Day 19: ট্রান্সফার লার্নিং 🔄

## ট্রান্সফার লার্নিং কী?
একটি মডেল যা একটি বড় ডেটাসেটে (যেমন ImageNet) ট্রেনিং করা হয়েছে, সেটিকে নতুন টাস্কের জন্য পুনরায় ব্যবহার করাকে ট্রান্সফার লার্নিং বলে।

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
```

## কেন ট্রান্সফার লার্নিং?
```python
benefits = """
✅ **কম ডেটা প্রয়োজন**: Pretrained মডেল আগে থেকেই অনেক ফিচার জানে
✅ **দ্রুত ট্রেনিং**: কয়েক ঘণ্টার পরিবর্তে কয়েক মিনিট
✅ **ভালো পারফরম্যান্স**: বড় ডেটাসেটের জ্ঞান কাজে লাগে
✅ **ফিন্যান্সের জন্য পারফেক্ট**: ছোট ডেটাসেটেও ভালো কাজ করে
"""
print(benefits)
```

## পদ্ধতি ১: ফিচার এক্সট্র্যাক্টর
```python
class FeatureExtractor:
    """Pretrained মডেল দিয়ে ফিচার এক্সট্র্যাকশন"""
    
    def __init__(self, model_name='resnet18'):
        # প্রিট্রেইন্ড মডেল লোড
        if model_name == 'resnet18':
            self.model = models.resnet18(pretrained=True)
            self.feature_dim = 512
        elif model_name == 'resnet50':
            self.model = models.resnet50(pretrained=True)
            self.feature_dim = 2048
        elif model_name == 'vgg16':
            self.model = models.vgg16(pretrained=True)
            self.feature_dim = 4096
        
        # ফিচার লেয়ার পর্যন্ত সব ফ্রিজ
        for param in self.model.parameters():
            param.requires_grad = False
        
        # ফাইনাল FC লেয়ার রিমুভ
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()
    
    def extract_features(self, x):
        """ইমেজ থেকে ফিচার এক্সট্র্যাক্ট"""
        with torch.no_grad():
            features = self.model(x)
            return features.squeeze()

# extractor = FeatureExtractor('resnet18')
# features = extractor.extract_features(torch.randn(1, 3, 224, 224))
# print(f"Extracted features: {features.shape}")
print("ফিচার এক্সট্র্যাক্টর প্রস্তুত")
```

## পদ্ধতি ২: Fine-tuning
```python
class FineTuner:
    """Pretrained মডেল Fine-tuning"""
    
    def __init__(self, num_classes=5, model_name='resnet18'):
        if model_name == 'resnet18':
            self.model = models.resnet18(pretrained=True)
            in_features = 512
        elif model_name == 'resnet50':
            self.model = models.resnet50(pretrained=True)
            in_features = 2048
        
        # পুরনো FC হেড রিপ্লেস
        self.model.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        
        self.model = self.model.to(device)
    
    def freeze_layers(self, freeze_until=6):
        """প্রথম কয়েকটা লেয়ার ফ্রিজ"""
        for i, param in enumerate(self.model.parameters()):
            if i < freeze_until:
                param.requires_grad = False
    
    def unfreeze_all(self):
        """সব লেয়ার আনফ্রিজ"""
        for param in self.model.parameters():
            param.requires_grad = True
    
    def get_optimizer(self):
        """ভিন্ন LR দিয়ে অপ্টিমাইজার"""
        # ফ্রিজ না করা প্যারামিটার শুধু আপডেট
        trainable_params = [p for p in self.model.parameters() if p.requires_grad]
        return optim.Adam(trainable_params, lr=0.0001)

# finetuner = FineTuner(num_classes=5)
# print(finetuner.model)
print("Fine-tuning মডেল প্রস্তুত")
```

## পদ্ধতি ৩: প্রগ্রেসিভ আনফ্রিজিং
```python
class ProgressiveUnfreezing:
    """ধীরে ধীরে লেয়ার আনফ্রিজ করা"""
    
    def __init__(self, model):
        self.model = model
        self.layers = list(model.parameters())
    
    def freeze_all(self):
        for param in self.model.parameters():
            param.requires_grad = False
        print("সব লেয়ার ফ্রিজ করা হয়েছে")
    
    def unfreeze_last_n(self, n):
        """শেষ n টি লেয়ার আনফ্রিজ"""
        params = list(self.model.parameters())
        n = min(n, len(params))
        
        for i, param in enumerate(params):
            if i >= len(params) - n:
                param.requires_grad = True
            else:
                param.requires_grad = False
        
        print(f"শেষ {n} টি লেয়ার আনফ্রিজ করা হয়েছে")
    
    def train_gradually(self, dataloader, epochs_per_stage=5, total_stages=3):
        """
        Stage 1: শুধু FC লেয়ার
        Stage 2: FC + Last Conv Block
        Stage 3: পুরো মডেল
        """
        for stage in range(total_stages):
            if stage == 0:
                self.freeze_all()
                # FC লেয়ার আনফ্রিজ
                for param in self.model.fc.parameters():
                    param.requires_grad = True
                print(f"\nStage {stage + 1}: Training FC layer only")
            elif stage == 1:
                self.unfreeze_last_n(20)
                print(f"\nStage {stage + 1}: Training last layers")
            else:
                self.unfreeze_all()
                print(f"\nStage {stage + 1}: Fine-tuning entire model")
            
            # এখানে ট্রেনিং হবে
            # for epoch in range(epochs_per_stage):
            #     train_one_epoch(self.model, dataloader)
            
            print(f"Stage {stage + 1} complete!")

# progressive = ProgressiveUnfreezing(finetuner.model)
# progressive.unfreeze_last_n(10)
print("প্রগ্রেসিভ আনফ্রিজিং সেটআপ করা হয়েছে")
```

## ফিন্যান্সে ট্রান্সফার লার্নিং
```python
class FinancialTransferLearning:
    """ফিন্যান্সিয়াল ডেটার জন্য ট্রান্সফার লার্নিং"""
    
    def __init__(self):
        # ResNet18 ফিন্যান্স চার্টের জন্য
        self.model = models.resnet18(pretrained=True)
        
        # ফিন্যান্সিয়াল চার্ট গ্রেস্কেল → 3 চ্যানেলে কনভার্ট
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        
        # নতুন ক্লাসিফায়ার (স্টক আপ/ডাউন/সাইডওয়েজ)
        self.model.fc = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 3)
        )
        
        self.model = self.model.to(device)
    
    def prepare_chart(self, stock_data, img_size=224):
        """স্টক ডেটা থেকে চার্ট ইমেজ তৈরি"""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from io import BytesIO
        from PIL import Image
        
        fig, ax = plt.subplots(figsize=(img_size/100, img_size/100))
        ax.plot(stock_data, color='black', linewidth=2)
        ax.axis('off')
        
        # ইমেজে রূপান্তর
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        
        img = Image.open(buf).convert('L')  # গ্রেস্কেল
        img = img.resize((img_size, img_size))
        img_tensor = torch.FloatTensor(np.array(img)) / 255.0
        img_tensor = img_tensor.unsqueeze(0).unsqueeze(0)  # (1, 1, H, W)
        
        plt.close()
        return img_tensor
    
    def predict(self, price_sequence):
        """প্রাইস সিকোয়েন্স থেকে প্রেডিকশন"""
        img = self.prepare_chart(price_sequence)
        img = img.to(device)
        
        self.model.eval()
        with torch.no_grad():
            output = self.model(img)
            probs = torch.softmax(output, dim=1)
            pred = torch.argmax(probs, dim=1).item()
        
        labels = ['DOWN', 'SIDEWAYS', 'UP']
        return {
            'prediction': labels[pred],
            'confidence': probs[0, pred].item(),
            'all_probs': {l: probs[0, i].item() for i, l in enumerate(labels)}
        }

# fin_model = FinancialTransferLearning()
# pred = fin_model.predict(np.cumsum(np.random.randn(100)) + 100)
# print(f"Prediction: {pred}")
print("ফিন্যান্সিয়াল ট্রান্সফার লার্নিং মডেল প্রস্তুত")
```

## ট্রান্সফার লার্নিং বেস্ট প্র্যাকটিস
```python
class TransferLearningGuide:
    """ট্রান্সফার লার্নিং গাইডলাইন"""
    
    @staticmethod
    def recommendations():
        guide = """
📌 **কখন কোন পদ্ধতি ব্যবহার করবেন?**

🔹 **আপনার ডেটা ছোট & Pretrained ডেটার মতো:**
   → ফিচার এক্সট্র্যাক্টর + SVM/Linear Classifier

🔹 **আপনার ডেটা মাঝারি:**
   → Fine-tune শেষ কয়েক লেয়ার

🔹 **আপনার ডেটা বড় & আলাদা:**
   → Fine-tune পুরো মডেল (ছোট LR)

🔹 **ফিন্যান্সিয়াল চার্ট:**
   → ImageNet pretrained (ResNet) + Fine-tune শেষ লেয়ার
   → চার্ট প্যাটার্ন ImageNet ইমেজ থেকে আলাদা → Fine-tune বেশি প্রয়োজন

📌 **সাজেস্টেড লার্নিং রেট:**
   - Feature Extraction: lr = 0.001 (classifier)
   - Partial Fine-tune: lr = 0.0001
   - Full Fine-tune: lr = 0.00001
   
📌 **ফিন্যান্সে ব্যবহৃত Pretrained মডেল:**
   - ResNet: চার্ট প্যাটার্ন রিকগনিশন
   - BERT: সেন্টিমেন্ট অ্যানালাইসিস (বাংলা নিউজ)
   - GPT: ফিন্যান্সিয়াল রিপোর্ট জেনারেশন
        """
        print(guide)

TransferLearningGuide.recommendations()
```

## সারসংক্ষেপ
- ট্রান্সফার লার্নিং = Pretrained মডেল + নতুন টাস্ক
- ৩ পদ্ধতি: Feature Extraction, Fine-tuning, Progressive Unfreezing
- ফিন্যান্সে: ImageNet → চার্ট প্যাটার্ন, BERT → সেন্টিমেন্ট
- কম ডেটায় ভালো পারফরম্যান্স
- LR কমিয়ে Fine-tune করা উচিত (1e-5 to 1e-4)