# Day 02: Python for Data Science Recap
## ডেটা সায়েন্সের জন্য পাইথন রিক্যাপ

### পাইথন ডেটা টাইপসমূহ:
```python
# মৌলিক ডেটা টাইপ
integer_num = 42          # int
float_num = 3.1416        # float
complex_num = 2 + 3j      # complex
text = "ডেটা সায়েন্স"     # str
boolean = True            # bool

# কালেকশন টাইপ
my_list = [1, 2, 3, 4, 5]           # list - পরিবর্তনযোগ্য
my_tuple = (1, 2, 3)                # tuple - অপরিবর্তনযোগ্য
my_dict = {'a': 1, 'b': 2}          # dict - কী-ভ্যালু পেয়ার
my_set = {1, 2, 3, 4, 5}            # set - ইউনিক উপাদান

print(f"লিস্ট: {my_list}")
print(f"টাপল: {my_tuple}")
print(f"ডিকশনারি: {my_dict}")
print(f"সেট: {my_set}")
```

### লিস্ট কম্প্রিহেনশন:
```python
# লিস্ট কম্প্রিহেনশন - ডেটা সায়েন্সে খুবই কার্যকর
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [n**2 for n in numbers]
evens = [n for n in numbers if n % 2 == 0]
even_squares = [n**2 for n in numbers if n % 2 == 0]
print(f"বর্গ: {squares}")
print(f"জোড় সংখ্যা: {evens}")
print(f"জোড় সংখ্যার বর্গ: {even_squares}")

# Nested list comprehension
matrix = [[j for j in range(3)] for i in range(3)]
print(f"ম্যাট্রিক্স: {matrix}")
```

### ফাংশন ও ল্যাম্বডা:
```python
# সাধারণ ফাংশন
def mean(numbers):
    """গড় (mean) বের করার ফাংশন"""
    return sum(numbers) / len(numbers)

def std_dev(numbers):
    """স্ট্যান্ডার্ড ডিভিয়েশন"""
    mu = mean(numbers)
    variance = sum((x - mu)**2 for x in numbers) / len(numbers)
    return variance ** 0.5

# ল্যাম্বডা ফাংশন - এক লাইনের ফাংশন
square = lambda x: x ** 2
add = lambda a, b: a + b

data = [10, 20, 30, 40, 50]
print(f"গড়: {mean(data):.2f}")
print(f"স্ট্যান্ডার্ড ডিভিয়েশন: {std_dev(data):.2f}")
print(f"ল্যাম্বডা স্কয়ার: {square(5)}")

# map, filter, reduce
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x*2, nums))
filtered = list(filter(lambda x: x > 2, nums))
print(f"ম্যাপ (x2): {doubled}")
print(f"ফিল্টার (>2): {filtered}")
```

### NumPy ও Pandas-এর ভূমিকা:
```python
import numpy as np
import pandas as pd

# NumPy array
arr = np.array([1, 2, 3, 4, 5])
print(f"NumPy Array: {arr}")
print(f"Array গড়: {arr.mean():.2f}")
print(f"Array Std: {arr.std():.2f}")

# Pandas Series ও DataFrame
s = pd.Series([1, 2, 3, 4, 5], name='মান')
print(f"\nPandas Series:\n{s}")

df = pd.DataFrame({
    'ফিচার': ['A', 'B', 'C', 'D', 'E'],
    'মান': [10, 20, 30, 40, 50],
    'বর্গ': [100, 400, 900, 1600, 2500]
})
print(f"\nPandas DataFrame:\n{df}")
```

### ফাইল I/O:
```python
import json
import csv

# CSV রাইটিং
with open('sample_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['নাম', 'বয়স', 'শহর'])
    writer.writerow(['আলিফ', 25, 'ঢাকা'])
    writer.writerow(['বর্ণা', 30, 'চট্টগ্রাম'])

# CSV রিডিং
df = pd.read_csv('sample_data.csv')
print("CSV থেকে ডেটা:\n", df)

# JSON
data = {'নাম': 'আলিফ', 'বয়স': 25, 'স্কোর': [85, 90, 78]}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
print("JSON থেকে ডেটা:", loaded_data)
```

### Error Handling:
```python
def safe_divide(a, b):
    """নিরাপদ ডিভিশন ফাংশন"""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: শূন্য দিয়ে ভাগ করা যায় না!")
        return None
    except TypeError as e:
        print(f"Error: ভুল ডেটা টাইপ - {e}")
        return None
    else:
        return result
    finally:
        print("ফাংশন এক্সিকিউশন শেষ")

print(safe_divide(10, 2))
print(safe_divide(10, 0))
```

### সারসংক্ষেপ:
- পাইথনের মৌলিক ডেটা টাইপ ও কালেকশন
- লিস্ট কম্প্রিহেনশন ও ফাংশন
- NumPy ও Pandas-এর প্রাথমিক ধারণা
- ফাইল I/O এবং Error Handling
- আগামী দিনে আমরা NumPy-তে গভীরভাবে কাজ করব