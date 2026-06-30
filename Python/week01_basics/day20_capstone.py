#!/usr/bin/env python3
"""
Day 20: Capstone Review — সম্পূর্ণ রিভিউ ও ফাইনাল চ্যালেঞ্জ
================================================================
Day 1-19 থেকে সব গুরুত্বপূর্ণ টপিকের রিভিউ:
  1. ভেরিয়েবল, ডেটা টাইপ, অপারেটর
  2. কন্ডিশনাল স্টেটমেন্ট
  3. লুপ (for, while)
  4. লিস্ট, ডিকশনারি, টাপল, সেট
  5. ফাংশন ও মডিউল
  6. ফাইল হ্যান্ডলিং (CSV, JSON, TXT)
  7. API ও ওয়েব স্ক্র্যাপিং
  8. Pandas ও Matplotlib
  9. OOP (ক্লাস ও অবজেক্ট)
  10. এরর হ্যান্ডলিং

🏆 ফাইনাল চ্যালেঞ্জ: ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর

Finance Graduate (Canada) — Jahirul Islam
"""

import csv
import json
import logging
import math
import os
import random
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# পার্ট 1: ভেরিয়েবল, ডেটা টাইপ ও অপারেটর (Day 1-2 রিভিউ)
# ============================================================
print("=" * 70)
print("   পার্ট 1: ভেরিয়েবল, ডেটা টাইপ ও অপারেটর")
print("=" * 70)

def review_variables():
    """
    বেসিক ভেরিয়েবল, ডেটা টাইপ এবং অপারেটর রিভিউ।
    ফাইন্যান্স ডেটার উদাহরণ সহ।
    """
    print("\n[1.1] ভেরিয়েবল ও ডেটা টাইপ\n")

    # --- উদাহরণ 1: ফাইন্যান্স ডেটা ভেরিয়েবল ---
    stock_name = "Royal Bank of Canada"      # str
    ticker = "RY.TO"                         # str
    shares = 100                              # int
    buy_price = 145.50                        # float
    current_price = 162.30                    # float
    is_profitable = current_price > buy_price  # bool

    print(f"   স্টক: {stock_name} ({ticker})")
    print(f"   শেয়ার: {shares} (টাইপ: {type(shares).__name__})")
    print(f"   ক্রয় মূল্য: ${buy_price} (টাইপ: {type(buy_price).__name__})")
    print(f"   বর্তমান মূল্য: ${current_price}")
    print(f"   লাভজনক? {is_profitable} (টাইপ: {type(is_profitable).__name__})")

    # --- উদাহরণ 2: অ্যারিথমেটিক অপারেটর ---
    print(f"\n   [1.2] অ্যারিথমেটিক অপারেটর\n")
    cost_basis = shares * buy_price
    current_value = shares * current_price
    profit_loss = current_value - cost_basis
    return_pct = ((current_price - buy_price) / buy_price) * 100

    print(f"   মোট বিনিয়োগ:  {shares} × ${buy_price} = ${cost_basis:,.2f}")
    print(f"   বর্তমান মূল্য: {shares} × ${current_price} = ${current_value:,.2f}")
    print(f"   লাভ/ক্ষতি:     ${profit_loss:+,.2f}")
    print(f"   রিটার্ন:        {return_pct:+.2f}%")

    # --- এক্সারসাইজ ১ ---
    print(f"\n   ✏️  এক্সারসাইজ ১: নিজে করুন")
    print(f"       একটি ভেরিয়েবল 'dividend_yield' তৈরি করুন = 4.5 (float)")
    print(f"       অ্যানুয়াল ডিভিডেন্ড = current_price × dividend_yield / 100")
    print(f"       প্রিন্ট করুন 'বার্ষিক ডিভিডেন্ড: $X.XX'")


review_variables()

# ============================================================
# পার্ট 2: কন্ডিশনাল স্টেটমেন্ট (Day 3 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 2: কন্ডিশনাল স্টেটমেন্ট (if/elif/else)")
print("=" * 70)

def review_conditionals():
    """
    if/elif/else দিয়ে ফাইন্যান্স ডিসিশন মেকিং।
    """
    print("\n[2.1] if/elif/else ডেমো\n")

    # ইনভেস্টমেন্ট ডিসিশন
    stock_price = 85.50
    sma_50 = 82.00  # 50-দিনের মূভিং এভারেজ
    sma_200 = 78.00

    print(f"   স্টক প্রাইস: ${stock_price}")
    print(f"   50-day SMA: ${sma_50}")
    print(f"   200-day SMA: ${sma_200}")

    # গোল্ডেন ক্রস / ডেড ক্রস সিগন্যাল
    if stock_price > sma_50 and sma_50 > sma_200:
        signal = "🟢 বুলিশ (Golden Cross) — কিনতে পারেন!"
    elif stock_price < sma_50 and sma_50 < sma_200:
        signal = "🔴 বিয়ারিশ (Dead Cross) — সাবধান!"
    elif stock_price > sma_50:
        signal = "🟡 নিউট্রাল-বুলিশ — পর্যবেক্ষণ করুন"
    else:
        signal = "🟠 নিউট্রাল-বিয়ারিশ — অপেক্ষা করুন"

    print(f"   সিগন্যাল: {signal}")

    # --- এক্সারসাইজ ২ ---
    print(f"\n   ✏️  এক্সারসাইজ ২:")
    print(f"       P/E রেশিও ভেরিয়েবল = 15 (int)")
    print(f"       যদি P/E < 15: 'আন্ডারভ্যালুড'")
    print(f"       যদি P/E 15-25: 'ফেয়ার ভ্যালু'")
    print(f"       যদি P/E > 25: 'ওভারভ্যালুড'")


review_conditionals()

# ============================================================
# পার্ট 3: লুপ (Day 4-5 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 3: লুপ — for, while")
print("=" * 70)

