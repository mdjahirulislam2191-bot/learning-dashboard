"""
Day 14: Aggregation — গ্রুপবাই ও পিভট টেবিল
==============================================
বিষয়: GroupBy, Pivot Tables, Aggregation Functions
লেখক: Jahirul Islam (Finance Grad, Canada)
উদ্দেশ্য: Pandas ব্যবহার করে ফাইন্যান্স ডেটা এগ্রিগেট করা

প্রয়োজনীয় লাইব্রেরি:
  pip install pandas numpy
"""

import pandas as pd
import numpy as np

# ============================================================
# ১. ডেটাসেট তৈরি — মাসিক খরচের রেকর্ড
# ============================================================
print("=" * 70)
print("১. ফাইন্যান্স ডেটাসেট তৈরি")
print("=" * 70)

np.random.seed(42)
dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')

# ক্যাটাগরি ও পেমেন্ট মেথড
categories = ['ভাড়া', 'খাবার', 'পরিবহন', 'বিনোদন', 'ইউটিলিটি', 'স্বাস্থ্য']
payment_methods = ['নগদ', 'কার্ড', 'মোবাইল ব্যাংকিং']
shops = ['সুপারশপ', 'অনলাইন', 'স্থানীয় দোকান', 'মল']

# র্যান্ডম ডেটা জেনারেট
data = {
    'তারিখ': np.random.choice(dates, size=200),
    'ক্যাটাগরি': np.random.choice(categories, size=200, p=[0.25, 0.20, 0.10, 0.15, 0.20, 0.10]),
    'পরিমাণ': np.random.randint(100, 5000, size=200),
    'পেমেন্ট_মেথড': np.random.choice(payment_methods, size=200, p=[0.3, 0.4, 0.3]),
    'দোকান': np.random.choice(shops, size=200, p=[0.35, 0.25, 0.25, 0.15])
}

df = pd.DataFrame(data)
df = df.sort_values('তারিখ').reset_index(drop=True)
df['মাস'] = df['তারিখ'].dt.to_period('M').astype(str)  # মাস কলাম যোগ
df['দিন'] = df['তারিখ'].dt.day_name()  # দিনের নাম যোগ

print(f"✅ ডেটাসেট তৈরি: {len(df)}টি লেনদেন")
print(df.head(10).to_string())
print()


# ============================================================
# ২. GroupBy — ক্যাটাগরি অনুযায়ী সমষ্টি
# ============================================================
print("=" * 70)
print("২. GroupBy: ক্যাটাগরি অনুযায়ী এগ্রিগেশন")
print("=" * 70)

# ক্যাটাগরি অনুযায়ী মোট খরচ
cat_total = df.groupby('ক্যাটাগরি')['পরিমাণ'].sum().sort_values(ascending=False)
print("\n📊 ক্যাটাগরি অনুযায়ী মোট খরচ:")
print(cat_total.to_string())

# ক্যাটাগরি অনুযায়ী গড় খরচ
cat_mean = df.groupby('ক্যাটাগরি')['পরিমাণ'].mean().sort_values(ascending=False)
print(f"\n📊 ক্যাটাগরি অনুযায়ী গড় খরচ (প্রতি লেনদেন):")
print(cat_mean.to_string())

# একাধিক এগ্রিগেশন ফাংশন
cat_agg = df.groupby('ক্যাটাগরি')['পরিমাণ'].agg(['sum', 'mean', 'count', 'min', 'max', 'std'])
print(f"\n📊 ক্যাটাগরি অনুযায়ী সব এগ্রিগেশন:")
print(cat_agg.to_string())
print()


# ============================================================
# ৩. মাসিক খরচ — ক্যাটাগরি অনুযায়ী
# ============================================================
print("=" * 70)
print("৩. মাসিক খরচ বিশ্লেষণ")
print("=" * 70)

monthly_by_cat = df.groupby(['মাস', 'ক্যাটাগরি'])['পরিমাণ'].sum().unstack(fill_value=0)
print(f"\n📊 মাসিক খরচ (ক্যাটাগরি অনুযায়ী):")
print(monthly_by_cat.to_string())

# মাসিক মোট খরচ
monthly_total = df.groupby('মাস')['পরিমাণ'].sum()
print(f"\n📊 মাসিক মোট খরচ:")
print(monthly_total.to_string())

# মাসিক লেনদেন সংখ্যা
monthly_count = df.groupby('মাস')['পরিমাণ'].count()
print(f"\n📊 মাসিক লেনদেন সংখ্যা:")
print(monthly_count.to_string())
print()


# ============================================================
# ৪. পেমেন্ট মেথড অনুযায়ী বিশ্লেষণ
# ============================================================
print("=" * 70)
print("৪. পেমেন্ট মেথড বিশ্লেষণ")
print("=" * 70)

payment_agg = df.groupby('পেমেন্ট_মেথড').agg(
    মোট_খরচ=('পরিমাণ', 'sum'),
    গড়_খরচ=('পরিমাণ', 'mean'),
    লেনদেন_সংখ্যা=('পরিমাণ', 'count')
).sort_values('মোট_খরচ', ascending=False)
print(f"\n📊 পেমেন্ট মেথড অনুযায়ী:")
print(payment_agg.to_string())
print()


