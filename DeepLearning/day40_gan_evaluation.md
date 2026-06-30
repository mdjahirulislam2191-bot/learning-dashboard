# Day 40: GAN ইভালুয়েশন 📊

## GAN ইভালুয়েশন কেন কঠিন?
GAN-এর পারফরম্যান্স মাপা কঠিন কারণ:
- নির্দিষ্ট লস ফাংশন নেই (জিরো-সাম গেম)
- জেনারেটরের আউটপুটের কোয়ালিটি subjectively মাপতে হয়
- মোড কোল্যাপস শনাক্ত করা জরুরি

### ইভালুয়েশন ডাইমেনশন
1. **ফিডেলিটি** (Fidelity): ডেটা কতটা বাস্তবসম্মত?
2. **ডাইভারসিটি** (Diversity): ডেটা কতটা বৈচিত্র্যময়?
3. **কনভারজেন্স** (Convergence): ট্রেনিং কতটা স্টেবল?

### ফিন্যান্স-স্পেসিফিক মেট্রিক্স
- স্ট্যাটিস্টিক্যাল ম্যাচিং
- পোর্টফোলিও ইমপ্যাক্ট
- রিস্ক মেট্রিক ম্যাচিং
- ডাউনস্ট্রিম টাস্ক পারফরম্যান্স

## ইভালুয়েশন মেট্রিক্স

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ks_2samp, wasserstein_distance
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## 1. FID-স্টাইল মেট্রিক

```python
class FIDScore:
    """Frechet Inception Distance-স্টাইল মেট্রিক"""
    def __init__(self):
        pass
    
    def compute_statistics(self, data):
        """ডেটার μ (মিন) এবং Σ (কভারিয়েন্স)"""
        mu = np.mean(data, axis=0)
        sigma = np.cov(data, rowvar=False)
        return mu, sigma
    
    def frechet_distance(self, mu1, sigma1, mu2, sigma2):
        """Frechet Distance / Wasserstein-2 Distance"""
        diff = mu1 - mu2
        covmean, _ = self._sqrtm(sigma1 @ sigma2)
        
        if np.iscomplexobj(covmean):
            covmean = covmean.real
        
        fd = diff @ diff + np.trace(sigma1 + sigma2 - 2 * covmean)
        return fd
    
    def _sqrtm(self, mat):
        """ম্যাট্রিক্স স্কয়ার রুট"""
        eigenvalues, eigenvectors = np.linalg.eigh(mat)
        eigenvalues = np.maximum(eigenvalues, 0)  # সংখ্যাগত স্থিতিশীলতা
        sqrt_mat = eigenvectors @ np.diag(np.sqrt(eigenvalues)) @ eigenvectors.T
        return sqrt_mat, None
    
    def compute(self, real, synthetic):
        mu_r, sigma_r = self.compute_statistics(real)
        mu_s, sigma_s = self.compute_statistics(synthetic)
        return self.frechet_distance(mu_r, sigma_r, mu_s, sigma_s)

# টেস্ট ডেটা
np.random.seed(42)
real = np.random.randn(1000, 50)
synthetic = np.random.randn(1000, 50) * 1.1 + 0.05  # সামান্য ভিন্ন

fid = FIDScore()
fid_score = fid.compute(real, synthetic)
print(f"FID স্কোর: {fid_score:.4f}")
print(f"(ছোট = ভালো, 0 = perfect match)")
```

## 2. মোড কোল্যাপস মেট্রিক্স

