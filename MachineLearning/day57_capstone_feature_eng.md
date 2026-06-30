# Day 57: ক্যাপস্টোন প্রোজেক্ট — ফিচার ইঞ্জিনিয়ারিং
## Capstone Project: Feature Engineering

### ফিচার ইঞ্জিনিয়ারিং কি?
কাঁচা ডেটা থেকে মডেলের জন্য উপযোগী ফিচার তৈরি করার প্রক্রিয়া। ভালো ফিচার ভালো মডেলের চাবিকাঠি।

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import (
    PolynomialFeatures, StandardScaler, 
    LabelEncoder, OneHotEncoder
)
from sklearn.feature_selection import (
    SelectKBest, f_regression, mutual_info_regression
)
import joblib
import warnings
warnings.filterwarnings('ignore')
```

### প্রিপেয়ারড ডেটা লোড

```python
# আগের দিনের প্রস্তুত ডেটা লোড
X_train = joblib.load('X_train.pkl')
X_test = joblib.load('X_test.pkl')
y_train = joblib.load('y_train.pkl')
y_test = joblib.load('y_test.pkl')

print("ট্রেইন:", X_train.shape)
print("টেস্ট:", X_test.shape)
print("\nফিচার লিস্ট:")
print(X_train.columns.tolist())
```

### ১. পলিনোমিয়াল ফিচার (ইন্টারঅ্যাকশন)

```python
def create_polynomial_features(X, degree=2, interaction_only=True):
    """
    পলিনোমিয়াল ও ইন্টারঅ্যাকশন ফিচার তৈরি
    
    interaction_only=True: শুধু ইন্টারঅ্যাকশন (x1*x2), x² না
    """
    poly = PolynomialFeatures(
        degree=degree, 
        interaction_only=interaction_only,
        include_bias=False
    )
    
    numeric_cols = ['area', 'age', 'distance_center', 'location_score']
    X_numeric = X[numeric_cols]
    
    X_poly = poly.fit_transform(X_numeric)
    feature_names = poly.get_feature_names_out(numeric_cols)
    
    X_poly_df = pd.DataFrame(
        X_poly, 
        columns=feature_names,
        index=X.index
    )
    
    # মূল ফিচারের সাথে যোগ
    X_enhanced = pd.concat([X, X_poly_df], axis=1)
    
    return X_enhanced, poly

X_train_poly, poly = create_polynomial_features(X_train)
X_test_poly = pd.concat([
    X_test,
    pd.DataFrame(
        poly.transform(X_test[['area', 'age', 'distance_center', 'location_score']]),
        columns=poly.get_feature_names_out(['area', 'age', 'distance_center', 'location_score']),
        index=X_test.index
    )
], axis=1)

print("পলিনোমিয়াল ফিচার যোগের পর:")
print(f"ফিচার সংখ্যা: {X_train_poly.shape[1]}")
print("\nনতুন ফিচার:")
print([c for c in X_train_poly.columns if c not in X_train.columns][:10])
```

### ২. বিনিং ও ডিসক্রিটাইজেশন

```python
def create_binned_features(X):
    """কন্টিনিউয়াস ফিচারকে বিনে বিভক্ত করা"""
    X_binned = X.copy()
    
    # এজ বিনিং
    X_binned['age_group'] = pd.cut(
        X['age'], 
        bins=[0, 5, 10, 20, 30, 50],
        labels=['new', 'relatively_new', 'moderate', 'old', 'very_old']
    )
    
    # দূরত্ব বিনিং
    X_binned['distance_category'] = pd.cut(
        X['distance_center'],
        bins=[0, 2, 5, 10, 20],
        labels=['very_close', 'close', 'medium', 'far']
    )
    
    # এরিয়া বিনিং
    X_binned['size_category'] = pd.cut(
        X['area'],
        bins=[0, 1000, 1500, 2000, 3000],
        labels=['small', 'medium', 'large', 'very_large']
    )
    
    return X_binned

X_train_binned = create_binned_features(X_train_poly)
X_test_binned = create_binned_features(X_test_poly)

print("বিনিংয়ের পর ক্যাটাগরি ডিস্ট্রিবিউশন:")
for col in ['age_group', 'distance_category', 'size_category']:
    print(f"\n{col}:")
    print(X_train_binned[col].value_counts())
