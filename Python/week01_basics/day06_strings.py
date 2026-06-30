"""
Day 6: স্ট্রিংস (Strings) এবং মেথডসমূহ
===========================================
লেখক: জাহিরুল ইসলাম
বিষয়: ফাইন্যান্স ও ডেটা অ্যানালাইসিসের জন্য পাইথন স্ট্রিং ম্যানিপুলেশন

তুমি কি জানো? ডেটা অ্যানালাইসিসের ৮০% সময়ই ডেটা ক্লিনিং এবং 
ফরম্যাটিং-এ কেটে যায়। স্ট্রিং ম্যানিপুলেশন শেখা মানে ডেটা 
প্রসেসিং-এ দক্ষ হওয়া।
"""

# ============================================================
# ১. স্ট্রিং বেসিক (String Basics)
# ============================================================

# স্ট্রিং তৈরি করা
stock_name = 'Apple Inc.'
ticker = "AAPL"
description = """Apple Inc. একটি টেকনোলজি কোম্পানি 
যা iPhone, iPad, Mac এবং অন্যান্য 
প্রোডাক্ট তৈরি করে।"""

print("=== স্ট্রিং বেসিক ===")
print(f"স্টকের নাম: {stock_name}")
print(f"টিকার: {ticker}")
print(f"বর্ণনা: {description}")
print()


# ============================================================
# ২. স্ট্রিং ইনডেক্সিং এবং স্লাইসিং
# ============================================================

print("=== ইনডেক্সিং এবং স্লাইসিং ===")

# ইনডেক্সিং
text = "PORTFOLIO"
print(f"টেক্সট: {text}")
print(f"প্রথম অক্ষর: '{text[0]}'")         # P
print(f"শেষ অক্ষর: '{text[-1]}'")           # O
print(f"তৃতীয় অক্ষর: '{text[2]}'")         # R
print(f"শেষ থেকে দ্বিতীয়: '{text[-2]}'")   # O

# স্লাইসিং [start:end:step]
print(f"প্রথম ৪টি: '{text[:4]}'")           # PORT
print(f"৪র্থ থেকে শেষ: '{text[4:]}'")        # FOLIO
print(f"মাঝের অংশ ২:৬: '{text[2:6]}'")       # RTFO
print(f"প্রতি ২য় অক্ষর: '{text[::2]}'")     # PRFO
print(f"রিভার্স: '{text[::-1]}'")            # OILOFITROP
print()


# ============================================================
# ৩. স্ট্রিং মেথডসমূহ (String Methods)
# ============================================================

print("=== স্ট্রিং মেথডসমূহ ===")

# upper(), lower(), title(), capitalize()
data = "  tesla motors, inc.  "
print(f"অরিজিনাল: '{data}'")
print(f"upper(): '{data.upper()}'")
print(f"lower(): '{data.lower()}'")
print(f"title(): '{data.title()}'")
print(f"capitalize(): '{data.capitalize()}'")

# strip() - স্পেস/ক্যারেক্টার রিমুভ করা
print(f"strip(): '{data.strip()}'")
print(f"lstrip(): '{data.lstrip()}'")
print(f"rstrip(): '{data.rstrip()}'")

# ফাইন্যান্সের উদাহরণ: ক্লিনিং স্টক ডেটা
dirty_data = "  $1,234.56  "
clean_data = dirty_data.strip().replace("$", "").replace(",", "")
print(f"\nডার্টি ডেটা: '{dirty_data}'")
print(f"ক্লিন ডেটা: '{clean_data}'")
print(f"ফ্লোটে রূপান্তর: {float(clean_data)}")
print()


# ============================================================
# ৪. স্প্লিট (split) এবং জয়েন (join)
# ============================================================

print("=== split() এবং join() ===")