```python
class ModeCollapseMetrics:
    """মোড কোল্যাপস ডিটেকশন"""
    
    @staticmethod
    def variance_ratio(synthetic):
        """ভ্যারিয়েন্স রেশিও"""
        var = synthetic.var(axis=0)
        return var / var.max()
    
    @staticmethod
    def fraction_of_low_variance(synthetic, threshold=0.1):
        """কম ভ্যারিয়েন্স ফিচারের অনুপাত"""
        ratio = ModeCollapseMetrics.variance_ratio(synthetic)
        return (ratio < threshold).mean()
    
    @staticmethod
    def pairwise_distance(synthetic):
        """পেয়ারওয়াইজ দূরত্ব (ডাইভারসিটি মাপে)"""
        nn = NearestNeighbors(n_neighbors=2, metric='euclidean')
        nn.fit(synthetic)
        distances, _ = nn.kneighbors(synthetic)
        return distances[:, 1].mean()  # নিজেকে বাদ দিয়ে নিকটতম
    
    @staticmethod
    def coverage(real, synthetic, n_dim=10):
        """কভারেজ স্কোর (PCA প্রজেকশনে)"""
        from sklearn.decomposition import PCA
        pca = PCA(n_components=n_dim)
        pca.fit(real)
        
        real_pca = pca.transform(real)
        syn_pca = pca.transform(synthetic)
        
        # গ্রিড কভারেজ
        coverage_score = 0
        for i in range(n_dim):
            r_min, r_max = real_pca[:, i].min(), real_pca[:, i].max()
            syn_in_range = ((syn_pca[:, i] >= r_min) & (syn_pca[:, i] <= r_max)).mean()
            coverage_score += syn_in_range
        
        return coverage_score / n_dim

# টেস্ট
mcm = ModeCollapseMetrics()

synthetic_1 = np.random.randn(1000, 50)  # নরমাল
synthetic_2 = np.ones((1000, 50)) * 0.5  # মোড কোল্যাপস!

print("মোড কোল্যাপস মেট্রিক্স:")
print(f"{'মেট্রিক':<25} {'নরমাল':<15} {'কোল্যাপসড':<15}")
print("-" * 55)
print(f"{'লো ভ্যারিয়েন্স ফ্রেশন':<25} "
      f"{mcm.fraction_of_low_variance(synthetic_1):<15.4f} "
      f"{mcm.fraction_of_low_variance(synthetic_2):<15.4f}")
print(f"{'পেয়ারওয়াইজ দূরত্ব':<25} "
      f"{mcm.pairwise_distance(synthetic_1):<15.4f} "
      f"{mcm.pairwise_distance(synthetic_2):<15.4f}")
print(f"{'কভারেজ স্কোর':<25} "
      f"{mcm.coverage(real, synthetic_1):<15.4f} "
      f"{mcm.coverage(real, synthetic_2):<15.4f}")
```

## 3. স্ট্যাটিস্টিক্যাল ম্যাচিং

```python
class StatisticalMatching:
    """স্ট্যাটিস্টিক্যাল ম্যাচিং মেট্রিক্স"""
    
    @staticmethod
    def ks_test(real, synthetic):
        """Kolmogorov-Smirnov টেস্ট (ডিস্ট্রিবিউশন ম্যাচিং)"""
        ks_stats = []
        for i in range(real.shape[1]):
            stat, _ = ks_2samp(real[:, i], synthetic[:, i])
            ks_stats.append(stat)
        return np.mean(ks_stats), np.std(ks_stats)
    
    @staticmethod
    def wasserstein_distance(real, synthetic):
        """Wasserstein / Earth Mover's Distance"""
        wd = []
        for i in range(real.shape[1]):
            wd.append(wasserstein_distance(real[:, i], synthetic[:, i]))
        return np.mean(wd), np.std(wd)
    
    @staticmethod
    def moment_matching(real, synthetic):
        """মোমেন্ট ম্যাচিং (প্রথম ৪ মোমেন্ট)"""
        moments = {}
        for name, func in [('মিন', np.mean), ('স্টাড', np.std), 
                           ('স্কিউ', lambda x: np.mean(x**3)), 
                           ('কার্টোসিস', lambda x: np.mean(x**4))]:
            r_m = func(real)
            s_m = func(synthetic)
            rel_diff = abs(r_m - s_m) / (abs(r_m) + 1e-8) * 100
            moments[name] = {'real': r_m, 'syn': s_m, 'diff_%': rel_diff}
        return moments
    
    @staticmethod
    def correlation_structure(real, synthetic):
        """কোরিলেশন স্ট্রাকচার ম্যাচিং"""
        corr_r = np.corrcoef(real[:, :20].T)
        corr_s = np.corrcoef(synthetic[:, :20].T)
        
        diff = np.abs(corr_r - corr_s)
        return diff.mean(), diff.std()
    
    @staticmethod
    def tail_behavior(real, synthetic, percentile=5):
        """টেইল বিহেভিয়র ম্যাচিং"""
        metrics = {}
        for p in [1, 5, 10, 90, 95, 99]:
            real_p = np.percentile(real, p, axis=0).mean()
            syn_p = np.percentile(synthetic, p, axis=0).mean()
            metrics[f'p{p}'] = {'real': real_p, 'syn': syn_p}
        return metrics

# টেস্ট
sm = StatisticalMatching()
real = np.random.randn(2000, 50)
synth = np.random.randn(2000, 50) * 1.1 + 0.05

ks_mean, ks_std = sm.ks_test(real, synth)
wd_mean, wd_std = sm.wasserstein_distance(real, synth)
corr_mean, corr_std = sm.correlation_structure(real, synth)

print(f"{'মেট্রিক':<30} {'মিন':<15} {'স্টাড':<15}")
print("-" * 60)
print(f"{'KS স্ট্যাট':<30} {ks_mean:<15.4f} {ks_std:<15.4f}")
print(f"{'Wasserstein D':<30} {wd_mean:<15.4f} {wd_std:<15.4f}")
print(f"{'কোরিলেশন ডিফ':<30} {corr_mean:<15.4f} {corr_std:<15.4f}")

moments = sm.moment_matching(real, synth)
print(f"\nমোমেন্ট ম্যাচিং:")
for name, vals in moments.items():
    print(f"  {name}: ডিফ={vals['diff_%']:.2f}%")

tails = sm.tail_behavior(real, synth)
print(f"\nটেইল বিহেভিয়র:")
for p, vals in tails.items():
    print(f"  {p}: রিয়েল={vals['real']:.4f}, সিন্থ={vals['syn']:.4f}")
```