def review_loops():
    """
    for এবং while লুপ দিয়ে ফাইন্যান্স ডেটা প্রসেসিং।
    """
    print("\n[3.1] for লুপ — স্টক প্রাইস লিস্ট\n")

    # সাপ্তাহিক স্টক প্রাইস
    weekly_prices = [145.20, 147.80, 146.50, 149.30, 152.10, 151.80, 153.40]

    print(f"   সাপ্তাহিক প্রাইস: {weekly_prices}")
    print()

    for i, price in enumerate(weekly_prices):
        day = i + 1
        bar = "█" * int(price / 3)
        print(f"   দিন {day}: ${price:<7.2f} {bar}")

    # --- while লুপ: কম্পাউন্ড ইন্টারেস্ট ক্যালকুলেশন ---
    print(f"\n   [3.2] while লুপ — কম্পাউন্ড ইন্টারেস্ট (চক্রবৃদ্ধি সুদ)\n")

    principal = 10000  # $10,000
    rate = 0.07        # 7% বার্ষিক
    target = 20000     # $20,000 টার্গেট
    years = 0
    amount = principal

    print(f"   প্রিন্সিপাল: ${principal:,}")
    print(f"   বার্ষিক সুদ: {rate*100}%")
    print(f"   টার্গেট: ${target:,}")
    print()

    while amount < target:
        amount *= (1 + rate)
        years += 1
        print(f"   বছর {years}: ${amount:,.2f}")

    print(f"\n   → ${principal:,} → ${target:,} হতে {years} বছর লেগেছে ({rate*100}% সুদে)")

    # --- এক্সারসাইজ ৩ ---
    print(f"\n   ✏️  এক্সারসাইজ ৩:")
    print(f"       মাসিক সেভিংস = $500, বার্ষিক রিটার্ন = 6%")
    print(f"       for লুপ দিয়ে ২৫ বছরের টোটাল বের করুন")
    print(f"       (প্রতি মাসে বিনিয়োগ + রিটার্ন যোগ হবে)")


review_loops()

# ============================================================
# পার্ট 4: লিস্ট, ডিকশনারি, টাপল, সেট (Day 6-8 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 4: ডেটা স্ট্রাকচার — লিস্ট, ডিকশনারি, টাপল, সেট")
print("=" * 70)

def review_data_structures():
    """
    Python ডেটা স্ট্রাকচার ফাইন্যান্স উদাহরণ সহ।
    """
    print("\n[4.1] লিস্ট — স্টক প্রাইসের তালিকা\n")

    prices = [142.30, 145.60, 143.80, 148.20, 150.10, 149.50, 152.80]
    print(f"   প্রাইস: {prices}")
    print(f"   সর্বোচ্চ: ${max(prices)}")
    print(f"   সর্বনিম্ন: ${min(prices)}")
    print(f"   গড়: ${sum(prices)/len(prices):.2f}")
    print(f"   সাজানো (উর্ধ্বক্রম): {sorted(prices)}")

    print(f"\n   [4.2] ডিকশনারি — স্টক ডেটা\n")

    stock_info = {
        "ticker": "RY.TO",
        "name": "Royal Bank of Canada",
        "sector": "Banking",
        "price": 162.45,
        "pe_ratio": 12.5,
        "dividend_yield": 4.2,
        "market_cap_b": 165.3,
    }

    for key, value in stock_info.items():
        print(f"   {key:20} → {value}")

    print(f"\n   [4.3] টাপল — (immutable ফাইন্যান্স ডেটা)\n")

    # টাপল: (টিকার, কোম্পানি, সেক্টর, প্রাইস)
    stock_tuple = ("RY.TO", "Royal Bank of Canada", "Banking", 162.45)
    ticker, name, sector, price = stock_tuple  # আনপ্যাকিং
    print(f"   স্টক টাপল: {stock_tuple}")
    print(f"   আনপ্যাকড: {ticker} — {name} ({sector}) @ ${price}")

    print(f"\n   [4.4] সেট — ইউনিক টিকার\n")

    portfolio_1 = {"RY.TO", "TD.TO", "BNS.TO", "CNQ.TO"}
    portfolio_2 = {"TD.TO", "RY.TO", "SHOP.TO", "ENB.TO"}

    print(f"   পোর্টফোলিও ১: {portfolio_1}")
    print(f"   পোর্টফোলিও ২: {portfolio_2}")
    print(f"   ইউনিয়ন (সব): {portfolio_1 | portfolio_2}")
    print(f"   ইন্টারসেকশন (কমন): {portfolio_1 & portfolio_2}")
    print(f"   ডিফারেন্স (শুধু ১): {portfolio_1 - portfolio_2}")

    # --- এক্সারসাইজ ৪ ---
    print(f"\n   ✏️  এক্সারসাইজ ৪:")
    print(f"       ৫টি স্টকের ডিকশনারি তৈরি করুন: টিকার → প্রাইস")
    print(f"       সর্বোচ্চ ও সর্বনিম্ন প্রাইসের স্টক বের করুন")
    print(f"       স্টকগুলোর গড় প্রাইস বের করুন")


review_data_structures()

# ============================================================
# পার্ট 5: ফাংশন ও মডিউল (Day 9-11 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 5: ফাংশন ও মডিউল")
print("=" * 70)

def review_functions():
    """
    ফাংশন (def), প্যারামিটার, রিটার্ন ভ্যালু, ল্যাম্বডা ফাংশন।
    """
    print("\n[5.1] ফাংশন ডেমো — ফাইন্যান্স ফাংশন\n")

    def calculate_sharpe_ratio(returns: list, risk_free_rate: float = 0.05) -> float:
        """
        Sharpe Ratio ক্যালকুলেট করে।

        Sharpe Ratio = (পোর্টফোলিও রিটার্ন - রিস্ক-ফ্রি রেট) / স্ট্যান্ডার্ড ডেভিয়েশন

        Parameters:
            returns: রিটার্নের তালিকা (%)
            risk_free_rate: রিস্ক-ফ্রি রেট (ডিফল্ট: 5%)

        Returns:
            float: Sharpe Ratio
        """
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)
        excess_return = avg_return - (risk_free_rate / 252)  # ডেইলি রিস্ক-ফ্রি
        return excess_return / std_dev if std_dev > 0 else 0

    # ডেইলি রিটার্ন ডেটা (%)
    daily_returns = [0.5, -0.3, 1.2, -0.8, 0.9, 0.1, -0.2, 1.5, -0.5, 0.7]
    sharpe = calculate_sharpe_ratio(daily_returns)
    print(f"   ডেইলি রিটার্ন: {daily_returns}")
    print(f"   Sharpe Ratio: {sharpe:.4f}")
    print(f"   → Sharpe > 1: ভাল, > 2: খুব ভাল, > 3: অসাধারণ")

    print(f"\n   [5.2] ল্যাম্বডা ফাংশন — মুনাফা সর্টিং\n")

    stocks = [
        ("RY.TO", 145.00, 162.30),
        ("TD.TO", 82.50, 85.60),
        ("BNS.TO", 70.25, 73.10),
        ("SHOP.TO", 95.50, 110.20),
    ]

    # ল্যাম্বডা দিয়ে রিটার্ন % অনুযায়ী সর্ট
    stocks_sorted = sorted(stocks, key=lambda s: (s[2] - s[1]) / s[1] * 100, reverse=True)

    print(f"   স্টক (রিটার্ন % অনুযায়ী সাজানো):")
    for ticker, buy, curr in stocks_sorted:
        ret = (curr - buy) / buy * 100
        print(f"   {ticker:<10} বাই: ${buy:<7.2f} বর্তমান: ${curr:<7.2f} রিটার্ন: {ret:+.2f}%")

    # --- এক্সারসাইজ ৫ ---
    print(f"\n   ✏️  এক্সারসাইজ ৫:")
    print(f"       একটি ফাংশন 'calculate_portfolio_beta' তৈরি করুন")
    print(f"       প্যারামিটার: stock_returns(list), market_returns(list)")
    print(f"       সূত্র: covariance(stock, market) / variance(market)")