# CSV ডেটা পার্সিং (ফাইন্যান্সে খুবই কমন!)
csv_line = "AAPL,150.25,152.80,149.10,151.50,78200000"
fields = csv_line.split(",")
print(f"CSV লাইন: {csv_line}")
print(f"পার্সড ফিল্ডস: {fields}")
print(f"টিকার: {fields[0]}")
print(f"ওপেন: ${float(fields[1]):.2f}")
print(f"হাই: ${float(fields[2]):.2f}")
print(f"লো: ${float(fields[3]):.2f}")
print(f"ক্লোজ: ${float(fields[4]):.2f}")
print(f"ভলিউম: {int(fields[5]):,}")

# জয়েন (join) - লিস্টকে স্ট্রিং এ রূপান্তর
stock_parts = ["GOOGL", "145.30", "148.20"]
joined = "|".join(stock_parts)
print(f"\nজয়েন করা ডেটা: {joined}")

# আরেকটি উদাহরণ
portfolio = ["Apple", "Microsoft", "Google", "Amazon"]
portfolio_str = ", ".join(portfolio)
print(f"পোর্টফোলিও: {portfolio_str}")
print()


# ============================================================
# ৫. f-স্ট্রিং এবং ফরম্যাটিং (আধুনিক ও সবচেয়ে ব্যবহৃত)
# ============================================================

print("=== f-স্ট্রিং ফরম্যাটিং ===")

name = "জাহিরুল ইসলাম"
age = 28
balance = 45230.789

# বেসিক f-string
print(f"নাম: {name}, বয়স: {age}, ব্যালেন্স: ${balance}")

# ফাইন্যান্সিয়াল ফরম্যাটিং
print(f"ব্যালেন্স (২ দশমিক): ${balance:.2f}")
print(f"ব্যালেন্স (কমা সহ): ${balance:,.2f}")
print(f"ব্যালেন্স (১০ ক্যারেক্টার): ${balance:>10,.2f}")
print(f"ব্যালেন্স (বামে): ${balance:<12.2f}")
print(f"ব্যালেন্স (মাঝে): ${balance:=^12.2f}")

# পার্সেন্টেজ ফরম্যাটিং
return_rate = 0.0875
print(f"রিটার্ন: {return_rate:.2%}")      # 8.75%
print(f"রিটার্ন: {return_rate:.1%}")      # 8.8%

# বড় সংখ্যা ফরম্যাটিং
revenue = 394328000000  # Apple-এর রেভিনিউ
print(f"রেভিনিউ: ${revenue:,}")          # কমা সহ
print(f"রেভিনিউ: ${revenue:,.0f}")       # $394,328,000,000

# একাধিক ভেরিয়েবল সহ
print(f"{'আইটেম':<15} {'মূল্য':>10} {'পরিমাণ':>8} {'মোট':>12}")
print("-" * 45)
print(f"{'Apple Stock':<15} {'$150.25':>10} {'100':>8} {'$15,025.00':>12}")
print(f"{'Microsoft':<15} {'$380.50':>10} {'50':>8} {'$19,025.00':>12}")
print()


# ============================================================
# ৬. পুরনো ফরম্যাটিং স্টাইল (% এবং .format())
# ============================================================

print("=== পুরনো ফরম্যাটিং স্টাইল ===")

# % ফরম্যাটিং (%s = string, %d = integer, %f = float)
name = "Tesla"
price = 245.678
print("স্টক: %s, মূল্য: $%.2f" % (name, price))

# .format() মেথড
print("স্টক: {}, মূল্য: ${:.2f}".format(name, price))
print("স্টক: {0}, মূল্য: ${1:.2f}, টিকার: {0}".format(name, price))
print("স্টক: {stock}, মূল্য: ${pr:.2f}".format(stock=name, pr=price))
print()


# ============================================================
# ৭. ক্যারেক্টার সার্চ এবং রিপ্লেস
# ============================================================

print("=== সার্চ এবং রিপ্লেস ===")

text = "Apple Inc. (AAPL) is a technology company based in Cupertino, California."

# find() এবং index()
print(f"টেক্সট: {text}")
print(f"'Apple' এর অবস্থান: {text.find('Apple')}")
print(f"'technology' এর অবস্থান: {text.index('technology')}")
print(f"'Google' খুঁজছে: {text.find('Google')}")  # -1 রিটার্ন করবে (নেই)

