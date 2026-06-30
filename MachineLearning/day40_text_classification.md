# Day 40: টেক্সট ক্লাসিফিকেশন
## Text Classification

### টেক্সট ক্লাসিফিকেশন কি?
টেক্সট ক্লাসিফিকেশন একটি NLP টাস্ক যা টেক্সটকে প্রিডিফাইন্ড ক্যাটেগরিতে অ্যাসাইন করে। ফাইন্যান্সে এটি নিউজ ক্যাটেগোরাইজেশন, ইমেইল ফিল্টারিং, ডকুমেন্ট ক্লাসিফিকেশনের জন্য ব্যবহৃত হয়।

### ফাইন্যান্স অ্যাপ্লিকেশন
- **নিউজ ক্যাটেগোরাইজেশন**: Market, Economy, IPO, M&A
- **ফ্রড ডিটেকশন**: সন্দেহজনক লেনদেন রিপোর্ট ক্লাসিফাই
- **কাস্টমার ইনকোয়ারি রাউটিং**: সাপোর্ট টিকেট ক্লাসিফিকেশন
- **রেগুলেটরি কমপ্লায়েন্স**: AML রিপোর্ট অ্যানালাইসিস

### ফাইন্যান্স উদাহরণ: নিউজ ক্যাটেগোরাইজেশন
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import re
import seaborn as sns

# ফাইন্যান্স নিউজ ক্যাটেগরি ডেটা
news_categories = [
    # Market
    ("S&P 500 hits new record high driven by tech sector rally", "market"),
    ("Dow Jones falls 200 points amid trade war concerns", "market"),
    ("Asian markets mixed as investors await Fed decision", "market"),
    ("European stocks rise on positive economic data", "market"),
    ("Nasdaq composite reaches milestone closing above 20000", "market"),
    # Economy
    ("GDP growth accelerates to 3.2 percent in latest quarter", "economy"),
    ("Unemployment rate drops to historic low of 3.5 percent", "economy"),
    ("Consumer spending increases by 2.8 percent in December", "economy"),
    ("Inflation rate remains steady at 2.1 percent as expected", "economy"),
    ("Federal Reserve holds interest rates steady amid uncertainty", "economy"),
    ("Manufacturing PMI expands for sixth consecutive month", "economy"),
    # IPO
    ("Reddit files for IPO targeting 6.5 billion valuation", "ipo"),
    ("Arm Holdings IPO surges 25 percent on first trading day", "ipo"),
    ("Instacart prices IPO above range raising 600 million", "ipo"),
    ("Klaviyo debuts on NYSE with strong first day performance", "ipo"),
    ("Birkenstock files for IPO in New York Stock Exchange", "ipo"),
    # M&A
    ("Microsoft acquires Activision Blizzard in 68 billion deal", "ma"),
    ("Amazon buys MGM Studios for 8.45 billion in cash", "ma"),
    ("Salesforce acquires Slack Technologies for 27 billion", "ma"),
    ("Nvidia announces acquisition of ARM for 40 billion", "ma"),
    ("Disney completes acquisition of 21st Century Fox assets", "ma"),
    # Technology
    ("Apple releases new iPhone with AI powered features", "technology"),
    ("Google unveils Gemini AI model outperforming GPT 4", "technology"),
    ("Tesla self driving software update faces regulatory review", "technology"),
    ("Nvidia earnings beat expectations on AI chip demand", "technology"),
    ("Meta announces new VR headset with advanced features", "technology"),
]

df = pd.DataFrame(news_categories, columns=['text', 'category'])
print("📊 News Category Dataset:")
print(f"Total articles: {len(df)}")
print(f"\nCategories:\n{df['category'].value_counts()}")
```

### 1. ডেটা প্রিপ্রসেসিং এবং ভেক্টরাইজেশন
```python
# টেক্সট ক্লিনিং ফাংশন
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['clean_text'] = df['text'].apply(clean_text)

# TF-IDF + N-grams
vectorizer = TfidfVectorizer(
    max_features=500,
    ngram_range=(1, 3),  # unigrams + bigrams + trigrams
    stop_words='english',
    min_df=2
)

X = vectorizer.fit_transform(df['clean_text'])
y = df['category']

print(f"TF-IDF Matrix: {X.shape}")
print(f"Vocabulary: {len(vectorizer.get_feature_names_out())} terms")
print(f"N-gram range: (1, 3)")

# ট্রেন/টেস্ট স্প্লিট
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                    random_state=42, stratify=y)
print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")
```

### 2. মডেল বিল্ডিং এবং ইভালুয়েশন
```python
# বিভিন্ন মডেল
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Linear SVC': LinearSVC(max_iter=2000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []
for name, model in models.items():
    # পাইপলাইন তৈরি
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
        ('clf', model)
    ])
    
    # ট্রেইন
    pipeline.fit(df['clean_text'], y)
    
    # প্রেডিক্ট
    y_pred = pipeline.predict(df['clean_text'])
    
    # ইভালুয়েশন
    accuracy = accuracy_score(y, y_pred)
    cv_scores = cross_val_score(pipeline, df['clean_text'], y, cv=3)
    
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'CV Mean': cv_scores.mean(),
        'CV Std': cv_scores.std()
    })
    
    print(f"\n📊 {name}:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  CV Score: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

results_df = pd.DataFrame(results)
print("\n📊 Model Comparison:")
print(results_df.to_string(index=False))
```

### 3. কনফিউশন ম্যাট্রিক্স বিশ্লেষণ
```python
# বেস্ট মডেল
best_model = LinearSVC(max_iter=2000, random_state=42)
pipeline_best = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
    ('clf', best_model)
])
pipeline_best.fit(df['clean_text'], y)
y_pred = pipeline_best.predict(df['clean_text'])

