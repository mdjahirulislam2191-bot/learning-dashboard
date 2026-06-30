#!/usr/bin/env python3
"""
Day 17: Web Scraping — ৱেব স্ক্র্যাপিং (ওয়েব থেকে ডেটা সংগ্রহ)
==================================================================
Topics:
  1. requests দিয়ে HTTP GET রিকুয়েস্ট পাঠানো
  2. BeautifulSoup (যদি ইন্সটল থাকে) দিয়ে HTML পার্স করা
  3. JSON API থেকে সরাসরি ডেটা নেওয়া
  4. ফাইন্যান্স রিলেটেড উদাহরণ: মুদ্রা বিনিময় হার, চাকরির পোস্টিং

Finance Graduate (Canada) — Jahirul Islam
"""

# ============================================================
# PART 1: Python-এ ওয়েব রিকুয়েস্ট পাঠানো (requests গ্রন্থাগার)
# ============================================================
# requests ইন্সটল না থাকলে: pip install requests
# BeautifulSoup ইন্সটল না থাকলে: pip install beautifulsoup4

import json
import sys

# -----------------------------------------------------------
# requests গ্রন্থাগার চেক করা (ইন্সটল না থাকলে মেসেজ দেখাবে)
# -----------------------------------------------------------
try:
    import requests
    REQUESTS_AVAILABLE = True
    print("✓ requests গ্রন্থাগার পাওয়া গেছে")
except ImportError:
    REQUESTS_AVAILABLE = False
    print("✗ requests ইন্সটল নেই। চালান: pip install requests")

# BeautifulSoup চেক
try:
    from bs4 import BeautifulSoup
    BS_AVAILABLE = True
    print("✓ BeautifulSoup গ্রন্থাগার পাওয়া গেছে")
except ImportError:
    BS_AVAILABLE = False
    print("✗ BeautifulSoup ইন্সটল নেই। চালান: pip install beautifulsoup4")

print("\n" + "=" * 60)


# ============================================================
# PART 2: HTTP রিকুয়েস্টের বেসিক — স্ট্যাটাস কোড, হেডার, কন্টেন্ট
# ============================================================
def basic_request_demo():
    """
    একটি সাধারণ HTTP GET রিকুয়েস্ট করে দেখা যায়
    স্ট্যাটাস কোড, হেডার, এবং কন্টেন্ট কিভাবে পড়তে হয়।
    """
    print("\n[2.1] বেসিক HTTP GET রিকুয়েস্ট ডেমো\n")

    if not REQUESTS_AVAILABLE:
        print("   → requests না থাকায় স্কিপ করা হলো")
        return

    try:
        url = "https://httpbin.org/get"
        response = requests.get(url, timeout=10)

        print(f"   URL: {url}")
        print(f"   স্ট্যাটাস কোড: {response.status_code}")
        print(f"   রেসপন্স টাইপ: {response.headers.get('Content-Type', 'N/A')}")

        # JSON রেসপন্স ডিকোড
        data = response.json()
        print(f"   Origin IP: {data.get('origin', 'N/A')}")
        print(f"   User-Agent: {data.get('headers', {}).get('User-Agent', 'N/A')}")
        print("   ✓ রিকুয়েস্ট সফল!")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ রিকুয়েস্ট ব্যর্থ: {e}")


basic_request_demo()
print("\n" + "=" * 60)


# ============================================================
# PART 3: ফাইন্যান্স উদাহরণ ১ — মুদ্রা বিনিময় হার (Exchange Rate)
# ============================================================
# ফ্রি API: exchangerate.host, frankfurter.app, অথবা exchangerate-api.com
# আমরা frankfurter.app ব্যবহার করব (কোনো API কী লাগে না)

