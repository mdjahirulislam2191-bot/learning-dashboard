"""
Day 16: APIs & JSON — লাইভ ডেটা ফেচ
=========================================
বিষয়: Requests লাইব্রেরি, JSON পার্সিং, API কী
লেখক: Jahirul Islam (Finance Grad, Canada)
উদ্দেশ্য: ফ্রি API ব্যবহার করে লাইভ ফাইন্যান্স ডেটা ফেচ করা

প্রয়োজনীয় লাইব্রেরি:
  pip install requests pandas
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time

# ============================================================
# ১. JSON কী এবং কেন?
# ============================================================
print("=" * 65)
print("📦 JSON ডেটা ফরম্যাট বোঝা")
print("=" * 65)

# JSON দেখতে কেমন — একটি উদাহরণ
sample_json = """
{
    "name": "Jahirul Islam",
    "age": 28,
    "city": "Toronto",
    "skills": ["Python", "SQL", "Excel"],
    "finance": {
        "income": 50000,
        "expenses": 35000,
        "savings_rate": 30.0
    },
    "is_employed": true,
    "portfolio": null
}
"""

print("\n🔍 JSON ডেটার স্ট্রাকচার:")
print(sample_json)

# JSON পার্স করা
data = json.loads(sample_json)
print(f"\n✅ JSON পার্স করা হয়েছে।")
print(f"   নাম: {data['name']}")
print(f"   শহর: {data['city']}")
print(f"   দক্ষতা: {', '.join(data['skills'])}")
print(f"   সেভিংস রেট: {data['finance']['savings_rate']}%")
print(f"   কর্মরত: {data['is_employed']}")
print()


# ============================================================
# ২. API থেকে ডেটা ফেচ — CoinDesk (Bitcoin Price)
# ============================================================
print("=" * 65)
print("💰 বিটকয়েন প্রাইস — CoinDesk API")
print("=" * 65)

# CoinDesk API — ফ্রি, কোন API কী লাগে না
BITCOIN_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

try:
    print("\n📡 বিটকয়েন প্রাইস ফেচ করা হচ্ছে...")
    response = requests.get(BITCOIN_URL, timeout=10)
    
    if response.status_code == 200:
        bitcoin_data = response.json()
        
        print(f"\n✅ স্ট্যাটাস: {response.status_code}")
        print(f"📅 আপডেট: {bitcoin_data['time']['updated']}")
        print(f"\n💲 বিটকয়েন প্রাইস:")
        
        for currency, info in bitcoin_data['bpi'].items():
            print(f"   {currency:5s}: {info['symbol']}{info['rate']}")
        
        # বিটকয়েন প্রাইস কাঠামো দেখানো
        print(f"\n🔍 JSON স্ট্রাকচার (সংক্ষিপ্ত):")
        print(json.dumps(bitcoin_data, indent=2)[:500])
    else:
        print(f"❌ API কল ব্যর্থ: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ ইন্টারনেট কানেকশন নেই!")
except requests.exceptions.Timeout:
    print("❌ টাইমআউট! API রেসপন্স দিচ্ছে না।")
except Exception as e:
    print(f"❌ এরর: {e}")

print()


# ============================================================
# ৩. ফ্রি স্টক প্রাইস API — Yahoo Finance (অল্টারনেটিভ)
# ============================================================
print("=" * 65)
print("📈 স্টক প্রাইস — Yahoo Finance (Unofficial)")
print("=" * 65)

# Yahoo Finance ফ্রি API (unofficial, no API key needed)
# এই API টা শুধু শিক্ষামূলক ব্যবহারের জন্য

STOCK_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=1d&interval=1d"

for symbol in STOCK_SYMBOLS[:2]:  # শুধু ২টি স্টক (ডেমোর জন্য)
    try:
        print(f"\n📡 {symbol} প্রাইস ফেচ করা হচ্ছে...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(YAHOO_URL.format(symbol), headers=headers, timeout=10)
        
        if response.status_code == 200:
            stock_data = response.json()
            
            try:
                meta = stock_data['chart']['result'][0]['meta']
                price = meta.get('regularMarketPrice', 'N/A')
                prev_close = meta.get('previousClose', 'N/A')
                change = (price - prev_close) if (price != 'N/A' and prev_close != 'N/A') else 0
                change_pct = (change / prev_close * 100) if prev_close != 'N/A' and prev_close != 0 else 0
                
                arrow = "🟢" if change >= 0 else "🔴"
                print(f"   {symbol:6s}: ${price:.2f} | আগের ক্লোজ: ${prev_close:.2f}")
                print(f"   {arrow} পরিবর্তন: ${change:+.2f} ({change_pct:+.2f}%)")
            except (KeyError, TypeError, IndexError):
                print(f"   {symbol}: ডেটা পার্স করা যায়নি।")
        else:
            print(f"   {symbol}: API কল ব্যর্থ ({response.status_code})")
            
    except Exception as e:
        print(f"   {symbol}: এরর — {e}")

print()


# ============================================================
# ৪. এক্সচেঞ্জ রেট API — Frankfurter (ফ্রি)
# ============================================================
print("=" * 65)
print("💱 এক্সচেঞ্জ রেট — Frankfurter API")
print("=" * 65)

# Frankfurter API — ফ্রি, কোন API কী লাগে না
FX_URL = "https://api.frankfurter.app/latest?from=USD"

try:
    print("\n📡 এক্সচেঞ্জ রেট ফেচ করা হচ্ছে (USD →其他国家)...")
    response = requests.get(FX_URL, timeout=10)
    
    if response.status_code == 200:
        fx_data = response.json()
        
        print(f"\n✅ স্ট্যাটাস: {response.status_code}")
        print(f"📅 তারিখ: {fx_data['date']}")
        print(f"💰 বেস কারেন্সি: {fx_data['base']}")
        
        # বাংলাদেশী টাকা (BDT) খোঁজা — Frankfurter এ BDT নাও থাকতে পারে
        rates = fx_data['rates']
        
        # কিছু গুরুত্বপূর্ণ কারেন্সি দেখানো
        important_currencies = ['EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'INR', 'CNY']
        print(f"\n📊 গুরুত্বপূর্ণ এক্সচেঞ্জ রেট (1 USD =):")
        for curr in important_currencies:
            if curr in rates:
                print(f"   {curr:5s}: {rates[curr]:.4f}")
        
        # BDT আছে কিনা চেক
        if 'BDT' in rates:
            print(f"\n   🇧🇩 BDT (বাংলাদেশী টাকা): {rates['BDT']:.2f}")
        else:
            # BDT নাই, তাই INR দিয়ে estimate
            if 'INR' in rates:
                estimated_bdt = rates['INR'] * 1.3  # মোটামুটি estimate: 1 INR ≈ 1.3 BDT
                print(f"\n   🇧🇩 BDT (estimated): ৳{estimated_bdt:.2f} (INR {rates['INR']:.2f} × 1.3)")
    else:
        print(f"❌ API কল ব্যর্থ: {response.status_code}")
        
except Exception as e:
    print(f"❌ এরর: {e}")

print()


# ============================================================
# ৫. কাস্টম API ফাংশন — পুনরায় ব্যবহারযোগ্য
# ============================================================
print("=" * 65)
print("⚙️ কাস্টম API ফাংশন তৈরি")
print("=" * 65)

def fetch_crypto_price(crypto="bitcoin", currency="usd"):
    """
    CoinGecko API থেকে ক্রিপ্টো প্রাইস ফেচ করে।
    
    Parameters:
        crypto (str): ক্রিপ্টোকারেন্সির নাম (bitcoin, ethereum, etc.)
        currency (str): কারেন্সি (usd, cad, bdt, etc.)
    
    Returns:
        dict: প্রাইস ডেটা অথবা None (যদি ব্যর্থ হয়)
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
    
    try:
        print(f"\n📡 {crypto.title()} প্রাইস ফেচ করা হচ্ছে ({currency.upper()})...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if crypto in data and currency in data[crypto]:
                price = data[crypto][currency]
                print(f"✅ {crypto.title()} মূল্য: {currency.upper()} {price:,.2f}")
                
                if currency == 'usd':
                    # CAD estimate
                    print(f"   Canadian Dollar (approx): CAD ${price * 1.36:,.2f}")
                
                return data
            else:
                print(f"❌ ডেটা ফরম্যাটে {crypto}/{currency} পাওয়া যায়নি।")
                print(f"   রেসপন্স: {data}")
                return None
        else:
            print(f"❌ HTTP {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ ইন্টারনেট কানেকশন নেই!")
        return None
    except requests.exceptions.Timeout:
        print("❌ টাইমআউট!")
        return None
    except Exception as e:
        print(f"❌ এরর: {e}")
        return None


# ফাংশন টেস্ট
print("\n🔧 ফাংশন টেস্ট — Bitcoin:")
btc_price = fetch_crypto_price("bitcoin", "usd")

print("\n🔧 ফাংশন টেস্ট — Ethereum:")
eth_price = fetch_crypto_price("ethereum", "usd")

print("\n🔧 ফাংশন টেস্ট — Solana:")
sol_price = fetch_crypto_price("solana", "usd")

print()


# ============================================================
# ৬. একাধিক ক্রিপ্টো একসাথে
# ============================================================
print("=" * 65)
print("📊 ক্রিপ্টো পোর্টফোলিও ভিউ — একাধিক কয়েন")
print("=" * 65)

def fetch_multiple_crypto_prices(cryptos=None, currency="usd"):
    """
    একাধিক ক্রিপ্টোকারেন্সির প্রাইস একসাথে ফেচ করে।
    
    Parameters:
        cryptos (list): ক্রিপ্টোকারেন্সির লিস্ট
        currency (str): কারেন্সি
    
    Returns:
        pd.DataFrame: প্রাইস ডেটা ফ্রেম
    """
    if cryptos is None:
        cryptos = ["bitcoin", "ethereum", "solana", "cardano", "polkadot", "ripple"]
    
    names_bn = {
        "bitcoin": "বিটকয়েন",
        "ethereum": "ইথেরিয়াম",
        "solana": "সোলানা",
        "cardano": "কার্ডানো",
        "polkadot": "পলকাডট",
        "ripple": "রিপল"
    }
    
    cryptos_str = ",".join(cryptos)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cryptos_str}&vs_currencies={currency}"
    
    try:
        print(f"\n📡 একাধিক ক্রিপ্টো প্রাইস ফেচ করা হচ্ছে...")
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            results = []
            for crypto in cryptos:
                if crypto in data and currency in data[crypto]:
                    price = data[crypto][currency]
                    bn_name = names_bn.get(crypto, crypto.title())
                    results.append({
                        'ক্রিপ্টো': bn_name,
                        'সিম্বল': crypto.upper()[:4],
                        f'মূল্য ({currency.upper()})': price,
                        'ক্যাপ ক্লাস': 'Large' if price > 100 else ('Mid' if price > 1 else 'Small')
                    })
            
            df = pd.DataFrame(results)
            print(f"\n✅ মোট {len(df)}টি ক্রিপ্টোর ডেটা:")
            print(df.to_string(index=False))
            
            # একটি ছোট ভিজুয়ালাইজেশন (টেক্সট)
            print(f"\n📊 মূল্য তুলনা (বার চার্ট — টেক্সট):")
            max_price = df[f'মূল্য ({currency.upper()})'].max()
            for _, row in df.iterrows():
                bar_len = int((row[f'মূল্য ({currency.upper()})'] / max_price) * 30)
                bar = '█' * bar_len
                print(f"  {row['ক্রিপ্টো']:10s}: {bar} ${row[f'মূল্য ({currency.upper()})']:>10,.2f}")
            
            return df
        else:
            print(f"❌ HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ এরর: {e}")
        return None


