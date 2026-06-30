#!/usr/bin/env python3
"""
Day 18: Portfolio Project — স্টক পোর্টফোলিও অ্যানালাইজার
=============================================================
একটি সম্পূর্ণ ওয়ার্কিং প্রজেক্ট:
  1. পোর্টফোলিও লোড করা (CSV ফাইল থেকে)
  2. স্টক প্রাইস ফেচ করা (yfinance অথবা ডেমো API দিয়ে)
  3. রিটার্ন ক্যালকুলেশন (ডেইলি রিটার্ন, কিউমুলেটিভ রিটার্ন)
  4. পারফরম্যান্স ভিজুয়ালাইজেশন (গ্রাফ)

Finance Graduate (Canada) — Jahirul Islam
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# প্রয়োজনীয় গ্রন্থাগার চেক
# ============================================================
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
    print("✓ pandas পাওয়া গেছে")
except ImportError:
    PANDAS_AVAILABLE = False
    print("✗ pandas ইন্সটল নেই → pip install pandas")

try:
    import matplotlib
    matplotlib.use('Agg')  # লোকাল ডিসপ্লে ছাড়া রেন্ডার
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
    print("✓ matplotlib পাওয়া গেছে")
except ImportError:
    MPL_AVAILABLE = False
    print("✗ matplotlib ইন্সটল নেই → pip install matplotlib")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    print("✓ numpy পাওয়া গেছে")
except ImportError:
    NUMPY_AVAILABLE = False
    print("✗ numpy ইন্সটল নেই → pip install numpy")

# yfinance চেক — Yahoo Finance থেকে স্টক ডেটা আনার জন্য
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
    print("✓ yfinance পাওয়া গেছে")
except ImportError:
    YFINANCE_AVAILABLE = False
    print("✗ yfinance ইন্সটল নেই → pip install yfinance")

print("\n" + "=" * 70)

# ============================================================
# সেটআপ: ফাইল পাথ ও ডিরেক্টরি
# ============================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# স্যাম্পল পোর্টফোলিও CSV ফাইল পাথ
PORTFOLIO_CSV = DATA_DIR / "portfolio.csv"
PORTFOLIO_JSON = DATA_DIR / "portfolio.json"
PERFORMANCE_PLOT = DATA_DIR / "portfolio_performance.png"
REPORT_TXT = DATA_DIR / "portfolio_report.txt"


# ============================================================
# PART 1: পোর্টফোলিও ডেটা তৈরি / লোড করা
# ============================================================
def create_sample_portfolio():
    """
    একটি স্যাম্পল পোর্টফোলিও তৈরি করে CSV ও JSON ফাইলে সেভ করে।
    কানাডিয়ান ফাইন্যান্স ছাত্রের জন্য বাস্তবসম্মত স্টক নির্বাচন।
    """
    print("\n[1.1] স্যাম্পল পোর্টফোলিও তৈরি করা হচ্ছে...\n")

    portfolio_data = {
        "stocks": [
            {"ticker": "RY.TO", "name": "Royal Bank of Canada", "shares": 50, "buy_price": 145.00},
            {"ticker": "TD.TO", "name": "Toronto-Dominion Bank", "shares": 75, "buy_price": 82.50},
            {"ticker": "BNS.TO", "name": "Bank of Nova Scotia", "shares": 40, "buy_price": 70.25},
            {"ticker": "CNQ.TO", "name": "Canadian Natural Resources", "shares": 30, "buy_price": 85.00},
            {"ticker": "SHOP.TO", "name": "Shopify Inc.", "shares": 15, "buy_price": 95.50},
            {"ticker": "ENB.TO", "name": "Enbridge Inc.", "shares": 60, "buy_price": 52.00},
            {"ticker": "BMO.TO", "name": "Bank of Montreal", "shares": 35, "buy_price": 128.00},
            {"ticker": "CP.TO", "name": "Canadian Pacific Kansas City", "shares": 20, "buy_price": 110.00},
        ],
        "cash": 5000.00,  # নগদ ব্যালেন্স
        "currency": "CAD",
        "investor": "Jahirul Islam",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # JSON ফাইল
    with open(PORTFOLIO_JSON, "w", encoding="utf-8") as f:
        json.dump(portfolio_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ JSON পোর্টফোলিও সেভ করা হয়েছে: {PORTFOLIO_JSON}")

    # CSV ফাইল (প্যান্ডাস দিয়ে তৈরি)
    if PANDAS_AVAILABLE:
        df = pd.DataFrame(portfolio_data["stocks"])
        df.to_csv(PORTFOLIO_CSV, index=False, encoding="utf-8")
        print(f"   ✓ CSV পোর্টফোলিও সেভ করা হয়েছে: {PORTFOLIO_CSV}")
    else:
        # Pandas ছাড়া ম্যানুয়ালি CSV লেখা
        with open(PORTFOLIO_CSV, "w", encoding="utf-8") as f:
            f.write("ticker,name,shares,buy_price\n")
            for s in portfolio_data["stocks"]:
                f.write(f"{s['ticker']},{s['name']},{s['shares']},{s['buy_price']}\n")
        print(f"   ✓ CSV পোর্টফোলিও (ম্যানুয়াল) সেভ করা হয়েছে: {PORTFOLIO_CSV}")

    # পোর্টফোলিও সারাংশ
    total_invested = sum(s["shares"] * s["buy_price"] for s in portfolio_data["stocks"])
    total_invested += portfolio_data["cash"]
    print(f"\n   পোর্টফোলিও সারাংশ:")
    print(f"   {'টিকার':<10} {'শেয়ার':<10} {'ক্রয় মূল্য':<12} {'বিনিয়োগ':<15}")
    print(f"   {'-'*10} {'-'*10} {'-'*12} {'-'*15}")
    for s in portfolio_data["stocks"]:
        cost = s["shares"] * s["buy_price"]
        print(f"   {s['ticker']:<10} {s['shares']:<10} ${s['buy_price']:<10.2f} ${cost:<12.2f}")
    print(f"   {'নগদ':<34} ${portfolio_data['cash']:<12.2f}")
    print(f"   {'মোট বিনিয়োগ':<34} ${total_invested:<12.2f}")

    return portfolio_data


# ============================================================
# PART 2: স্টক প্রাইস ফেচ করা
# ============================================================
def fetch_stock_prices(tickers, period="6mo"):
    """
    Yahoo Finance (yfinance) থেকে স্টক প্রাইস ডেটা ডাউনলোড করে।
    yfinance না থাকলে সিমুলেটেড ডেটা তৈরি করে।

    প্যারামিটার:
        tickers (list): স্টক টিকার সিম্বলের তালিকা
        period (str): সময়সীমা (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)

    রিটার্ন:
        DataFrame: প্রতিটি স্টকের জন্য প্রাইস ডেটা
    """
    print(f"\n[2.1] স্টক প্রাইস ফেচ করা হচ্ছে ({len(tickers)} টি স্টক)...\n")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months

    if YFINANCE_AVAILABLE:
        try:
            print("   → yfinance দিয়ে রিয়েল ডেটা ডাউনলোড হচ্ছে...")
            data = yf.download(
                tickers,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                group_by="ticker",
                auto_adjust=True,
                progress=False,
            )

            if data.empty:
                print("   ⚠ yfinance খালি ডেটা দিয়েছে, সিমুলেটেড ব্যবহার হবে")
                return _simulate_prices(tickers, start_date, end_date)

            print(f"   ✓ ডেটা ডাউনলোড সফল! মোট {len(data)} টি রেকর্ড")
            return data

        except Exception as e:
            print(f"   ⚠ yfinance ত্রুটি: {e}")
            print("   → সিমুলেটেড ডেটা ব্যবহার করা হচ্ছে")
            return _simulate_prices(tickers, start_date, end_date)
    else:
        print("   → yfinance না থাকায় সিমুলেটেড ডেটা ব্যবহার করা হচ্ছে")
        return _simulate_prices(tickers, start_date, end_date)


def _simulate_prices(tickers, start_date, end_date):
    """
    সিমুলেটেড স্টক প্রাইস ডেটা তৈরি করে।
    বাস্তব স্টকের মতো র্যান্ডম ওয়াক + ট্রেন্ড জেনারেট করে।

    প্যারামিটার:
        tickers (list): টিকার তালিকা
        start_date, end_date: তারিখ রেঞ্জ

    রিটার্ন:
        dict: {ticker: DataFrame} ফরম্যাটে ডেটা
    """
    print("   → সিমুলেটেড প্রাইস ডেটা তৈরি হচ্ছে...")

    if not NUMPY_AVAILABLE:
        # numpy না থাকলে সরল ডেটা
        data = {}
        import random
        for ticker in tickers:
            dates = pd.date_range(start_date, end_date, freq="B")
            base_price = random.uniform(50, 200)
            prices = []
            price = base_price
            for _ in range(len(dates)):
                change = random.uniform(-2, 2)
                price = max(price + change, price * 0.5)  # 50% এর বেশি পড়বে না
                prices.append(price)
            df = pd.DataFrame({"Close": prices}, index=dates)
            data[ticker] = df
        return data

    # numpy দিয়ে বাস্তবসম্মত সিমুলেশন
    np.random.seed(42)  # রিপ্রোডিউসিবিলিটির জন্য
    data = {}
    n_days = len(pd.bdate_range(start_date, end_date))

    # প্রতিটি স্টকের জন্য আলাদা বৈশিষ্ট্য
    stock_params = {
        "RY.TO": {"base": 165.00, "vol": 0.8, "drift": 0.03},
        "TD.TO": {"base": 85.00, "vol": 0.9, "drift": 0.02},
        "BNS.TO": {"base": 72.50, "vol": 1.0, "drift": 0.01},
        "CNQ.TO": {"base": 98.00, "vol": 1.5, "drift": 0.04},
        "SHOP.TO": {"base": 110.00, "vol": 2.5, "drift": 0.05},
        "ENB.TO": {"base": 53.00, "vol": 0.7, "drift": 0.02},
        "BMO.TO": {"base": 130.00, "vol": 0.9, "drift": 0.03},
        "CP.TO": {"base": 115.00, "vol": 1.2, "drift": 0.035},
    }

    for ticker in tickers:
        params = stock_params.get(ticker, {"base": 100.00, "vol": 1.0, "drift": 0.02})
        prices = []
        price = params["base"]
        for _ in range(n_days):
            change = np.random.normal(params["drift"] / 100, params["vol"] / 100)
            price = price * (1 + change)
            prices.append(price)

        dates = list(pd.bdate_range(start_date, end_date))
        data[ticker] = pd.DataFrame({"Close": prices}, index=dates)

    print(f"   ✓ {len(tickers)} টি স্টকের জন্য {n_days} দিনের সিমুলেটেড ডেটা তৈরি হয়েছে")
    return data


# ============================================================
# PART 3: পোর্টফোলিও পারফরম্যান্স ক্যালকুলেশন
# ============================================================
def calculate_portfolio_performance(portfolio, price_data):
    """
    পোর্টফোলিওর পারফরম্যান্স বিশ্লেষণ:
    - প্রতিটি স্টকের বর্তমান মূল্য ও রিটার্ন
    - পোর্টফোলিওর মোট ভ্যালু ও রিটার্ন
    - ডেইলি রিটার্ন ও কিউমুলেটিভ রিটার্ন
    - ডাইভার্সিফিকেশন অ্যানালাইসিস

    প্যারামিটার:
        portfolio (dict): পোর্টফোলিও ডেটা
        price_data (dict): {ticker: DataFrame} প্রাইস ডেটা

    রিটার্ন:
        dict: পারফরম্যান্স রিপোর্ট
    """
    print("\n[3.1] পোর্টফোলিও পারফরম্যান্স বিশ্লেষণ...\n")

    results = {
        "stocks": [],
        "total_value": 0,
        "total_cost": 0,
        "total_return": 0,
        "total_return_pct": 0,
        "daily_returns": None,
        "cumulative_returns": None,
        "best_performer": None,
        "worst_performer": None,
    }

    total_value = portfolio.get("cash", 0)
    total_cost = portfolio.get("cash", 0)
    stock_returns = []

    print(f"   {'টিকার':<10} {'শেয়ার':<8} {'ক্রয়':<10} {'বর্তমান':<10} {'মোট খরচ':<12} {'মোট মূল্য':<12} {'রিটার্ন%':<10}")
    print(f"   {'-'*10} {'-'*8} {'-'*10} {'-'*10} {'-'*12} {'-'*12} {'-'*10}")

    for stock in portfolio["stocks"]:
        ticker = stock["ticker"]
        shares = stock["shares"]
        buy_price = stock["buy_price"]
        cost = shares * buy_price

        # বর্তমান প্রাইস (সর্বশেষ Close)
        if ticker in price_data:
            if isinstance(price_data[ticker], pd.DataFrame):
                current_price = price_data[ticker]["Close"].iloc[-1]
            else:
                current_price = buy_price  # বিকল্প
        else:
            current_price = buy_price

        current_value = shares * current_price
        stock_return_pct = ((current_price - buy_price) / buy_price) * 100

        total_cost += cost
        total_value += current_value

        stock_info = {
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": round(current_price, 2),
            "cost": round(cost, 2),
            "value": round(current_value, 2),
            "return_pct": round(stock_return_pct, 2),
            "return_dollar": round(current_value - cost, 2),
        }
        results["stocks"].append(stock_info)
        stock_returns.append(stock_return_pct)

        arrow = "▲" if stock_return_pct >= 0 else "▼"
        print(f"   {ticker:<10} {shares:<8} ${buy_price:<8.2f} ${current_price:<8.2f} "
              f"${cost:<10.2f} ${current_value:<10.2f} {arrow}{stock_return_pct:<+8.2f}")

    # মোট রিটার্ন
    results["total_cost"] = round(total_cost, 2)
    results["total_value"] = round(total_value, 2)
    results["total_return"] = round(total_value - total_cost, 2)
    results["total_return_pct"] = round(((total_value - total_cost) / total_cost) * 100, 2)

    print(f"\n   {'নগদ':<63} ${portfolio.get('cash', 0):<10.2f}")
    print(f"   {'মোট খরচ':<63} ${results['total_cost']:<10.2f}")
    print(f"   {'মোট বর্তমান মূল্য':<63} ${results['total_value']:<10.2f}")
    print(f"   {'মোট রিটার্ন':<63} ${results['total_return']:<+10.2f} ({results['total_return_pct']:<+.2f}%)")

    # সেরা ও সবচেয়ে খারাপ পারফরমার
    if results["stocks"]:
        results["best_performer"] = max(results["stocks"], key=lambda x: x["return_pct"])
        results["worst_performer"] = min(results["stocks"], key=lambda x: x["return_pct"])
        print(f"\n   🏆 সেরা পারফরমার: {results['best_performer']['ticker']} "
              f"({results['best_performer']['return_pct']:+.2f}%)")
        print(f"   ⚠️ সবচেয়ে খারাপ: {results['worst_performer']['ticker']} "
              f"({results['worst_performer']['return_pct']:+.2f}%)")

    # ডেইলি পোর্টফোলিও রিটার্ন হিসাব
    if PANDAS_AVAILABLE:
        try:
            # পোর্টফোলিও হিসেবে টোটাল ভ্যালুর সময় সিরিজ
            portfolio_values = []
            for i in range(len(next(iter(price_data.values())))):
                daily_value = portfolio.get("cash", 0)
                for stock in portfolio["stocks"]:
                    ticker = stock["ticker"]
                    if ticker in price_data:
                        df = price_data[ticker]
                        if i < len(df):
                            daily_value += stock["shares"] * df["Close"].iloc[i]
                portfolio_values.append(daily_value)

            dates = next(iter(price_data.values())).index
            portfolio_series = pd.Series(portfolio_values, index=dates)
            results["daily_returns"] = portfolio_series.pct_change().dropna()
            results["cumulative_returns"] = (1 + results["daily_returns"]).cumprod() - 1

            print(f"\n   📊 ডেইলি রিটার্নের পরিসংখ্যান:")
            print(f"       গড়: {results['daily_returns'].mean()*100:.4f}%")
            print(f"       স্ট্যান্ডার্ড ডেভিয়েশন: {results['daily_returns'].std()*100:.4f}%")
            print(f"       সর্বোচ্চ: {results['daily_returns'].max()*100:.4f}%")
            print(f"       সর্বনিম্ন: {results['daily_returns'].min()*100:.4f}%")
        except Exception as e:
            print(f"   ⚠ সময় সিরিজ বিশ্লেষণ ত্রুটি: {e}")

    return results


# ============================================================
# PART 4: পারফরম্যান্স গ্রাফ প্লটিং
# ============================================================
def plot_portfolio_performance(performance, price_data):
    """
    পোর্টফোলিও পারফরম্যান্সের ভিজুয়ালাইজেশন:
    1. কিউমুলেটিভ রিটার্ন (%)
    2. পৃথক স্টকের রিটার্ন (বার চার্ট)
    3. পোর্টফোলিও অ্যালোকেশন (পাই চার্ট)

    প্যারামিটার:
        performance (dict): পারফরম্যান্স রিপোর্ট
        price_data (dict): প্রাইস ডেটা
    """
    print(f"\n[4.1] পারফরম্যান্স গ্রাফ তৈরি করা হচ্ছে...\n")

    if not MPL_AVAILABLE:
        print("   ✗ matplotlib না থাকায় গ্রাফ তৈরি সম্ভব নয়")
        return

    try:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("📈 স্টক পোর্টফোলিও অ্যানালাইজার — পারফরম্যান্স রিপোর্ট",
                     fontsize=16, fontweight="bold")

        # গ্রাফ 1: কিউমুলেটিভ রিটার্ন
        ax1 = axes[0, 0]
        if performance.get("cumulative_returns") is not None:
            cum_returns = performance["cumulative_returns"] * 100
            cum_returns.plot(ax=ax1, color="#2E86AB", linewidth=2)
            ax1.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
            ax1.fill_between(cum_returns.index, 0, cum_returns.values,
                             alpha=0.2, color="#2E86AB")
            ax1.set_title("কিউমুলেটিভ রিটার্ন (%)", fontsize=12)
            ax1.set_ylabel("রিটার্ন (%)")
            ax1.grid(True, alpha=0.3)
            ax1.legend(["পোর্টফোলিও"])

        # গ্রাফ 2: পৃথক স্টকের রিটার্ন
        ax2 = axes[0, 1]
        tickers = [s["ticker"] for s in performance["stocks"]]
        returns = [s["return_pct"] for s in performance["stocks"]]
        colors = ["#2ECC71" if r >= 0 else "#E74C3C" for r in returns]
        bars = ax2.bar(tickers, returns, color=colors, alpha=0.8)
        ax2.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
        ax2.set_title("প্রতি স্টকের রিটার্ন (%)", fontsize=12)
        ax2.set_ylabel("রিটার্ন (%)")
        ax2.tick_params(axis="x", rotation=45)
        # বারগুলোর উপরে মান দেখানো
        for bar, ret in zip(bars, returns):
            ax2.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + (0.5 if ret >= 0 else -1.5),
                     f"{ret:+.1f}%", ha="center", fontsize=8)

        # গ্রাফ 3: পোর্টফোলিও অ্যালোকেশন (পাই চার্ট)
        ax3 = axes[1, 0]
        values = [s["value"] for s in performance["stocks"]]
        labels = [s["ticker"] for s in performance["stocks"]]
        # ছোট ভ্যালুগুলো "অন্যান্য" তে মার্জ করা
        total = sum(values)
        threshold = total * 0.05  # 5% এর নিচে
        other = 0
        main_labels = []
        main_values = []
        for label, value in zip(labels, values):
            if value / total < 0.05:
                other += value
            else:
                main_labels.append(label)
                main_values.append(value)
        if other > 0:
            main_labels.append("অন্যান্য")
            main_values.append(other)

        wedges, texts, autotexts = ax3.pie(
            main_values, labels=main_labels, autopct="%1.1f%%",
            startangle=90, colors=plt.cm.Set2.colors,
            textprops={"fontsize": 9}
        )
        ax3.set_title("পোর্টফোলিও অ্যালোকেশন", fontsize=12)

        # গ্রাফ 4: প্রাইস ট্রেন্ড (সব স্টক)
        ax4 = axes[1, 1]
        if PANDAS_AVAILABLE:
            for ticker, df in price_data.items():
                if isinstance(df, pd.DataFrame) and "Close" in df.columns:
                    # নরমালাইজড প্রাইস (baseline 100)
                    normalized = (df["Close"] / df["Close"].iloc[0]) * 100
                    normalized.plot(ax=ax4, linewidth=1.5, alpha=0.8, label=ticker)
            ax4.set_title("স্টক প্রাইস ট্রেন্ড (বেস=100)", fontsize=12)
            ax4.set_ylabel("প্রাইস ইনডেক্স")
            ax4.grid(True, alpha=0.3)
            ax4.legend(loc="best", fontsize=7)

        plt.tight_layout()
        plt.savefig(PERFORMANCE_PLOT, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"   ✓ গ্রাফ সেভ করা হয়েছে: {PERFORMANCE_PLOT}")
        print(f"   ✓ ফাইল সাইজ: {os.path.getsize(PERFORMANCE_PLOT):,} বাইট")

    except Exception as e:
        print(f"   ✗ গ্রাফ তৈরি করতে ব্যর্থ: {e}")
        import traceback
        traceback.print_exc()


# ============================================================
# PART 5: রিপোর্ট জেনারেটর
# ============================================================
def generate_report(portfolio, performance):
    """
    পোর্টফোলিও অ্যানালাইসিস রিপোর্ট টেক্সট ফাইলে সেভ করে।

    প্যারামিটার:
        portfolio (dict): পোর্টফোলিও ডেটা
        performance (dict): পারফরম্যান্স ডেটা
    """
    print(f"\n[5.1] রিপোর্ট জেনারেট করা হচ্ছে...\n")

    try:
        with open(REPORT_TXT, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("   স্টক পোর্টফোলিও অ্যানালাইসিস রিপোর্ট\n")
            f.write(f"   তারিখ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"   ইনভেস্টর: {portfolio.get('investor', 'N/A')}\n")
            f.write("=" * 70 + "\n\n")

            f.write("পোর্টফোলিও সারাংশ:\n")
            f.write("-" * 60 + "\n")
            f.write(f"মোট স্টক: {len(portfolio['stocks'])} টি\n")
            f.write(f"মোট বিনিয়োগ: ${performance['total_cost']:,.2f}\n")
            f.write(f"বর্তমান মূল্য: ${performance['total_value']:,.2f}\n")
            f.write(f"মোট রিটার্ন: ${performance['total_return']:+,.2f} "
                    f"({performance['total_return_pct']:+.2f}%)\n\n")

            f.write("প্রতি স্টকের বিস্তারিত:\n")
            f.write("-" * 80 + "\n")
            header = f"{'টিকার':<10} {'শেয়ার':<8} {'ক্রয়':<10} {'বর্তমান':<10} {'বিনিয়োগ':<12} {'মূল্য':<12} {'রিটার্ন%':<10}"
            f.write(header + "\n")
            f.write("-" * 80 + "\n")
            for s in performance["stocks"]:
                f.write(f"{s['ticker']:<10} {s['shares']:<8} ${s['buy_price']:<8.2f} "
                        f"${s['current_price']:<8.2f} ${s['cost']:<10.2f} "
                        f"${s['value']:<10.2f} {s['return_pct']:<+8.2f}%\n")

            f.write("\n\nপ্রধান ফলাফল:\n")
            f.write("-" * 60 + "\n")
            f.write(f"🏆 সেরা স্টক: {performance['best_performer']['ticker']} "
                    f"({performance['best_performer']['return_pct']:+.2f}%)\n")
            f.write(f"⚠️ সবচেয়ে খারাপ: {performance['worst_performer']['ticker']} "
                    f"({performance['worst_performer']['return_pct']:+.2f}%)\n\n")

            if performance.get("daily_returns") is not None:
                dr = performance["daily_returns"]
                f.write("ডেইলি রিটার্ন পরিসংখ্যান:\n")
                f.write(f"  গড়: {dr.mean()*100:.4f}%\n")
                f.write(f"  স্ট্যান্ডার্ড ডেভিয়েশন (ঝুঁকি): {dr.std()*100:.4f}%\n")
                f.write(f"  সর্বোচ্চ: {dr.max()*100:.4f}%\n")
                f.write(f"  সর্বনিম্ন: {dr.min()*100:.4f}%\n")
                f.write(f"  Sharp Ratio (approx): {dr.mean()/dr.std()*252**0.5:.4f}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("   রিপোর্ট জেনারেটেড বাই Python পোর্টফোলিও অ্যানালাইজার\n")
            f.write("=" * 70 + "\n")

        print(f"   ✓ রিপোর্ট সেভ করা হয়েছে: {REPORT_TXT}")
        print(f"   ✓ ফাইল সাইজ: {os.path.getsize(REPORT_TXT):,} বাইট")

    except Exception as e:
        print(f"   ✗ রিপোর্ট জেনারেট করতে ব্যর্থ: {e}")


# ============================================================
# MAIN: পুরো প্রজেক্ট রান করা
# ============================================================
def main():
    """
    পোর্টফোলিও অ্যানালাইজারের মেইন ফাংশন।
    পুরো ওয়ার্কফ্লো একসাথে রান করে।
    """
    print("\n" + "=" * 70)
    print("   📊 স্টক পোর্টফোলিও অ্যানালাইজার v1.0")
    print("   Python ফাইন্যান্স প্রজেক্ট — Day 18")
    print("=" * 70)

    # STEP 1: পোর্টফোলিও তৈরি/লোড
    portfolio = create_sample_portfolio()

    # STEP 2: স্টক প্রাইস ফেচ
    tickers = [s["ticker"] for s in portfolio["stocks"]]
    price_data = fetch_stock_prices(tickers)

    # STEP 3: পারফরম্যান্স ক্যালকুলেশন
    performance = calculate_portfolio_performance(portfolio, price_data)

    # STEP 4: গ্রাফ প্লট
    plot_portfolio_performance(performance, price_data)

    # STEP 5: রিপোর্ট জেনারেট
    generate_report(portfolio, performance)

    # ফাইনাল সারাংশ
    print("\n" + "=" * 70)
    print("   ✅ পোর্টফোলিও অ্যানালাইসিস সম্পন্ন!")
    print(f"   📁 ডেটা ফাইল: {DATA_DIR}")
    print(f"   📊 রিপোর্ট: {REPORT_TXT}")
    print(f"   📈 গ্রাফ: {PERFORMANCE_PLOT}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
