# Day 08: পলিনমিয়াল রিগ্রেশন
## Polynomial Regression

### পলিনমিয়াল রিগ্রেশন কি?
যখন ডেটা লিনিয়ার না হয়, তখন পলিনমিয়াল রিগ্রেশন ব্যবহার করা হয়। এটি ফিচারগুলোর পলিনমিয়াল (x², x³, ইত্যাদি) তৈরি করে।

**সমীকরণ:** y = β₀ + β₁x + β₂x² + β₃x³ + ... + ε

### ফাইন্যান্স উদাহরণ: রিটার্ন প্রেডিকশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

# অ-লিনিয়ার ফাইন্যান্স ডেটা
np.random.seed(42)
n = 300
X = np.linspace(0, 10, n).reshape(-1, 1)

# অ-লিনিয়ার সম্পর্ক (যেমন: diminishing returns)
y = 0.5 * X.squeeze()**2 - 0.1 * X.squeeze()**3 + np.random.randn(n) * 2
y = y + 50  # অফসেট

print("ডেটা তৈরি সম্পন্ন!")
print(f"X রেঞ্জ: {X.min():.1f} - {X.max():.1f}")
print(f"y রেঞ্জ: {y.min():.1f} - {y.max():.1f}")
```

### পলিনমিয়াল ফিচার তৈরি
```python
# বিভিন্ন ডিগ্রি ট্রাই করা
degrees = [1, 2, 3, 5, 10]
colors = ['blue', 'green', 'red', 'orange', 'purple']

X_plot = np.linspace(0, 10, 100).reshape(-1, 1)

plt.figure(figsize=(12, 6))
plt.scatter(X, y, alpha=0.3, label='Actual Data')

for degree, color in zip(degrees, colors):
    # পলিনমিয়াল ফিচার
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    # মডেল
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # প্রেডিকশন
    X_plot_poly = poly.transform(X_plot)
    y_plot = model.predict(X_plot_poly)
    
    # Score
    r2 = r2_score(y, model.predict(X_poly))
    
    plt.plot(X_plot, y_plot, color, label=f'Degree {degree} (R²={r2:.3f})', linewidth=2)

plt.xlabel('Investment Amount (x)')
plt.ylabel('Return (y)')
plt.title('পলিনমিয়াল রিগ্রেশন - বিভিন্ন ডিগ্রি')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### Overfitting এবং Underfitting
```python
print("📊 Degree Analysis:")
for degree in degrees:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_poly, y, test_size=0.2, random_state=42
    )
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    train_r2 = r2_score(y_train, model.predict(X_train))
    test_r2 = r2_score(y_test, model.predict(X_test))
    
    print(f"Degree {degree:2d}: Train R²={train_r2:.4f}, Test R²={test_r2:.4f}", 
          end="")
    if train_r2 > 0.95 and test_r2 < 0.7:
        print(" ⚠️ Overfitting!")
    elif train_r2 < 0.3:
        print(" ⚠️ Underfitting!")
    else:
        print(" ✅ Good fit")
```

### পলিনমিয়াল রিগ্রেশন - ফাইন্যান্সিয়াল উদাহরণ
```python
# diminishing returns on marketing spend
np.random.seed(42)
n = 200

marketing_spend = np.random.uniform(0, 100, n).reshape(-1, 1)

# অ-লিনিয়ার সম্পর্ক: প্রথমে বৃদ্ধি, পরে চ্যাপ্টা
revenue = (
    100 + 
    3 * marketing_spend.squeeze() - 
    0.02 * marketing_spend.squeeze()**2 +
    np.random.randn(n) * 5
)
revenue = np.maximum(revenue, 0)  # নেগেটিভ না হওয়া

# পাইপলাইন ব্যবহার
degree = 2
pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=degree, include_bias=False)),
    ('linear', LinearRegression())
])

X_train, X_test, y_train, y_test = train_test_split(
    marketing_spend, revenue, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"\n📈 Marketing ROI Model (Degree {degree}):")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

# Optimal spend point
coefs = pipeline.named_steps['linear'].coef_
intercept = pipeline.named_steps['linear'].intercept_
print(f"\nEquation: Revenue = {intercept:.2f} + {coefs[0]:.2f}*spend + {coefs[1]:.4f}*spend²")

if coefs[1] < 0:  # নেগেটিভ কোএফিসিয়েন্ট = diminishing returns
    optimal_spend = -coefs[0] / (2 * coefs[1])
    optimal_revenue = intercept + coefs[0]*optimal_spend + coefs[1]*optimal_spend**2
    print(f"\n💡 Optimal Marketing Spend: ${optimal_spend:.1f}k")
    print(f"   Expected Revenue: ${optimal_revenue:.1f}k")
```

### Overfitting এড়ানোর উপায়
```python
# 1. Cross-validation ব্যবহার
from sklearn.model_selection import cross_val_score

for degree in [2, 3, 4, 5]:
    pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=degree, include_bias=False)),
        ('linear', LinearRegression())
    ])
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2')
    print(f"Degree {degree}: CV R² = {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
```

### Underfitting vs Overfitting Graph
```python
print("""
📊 Bias-Variance Tradeoff:

Underfitting        Good Fit           Overfitting
(High Bias)                         (High Variance)

High Train Error   Low Train Error   Very Low Train Error
High Test Error    Low Test Error    High Test Error
Simple Model       Balanced          Complex Model

Solution:          Solution:         Solution:
↑ Model Complexity ↑ Data            ↑ Regularization
                   ↑ Features        ↑ Training Data
""")
```

### সারসংক্ষেপ
পলিনমিয়াল রিগ্রেশন অ-লিনিয়ার ডেটার জন্য লিনিয়ার রিগ্রেশনকে এক্সটেন্ড করে। সঠিক ডিগ্রি নির্বাচন করা গুরুত্বপূর্ণ - কম ডিগ্রি = underfitting, বেশি ডিগ্রি = overfitting। ফাইন্যান্সে diminishing returns, growth curves ইত্যাদি মডেল করতে ব্যবহার করা হয়।