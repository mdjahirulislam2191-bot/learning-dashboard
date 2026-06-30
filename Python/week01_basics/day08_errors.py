"""
Day 8: এরর হ্যান্ডলিং (Error Handling)
==========================================
লেখক: জাহিরুল ইসলাম
বিষয়: ফাইন্যান্স ও ডেটা অ্যানালাইসিসের জন্য পাইথন এরর হ্যান্ডলিং

তুমি কি জানো? ফাইন্যান্স সফটওয়্যারে এরর হ্যান্ডলিং ক্রিটিকাল!
একটি ভুল ইনপুট বা ফাইল মিস করলে পুরো ক্যালকুলেশন ভুল হতে পারে।
এরর হ্যান্ডলিং শেখা মানে প্রোডাকশন-রেডি কোড লেখা।
"""

# ============================================================
# ১. এরর এর প্রকারভেদ (Types of Errors)
# ============================================================

print("=== এররের প্রকারভেদ ===")

# Syntax Error - কোডের সিনট্যাক্স ভুল
print("❌ SyntaxError: প্রোগ্রাম রান করার আগেই ধরা পড়ে")
print("উদাহরণ: print 'হ্যালো' (() না থাকলে)")
print()

# Runtime Error - প্রোগ্রাম চলাকালীন এরর
print("❌ Runtime Error: প্রোগ্রাম চলাকালীন হয়")
print("যেমন: ০ দিয়ে ভাগ, ফাইল না পাওয়া, টাইপ মিসম্যাচ")
print()


# ============================================================
# ২. কমন এক্সেপশন (Common Exceptions)
# ============================================================

print("=== কমন এক্সেপশন ===")

print("""
🔴 ZeroDivisionError: ০ দিয়ে ভাগ করলে
🔴 FileNotFoundError: ফাইল না পেলে
🔴 ValueError: ভুল টাইপের ভ্যালু পাস করলে
🔴 TypeError: ভুল টাইপের অপারেশন করলে
🔴 IndexError: ভুল ইনডেক্স ব্যবহার করলে
🔴 KeyError: ডিকশনারিতে কী না থাকলে
🔴 NameError: ভেরিয়েবল ডিফাইন না থাকলে
🔴 AttributeError: অবজেক্টের অ্যাট্রিবিউট না থাকলে
""")

# প্রতিটি এররের উদাহরণ (কমেন্টেড - আনকমেন্ট করে দেখতে পারো)
# print(10 / 0)           # ZeroDivisionError
# open("nonexistent.txt")  # FileNotFoundError
# int("abc")              # ValueError
# "hello" + 5             # TypeError
# [1,2,3][10]             # IndexError
# print(undefined_var)    # NameError
print()


# ============================================================
# ৩. try/except ব্লক - বেসিক
# ============================================================

print("=== try/except বেসিক ===")

def safe_divide(a, b):
    """
    নিরাপদে দুটি সংখ্যা ভাগ করে। ০ দিয়ে ভাগ করলে এরর ধরে।
    """
    try:
        result = a / b
        print(f"  ✅ {a} / {b} = {result:.2f}")
        return result
    except ZeroDivisionError:
        print(f"  ❌ এরর: শূন্য দিয়ে ভাগ করা যাবে না!")
        return None

# টেস্ট
safe_divide(100, 5)    # কাজ করবে
safe_divide(100, 0)    # এরর ধরবে
safe_divide(250, 3)    # কাজ করবে
print()


# ============================================================
# ৪. একাধিক except ব্লক এবং নির্দিষ্ট এক্সেপশন
# ============================================================

print("=== একাধিক except ব্লক ===")

def calculate_stock_value(ticker, shares, price):
    """
    স্টকের মূল্য ক্যালকুলেট করে। একাধিক এরর হ্যান্ডল করে।
    """
    try:
        # টাইপ চেক
        shares = int(shares)
        price = float(price)
        
        # নেগেটিভ ভ্যালু চেক
        if shares < 0 or price < 0:
            raise ValueError("শেয়ার বা মূল্য নেগেটিভ হতে পারে না!")
        
        total = shares * price
        print(f"  ✅ {ticker}: {shares} শেয়ার × ${price:.2f} = ${total:,.2f}")
        return total
    
    except ValueError as e:
        print(f"  ❌ ভ্যালু এরর ({ticker}): {e}")
        return None
    except TypeError as e:
        print(f"  ❌ টাইপ এরর ({ticker}): {e}")
        return None
    except Exception as e:
        print(f"  ❌ অজানা এরর ({ticker}): {e}")
        return None