review_functions()

# ============================================================
# পার্ট 6: ফাইল হ্যান্ডলিং (Day 12-13 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 6: ফাইল হ্যান্ডলিং — CSV, JSON, TXT")
print("=" * 70)

def review_file_handling():
    """
    CSV, JSON, TXT ফাইল রিড/রাইট করা।
    """
    print("\n[6.1] CSV ফাইল রাইট ও রিড\n")

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # CSV ফাইল তৈরি
    csv_path = output_dir / "stocks_review.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Company", "Shares", "BuyPrice", "CurrentPrice"])
        writer.writerow(["RY.TO", "Royal Bank of Canada", 50, 145.00, 162.30])
        writer.writerow(["TD.TO", "TD Bank", 75, 82.50, 85.60])
        writer.writerow(["BNS.TO", "Bank of Nova Scotia", 40, 70.25, 73.10])

    print(f"   ✓ CSV তৈরি: {csv_path}")

    # CSV ফাইল পড়া
    print(f"\n   CSV ফাইল থেকে পড়া:")
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        print(f"   হেডার: {headers}")
        for row in reader:
            ticker, company, shares, buy, curr = row
            print(f"   {ticker:<10} {company:<25} {shares:>5} shares | "
                  f"Buy: ${float(buy):<7.2f} | Now: ${float(curr):<7.2f}")

    # JSON ফাইল
    print(f"\n   [6.2] JSON ফাইল\n")
    portfolio_data = {
        "investor": "Jahirul Islam",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "holdings": [
            {"ticker": "RY.TO", "shares": 50, "avg_cost": 145.00},
            {"ticker": "TD.TO", "shares": 75, "avg_cost": 82.50},
        ]
    }

    json_path = output_dir / "portfolio_review.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(portfolio_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ JSON তৈরি: {json_path}")

    # JSON রিড
    with open(json_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"   ইনভেস্টর: {loaded['investor']}")
    print(f"   মোট হোল্ডিং: {len(loaded['holdings'])} টি")

    # --- এক্সারসাইজ ৬ ---
    print(f"\n   ✏️  এক্সারসাইজ ৬:")
    print(f"       একটি ট্রানজেকশন CSV তৈরি করুন:")
    print(f"       Date,Ticker,Type,Shares,Price")
    print(f"       ২০২৪-০১-১৫,RY.TO,BUY,৫০,১৪৫.০০")
    print(f"       ফাইল পড়ে BUY vs SELL ট্রানজেকশন কাউন্ট করুন")


review_file_handling()

# ============================================================
# পার্ট 7: API ও ওয়েব স্ক্র্যাপিং (Day 14-17 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 7: API ও ওয়েব স্ক্র্যাপিং")
print("=" * 70)

def review_api():
    """
    API কল (requests), JSON রেসপন্স হ্যান্ডলিং, ডেটা প্রসেসিং।
    """
    print("\n[7.1] API ডেমো — সিমুলেটেড API কল\n")

    # সিমুলেটেড API রেসপন্স
    simulated_response = {
        "base": "CAD",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rates": {
            "USD": 0.74,
            "EUR": 0.68,
            "GBP": 0.58,
            "JPY": 110.25,
            "BDT": 81.50,
            "INR": 61.75,
            "AUD": 1.12,
            "CHF": 0.65,
        }
    }

    print(f"   API বেস: {simulated_response['base']}")
    print(f"   তারিখ: {simulated_response['date']}")
    print(f"   উপলব্ধ রেট: {len(simulated_response['rates'])} টি")
    print()

    # এক্সচেঞ্জ রেট কনভার্সন
    cad_amount = 1000  # 1000 CAD
    print(f"   {cad_amount} CAD → অন্যান্য কারেন্সি:")
    for currency, rate in simulated_response['rates'].items():
        converted = cad_amount * rate
        print(f"      {cad_amount} CAD = {converted:,.2f} {currency} (রেট: {rate})")

    # এক্সারসাইজ: নিজে API কল করা
    print(f"\n   💡 রিয়েল API দিয়ে কাজ করার কোড:\n")
    print(f'   import requests')
    print(f"   url = 'https://api.frankfurter.app/latest?from=CAD'")
    print(f"   response = requests.get(url, timeout=10)")
    print(f"   data = response.json()")
    print(f"   print(data['rates']['USD'])  # CAD to USD")

    # --- এক্সারসাইজ ৭ ---
    print(f"\n   ✏️  এক্সারসাইজ ৭:")
    print(f"       একটি এক্সচেঞ্জ কনভার্টার ফাংশন তৈরি করুন")
    print(f"       ট্রাভেল বাজেট: 5000 CAD")
    print(f"       কনভার্ট করুন: USD, EUR, GBP, JPY — প্রতিটিতে কত হবে?")


review_api()

# ============================================================
# পার্ট 8: Pandas ও Matplotlib (Day 15-16 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 8: Pandas ও Matplotlib (ডেটা অ্যানালাইসিস)")
print("=" * 70)

