"""
============================================
📚 DAY 2 — Input & Conditions (ইনপুট ও শর্ত)
============================================
গতকাল variable-এ data জমা রাখা শিখেছো। আজ শিখবে:
1. input() — ইউজারের কাছ থেকে data নেওয়া
2. if/elif/else — শর্ত দিয়ে decision making

Finance-এ এটা কাজে লাগে: budget check, loan eligibility, tax bracket ইত্যাদি।

Run command: python "C:/Users/Md Jahirul Islam/LearningPath/Python/week01_basics/day02_conditions.py"
============================================
"""

print("=" * 50)
print("🐍 DAY 2: INPUT & CONDITIONS")
print("=" * 50)

# ===== 1. INPUT (ইউজার থেকে ডাটা নেওয়া) =====
# input() সবসময় STRING return করে — math করতে হলে convert করতে হবে

name = input("তোমার নাম কী? ")
print(f"স্বাগতম, {name}!\n")

# ===== 2. TYPE CONVERSION (টাইপ কনভার্শন) =====
# int(), float(), str() দিয়ে convert করা যায়

age_str = input("তোমার বয়স কত? ")
age = int(age_str)          # string → integer
print(f"৫ বছর পরে বয়স হবে: {age + 5}\n")

income_str = input("তোমার মাসিক আয় কত (CAD)? ")
income = float(income_str)   # string → float
print(f"বাৎসরিক আয়: ${income * 12:,.2f}\n")

# ===== 3. IF/ELIF/ELSE (শর্ত) =====
# Python-এ if condition: দিয়ে block শুরু, indentation (4 space/tab) জরুরি

score = int(input("তোমার পরীক্ষার নাম্বার (0-100)? "))

if score >= 80:
    print("🎉 A+ — দারুণ করেছো!")
elif score >= 70:
    print("👍 A — ভালো!")
elif score >= 60:
    print("📚 B — আরেকটু উন্নতি দরকার")
elif score >= 50:
    print("😐 C — pass করেছো")
else:
    print("💪 F — হাল ছাড়বে না, আবার চেষ্টা করো")

# ===== 4. COMPARISON OPERATORS =====
# ==  (সমান কিনা)
# !=  (সমান না)
# >   (বড়)
# <   (ছোট)
# >=  (বড় বা সমান)
# <=  (ছোট বা সমান)

print("\n--- Comparison Demo ---")
a, b = 10, 20
print(f"{a} == {b} : {a == b}")
print(f"{a} != {b} : {a != b}")
print(f"{a} <  {b} : {a < b}")
print(f"{a} >  {b} : {a > b}")

# ===== 5. LOGICAL OPERATORS (and, or, not) =====
# একাধিক শর্ত check করার জন্য

has_job = True
has_degree = True
has_experience = False

print("\n--- Logical Operators ---")
print(f"চাকরি আছে AND ডিগ্রি আছে: {has_job and has_degree}")       # দুটোই True → True
print(f"চাকরি আছে OR অভিজ্ঞতা আছে: {has_job or has_experience}")   # একটা True → True
print(f"অভিজ্ঞতা নেই (NOT): {not has_experience}")                 # উল্টা

# ===== 6. REAL EXAMPLE: LOAN ELIGIBILITY =====
# টাকার হিসাব — finance-এর জন্য perfect practice

print("\n--- 🏦 Loan Eligibility Checker ---")
salary = float(input("মাসিক বেতন (CAD): "))
credit_score = int(input("ক্রেডিট স্কোর (300-900): "))
existing_loan = float(input("বর্তমান লোনের মাসিক কিস্তি (CAD): "))

debt_to_income = existing_loan / salary  # DTI ratio

if salary >= 3000 and credit_score >= 650 and debt_to_income < 0.40:
    print("✅ লোন APPROVED — তুমি eligible!")
elif salary < 3000:
    print("❌ REJECTED — মাসিক আয় $3000-এর কম")
elif credit_score < 650:
    print("❌ REJECTED — ক্রেডিট স্কোর 650-এর নিচে")
else:
    print("❌ REJECTED — DTI ratio অনেক বেশি (40%+)")


print(f"\nতোমার Debt-to-Income ratio: {debt_to_income:.2%}")

# ===== 7. TAX BRACKET CALCULATOR =====
# Progressive tax system — Canada-র মতো

print("\n--- 🧾 Tax Bracket Calculator ---")
income = float(input("বাৎসরিক আয় (CAD): "))

if income <= 53359:
    tax_rate = 0.15
elif income <= 106717:
    tax_rate = 0.205
elif income <= 165430:
    tax_rate = 0.26
elif income <= 235675:
    tax_rate = 0.29
else:
    tax_rate = 0.33

tax = income * tax_rate
net = income - tax
print(f"ট্যাক্স রেট: {tax_rate:.1%}")
print(f"মোট ট্যাক্স: ${tax:,.2f}")
print(f"হাতে থাকবে: ${net:,.2f}")

"""
============================================
🏋️ PRACTICE (অনুশীলন)
============================================

TASK 1: Savings Goal Checker
   - input নাও: monthly_income, monthly_expense, monthly_savings_goal
   - check করো: savings (income - expense) তোমার goal-এর চেয়ে বেশি কিনা
   - বেশি হলে "🎉 Goal achieved", কম হলে কত shortage সেটা দেখাও

TASK 2: Emergency Fund Calculator
   - input নাও: monthly_expense
   - emergency fund = 6 × monthly_expense
   - check করো: fund $10,000-এর বেশি কিনা, $5,000-$10,000, নাকি $5,000-এর নিচে
   - প্রতিটা case-এ advice দাও (e.g. "ভালো buffer", "আরও জমাও")

TASK 3: Investment Risk Profile
   - input নাও: age, monthly_savings
   - risk = age < 30 and monthly_savings > 500 → "High Risk OK"
   - age 30-50 → "Medium Risk"
   - age > 50 → "Low Risk / Safe Investments"
   - প্রিন্ট করো risk profile + explanation

============================================
PROGRESS.md-তে Day 2 টিক দাও ✅
============================================
"""