# টেস্ট বিভিন্ন ইনপুট দিয়ে
print("স্টক ভ্যালু ক্যালকুলেশন:")
calculate_stock_value("AAPL", "100", "150.25")     # ✅ কাজ করবে (স্ট্রিং থেকেও)
calculate_stock_value("MSFT", 50, 380.50)           # ✅ কাজ করবে
calculate_stock_value("TSLA", -10, 245.60)          # ❌ নেগেটিভ শেয়ার
calculate_stock_value("GOOGL", "abc", 140.80)       # ❌ ভুল শেয়ার সংখ্যা
calculate_stock_value("AMZN", 30, None)             # ❌ None ভ্যালু
print()


# ============================================================
# ৫. else এবং finally ব্লক
# ============================================================

print("=== else এবং finally ব্লক ===")

def process_payment(amount, balance):
    """
    পেমেন্ট প্রসেস করে। else এবং finally ব্লক ব্যবহার করে।
    """
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("পেমেন্ট অ্যামাউন্ট পজিটিভ হতে হবে")
        
        if amount > balance:
            raise ValueError("অপর্যাপ্ত ব্যালেন্স!")
        
    except ValueError as e:
        print(f"  ❌ ভ্যালিডেশন এরর: {e}")
        return False
    
    except Exception as e:
        print(f"  ❌ অপ্রত্যাশিত এরর: {e}")
        return False
    
    else:
        # কোনো এরর না হলে এই ব্লক রান করে
        new_balance = balance - amount
        print(f"  ✅ পেমেন্ট সফল! বাকি ব্যালেন্স: ${new_balance:,.2f}")
        return True
    
    finally:
        # এই ব্লক সবসময় রান করে (এরর থাকুক বা না থাকুক)
        print(f"  📋 লেনদেন সম্পন্ন হয়েছে - বর্তমান ব্যালেন্স: ${balance:,.2f}")

# টেস্ট
print("পেমেন্ট প্রসেসিং:")
process_payment(500, 1000)     # ✅ সফল
print()
process_payment(-50, 1000)     # ❌ নেগেটিভ অ্যামাউন্ট
print()
process_payment(1500, 1000)    # ❌ অপর্যাপ্ত ব্যালেন্স
print()


# ============================================================
# ৬. ফাইল অপারেশনে এরর হ্যান্ডলিং
# ============================================================

print("=== ফাইল অপারেশনে এরর হ্যান্ডলিং ===")

import os