## 4. ডাউনস্ট্রিম ইভালুয়েশন

```python
class DownstreamEvaluation:
    """ডাউনস্ট্রিম টাস্কে GAN ইভালুয়েশন"""
    
    @staticmethod
    def train_on_synthetic_test_on_real(real, synthetic, task='regression'):
        """সিন্থেটিক ডেটায় ট্রেন, রিয়েলে টেস্ট"""
        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score, accuracy_score
        
        n_real = len(real)
        n_syn = len(synthetic)
        
        if task == 'regression':
            y = real[:, 0] + 0.5 * real[:, 1] + np.random.randn(n_real) * 0.1
            y_syn = synthetic[:, 0] + 0.5 * synthetic[:, 1] + np.random.randn(n_syn) * 0.1
            model = RandomForestRegressor(n_estimators=50, max_depth=5)
            metric = r2_score
        else:
            y = (real[:, 0] + real[:, 1] > 0).astype(int)
            y_syn = (synthetic[:, 0] + synthetic[:, 1] > 0).astype(int)
            model = RandomForestClassifier(n_estimators=50, max_depth=5)
            metric = accuracy_score
        
        # রিয়েল টেস্ট সেট
        _, X_test, _, y_test = train_test_split(real[:, 2:], y, test_size=0.2, random_state=42)
        
        # শুধু সিন্থেটিকে ট্রেন
        X_syn, y_syn_clean = synthetic[:, 2:], y_syn
        model.fit(X_syn, y_syn_clean)
        syn_score = metric(y_test, model.predict(X_test))
        
        # শুধু রিয়েলে ট্রেন
        X_real_train, _, y_real_train, _ = train_test_split(
            real[:, 2:], y, test_size=0.2, random_state=42)
        model.fit(X_real_train, y_real_train)
        real_score = metric(y_test, model.predict(X_test))
        
        # রিয়েল + সিন্থেটিক
        X_combined = np.vstack([X_real_train, X_syn])
        y_combined = np.hstack([y_real_train, y_syn_clean])
        model.fit(X_combined, y_combined)
        combined_score = metric(y_test, model.predict(X_test))
        
        return {
            'real_only': real_score,
            'syn_only': syn_score,
            'combined': combined_score,
            'syn_vs_real_ratio': syn_score / real_score if real_score != 0 else 0
        }

# টেস্ট
de = DownstreamEvaluation()
results = de.train_on_synthetic_test_on_real(real, synth)

print(f"\nডাউনস্ট্রিম ইভালুয়েশন:")
print(f"{'ট্রেনিং সেট':<25} {'স্কোর':<15}")
print("-" * 40)
for k, v in results.items():
    print(f"{k:<25} {v:<15.4f}")
```

## 5. GAN ট্রেনিং কনভারজেন্স

```python
class ConvergenceMetrics:
    """GAN কনভারজেন্স মনিটরিং"""
    
    @staticmethod
    def discriminator_accuracy(D, real, fake):
        """ডিসক্রিমিনেটরের অ্যাকুরেসি ট্র্যাক"""
        with torch.no_grad():
            d_real = D(real).mean().item()
            d_fake = D(fake).mean().item()
        return {
            'd_real_accuracy': d_real,
            'd_fake_accuracy': 1 - d_fake,
            'd_avg_accuracy': (d_real + 1 - d_fake) / 2
        }
    
    @staticmethod
    def gradient_norm(model):
        """গ্র্যাডিয়েন্ট নর্ম (স্টেবিলিটি ইন্ডিকেটর)"""
        total_norm = 0
        for p in model.parameters():
            if p.grad is not None:
                total_norm += p.grad.norm().item() ** 2
        return total_norm ** 0.5
    
    @staticmethod
    def generated_variance_trend(G, noise_dim=128, n_samples=500):
        """জেনারেটেড ডেটার ভ্যারিয়েন্স ট্র্যাক"""
        with torch.no_grad():
            z = torch.randn(n_samples, noise_dim).to(device)
            fake = G(z).cpu().numpy()
        return fake.var(axis=0).mean()

# সিমুলেটেড কনভারজেন্স ডেটা
print("\nকনভারজেন্স মেট্রিক্স (সিমুলেটেড):")
print(f"{'ইপক':<10} {'D অ্যাকুরেসি':<15} {'G ভ্যারিয়েন্স':<15} {'মোড কোল্যাপস':<15}")
print("-" * 55)

for epoch in [0, 25, 50, 75, 100]:
    # সিমুলেটেড ভ্যালু
    d_acc = 0.9 - 0.4 * (epoch/100)  # ধীরে ধীরে কমে
    g_var = 0.5 + 0.5 * (epoch/100)  # ধীরে ধীরে বাড়ে
    mode_collapse = '❌' if epoch < 50 else '✅'
    print(f"{epoch:<10} {d_acc:<15.4f} {g_var:<15.4f} {mode_collapse:<15}")

print("\n✅ কনভারজেন্স: D অ্যাকুরেসি ~0.5, G ভ্যারিয়েন্স স্থিতিশীল")
```

