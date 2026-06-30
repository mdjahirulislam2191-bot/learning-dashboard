# Day 39: সেন্টিমেন্ট অ্যানালাইসিস
## Sentiment Analysis

### সেন্টিমেন্ট অ্যানালাইসিস কি?
সেন্টিমেন্ট অ্যানালাইসিস হল NLP টেকনিক যা টেক্সটের আবেগ, মতামত বা সেন্টিমেন্ট (পজিটিভ, নেগেটিভ, নিউট্রাল) নির্ধারণ করে।

### ফাইন্যান্সে সেন্টিমেন্ট অ্যানালাইসিসের ব্যবহার
- **মার্কেট সেন্টিমেন্ট**: সোশ্যাল মিডিয়া, নিউজ থেকে ট্রেডিং সিগন্যাল
- **কাস্টমার ফিডব্যাক**: ব্যাংকিং সেবার রিভিউ অ্যানালাইসিস
- **ইআর সেন্টিমেন্ট**: আর্নিংস কল ট্রান্সক্রিপ্ট অ্যানালাইসিস
- **রিস্ক অ্যাসেসমেন্ট**: কোম্পানি সম্পর্কে নেগেটিভ নিউজ ডিটেক্ট

### ফাইন্যান্স উদাহরণ: নিউজ সেন্টিমেন্ট
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import re
import seaborn as sns

# ফাইন্যান্স নিউজ + সেন্টিমেন্ট ডেটা
news_data = [
    # পজিটিভ
    ("Apple stock surges 5% after record breaking earnings quarter", "positive"),
    ("Company profits exceed all analyst expectations by wide margin", "positive"),
    ("Strong revenue growth driven by innovative product launches", "positive"),
    ("Market rally continues as investor confidence improves dramatically", "positive"),
    ("CEO announces aggressive expansion plan into emerging markets", "positive"),
    ("Tech sector leads market higher with record breaking volumes", "positive"),
    ("Company announces massive share buyback program boosting value", "positive"),
    ("New partnership expected to generate billions in revenue growth", "positive"),
    ("Quarterly results show strongest performance in company history", "positive"),
    ("Investors celebrate as dividend increased by fifty percent", "positive"),
    # নেগেটিভ
    ("Stock crashes twenty percent after devastating earnings miss", "negative"),
    ("Company faces major lawsuit threatening financial stability", "negative"),
    ("Revenue falls sharply disappointing investors and analysts alike", "negative"),
    ("CEO resigns amid scandal and allegations of financial fraud", "negative"),
    ("Credit rating downgraded to junk status by major agencies", "negative"),
    ("Massive layoffs announced as company struggles to survive", "negative"),
    ("Regulatory investigation launched into accounting irregularities", "negative"),
    ("Supply chain crisis leads to production halt and revenue loss", "negative"),
    ("Stock price hits all time low as bankruptcy fears grow", "negative"),
    ("Customer complaints surge as service quality deteriorates rapidly", "negative"),
    # নিউট্রাল
    ("Federal Reserve maintains current interest rate policy unchanged", "neutral"),
    ("Company announces quarterly dividend of fifty cents per share", "neutral"),
    ("Market trading within expected range with moderate volatility", "neutral"),
    ("New regulations expected to impact banking sector operations", "neutral"),
    ("Economic data shows mixed signals for upcoming quarter results", "neutral"),
    ("Board of directors meeting scheduled for next month agenda", "neutral"),
    ("Company reports flat revenue compared to previous year quarter", "neutral"),
    ("Industry analysts provide mixed outlook for technology sector", "neutral"),
    ("Trading volume consistent with historical averages for this period", "neutral"),
    ("Partnership agreement terms under review by legal department", "neutral"),
    # আরও কিছু
    ("This stock is amazing and will go to the moon", "positive"),
    ("Terrible investment worst decision I ever made regret everything", "negative"),
    ("Goldman Sachs reports steady earnings for this quarter", "neutral"),
    ("I am very bullish on this company long term prospects", "positive"),
    ("Bearish sentiment growing as economic indicators weaken rapidly", "negative"),
    ("Market outlook remains uncertain given global trade tensions", "neutral"),
    ("Outstanding performance by management team this quarter results", "positive"),
    ("Complete disaster for shareholders as value continues to decline", "negative"),
]

df = pd.DataFrame(news_data, columns=['text', 'sentiment'])
print("📊 Sentiment Dataset:")
print(f"Total samples: {len(df)}")
print(f"Sentiment distribution:\n{df['sentiment'].value_counts()}")
```

### 1. ডেটা প্রিপ্রসেসিং
```python
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['cleaned_text'] = df['text'].apply(preprocess_text)

# TF-IDF ভেক্টরাইজেশন
vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2), stop_words='english')
X = vectorizer.fit_transform(df['cleaned_text'])
y = df['sentiment']

print(f"\nTF-IDF Matrix: {X.shape}")
print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
```

### 2. ট্রেন/টেস্ট স্প্লিট এবং মডেল ট্রেইনিং
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# মডেল
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n📊 {name}:")
    print(f"  Accuracy: {acc:.4f}")
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred))
```

