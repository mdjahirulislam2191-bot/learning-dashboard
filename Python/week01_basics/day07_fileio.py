"""
Day 7: ফাইল I/O (File Input/Output)
======================================
লেখক: জাহিরুল ইসলাম
বিষয়: ফাইন্যান্স ও ডেটা অ্যানালাইসিসের জন্য ফাইল রিডিং এবং রাইটিং

তুমি কি জানো? ডেটা অ্যানালাইস্ট হিসেবে প্রতিদিন CSV, TXT, JSON 
ফাইল নিয়ে কাজ করতে হবে। ফাইল I/O ছাড়া ডেটা অ্যানালাইসিস সম্ভব না!
"""

import os
from datetime import datetime

# ============================================================
# ১. ফাইল খোলা এবং পড়া (Open and Read Files)
# ============================================================

print("=== ফাইল খোলা এবং পড়া ===")

# একটি নমুনা ফাইল তৈরি করা (যদি না থাকে)
sample_expense_file = os.path.expanduser("~/LearningPath/Python/week01_basics/expenses.txt")

# ফাইল না থাকলে তৈরি করুন
if not os.path.exists(sample_expense_file):
    with open(sample_expense_file, "w", encoding="utf-8") as f:
        f.write("তারিখ,ক্যাটাগরি,বিবরণ,পরিমাণ\n")
        f.write("2024-01-05,খাদ্য,গ্রোসারি স্টোর,120.50\n")
        f.write("2024-01-06,পরিবহন,গ্যাস/পেট্রোল,65.00\n")
        f.write("2024-01-07,বিনোদন,নেটফ্লিক্স সাবস্ক্রিপশন,18.99\n")
        f.write("2024-01-08,খাদ্য,রেস্টুরেন্ট ডিনার,85.40\n")
        f.write("2024-01-09,ইউটিলিটি,বিদ্যুৎ বিল,145.30\n")
        f.write("2024-01-10,পরিবহন,উবার রাইড,22.50\n")
        f.write("2024-01-11,খাদ্য,কফি শপ,6.75\n")
        f.write("2024-01-12,বিনোদন,সিনেমা টিকেট,15.00\n")
        f.write("2024-01-13,স্বাস্থ্য,জিম মেম্বারশিপ,55.00\n")
        f.write("2024-01-14,ইউটিলিটি,ইন্টারনেট বিল,89.99\n")
    print(f"✅ নমুনা ফাইল তৈরি করা হয়েছে: {sample_expense_file}")

# ফাইল রিড করা - পদ্ধতি ১: read() পুরো ফাইল
print("\n1️⃣ read() পদ্ধতি:")
with open(sample_expense_file, "r", encoding="utf-8") as file:
    content = file.read()
print(content[:200] + "...")  # প্রথম ২০০ ক্যারেক্টার
print()


# ============================================================
# ২. ফাইল রিড করার বিভিন্ন পদ্ধতি
# ============================================================

print("=== বিভিন্ন রিডিং পদ্ধতি ===")

# readline() - লাইন বাই লাইন
print("2️⃣ readline() পদ্ধতি:")
with open(sample_expense_file, "r", encoding="utf-8") as file:
    header = file.readline().strip()
    print(f"হেডার: {header}")
    first_line = file.readline().strip()
    print(f"প্রথম লাইন: {first_line}")
print()

# readlines() - সব লাইন লিস্ট আকারে
print("3️⃣ readlines() পদ্ধতি:")
with open(sample_expense_file, "r", encoding="utf-8") as file:
    lines = file.readlines()
    print(f"মোট লাইন সংখ্যা: {len(lines)}")
    print(f"প্রথম ৩ লাইন: {lines[:3]}")
print()

# লুপ ব্যবহার করে (সবচেয়ে এফিশিয়েন্ট)
print("4️⃣ লুপ ব্যবহার করে:")
with open(sample_expense_file, "r", encoding="utf-8") as file:
    for i, line in enumerate(file):
        if i == 0:  # হেডার স্কিপ
            continue
        if i > 3:   # প্রথম ৩ ডেটা লাইন দেখাবো
            break
        date, category, description, amount = line.strip().split(",")
        print(f"📅 {date} | {category} | {description} | ${float(amount):.2f}")
