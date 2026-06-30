# Day 38: NLP বেসিক
## Natural Language Processing Basics

### NLP কি?
ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP) হল কৃত্রিম বুদ্ধিমত্তার একটি শাখা যা কম্পিউটারকে মানব ভাষা বুঝতে, ব্যাখ্যা করতে এবং জেনারেট করতে সাহায্য করে।

### ফাইন্যান্সে NLP-এর ব্যবহার
- **সেন্টিমেন্ট অ্যানালাইসিস**: নিউজ, সোশ্যাল মিডিয়া থেকে মার্কেট সেন্টিমেন্ট
- **ফাইন্যান্সিয়াল রিপোর্ট পার্সিং**: 10-K, 10-Q রিপোর্ট অ্যানালাইসিস
- **ফ্রড ডিটেকশন**: অস্বাভাবিক প্যাটার্ন শনাক্তকরণ
- **কাস্টমার সাপোর্ট**: চ্যাটবট, ইমেইল অটোমেশন

### ফাইন্যান্স উদাহরণ: টেক্সট প্রিপ্রসেসিং
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

# NLTK ডেটা ডাউনলোড
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')

# ফাইন্যান্স নিউজ ডেটা
news_data = [
    "Apple stock surged 5% after strong earnings report, beating analyst expectations.",
    "Federal Reserve raises interest rates by 25 basis points, citing inflation concerns.",
    "Tesla shares fall 3% amid production delays and supply chain issues.",
    "JP Morgan reports record quarterly profit, driven by trading revenue.",
    "Bitcoin crashes below $30,000 as regulatory fears intensify.",
    "Amazon acquires AI startup for $2 billion to boost cloud capabilities.",
    "Oil prices jump 4% after OPEC+ announces production cuts.",
    "Goldman Sachs downgrades tech sector citing valuation concerns.",
    "S&P 500 hits new all-time high as market sentiment improves.",
    "Recession fears grow as manufacturing data disappoints."
]

news_df = pd.DataFrame({'text': news_data, 'date': pd.date_range('2024-01-01', periods=10, freq='D')})
print("📰 Financial News Dataset:")
for i, row in news_df.iterrows():
    print(f"{row['date'].date()}: {row['text']}")
```

### 1. টেক্সট ক্লিনিং
```python
def clean_text(text):
    # লোয়ারকেস
    text = text.lower()
    # পাঙ্কচুয়েশন রিমুভ
    text = re.sub(r'[^\w\s]', '', text)
    # সংখ্যা রিমুভ
    text = re.sub(r'\d+', '', text)
    # এক্সট্রা স্পেস রিমুভ
    text = re.sub(r'\s+', ' ', text).strip()
    return text

cleaned = [clean_text(text) for text in news_df['text']]
news_df['cleaned'] = cleaned

print("📝 Text Cleaning Results:")
for orig, clean in zip(news_df['text'][:3], cleaned[:3]):
    print(f"\nOriginal:  {orig}")
    print(f"Cleaned:   {clean}")
```

### 2. টোকেনাইজেশন এবং স্টপওয়ার্ডস
```python
# টোকেনাইজেশন
news_df['tokens'] = news_df['cleaned'].apply(word_tokenize)

# স্টপওয়ার্ডস রিমুভ
stop_words = set(stopwords.words('english'))
news_df['tokens_no_stop'] = news_df['tokens'].apply(
    lambda tokens: [t for t in tokens if t not in stop_words]
)

print("📊 Tokenization Example:")
for i in range(2):
    print(f"\nSentence: {news_df['cleaned'][i]}")
    print(f"Tokens: {news_df['tokens'][i]}")
    print(f"Without stopwords: {news_df['tokens_no_stop'][i]}")
```

### 3. স্টেমিং এবং লেমাটাইজেশন
```python
# স্টেমিং
stemmer = PorterStemmer()
news_df['stemmed'] = news_df['tokens_no_stop'].apply(
    lambda tokens: [stemmer.stem(t) for t in tokens]
)

# লেমাটাইজেশন
lemmatizer = WordNetLemmatizer()
news_df['lemmatized'] = news_df['tokens_no_stop'].apply(
    lambda tokens: [lemmatizer.lemmatize(t) for t in tokens]
)

print("📝 Stemming vs Lemmatization:")
example_tokens = ['rising', 'improves', 'crashes', 'trading', 'expectations', 'concerns']
print(f"\nOriginal:    {example_tokens}")
print(f"Stemmed:     {[stemmer.stem(t) for t in example_tokens]}")
print(f"Lemmatized:  {[lemmatizer.lemmatize(t) for t in example_tokens]}")
```

### 4. Bag of Words (BoW)
```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Bag of Words
bow_vectorizer = CountVectorizer(max_features=50, stop_words='english')
bow_matrix = bow_vectorizer.fit_transform(news_df['text'])