# ফাংশন টেস্ট
portfolio_df = fetch_multiple_crypto_prices()
print()


# ============================================================
# ৭. API কী ব্যবহার — নিরাপদ পদ্ধতি
# ============================================================
print("=" * 65)
print("🔑 API কী — নিরাপদ ব্যবহার")
print("=" * 65)

print("""
🔐 API কী ব্যবহারের নিয়ম:
  1. API কী কখনোই কোডে হার্ডকোড করবেন না!
  2. .env ফাইল বা environment variables ব্যবহার করুন।
  3. .gitignore এ API কী ফাইল যোগ করুন।

✅ সঠিক পদ্ধতি:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

❌ ভুল পদ্ধতি (কখনোই করবেন না):
    API_KEY = "sk-1234567890abcdef"  # ❌ এইটা বিপজ্জনক!

📋 ফ্রি ফাইন্যান্স API লিস্ট:
  • CoinGecko     : https://www.coingecko.com/en/api (ক্রিপ্টো)
  • Alpha Vantage : https://www.alphavantage.co (স্টক)
  • Twelve Data   : https://twelvedata.com (স্টক, ফরেক্স)
  • Yahoo Finance : yfinance Python লাইব্রেরি (unofficial)
  • FRED          : https://fred.stlouisfed.org (ম্যাক্রো ইকোনমিক)
  • OpenExchangeRates: https://openexchangerates.org (ফরেক্স)
""")

