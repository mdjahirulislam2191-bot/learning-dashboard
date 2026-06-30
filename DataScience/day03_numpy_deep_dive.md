# Day 03: NumPy ডিপ ডাইভ
## NumPy Deep Dive

### NumPy কী?
NumPy (Numerical Python) হলো পাইথনে সংখ্যাত্মক কম্পিউটিংয়ের মূল লাইব্রেরি। এটি দ্রুতগতির মাল্টি-ডাইমেনশনাল অ্যারে অপারেশন সাপোর্ট করে।

```python
import numpy as np

print(f"NumPy ভার্সন: {np.__version__}")
```

### NumPy অ্যারে তৈরি:
```python
# বিভিন্ন উপায়ে অ্যারে তৈরি
arr1 = np.array([1, 2, 3, 4, 5])           # 1D
arr2 = np.array([[1, 2, 3], [4, 5, 6]])    # 2D
arr3 = np.zeros((3, 4))                     # শূন্য দিয়ে
arr4 = np.ones((2, 3))                      # এক দিয়ে
arr5 = np.full((2, 2), 7)                   # নির্দিষ্ট মান দিয়ে
arr6 = np.eye(3)                            # আইডেন্টিটি ম্যাট্রিক্স
arr7 = np.random.random((2, 3))             # র্যান্ডম
arr8 = np.arange(0, 10, 2)                  # রেঞ্জ দিয়ে
arr9 = np.linspace(0, 1, 5)                 # সমান ব্যবধানে

print(f"1D অ্যারে: {arr1}")
print(f"2D অ্যারে:\n{arr2}")
print(f"Zeros:\n{arr3}")
print(f"Ones:\n{arr4}")
print(f"আইডেন্টিটি:\n{arr6}")
print(f"Arange: {arr8}")
print(f"Linspace: {arr9}")
```

### অ্যারে অ্যাট্রিবিউট:
```python
arr = np.random.randint(0, 10, (3, 4))
print(f"অ্যারে:\n{arr}")
print(f"Shape: {arr.shape}")        # আকৃতি
print(f"Dimension: {arr.ndim}")     # মাত্রা
print(f"Size: {arr.size}")          # মোট উপাদান
print(f"Data Type: {arr.dtype}")    # ডেটা টাইপ
print(f"Item Size: {arr.itemsize} bytes")  # প্রতিটি উপাদানের সাইজ
print(f"Memory: {arr.nbytes} bytes")       # মোট মেমোরি
```

### অ্যারে ইনডেক্সিং ও স্লাইসিং:
```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print(f"মূল অ্যারে:\n{arr}")
print(f"প্রথম সারি: {arr[0]}")
print(f"দ্বিতীয় কলাম: {arr[:, 1]}")
print(f"সাব-অ্যারে (0:2, 1:3):\n{arr[0:2, 1:3]}")
print(f"শেষ উপাদান: {arr[-1, -1]}")
print(f"প্রথম কলাম ব্যতীত সব: {arr[:, 1:]}")

# ফ্যান্সি ইনডেক্সিং
rows = np.array([0, 2])
cols = np.array([1, 3])
print(f"ফ্যান্সি ইনডেক্সিং: {arr[rows, cols]}")

# বুলিয়ান ইনডেক্সিং
print(f"৫-এর বেশি: {arr[arr > 5]}")
print(f"জোড় সংখ্যা: {arr[arr % 2 == 0]}")
```

### অ্যারে অপারেশন:
```python
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# বেসিক অপারেশন
print(f"যোগ: {a + b}")
print(f"বিয়োগ: {a - b}")
print(f"গুণ: {a * b}")
print(f"ভাগ: {a / b}")
print(f"পাওয়ার: {a ** 2}")

# ইউনিভার্সাল ফাংশন (ufunc)
print(f"sqrt: {np.sqrt(a)}")
print(f"exp: {np.exp(a)}")
print(f"log: {np.log(a)}")
print(f"sin: {np.sin(a)}")
print(f"cos: {np.cos(a)}")
print(f"abs: {np.abs([-1, -2, -3])}")
```

### ব্রডকাস্টিং:
```python
# ব্রডকাস্টিং - বিভিন্ন shape-এর অ্যারে নিয়ে অপারেশন
a = np.array([[1, 2, 3],
              [4, 5, 6]])
b = np.array([10, 20, 30])

print(f"a:\n{a}")
print(f"b: {b}")
print(f"a + b (ব্রডকাস্টিং):\n{a + b}")

# স্কেলার ব্রডকাস্টিং
print(f"a + 100:\n{a + 100}")
print(f"a * 2:\n{a * 2}")
```

