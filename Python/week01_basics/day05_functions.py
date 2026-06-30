"""
Day 5: ফাংশন (Functions) এবং স্কোপ (Scope)
=============================================
লেখক: জাহিরুল ইসলাম
বিষয়: ফাইন্যান্স ও ডেটা অ্যানালাইসিসের জন্য পাইথন ফাংশন

তুমি কি জানো? ফাংশন হলো রি-ইউজেবল কোডের ব্লক। ফাইন্যান্সে আমরা বারবার
ট্যাক্স ক্যালকুলেশন, সুদের হার হিসাব, এবং ডেটা প্রসেসিং-এর জন্য ফাংশন ব্যবহার করি।
"""

# ============================================================
# ১. ফাংশন ডিফাইন এবং কল করা (Defining and Calling Functions)
# ============================================================

# ফাংশন ডিফাইন করা: def কীওয়ার্ড দিয়ে শুরু
def greet_investor():
    """
    একটি সাধারণ ফাংশন যা বিনিয়োগকারীকে স্বাগতম জানায়।
    """
    print("=" * 50)
    print("স্বাগতম! বিনিয়োগ বিশ্লেষণ টুলে আপনাকে স্বাগত।")
    print("=" * 50)

# ফাংশন কল করা
greet_investor()
print()  # খালি লাইন


# ============================================================
# ২. প্যারামিটার এবং আর্গুমেন্ট (Parameters & Arguments)
# ============================================================

# প্যারামিটার সহ ফাংশন - ট্যাক্স ক্যালকুলেটর
def calculate_tax(income, tax_rate=0.25):
    """
    আয় এবং ট্যাক্স রেট এর ভিত্তিতে ট্যাক্স গণনা করে।
    
    প্যারামিটার:
        income (float): বার্ষিক আয়
        tax_rate (float): ট্যাক্সের হার (ডিফল্ট: 25%)
    
    রিটার্ন:
        float: মোট ট্যাক্সের পরিমাণ
    """
    tax_amount = income * tax_rate
    return tax_amount

# ফাংশন কল করা বিভিন্ন আর্গুমেন্ট সহ
income_1 = 75000  # $75,000 বার্ষিক আয়
tax_1 = calculate_tax(income_1)  # ডিফল্ট ট্যাক্স রেট ব্যবহার
print(f"আয়: ${income_1:,.2f}")
print(f"ট্যাক্স (ডিফল্ট 25%): ${tax_1:,.2f}")

income_2 = 120000
tax_2 = calculate_tax(income_2, tax_rate=0.30)  # কাস্টম ট্যাক্স রেট
print(f"আয়: ${income_2:,.2f}")
print(f"ট্যাক্স (30%): ${tax_2:,.2f}")
print()


# ============================================================
# ৩. রিটার্ন ভ্যালু (Return Values)
# ============================================================

# চক্রবৃদ্ধি সুদ (Compound Interest) ক্যালকুলেটর
def compound_interest(principal, rate, time, n=12):
    """
    চক্রবৃদ্ধি সুদের পরিমাণ গণনা করে।
    
    A = P(1 + r/n)^(nt)
    
    প্যারামিটার:
        principal (float): মূলধন/আসল
        rate (float): বার্ষিক সুদের হার (যেমন: 0.05 = 5%)
        time (float): সময় (বছর)
        n (int): বার্ষিক চক্রবৃদ্ধির সংখ্যা (ডিফল্ট: 12 = মাসিক)
    
    রিটার্ন:
        tuple: (total_amount, interest_earned)
    """
    amount = principal * (1 + rate / n) ** (n * time)
    interest = amount - principal
    return amount, interest  # একাধিক মান রিটার্ন

# উদাহরণ: $10,000 বিনিয়োগ, 8% বার্ষিক সুদ, 5 বছর, মাসিক চক্রবৃদ্ধি
principal = 10000
annual_rate = 0.08
years = 5