print()


# ============================================================
# ৩. ফাইল রাইটিং (Writing to Files)
# ============================================================

print("=== ফাইল রাইটিং ===")

# write() - ওভাররাইট মোড ('w')
portfolio_file = os.path.expanduser("~/LearningPath/Python/week01_basics/portfolio_summary.txt")

with open(portfolio_file, "w", encoding="utf-8") as file:
    file.write("=" * 60 + "\n")
    file.write("পোর্টফোলিও সামারি\n")
    file.write(f"জেনারেটেড: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write("=" * 60 + "\n\n")
    file.write(f"{'টিকার':<8} {'শেয়ার':<8} {'মূল্য':<12} {'মোট মূল্য':<15} {'ওজন':<10}\n")
    file.write("-" * 53 + "\n")

    portfolio_data = [
        ("AAPL", 100, 150.25),
        ("MSFT", 50, 380.50),
        ("GOOGL", 25, 140.80),
        ("AMZN", 30, 178.20),
        ("TSLA", 40, 245.60),
    ]

    total_value = sum(shares * price for _, shares, price in portfolio_data)

    for ticker, shares, price in portfolio_data:
        total = shares * price
        weight = (total / total_value) * 100
        file.write(f"{ticker:<8} {shares:<8} ${price:<8.2f} ${total:<10,.2f} {weight:<7.2f}%\n")

    file.write("-" * 53 + "\n")
    file.write(f"{'মোট':<8} {'':<8} {'':<12} ${total_value:<10,.2f} {'100.00%':<10}\n")
    file.write("=" * 60 + "\n")

print(f"✅ পোর্টফোলিও সামারি তৈরি: {portfolio_file}")

# ফাইল দেখানো
with open(portfolio_file, "r", encoding="utf-8") as f:
    print(f.read())
print()


# ============================================================
# ৪. অ্যাপেন্ড মোড (Appending to Files)
# ============================================================

print("=== অ্যাপেন্ড মোড ('a') ===")

log_file = os.path.expanduser("~/LearningPath/Python/week01_basics/activity_log.txt")

# প্রথম বার তৈরি
with open(log_file, "a", encoding="utf-8") as file:
    file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] প্রোগ্রাম স্টার্ট\n")
    file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] পোর্টফোলিও তৈরি করা হয়েছে\n")
    file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ব্যবহারকারী: জাহিরুল ইসলাম\n")

print(f"✅ লগ ফাইল তৈরি: {log_file}")
with open(log_file, "r", encoding="utf-8") as f:
    print(f.read())
print()


# ============================================================
# ৫. with স্টেটমেন্ট (Context Manager)
# ============================================================

print("=== with স্টেটমেন্ট ===")

# with স্টেটমেন্ট ছাড়া (ম্যানুয়ালি ক্লোজ করতে হয়)
print("🟡 পদ্ধতি ১ (with ছাড়া - ঝামেলাপূর্ণ):")
file = open(sample_expense_file, "r", encoding="utf-8")
try:
    data = file.read()
    print(f"  ✅ ডেটা পড়া হয়েছে: {len(data)} ক্যারেক্টার")
finally:
    file.close()  # ম্যানুয়ালি ক্লোজ করতে হবে
print()

# with স্টেটমেন্ট সহ (অটো ক্লোজ - রেকমেন্ডেড)
print("🟢 পদ্ধতি ২ (with সহ - রেকমেন্ডেড):")
with open(sample_expense_file, "r", encoding="utf-8") as file:
    data = file.read()
    print(f"  ✅ ডেটা পড়া হয়েছে: {len(data)} ক্যারেক্টার")
    # ফাইল অটোমেটিক ক্লোজ হয়ে যাবে
print(f"  ✅ ফাইল ক্লোজ হয়েছে? {file.closed}")  # True
print()


# ============================================================
# ৬. CSV ফাইল প্রসেসিং (ফাইন্যান্সে সবচেয়ে কমন)
# ============================================================

print("=== CSV ফাইল প্রসেসিং ===")

import csv

# CSV ফাইল রিড করা
csv_file = os.path.expanduser("~/LearningPath/Python/week01_basics/transactions.csv")