# .env ফাইল তৈরি (শুধু টেমপ্লেট)
env_template = """# API কী কনফিগারেশন
# আপনার API কী এখানে সেট করুন (প্রাইভেট রাখুন!)
ALPHA_VANTAGE_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here
"""

with open('.env.template', 'w') as f:
    f.write(env_template)
print("✅ .env.template ফাইল তৈরি করা হয়েছে।")


# ============================================================
# ৮. সময় সিরিজ ডেটা — Alpha Vantage (যদি API কী থাকে)
# ============================================================
print("\n" + "=" * 65)
print("📈 সময় সিরিজ ডেটা — Alpha Vantage (বোনাস)")
print("=" * 65)

def demo_alpha_vantage():
    """
    Alpha Vantage API ডেমো।
    API কী না থাকলে ডেমো ডেটা দেখায়।
    """
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
        
        if API_KEY == 'demo' or API_KEY == 'your_key_here':
            print("\n⚠️  Alpha Vantage API কী সেট করা নেই।")
            print("   ফ্রিতে সাইনআপ করুন: https://www.alphavantage.co/support/#api-key")
            print()
            
            # ডেমো ডেটা দেখানো
            demo_data = {
                'তারিখ': pd.date_range(start='2024-06-01', periods=7, freq='D'),
                'ওপেন': [150.00, 152.30, 151.10, 153.45, 154.00, 153.80, 155.20],
                'হাই': [153.00, 154.50, 153.20, 155.00, 156.30, 155.40, 156.80],
                'লো': [148.80, 151.00, 150.50, 152.00, 153.10, 152.90, 154.50],
                'ক্লোজ': [152.30, 151.10, 153.45, 154.00, 153.80, 155.20, 156.50],
                'ভলিউম': [50000, 55000, 48000, 60000, 62000, 58000, 65000]
            }
            demo_df = pd.DataFrame(demo_data)
            print("📊 ডেমো স্টক ডেটা (AAPL — সিমুলেটেড):")
            print(demo_df.to_string(index=False))
            print()
            print("💡 টিপ: API কী সেট করে বাস্তব ডেটা ফেচ করুন!")
            return demo_df
        else:
            # API কী থাকলে বাস্তব ডেটা ফেচ
            symbol = 'AAPL'
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'Time Series (Daily)' in data:
                    ts = data['Time Series (Daily)']
                    records = []
                    for date, values in list(ts.items())[:10]:
                        records.append({
                            'তারিখ': date,
                            'ওপেন': float(values['1. open']),
                            'হাই': float(values['2. high']),
                            'লো': float(values['3. low']),
                            'ক্লোজ': float(values['4. close']),
                            'ভলিউম': int(values['5. volume'])
                        })
                    df = pd.DataFrame(records)
                    print(f"\n✅ {symbol} — লাইভ ডেটা:")
                    print(df.to_string(index=False))
                    return df
                else:
                    print(f"❌ API রেসপন্সে ডেটা নেই: {data.get('Note', '')[:100]}")
            else:
                print(f"❌ HTTP {response.status_code}")
                
    except ImportError:
        print("❌ python-dotenv লাইব্রেরি ইনস্টল নেই।")
        print("   ইনস্টল করুন: pip install python-dotenv")
    except Exception as e:
        print(f"❌ এরর: {e}")
    
    return None