total, earned = compound_interest(principal, annual_rate, years)
print("=== চক্রবৃদ্ধি সুদ ক্যালকুলেটর ===")
print(f"মূলধন: ${principal:,.2f}")
print(f"সুদের হার: {annual_rate*100:.1f}%")
print(f"সময়: {years} বছর")
print(f"মোট পরিমাণ: ${total:,.2f}")
print(f"সুদ আয়: ${earned:,.2f}")
print()


# ============================================================
# ৪. ডিফল্ট প্যারামিটার এবং কীওয়ার্ড আর্গুমেন্ট
# ============================================================

def investment_balance(initial, monthly_contribution, annual_return, years, 
                       compound_per_year=12):
    """
    নিয়মিত মাসিক জমা সহ বিনিয়োগের ভবিষ্যৎ মূল্য গণনা করে।
    """
    total = initial
    monthly_rate = annual_return / compound_per_year
    total_months = years * compound_per_year
    
    for month in range(1, total_months + 1):
        # প্রতি মাসে সুদ যোগ
        total = total * (1 + monthly_rate)
        # মাসিক জমা যোগ
        if month <= total_months:
            total += monthly_contribution
    
    total_contributed = initial + (monthly_contribution * total_months)
    earnings = total - total_contributed
    
    return total, total_contributed, earnings

# কল করা
final, contributed, earnings = investment_balance(
    initial=5000,
    monthly_contribution=500,
    annual_return=0.07,
    years=10
)
print("=== বিনিয়োগ ভবিষ্যৎ মূল্য ===")
print(f"প্রাথমিক বিনিয়োগ: $5,000")
print(f"মাসিক জমা: $500")
print(f"বার্ষিক রিটার্ন: 7%")
print(f"সময়: ১০ বছর")
print(f"মোট জমা: ${contributed:,.2f}")
print(f"সুদ/মুনাফা: ${earnings:,.2f}")
print(f"মোট ব্যালেন্স: ${final:,.2f}")
print()


# ============================================================
# ৫. স্কোপ (Scope) - লোকাল vs গ্লোবাল ভেরিয়েবল
# ============================================================

# গ্লোবাল ভেরিয়েবল
global_tax_rate = 0.25  # এটি পুরো প্রোগ্রাম জুড়ে доступно
company_name = "জাহিরুল ফাইন্যান্স কর্পোরেশন"

def calculate_net_income(gross_income, deductions=0):
    """
    নেট আয় গণনা করে। গ্লোবাল ট্যাক্স রেট ব্যবহার করে।
    """
    # লোকাল ভেরিয়েবল - শুধু এই ফাংশনের ভিতরে доступно
    taxable_income = gross_income - deductions
    tax_amount = taxable_income * global_tax_rate  # গ্লোবাল ভেরিয়েবল ব্যবহার
    net_income = taxable_income - tax_amount
    
    # লোকাল ভেরিয়েবল প্রিন্ট (শুধু ডিবাগিং এর জন্য)
    print(f"  [ফাংশনের ভিতরে] ট্যাক্সযোগ্য আয়: ${taxable_income:,.2f}")
    print(f"  [ফাংশনের ভিতরে] কর: ${tax_amount:,.2f}")
    
    return net_income

print(f"গ্লোবাল ট্যাক্স রেট: {global_tax_rate * 100}%")
print(f"কোম্পানি: {company_name}")

net = calculate_net_income(85000, deductions=5000)
print(f"নেট আয়: ${net:,.2f}")

# নিচের লাইনগুলো আনকমেন্ট করলে এরর হবে (লোকাল ভেরিয়েবল বাইরে доступно না)
# print(taxable_income)  # NameError: name 'taxable_income' is not defined
# print(tax_amount)      # NameError: name 'tax_amount' is not defined
print()


# ============================================================
# ৬. গ্লোবাল কীওয়ার্ড (Global Keyword)
# ============================================================

bonus_percentage = 0.05  # গ্লোবাল ভেরিয়েবল

def update_bonus(new_rate):
    """
    গ্লোবাল বোনাস রেট আপডেট করে।
    """
    global bonus_percentage  # গ্লোবাল ভেরিয়েবল পরিবর্তনের জন্য
    old_rate = bonus_percentage
    bonus_percentage = new_rate
    print(f"বোনাস রেট পরিবর্তন: {old_rate*100}% -> {new_rate*100}%")