```

### ৩. রেশিও ও কম্বিনেশন ফিচার

```python
def create_ratio_features(X):
    """রেশিও এবং কম্বিনেশন ফিচার তৈরি"""
    X_ratio = X.copy()
    
    # এলাকা প্রতি রুম
    X_ratio['area_per_room'] = X['area'] / (X['bedrooms'] + X['bathrooms'])
    
    # ফ্লোর রেশিও
    X_ratio['floor_ratio'] = X['floor'] / (X['total_floors'] + 1)
    
    # লোকেশন স্কোর / দূরত্ব
    X_ratio['location_efficiency'] = X['location_score'] / \
                                      (X['distance_center'] + 0.1)
    
    # সুবিধা স্কোর
    X_ratio['amenities_score'] = X['has_garage'] + X['has_garden']
    
    # মোট রুম
    X_ratio['total_rooms'] = X['bedrooms'] + X['bathrooms']
    
    # বাড়ির ধরন (ছোট/বড়)
    X_ratio['is_large_house'] = (X['area'] > 2000).astype(int)
    
    # প্রিমিয়াম লোকেশন
    X_ratio['is_premium_location'] = (
        (X['location_score'] > 7) & 
        (X['distance_center'] < 3)
    ).astype(int)
    
    return X_ratio

X_train_ratio = create_ratio_features(X_train_binned)
X_test_ratio = create_ratio_features(X_test_binned)

print("নতুন রেশিও ফিচার:")
ratio_features = ['area_per_room', 'floor_ratio', 'location_efficiency',
                  'amenities_score', 'total_rooms', 'is_large_house',
                  'is_premium_location']
for col in ratio_features:
    print(f"\n{col}:")
    print(X_train_ratio[col].describe())
```

### ৪. এনকোডিং

```python
def encode_categorical_features(X_train, X_test):
    """ক্যাটাগোরিকাল ফিচার এনকোডিং"""
    # ক্যাটেগরি কলাম আইডেন্টিফাই
    cat_cols = X_train.select_dtypes(include=['category', 'object']).columns
    
    X_train_encoded = X_train.copy()
    X_test_encoded = X_test.copy()
    
    # One-Hot Encoding
    for col in cat_cols:
        # ডামি ভেরিয়েবল
        dummies_train = pd.get_dummies(X_train[col], prefix=col, drop_first=True)
        dummies_test = pd.get_dummies(X_test[col], prefix=col, drop_first=True)
        
        # ট্রেইন ও টেস্টে একই কলাম নিশ্চিত
        missing_cols = set(dummies_train.columns) - set(dummies_test.columns)
        for c in missing_cols:
            dummies_test[c] = 0
        dummies_test = dummies_test[dummies_train.columns]
        
        # মূল ডেটার সাথে যোগ
        X_train_encoded = pd.concat([X_train_encoded, dummies_train], axis=1)
        X_test_encoded = pd.concat([X_test_encoded, dummies_test], axis=1)
        
        # মূল ক্যাটাগরি কলাম ড্রপ
        X_train_encoded.drop(col, axis=1, inplace=True)
        X_test_encoded.drop(col, axis=1, inplace=True)
    
    return X_train_encoded, X_test_encoded

X_train_encoded, X_test_encoded = encode_categorical_features(
    X_train_ratio, X_test_ratio
)

print(f"এনকোডিং এর পর ফিচার সংখ্যা:")
print(f"  ট্রেইন: {X_train_encoded.shape[1]}")
print(f"  টেস্ট: {X_test_encoded.shape[1]}")
```

### ৫. ফিচার সিলেকশন

```python
def select_best_features(X_train, y_train, X_test, k=20):
    """শীর্ষ k ফিচার সিলেক্ট করা"""
    
    # মিউচুয়াল ইনফরমেশন
    mi_scores = mutual_info_regression(X_train, y_train, random_state=42)
    mi_selector = SelectKBest(mutual_info_regression, k=k)
    mi_selector.fit(X_train, y_train)
    
    # ফিচার স্কোর
    feature_scores = pd.DataFrame({
        'feature': X_train.columns,
        'mi_score': mi_scores,
        'selected': mi_selector.get_support()
    }).sort_values('mi_score', ascending=False)
    
    print("শীর্ষ ফিচার (মিউচুয়াল ইনফরমেশন):")
    print(feature_scores.head(k))
    
    # সিলেক্টেড ফিচার
    selected_features = feature_scores[feature_scores['selected']]['feature'].tolist()
    
    X_train_selected = X_train[selected_features]
    X_test_selected = X_test[selected_features]
    
    return X_train_selected, X_test_selected, feature_scores

X_train_selected, X_test_selected, feature_scores = select_best_features(
    X_train_encoded.fillna(0), 
    y_train, 
    X_test_encoded.fillna(0),
    k=20
)