bow_df = pd.DataFrame(bow_matrix.toarray(), columns=bow_vectorizer.get_feature_names_out())
print("📊 Bag of Words Matrix:")
print(f"Shape: {bow_df.shape}")
print(bow_df)
```

### 5. TF-IDF
```python
# TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(news_df['text'])

tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
print("📊 TF-IDF Matrix:")
print(f"Shape: {tfidf_df.shape}")
print(tfidf_df.round(3))

# টপ TF-IDF শব্দ
print("\nTop TF-IDF Words:")
for i in range(len(news_df)):
    doc = tfidf_df.iloc[i]
    top_words = doc.nlargest(3)
    print(f"Doc {i+1}: {', '.join([f'{w}({s:.3f})' for w, s in top_words.items()])}")
```

### 6. ওয়ার্ড এম্বেডিং (Word2Vec)
```python
# Word2Vec
from gensim.models import Word2Vec
from sklearn.decomposition import PCA

# টোকেনাইজড সেন্টেন্স
sentences = [row.split() for row in news_df['cleaned']]

# Word2Vec মডেল
w2v_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
print("✅ Word2Vec model trained!")
print(f"Vocabulary size: {len(w2v_model.wv.key_to_index)}")

# সিমিলার শব্দ খোঁজা
try:
    similar_words = w2v_model.wv.most_similar('stock', topn=5)
    print(f"\nWords similar to 'stock':")
    for word, score in similar_words:
        print(f"  {word}: {score:.4f}")
except KeyError:
    print("\n(Word 'stock' not in vocabulary for similarity)")

# ওয়ার্ড ভেক্টর
vector = w2v_model.wv['market']
print(f"\nVector for 'market' (first 10 dims): {vector[:10]}")
```

### 7. টেক্সট সিমিলারিটি
```python
from sklearn.metrics.pairwise import cosine_similarity

# Cosine similarity of TF-IDF vectors
similarity_matrix = cosine_similarity(tfidf_matrix)

news_df['doc_id'] = range(len(news_df))

plt.figure(figsize=(10, 8))
plt.imshow(similarity_matrix, cmap='viridis', aspect='auto')
plt.colorbar(label='Cosine Similarity')
plt.title('Document Similarity Matrix')
plt.xlabel('Document')
plt.ylabel('Document')

# এনোটেশন
for i in range(len(similarity_matrix)):
    for j in range(len(similarity_matrix)):
        plt.text(j, i, f'{similarity_matrix[i,j]:.2f}', 
                ha='center', va='center', color='white', fontsize=8)

plt.tight_layout()
plt.show()

print("\n📊 Most Similar Documents:")
for i in range(5):
    for j in range(i+1, 5):
        sim = similarity_matrix[i, j]
        if sim > 0.5:
            print(f"Doc {i+1} & Doc {j+1}: {sim:.3f}")
```

### NLP বেস্ট প্র্যাকটিস
```python
print("""
✅ NLP Best Practices:
1️⃣ Always clean text thoroughly
2️⃣ Choose right preprocessing (stemming vs lemmatization)
3️⃣ Remove domain-specific stopwords
4️⃣ Consider n-grams for better context
5️⃣ Use TF-IDF for feature importance
6️⃣ Consider word embeddings for semantics

📊 Text Representation Methods:
- Bag of Words: Simple count, loses word order
- TF-IDF: Adjusts for document frequency
- Word2Vec: Captures semantic meaning
- BERT: Contextual embeddings (state-of-art)

🔧 NLP Pipeline:
Raw Text → Cleaning → Tokenization → Normalization
→ Feature Extraction (BoW/TF-IDF/Embeddings)
→ Modeling (Classification, Clustering, etc.)
""")
```

### সারসংক্ষেপ
আজ আমরা NLP বেসিক শিখলাম:
- **টেক্সট ক্লিনিং**: লোয়ারকেস, পাঙ্কচুয়েশন রিমুভ
- **টোকেনাইজেশন**: শব্দে ভাগ করা
- **স্টপওয়ার্ডস রিমুভ**: অপ্রয়োজনীয় শব্দ বাদ
- **স্টেমিং/লেমাটাইজেশন**: শব্দের মূল রূপ
- **BoW/TF-IDF**: টেক্সট ভেক্টরাইজেশন
- **Word2Vec**: সিম্যান্টিক এম্বেডিং

### অনুশীলনী
1. রিয়েল ফাইন্যান্স নিউজ ডেটাসেট সংগ্রহ করুন
2. কাস্টম স্টপওয়ার্ডস লিস্ট তৈরি করুন (ফাইন্যান্স-স্পেসিফিক)
3. N-gram (বাইগ্রাম, ট্রাইগ্রাম) ফিচার ব্যবহার করুন
4. fastText বা GloVe এম্বেডিং ব্যবহার করে দেখুন