def read_financial_report(file_path):
    """
    ফাইন্যান্সিয়াল রিপোর্ট ফাইল রিড করে। সব ধরনের এরর হ্যান্ডল করে।
    """
    print(f"📂 ফাইল পড়ার চেষ্টা: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
            
    except FileNotFoundError:
        print(f"  ❌ ফাইল পাওয়া যায়নি: {file_path}")
        print(f"  💡 টিপ: সঠিক ফাইল পাথ চেক করুন")
        return None
    
    except PermissionError:
        print(f"  ❌ ফাইল পড়ার অনুমতি নেই!")
        return None
    
    except UnicodeDecodeError:
        print(f"  ❌ ফাইলের এনকোডিং সঠিক নয়। UTF-8 চেক করুন")
        return None
    
    except Exception as e:
        print(f"  ❌ অজানা এরর: {type(e).__name__} - {e}")
        return None
    
    else:
        print(f"  ✅ ফাইল সফলভাবে পড়া হয়েছে ({len(data)} ক্যারেক্টার)")
        return data
    
    finally:
        print(f"  📋 ফাইল অপারেশন শেষ")

# বিদ্যমান ফাইল দিয়ে টেস্ট
valid_file = os.path.expanduser("~/LearningPath/Python/week01_basics/expenses.txt")
read_financial_report(valid_file)
print()

# নেই এমন ফাইল দিয়ে টেস্ট
read_financial_report("nonexistent_report.txt")
print()


# ============================================================
# ৭. raise - নিজে এরর তৈরি করা
# ============================================================

print("=== raise দিয়ে নিজে এরর তৈরি ===")

def validate_stock_price(price):
    """
    স্টক প্রাইস ভ্যালিডেট করে। প্রয়োজন হলে নিজে এরর raise করে।
    """
    if price is None:
        raise ValueError("❌ স্টক প্রাইস None হতে পারে না!")
    
    if not isinstance(price, (int, float)):
        raise TypeError(f"❌ ভুল টাইপ: {type(price).__name__}, সংখ্যা প্রয়োজন")
    
    if price <= 0:
        raise ValueError(f"❌ প্রাইস {price} <= 0! পজিটিভ সংখ্যা প্রয়োজন")
    
    if price > 100000:
        raise ValueError(f"❌ প্রাইস {price} অনেক বেশি! রিয়েলিস্টিক প্রাইস দিন")
    
    return True

# ভ্যালিডেশন টেস্ট
test_prices = [150.25, -10, 0, "abc", None, 999999]

for price in test_prices:
    try:
        validate_stock_price(price)
        print(f"  ✅ ${price} - বৈধ প্রাইস")
    except (ValueError, TypeError) as e:
        print(f"  {e}")

print()


# ============================================================
# ৮. কাস্টম এক্সেপশন (Custom Exceptions)
# ============================================================

print("=== কাস্টম এক্সেপশন ===")

# নিজের এরর ক্লাস তৈরি
class InsufficientFundsError(Exception):
    """ব্যালেন্স অপর্যাপ্ত হলে এই এরর হয়"""
    pass

class InvalidTransactionError(Exception):
    """অবৈধ লেনদেন হলে এই এরর হয়"""
    pass

class MarketClosedError(Exception):
    """মার্কেট বন্ধ থাকলে এই এরর হয়"""
    pass


def place_trade(ticker, shares, price, balance, market_open=True):
    """
    ট্রেড প্লেস করার ফাংশন - কাস্টম এক্সেপশন ব্যবহার করে।
    """
    try:
        # মার্কেট চেক
        if not market_open:
            raise MarketClosedError("মার্কেট এখন বন্ধ! শুধু ৯:৩০ এএম - ৪:০০ পিএম ET")
        
        # ভ্যালিডেশন
        if shares <= 0:
            raise InvalidTransactionError("শেয়ার সংখ্যা পজিটিভ হতে হবে!")
        
        if price <= 0:
            raise InvalidTransactionError("স্টক প্রাইস পজিটিভ হতে হবে!")
        
        total_cost = shares * price
        
        # ব্যালেন্স চেক
        if total_cost > balance:
            raise InsufficientFundsError(
                f"অপর্যাপ্ত ব্যালেন্স! প্রয়োজন: ${total_cost:,.2f}, "
                f"আছে: ${balance:,.2f}"
            )
        
        # সফল ট্রেড
        new_balance = balance - total_cost
        print(f"  ✅ ট্রেড সফল! {shares} {ticker} @ ${price:.2f} = ${total_cost:,.2f}")
        print(f"  💰 নতুন ব্যালেন্স: ${new_balance:,.2f}")
        return new_balance
    
    except MarketClosedError as e:
        print(f"  🔒 মার্কেট ক্লোজড: {e}")
        return balance
    
    except InvalidTransactionError as e:
        print(f"  ⚠️ অবৈধ ট্রানজেকশন: {e}")
        return balance
    
    except InsufficientFundsError as e:
        print(f"  💳 ফান্ড অপ্রতুল: {e}")
        return balance
    
    except Exception as e:
        print(f"  ❌ অপ্রত্যাশিত এরর: {e}")
        return balance

# টেস্ট
print("ট্রেডিং সিমুলেশন:")
print("-" * 50)

# টেস্ট ১: সফল ট্রেড
print("\n📌 টেস্ট ১: সফল ট্রেড")
place_trade("AAPL", 10, 150.25, 5000)

# টেস্ট ২: অপর্যাপ্ত ব্যালেন্স
print("\n📌 টেস্ট ২: অপর্যাপ্ত ব্যালেন্স")
place_trade("TSLA", 50, 245.60, 2000)

# টেস্ট ৩: মার্কেট বন্ধ
print("\n📌 টেস্ট ৩: মার্কেট বন্ধ")
place_trade("MSFT", 5, 380.50, 5000, market_open=False)

# টেস্ট ৪: অবৈধ ট্রানজেকশন
print("\n📌 টেস্ট ৪: অবৈধ শেয়ার সংখ্যা")
place_trade("GOOGL", -5, 140.80, 5000)
print()


# ============================================================
# ৯. প্র্যাকটিক্যাল উদাহরণ: স্টক প্রাইস ক্যালকুলেটর
# ============================================================

print("=== স্টক প্রাইস ক্যালকুলেটর (সম্পূর্ণ এরর হ্যান্ডলিং সহ) ===")

def get_stock_input():
    """
    ব্যবহারকারীর কাছ থেকে স্টক ইনপুট নেয় এবং ভ্যালিডেট করে।
    """
    while True:
        try:
            ticker = input("স্টক টিকার লিখুন (যেমন: AAPL): ").strip().upper()
            if not ticker:
                raise ValueError("টিকার খালি হতে পারে না!")
            if not ticker.isalpha():
                raise ValueError("টিকারে শুধু অক্ষর থাকতে পারে!")
            
            shares = input("শেয়ার সংখ্যা: ").strip()
            if not shares:
                raise ValueError("শেয়ার সংখ্যা প্রয়োজন!")
            shares = int(shares)
            if shares <= 0:
                raise ValueError("শেয়ার সংখ্যা পজিটিভ হতে হবে!")
            
            price = input("শেয়ার প্রতি মূল্য ($): ").strip()
            if not price:
                raise ValueError("মূল্য প্রয়োজন!")
            price = float(price)
            if price <= 0:
                raise ValueError("মূল্য পজিটিভ হতে হবে!")
            
            total = shares * price
            print(f"\n✅ {ticker}: {shares} শেয়ার × ${price:.2f} = ${total:,.2f}")
            return total
        
        except ValueError as e:
            print(f"❌ ইনপুট এরর: {e}")
            print("পুনরায় চেষ্টা করুন...\n")
            continue
        except KeyboardInterrupt:
            print("\n\nপ্রোগ্রাম বন্ধ করা হয়েছে।")
            return None
        except Exception as e:
            print(f"❌ অপ্রত্যাশিত এরর: {e}")
            return None


# স্টক ইনপুট নেওয়া (ইউজার ইন্টারঅ্যাকশন দেখানোর জন্য প্রিন্ট ম্যাসেজ রাখা হয়েছে,
# আসলে এটি রিয়েল ইনপুট নেবে। টেস্টিংয়ের জন্য কমেন্টেড রাখলাম।)
print("📝 নিচে ইনপুট নেয়া হবে। টেস্টিং এর জন্য আমরা হার্ডকোডেড ভ্যালু ব্যবহার করছি।\n" + "# "*20)
print("রান করার পর ইন্টারঅ্যাক্টিভली ইনপুট দিতে পারবেন। আপাতত ম্যানুয়াল টেস্টগুলো দেখুন:")
print()

# ম্যানুয়াল টেস্ট (ইন্টারঅ্যাকটিভ না চালিয়ে)
def manual_stock_calc(ticker, shares_str, price_str):
    """
    ম্যানুয়াল স্টক ক্যালকুলেশন - এরর হ্যান্ডলিং সহ।
    """
    try:
        shares = int(shares_str)
        price = float(price_str)
        
        if shares <= 0:
            return "❌ শেয়ার সংখ্যা পজিটিভ হতে হবে!"
        if price <= 0:
            return "❌ মূল্য পজিটিভ হতে হবে!"
        
        total = shares * price
        return f"✅ {ticker}: {shares} শেয়ার × ${price:.2f} = ${total:,.2f}"
    
    except ValueError:
        return "❌ সংখ্যায় কনভার্ট করা যায়নি! ভ্যালিড সংখ্যা দিন"
    except Exception as e:
        return f"❌ এরর: {e}"

# টেস্ট কেস
test_cases = [
    ("AAPL", "100", "150.25"),
    ("MSFT", "fifty", "380.50"),
    ("TSLA", "10", "-50"),
    ("GOOGL", "25", "140.80"),
]

for t, s, p in test_cases:
    print(f"  ইনপুট: {t}, {s}, {p}")
    print(f"  রেজাল্ট: {manual_stock_calc(t, s, p)}\n")
print()


# ============================================================
# ১০. with try/except ব্যবহার করে রিসোর্স ম্যানেজমেন্ট
# ============================================================

print("=== রিসোর্স ম্যানেজমেন্ট ===")

def backup_portfolio(source_path, backup_path):
    """
    পোর্টফোলিও ফাইল ব্যাকআপ করে। ট্রাই/এক্সসেপ্ট সহ।
    """
    try:
        # সোর্স ফাইল চেক
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"সোর্স ফাইল নেই: {source_path}")
        
        # ডেস্টিনেশন ডিরেক্টরি চেক
        backup_dir = os.path.dirname(backup_path)
        if backup_dir and not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print(f"  📁 ব্যাকআপ ডিরেক্টরি তৈরি: {backup_dir}")
        
        # ফাইল কপি
        with open(source_path, "r", encoding="utf-8") as src:
            data = src.read()
        
        with open(backup_path, "w", encoding="utf-8") as dst:
            dst.write(data)
        
        print(f"  ✅ ব্যাকআপ সফল!")
        print(f"  📂 সোর্স: {os.path.getsize(source_path):,} bytes")
        print(f"  📂 ব্যাকআপ: {os.path.getsize(backup_path):,} bytes")
        return True
    
    except FileNotFoundError as e:
        print(f"  ❌ {e}")
        return False
    except PermissionError:
        print(f"  ❌ ফাইল পড়া/লেখার অনুমতি নেই!")
        return False
    except Exception as e:
        print(f"  ❌ ব্যাকআপ ব্যর্থ: {type(e).__name__}: {e}")
        return False
    finally:
        print(f"  📋 ব্যাকআপ অপারেশন শেষ")