# নমুনা CSV তৈরি
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Type", "Symbol", "Shares", "Price", "Total"])
    writer.writerow(["2024-01-15", "BUY", "AAPL", 10, 150.25, 1502.50])
    writer.writerow(["2024-01-20", "BUY", "MSFT", 5, 380.50, 1902.50])
    writer.writerow(["2024-02-01", "SELL", "AAPL", 3, 155.80, 467.40])
    writer.writerow(["2024-02-10", "BUY", "GOOGL", 8, 140.80, 1126.40])
    writer.writerow(["2024-02-15", "BUY", "AMZN", 5, 178.20, 891.00])
    writer.writerow(["2024-03-01", "SELL", "MSFT", 2, 395.00, 790.00])

print(f"✅ CSV ফাইল তৈরি: {csv_file}")

# CSV ডেটা পড়া এবং বিশ্লেষণ
print("\n📊 ট্রানজেকশন বিশ্লেষণ:")
total_buy = 0
total_sell = 0
buy_count = 0
sell_count = 0

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # DictReader! হেডার অটো ডিটেক্ট করে
    for row in reader:
        print(f"  {row['Date']} | {row['Type']:4} | {row['Symbol']:5} | "
              f"{row['Shares']:>3} শেয়ার | ${float(row['Total']):>7.2f}")
        if row["Type"] == "BUY":
            total_buy += float(row["Total"])
            buy_count += 1
        else:
            total_sell += float(row["Total"])
            sell_count += 1

print(f"\n📈 মোট ক্রয় ({buy_count}টি): ${total_buy:,.2f}")
print(f"📉 মোট বিক্রয় ({sell_count}টি): ${total_sell:,.2f}")
print(f"💵 নেট ক্যাশ ফ্লো: ${total_sell - total_buy:,.2f}")
print()


# ============================================================
# ৭. JSON ফাইল প্রসেসিং (API ডেটার জন্য)
# ============================================================

print("=== JSON ফাইল প্রসেসিং ===")

import json

# স্টক ডেটা JSON
stock_data = {
    "portfolio": {
        "owner": "Jahirul Islam",
        "created": "2024-12-01",
        "total_value": 45230.79
    },
    "holdings": [
        {"ticker": "AAPL", "shares": 100, "avg_price": 145.30},
        {"ticker": "MSFT", "shares": 50, "avg_price": 370.20},
        {"ticker": "GOOGL", "shares": 25, "avg_price": 138.50},
    ],
    "performance": {
        "daily_change": 0.012,
        "ytd_return": 0.085,
        "volatility": 0.18
    }
}