### স্ট্যাটিস্টিক্যাল ফাংশন:
```python
data = np.random.normal(50, 10, 1000)  # ১০০০ নমুনা, গড়=৫০, std=১০

print(f"Mean: {np.mean(data):.2f}")
print(f"Median: {np.median(data):.2f}")
print(f"Std Dev: {np.std(data):.2f}")
print(f"Variance: {np.var(data):.2f}")
print(f"Min: {np.min(data):.2f}")
print(f"Max: {np.max(data):.2f}")
print(f"25th Percentile: {np.percentile(data, 25):.2f}")
print(f"75th Percentile: {np.percentile(data, 75):.2f}")
print(f"Sum: {np.sum(data):.2f}")
print(f"Product: {np.prod(data[:10]):.2f}")
print(f"Cumulative Sum: {np.cumsum(data[:10])}")
```

### লিনিয়ার আলজেব্রা:
```python
# ম্যাট্রিক্স অপারেশন
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"A:\n{A}")
print(f"B:\n{B}")
print(f"Dot Product:\n{np.dot(A, B)}")
print(f"Matrix Multiply:\n{A @ B}")
print(f"Transpose of A:\n{A.T}")
print(f"Determinant: {np.linalg.det(A):.2f}")
print(f"Inverse:\n{np.linalg.inv(A)}")
print(f"Eigenvalues: {np.linalg.eigvals(A)}")

# লিনিয়ার রিগ্রেশন সমাধান
X = np.array([[1, 1], [1, 2], [1, 3]])
y = np.array([1, 2, 3])
coeff = np.linalg.lstsq(X, y, rcond=None)[0]
print(f"Linear Regression Coefficients: {coeff}")
```

### রি shaping ও রিসাইজিং:
```python
arr = np.arange(12)
print(f"মূল: {arr}")
print(f"Reshape (3,4):\n{arr.reshape(3, 4)}")
print(f"Reshape (2,6):\n{arr.reshape(2, 6)}")
print(f"Flatten: {arr.reshape(3, 4).flatten()}")
print(f"Ravel: {arr.reshape(3, 4).ravel()}")

# স্ট্যাকিং
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"Vertical Stack:\n{np.vstack([a, b])}")
print(f"Horizontal Stack:\n{np.hstack([a, b])}")

# স্প্লিটিং
arr = np.arange(12).reshape(3, 4)
print(f"Split:\n{np.split(arr, 3)}")
print(f"hsplit:\n{np.hsplit(arr, 2)}")
```

### র্যান্ডম নাম্বার জেনারেশন:
```python
np.random.seed(42)  # reproducible results

print(f"Uniform [0,1]: {np.random.random(5)}")
print(f"Randint: {np.random.randint(0, 100, 10)}")
print(f"Normal: {np.random.normal(0, 1, 5)}")
print(f"Binomial: {np.random.binomial(10, 0.5, 5)}")
print(f"Choice: {np.random.choice(['A', 'B', 'C'], 5)}")
print(f"Shuffle: {np.random.permutation([1, 2, 3, 4, 5])}")
```

### পারফরম্যান্স টিপস:
```python
# Python লিস্ট vs NumPy অ্যারে - স্পিড টেস্ট
import time

size = 1000000
py_list = list(range(size))
np_arr = np.arange(size)

# Python লিস্টের সাথে
start = time.time()
py_result = [x**2 for x in py_list]
py_time = time.time() - start

# NumPy অ্যারের সাথে
start = time.time()
np_result = np_arr ** 2
np_time = time.time() - start

print(f"Python List Time: {py_time:.4f} sec")
print(f"NumPy Array Time: {np_time:.4f} sec")
print(f"NumPy is {py_time/np_time:.1f}x faster!")
```

### সারসংক্ষেপ:
- NumPy অ্যারে তৈরি ও ম্যানিপুলেশন
- ইনডেক্সিং, স্লাইসিং, ব্রডকাস্টিং
- স্ট্যাটিস্টিক্যাল ও লিনিয়ার আলজেব্রা অপারেশন
- রি shaping, স্ট্যাকিং, স্প্লিটিং
- র্যান্ডম নাম্বার জেনারেশন
- পারফরম্যান্স অপটিমাইজেশন