# count()
print(f"'a' এর সংখ্যা: {text.count('a')}")
print(f"'e' এর সংখ্যা: {text.count('e')}")

# startswith() এবং endswith()
print(f"'Apple' দিয়ে শুরু?: {text.startswith('Apple')}")
print(f"'California.' দিয়ে শেষ?: {text.endswith('California.')}")

# replace()
updated = text.replace("Apple Inc.", "Tesla Inc.")
print(f"রিপ্লেসের পর: {updated}")

# কেস চেকিং
code = "AAPL"
print(f"সব বড়হাতের?: {code.isupper()}")
print(f"সব ছোটহাতের?: {code.islower()}")
print(f"আলফানিউমেরিক?: {code.isalnum()}")

# স্টক প্রাইস ভালিডেশন
price_str = "150.25"
print(f"ডিজিটাল?: {price_str.isdigit()}")  # False (ডট আছে)
print(f"ডেসিমাল?: {price_str.isdecimal()}")  # False
print()


# ============================================================
# ৮. ফাইন্যান্সিয়াল ডেটা ক্লিনিং (রিয়েল-ওয়ার্ল্ড উদাহরণ)
# ============================================================

print("=== ফাইন্যান্সিয়াল ডেটা ক্লিনিং ===")

# ডার্টি ডেটা থেকে ক্লিন ডেটা বানানো
dirty_records = [
    "  AAPL , $150.25 , +2.5%  ",
    "  MSFT , $380.50 , +1.2%  ",
    "  GOOGL , $140.80 , -0.5%  ",
    "  AMZN , $178.20 , +0.8%  ",
]

def clean_stock_record(record):
    """
    একটি স্টক রেকর্ড ক্লিন করে স্ট্রাকচার্ড ডেটায় রূপান্তর করে।
    """
    # স্পেস রিমুভ এবং কমা দিয়ে স্প্লিট
    parts = [p.strip() for p in record.split(",")]
    
    ticker = parts[0]
    price_str = parts[1].replace("$", "").strip()
    change_str = parts[2].replace("%", "").strip()
    
    price = float(price_str)
    change = float(change_str) / 100  # পার্সেন্টেজকে ডেসিমালে
    
    return {
        "ticker": ticker,
        "price": price,
        "change": change
    }

print(f"{'টিকার':<8} {'মূল্য':<12} {'পরিবর্তন':<12} {'স্ট্যাটাস':<10}")
print("-" * 42)

for record in dirty_records:
    cleaned = clean_stock_record(record)
    status = "📈 বেড়েছে" if cleaned["change"] > 0 else "📉 কমেছে"
    print(f"{cleaned['ticker']:<8} ${cleaned['price']:<8.2f} {cleaned['change']*100:<+6.2f}% {status:<10}")

print()


# ============================================================
# ৯. রেগুলার এক্সপ্রেশন (RegEx) বেসিক - প্যাটার্ন ম্যাচিং
# ============================================================

import re

print("=== রেগুলার এক্সপ্রেশন (RegEx) ===")

# ইমেল অ্যাড্রেস এক্সট্র্যাক্ট
text = "Contact us at support@finance.com or ceo@company.org"
emails = re.findall(r'\S+@\S+', text)
print(f"ইমেলগুলো: {emails}")

# ফোন নাম্বার ভ্যালিডেশন
phone_pattern = r'\+\d{1,3}-\d{3}-\d{3}-\d{4}'
phone = "+1-416-555-0198"
if re.match(phone_pattern, phone):
    print(f"✅ বৈধ ফোন নাম্বার: {phone}")
else:
    print(f"❌ অকার্যকর ফোন নাম্বার: {phone}")

# স্টক টিকার ভ্যালিডেশন (বড়হাতের ১-৫ অক্ষর)
tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "abc", "123", "BRK.A"]
valid_ticker = r'^[A-Z]{1,5}$'

for t in tickers:
    if re.match(valid_ticker, t):
        print(f"✅ বৈধ টিকার: {t}")
    else:
        print(f"❌ অকার্যকর টিকার: {t}")

