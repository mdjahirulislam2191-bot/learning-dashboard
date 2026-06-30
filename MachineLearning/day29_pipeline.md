# Day 29: পাইপলাইন
## Pipeline

### পাইপলাইন কি?
পাইপলাইন একটি sklearn ইউটিলিটি যা একাধিক ট্রান্সফরমেশন এবং একটি ফাইনাল এস্টিমেটরকে একটি সিঙ্গেল ইউনিটে চেইন করে। এটি ডেটা প্রিপ্রসেসিং এবং মডেল ট্রেইনিংকে অটোমেট করে।

### পাইপলাইন কেন ব্যবহার করবেন?
- **ডেটা লিকেজ** প্রতিরোধ করে
- **কোড রিইউজ** সহজ করে
- **হাইপারপ্যারামিটার টিউনিং** সহজ করে
- **ডিপ্লয়মেন্ট** সহজ করে

### ফাইন্যান্স উদাহরণ: ক্রেডিট রিস্ক মডেল পাইপলাইন
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import matplotlib.pyplot as plt

# ক্রেডিট ডেটা তৈরি
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'income': np.random.randn(n) * 30000 + 50000,
    'age': np.random.randint(22, 70, n),
    'credit_score': np.random.randint(500, 850, n),
    'loan_amount': np.random.randn(n) * 20000 + 100000,
    'employment_years': np.random.randint(0, 30, n),
    'debt_ratio': np.random.rand(n) * 0.5,
    'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n),
    'employment_type': np.random.choice(['Full-time', 'Part-time', 'Self-employed', 'Unemployed'], n),
    'default': np.random.binomial(1, 0.2, n)  # 20% default rate
})

# কিছু মিসিং ডেটা
data.loc[np.random.choice(n, 50), 'credit_score'] = np.nan
data.loc[np.random.choice(n, 30), 'income'] = np.nan

print("Credit Dataset Shape:", data.shape)
print(data.head())
print(f"\nDefault rate: {data['default'].mean():.2%}")
```

### 1. বেসিক পাইপলাইন
```python
# Numeric এবং Categorical ফিচার আলাদা করা
numeric_features = ['income', 'age', 'credit_score', 'loan_amount', 
                    'employment_years', 'debt_ratio']
categorical_features = ['education', 'employment_type']

X = data.drop('default', axis=1)
y = data['default']

# নিউমেরিক পাইপলাইন
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# ক্যাটেগোরিক্যাল পাইপলাইন
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# কলাম ট্রান্সফরমার
preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('cat', categorical_pipeline, categorical_features)
])

# ফুল পাইপলাইন
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# ট্রেইন-টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42, stratify=y)

# পাইপলাইন ট্রেইন
pipeline.fit(X_train, y_train)

# প্রেডিকশন
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print("Pipeline Performance:")
print(f"Accuracy: {pipeline.score(X_test, y_test):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
```

### 2. পাইপলাইন সহ GridSearchCV
```python
# প্যারামিটার গ্রিড
param_grid = {
    'preprocessor__num__scaler': [StandardScaler(), MinMaxScaler()],
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, None],
    'classifier__min_samples_split': [2, 5]
}

# GridSearchCV
grid_search = GridSearchCV(pipeline, param_grid, cv=5, 
                          scoring='roc_auc', n_jobs=-1, verbose=0)

print("Running GridSearchCV on Pipeline...")
grid_search.fit(X_train, y_train)

print(f"\nBest parameters: {grid_search.best_params_}")
print(f"Best CV ROC-AUC: {grid_search.best_score_:.4f}")
print(f"Test ROC-AUC: {roc_auc_score(y_test, grid_search.predict_proba(X_test)[:, 1]):.4f}")
```

### 3. মাল্টিপল মডেল পাইপলাইন
```python
# বিভিন্ন মডেলের জন্য পাইপলাইন
pipelines = {
    'Logistic Regression': Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ]),
    'Random Forest': Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
}

# ক্রস-ভ্যালিডেশন
results = []
for name, pipe in pipelines.items():
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='roc_auc')
    pipe.fit(X_train, y_train)
    test_auc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
    
    results.append({
        'Model': name,
        'CV AUC Mean': scores.mean(),
        'CV AUC Std': scores.std(),
        'Test AUC': test_auc
    })
    
    print(f"{name}: CV AUC = {scores.mean():.4f} ± {scores.std():.4f}, Test AUC = {test_auc:.4f}")