def scrape_currency_exchange_rates():
    """
    frankfurter.app API থেকে বর্তমান মুদ্রা বিনিময় হার সংগ্রহ।
    CAD (কানাডিয়ান ডলার) থেকে বিভিন্ন কারেন্সির রেট দেখাবে।
    """
    print("\n[3.1] মুদ্রা বিনিময় হার — Currency Exchange Rates\n")

    if not REQUESTS_AVAILABLE:
        print("   → requests না থাকায় স্কিপ করা হলো")
        return

    try:
        # ফ্রি API — Frankfurter (ইউরোপীয়ান সেন্ট্রাল ব্যাংকের ডেটা)
        url = "https://api.frankfurter.app/latest?from=CAD"
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            print(f"   ✗ API কল ব্যর্থ (স্ট্যাটাস: {response.status_code})")
            return

        data = response.json()
        base_currency = data.get("base", "CAD")
        rates = data.get("rates", {})
        date = data.get("date", "N/A")

        print(f"   বেস কারেন্সি: {base_currency}")
        print(f"   তারিখ: {date}")
        print(f"   মোট উপলব্ধ রেট: {len(rates)} টি")
        print()

        # গুরুত্বপূর্ণ কিছু কারেন্সি বাছাই করে দেখানো
        important_currencies = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "BDT": "Bangladeshi Taka",
            "MXN": "Mexican Peso",
        }

        print(f"   {'কারেন্সি':<10} {'নাম':<25} {'রেট (1 CAD =)':<15}")
        print(f"   {'-'*10} {'-'*25} {'-'*15}")
        for code, name in important_currencies.items():
            rate = rates.get(code)
            if rate:
                print(f"   {code:<10} {name:<25} {rate:<15.6f}")

        # কানাডিয়ান ডলার → কানাডিয়ান ডলার = ১
        print(f"   CAD (Canadian Dollar) কার্যত 1.000000")

        # যদি আপনি প্রতি USD-তে কত CAD জানতে চান:
        usd_rate = rates.get("USD")
        if usd_rate:
            print(f"\n   → 1 CAD = {usd_rate:.4f} USD")
            print(f"   → 1 USD = {1/usd_rate:.4f} CAD (বিপরীত)")

    except requests.exceptions.RequestException as e:
        print(f"   ✗ API কানেক্ট করতে ব্যর্থ: {e}")
    except json.JSONDecodeError:
        print("   ✗ JSON ডিকোড করতে ব্যর্থ")
    except Exception as e:
        print(f"   ✗ অজানা ত্রুটি: {e}")


scrape_currency_exchange_rates()
print("\n" + "=" * 60)


# ============================================================
# PART 4: ফাইন্যান্স উদাহরণ ২ — চাকরির পোস্টিং (Job Postings)
# ============================================================
# আমরা একটি ফ্রি জব সার্চ API (Adzuna বা JSearch) ব্যবহার করব
# কিন্তু API কী না থাকলে, আমরা একটি ডেমো JSON থেকে দেখাব
# এবং বাস্তব API কলের কোডও লিখব

def scrape_job_postings_demo():
    """
    চাকরির পোস্টিং সংগ্রহের জন্য ডেমো ফাংশন।
    রিয়েল API কী না থাকলে লোকাল JSON ডেটা ব্যবহার করে
    ফাইন্যান্স রিলেটেড জব দেখায়।
    """
    print("\n[4.1] চাকরির পোস্টিং স্ক্র্যাপার ডেমো\n")

    # লোকাল ডেমো ডেটা — ফাইন্যান্স জব পোস্টিং
    demo_jobs = [
        {"title": "Financial Analyst", "company": "RBC Royal Bank",
         "location": "Toronto, ON", "salary": "$65K-$85K",
         "description": "মাসিক ফাইন্যান্সিয়াল রিপোর্ট তৈরি ও বিশ্লেষণ। এক্সেল ও পাইথন দক্ষতা প্রয়োজন।"},
        {"title": "Data Analyst - Finance", "company": "TD Bank",
         "location": "Toronto, ON", "salary": "$70K-$90K",
         "description": "ফাইন্যান্সিয়াল ডেটা অ্যানালাইসিস, ড্যাশবোর্ড তৈরি, SQL ও পাইথন।"},
        {"title": "Junior Risk Analyst", "company": "BMO Financial Group",
         "location": "Montreal, QC", "salary": "$55K-$75K",
         "description": "ক্রেডিট রিস্ক অ্যানালাইসিস, মডেল ভ্যালিডেশন, স্ট্যাটিস্টিক্যাল পদ্ধতি।"},
        {"title": "Investment Banking Analyst", "company": "CIBC World Markets",
         "location": "Toronto, ON", "salary": "$80K-$120K",
         "description": "M&A ডিল সাপোর্ট, ফাইন্যান্সিয়াল মডেলিং, পিচ বুক তৈরি।"},
        {"title": "Portfolio Analyst", "company": "Manulife",
         "location": "Waterloo, ON", "salary": "$60K-$80K",
         "description": "পোর্টফোলিও পারফরম্যান্স মেজারমেন্ট, রিপোর্টিং ও অ্যাট্রিবিউশন অ্যানালাইসিস।"},
    ]

    print(f"   {'#'}  {'পজিশন':<35} {'কোম্পানি':<25} {'লোকেশন':<22} {'স্যালারি':<15}")
    print(f"   {'-'*2} {'-'*35} {'-'*25} {'-'*22} {'-'*15}")
    for i, job in enumerate(demo_jobs, 1):
        print(f"   {i:<2} {job['title']:<35} {job['company']:<25} "
              f"{job['location']:<22} {job['salary']:<15}")

    print("\n   → উপরে {len(demo_jobs)} টি ডেমো জব পোস্টিং দেখানো হয়েছে")
    print("   → বাস্তব API দিয়ে কাজ করতে নিচের ফাংশন ব্যবহার করুন")

    # ---------- রিয়েল API কলের জন্য কোড (কমেন্টেড) ----------
    # Adzuna API (ফ্রি, রেজিস্ট্রেশন প্রয়োজন)
    # URL: https://api.adzuna.com/v1/api/jobs/ca/search/1
    # প্যারামিটার: app_id, app_key, what="finance", where="Toronto"
    """
    ADZUNA_APP_ID = "YOUR_APP_ID"
    ADZUNA_APP_KEY = "YOUR_APP_KEY"

    url = "https://api.adzuna.com/v1/api/jobs/ca/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": "financial analyst",
        "where": "Toronto",
        "max_days_old": 30,
    }
    response = requests.get(url, params=params, timeout=15)
    data = response.json()
    for job in data.get("results", []):
        print(f"{job['title']} — {job['company']['display_name']}")
    """


