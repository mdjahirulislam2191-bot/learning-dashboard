# Day 36: রিকমেন্ডার সিস্টেম
## Recommender Systems

### রিকমেন্ডার সিস্টেম কি?
রিকমেন্ডার সিস্টেম হল অ্যালগরিদম যা ব্যবহারকারীদের পছন্দ বা আচরণের ভিত্তিতে তাদের জন্য পণ্য, সেবা বা কন্টেন্ট সুপারিশ করে।

### ফাইন্যান্সে রিকমেন্ডার সিস্টেমের ব্যবহার
- **স্টক রিকমেন্ডেশন**: অনুরূপ ইনভেস্টরদের পোর্টফোলিও দেখে স্টক সুপারিশ
- **প্রোডাক্ট রিকমেন্ডেশন**: ব্যাংকিং প্রোডাক্ট (লোন, ক্রেডিট কার্ড)
- **পার্সোনালাইজড পোর্টফোলিও**: ঝুঁকি প্রোফাইল অনুযায়ী বিনিয়োগ সুপারিশ

### রিকমেন্ডার সিস্টেমের প্রকারভেদ
1. **কলাবরেটিভ ফিল্টারিং**: ইউজার-ইউজার বা আইটেম-আইটেম সিমিলারিটি
2. **কন্টেন্ট-বেসড ফিল্টারিং**: আইটেমের বৈশিষ্ট্যের ভিত্তিতে
3. **হাইব্রিড**: উভয় পদ্ধতির কম্বিনেশন

### ফাইন্যান্স উদাহরণ: স্টক রিকমেন্ডার
```python
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import seaborn as sns

# ইনভেস্টর-স্টক রেটিং ডেটা
np.random.seed(42)
n_users = 200
n_stocks = 50

# স্টক তথ্য
stock_info = pd.DataFrame({
    'stock_id': range(n_stocks),
    'ticker': [f'STK_{i:03d}' for i in range(n_stocks)],
    'sector': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Energy', 'Consumer'], n_stocks),
    'market_cap': np.random.randint(10, 1000, n_stocks),  # Billion $
    'volatility': np.random.rand(n_stocks) * 0.5
})

print("📊 Stock Universe:")
print(stock_info.head())
print(f"\nSectors: {stock_info['sector'].value_counts().to_dict()}")
```

### 1. ইউজার-স্টক ইন্টারঅ্যাকশন ডেটা
```python
# স্পার্স রেটিং ম্যাট্রিক্স (বেশিরভাগ NaN)
ratings = np.random.rand(n_users, n_stocks)
ratings[ratings < 0.7] = np.nan  # 70% sparse
ratings = ratings * 5  # 0-5 স্কেল

# কিছু ইউজার প্রেফারেন্স
user_prefs = pd.DataFrame({
    'user_id': range(n_users),
    'risk_tolerance': np.random.choice(['Low', 'Medium', 'High'], n_users),
    'investment_horizon': np.random.choice(['Short', 'Medium', 'Long'], n_users),
    'age_group': np.random.choice(['Young', 'Mid', 'Senior'], n_users)
})

# রেটিং ডেটাফ্রেম
rating_df = pd.DataFrame(ratings, columns=stock_info['ticker'])
rating_df['user_id'] = range(n_users)

print("User-Stock Rating Matrix:")
print(f"Shape: {rating_df.shape}")
print(f"Non-null ratings: {ratings[~np.isnan(ratings)].shape[0]:,}")
print(f"Sparsity: {np.isnan(ratings).mean():.2%}")
print(f"\nRating distribution:")
print(rating_df.drop('user_id', axis=1).describe().loc[['count', 'mean', 'std', 'min', 'max']])
```