comparison = pd.DataFrame(results)
print("\nModel Comparison:")
print(comparison.to_string(index=False))
```

### 4. কাস্টম ট্রান্সফর্মার
```python
from sklearn.base import BaseEstimator, TransformerMixin

# কাস্টম ফিচার ইঞ্জিনিয়ারিং ট্রান্সফর্মার
class FinancialFeatureCreator(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.feature_names_ = None
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_new = X.copy()
        
        # লোন টু ইনকাম রেশিও
        X_new['loan_to_income'] = X_new['loan_amount'] / (X_new['income'] + 1)
        
        # ক্রেডিট স্কোর ক্যাটেগরি
        X_new['credit_category'] = pd.cut(X_new['credit_score'], 
                                          bins=[0, 580, 670, 740, 800, 850],
                                          labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
        
        # ডেট টু ইনকাম রেশিও
        X_new['debt_service_ratio'] = X_new['debt_ratio'] * X_new['income'] / X_new['loan_amount']
        
        # এজ গ্রুপ
        X_new['age_group'] = pd.cut(X_new['age'], 
                                    bins=[0, 30, 45, 60, 100],
                                    labels=['Young', 'Mid', 'Senior', 'Retired'])
        
        self.feature_names_ = X_new.columns.tolist()
        return X_new

# আপডেটেড পাইপলাইন
custom_pipeline = Pipeline([
    ('feature_creator', FinancialFeatureCreator()),
    ('preprocessor', ColumnTransformer([
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features + ['loan_to_income', 'debt_service_ratio']),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), ['education', 'employment_type', 'credit_category', 'age_group'])
    ])),
    ('classifier', RandomForestClassifier(random_state=42))
])

custom_pipeline.fit(X_train, y_train)
print(f"\nCustom Pipeline Test AUC: {roc_auc_score(y_test, custom_pipeline.predict_proba(X_test)[:, 1]):.4f}")
```

### 5. পাইপলাইন সেভ এবং লোড
```python
import pickle
import joblib

# পাইপলাইন সেভ
with open('credit_risk_pipeline.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# পাইপলাইন লোড
with open('credit_risk_pipeline.pkl', 'rb') as f:
    loaded_pipeline = pickle.load(f)

# লোডেড পাইপলাইন টেস্ট
y_pred_loaded = loaded_pipeline.predict(X_test)
print(f"Loaded Pipeline Accuracy: {(y_pred_loaded == y_test).mean():.4f}")

# অথবা joblib ব্যবহার করে
joblib.dump(pipeline, 'credit_risk_pipeline.joblib')
loaded_pipeline2 = joblib.load('credit_risk_pipeline.joblib')
print(f"Joblib Loaded Pipeline Accuracy: {(loaded_pipeline2.predict(X_test) == y_test).mean():.4f}")
```

### পাইপলাইন অ্যাডভান্টেজেস সামারি
```python
print("""
✅ Pipeline Advantages:
1️⃣ Encapsulates preprocessing + model in one object
2️⃣ Prevents data leakage during cross-validation
3️⃣ Makes hyperparameter tuning easier
4️⃣ Simplifies deployment
5️⃣ Reduces boilerplate code
6️⃣ Ensures consistent preprocessing

🔄 Pipeline Workflow:
Raw Data → Imputer → Scaler → Feature Engineering → OneHot → Model → Prediction
""")
```

### সারসংক্ষেপ
আজ আমরা পাইপলাইন এর বিভিন্ন দিক শিখলাম:
- **বেসিক পাইপলাইন**: প্রিপ্রসেসিং + মডেল
- **ColumnTransformer**: বিভিন্ন টাইপের ফিচার আলাদা হ্যান্ডলিং
- **GridSearchCV + Pipeline**: সম্মিলিত হাইপারপ্যারামিটার টিউনিং
- **কাস্টম ট্রান্সফর্মার**: ফাইন্যান্স-স্পেসিফিক ফিচার তৈরি
- **পাইপলাইন সেভ/লোড**: ডিপ্লয়মেন্টের জন্য

### অনুশীলনী
1. নিজের ডেটাসেটের জন্য একটি সম্পূর্ণ পাইপলাইন তৈরি করুন
2. বিভিন্ন প্রিপ্রসেসিং স্টেপ সহ পাইপলাইন GridSearchCV ব্যবহার করে টিউন করুন
3. একটি কাস্টম ট্রান্সফর্মার তৈরি করুন যা আউটলায়ার রিমুভ করে
4. পাইপলাইনকে একটি ফাংশনে র‍্যাপ করুন যা ইনপুট ডেটা নিয়ে প্রেডিকশন রিটার্ন করে