## 6. কম্প্রিহেন্সিভ GAN রিপোর্ট

```python
def gan_evaluation_report(real, synthetic, G=None, D=None):
    """সম্পূর্ণ GAN ইভালুয়েশন রিপোর্ট"""
    
    print("=" * 60)
    print("📊 GAN ইভালুয়েশন রিপোর্ট")
    print("=" * 60)
    
    # 1. ফিডেলিটি
    fid_score = FIDScore().compute(real, synthetic)
    print(f"\n1. ফিডেলিটি (FID): {fid_score:.4f}")
    print(f"   {'✅ ভালো' if fid_score < 10 else '⚠️ মাঝারি' if fid_score < 50 else '❌ খারাপ'}")
    
    # 2. ডাইভারসিটি
    mcm = ModeCollapseMetrics()
    diversity = mcm.pairwise_distance(synthetic)
    coverage = mcm.coverage(real, synthetic)
    low_var = mcm.fraction_of_low_variance(synthetic)
    
    print(f"\n2. ডাইভারসিটি:")
    print(f"   পেয়ারওয়াইজ দূরত্ব: {diversity:.4f}")
    print(f"   কভারেজ স্কোর: {coverage:.4f}")
    print(f"   লো ভ্যারিয়েন্স ফিচার: {low_var:.2%}")
    
    # 3. স্ট্যাটিস্টিক্যাল ম্যাচিং
    sm = StatisticalMatching()
    ks, _ = sm.ks_test(real, synthetic)
    wd, _ = sm.wasserstein_distance(real, synthetic)
    
    print(f"\n3. স্ট্যাটিস্টিক্যাল ম্যাচিং:")
    print(f"   KS স্ট্যাট: {ks:.4f}")
    print(f"   Wasserstein: {wd:.4f}")
    
    # 4. ডাউনস্ট্রিম
    de = DownstreamEvaluation()
    try:
        downstream = de.train_on_synthetic_test_on_real(real, synthetic)
        print(f"\n4. ডাউনস্ট্রিম পারফরম্যান্স:")
        print(f"   রিয়েল কোয়ালিটি রেশিও: {downstream['syn_vs_real_ratio']:.2%}")
    except:
        print(f"\n4. ডাউনস্ট্রিম: স্কিপ")
    
    # 5. সারাংশ
    print(f"\n5. 📋 সারাংশ:")
    score = 0
    score += 10 if fid_score < 10 else 5 if fid_score < 50 else 0
    score += 10 if low_var < 0.1 else 5 if low_var < 0.3 else 0
    score += 10 if ks < 0.1 else 5 if ks < 0.2 else 0
    
    print(f"   GAN কোয়ালিটি স্কোর: {score}/30")
    if score >= 25:
        print("   রেটিং: 🏆 চমৎকার")
    elif score >= 15:
        print("   রেটিং: ⭐ ভালো")
    else:
        print("   রেটিং: 🔄 উন্নতি প্রয়োজন")

# রান রিপোর্ট
gan_evaluation_report(real, synth)
```

## সারাংশ
- GAN ইভালুয়েশন মাল্টি-ডাইমেনশনাল: ফিডেলিটি, ডাইভারসিটি, কনভারজেন্স
- FID, KS টেস্ট, Wasserstein Distance প্রধান মেট্রিক্স
- মোড কোল্যাপস ডিটেকশন জরুরি (ভ্যারিয়েন্স, পেয়ারওয়াইজ দূরত্ব)
- ডাউনস্ট্রিম টাস্ক ইভালুয়েশন সবচেয়ে প্র্যাকটিক্যাল
- ফিন্যান্সে স্ট্যাটিস্টিক্যাল ম্যাচিং + পোর্টফোলিও ইমপ্যাক্ট গুরুত্বপূর্ণ
- কোয়ালিটি স্কোর 0-30 রেঞ্জে সমগ্রিক মূল্যায়ন