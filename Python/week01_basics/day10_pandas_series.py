"""
Day 10 — Pandas Series পরিচিতি (Pandas Series Introduction)
=============================================================
লেখক: Jahirul Islam
বিষয়: Pandas Series — তৈরি, ইনডেক্সিং, ফিল্টারিং, ম্যাথ অপস
ফাইন্যান্স উদাহরণ: মাসিক আয়ের সিরিজ (Monthly Income Series)

কি শিখবো:
  1. Pandas ইম্পোর্ট ও Series তৈরি
  2. কাস্টম ইনডেক্স (লেবেল)
  3. সিরিজ থেকে ডেটা সিলেক্ট ও ফিল্টার
  4. ম্যাথ অপারেশন (গণিত)
  5. ফাইন্যান্সিয়াল ডেটা বিশ্লেষণ
"""

import pandas as pd
import numpy as np

# ============================================================
# ১. Pandas Series তৈরি (Creating a Series)
# ============================================================

print("=" * 60)
print("১. Pandas Series তৈরি")
print("=" * 60)

# লিস্ট থেকে Series
monthly_income = pd.Series([4500, 4800, 5100, 4900, 5200, 5500])
print("মাসিক আয় (ডিফল্ট ইনডেক্স):")
print(monthly_income)
print()

print("Series টাইপ:", type(monthly_income))
print("ডেটা টাইপ (dtype):", monthly_income.dtype)
print("মোট এলিমেন্ট:", len(monthly_income))
print()

# কাস্টম ইনডেক্স সহ Series
months = ['জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন']
income_with_index = pd.Series([4500, 4800, 5100, 4900, 5200, 5500], index=months)
print("মাসিক আয় (কাস্টম ইনডেক্স):")
print(income_with_index)
print()

# ডিকশনারি থেকে Series
expenses_dict = {
    'জানুয়ারি': 3200,
    'ফেব্রুয়ারি': 3100,
    'মার্চ': 3300,
    'এপ্রিল': 3150,
    'মে': 3400,
    'জুন': 3250
}
monthly_expenses = pd.Series(expenses_dict)
print("মাসিক খরচ (ডিকশনারি থেকে):")
print(monthly_expenses)
print()

# scalar মান থেকে Series — সব ইনডেক্সে একই মান
tax_rate = pd.Series(0.15, index=months)
print("কর হার (প্রতি মাসে ১৫%):")
print(tax_rate)
print()

# NumPy অ্যারে থেকে Series
np_array = np.array([4500, 4800, 5100, 4900, 5200, 5500])
income_from_np = pd.Series(np_array, index=months)
print("NumPy অ্যারে থেকে Series:")
print(income_from_np)
print()

# ============================================================
# ২. Series থেকে ডেটা অ্যাক্সেস (Indexing & Selection)
# ============================================================

print("=" * 60)
print("২. Series থেকে ডেটা অ্যাক্সেস")
print("=" * 60)

print("মাসিক আয় সিরিজ:")
print(income_with_index)

# পজিশনাল ইনডেক্স (iloc) — ০ থেকে শুরু
print("\n--- পজিশনাল ইনডেক্সিং (iloc) ---")
print("প্রথম মাসের আয় (iloc[0]):", income_with_index.iloc[0])
print("তৃতীয় মাসের আয় (iloc[2]):", income_with_index.iloc[2])
print("শেষ মাসের আয় (iloc[-1]):", income_with_index.iloc[-1])
print("প্রথম ৩ মাস (iloc[:3]):")
print(income_with_index.iloc[:3])

# লেবেল-ভিত্তিক ইনডেক্স (loc)
print("\n--- লেবেল ইনডেক্সিং (loc) ---")
print("মার্চের আয় (loc['মার্চ']):", income_with_index.loc['মার্চ'])
print("জানুয়ারি-মার্চ (loc['জানুয়ারি':'মার্চ']):")
print(income_with_index.loc['জানুয়ারি':'মার্চ'])