### 3. সেন্টিমেন্ট প্রেডিকশন
```python
# বেস্ট মডেল সিলেক্ট
best_model = LogisticRegression(max_iter=1000, random_state=42)
best_model.fit(X_train, y_train)

# নতুন নিউজের সেন্টিমেন্ট প্রেডিক্ট
new_news = [
    "Stock market rallies as Fed signals dovish policy stance",
    "Company earnings miss leads to sharp decline in share price",
    "Quarterly results meet analyst expectations",
    "This is the most profitable quarter in our history says CEO",
    "Investors panic as cryptocurrency market collapses completely",
    "Bank announces moderate growth in consumer lending division"
]

X_new = vectorizer.transform([preprocess_text(t) for t in new_news])
predictions = best_model.predict(X_new)
probabilities = best_model.predict_proba(X_new)

print("🔮 Sentiment Predictions for New News:")
print("-" * 60)
for i, (text, sent) in enumerate(zip(new_news, predictions)):
    prob = probabilities[i]
    conf = prob[list(best_model.classes_).index(sent)]
    sentiment_emoji = {'positive': '🟢', 'negative': '🔴', 'neutral': '🟡'}
    print(f"{sentiment_emoji.get(sent, '⚪')} {sent.upper():>8} ({conf:.2%}): {text}")
```

### 4. ফাইন্যান্স-স্পেসিফিক সেন্টিমেন্ট (VADER)
```python
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.download('vader_lexicon')
except:
    pass

# VADER সেন্টিমেন্ট এনালাইসিস
sia = SentimentIntensityAnalyzer()

print("📊 VADER Sentiment Analysis:")
print("-" * 60)
for text in news_data[:8]:
    text_content = text[0]
    scores = sia.polarity_scores(text_content)
    compound = scores['compound']
    
    if compound >= 0.05:
        vader_sent = 'positive'
    elif compound <= -0.05:
        vader_sent = 'negative'
    else:
        vader_sent = 'neutral'
    
    print(f"\nText: {text_content}")
    print(f"  Scores: pos={scores['pos']:.2f}, neu={scores['neu']:.2f}, neg={scores['neg']:.2f}")
    print(f"  Compound: {compound:.3f} -> {vader_sent}")
```

### 5. ট্রান্সফরমার-বেসড সেন্টিমেন্ট
```python
# Hugging Face ট্রান্সফরমার
try:
    from transformers import pipeline
    
    sentiment_pipeline = pipeline("sentiment-analysis")
    
    print("🔮 Transformer-based Sentiment Analysis:")
    for text in new_news:
        result = sentiment_pipeline(text)[0]
        print(f"  {result['label']} ({result['score']:.2%}): {text}")
    
except ImportError:
    print("Transformers not installed.")
    print("Install: pip install transformers torch")
```

### 6. সেন্টিমেন্ট টাইম সিরিজ
```python
# সেন্টিমেন্ট টাইম সিরিজ
np.random.seed(42)
n_days = 100
dates = pd.date_range('2024-01-01', periods=n_days, freq='D')

# সিন্থেটিক সেন্টিমেন্ট স্কোর
sentiment_scores = np.random.randn(n_days) * 0.3
sentiment_scores = np.convolve(sentiment_scores, np.ones(5)/5, mode='same')
sentiment_scores = np.clip(sentiment_scores, -1, 1)

sentiment_df = pd.DataFrame({
    'date': dates,
    'sentiment': sentiment_scores
})

# সেন্টিমেন্ট এবং স্টক রিটার্ন
stock_returns = sentiment_scores * 0.02 + np.random.randn(n_days) * 0.01
sentiment_df['stock_return'] = stock_returns

plt.figure(figsize=(15, 8))

plt.subplot(2, 1, 1)
colors = ['green' if s > 0 else 'red' for s in sentiment_scores]
plt.bar(sentiment_df['date'], sentiment_scores, color=colors, alpha=0.6, width=0.8)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.title('Daily Sentiment Score')
plt.ylabel('Sentiment Score')
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(sentiment_df['date'], sentiment_df['stock_return'], linewidth=2)
plt.title('Stock Returns')
plt.xlabel('Date')
plt.ylabel('Return')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Correlation
correlation = sentiment_df['sentiment'].corr(sentiment_df['stock_return'])
print(f"\n📊 Sentiment-Return Correlation: {correlation:.4f}")
```

### সেন্টিমেন্ট অ্যানালাইসিস বেস্ট প্র্যাকটিস
```python
print("""
✅ Sentiment Analysis Best Practices:
1️⃣ Use finance-specific sentiment lexicons (Loughran-McDonald)
2️⃣ Handle sarcasm and negation carefully
3️⃣ Consider context (industry, company specific)
4️⃣ Use domain-adapted models
5️⃣ Combine multiple sentiment sources
6️⃣ Validate with actual market movements

📊 Methods Comparison:
- Lexicon-based (VADER): Fast, no training needed
- ML-based (NB, LR): Good accuracy, needs labeled data
- Deep Learning (BERT): Best accuracy, computationally heavy

⚠️ Limitations:
- Sarcasm and irony are hard to detect
- Context matters (e.g., "bear" vs "bull")
- Market sentiment ≠ price movement
""")
```

### সারসংক্ষেপ
আজ আমরা সেন্টিমেন্ট অ্যানালাইসিস শিখলাম:
- **ML মডেল**: Naive Bayes, Logistic Regression, Random Forest
- **VADER**: রুল-বেসড লেক্সিকন অ্যানালাইসিস
- **ট্রান্সফরমার**: BERT-ভিত্তিক সেন্টিমেন্ট
- **টাইম সিরিজ**: সেন্টিমেন্ট-রিটার্ন কোরিলেশন
- **ইভালুয়েশন**: Classification Report, Accuracy

### অনুশীলনী
1. ফাইন্যান্স-স্পেসিফিক লেক্সিকন (Loughran-McDonald) ব্যবহার করুন
2. Twitter API ব্যবহার করে রিয়েল-টাইম সেন্টিমেন্ট সংগ্রহ করুন
3. সেন্টিমেন্ট-বেসড ট্রেডিং স্ট্র্যাটেজি তৈরি করুন
4. FinBERT (BERT fine-tuned on financial text) ব্যবহার করুন