print(f"বর্তমান বোনাস: {bonus_percentage*100}%")
update_bonus(0.08)
print(f"আপডেটেড বোনাস: {bonus_percentage*100}%")
print()


# ============================================================
# ৭. ল্যাম্বডা ফাংশন (Lambda / Anonymous Functions)
# ============================================================

# ল্যাম্বডা: ছোট, এক-লাইনের ফাংশন
# ফাইন্যান্সে দ্রুত গণনার জন্য ব্যবহার করা হয়

# সরল সুদ ক্যালকুলেটর (ল্যাম্বডা)
simple_interest = lambda p, r, t: p * r * t

# ডিসকাউন্ট ক্যালকুলেটর
discount_price = lambda price, discount: price * (1 - discount)

# উদাহরণ
loan = 50000
rate = 0.10
time = 3
interest = simple_interest(loan, rate, time)
print(f"সরল সুদ: ${interest:,.2f} (লোন: ${loan:,.2f}, রেট: {rate*100}%, সময়: {time}বছর)")

original_price = 1200
discount = 0.15
final_price = discount_price(original_price, discount)
print(f"ডিসকাউন্টের পর দাম: ${final_price:,.2f} (মূল্য: ${original_price}, ডিসকাউন্ট: {discount*100}%)")
print()


# ============================================================
# ৮. ডেটা অ্যানালাইসিসের জন্য ফাংশন
# ============================================================

# পোর্টফোলিও রিটার্ন গণনা
def calculate_portfolio_return(assets):
    """
    পোর্টফোলিওর ওয়েটেড এভারেজ রিটার্ন গণনা করে।
    
    প্যারামিটার:
        assets (list): প্রতিটি (asset_name, weight, return_rate) টাপল
    
    রিটার্ন:
        float: পোর্টফোলিও রিটার্ন (%)
    """
    portfolio_return = 0
    print("পোর্টফোলিও বিশ্লেষণ:")
    print("-" * 50)
    print(f"{'সম্পদ':<15} {'ওজন':<10} {'রিটার্ন':<10} {'কন্ট্রিবিউশন':<15}")
    print("-" * 50)
    
    for name, weight, ret in assets:
        contribution = weight * ret
        portfolio_return += contribution
        print(f"{name:<15} {weight*100:<9.1f}% {ret*100:<9.2f}% {contribution*100:<13.2f}%")
    
    print("-" * 50)
    print(f"পোর্টফোলিও রিটার্ন: {portfolio_return*100:.2f}%")
    return portfolio_return

# পোর্টফোলিও ডেটা
my_portfolio = [
    ("স্টক (Stock)", 0.50, 0.12),     # 50% ওজন, 12% রিটার্ন
    ("বন্ড (Bond)", 0.30, 0.05),       # 30% ওজন, 5% রিটার্ন
    ("গোল্ড (Gold)", 0.10, 0.08),      # 10% ওজন, 8% রিটার্ন
    ("ক্রিপ্টো (Crypto)", 0.10, 0.25)  # 10% ওজন, 25% রিটার্ন
]

port_return = calculate_portfolio_return(my_portfolio)
print()


# শার্প রেশিও (Sharpe Ratio) ক্যালকুলেটর
def sharpe_ratio(portfolio_return, risk_free_rate, std_dev):
    """
    শার্প রেশিও গণনা করে - রিস্ক-অ্যাডজাস্টেড রিটার্ন।
    
    Sharpe = (Portfolio Return - Risk Free Rate) / Standard Deviation
    """
    excess_return = portfolio_return - risk_free_rate
    sharpe = excess_return / std_dev
    return sharpe

risk_free = 0.04  # 4% রিস্ক-ফ্রি রেট (যেমন: ট্রেজারি বন্ড)
portfolio_std = 0.15  # 15% স্ট্যান্ডার্ড ডেভিয়েশন

sharpe = sharpe_ratio(port_return, risk_free, portfolio_std)
print(f"শার্প রেশিও: {sharpe:.4f}")
if sharpe > 1:
    print("✅ ভালো রিস্ক-অ্যাডজাস্টেড রিটার্ন!")