def review_pandas_matplotlib():
    """
    Pandas ডেটাফ্রেম এবং Matplotlib চার্টিং।
    """
    print("\n[8.1] Pandas ডেমো — স্টক ডেটাফ্রেম\n")

    try:
        import pandas as pd

        # ডেটাফ্রেম তৈরি
        df = pd.DataFrame({
            "Ticker": ["RY.TO", "TD.TO", "BNS.TO", "CNQ.TO", "SHOP.TO"],
            "Company": ["Royal Bank", "TD Bank", "Scotia Bank", "Canadian Natural", "Shopify"],
            "Shares": [50, 75, 40, 30, 15],
            "BuyPrice": [145.00, 82.50, 70.25, 85.00, 95.50],
            "CurrentPrice": [162.30, 85.60, 73.10, 98.40, 110.20],
            "Sector": ["Banking", "Banking", "Banking", "Energy", "Technology"],
        })

        # ক্যালকুলেটেড কলাম
        df["Cost"] = df["Shares"] * df["BuyPrice"]
        df["Value"] = df["Shares"] * df["CurrentPrice"]
        df["Return%"] = ((df["CurrentPrice"] - df["BuyPrice"]) / df["BuyPrice"]) * 100

        print("   স্টক পোর্টফোলিও ডেটাফ্রেম:")
        print(df.to_string(index=False))
        print()
        print(f"   মোট স্টক: {len(df)} টি")
        print(f"   মোট বিনিয়োগ: ${df['Cost'].sum():,.2f}")
        print(f"   বর্তমান মূল্য: ${df['Value'].sum():,.2f}")
        print(f"   মোট রিটার্ন: ${df['Value'].sum() - df['Cost'].sum():+,.2f}")
        print(f"   গড় রিটার্ন: {df['Return%'].mean():+.2f}%")
        print(f"\n   সেক্টর অনুযায়ী গ্রুপ:")
        sector_group = df.groupby("Sector")["Value"].sum()
        print(sector_group)

        # --- এক্সারসাইজ ৮ ---
        print(f"\n   ✏️  এক্সারসাইজ ৮:")
        print(f"       ২০টি র্যান্ডম স্টক প্রাইসের সিরিজ তৈরি করুন")
        print(f"       pandas.Series দিয়ে, তারপর:")
        print(f"       - মূভিং এভারেজ (৩ দিনের) বের করুন")
        print(f"       - প্রাইস ৫% বেড়েছে এমন দিন চিহ্নিত করুন")

    except ImportError:
        print("   ⚠ pandas ইন্সটল নেই।pip install pandas' দিয়ে ইন্সটল করুন")
        print()
        print("   pandas ছাড়া ম্যানুয়ালি:")
        data = [
            ["RY.TO", "Royal Bank", 50, 145.00, 162.30],
            ["TD.TO", "TD Bank", 75, 82.50, 85.60],
        ]
        for row in data:
            cost = row[2] * row[3]
            val = row[2] * row[4]
            ret = (row[4] - row[3]) / row[3] * 100
            print(f"   {row[0]:<10} {row[1]:<15} Cost: ${cost:<8.2f} Value: ${val:<8.2f} Return: {ret:+.2f}%")


review_pandas_matplotlib()

# ============================================================
# পার্ট 9: OOP — ক্লাস ও অবজেক্ট (Day 14 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট 9: OOP — অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং")
print("=" * 70)

def review_oop():
    """
    ক্লাস, অবজেক্ট, ইনহেরিটেন্স, এনক্যাপসুলেশন।
    """
    print("\n[9.1] ক্লাস ডেমো — স্টক ট্রেডিং ক্লাস\n")

    class Stock:
        """একটি স্টক রিপ্রেজেন্ট করে"""

        exchange = "TSX"  # ক্লাস ভেরিয়েবল

        def __init__(self, ticker: str, name: str, price: float):
            self.ticker = ticker        # ইন্সট্যান্স ভেরিয়েবল
            self.name = name
            self._price = price         # প্রাইভেট (আন্ডারস্কোর কনভেনশন)

        @property
        def price(self) -> float:
            """গেটার — প্রাইস রিটার্ন করে"""
            return self._price

        @price.setter
        def price(self, new_price: float):
            """সেটার — প্রাইস সেট করে ভ্যালিডেশন সহ"""
            if new_price <= 0:
                raise ValueError("দাম ০ বা নেগেটিভ হতে পারে না!")
            self._price = new_price

        def __str__(self) -> str:
            return f"{self.ticker} ({self.name}) @ ${self.price:.2f}"

        def __repr__(self) -> str:
            return f"Stock('{self.ticker}', '{self.name}', {self.price})"

    # Inheritance — ইনহেরিটেন্স
    class DividendStock(Stock):
        """স্টকের সাবক্লাস — ডিভিডেন্ড স্টক"""

        def __init__(self, ticker: str, name: str, price: float,
                     dividend_yield: float):
            super().__init__(ticker, name, price)
            self.dividend_yield = dividend_yield

        def annual_dividend(self) -> float:
            """বার্ষিক ডিভিডেন্ড ক্যালকুলেট করে"""
            return self.price * (self.dividend_yield / 100)

        def __str__(self) -> str:
            return (f"{super().__str__()} | "
                    f"Div: {self.dividend_yield:.2f}% "
                    f"(${self.annual_dividend():.2f}/share)")

    # ব্যবহার
    ry = DividendStock("RY.TO", "Royal Bank of Canada", 162.30, 4.2)
    td = DividendStock("TD.TO", "TD Bank", 85.60, 4.8)
    shop = Stock("SHOP.TO", "Shopify Inc.", 110.20)  # নো ডিভিডেন্ড

    print(f"   {ry}")
    print(f"   {td}")
    print(f"   {shop}")
    print(f"\n   এক্সচেঞ্জ: {Stock.exchange}")

    # প্রপার্টি সেটার টেস্ট
    try:
        ry.price = -50  # ভ্যালু
    except ValueError as e:
        print(f"\n   ⚠ এরর হ্যান্ডলিং: {e}")

    # --- এক্সারসাইজ ৯ ---
    print(f"\n   ✏️  এক্সারসাইজ ৯:")
    print(f"       Portfolio নামে একটি ক্লাস তৈরি করুন")
    print(f"       মেথড: add_stock(), remove_stock(), total_value(),")
    print(f"       best_performer(), worst_performer()")


review_oop()

# ============================================================
# পার্ট 10: এরর হ্যান্ডলিং (Day 19 রিভিউ)
# ============================================================
print("\n" + "=" * 70)
print("   পার্ট ১০: এরর হ্যান্ডলিং (Try/Except)")
print("=" * 70)