# ============================================================
# ৫. পিভট টেবিল (Pivot Table)
# ============================================================
print("=" * 70)
print("৫. পিভট টেবিল — মাস × ক্যাটাগরি")
print("=" * 70)

pivot_month_cat = pd.pivot_table(
    df,
    values='পরিমাণ',
    index='মাস',
    columns='ক্যাটাগরি',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='সর্বমোট'
)
print(f"\n📊 পিভট টেবিল — মাস × ক্যাটাগরি:")
print(pivot_month_cat.to_string())
print()

# পিভট টেবিল — পেমেন্ট মেথড × ক্যাটাগরি
pivot_payment_cat = pd.pivot_table(
    df,
    values='পরিমাণ',
    index='পেমেন্ট_মেথড',
    columns='ক্যাটাগরি',
    aggfunc=['sum', 'count'],
    fill_value=0
)
print(f"\n📊 পিভট টেবিল — পেমেন্ট মেথড × ক্যাটাগরি:")
print(pivot_payment_cat.to_string())
print()


# ============================================================
# ৬. উন্নত এগ্রিগেশন — একাধিক গ্রুপ
# ============================================================
print("=" * 70)
print("৬. উন্নত এগ্রিগেশন — ক্যাটাগরি × পেমেন্ট মেথড")
print("=" * 70)

cat_payment = df.groupby(['ক্যাটাগরি', 'পেমেন্ট_মেথড'])['পরিমাণ'].agg(['sum', 'mean', 'count'])
print(f"\n📊 ক্যাটাগরি × পেমেন্ট মেথড:")
print(cat_payment.to_string())
print()


# ============================================================
# ৭. সাপ্তাহিক ও দিনভিত্তিক বিশ্লেষণ
# ============================================================
print("=" * 70)
print("৭. সাপ্তাহিক ও দিনভিত্তিক বিশ্লেষণ")
print("=" * 70)

# দিন অনুযায়ী খরচ
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_names_bn = {'Monday': 'সোমবার', 'Tuesday': 'মঙ্গলবার', 'Wednesday': 'বুধবার',
                'Thursday': 'বৃহস্পতিবার', 'Friday': 'শুক্রবার', 'Saturday': 'শনিবার', 'Sunday': 'রবিবার'}

day_expense = df.groupby('দিন')['পরিমাণ'].agg(['sum', 'mean', 'count'])
day_expense.index = day_expense.index.map(day_names_bn)
day_expense = day_expense.reindex([day_names_bn[d] for d in day_order])
print(f"\n📊 দিন অনুযায়ী খরচ:")
print(day_expense.to_string())
print()


# ============================================================
# ৮. টপ এন আইটেম — সর্বোচ্চ খরচ
# ============================================================
print("=" * 70)
print("৮. টপ বিশ্লেষণ")
print("=" * 70)

# সর্বোচ্চ ১০টি লেনদেন
top_10 = df.nlargest(10, 'পরিমাণ')[['তারিখ', 'ক্যাটাগরি', 'পরিমাণ', 'পেমেন্ট_মেথড', 'দোকান']]
print(f"\n📊 সর্বোচ্চ ১০টি খরচ:")
print(top_10.to_string())

# সর্বনিম্ন ৫টি লেনদেন
bottom_5 = df.nsmallest(5, 'পরিমাণ')[['তারিখ', 'ক্যাটাগরি', 'পরিমাণ', 'পেমেন্ট_মেথড']]
print(f"\n📊 সর্বনিম্ন ৫টি খরচ:")
print(bottom_5.to_string())
print()


# ============================================================
# ৯. ক্যাটাগরি অনুযায়ী শতাংশ
# ============================================================
print("=" * 70)
print("৯. ক্যাটাগরি অনুযায়ী খরচের শতাংশ")
print("=" * 70)

cat_pct = (df.groupby('ক্যাটাগরি')['পরিমাণ'].sum() / df['পরিমাণ'].sum() * 100).sort_values(ascending=False)
print(f"\n📊 প্রতিটি ক্যাটাগরির শতাংশ:")
for cat, pct in cat_pct.items():
    bar = '█' * int(pct)
    print(f"  {cat:10s}: {pct:5.1f}% {bar}")

total_expense = df['পরিমাণ'].sum()
print(f"\n  মোট খরচ: ৳{total_expense:,.0f}")
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 70)
print("📝 প্র্যাকটিস টাস্ক (Day 14)")
print("=" * 70)
print("""
১. উপরের ডেটাসেটে 'দোকান' কলাম ব্যবহার করে GroupBy করে দেখুন কোন দোকানে সবচেয়ে বেশি খরচ হয়েছে।
২. পিভট টেবিলে 'মাস' × 'পেমেন্ট_মেথড' ক্রস-সেকশন তৈরি করুন।
৩. 'ক্যাটাগরি' অনুযায়ী প্রতিটি পেমেন্ট মেথডের শতাংশ বের করুন।
৪. নিজের ১০টি লেনদেনের ডেটা নিয়ে একটি ছোট ডেটাসেট তৈরি করে সব ফাংশন প্রয়োগ করুন।
৫. প্রতি মাসে কোন ক্যাটাগরিতে খরচ বেড়েছে বা কমেছে তা বের করুন (Month-over-Month change)।
""")