# কনফিউশন ম্যাট্রিক্স
cm = confusion_matrix(y, y_pred)
categories = pipeline_best.classes_

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=categories, yticklabels=categories)
plt.title('Confusion Matrix - News Classification')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.show()

print("\n📊 Detailed Classification Report:")
print(classification_report(y, y_pred, target_names=categories))
```

### 4. নতুন নিউজ ক্লাসিফিকেশন
```python
# নতুন নিউজ ক্লাসিফাই
new_articles = [
    "Stock market opens higher as quarterly earnings season begins",  # market
    "Federal Reserve chairman signals potential rate cut next meeting",  # economy
    "Tech startup Stripe confidentially files for IPO",  # ipo
    "Oracle completes 28 billion acquisition of Cerner healthcare",  # ma
    "AMD launches new AI accelerator chip competing with Nvidia",  # technology
    "Inflation data shows unexpected decline in consumer prices",  # economy
    "Airbnb stock jumps after exceeding quarterly earnings expectations"  # market
]

predictions = pipeline_best.predict(new_articles)
probabilities = pipeline_best.decision_function(new_articles)

print("🔮 News Classification Results:")
print("-" * 60)
for article, pred in zip(new_articles, predictions):
    print(f"📰 {article}")
    print(f"  → Categorized as: [{pred}]\n")
```

### 5. মাল্টি-লেবেল ক্লাসিফিকেশন
```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# মাল্টি-লেবেল ডেটা (এক নিউজে একাধিক ক্যাটেগরি)
multilabel_data = [
    ("Apple stock surges after earnings driven by AI product sales", 
     ["market", "technology"]),
    ("IPO market heats up as Fed signals rate cuts to boost economy",
     ["ipo", "economy", "market"]),
    ("Microsoft acquisition of gaming company approved by regulators",
     ["ma", "technology"]),
    ("Economic data disappoints as market falls on recession fears",
     ["economy", "market"]),
    ("New AI chip announcement boosts tech stocks in after hours trading",
     ["technology", "market"])
]

ml_texts = [item[0] for item in multilabel_data]
ml_labels = [item[1] for item in multilabel_data]

# মাল্টি-লেবেল এনকোডিং
mlb = MultiLabelBinarizer()
y_ml = mlb.fit_transform(ml_labels)

# TF-IDF
X_ml = vectorizer.fit_transform(ml_texts)

# মডেল (OneVsRest)
ml_model = OneVsRestClassifier(LinearSVC(max_iter=2000, random_state=42))
ml_model.fit(X_ml, y_ml)

print("\n📊 Multi-label Classification:")
for text, true_labels in multilabel_data:
    X_new_ml = vectorizer.transform([clean_text(text)])
    pred = ml_model.predict(X_new_ml)
    pred_labels = mlb.inverse_transform(pred)
    print(f"\nText: {text}")
    print(f"  True labels: {true_labels}")
    print(f"  Predicted:   {pred_labels}")
```

### 6. হাইপারপ্যারামিটার টিউনিং
```python
from sklearn.model_selection import GridSearchCV

# Grid Search
param_grid = {
    'tfidf__max_features': [100, 300, 500],
    'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
    'clf__C': [0.1, 1.0, 10.0]
}

grid_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LinearSVC(max_iter=2000, random_state=42))
])

grid_search = GridSearchCV(grid_pipeline, param_grid, cv=3, scoring='accuracy')
grid_search.fit(df['clean_text'], y)

print("\n🎯 Grid Search Results:")
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV accuracy: {grid_search.best_score_:.4f}")

# বেস্ট মডেল দিয়ে প্রেডিক্ট
best_pipeline = grid_search.best_estimator_
y_pred_best = best_pipeline.predict(df['clean_text'])
print(f"Test accuracy: {accuracy_score(y, y_pred_best):.4f}")
```

### টেক্সট ক্লাসিফিকেশন বেস্ট প্র্যাকটিস
```python
print("""
✅ Text Classification Best Practices:
1️⃣ Use domain-specific preprocessing
2️⃣ Balance your dataset across categories
3️⃣ Experiment with different n-gram ranges
4️⃣ Use cross-validation for robust evaluation
5️⃣ Try ensemble methods for better accuracy
6️⃣ Consider class weights for imbalanced data

📊 Model Selection Guide:
- Naive Bayes: Fast, good for text, strong baseline
- Logistic Regression: Good probability calibration
- Linear SVC: Often best for text classification
- Deep Learning: State-of-art, needs more data

⚠️ Common Pitfalls:
- Overfitting on small datasets
- Irrelevant features in vocabulary
- Class imbalance
- Data leakage (using future info)
""")
```

### সারসংক্ষেপ
আজ আমরা টেক্সট ক্লাসিফিকেশন শিখলাম:
- **মডেল**: MultinomialNB, LogisticRegression, SVC, RandomForest
- **TF-IDF + N-grams**: ফিচার এক্সট্রাকশন
- **মাল্টি-লেবেল**: OneVsRest ক্লাসিফিকেশন
- **GridSearchCV**: হাইপারপ্যারামিটার টিউনিং
- **কনফিউশন ম্যাট্রিক্স**: ক্লাসিফিকেশন পারফরম্যান্স

### অনুশীলনী
1. বড় ফাইন্যান্স নিউজ ডেটাসেটে (50+ articles) মডেল ট্রেইন করুন
2. ডিপ লার্নিং (BERT) ক্লাসিফায়ার ইমপ্লিমেন্ট করুন
3. স্প্যাম ডিটেকশন মডেল তৈরি করুন (ফাইন্যান্স ইমেইল)
4. অনলাইন লার্নিংয়ের জন্য স্ট্রিমিং ক্লাসিফায়ার তৈরি করুন