def review_error_handling():
    """
    Try/Except, Finally, কাস্টম এক্সেপশন।
    """
    print("\n[10.1] try/except ডেমো\n")

    def safe_division(a: float, b: float) -> float:
        """নিরাপদে ভাগ করে, এরর হ্যান্ডল সহ।"""
        try:
            result = a / b
        except ZeroDivisionError:
            print(f"   ⚠ ZeroDivisionError: ০ দিয়ে ভাগ করা যায় না!")
            return float('inf')
        except TypeError as e:
            print(f"   ⚠ TypeError: {e}")
            return 0.0
        else:
            # কোনো এরর না হলে
            return result
        finally:
            # সব সময় রান হবে
            pass

    print(f"   ১০/২ = {safe_division(10, 2)}")
    print(f"   ১০/০ = {safe_division(10, 0)}")
    print(f"   ১০/'ক' = {safe_division(10, 'ক')}")

    print(f"\n   [10.2] কাস্টম এক্সেপশন\n")

    class InsufficientFundsError(Exception):
        """অ্যাকাউন্টে পর্যাপ্ত টাকা না থাকলে।"""
        pass

    class BankAccount:
        def __init__(self, balance: float):
            self.balance = balance

        def withdraw(self, amount: float):
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"পর্যাপ্ত ব্যালেন্স নেই! প্রয়োজন: ${amount:.2f}, "
                    f"উপলব্ধ: ${self.balance:.2f}"
                )
            self.balance -= amount
            print(f"   ✓ ${amount:.2f} উত্তোলন করা হয়েছে। বাকি: ${self.balance:.2f}")

    account = BankAccount(5000)
    try:
        account.withdraw(3000)
        account.withdraw(3000)  # দ্বিতীয়বার ব্যর্থ হবে
    except InsufficientFundsError as e:
        print(f"   ⚠ {e}")

    print(f"\n   [10.3] ট্রানজেকশন লগিং\n")

    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("Bank")

    try:
        amount = 1000
        logger.info(f"উত্তোলন শুরু: ${amount}")
        account.withdraw(amount)
        logger.info(f"উত্তোলন সফল: ${amount}")
    except InsufficientFundsError:
        logger.error(f"উত্তোলন ব্যর্থ: ব্যালেন্স কম!")
    except Exception as e:
        logger.critical(f"অপ্রত্যাশিত ত্রুটি: {e}")
    finally:
        logger.info(f"বর্তমান ব্যালেন্স: ${account.balance:.2f}")

    # --- এক্সারসাইজ ১০ ---
    print(f"\n   ✏️  এক্সারসাইজ ১০:")
    print(f"       একটি ফাংশন 'validate_stock_data' তৈরি করুন")
    print(f"       ভ্যালিডেশন: টিকার খালি নয়, শেয়ার > ০, প্রাইস > ০")
    print(f"       প্রতিটি ভ্যালিডেশনের জন্য আলাদা কাস্টম এক্সেপশন")


review_error_handling()

# ============================================================
# 🏆 ফাইনাল চ্যালেঞ্জ: ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর
# ============================================================
print("\n" + "=" * 70)
print("   🏆 ফাইনাল চ্যালেঞ্জ: ফাইন্যান্সিয়াল রিপোর্ট জENerator")
print("   (Capstone — সব টপিকের সমন্বয়)")
print("=" * 70)