# ডিরেক্ট লেবেল এক্সেস (loc ছাড়াও)
print("\n--- ডিরেক্ট লেবেল এক্সেস ---")
print("এপ্রিল:", income_with_index['এপ্রিল'])
print("মে ও জুন:", income_with_index[['মে', 'জুন']])
print()

# ============================================================
# ৩. Series ফিল্টারিং (Filtering — Boolean Indexing)
# ============================================================

print("=" * 60)
print("৩. Series ফিল্টারিং (শর্ত দিয়ে ডেটা বাছাই)")
print("=" * 60)

print("মাসিক আয়:")
print(income_with_index)
print()

# ৫০০০-এর উপরে আয়ের মাস
high_income = income_with_index[income_with_index > 5000]
print("৫০০০-এর উপরে আয়ের মাস:")
print(high_income)
print()

# নির্দিষ্ট রেঞ্জের আয়
mid_income = income_with_index[(income_with_index >= 4700) & (income_with_index <= 5100)]
print("৪৭০০-৫১০০ রেঞ্জের আয়ের মাস:")
print(mid_income)
print()

# ইনডেক্স চেক করা (কোন মাসে আয় বেশি?)
above_avg = income_with_index > income_with_index.mean()
print("গড়ের উপরে আয়ের মাস (bool):")
print(above_avg)
print("গড়ের উপরে আয়ের মাসগুলোর আয়:")
print(income_with_index[above_avg])
print()

# ============================================================
# ৪. Series-এ ম্যাথ অপারেশন (Mathematical Operations)
# ============================================================

print("=" * 60)
print("৪. Series-এ ম্যাথ অপারেশন")
print("=" * 60)

print("মাসিক আয়:")
print(income_with_index)
print("মাসিক খরচ:")
print(monthly_expenses)
print()

# দুটি Series-এর মধ্যে অপারেশন
savings = income_with_index - monthly_expenses
print("প্রতি মাসে সঞ্চয় (আয় - খরচ):")
print(savings)
print(f"মোট সঞ্চয়: ${savings.sum()}")
print()

# স্কেলার অপারেশন (ব্রডকাস্টিং)
income_doubled = income_with_index * 2
print("আয় দ্বিগুণ:")
print(income_doubled)

# কর গণনা (১৫%)
tax_amount = income_with_index * 0.15
print("\nপ্রতি মাসে কর (১৫%):")
print(tax_amount)
print(f"মোট কর: ${tax_amount.sum():.2f}")

# শুধু আয়ের ৭০% (হাতে পাওয়া)
after_tax = income_with_index * 0.85
print("\nকর পরে হাতে পাওয়া (৮৫%):")
print(after_tax)
print()

# ============================================================
# ৫. বিল্ট-ইন পরিসংখ্যান মেথড (Built-in Statistics)
# ============================================================

print("=" * 60)
print("৫. Series-এ পরিসংখ্যান")
print("=" * 60)

print("মাসিক আয় পরিসংখ্যান:")
print(f"  মোট আয় (sum):           ${income_with_index.sum()}")
print(f"  গড় আয় (mean):           ${income_with_index.mean():.2f}")
print(f"  মধ্যমা (median):        ${income_with_index.median():.2f}")
print(f"  সর্বনিম্ন (min):        ${income_with_index.min()}")
print(f"  সর্বোচ্চ (max):         ${income_with_index.max()}")
print(f"  স্ট্যান্ডার্ড ডেভিয়েশন: ${income_with_index.std():.2f}")
print(f"  ভ্যারিয়েন্স:            ${income_with_index.var():.2f}")

# describe() — সব গুরুত্বপূর্ণ পরিসংখ্যান একসাথে
print("\ndescribe() — একবারেই সব:")
print(income_with_index.describe())
print()

# ============================================================
# ৬. ফাইন্যান্সিয়াল উদাহরণ: আয়-ব্যয় বিশ্লেষণ
# ============================================================

print("=" * 60)
print("৬. আয়-ব্যয় বিশ্লেষণ")
print("=" * 60)

# সঞ্চয়ের হার
savings_rate = (savings / income_with_index) * 100
print("প্রতি মাসে সঞ্চয়ের হার (%):")
print(savings_rate.round(2))
print(f"গড় সঞ্চয়ের হার: {savings_rate.mean():.2f}%")
print()