# JSON ফাইলে রাইট করা
json_file = os.path.expanduser("~/LearningPath/Python/week01_basics/portfolio.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(stock_data, f, indent=4)  # indent=4 ফরম্যাটেড আউটপুট
print(f"✅ JSON ফাইল তৈরি: {json_file}")

# JSON ফাইল রিড করা
with open(json_file, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print("পোর্টফোলিও মালিক:", loaded_data["portfolio"]["owner"])
print("মোট হোল্ডিংস:", len(loaded_data["holdings"]))
print("YTD রিটার্ন: {:.2%}".format(loaded_data["performance"]["ytd_return"]))
print()


# ============================================================
# ৮. ফাইল চেক করা - os.path এবং pathlib
# ============================================================

print("=== ফাইল চেক করা ===")

# os.path ব্যবহার করে
print(f"📂 ফাইল আছে? {os.path.exists(csv_file)}")
print(f"📂 ফাইলের সাইজ: {os.path.getsize(csv_file)} bytes")
print(f"📂 শেষ মডিফাই: {datetime.fromtimestamp(os.path.getmtime(csv_file))}")
print(f"📂 ফাইল নাকি ডিরেক্টরি? {'ফাইল' if os.path.isfile(csv_file) else 'ডিরেক্টরি'}")

# pathlib (আধুনিক পদ্ধতি)
from pathlib import Path

p = Path(csv_file)
print(f"\n📂 pathlib ব্যবহার:")
print(f"  ফাইল নাম: {p.name}")
print(f"  স্টেম: {p.stem}")
print(f"  এক্সটেনশন: {p.suffix}")
print(f"  প্যারেন্ট: {p.parent}")
print()


# ============================================================
# ৯. একাধিক ফাইল একসাথে ম্যানেজ করা
# ============================================================

print("=== একাধিক ফাইল প্রসেসিং ===")

# expense_report_analysis ফাংশন
def analyze_expenses(file_path):
    """
    এক্সপেন্স ফাইল রিড করে ক্যাটাগরি অনুযায়ী টোটাল বের করে।
    """
    expenses = {}
    total = 0
    line_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        next(f)  # হেডার স্কিপ
        for line in f:
            line = line.strip()
            if not line:
                continue
            date, category, desc, amount = line.split(",")
            amount = float(amount)
            
            # ক্যাটাগরি অনুযায়ী যোগ
            if category not in expenses:
                expenses[category] = 0
            expenses[category] += amount
            total += amount
            line_count += 1

    return expenses, total, line_count

# এক্সপেন্স অ্যানালাইসিস করা
ex_categories, ex_total, ex_count = analyze_expenses(sample_expense_file)

print(f"মোট এন্ট্রি: {ex_count}")
print(f"মোট খরচ: ${ex_total:.2f}")
print("\nক্যাটাগরি অনুযায়ী খরচ:")
print("-" * 40)
for cat, amount in sorted(ex_categories.items(), key=lambda x: x[1], reverse=True):
    pct = (amount / ex_total) * 100
    bar = "█" * int(pct // 5)
    print(f"{cat:<12} ${amount:<7.2f} ({pct:5.1f}%) {bar}")
print()


# ============================================================
# ১০. ফাইল এনকোডিং (File Encoding)
# ============================================================

print("=== ফাইল এনকোডিং ===")

# UTF-8 এনকোডিং (সবচেয়ে কমন, বাংলা সাপোর্ট করে)
encoded_file = os.path.expanduser("~/LearningPath/Python/week01_basics/bangla_finance.txt")

with open(encoded_file, "w", encoding="utf-8") as f:
    f.write("বিনিয়োগ বিশ্লেষণ রিপোর্ট\n")
    f.write("আয়: ১,২৫,০০০ টাকা\n")
    f.write("খরচ: ৮৫,০০০ টাকা\n")
    f.write("সঞ্চয়: ৪০,০০০ টাকা\n")

with open(encoded_file, "r", encoding="utf-8") as f:
    bangla_content = f.read()

print("বাংলা ফাইলের কন্টেন্ট:")
print(bangla_content)
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================

print("=" * 60)
print("📝 প্র্যাকটিস টাস্ক - নিজে করুন!")
print("=" * 60)

print("""
টাস্ক ১: সেলস রিপোর্ট জেনারেটর
    products.txt ফাইল থেকে প্রোডাক্টের নাম, মূল্য, এবং বিক্রির পরিমাণ
    পড়ে একটি ফরম্যাটেড সেলস রিপোর্ট তৈরি করুন।

টাস্ক ২: CSV ফিল্টার
    transaction.csv ফাইল থেকে শুধুমাত্র 'SELL' ট্রানজেকশনগুলো ফিল্টার
    করে আলাদা sells.csv ফাইলে সেভ করুন।

টাস্ক ৩: মাল্টি-ফাইল মার্জার
    একাধিক expense_jan.txt, expense_feb.txt ইত্যাদি ফাইল থেকে ডেটা
    পড়ে একটি combined_expense.txt ফাইল তৈরি করুন।

টাস্ক ৪: JSON আপডেটার
    portfolio.json ফাইল থেকে ডেটা পড়ুন, নতুন একটি স্টক যোগ করুন
    এবং আপডেটেড ডেটা আবার JSON ফাইলে সেভ করুন।
""")

print("--- ইঙ্গিত (Hints) ---")
print("""
# টাস্ক ২ এর জন্য ইঙ্গিত:
def filter_sells(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \\
         open(output_file, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if row[1] == 'SELL':
                writer.writerow(row)

# টাস্ক ৪ এর জন্য ইঙ্গিত:
def add_stock(json_path, new_stock):
    with open(json_path, 'r') as f:
        data = json.load(f)
    data['holdings'].append(new_stock)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
""")