demo_alpha_vantage()
print()


# ============================================================
# ৯. JSON ডেটা সেভ ও রিলোড
# ============================================================
print("=" * 65)
print("💾 JSON ডেটা সেভ ও রিলোড")
print("=" * 65)

# ফেচ করা ডেটা JSON ফাইলে সেভ
if btc_price:
    with open('day16_crypto_data.json', 'w') as f:
        json.dump(btc_price, f, indent=2)
    print("✅ ক্রিপ্টো ডেটা সেভ করা হয়েছে: day16_crypto_data.json")

# JSON ফাইল রিলোড
with open('day16_crypto_data.json', 'r') as f:
    loaded_data = json.load(f)
print(f"✅ JSON ফাইল রিলোড করা হয়েছে: {loaded_data}")
print()


# ============================================================
# প্র্যাকটিস টাস্ক (Practice Tasks)
# ============================================================
print("=" * 65)
print("📝 প্র্যাকটিস টাস্ক (Day 16)")
print("=" * 65)
print("""
১. CoinGecko API ব্যবহার করে টপ ৫টি ক্রিপ্টোকারেন্সির প্রাইস ফেচ করুন।
২. Frankfurter API থেকে USD→CAD, USD→EUR, USD→GBP এর দর বের করুন।
৩. নিজের Portfolio (যেমন: 1 BTC, 5 ETH, 100 SOL) এর মোট ভ্যালু বের করুন।
৪. Alpha Vantage-এ ফ্রি API কী নিন এবং আপনার পছন্দের স্টকের প্রাইস ফেচ করুন।
৫. API কলের ফলাফল JSON ফাইলে সেভ করে পরে সেখান থেকে রিলোড করার সিস্টেম তৈরি করুন।
""")