### 2. কলাবরেটিভ ফিল্টারিং (ইউজার-ইউজার)
```python
# ইউজার-ইউজার সিমিলারিটি
user_ratings = rating_df.drop('user_id', axis=1).fillna(0)
user_sim = cosine_similarity(user_ratings)
user_sim_df = pd.DataFrame(user_sim, index=range(n_users), columns=range(n_users))

print("User-User Similarity Matrix:")
print(f"Shape: {user_sim_df.shape}")
print(f"Mean similarity: {user_sim_df.values[np.triu_indices(n_users, k=1)].mean():.4f}")

# ইউজার-বেসড রিকমেন্ডেশন
def recommend_for_user(user_id, n_recommendations=5):
    # সিমিলার ইউজার খুঁজে
    sim_users = user_sim_df[user_id].sort_values(ascending=False)
    sim_users = sim_users[sim_users.index != user_id]
    
    # টপ 10 সিমিলার ইউজার
    top_users = sim_users.head(10)
    
    # ইউজারের দেখা স্টক
    user_watched = rating_df.iloc[user_id].drop('user_id').dropna().index
    
    # রেটিং ওয়েটেড এভারেজ
    recommendations = {}
    for stock in rating_df.columns.drop('user_id'):
        if stock not in user_watched:
            ratings_for_stock = rating_df.loc[top_users.index, stock]
            valid_ratings = ratings_for_stock.dropna()
            if len(valid_ratings) > 0:
                weighted_score = np.average(
                    valid_ratings.values,
                    weights=top_users[valid_ratings.index].values
                )
                recommendations[stock] = weighted_score
    
    # টপ রিকমেন্ডেশন
    recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    return recommendations[:n_recommendations]

# উদাহরণ
user_id = 5
recommendations = recommend_for_user(user_id)
print(f"\n🎯 User {user_id} Recommendations (Collaborative):")
for stock, score in recommendations:
    stock_info_row = stock_info[stock_info['ticker'] == stock].iloc[0]
    print(f"  {stock} ({stock_info_row['sector']}, Market Cap: ${stock_info_row['market_cap']}B) - Score: {score:.2f}")
```

### 3. আইটেম-বেসড কলাবরেটিভ ফিল্টারিং
```python
# আইটেম-আইটেম সিমিলারিটি
item_ratings = rating_df.drop('user_id', axis=1).fillna(0).T
item_sim = cosine_similarity(item_ratings)
item_sim_df = pd.DataFrame(item_sim, index=item_ratings.index, columns=item_ratings.index)

print("Item-Item Similarity Matrix:")
print(f"Shape: {item_sim_df.shape}")

# আইটেম-বেসড রিকমেন্ডেশন
def recommend_similar_stocks(ticker, n_recommendations=5):
    similar = item_sim_df[ticker].sort_values(ascending=False)
    similar = similar[similar.index != ticker]
    return similar.head(n_recommendations)

# উদাহরণ
example_stock = 'STK_010'
similar_stocks = recommend_similar_stocks(example_stock)
print(f"\n📈 Stocks similar to {example_stock}:")
for stock, sim_score in similar_stocks.items():
    stock_info_row = stock_info[stock_info['ticker'] == stock].iloc[0]
    print(f"  {stock} (Sector: {stock_info_row['sector']}) - Similarity: {sim_score:.4f}")
```

### 4. কন্টেন্ট-বেসড ফিল্টারিং
```python
# স্টক ফিচার ভেক্টরাইজেশন
stock_features = pd.get_dummies(stock_info[['sector']], columns=['sector'])
stock_features['market_cap'] = stock_info['market_cap'] / 1000  # স্কেল
stock_features['volatility'] = stock_info['volatility']

# সিমিলারিটি
stock_content_sim = cosine_similarity(stock_features)
stock_content_sim_df = pd.DataFrame(
    stock_content_sim, 
    index=stock_info['ticker'], 
    columns=stock_info['ticker']
)

# কন্টেন্ট-বেসড রিকমেন্ডেশন
def content_based_recommend(ticker, n=5):
    similar = stock_content_sim_df[ticker].sort_values(ascending=False)
    similar = similar[similar.index != ticker]
    return similar.head(n)

print("📊 Content-Based Recommendations:")
example = 'STK_005'
content_recs = content_based_recommend(example)
for stock, score in content_recs.items():
    info = stock_info[stock_info['ticker'] == stock].iloc[0]
    print(f"  {stock}: {info['sector']}, MCap=${info['market_cap']}B - Score: {score:.4f}")
```

### 5. ম্যাট্রিক্স ফ্যাক্টরাইজেশন (SVD)
```python
# SVD দিয়ে ম্যাট্রিক্স ফ্যাক্টরাইজেশন
user_item_matrix = rating_df.drop('user_id', axis=1).fillna(0)
n_factors = 10

svd = TruncatedSVD(n_components=n_factors, random_state=42)
user_factors = svd.fit_transform(user_item_matrix)
item_factors = svd.components_.T

# রিকন্সট্রাক্টেড ম্যাট্রিক্স
reconstructed = user_factors @ item_factors.T
reconstructed_df = pd.DataFrame(reconstructed, columns=user_item_matrix.columns)

print(f"User factors: {user_factors.shape}")
print(f"Item factors: {item_factors.shape}")
print(f"Explained variance: {svd.explained_variance_ratio_.sum():.4f}")

# SVD-বেসড রিকমেন্ডেশন
def svd_recommend(user_id, n=5):
    user_ratings = reconstructed_df.iloc[user_id]
    watched = rating_df.iloc[user_id].drop('user_id').dropna().index
    unseen = user_ratings.drop(watched).sort_values(ascending=False)
    return unseen.head(n)

print(f"\n🔮 SVD Recommendations for User {user_id}:")
svd_recs = svd_recommend(user_id)
for stock, score in svd_recs.items():
    info = stock_info[stock_info['ticker'] == stock].iloc[0]
    print(f"  {stock} ({info['sector']}) - Predicted: {score:.2f}")
```

