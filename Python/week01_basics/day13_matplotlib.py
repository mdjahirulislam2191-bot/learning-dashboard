"""
Day 13: Matplotlib Basics — ভিজুয়ালাইজেশন
==============================================
বিষয়: লাইন প্লট, বার চার্ট, পাই চার্ট, হিস্টোগ্রাম
লেখক: Jahirul Islam (Finance Grad, Canada)
উদ্দেশ্য: Matplotlib ব্যবহার করে ফাইন্যান্স ডেটা ভিজুয়ালাইজ করা

প্রয়োজনীয় লাইব্রেরি:
  pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Bangla ফন্ট সেটআপ (যদি সিস্টেমে Bangla ফন্ট থাকে)
# ============================================================
# plt.rcParams['font.family'] = 'Siyam Rupali'  # অথবা 'Noto Sans Bengali'
# plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. লাইন প্লট (Line Plot) — আয়ের ট্রেন্ড
# ============================================================
print("=" * 60)
print("১. লাইন প্লট: মাসিক আয়ের ট্রেন্ড")
print("=" * 60)

months = ['জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন']
income = [45000, 47000, 46000, 51000, 53000, 55000]  # টাকায়

plt.figure(figsize=(10, 5))
plt.plot(months, income, marker='o', linestyle='-', color='green', linewidth=2, markersize=8, label='মাসিক আয়')
plt.title('মাসিক আয়ের ট্রেন্ড (২০২৪)', fontsize=14, fontweight='bold')
plt.xlabel('মাস', fontsize=12)
plt.ylabel('আয় (টাকা)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('day13_income_trend.png', dpi=100)
plt.show()
print("✅ লাইন প্লট সেভ করা হয়েছে: day13_income_trend.png\n")


# ============================================================
# 2. বার চার্ট (Bar Chart) — ক্যাটাগরি অনুযায়ী খরচ
# ============================================================
print("=" * 60)
print("২. বার চার্ট: ক্যাটাগরি অনুযায়ী মাসিক খরচ")
print("=" * 60)

categories = ['ভাড়া', 'খাবার', 'পরিবহন', 'বিনোদন', 'সঞ্চয়', 'ইউটিলিটি']
expenses = [15000, 8000, 3000, 2500, 5000, 2000]  # টাকায়
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, expenses, color=colors, edgecolor='black', linewidth=1.2)

# প্রতিটি বারের উপরে মান দেখানো
for bar, val in zip(bars, expenses):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'৳{val:,}', ha='center', fontsize=10, fontweight='bold')

plt.title('ক্যাটাগরি অনুযায়ী মাসিক খরচ', fontsize=14, fontweight='bold')
plt.xlabel('খরচের ক্যাটাগরি', fontsize=12)
plt.ylabel('খরচ (টাকা)', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('day13_expense_bar.png', dpi=100)
plt.show()
print("✅ বার চার্ট সেভ করা হয়েছে: day13_expense_bar.png\n")


# ============================================================
# 3. পাই চার্ট (Pie Chart) — খরচের অনুপাত
# ============================================================
print("=" * 60)
print("৩. পাই চার্ট: খরচের অনুপাত (Expense Breakdown)")
print("=" * 60)

labels = ['ভাড়া', 'খাবার', 'পরিবহন', 'বিনোদন', 'সঞ্চয়', 'ইউটিলিটি']
sizes = [15000, 8000, 3000, 2500, 5000, 2000]
explode = (0.05, 0.02, 0.02, 0.02, 0.05, 0.02)  # ভাড়া ও সঞ্চয় একটু আলাদা করে দেখানো

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct=lambda p: f'৳{int(p*sum(sizes)/100):,}\n({p:.1f}%)',
    explode=explode,
    colors=colors,
    startangle=90,
    textprops={'fontsize': 11}
)
# শতাংশের লেখা সাদা ও বোল্ড করা
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.title('মাসিক খরচের ভাঙ্গন (Expense Breakdown)', fontsize=14, fontweight='bold')
plt.axis('equal')  # পাই চার্টকে গোলাকার রাখে
plt.tight_layout()
plt.savefig('day13_expense_pie.png', dpi=100)
plt.show()
print("✅ পাই চার্ট সেভ করা হয়েছে: day13_expense_pie.png\n")


# ============================================================
# 4. হিস্টোগ্রাম (Histogram) — খরচের ডিস্ট্রিবিউশন
# ============================================================
print("=" * 60)
print("৪. হিস্টোগ্রাম: দৈনিক খরচের ডিস্ট্রিবিউশন")
print("=" * 60)

# সিমুলেটেড দৈনিক খরচ ডেটা (৩০ দিন)
np.random.seed(42)
daily_expenses = np.random.normal(loc=1200, scale=300, size=30).astype(int)
daily_expenses = np.clip(daily_expenses, 500, 2500)  # ৫০০-২৫০০ টাকার মধ্যে রাখা

plt.figure(figsize=(10, 5))
counts, bins, patches = plt.hist(
    daily_expenses,
    bins=10,
    color='skyblue',
    edgecolor='black',
    alpha=0.8,
    density=False
)

plt.title('দৈনিক খরচের ডিস্ট্রিবিউশন (৩০ দিন)', fontsize=14, fontweight='bold')
plt.xlabel('দৈনিক খরচ (টাকা)', fontsize=12)
plt.ylabel('দিন সংখ্যা', fontsize=12)
plt.grid(True, alpha=0.3)

# গড় ও মধ্যমা দেখানো
mean_exp = np.mean(daily_expenses)
median_exp = np.median(daily_expenses)
plt.axvline(mean_exp, color='red', linestyle='dashed', linewidth=2, label=f'গড়: ৳{mean_exp:.0f}')
plt.axvline(median_exp, color='green', linestyle='dashed', linewidth=2, label=f'মধ্যমা: ৳{median_exp:.0f}')
plt.legend()

plt.tight_layout()
plt.savefig('day13_expense_hist.png', dpi=100)
plt.show()
print(f"✅ হিস্টোগ্রাম সেভ করা হয়েছে: day13_expense_hist.png")
print(f"   গড় দৈনিক খরচ: ৳{mean_exp:.0f}")
print(f"   মধ্যমা: ৳{median_exp:.0f}")
print(f"   সর্বনিম্ন: ৳{daily_expenses.min()}, সর্বোচ্চ: ৳{daily_expenses.max()}")
print()


# ============================================================
# 5. সাবপ্লট (Subplots) — একসাথে সব প্লট
# ============================================================
print("=" * 60)
print("৫. সাবপ্লট: একসাথে সব চার্ট")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ব্যক্তিগত ফাইন্যান্স ভিজুয়ালাইজেশন ড্যাশবোর্ড', fontsize=16, fontweight='bold')

# উপরে-বাম: আয়ের লাইন প্লট
ax1 = axes[0, 0]
ax1.plot(months, income, marker='o', color='green', linewidth=2)
ax1.set_title('মাসিক আয়ের ট্রেন্ড')
ax1.set_xlabel('মাস')
ax1.set_ylabel('আয় (টাকা)')
ax1.grid(True, alpha=0.3)

# উপরে-ডান: খরচের বার চার্ট
ax2 = axes[0, 1]
ax2.bar(categories, expenses, color=colors)
ax2.set_title('ক্যাটাগরি অনুযায়ী খরচ')
ax2.set_xlabel('ক্যাটাগরি')
ax2.set_ylabel('খরচ (টাকা)')
ax2.tick_params(axis='x', rotation=45)

# নিচে-বাম: পাই চার্ট
ax3 = axes[1, 0]
ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax3.set_title('খরচের অনুপাত')

# নিচে-ডান: হিস্টোগ্রাম
ax4 = axes[1, 1]
ax4.hist(daily_expenses, bins=10, color='skyblue', edgecolor='black', alpha=0.8)
ax4.axvline(mean_exp, color='red', linestyle='dashed', linewidth=2, label=f'গড়: ৳{mean_exp:.0f}')
ax4.set_title('দৈনিক খরচের ডিস্ট্রিবিউশন')
ax4.set_xlabel('খরচ (টাকা)')
ax4.set_ylabel('দিন সংখ্যা')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('day13_dashboard.png', dpi=120)
plt.show()
print("✅ ড্যাশবোর্ড সেভ করা হয়েছে: day13_dashboard.png\n")


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 60)
print("📝 প্র্যাকটিস টাস্ক (Day 13)")
print("=" * 60)
print("""
১. আপনার নিজের ৬ মাসের আয়-খরচ ডেটা নিয়ে একটি লাইন প্লট তৈরি করুন।
২. পাই চার্টে explode প্যারামিটার পরিবর্তন করে ভিন্ন ভিন্ন সেক্টর আলাদা করে দেখান।
৩. তিনটি ভিন্ন ক্যাটাগরির (খাদ্য, ভাড়া, বিল) জন্য পাশাপাশি বার চার্ট তৈরি করুন।
৪. হিস্টোগ্রামে bins সংখ্যা পরিবর্তন করে (৫, ১৫, ২০) দেখুন ডিস্ট্রিবিউশন কেমন পরিবর্তন হয়।
৫. নিজের পছন্দের color scheme ব্যবহার করে একটি কাস্টম ড্যাশবোর্ড তৈরি করুন।
""")