# টেস্ট
source = os.path.expanduser("~/LearningPath/Python/week01_basics/portfolio_summary.txt")
backup = os.path.expanduser("~/LearningPath/Python/week01_basics/backups/portfolio_backup.txt")

print("পোর্টফোলিও ব্যাকআপ:")
backup_portfolio(source, backup)
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================

print("=" * 60)
print("📝 প্র্যাকটিস টাস্ক - নিজে করুন!")
print("=" * 60)

print("""
টাস্ক ১: ব্যাংক অ্যাকাউন্ট ক্লাস (এরর হ্যান্ডলিং সহ)
    একটি ব্যাংক অ্যাকাউন্ট ক্লাস তৈরি করুন যেখানে:
    - deposit() - টাকা জমা (নেগেটিভ হলে এরর)
    - withdraw() - টাকা তোলা (অপর্যাপ্ত ব্যালেন্স হলে এরর)
    - transfer() - অন্য অ্যাকাউন্টে টাকা স্থানান্তর
    সব অপারেশনে try/except ব্যবহার করুন।

টাস্ক ২: ডেটা ইম্পোর্টার (মাল্টি-এরর হ্যান্ডলিং)
    একটি ফাংশন তৈরি করুন যা CSV ফাইল ইম্পোর্ট করে:
    - ফাইল না থাকলে FileNotFoundError হ্যান্ডল
    - ডেটা ফরম্যাট ভুল হলে ValueError হ্যান্ডল
    - খালি ফাইল হলে কাস্টম EmptyFileError

টাস্ক ৩: ক্যালকুলেটর (ইউজার ইনপুট এরর)
    একটি ফাইন্যান্সিয়াল ক্যালকুলেটর তৈরি করুন যা ইউজারের
    ইনপুট নেয় এবং সব ধরনের ইনপুট এরর হ্যান্ডল করে।
    ব্যবহারকারী 'quit' লিখলে প্রোগ্রাম বন্ধ হবে।

টাস্ক ৪: API রেট লিমিটার (কাস্টম এক্সেপশন)
    একটি কাস্টম RateLimitError তৈরি করুন এবং একটি ফাংশন লিখুন
    যা প্রতি মিনিটে সর্বোচ্চ ৫ বার কল করা যাবে। তার বেশি হলে
    এরর throw করবে।
""")

print("--- ইঙ্গিত (Hints) ---")
print("""
# টাস্ক ১ এর জন্য ইঙ্গিত:
class InsufficientBalanceError(Exception):
    pass

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def withdraw(self, amount):
        try:
            if amount <= 0:
                raise ValueError("পজিটিভ অ্যামাউন্ট দিন")
            if amount > self.balance:
                raise InsufficientBalanceError(f"${self.balance:.2f} আছে, ${amount:.2f} চেয়েছেন")
            self.balance -= amount
            return self.balance
        except (ValueError, InsufficientBalanceError) as e:
            print(f"❌ {e}")
            return None

# টাস্ক ৪ এর জন্য ইঙ্গিত:
class RateLimitError(Exception):
    pass

class APIRateLimiter:
    def __init__(self, max_calls=5, period=60):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def call(self, func):
        from time import time
        now = time()
        self.calls = [c for c in self.calls if now - c < self.period]
        if len(self.calls) >= self.max_calls:
            raise RateLimitError("লিমিট অতিক্রম! অপেক্ষা করুন")
        self.calls.append(now)
        return func()
""")