print(f"\nসিলেক্টেড ফিচার সংখ্যা: {X_train_selected.shape[1]}")
print("\nসিলেক্টেড ফিচার লিস্ট:")
print(X_train_selected.columns.tolist())
```

### ৬. ফিচার ইম্পরটেন্স ভিজুয়ালাইজেশন

```python
plt.figure(figsize=(12, 8))
top_features = feature_scores.head(15)

plt.barh(range(len(top_features)), top_features['mi_score'].values)
plt.yticks(range(len(top_features)), top_features['feature'].values)
plt.xlabel('মিউচুয়াল ইনফরমেশন স্কোর')
plt.title('শীর্ষ ১৫ ফিচার — মিউচুয়াল ইনফরমেশন')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('capstone_feature_importance.png', dpi=100)
plt.show()
print("ফিচার ইম্পরটেন্স প্লট সেভ করা হয়েছে")
```

### ফিচার ইঞ্জিনিয়ারিং পাইপলাইন

```python
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """সম্পূর্ণ ফিচার ইঞ্জিনিয়ারিং পাইপলাইন"""
    
    def __init__(self, poly_degree=2, k_best=20):
        self.poly_degree = poly_degree
        self.k_best = k_best
        self.poly = None
        self.selected_features = None
    
    def fit(self, X, y=None):
        # পলিনোমিয়াল ফিচার
        numeric_cols = ['area', 'age', 'distance_center', 'location_score']
        self.poly = PolynomialFeatures(
            degree=self.poly_degree, 
            interaction_only=True,
            include_bias=False
        )
        self.poly.fit(X[numeric_cols])
        
        # ফিচার সিলেকশন (সম্পূর্ণ পাইপলাইন ডেটা অনুমান করে)
        X_full = self._transform(X)
        mi_scores = mutual_info_regression(X_full, y, random_state=42)
        self.selector = SelectKBest(mutual_info_regression, k=self.k_best)
        self.selector.fit(X_full, y)
        self.selected_features = X_full.columns[self.selector.get_support()]
        
        return self
    
    def transform(self, X):
        X_transformed = self._transform(X)
        return X_transformed[self.selected_features]
    
    def _transform(self, X):
        X_new = X.copy()
        # পলিনোমিয়াল
        X_poly = self.poly.transform(X[['area', 'age', 'distance_center', 'location_score']])
        X_poly_df = pd.DataFrame(
            X_poly,
            columns=self.poly.get_feature_names_out(['area', 'age', 'distance_center', 'location_score']),
            index=X.index
        )
        X_new = pd.concat([X_new, X_poly_df], axis=1)
        
        # বিনিং
        X_new['age_group'] = pd.cut(X['age'], bins=[0, 5, 10, 20, 30, 50],
                                    labels=['new', 'relatively_new', 'moderate', 'old', 'very_old'])
        X_new['size_category'] = pd.cut(X['area'], bins=[0, 1000, 1500, 2000, 3000],
                                        labels=['small', 'medium', 'large', 'very_large'])
        
        # রেশিও
        X_new['area_per_room'] = X['area'] / (X['bedrooms'] + X['bathrooms'])
        X_new['location_efficiency'] = X['location_score'] / (X['distance_center'] + 0.1)
        X_new['total_rooms'] = X['bedrooms'] + X['bathrooms']
        
        # এনকোডিং
        X_new = pd.get_dummies(X_new, drop_first=True)
        
        return X_new.fillna(0)

# ফাইনাল ফিচার সেভ
joblib.dump(X_train_selected, 'X_train_final.pkl')
joblib.dump(X_test_selected, 'X_test_final.pkl')
joblib.dump(feature_scores, 'feature_scores.pkl')
joblib.dump(FeatureEngineer(), 'feature_engineer.pkl')

print("\nফিচার ইঞ্জিনিয়ারিং সম্পন্ন!")
print(f"ফাইনাল ফিচার সংখ্যা: {X_train_selected.shape[1]}")
```

### সারাংশ
- ✅ পলিনোমিয়াল ও ইন্টারঅ্যাকশন ফিচার তৈরি
- ✅ কন্টিনিউয়াস ফিচার বিনিং
- ✅ রেশিও ও কম্বিনেশন ফিচার
- ✅ ক্যাটাগোরিকাল ফিচার এনকোডিং
- ✅ ফিচার সিলেকশন (মিউচুয়াল ইনফরমেশন)
- ✅ ফিচার ইঞ্জিনিয়ারিং পাইপলাইন তৈরি
- ✅ ফাইনাল ফিচার সেভ