# কোন মাসে সবচেয়ে বেশি সঞ্চয়?
best_month = savings.idxmax()    # ইনডেক্স (মাসের নাম)
best_value = savings.max()
print(f"সবচেয়ে বেশি সঞ্চয় হয়েছে: {best_month} (${best_value})")

# কোন মাসে সবচেয়ে কম সঞ্চয়?
worst_month = savings.idxmin()
worst_value = savings.min()
print(f"সবচেয়ে কম সঞ্চয় হয়েছে: {worst_month} (${worst_value})")
print()

# খরচের শতাংশ
expense_pct = (monthly_expenses / income_with_index) * 100
print("প্রতি মাসে খরচের হার (%):")
print(expense_pct.round(2))
print(f"গড় খরচের হার: {expense_pct.mean():.2f}%")
print()

# ============================================================
# ৭. Series মেথডস — দরকারি ফাংশন
# ============================================================

print("=" * 60)
print("৭. দরকারি Series মেথডস")
print("=" * 60)

# সর্ট করা
sorted_income = income_with_index.sort_values()
print("আয় অনুযায়ী সর্টেড (ছোট → বড়):")
print(sorted_income)

sorted_desc = income_with_index.sort_values(ascending=False)
print("\nআয় অনুযায়ী সর্টেড (বড় → ছোট):")
print(sorted_desc)

# ইনডেক্স অনুযায়ী সর্ট
sorted_index = income_with_index.sort_index()
print("\nইনডেক্স (মাস) অনুযায়ী সর্টেড:")
print(sorted_index)

# head() ও tail()
print("\nপ্রথম ৩ মাসের আয় (head):")
print(income_with_index.head(3))
print("\nশেষ ২ মাসের আয় (tail):")
print(income_with_index.tail(2))

# unique() ও value_counts()
income_with_dup = pd.Series([4500, 4800, 5100, 4500, 5200, 4800], index=months)
print("\nunique মান:", income_with_dup.unique())
print("প্রতি ইউনিক মানের কাউন্ট:")
print(income_with_dup.value_counts())
print()

# ============================================================
# ৮. ভ্যালু যোগ/পরিবর্তন (Adding/Updating Values)
# ============================================================

print("=" * 60)
print("৮. Series-এ ভ্যালু যোগ ও পরিবর্তন")
print("=" * 60)

# নতুন মাস যোগ করা
new_income = income_with_index.copy()
new_income['জুলাই'] = 5800
new_income['আগস্ট'] = 5600
print("নতুন মাস যোগ করার পর:")
print(new_income)
print()

# ভ্যালু আপডেট
new_income['জানুয়ারি'] = 4700   # জানুয়ারির আয় আপডেট
print("জানুয়ারি আপডেট করার পর:")
print(new_income.head(3))
print()

# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 60)
print("🎯 প্র্যাকটিস টাস্ক")
print("=" * 60)
print("""
টাস্ক ১: ১২ মাসের জন্য একটি মাসিক বেতন Series তৈরি করুন
         (বাংলা মাসের নাম ইনডেক্স হিসেবে)। প্রতি মাসের খরচের
         Series তৈরি করে মাসিক সঞ্চয় এবং সঞ্চয়ের হার বের করুন।
         
টাস্ক ২: ৫টি কোম্পানির স্টক প্রাইস নিয়ে একটি Series তৈরি করুন
         (কোম্পানির নাম ইনডেক্স)। ৫% প্রাইস বৃদ্ধির পরে নতুন
         প্রাইস বের করুন। কোন কোম্পানির প্রাইস সবচেয়ে বেশি?
         
টাস্ক ৩: একটি Series-এ ৩০টি র্যান্ডম ডেইলি রিটার্ন জেনারেট করুন
         (np.random.normal)। এদের উপর পরিসংখ্যান (mean, std,
         min, max) বের করুন এবং কতগুলি রিটার্ন পজিটিভ তা গণনা
         করুন। পজিটিভ রিটার্নগুলির গড় কত?
""")
