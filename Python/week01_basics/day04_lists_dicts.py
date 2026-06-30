"""
============================================
📚 DAY 4 — Python Lists & Dictionaries
============================================
Python-এর সবচেয়ে দরকারি ডাটা স্ট্রাকচার: List (তালিকা) আর Dictionary (অভিধান)।
এগুলো দিয়েই আপনি ডাটা organize করবেন Data Analyst হিসেবে।
============================================
"""

# ===== Section 1: List =====
# List = একাধিক আইটেম রাখার জন্য []
# ফাইন্যান্স উদাহরণ: আপনার মাসিক খরচের তালিকা

print("===== 📋 LIST BASICS =====")

# আমার মাসিক খরচের তালিকা
expenses = [1200, 350, 95, 55, 35]  # rent, grocery, electricity, transport, food
print("Monthly expenses:", expenses)

# List length
print("Total expense items:", len(expenses))

# Access by index (0 থেকে শুরু)
print("1st item (Rent):", expenses[0])
print("Last item (Food):", expenses[-1])

# Slicing — part of list
print("First 3 expenses:", expenses[0:3])
print("Last 2 expenses:", expenses[-2:])

# Add item
expenses.append(200)  # new expense: mobile bill
print("After adding mobile bill:", expenses)

# Remove item
expenses.remove(95)  # electricity bill paid and removed
print("After removing electricity:", expenses)

# Sum all expenses
total = sum(expenses)
print("Total monthly expenses: $", total)

# Loop through list
print("\n📌 Expense Breakdown:")
for i, e in enumerate(expenses):
    print(f"  Item {i+1}: ${e}")

# ===== Section 2: Dictionary =====
# Dictionary = key-value pair, ডাটাকে নাম দিয়ে存取 করা যায়

print("\n===== 📚 DICTIONARY BASICS =====")

# আপনার মাসিক আয়-খরচের বিশদ বিবরণ
my_finance = {
    "name": "Jahirul Islam",
    "income": 4000,
    "currency": "CAD",
    "expenses": {
        "rent": 1200,
        "grocery": 350,
        "transport": 55,
        "food": 35,
        "internet": 75,
        "phone": 50
    },
    "goal": "Data Analyst",
    "savings_target": 100000000000  # $100B dream!
}

print("Name:", my_finance["name"])
print("Income: $", my_finance["income"])

# Loop through dictionary
print("\n📌 Your Monthly Expenses:")
total_exp = 0
for category, amount in my_finance["expenses"].items():
    print(f"  {category}: ${amount}")
    total_exp += amount
print(f"  ─────────────────")
print(f"  Total: ${total_exp}")
print(f"  Remaining: ${my_finance['income'] - total_exp}")

# Check if key exists
if "savings" in my_finance:
    print("Savings target set!")
else:
    print("No savings key yet — adding now...")
    my_finance["savings"] = 500  # per month

print("Updated finance:", my_finance)

# ===== Section 3: List of Dictionaries =====
# Data Analyst-দের জন্য সবচেয়ে দরকারি প্যাটার্ন!
print("\n===== 📊 LIST OF DICTIONARIES =====")

# Portfolio: একাধিক স্টকের ডাটা
portfolio = [
    {"ticker": "AAPL", "name": "Apple Inc.", "shares": 10, "buy_price": 180.50},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "shares": 5, "buy_price": 140.20},
    {"ticker": "TSLA", "name": "Tesla Inc.", "shares": 8, "buy_price": 245.30},
    {"ticker": "MSFT", "name": "Microsoft Corp.", "shares": 12, "buy_price": 378.40}
]

print("📈 My Stock Portfolio:")
total_investment = 0
for stock in portfolio:
    value = stock["shares"] * stock["buy_price"]
    total_investment += value
    print(f"  {stock['ticker']} ({stock['name']}): {stock['shares']} shares × ${stock['buy_price']} = ${value:.2f}")

print(f"\n💰 Total Investment: ${total_investment:.2f}")

# Filter: যেসব স্টকে investment $2000+ 
print("\n🔍 Stocks with investment > $2000:")
for stock in portfolio:
    value = stock["shares"] * stock["buy_price"]
    if value > 2000:
        print(f"  ✅ {stock['ticker']}: ${value:.2f}")

"""
============================================
🏋️ PRACTICE - তোমার পালা!
============================================

TASK 1: নিজের মাসিক খরচের list বানাও। অন্তত ৫টি item যোগ করো।
        তারপর মোট খরচ বের করো।

TASK 2: তোমার পারসোনাল finance dictionary বানাও:
        - name, age, city, monthly_income, monthly_expenses (list)
        - তারপর income - total_expenses = savings বের করো

TASK 3: ৫টি স্টকের portfolio list বানাও। 
        প্রতিটি stock-এর জন্য: ticker, company, shares, buy_price
        তারপর দেখাও কোন স্টকগুলোতে $500+ investment করেছো।

TASK 4 (চ্যালেঞ্জ): 
        তোমার expenses dictionary থেকে সবচেয়ে বেশি খরচের ক্যাটাগরি বের করো।
============================================
"""

print("\n✅ Day 4 complete! Now try the Practice Tasks above ☝️")