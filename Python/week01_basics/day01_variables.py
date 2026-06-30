"""
============================================
📚 DAY 1 — Variables & Data Types (ভেরিয়েবল ও ডাটা টাইপ)
============================================
Python-এর একদম বেসিক। ভেরিয়েবল মানে একটা বাক্স যেখানে ডাটা রাখো।
ডাটা টাইপ মানে সেই ডাটার ধরন — সংখ্যা, টেক্সট, সত্য/মিথ্যা ইত্যাদি।

তোমার finance background কাজে লাগিয়ে real-life example দিয়ে শিখবো।
প্রতিটা code block রান করে দেখো — output কী আসে বুঝার চেষ্টা করো।

Run command: python "C:/Users/Md Jahirul Islam/LearningPath/Python/week01_basics/day01_variables.py"
============================================
"""

print("=" * 50)
print("🐍 DAY 1: VARIABLES & DATA TYPES")
print("=" * 50)

# ===== 1. VARIABLES (ভেরিয়েবল) =====
# ভেরিয়েবল = নাম দেওয়া জিনিস যেখানে value জমা রাখো
# Python-এ var বা let লাগে না — সরাসরি নাম লিখে = দিয়ে value বসাও

name = "Jahirul"           # string (টেক্সট) — সবসময় quotes-এর ভিতরে
age = 30                    # integer (পূর্ণ সংখ্যা) — কোন quotes লাগে না
monthly_income = 4000       # float-ও হতে পারে, কিন্তু এটা integer
hourly_rate = 22.50         # float (দশমিক সংখ্যা)
is_student = True           # boolean (সত্য/মিথ্যা) — True অথবা False

print("নাম:", name)
print("বয়স:", age)
print("মাসিক আয়: $", monthly_income)
print("ঘণ্টাপ্রতি রেট: $", hourly_rate)
print("স্টুডেন্ট?:", is_student)

# ===== 2. DATA TYPES চেক করা =====
# type() ফাংশন দিয়ে দেখো ভেরিয়েবলের type কী

print("\n--- Data Types ---")
print("name →", type(name))           # <class 'str'>
print("age →", type(age))             # <class 'int'>
print("hourly_rate →", type(hourly_rate))  # <class 'float'>
print("is_student →", type(is_student))    # <class 'bool'>

# ===== 3. STRING (স্ট্রিং — টেক্সট) =====
# ৩ ভাবে বানানো যায়: single quote, double quote, triple quote

city = 'Toronto'
country = "Canada"
bio = """Finance graduate,
refugee claimant,
learning Data Analytics."""

print("\n--- Strings ---")
print("থাকি:", city + ", " + country)  # + দিয়ে string জোড়া লাগানো যায়
print("\nBio:", bio)

# f-string — সবচেয়ে কাজের জিনিস। f দিয়ে string শুরু করলে {}-এর ভিতরে variable বসে
print(f"\nআমি {name}, বয়স {age} বছর। থাকি {city}, {country}-তে।")

# ===== 4. NUMBERS & MATH (গণিত) =====
# Finance-এর জন্য এইগুলো সবচেয়ে জরুরি

rent = 1200
food = 500
transport = 200
savings = monthly_income - rent - food - transport

print("\n--- Monthly Budget ---")
print(f"মাসিক আয়:       ${monthly_income}")
print(f"ভাড়া:           -${rent}")
print(f"খাবার:           -${food}")
print(f"যাতায়াত:        -${transport}")
print(f"জমা বাকি:        ${savings}")

# Math operators: + - * / // % **
print("\n--- Math Operators ---")
print("5 + 3  =", 5 + 3)    # যোগ
print("10 - 4 =", 10 - 4)   # বিয়োগ
print("6 * 7  =", 6 * 7)    # গুণ
print("15 / 4 =", 15 / 4)   # ভাগ (float result)
print("15 // 4 =", 15 // 4)  # integer ভাগ (দশমিক বাদ)
print("15 % 4 =", 15 % 4)   # modulus (ভাগশেষ)
print("2 ** 10 =", 2 ** 10)  # power (2^10)

# ===== 5. COMPOUND INTEREST (চক্রবৃদ্ধি সুদ) =====
# Finance-এর সবচেয়ে দরকারি formula — এখনই শিখে ফেলো

principal = 10000      # $10,000 বিনিয়োগ
rate = 0.08            # 8% বার্ষিক সুদ
years = 10             # ১০ বছর

# Future Value = P * (1 + r)^t
future_value = principal * (1 + rate) ** years
print(f"\n--- চক্রবৃদ্ধি সুদ ---")
print(f"${principal:,} বিনিয়োগ করলে {rate*100}% হারে {years} বছরে:")
print(f"Future Value = ${future_value:,.2f}")

"""
============================================
🏋️ PRACTICE (অনুশীলন)
============================================

TASK 1: নিজের একটা monthly budget বানাও
   - income, expense (3-4 category), leftover variable বানাও
   - f-string দিয়ে সুন্দর করে print করো

TASK 2: Compound interest calculator
   - principal = 5000, rate = 12%, years = 5, 10, 15-এর জন্য future value বের করো
   - উপরের formula ব্যবহার করো (P * (1+r)^t)

TASK 3: Currency conversion
   - CAD → USD rate = 0.73, CAD → BDT rate = 86.5
   - $4000 CAD-কে USD এবং BDT-তে convert করে print করো

============================================
কাজ শেষে PROGRESS.md-তে Day 1 টিক দিও ✅
আটকে গেলে ask করো। Happy coding! 🚀
============================================
"""