scrape_job_postings_demo()
print("\n" + "=" * 60)


# ============================================================
# PART 5: BeautifulSoup দিয়ে HTML পার্স করার ডেমো
# ============================================================
def beautifulsoup_demo():
    """
    BeautifulSoup ব্যবহার করে HTML পার্স করার ডেমো।
    অনলাইনে না গিয়ে আমরা একটি HTML স্ট্রিং পার্স করব।
    """
    print("\n[5.1] BeautifulSoup দিয়ে HTML পার্সিং ডেমো\n")

    if not BS_AVAILABLE:
        print("   → BeautifulSoup না থাকায় স্কিপ করা হলো")
        print("   → তবে নিচের কোডটি বুঝে রাখুন:")
        print()

    # ডেমো HTML — একটি স্টক মার্কেট টেবিল
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Stock Prices</title></head>
    <body>
        <h1>বাজার সারসংক্ষেপ</h1>
        <table class="stock-table">
            <tr>
                <th>Symbol</th><th>Company</th><th>Price</th><th>Change%</th>
            </tr>
            <tr>
                <td>RY</td><td>Royal Bank of Canada</td><td>162.45</td><td class="up">+1.23</td>
            </tr>
            <tr>
                <td>TD</td><td>Toronto-Dominion Bank</td><td>85.67</td><td class="up">+0.87</td>
            </tr>
            <tr>
                <td>BNS</td><td>Bank of Nova Scotia</td><td>73.21</td><td class="down">-0.45</td>
            </tr>
            <tr>
                <td>CNQ</td><td>Canadian Natural Resources</td><td>98.34</td><td class="down">-1.12</td>
            </tr>
        </table>
        <p>সর্বশেষ আপডেট: 22 জুন 2026</p>
    </body>
    </html>
    """

    if BS_AVAILABLE:
        soup = BeautifulSoup(html_content, "html.parser")

        # টাইটেল দেখা
        title = soup.title.text
        print(f"   পেজ টাইটেল: {title}")

        # টেবিল থেকে ডেটা বের করা
        rows = soup.select("table.stock-table tr")
        print(f"\n   {'Symbol':<8} {'Company':<35} {'Price':<10} {'Change%':<10}")
        print(f"   {'-'*8} {'-'*35} {'-'*10} {'-'*10}")

        for row in rows[1:]:  # হেডার বাদ
            cols = row.find_all("td")
            if len(cols) >= 4:
                symbol = cols[0].text.strip()
                company = cols[1].text.strip()
                price = cols[2].text.strip()
                change = cols[3].text.strip()
                print(f"   {symbol:<8} {company:<35} {price:<10} {change:<10}")

        print("\n   → BeautifulSoup দিয়ে HTML থেকে সহজেই ডেটা বের করা যায়")
    else:
        print("   BeautifulSoup না থাকায় HTML পার্স করা সম্ভব নয়।")
        print("   তবে, নিচের কোডটি দেখুন — এটি BeautifulSoup দিয়ে HTML পার্স করে:\n")
        print("""
   from bs4 import BeautifulSoup
   soup = BeautifulSoup(html_content, 'html.parser')
   rows = soup.select('table.stock-table tr')
   for row in rows:
       cols = row.find_all('td')
       print([c.text for c in cols])
        """)


beautifulsoup_demo()
print("\n" + "=" * 60)


# ============================================================
# PART 6: API ডেটা সেভ করা JSON ফাইলে
# ============================================================
def save_data_to_json():
    """
    API থেকে পাওয়া ডেটা JSON ফাইলে সেভ করার উদাহরণ।
    """
    print("\n[6.1] ডেটা JSON ফাইলে সেভ করা\n")

    if not REQUESTS_AVAILABLE:
        print("   → requests না থাকায় স্কিপ করা হলো")
        return

    try:
        # CAD থেকে কিছু কারেন্সির রেট নিয়ে আসি
        url = "https://api.frankfurter.app/latest?from=CAD&to=USD,EUR,GBP,JPY,AUD,INR,BDT"
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            print(f"   ✗ API ব্যর্থ: {response.status_code}")
            return

        data = response.json()

        # ফাইলে সেভ করা
        import os
        from datetime import datetime

        # ~/LearningPath/Python/week01_basics/data/ ফোল্ডারে সেভ
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(save_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exchange_rates_{timestamp}.json"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"   ✓ ডেটা সেভ করা হয়েছে: {filepath}")
        print(f"   ✓ ফাইল সাইজ: {os.path.getsize(filepath):,} বাইট")

    except Exception as e:
        print(f"   ✗ ত্রুটি: {e}")


save_data_to_json()
print("\n" + "=" * 60)


# ============================================================
# PART 7: গুরুত্বপূর্ণ শব্দকোষ (Bangla Glossary)
# ============================================================
def glossary():
    """
    ওয়েব স্ক্র্যাপিং সম্পর্কিত গুরুত্বপূর্ণ ইংরেজি → বাংলা শব্দকোষ।
    """
    print("\n[7.1] গুরুত্বপূর্ণ শব্দকোষ — Glossary\n")

    terms = [
        ("Web Scraping", "ওয়েব স্ক্র্যাপিং", "ওয়েবসাইট থেকে স্বয়ংক্রিয়ভাবে ডেটা সংগ্রহ"),
        ("HTTP Request", "HTTP রিকুয়েস্ট", "সার্ভারের কাছে ডেটা চাওয়া"),
        ("HTTP Response", "HTTP রেসপন্স", "সার্ভার থেকে পাওয়া উত্তর"),
        ("Status Code", "স্ট্যাটাস কোড", "রিকুয়েস্টের ফলাফল নির্দেশক সংখ্যা (200=সফল, 404=পাওয়া যায়নি)"),
        ("API", "API (এপিআই)", "অ্যাপ্লিকেশন প্রোগ্রামিং ইন্টারফেস — ডেটা আদান-প্রদানের মাধ্যম"),
        ("JSON", "JSON (জেসন)", "ডেটা বিন্যাস — JavaScript Object Notation"),
        ("Parser", "পার্সার", "HTML বা XML কে বিশ্লেষণ করে ডেটা বের করার টুল"),
        ("Endpoint", "এন্ডপয়েন্ট", "API-র নির্দিষ্ট URL ঠিকানা"),
        ("Rate Limit", "রেট লিমিট", "নির্দিষ্ট সময়ে কতগুলো রিকুয়েস্ট পাঠানো যাবে"),
        ("User-Agent", "ইউজার-এজেন্ট", "ব্রাউজার বা ক্লায়েন্ট পরিচিতি হেডার"),
    ]

    print(f"   {'ইংরেজি':<20} {'বাংলা':<20} {'ব্যাখ্যা':<50}")
    print(f"   {'-'*20} {'-'*20} {'-'*50}")
    for en, bn, desc in terms:
        print(f"   {en:<20} {bn:<20} {desc:<50}")


glossary()
print("\n" + "=" * 60)


# ============================================================
# PART 8: প্র্যাকটিস এক্সারসাইজ
# ============================================================
def practice_exercises():
    """
    নিজে করার জন্য কিছু এক্সারসাইজ।
    """
    print("\n[8.1] প্র্যাকটিস এক্সারসাইজ — নিজে করুন!\n")

    exercises = [
        "১. https://api.frankfurter.app/latest?from=USD  — থেকে সব কারেন্সির রেট বের করুন",
        "২. আপনার নিজের একটি API কী দিয়ে Adzuna থেকে ফাইন্যান্স জব সার্চ করুন",
        "৩. Yahoo Finance (yfinance) দিয়ে রিয়েল-টাইম স্টক প্রাইস সংগ্রহ করুন",
        "৪. JSON ফাইল থেকে কারেন্সি রেট লোড করে কনভার্টার তৈরি করুন",
        "৫. একটি ওয়েবসাইট থেকে টেবিল ডেটা BeautifulSoup দিয়ে স্ক্র্যাপ করুন",
    ]

    for ex in exercises:
        print(f"   {ex}")

    print()
    print("   💡 টিপ: প্রতিদিন ১টি করে এক্সারসাইজ করার চেষ্টা করুন!")


practice_exercises()
print("\n" + "=" * 60)

print("\n✅ Day 17 শেষ! তুমি এখন ওয়েব স্ক্র্যাপিং বেসিক শিখেছ।")
print("   পরবর্তী: Day 18 — স্টক পোর্টফোলিও অ্যানালাইজার প্রজেক্ট!\n")