# ডলারের অ্যামাউন্ট এক্সট্র্যাক্ট
report = "Q1 Revenue: $85.3B, Net Income: $23.2B, EPS: $1.53"
amounts = re.findall(r'\$\d+\.?\d*[BMK]?', report)
print(f"\nএক্সট্রাক্টেড অ্যামাউন্ট: {amounts}")
print()


# ============================================================
# ১০. এসকেপ ক্যারেক্টার এবং র স্ট্রিং
# ============================================================

print("=== এসকেপ ক্যারেক্টার ===")

# কমন এসকেপ সিকোয়েন্স
print("লাইন ১\nলাইন ২")           # \n = নিউ লাইন
print("কলাম 1\tকলাম 2\tকলাম 3")     # \t = ট্যাব
print("সে বলল, \"হ্যালো\"")       # \" = ডাবল কোট
print("পাথ: C:\\Users\\Jahirul")  # \\ = ব্যাকস্ল্যাশ

# র স্ট্রিং (Raw String) - ব্যাকস্ল্যাশকে এসকেপ করে না
raw_path = r"C:\Users\Jahirul"
normal_path = "C:" + "\\Users\\Jahirul"
print(f"র পাথ: {raw_path}")
print(f"নরমাল পাথ: {normal_path}")

# ফাইন্যান্স রিপোর্ট প্রিন্টিং
print("\n" + "=" * 40)
print("মাসিক বিনিয়োগ রিপোর্ট")
print("=" * 40)
print(f"তারিখ:\t\t2024-12-01")
print(f"বিনিয়োগকারী:\t{name}")
print(f"মোট মূল্য:\t${balance:>8,.2f}")
print(f"দৈনিক পরিবর্তন:\t{return_rate:>+7.2%}")
print("=" * 40)
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================

print("=" * 60)
print("📝 প্র্যাকটিস টাস্ক - নিজে করুন!")
print("=" * 60)

print("""
টাস্ক ১: CSV পার্সার
    একটি ফাংশন তৈরি করুন যা কমা সেপারেটেড স্টক ডেটা পার্স করে
    এবং একটি ডিকশনারি রিটার্ন করে।
    ইনপুট: "AAPL,150.25,152.80,149.10,151.50,78200000"
    আউটপুট: {'ticker': 'AAPL', 'open': 150.25, 'high': 152.80, ...}

টাস্ক ২: ফাইন্যান্সিয়াল ফরম্যাটার
    একটি ফাংশন তৈরি করুন যা যেকোনো সংখ্যাকে ফাইন্যান্সিয়াল ফরম্যাটে
    রূপান্তর করে:
    - 1234.5 -> "$1,234.50"
    - 1000000 -> "$1,000,000.00"
    - 0.05 -> "5.00%"

টাস্ক ৩: টিকার ভালিডেটর
    একটি ফাংশন তৈরি করুন যা একটি লিস্ট থেকে শুধুমাত্র বৈধ
    স্টক টিকার (১-৫ বড়হাতের অক্ষর) বের করে।

টাস্ক ৪: ডেটা ক্লিনার
    একটি ফাংশন তৈরি করুন যা ডার্টি ফাইন্যান্সিয়াল ডেটা থেকে
    অপ্রয়োজনীয় ক্যারেক্টার ($, %, কমা, স্পেস) রিমুভ করে
    এবং ক্লিন ডেটা রিটার্ন করে।
""")

print("--- ইঙ্গিত (Hints) ---")
print("""
# টাস্ক ১ এর জন্য ইঙ্গিত:
def parse_csv_line(csv_line):
    parts = csv_line.split(',')
    return {
        'ticker': parts[0],
        'open': float(parts[1]),
        'high': float(parts[2]),
        'low': float(parts[3]),
        'close': float(parts[4]),
        'volume': int(parts[5])
    }

# টাস্ক ২ এর জন্য ইঙ্গিত:
def format_currency(amount):
    return f"${amount:,.2f}"

# টাস্ক ৪ এর জন্য ইঙ্গিত:
def clean_value(dirty_str):
    return float(dirty_str.strip().replace('$', '').replace(',', '').replace('%', ''))
""")