### 6. হাইব্রিড রিকমেন্ডার
```python
# কলাবরেটিভ + কন্টেন্ট ব্লেন্ডিং
def hybrid_recommend(user_id, ticker, alpha=0.5, n=10):
    # কলাবরেটিভ স্কোর
    collab_recs = recommend_for_user(user_id, n=n)
    collab_scores = {stock: score for stock, score in collab_recs}
    
    # কন্টেন্ট স্কোর
    content_recs = content_based_recommend(ticker, n=n)
    content_scores = content_recs.to_dict()
    
    # সব স্টক
    all_stocks = set(list(collab_scores.keys()) + list(content_scores.keys()))
    
    # হাইব্রিড স্কোর
    hybrid_scores = {}
    for stock in all_stocks:
        collab = collab_scores.get(stock, 0)
        content = content_scores.get(stock, 0)
        hybrid_scores[stock] = alpha * collab + (1 - alpha) * content
    
    return sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n]

print("\n🎯 Hybrid Recommendations:")
hybrid_recs = hybrid_recommend(user_id=5, ticker='STK_010')
for stock, score in hybrid_recs:
    info = stock_info[stock_info['ticker'] == stock].iloc[0]
    print(f"  {stock} ({info['sector']}) - Hybrid Score: {score:.2f}")
```

### 7. ইভালুয়েশন মেট্রিক্স
```python
from sklearn.metrics import mean_squared_error

# প্রেডিকশন এরর
actual = rating_df.drop('user_id', axis=1).values
predicted = reconstructed_df.values

# শুধু নন-নাল ভ্যালু
mask = ~np.isnan(actual)
rmse = np.sqrt(mean_squared_error(actual[mask], predicted[mask]))

print(f"📊 Recommender System Metrics:")
print(f"  RMSE (prediction error): {rmse:.4f}")
print(f"  Coverage: {mask.sum() / mask.size:.2%}")

# Precision@K
def precision_at_k(recommended, relevant, k=5):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for r in recommended_k if r in relevant_set)
    return hits / k

print(f"  Precision@5: {precision_at_k([r[0] for r in recommendations], ['STK_001','STK_002'], k=5):.2%}")
```

### রিকমেন্ডার সিস্টেম বেস্ট প্র্যাকটিস
```python
print("""
✅ Recommender System Best Practices:
1️⃣ Handle cold-start problem (new users/items)
2️⃣ Consider implicit feedback (views, clicks)
3️⃣ Use hybrid approaches for better results
4️⃣ Regular model retraining
5️⃣ A/B test recommendations
6️⃣ Consider diversity (avoid filter bubbles)
7️⃣ Account for recency (newer items preferred)

⚖️ Trade-offs:
⚫ Collaborative: Better for established users, cold-start problem
⚫ Content-based: No cold-start, but less serendipity
⚫ Hybrid: Best of both, more complex
""")
```

### সারসংক্ষেপ
আজ আমরা রিকমেন্ডার সিস্টেম শিখলাম:
- **কলাবরেটিভ ফিল্টারিং**: User-User, Item-Item সিমিলারিটি
- **কন্টেন্ট-বেসড**: স্টক ফিচার ব্যবহার করে
- **ম্যাট্রিক্স ফ্যাক্টরাইজেশন**: SVD
- **হাইব্রিড**: কলাবরেটিভ + কন্টেন্ট কম্বাইন
- **ইভালুয়েশন**: RMSE, Precision@K

### অনুশীলনী
1. বিভিন্ন সিমিলারিটি মেট্রিক (Pearson, Euclidean) নিয়ে এক্সপেরিমেন্ট করুন
2. ইমপ্লিসিট ফিডব্যাক (ক্লিক, ভিউ) ব্যবহার করে রেটিং ইম্পিউট করুন
3. FunkSVD (SGD-based MF) অ্যালগরিদম ইমপ্লিমেন্ট করুন
4. নিউজ-বেসড রিকমেন্ডেশন সিস্টেম তৈরি করুন