class FinancialReportGenerator:
    """
    সম্পূর্ণ ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর।
    Day 1-20 এর সব শেখা বিষয় একসাথে ব্যবহার করে।

    বৈশিষ্ট্য:
    - পোর্টফোলিও লোড/ম্যানেজ (CSV, JSON)
    - স্টক পারফরম্যান্স অ্যানালাইসিস
    - ফাইন্যান্সিয়াল রেশিও ক্যালকুলেশন
    - রিপোর্ট জেনারেশন (TXT, CSV, JSON)
    - এরর হ্যান্ডলিং ও লগিং
    - OOP ডিজাইন
    """

    VERSION = "1.0.0"

    def __init__(self, investor_name: str = "Jahirul Islam"):
        """রিপোর্ট জেনারেটর ইনিশিয়ালাইজ"""
        self.investor = investor_name
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.portfolio = []
        self.cash_balance = 0.0
        self.output_dir = Path(__file__).parent / "reports"
        self.output_dir.mkdir(exist_ok=True)

        # লগিং সেটাপ
        self.logger = logging.getLogger("FinancialReport")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        print(f"\n   📋 ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর v{self.VERSION}")
        print(f"   ইনভেস্টর: {self.investor}")
        print(f"   তারিখ: {self.report_date}")
        print(f"   আউটপুট: {self.output_dir}")
        self.logger.info("রিপোর্ট জেনারেটর প্রস্তুত ✅")

    # -------------------------------------------------------
    # হোল্ডিং ম্যানেজমেন্ট
    # -------------------------------------------------------
    def add_holding(self, ticker: str, name: str, shares: int,
                    buy_price: float, current_price: float,
                    sector: str = "Unknown") -> dict:
        """
        পোর্টফোলিওতে নতুন হোল্ডিং যোগ করে।

        Parameters:
            ticker (str): স্টক টিকার
            name (str): কোম্পানির নাম
            shares (int): শেয়ার সংখ্যা
            buy_price (float): ক্রয় মূল্য
            current_price (float): বর্তমান মূল্য
            sector (str): সেক্টর

        Returns:
            dict: হোল্ডিং ডেটা
        """
        # ভ্যালিডেশন
        if not ticker or not name:
            raise ValueError("টিকার ও নাম প্রয়োজন")
        if shares <= 0:
            raise ValueError("শেয়ার সংখ্যা পজিটিভ হতে হবে")
        if buy_price <= 0 or current_price <= 0:
            raise ValueError("প্রাইস পজিটিভ হতে হবে")

        cost = shares * buy_price
        value = shares * current_price
        return_pct = ((current_price - buy_price) / buy_price) * 100

        holding = {
            "ticker": ticker.upper(),
            "name": name,
            "sector": sector,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "cost_basis": round(cost, 2),
            "market_value": round(value, 2),
            "return_pct": round(return_pct, 2),
            "return_dollar": round(value - cost, 2),
        }

        self.portfolio.append(holding)
        self.logger.info(f"➕ {ticker} যোগ করা হয়েছে ({shares} shares)")
        return holding

    def set_cash_balance(self, amount: float):
        """নগদ ব্যালেন্স সেট করে"""
        if amount < 0:
            raise ValueError("নগদ ব্যালেন্স নেগেটিভ হতে পারে না")
        self.cash_balance = amount
        self.logger.info(f"💰 নগদ ব্যালেন্স: ${amount:,.2f}")

    def load_from_csv(self, filepath: str) -> int:
        """CSV ফাইল থেকে হোল্ডিং লোড করে"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"ফাইল পাওয়া যায়নি: {filepath}")

        count = 0
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_holding(
                    ticker=row["ticker"],
                    name=row.get("name", row["ticker"]),
                    shares=int(row["shares"]),
                    buy_price=float(row["buy_price"]),
                    current_price=float(row.get("current_price", row["buy_price"])),
                    sector=row.get("sector", "Unknown"),
                )
                count += 1

        self.logger.info(f"📂 CSV থেকে {count} টি হোল্ডিং লোড করা হয়েছে")
        return count

    def remove_holding(self, ticker: str) -> bool:
        """পোর্টফোলিও থেকে হোল্ডিং রিমুভ করে"""
        for i, h in enumerate(self.portfolio):
            if h["ticker"] == ticker.upper():
                removed = self.portfolio.pop(i)
                self.logger.info(f"➖ {ticker} রিমুভ করা হয়েছে")
                return True
        self.logger.warning(f"⚠ {ticker} পোর্টফোলিওতে নেই")
        return False

    # -------------------------------------------------------
    # অ্যানালাইসিস
    # -------------------------------------------------------
    def calculate_portfolio_stats(self) -> dict:
        """পোর্টফোলিওর সম্পূর্ণ পরিসংখ্যান বের করে"""
        if not self.portfolio:
            return {"error": "পোর্টফোলিও খালি"}

        total_cost = sum(h["cost_basis"] for h in self.portfolio) + self.cash_balance
        total_value = sum(h["market_value"] for h in self.portfolio) + self.cash_balance
        total_return = total_value - total_cost
        total_return_pct = ((total_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0

        # সেক্টর অ্যালোকেশন
        sector_allocation = {}
        for h in self.portfolio:
            sector = h["sector"]
            sector_allocation[sector] = sector_allocation.get(sector, 0) + h["market_value"]

        # সেরা/খারাপ পারফরমার
        best = max(self.portfolio, key=lambda h: h["return_pct"])
        worst = min(self.portfolio, key=lambda h: h["return_pct"])

        # ডাইভার্সিফিকেশন স্কোর (০-১০০)
        if len(self.portfolio) <= 1:
            diversification = 0
        else:
            sector_count = len(sector_allocation)
            holding_count = len(self.portfolio)
            diversification = min((sector_count * 20 + holding_count * 5), 100)

        stats = {
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "total_return": round(total_return, 2),
            "total_return_pct": round(total_return_pct, 2),
            "holding_count": len(self.portfolio),
            "cash_balance": self.cash_balance,
            "best_performer": best,
            "worst_performer": worst,
            "sector_allocation": sector_allocation,
            "diversification_score": diversification,
            "avg_return_pct": round(
                sum(h["return_pct"] for h in self.portfolio) / len(self.portfolio), 2
            ),
        }
        return stats

    def calculate_financial_ratios(self) -> dict:
        """ফাইন্যান্সিয়াল রেশিও ক্যালকুলেট করে"""
        stats = self.calculate_portfolio_stats()
        if "error" in stats:
            return stats

        ratios = {}

        # P/B Ratio (সিম্পলিফাইড — ধরুন বুক ভ্যালু জানা আছে)
        if stats["total_value"] > 0:
            book_value = stats["total_cost"] * 0.85  # আনুমানিক
            ratios["price_to_book"] = round(stats["total_value"] / book_value, 2)

        # ডেট-টু-ইকুইটি (সিম্পলিফাইড)
        # ধরে নিই পোর্টফোলিওতে কোনো ডেট নেই
        ratios["debt_to_equity"] = 0.0

        # রিটার্ন অন ইনভেস্টমেন্ট (ROI)
        if stats.get("total_return_pct"):
            ratios["roi"] = stats["total_return_pct"]

        # রিস্ক-অ্যাডজাস্টেড রিটার্ন (সিম্পলিফাইড Sharpe)
        returns_list = [h["return_pct"] for h in self.portfolio]
        if returns_list:
            avg_ret = sum(returns_list) / len(returns_list)
            variance = sum((r - avg_ret) ** 2 for r in returns_list) / len(returns_list)
            std_dev = math.sqrt(variance) if variance > 0 else 1
            risk_free = 5.0  # 5% risk-free rate (CAD)
            ratios["sharpe_ratio"] = round((avg_ret - risk_free) / std_dev, 4)

        return ratios

    # -------------------------------------------------------
    # রিপোর্ট জেনারেশন
    # -------------------------------------------------------
    def generate_txt_report(self, filename: str = "financial_report.txt") -> Path:
        """
        বিস্তারিত টেক্সট রিপোর্ট জেনারেট করে।

        Returns:
            Path: জেনারেট করা ফাইলের পাথ
        """
        stats = self.calculate_portfolio_stats()
        ratios = self.calculate_financial_ratios()
        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"   📊 ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর\n")
            f.write(f"   {'='*76}\n")
            f.write(f"   ইনভেস্টর: {self.investor}\n")
            f.write(f"   রিপোর্ট তারিখ: {self.report_date}\n")
            f.write("=" * 80 + "\n\n")

            # এক্সিকিউটিভ সামারি
            f.write("১. এক্সিকিউটিভ সামারি\n")
            f.write("-" * 60 + "\n")
            f.write(f"   পোর্টফোলিওর অবস্থা:\n")
            f.write(f"     মোট হোল্ডিং: {stats['holding_count']} টি স্টক\n")
            f.write(f"     নগদ ব্যালেন্স: ${stats['cash_balance']:,.2f}\n")
            f.write(f"     মোট বিনিয়োগ: ${stats['total_cost']:,.2f}\n")
            f.write(f"     বর্তমান মূল্য: ${stats['total_value']:,.2f}\n")
            arrow = "📈" if stats["total_return"] >= 0 else "📉"
            f.write(f"     মোট রিটার্ন: ${stats['total_return']:+,.2f} "
                    f"({stats['total_return_pct']:+.2f}%){arrow}\n")
            f.write(f"     ডাইভার্সিফিকেশন স্কোর: {stats['diversification_score']}/১০০\n\n")

            # হোল্ডিং ডিটেইল
            f.write("২. হোল্ডিং বিস্তারিত\n")
            f.write("-" * 80 + "\n")
            header = (
                f"   {'টিকার':<10} {'কোম্পানি':<25} {'সেক্টর':<15} {'শেয়ার':<8} "
                f"{'খরচ':<10} {'মূল্য':<10} {'রিটার্ন%':<10}"
            )
            f.write(header + "\n")
            f.write("   " + "-" * 78 + "\n")

            for h in sorted(self.portfolio, key=lambda x: x["return_pct"], reverse=True):
                sign = "▲" if h["return_pct"] >= 0 else "▼"
                f.write(
                    f"   {h['ticker']:<10} {h['name'][:24]:<25} {h['sector'][:14]:<15} "
                    f"{h['shares']:<8} ${h['cost_basis']:<8.2f} ${h['market_value']:<8.2f} "
                    f"{sign}{h['return_pct']:<+8.2f}\n"
                )

            # সেক্টর অ্যালোকেশন
            f.write("\n৩. সেক্টর অ্যালোকেশন\n")
            f.write("-" * 60 + "\n")
            for sector, value in sorted(
                stats["sector_allocation"].items(),
                key=lambda x: x[1], reverse=True
            ):
                pct = (value / stats["total_value"]) * 100
                bar = "█" * int(pct / 2)
                f.write(f"   {sector:<20} ${value:>10,.2f} ({pct:>5.1f}%) {bar}\n")

            # পারফরম্যান্স সারাংশ
            f.write("\n৪. পারফরম্যান্স সারাংশ\n")
            f.write("-" * 60 + "\n")
            f.write(f"   🏆 সেরা: {stats['best_performer']['ticker']} — "
                    f"{stats['best_performer']['return_pct']:+.2f}%\n")
            f.write(f"   ⚠️ খারাপ: {stats['worst_performer']['ticker']} — "
                    f"{stats['worst_performer']['return_pct']:+.2f}%\n")
            f.write(f"   📊 গড় রিটার্ন: {stats['avg_return_pct']:+.2f}%\n\n")

            # ফাইন্যান্সিয়াল রেশিও
            f.write("৫. ফাইন্যান্সিয়াল রেশিও\n")
            f.write("-" * 60 + "\n")
            for ratio_name, ratio_value in ratios.items():
                name_bn = {
                    "price_to_book": "P/B রেশিও (প্রাইস টু বুক)",
                    "debt_to_equity": "D/E রেশিও (ডেট টু ইকুইটি)",
                    "roi": "ROI (রিটার্ন অন ইনভেস্টমেন্ট)",
                    "sharpe_ratio": "Sharpe Ratio",
                }.get(ratio_name, ratio_name)
                f.write(f"   {name_bn:<40} {ratio_value}\n")

            # রিকমেন্ডেশন
            f.write("\n৬. রিকমেন্ডেশন\n")
            f.write("-" * 60 + "\n")
            if stats["diversification_score"] < 50:
                f.write("   ⚠️ পোর্টফোলিও ডাইভার্সিফাইড নয়। নতুন সেক্টর যোগ করুন।\n")
            if stats["total_return_pct"] < 0:
                f.write("   🔴 পোর্টফোলিও নেতিবাচক রিটার্ন দিচ্ছে। রিভিউ প্রয়োজন।\n")
            elif stats["total_return_pct"] > 20:
                f.write("   🟢 পোর্টফোলিও ভালো পারফর্ম করছে। বর্তমান কৌশল বজায় রাখুন।\n")
            else:
                f.write("   🟡 পোর্টফোলিও স্থিতিশীল। বাজারের动向 পর্যবেক্ষণ করুন।\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("   রিপোর্ট জেনারেটেড বাই Python Financial Report Generator\n")
            f.write("   Capstone — Day 20\n")
            f.write("=" * 80 + "\n")

        self.logger.info(f"✅ TXT রিপোর্ট তৈরি: {filepath}")
        return filepath

    def generate_csv_report(self, filename: str = "financial_report.csv") -> Path:
        """CSV ফরম্যাটে রিপোর্ট"""
        filepath = self.output_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["টিকার", "কোম্পানি", "সেক্টর", "শেয়ার",
                             "ক্রয় মূল্য", "বর্তমান মূল্য",
                             "মোট খরচ", "বর্তমান মান", "রিটার্ন $", "রিটার্ন %"])
            for h in self.portfolio:
                writer.writerow([
                    h["ticker"], h["name"], h["sector"], h["shares"],
                    h["buy_price"], h["current_price"],
                    h["cost_basis"], h["market_value"],
                    h["return_dollar"], h["return_pct"],
                ])
        self.logger.info(f"✅ CSV রিপোর্ট তৈরি: {filepath}")
        return filepath

    def generate_json_report(self, filename: str = "financial_report.json") -> Path:
        """JSON ফরম্যাটে সম্পূর্ণ রিপোর্ট"""
        stats = self.calculate_portfolio_stats()
        ratios = self.calculate_financial_ratios()

        report = {
            "report_metadata": {
                "generator": f"FinancialReportGenerator v{self.VERSION}",
                "investor": self.investor,
                "date": self.report_date,
                "python_version": sys.version,
            },
            "portfolio": self.portfolio,
            "cash_balance": self.cash_balance,
            "statistics": stats,
            "ratios": ratios,
        }

        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        self.logger.info(f"✅ JSON রিপোর্ট তৈরি: {filepath}")
        return filepath

    def generate_all_reports(self) -> dict:
        """সব ফরম্যাটে রিপোর্ট জেনারেট করে"""
        return {
            "txt": self.generate_txt_report(),
            "csv": self.generate_csv_report(),
            "json": self.generate_json_report(),
        }


# ============================================================
# ফাইনাল চ্যালেঞ্জ রান করা
# ============================================================
def run_capstone():
    """
    ফাইনাল চ্যালেঞ্জ রান করে — সম্পূর্ণ ফাইন্যান্সিয়াল রিপোর্ট।
    """
    print("\n" + "-" * 70)
    print("   🚀 ফাইনাল চ্যালেঞ্জ রান হচ্ছে...")
    print("-" * 70)

    # রিপোর্ট জেনারেটর তৈরি
    generator = FinancialReportGenerator(investor_name="Jahirul Islam")
    generator.set_cash_balance(5000.00)

    # হোল্ডিং যোগ করা
    generator.add_holding("RY.TO", "Royal Bank of Canada", 50, 145.00, 162.30, "Banking")
    generator.add_holding("TD.TO", "Toronto-Dominion Bank", 75, 82.50, 85.60, "Banking")
    generator.add_holding("BNS.TO", "Bank of Nova Scotia", 40, 70.25, 73.10, "Banking")
    generator.add_holding("CNQ.TO", "Canadian Natural Resources", 30, 85.00, 98.40, "Energy")
    generator.add_holding("SHOP.TO", "Shopify Inc.", 15, 95.50, 110.20, "Technology")
    generator.add_holding("ENB.TO", "Enbridge Inc.", 60, 52.00, 54.80, "Energy")
    generator.add_holding("BMO.TO", "Bank of Montreal", 35, 128.00, 135.50, "Banking")
    generator.add_holding("CP.TO", "Canadian Pacific Kansas City", 20, 110.00, 118.75, "Transportation")

    # স্ট্যাটস দেখা
    stats = generator.calculate_portfolio_stats()
    print(f"\n   📊 পোর্টফোলিও সারাংশ:")
    print(f"   মোট হোল্ডিং: {stats['holding_count']} টি স্টক")
    print(f"   মোট বিনিয়োগ: ${stats['total_cost']:,.2f}")
    print(f"   বর্তমান মূল্য: ${stats['total_value']:,.2f}")
    print(f"   মোট রিটার্ন: ${stats['total_return']:+,.2f} ({stats['total_return_pct']:+.2f}%)")
    print(f"   🏆 সেরা: {stats['best_performer']['ticker']} ({stats['best_performer']['return_pct']:+.2f}%)")
    print(f"   ⚠️ খারাপ: {stats['worst_performer']['ticker']} ({stats['worst_performer']['return_pct']:+.2f}%)")
    print(f"   ডাইভার্সিফিকেশন: {stats['diversification_score']}/১০০")

    # ফাইন্যান্সিয়াল রেশিও
    ratios = generator.calculate_financial_ratios()
    print(f"\n   📈 ফাইন্যান্সিয়াল রেশিও:")
    for name, value in ratios.items():
        name_bn = {
            "price_to_book": "P/B Ratio",
            "debt_to_equity": "D/E Ratio",
            "roi": "ROI (%)",
            "sharpe_ratio": "Sharpe Ratio",
        }.get(name, name)
        print(f"   {name_bn:<20} = {value}")

    # সব রিপোর্ট জেনারেট
    files = generator.generate_all_reports()
    print(f"\n   📁 জেনারেট করা ফাইল:")
    for fmt, path in files.items():
        size = os.path.getsize(path)
        print(f"   • {fmt.upper()}: {path} ({size:,} বাইট)")

    return generator


# ============================================================
# বোনাস: নিজে করার জন্য এক্সট্রা চ্যালেঞ্জ
# ============================================================
def extra_challenges():
    """
    Day 20-এর পর আরও প্র্যাকটিস করার জন্য চ্যালেঞ্জ।
    """
    print("\n" + "=" * 70)
    print("   💪 এক্সট্রা চ্যালেঞ্জ — নিজে করার জন্য")
    print("=" * 70)
    print()

    challenges = [
        ("১. মার্কেট ডেটা ফেচার",
         "yfinance বা Alpha Vantage API দিয়ে রিয়েল-টাইম স্টক প্রাইস ফেচ করুন"),
        ("২. ডিভিডেন্ড ক্যালকুলেটর",
         "পোর্টফোলিওর মোট বার্ষিক ডিভিডেন্ড ইনকাম ক্যালকুলেট করুন"),
        ("৩. পোর্টফোলিও রিব্যালেন্সার",
         "টার্গেট অ্যালোকেশন (%) অনুযায়ী কত শেয়ার কিনতে/বিক্রি করতে হবে তা বের করুন"),
        ("৪. ট্যাক্স ক্যালকুলেটর",
         "কানাডিয়ান ক্যাপিটাল গেইনস ট্যাক্স (৫০% ইনক্লুশন রেট) ক্যালকুলেট করুন"),
        ("৫. মুদ্রা কনভার্টার",
         "API থেকে রেট এনে যেকোনো কারেন্সি কনভার্ট করুন (GUI সহ)"),
        ("৬. ওয়েব ড্যাশবোর্ড",
         "Flask বা Streamlit দিয়ে একটি ওয়েব ড্যাশবোর্ড তৈরি করুন"),
        ("৭. ব্যাকটেস্টিং ইঞ্জিন",
         "ঐতিহাসিক ডেটা দিয়ে ট্রেডিং স্ট্র্যাটেজি ব্যাকটেস্ট করুন"),
        ("৮. ইমোশনাল অ্যানালাইসিস",
         "News API দিয়ে স্টক সম্পর্কিত নিউজের সেন্টিমেন্ট অ্যানালাইসিস করুন"),
        ("৯. API মাইক্রোসার্ভিস",
         "FastAPI দিয়ে আপনার পোর্টফোলিও অ্যানালাইজারকে API সার্ভিস বানান"),
        ("১০. অটোমেটেড রিপোর্ট",
         "প্রতিদিন স্বয়ংক্রিয়ভাবে ইমেইলে রিপোর্ট পাঠানোর সিস্টেম তৈরি করুন"),
    ]

    for i, (title, desc) in enumerate(challenges, 1):
        print(f"   {title}")
        print(f"   {'':40} → {desc}")
        print()

    print(f"   💡 টিপ: প্রতিটি চ্যালেঞ্জের জন্য আলাদা .py ফাইল তৈরি করুন")
    print(f"   📁 ~/LearningPath/Python/week01_basics/projects/ ফোল্ডারে রাখুন")


# ============================================================
# মেইন ফাংশন
# ============================================================
def main():
    """
    Day 20 ক্যাপস্টোন রিভিউ — প্রধান এন্ট্রি পয়েন্ট।
    """
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "   🎓 Python ফাইন্যান্স — Day 20 ক্যাপস্টোন রিভিউ".center(66) + "║")
    print("║" + "   লেখক: Jahirul Islam — Finance Graduate, Canada".center(66) + "║")
    print("║" + "   টপিক কভার: Day 1 থেকে Day 19 পর্যন্ত সবকিছু".center(66) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("   📋 রিভিউ অংশ:")
    print("   পার্ট 1:  ভেরিয়েবল, ডেটা টাইপ ও অপারেটর")
    print("   পার্ট 2:  কন্ডিশনাল স্টেটমেন্ট")
    print("   পার্ট 3:  লুপ (for, while)")
    print("   পার্ট 4:  ডেটা স্ট্রাকচার (list, dict, tuple, set)")
    print("   পার্ট 5:  ফাংশন ও মডিউল")
    print("   পার্ট 6:  ফাইল হ্যান্ডলিং")
    print("   পার্ট 7:  API ও ওয়েব স্ক্র্যাপিং")
    print("   পার্ট 8:  Pandas ও Matplotlib")
    print("   পার্ট 9:  OOP (ক্লাস ও অবজেক্ট)")
    print("   পার্ট 10: এরর হ্যান্ডলিং")
    print("   🏆 ফাইনাল: ফাইন্যান্সিয়াল রিপোর্ট জেনারেটর")

    # এক্সারসাইজের উত্তর চেক করার জন্য ইউজার ইনপুট নেওয়া
    print("\n   ক্যাপস্টোন রান করতে 'y' চাপুন (অথবা Enter দিয়ে স্কিপ করুন): ", end="")
    try:
        choice = input().strip().lower()
        if choice == "y":
            run_capstone()
    except (EOFError, KeyboardInterrupt):
        pass

    # এক্সট্রা চ্যালেঞ্জ দেখানো
    extra_challenges()

    print("\n" + "=" * 70)
    print("   🎉 অভিনন্দন! তুমি Python ফাইন্যান্স কোর্স সম্পূর্ণ করেছ!")
    print("   Day 1 থেকে Day 20 পর্যন্ত সব টপিক কভার হয়েছে।")
    print()
    print("   📌 পরবর্তী পদক্ষেপ:")
    print("   ১. প্রতিটি এক্সারসাইজ নিজে করার চেষ্টা করুন")
    print("   ২. এক্সট্রা চ্যালেঞ্জগুলোর উপর কাজ করুন")
    print("   ৩. রিয়েল মার্কেট ডেটা দিয়ে আপনার পোর্টফোলিও অ্যানালাইজ করুন")
    print("   ৪. GitHub-এ আপনার প্রজেক্ট পাবলিশ করুন")
    print("   ৫. Data Analyst চাকরির জন্য পোর্টফোলিও তৈরি করুন")
    print()
    print("   ☕ শুভকামনা! — Jahirul Islam")
    print("=" * 70 + "\n")

    return 0


if __name__ == "__main__":
    main()