elif sharpe > 0:
    print("⚠️ গড় রিটার্ন, উন্নতি সম্ভব")
else:
    print("❌ রিস্ক-ফ্রি রেটের থেকেও কম রিটার্ন")
print()


# ============================================================
# ৯. ডকস্ট্রিং (Docstrings) - ফাংশনের ডকুমেন্টেশন
# ============================================================

def calculate_dividend_yield(annual_dividend, stock_price):
    """
    ডিভিডেন্ড ইল্ড (Dividend Yield) গণনা করে।
    
    Dividend Yield = বার্ষিক ডিভিডেন্ড / স্টক মূল্য
    
    প্যারামিটার:
        annual_dividend (float): শেয়ার প্রতি বার্ষিক ডিভিডেন্ড ($)
        stock_price (float): বর্তমান শেয়ার মূল্য ($)
    
    রিটার্ন:
        float: ডিভিডেন্ড ইল্ড (%)
    
    উদাহরণ:
        >>> calculate_dividend_yield(3.50, 140.00)
        0.025  # 2.5%
    """
    if stock_price <= 0:
        return 0.0
    yield_pct = annual_dividend / stock_price
    return yield_pct

# ডকস্ট্রিং দেখা (হেল্প ফাংশন)
help(calculate_dividend_yield)
print()

# ব্যবহার
div_yield = calculate_dividend_yield(3.50, 140.00)
print(f"ডিভিডেন্ড ইল্ড: {div_yield*100:.2f}%")
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================

print("=" * 60)
print("📝 প্র্যাকটিস টাস্ক - নিজে করুন!")
print("=" * 60)

print("""
টাস্ক ১: ইনফ্লেশন অ্যাডজাস্টমেন্ট ফাংশন
    একটি ফাংশন তৈরি করুন যা একটি পরিমাণকে মুদ্রাস্ফীতি অনুযায়ী অ্যাডজাস্ট করে।
    ফাংশন: inflation_adjust(amount, inflation_rate, years)
    উদাহরণ: $1000, 6% ইনফ্লেশন, ৫ বছর -> ভবিষ্যৎ মূল্য কত?

টাস্ক ২: ইএমআই (EMI) ক্যালকুলেটর
    একটি ফাংশন তৈরি করুন যা লোনের মাসিক কিস্তি (EMI) গণনা করে।
    ফর্মুলা: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]
    যেখানে P = লোনের পরিমাণ, r = মাসিক সুদের হার, n = মাসের সংখ্যা

টাস্ক ৩: ডেটা ক্লিনিং ফাংশন
    একটি ফাংশন তৈরি করুন যা ফাইন্যান্সিয়াল ডেটার একটি তালিকা থেকে
    'N/A' বা None ভ্যালুগুলো সরিয়ে ফেলে এবং গড় রিটার্ন বের করে।

টাস্ক ৪: স্টক প্রাইস সিমুলেটর
    একটি ফাংশন তৈরি করুন যা প্রতিদিনের র্যান্ডম রিটার্নের ভিত্তিতে
    স্টকের ভবিষ্যৎ মূল্য সিমুলেট করে। (মন্টে কার্লো সিমুলেশন)
""")

# ============================================================
# সমাধানের ইঙ্গিত (Hints)
# ============================================================

print("--- ইঙ্গিত (Hints) ---")
print("""
# টাস্ক ১ এর জন্য ইঙ্গিত:
def inflation_adjust(amount, inflation_rate, years):
    future_value = amount * (1 + inflation_rate) ** years
    return future_value

# টাস্ক ২ এর জন্য ইঙ্গিত:
def emi_calculator(loan_amount, annual_rate, months):
    monthly_rate = annual_rate / 12
    emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
    return emi

# টাস্ক ৩ এর জন্য ইঙ্গিত:
def clean_financial_data(data_list):
    clean_data = [x for x in data_list if x is not None and x != 'N/A']
    return sum(clean_data) / len(clean_data) if clean_data else 0
""")