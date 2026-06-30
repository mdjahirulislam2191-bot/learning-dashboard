"""
Day 15: Mini Project — Personal Finance Analyzer
==================================================
বিষয়: প্যান্ডাস + ম্যাটপ্লটলিব ব্যবহার করে সম্পূর্ণ ফাইন্যান্স বিশ্লেষক
লেখক: Jahirul Islam (Finance Grad, Canada)
উদ্দেশ্য: বাস্তব ফাইন্যান্স ডেটা লোড, বিশ্লেষণ ও ভিজুয়ালাইজেশন

এই প্রজেক্টে যা শিখবেন:
  ✓ সিএসভি ডেটা লোড করা
  ✓ ডেটা ক্লিনিং
  ✓ এগ্রিগেশন ও গ্রুপবাই
  ✓ ম্যাটপ্লটলিব দিয়ে ভিজুয়ালাইজেশন
  ✓ রিপোর্ট জেনারেট

প্রয়োজনীয় লাইব্রেরি:
  pip install pandas matplotlib numpy
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# ১. ডেটা জেনারেট / লোড
# ============================================================
print("=" * 65)
print("🏦 পার্সোনাল ফাইন্যান্স অ্যানালাইজার")
print("=" * 65)

# ডেটা জেনারেটর ফাংশন
def generate_finance_data(months=6, transactions_per_month=40):
    """
    সিমুলেটেড ফাইন্যান্স ডেটা জেনারেট করে।
    Parameters:
        months (int): কত মাসের ডেটা
        transactions_per_month (int): প্রতি মাসে লেনদেন সংখ্যা
    Returns:
        pd.DataFrame: ফাইন্যান্স ডেটাসেট
    """
    np.random.seed(42)
    
    # ক্যাটাগরি ও সাব-ক্যাটাগরি
    categories = {
        'আয়': ['বেতন', 'ফ্রিল্যান্সিং', 'বিনিয়োগ_লভ্যাংশ', 'অন্যান্য_আয়'],
        'খাদ্য': ['বাজার', 'রেস্টুরেন্ট', 'ফাস্ট_ফুড', 'স্ন্যাকস'],
        'ভাড়া_ও_বিল': ['বাসা_ভাড়া', 'বিদ্যুৎ', 'পানি', 'গ্যাস', 'ইন্টারনেট'],
        'পরিবহন': ['পেট্রোল', 'বাস_ভাড়া', 'উবার', 'গাড়ি_মেইন্টেন্যান্স'],
        'স্বাস্থ্য': ['ডাক্তার', 'ওষুধ', 'জিম'],
        'বিনোদন': ['সিনেমা', 'ভ্রমণ', 'গেমিং', 'স্ট্রিমিং'],
        'সঞ্চয়_ও_বিনিয়োগ': ['এফডিআর', 'মিউচুয়াল_ফান্ড', 'স্টক', 'ইমার্জেন্সি_ফান্ড'],
        'শিক্ষা': ['কোর্স', 'বই', 'সেমিনার'],
        'শপিং': ['পোশাক', 'ইলেকট্রনিক্স', 'গৃহস্থালি'],
        'অন্যান্য': ['উপহার', 'দান', 'অন্যান্য']
    }
    
    start_date = datetime(2024, 1, 1)
    records = []
    
    for month in range(months):
        month_date = start_date + timedelta(days=month * 30)
        for _ in range(transactions_per_month):
            day_offset = np.random.randint(1, 28)
            date = month_date.replace(day=day_offset)
            
            # আয় বা খরচ নির্ধারণ (৮০% খরচ, ২০% আয়)
            is_income = np.random.random() < 0.20
            
            if is_income:
                cat = 'আয়'
                sub = np.random.choice(categories[cat])
                amount = np.random.choice([45000, 50000, 55000, 60000, 8000, 10000, 5000, 3000, 2000])
            else:
                cat = np.random.choice(list(categories.keys() - {'আয়'}))
                sub = np.random.choice(categories[cat])
                # ক্যাটাগরি অনুযায়ী খরচের রেঞ্জ
                ranges = {
                    'খাদ্য': (100, 3000),
                    'ভাড়া_ও_বিল': (500, 20000),
                    'পরিবহন': (50, 2000),
                    'স্বাস্থ্য': (200, 5000),
                    'বিনোদন': (100, 2000),
                    'সঞ্চয়_ও_বিনিয়োগ': (1000, 15000),
                    'শিক্ষা': (200, 5000),
                    'শপিং': (200, 5000),
                    'অন্যান্য': (50, 3000)
                }
                low, high = ranges[cat]
                amount = np.random.randint(low, high + 1)
            
            records.append({
                'তারিখ': date,
                'ক্যাটাগরি': 'আয়' if is_income else 'খরচ',
                'ক্যাটাগরি_বিস্তারিত': cat,
                'সাব_ক্যাটাগরি': sub,
                'পরিমাণ': amount,
                'বিবরণ': f'{cat} - {sub}'
            })
    
    df = pd.DataFrame(records)
    df = df.sort_values('তারিখ').reset_index(drop=True)
    df['মাস'] = df['তারিখ'].dt.to_period('M').astype(str)
    df['দিনের_নাম'] = df['তারিখ'].dt.day_name()
    
    return df

print("\n📊 ডেটা জেনারেট হচ্ছে...")
df = generate_finance_data(months=6, transactions_per_month=45)
print(f"✅ মোট {len(df)}টি লেনদেন লোড করা হয়েছে")
print(f"📅 সময়কাল: {df['তারিখ'].min().date()} থেকে {df['তারিখ'].max().date()}")
print()


# ============================================================
# ২. ডেটা ক্লিনিং ও প্রিপ্রসেসিং
# ============================================================
print("=" * 65)
print("📋 ডেটা ক্লিনিং ও ওভারভিউ")
print("=" * 65)

print(f"\n🔍 ডেটার প্রথম ৫টি রো:")
print(df.head().to_string())

print(f"\n📈 ডেটার বেসিক ইনফো:")
print(f"  মোট লেনদেন        : {len(df)}")
print(f"  মোট আয়            : ৳{df[df['ক্যাটাগরি']=='আয়']['পরিমাণ'].sum():,.0f}")
print(f"  মোট খরচ            : ৳{df[df['ক্যাটাগরি']=='খরচ']['পরিমাণ'].sum():,.0f}")
print(f"  নেট সেভিংস         : ৳{df[df['ক্যাটাগরি']=='আয়']['পরিমাণ'].sum() - df[df['ক্যাটাগরি']=='খরচ']['পরিমাণ'].sum():,.0f}")

print(f"\n🔍 নাল ভ্যালু চেক: {df.isnull().sum().sum()}")
print(f"🔍 ডুপ্লিকেট চেক: {df.duplicated().sum()}")
print(f"🔍 ইউনিক ক্যাটাগরি: {df['ক্যাটাগরি_বিস্তারিত'].nunique()}")
print()


# ============================================================
# ৩. মেট্রিক্স ক্যালকুলেশন
# ============================================================
print("=" * 65)
print("📊 ফাইন্যান্স মেট্রিক্স")
print("=" * 65)

# আয়-খরচ আলাদা করা
income_df = df[df['ক্যাটাগরি'] == 'আয়']
expense_df = df[df['ক্যাটাগরি'] == 'খরচ']

total_income = income_df['পরিমাণ'].sum()
total_expense = expense_df['পরিমাণ'].sum()
net_savings = total_income - total_expense
savings_rate = (net_savings / total_income) * 100

print(f"\n💰 আয় ও খরচের সারসংক্ষেপ:")
print(f"  📌 মোট আয়      : ৳{total_income:>10,.0f}")
print(f"  📌 মোট খরচ      : ৳{total_expense:>10,.0f}")
print(f"  📌 নেট সেভিংস   : ৳{net_savings:>10,.0f}")
print(f"  📌 সেভিংস রেট   : {savings_rate:>9.1f}%")

# মাসিক মেট্রিক্স
monthly_income = income_df.groupby('মাস')['পরিমাণ'].sum()
monthly_expense = expense_df.groupby('মাস')['পরিমাণ'].sum()
monthly_net = monthly_income - monthly_expense

print(f"\n📅 মাসিক সারসংক্ষেপ:")
monthly_summary = pd.DataFrame({
    'আয়': monthly_income,
    'খরচ': monthly_expense,
    'নেট': monthly_net
})
print(monthly_summary.to_string())

# ক্যাটাগরি অনুযায়ী খরচ
expense_by_cat = expense_df.groupby('ক্যাটাগরি_বিস্তারিত')['পরিমাণ'].sum().sort_values(ascending=False)
print(f"\n📂 ক্যাটাগরি অনুযায়ী খরচ (টপ ৫):")
for cat, amount in expense_by_cat.head(5).items():
    pct = (amount / total_expense) * 100
    print(f"  {cat:15s}: ৳{amount:>8,.0f} ({pct:5.1f}%)")

# সেরা খরচের দিন
top_expense_day = df.loc[df['পরিমাণ'].idxmax()]
print(f"\n💰 সবচেয়ে বড় লেনদেন:")
print(f"  {top_expense_day['তারিখ'].date()} | {top_expense_day['ক্যাটাগরি_বিস্তারিত']} | {top_expense_day['সাব_ক্যাটাগরি']} | ৳{top_expense_day['পরিমাণ']:,.0f}")
print()


# ============================================================
# ৪. ভিজুয়ালাইজেশন
# ============================================================
print("=" * 65)
print("📈 চার্ট জেনারেট হচ্ছে...")
print("=" * 65)

# স্টাইল সেটিংস
plt.style.use('seaborn-v0_8-darkgrid')
colors_income_expense = ['#2ecc71', '#e74c3c']

# 4a. আয় vs খরচ — বার চার্ট
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('পার্সোনাল ফাইন্যান্স অ্যানালাইসিস রিপোর্ট', fontsize=16, fontweight='bold')

ax1 = axes[0, 0]
ax1.bar(['আয়', 'খরচ'], [total_income, total_expense], color=colors_income_expense, edgecolor='black', linewidth=1.5)
ax1.set_title('মোট আয় vs খরচ', fontsize=12, fontweight='bold')
ax1.set_ylabel('পরিমাণ (টাকা)')
for i, v in enumerate([total_income, total_expense]):
    ax1.text(i, v + 1000, f'৳{v:,.0f}', ha='center', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# 4b. মাসিক আয়-খরচ ট্রেন্ড — লাইন প্লট
ax2 = axes[0, 1]
months_labels = monthly_income.index.tolist()
ax2.plot(months_labels, monthly_income.values, marker='o', color='#2ecc71', linewidth=2, label='আয়')
ax2.plot(months_labels, monthly_expense.values, marker='s', color='#e74c3c', linewidth=2, label='খরচ')
ax2.plot(months_labels, monthly_net.values, marker='^', color='#3498db', linewidth=2, label='নেট সেভিংস')
ax2.set_title('মাসিক আয়, খরচ ও সেভিংস', fontsize=12, fontweight='bold')
ax2.set_xlabel('মাস')
ax2.set_ylabel('পরিমাণ (টাকা)')
ax2.legend()
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)

# 4c. খরচের পাই চার্ট
ax3 = axes[1, 0]
top_categories = expense_by_cat.head(6)
others = expense_by_cat.iloc[6:].sum() if len(expense_by_cat) > 6 else 0
if others > 0:
    top_categories = pd.concat([top_categories, pd.Series({'অন্যান্য': others})])
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(top_categories)))
ax3.pie(
    top_categories.values,
    labels=top_categories.index,
    autopct=lambda p: f'৳{int(p*sum(top_categories.values)/100):,}',
    colors=colors_pie,
    startangle=90,
    textprops={'fontsize': 9}
)
ax3.set_title('খরচের ক্যাটাগরি অনুযায়ী ভাঙ্গন', fontsize=12, fontweight='bold')

# 4d. হিস্টোগ্রাম
ax4 = axes[1, 1]
ax4.hist(expense_df['পরিমাণ'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
ax4.axvline(expense_df['পরিমাণ'].mean(), color='red', linestyle='dashed', linewidth=2, label=f"গড়: ৳{expense_df['পরিমাণ'].mean():.0f}")
ax4.axvline(expense_df['পরিমাণ'].median(), color='green', linestyle='dashed', linewidth=2, label=f"মধ্যমা: ৳{expense_df['পরিমাণ'].median():.0f}")
ax4.set_title('লেনদেনের পরিমাণ ডিস্ট্রিবিউশন', fontsize=12, fontweight='bold')
ax4.set_xlabel('পরিমাণ (টাকা)')
ax4.set_ylabel('লেনদেন সংখ্যা')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('day15_finance_report.png', dpi=120)
plt.show()
print("✅ ফাইন্যান্স রিপোর্ট সেভ করা হয়েছে: day15_finance_report.png\n")


# ============================================================
# ৫. উন্নত ভিজুয়ালাইজেশন
# ============================================================
print("=" * 65)
print("📈 উন্নত ভিজুয়ালাইজেশন")
print("=" * 65)

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
fig2.suptitle('উন্নত ফাইন্যান্স অ্যানালাইসিস', fontsize=14, fontweight='bold')

# 5a. সেভিংস রেট — গজ চার্ট (স্টাইলাইজড বার)
ax5 = axes2[0]
savings_rate_color = '#2ecc71' if savings_rate >= 20 else ('#f39c12' if savings_rate >= 10 else '#e74c3c')
ax5.barh(['সেভিংস রেট'], [savings_rate], color=savings_rate_color, edgecolor='black', height=0.5)
ax5.set_xlim(0, 100)
ax5.set_xlabel('শতাংশ (%)')
ax5.set_title(f'সেভিংস রেট: {savings_rate:.1f}%', fontsize=12, fontweight='bold')
ax5.text(savings_rate + 1, 0, f'{savings_rate:.1f}%', va='center', fontweight='bold')
ax5.grid(axis='x', alpha=0.3)

# আদর্শ সেভিংস রেট লাইন
ax5.axvline(20, color='green', linestyle=':', alpha=0.7, label='টার্গেট: ২০%')
ax5.axvline(10, color='orange', linestyle=':', alpha=0.7, label='মিনিমাম: ১০%')
ax5.legend(loc='upper right')

# 5b. সাপ্তাহিক খরচ প্যাটার্ন
ax6 = axes2[1]
expense_df['দিনের_নাম'] = expense_df['তারিখ'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_labels = ['সোম', 'মঙ্গল', 'বুধ', 'বৃহস্পতি', 'শুক্র', 'শনি', 'রবি']
day_expense = expense_df.groupby('দিনের_নাম')['পরিমাণ'].mean()
day_expense = day_expense.reindex(day_order)
ax6.bar(day_labels, day_expense.values, color=plt.cm.viridis(np.linspace(0.2, 0.8, 7)), edgecolor='black')
ax6.set_title('দিন অনুযায়ী গড় খরচ', fontsize=12, fontweight='bold')
ax6.set_xlabel('দিন')
ax6.set_ylabel('গড় খরচ (টাকা)')
ax6.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('day15_advanced_analysis.png', dpi=120)
plt.show()
print("✅ অ্যাডভান্সড অ্যানালাইসিস সেভ করা হয়েছে: day15_advanced_analysis.png\n")


# ============================================================
# ৬. টেক্সট রিপোর্ট
# ============================================================
print("=" * 65)
print("📄 ফাইন্যান্স রিপোর্ট")
print("=" * 65)

report = f"""
╔══════════════════════════════════════════════════════════════╗
║              পার্সোনাল ফাইন্যান্স রিপোর্ট                    ║
║              {df['তারিখ'].min().date()} - {df['তারিখ'].max().date()}                   ║
╠══════════════════════════════════════════════════════════════╣
║ 📊 এক্সিকিউটিভ সামারি                                      ║
║                                                              ║
║   মোট আয়            : ৳{total_income:>10,.0f}                           ║
║   মোট খরচ            : ৳{total_expense:>10,.0f}                           ║
║   নেট সেভিংস         : ৳{net_savings:>10,.0f}                           ║
║   সেভিংস রেট         : {savings_rate:>9.1f}%                               ║
║   মোট লেনদেন         : {len(df):>5d}                                     ║
║                                                              ║
║ 📈 সবচেয়ে বেশি খরচের ক্যাটাগরি:                              ║
"""
for cat, amount in expense_by_cat.head(3).items():
    pct = (amount / total_expense) * 100
    report += f"║   • {cat:20s}: ৳{amount:>8,.0f} ({pct:5.1f}%)                      ║\n"

report += f"""║                                                              ║
║ 💡 সুপারিশ:                                                ║
"""
if savings_rate < 10:
    report += f"""║   ⚠️  সেভিংস রেট খুব কম! ২০% টার্গেট করুন।                     ║"""
elif savings_rate < 20:
    report += f"""║   ✅ ভালো, কিন্তু আরও ২০% টার্গেটে উন্নতি করুন।                ║"""
else:
    report += f"""║   🎉 চমৎকার! আপনি ২০% এর বেশি সঞ্চয় করছেন!                  ║"""

report += f"""
╚══════════════════════════════════════════════════════════════╝
"""

print(report)
print()


# ============================================================
# ৭. এক্সপোর্ট অপশন
# ============================================================
print("=" * 65)
print("💾 ডেটা এক্সপোর্ট")
print("=" * 65)

# ডেটা সিএসভি-তে সেভ
df.to_csv('day15_finance_data.csv', index=False)
print("✅ ডেটা সেভ করা হয়েছে: day15_finance_data.csv")

# মাসিক সারসংখ্যা এক্সপোর্ট
monthly_summary.to_csv('day15_monthly_summary.csv')
print("✅ মাসিক সারসংক্ষেপ: day15_monthly_summary.csv")

# ক্যাটাগরি অনুযায়ী খরচ
expense_by_cat.to_csv('day15_category_expense.csv')
print("✅ ক্যাটাগরি অনুযায়ী খরচ: day15_category_expense.csv")
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 65)
print("📝 প্র্যাকটিস টাস্ক (Day 15)")
print("=" * 65)
print("""
🚀 চ্যালেঞ্জ ১: নিজের বাস্তব আয়-খরচের ডেটা নিয়ে এই প্রজেক্ট রান করুন।
   (এক্সেল/সিএসভি ফরম্যাটে ডেটা তৈরি করে df = pd.read_csv() দিয়ে লোড করুন)

🚀 চ্যালেঞ্জ ২: নতুন মেট্রিক যোগ করুন:
   - Debt-to-Income Ratio (ঋণ-আয় অনুপাত)
   - Emergency Fund Coverage (জরুরি তহবিল কভারেজ)
   - Year-over-Year growth

🚀 চ্যালেঞ্জ ৩: ক্যাটাগরি অনুযায়ী বাজেট সীমা নির্ধারণ করুন এবং
   সীমা অতিক্রম করলে সতর্কতা (alert) দেখান।

🚀 চ্যালেঞ্জ ৪: একটি Stacked Bar Chart তৈরি করুন যা মাসিক খরচের
   ক্যাটাগরি ভিত্তিক ভাঙ্গন দেখায়।

🚀 চ্যালেঞ্জ ৫: সব ফাইল (dataframe, charts, reports) একটি ফোল্ডারে
   'finance_report' নামে সেভ করুন।
""")