"""
============================================
📚 DAY 3 — Loops (লুপ — for, while, range)
============================================
লুপ মানে একই কাজ বারবার করা। ১০০টা জিনিস manually করার দরকার নেই —
loop এক লাইনেই করে ফেলবে।

Finance-এ লুপ লাগে: portfolio tracking, compound interest projection,
loan amortization table, monthly budget iteration ইত্যাদি।

Run command: python "C:/Users/Md Jahirul Islam/LearningPath/Python/week01_basics/day03_loops.py"
============================================
"""

print("=" * 50)
print("🐍 DAY 3: LOOPS (for, while, range)")
print("=" * 50)

# ===== 1. FOR LOOP (নির্দিষ্ট সংখ্যকবার চলবে) =====
# for item in collection:
#     do something

print("\n--- Basic for loop ---")
for i in range(5):        # 0, 1, 2, 3, 4 — total ৫ বার
    print(f"বার #{i+1}")

# ===== 2. RANGE() বিস্তারিত =====
# range(start, stop, step)
# start: শুরু (default 0)
# stop:  শেষ (এইটা inclusive না — অর্থাৎ stop-1 পর্যন্ত)
# step:  কত করে বাড়বে (default 1)

print("\n--- range(start, stop, step) ---")

print("range(5):      ", list(range(5)))        # [0, 1, 2, 3, 4]
print("range(1, 6):   ", list(range(1, 6)))     # [1, 2, 3, 4, 5]
print("range(1, 11, 2):", list(range(1, 11, 2))) # [1, 3, 5, 7, 9] — বিজোড় সংখ্যা
print("range(10, 0, -1):", list(range(10, 0, -1))) # [10, 9, 8, ..., 1] — উল্টা

# ===== 3. LOOP + CONDITION (লুপের ভিতরে if) =====
# জোড়/বিজোড় check করা

print("\n--- Even/Odd Check (1-10) ---")
for num in range(1, 11):
    if num % 2 == 0:
        print(f"  {num} → জোড় (EVEN)")
    else:
        print(f"  {num} → বিজোড় (ODD)")

# ===== 4. COMPOUND INTEREST PROJECTION (তোমার জন্য দরকারি!) =====
# প্রতি বছরের growth দেখাবে — finance interview-তে কাজে দেবে

print("\n--- 📈 10-Year Compound Interest Projection ---")
principal = 10000
rate = 0.08

print(f"Starting: ${principal:,} @ {rate*100}%")
print("-" * 30)

balance = principal
for year in range(1, 11):
    interest = balance * rate
    balance += interest  # same as: balance = balance + interest
    print(f"Year {year:2d}: ${balance:>10,.2f}  (interest: ${interest:,.2f})")

print(f"\nFinal: ${balance:,.2f}  (Profit: ${balance - principal:,.2f})")

# ===== 5. LOAN AMORTIZATION TABLE =====
# মাসিক কিস্তি কত, কত সুদ, কত principal — টেবিল আকারে

print("\n--- 🏦 Loan Amortization (First 12 Months) ---")
loan = 50000
annual_rate = 0.06
monthly_rate = annual_rate / 12
monthly_payment = 966.64  # fixed EMI

print(f"Loan: ${loan:,} | Rate: {annual_rate*100}% | EMI: ${monthly_payment}")
print(f"{'Month':<8}{'Interest':<12}{'Principal':<12}{'Balance':<12}")
print("-" * 44)

balance = loan
for month in range(1, 13):
    interest = balance * monthly_rate
    principal_paid = monthly_payment - interest
    balance -= principal_paid
    print(f"{month:<8}${interest:<11,.2f}${principal_paid:<11,.2f}${balance:<11,.2f}")

# ===== 6. WHILE LOOP =====
# while condition: — যতক্ষণ condition True, ততক্ষণ চলবে
# for loop-এর বিপরীতে while loop-এ আগে থেকে জানা লাগে না কতবার চলবে

print("\n--- ⏳ While Loop: Doubling Money ---")
money = 1
days = 0
target = 1000000

while money < target:
    money *= 2     # money = money * 2
    days += 1
    if days <= 10 or money >= target:  # first 10 and last print
        print(f"Day {days}: ${money:,}")

print(f"\n$1 doubled every day → ${money:,} in {days} days!")

# ===== 7. BREAK & CONTINUE =====
# break: loop থেকে বেরিয়ে যাও
# continue: বাকি অংশ skip করে পরের iteration-এ যাও

print("\n--- Break & Continue ---")
for i in range(1, 11):
    if i == 3:
        continue   # 3 skip
    if i == 8:
        break      # 8-এ থামো
    print(i, end=" ")
print("\n→ 3 skip হয়েছে, 8-এ থেমে গেছে")

# ===== 8. MONTHLY SAVINGS ACCUMULATOR =====
# Real-life: প্রতি মাসে কিছু save করলে বছরে কত হয়

print("\n--- 💰 Monthly Savings Tracker ---")
monthly_save = 500
rate = 0.05 / 12     # monthly interest rate

balance = 0
for month in range(1, 13):
    balance += monthly_save          # deposit
    balance *= (1 + rate)            # interest
    print(f"Month {month:2d}: ${balance:,.2f}")

print(f"\nYear-end balance with $500/month + 5% interest: ${balance:,.2f}")
print(f"Total deposited: ${monthly_save * 12:,}")
print(f"Interest earned: ${balance - monthly_save * 12:,.2f}")

"""
============================================
🏋️ PRACTICE (অনুশীলন)
============================================

TASK 1: Multiplication Table
   - for loop দিয়ে ৫-এর নামতা print করো (5 × 1 = 5 থেকে 5 × 10 = 50)
   - তারপর user-এর কাছ থেকে number input নিয়ে সেটার নামতা print করো

TASK 2: Retirement Calculator (তোমার $100B goal-এর warmup!)
   - principal = 10000, monthly_contribution = 500
   - annual_return = 10%
   - 20 বছর পর কত হবে? প্রতি বছরের balance দেখাও
   - formula: balance = balance * (1 + rate) + monthly * 12

TASK 3: FizzBuzz (popular interview question!)
   - 1 থেকে 50 পর্যন্ত loop
   - 3 দিয়ে বিভাজ্য → print "Fizz"
   - 5 দিয়ে বিভাজ্য → print "Buzz"
   - 3 এবং 5 দুটো দিয়েই বিভাজ্য → print "FizzBuzz"
   - কোনটাই না → number টাই print

TASK 4 (Challenge): Debt Payoff Calculator
   - debt = 20000, monthly_payment = 1000, interest_rate = 18% annually
   - while loop দিয়ে হিসাব করো: কত মাসে শোধ হবে?
   - প্রতি মাসের balance দেখাও (প্রথম ৬ মাস + শেষ ৩ মাস)

============================================
PROGRESS.md-তে Day 3 টিক দাও ✅
============================================
"""
