#!/usr/bin/env python3
"""
Day 19: Portfolio Polish — পেশাদার কোড স্ট্রাকচার
======================================================
Day 18-এর প্রজেক্টকে পলিশ করা:
  1. এরর হ্যান্ডলিং (কাস্টম এক্সেপশন)
  2. ডকস্ট্রিং (NumPy স্টাইল, বাংলা ও ইংরেজি)
  3. ফাংশন সংগঠন (একক দায়িত্ব — SRP)
  4. CSV আউটপুট
  5. টাইপ হিন্টিং
  6. লগিং
  7. কনফিগারেশন ম্যানেজমেন্ট

Finance Graduate (Canada) — Jahirul Islam
"""

# ============================================================
# ইম্পোর্ট
# ============================================================
import csv
import json
import logging
import os
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

# প্রয়োজনীয় গ্রন্থাগার চেক (Try/Except দিয়ে)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


# ============================================================
# লগিং কনফিগারেশন (লগিং সিস্টেম)
# ============================================================
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    লগিং সিস্টেম সেটআপ করে।

    Parameters
    ----------
    log_level : str
        লগ লেভেল — "DEBUG", "INFO", "WARNING", "ERROR"

    Returns
    -------
    logging.Logger
        কনফিগারড লগার অবজেক্ট
    """
    logger = logging.getLogger("PortfolioAnalyzer")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # কনসোল হ্যান্ডলার
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# গ্লোবাল লগার
logger = setup_logging()


# ============================================================
# কাস্টম এক্সেপশন ক্লাস (Custom Exception Hierarchy)
# ============================================================
class PortfolioError(Exception):
    """পোর্টফোলিও সম্পর্কিত সব ত্রুটির বেস ক্লাস।"""
    pass


class PortfolioLoadError(PortfolioError):
    """পোর্টফোলিও ফাইল লোড করতে ব্যর্থ হলে।"""
    pass


class PriceFetchError(PortfolioError):
    """স্টক প্রাইস ফেচ করতে ব্যর্থ হলে।"""
    pass


class DataValidationError(PortfolioError):
    """ডেটা ভ্যালিডেশন ব্যর্থ হলে।"""
    pass


class PlottingError(PortfolioError):
    """গ্রাফ তৈরি করতে ব্যর্থ হলে।"""
    pass


# ============================================================
# ডেটাক্লাস — আধুনিক Python ডেটা মডেল
# ============================================================
@dataclass
class StockHolding:
    """
    একটি স্টক হোল্ডিংয়ের ডেটা মডেল।

    Attributes
    ----------
    ticker : str
        স্টক টিকার সিম্বল (যেমন: RY.TO)
    name : str
        কোম্পানির নাম
    shares : int
        শেয়ারের সংখ্যা
    buy_price : float
        প্রতি শেয়ারের ক্রয় মূল্য (CAD)
    """
    ticker: str
    name: str
    shares: int
    buy_price: float

    @property
    def cost_basis(self) -> float:
        """মোট বিনিয়োগের পরিমাণ (শেয়ার × ক্রয় মূল্য)"""
        return self.shares * self.buy_price


@dataclass
class Portfolio:
    """
    সম্পূর্ণ পোর্টফোলিওর ডেটা মডেল।

    Attributes
    ----------
    stocks : List[StockHolding]
        স্টক হোল্ডিংয়ের তালিকা
    cash : float
        নগদ ব্যালেন্স (CAD)
    investor : str
        বিনিয়োগকারীর নাম
    currency : str
        মুদ্রার একক (ডিফল্ট: CAD)
    """
    stocks: List[StockHolding]
    cash: float = 0.0
    investor: str = "Jahirul Islam"
    currency: str = "CAD"
    created: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def total_invested(self) -> float:
        """মোট বিনিয়োগ (স্টক + নগদ)"""
        return sum(s.cost_basis for s in self.stocks) + self.cash

    @property
    def stock_count(self) -> int:
        """পোর্টফোলিওতে মোট স্টকের সংখ্যা"""
        return len(self.stocks)


@dataclass
class StockPerformance:
    """
    একটি স্টকের পারফরম্যান্স ডেটা।

    Attributes
    ----------
    ticker : str
        স্টক টিকার
    shares : int
        শেয়ার সংখ্যা
    buy_price : float
        ক্রয় মূল্য
    current_price : float
        বর্তমান মূল্য
    cost : float
        মোট খরচ
    value : float
        বর্তমান মূল্য (মোট)
    return_pct : float
        রিটার্ন শতাংশ
    return_dollar : float
        রিটার্ন ডলারে
    """
    ticker: str
    shares: int
    buy_price: float
    current_price: float
    cost: float
    value: float
    return_pct: float
    return_dollar: float


# ============================================================
# কনফিগারেশন ম্যানেজার
# ============================================================
class Config:
    """
    অ্যাপ্লিকেশন কনফিগারেশন।
    সব সেটিংস এক জায়গায় রাখা হয়েছে — maintainability বাড়ে।
    """

    # ফাইল পাথ
    SCRIPT_DIR = Path(__file__).parent.resolve()
    DATA_DIR = SCRIPT_DIR / "data"
    OUTPUT_DIR = SCRIPT_DIR / "output"

    # আউটপুট ফাইল
    PORTFOLIO_CSV = DATA_DIR / "portfolio.csv"
    PORTFOLIO_JSON = DATA_DIR / "portfolio.json"
    PERFORMANCE_CSV = OUTPUT_DIR / "performance_report.csv"
    PERFORMANCE_PLOT = OUTPUT_DIR / "portfolio_performance.png"
    REPORT_TXT = OUTPUT_DIR / "portfolio_report.txt"

    # API সেটিংস
    PRICE_PERIOD = "6mo"
    REQUEST_TIMEOUT = 15
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # সিমুলেশন সেটিংস
    RANDOM_SEED = 42

    # প্লট সেটিংস
    PLOT_DPI = 150
    PLOT_FIGSIZE = (14, 10)

    @classmethod
    def ensure_dirs(cls):
        """প্রয়োজনীয় ডিরেক্টরি তৈরি করে"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# ইউটিলিটি ফাংশন
# ============================================================
def validate_price(price: float, ticker: str) -> bool:
    """
    স্টক প্রাইস ভ্যালিডেশন।

    Parameters
    ----------
    price : float
        ভ্যালিডেট করার জন্য প্রাইস
    ticker : str
        স্টক টিকার (লগিংয়ের জন্য)

    Returns
    -------
    bool
        True যদি প্রাইস ভ্যালিড হয়

    Raises
    ------
    DataValidationError
        মূল্য ০ বা নেগেটিভ হলে
    """
    if price <= 0:
        raise DataValidationError(
            f"{ticker}: দাম বৈধ নয় ({price})। দাম পজিটিভ হতে হবে।"
        )
    if price > 1_000_000:
        raise DataValidationError(
            f"{ticker}: দাম অবাস্তবিক ({price})। ১০ লক্ষ CAD এর বেশি? নিশ্চিত?"
        )
    return True


def format_currency(amount: float, currency: str = "CAD") -> str:
    """
    সংখ্যাকে মুদ্রা ফরম্যাটে রূপান্তর করে।

    Parameters
    ----------
    amount : float
        ফরম্যাট করার পরিমাণ
    currency : str
        মুদ্রার কোড

    Returns
    -------
    str
        ফরম্যাটেড স্ট্রিং (যেমন: "$1,234.56 CAD")
    """
    return f"${amount:,.2f} {currency}"


# ============================================================
# পোর্টফোলিও ম্যানেজার — পোর্টফোলিও লোড/সেভ/ক্রিয়েট
# ============================================================
class PortfolioManager:
    """
    পোর্টফোলিও ডেটা পরিচালনার জন্য ক্লাস।

    Methods
    -------
    create_default() -> Portfolio
        ডিফল্ট পোর্টফোলিও তৈরি
    save_csv(portfolio) -> Path
        CSV ফাইলে সেভ
    save_json(portfolio) -> Path
        JSON ফাইলে সেভ
    load_csv(path) -> Portfolio
        CSV ফাইল থেকে লোড
    display_summary(portfolio) -> None
        সারাংশ প্রদর্শন
    """

    @staticmethod
    def create_default() -> Portfolio:
        """
        কানাডিয়ান স্টকের ডিফল্ট পোর্টফোলিও তৈরি করে।

        Returns
        -------
        Portfolio
            স্যাম্পল ডেটাসহ পোর্টফোলিও
        """
        logger.info("ডিফল্ট পোর্টফোলিও তৈরি করা হচ্ছে...")

        stocks = [
            StockHolding("RY.TO", "Royal Bank of Canada", 50, 145.00),
            StockHolding("TD.TO", "Toronto-Dominion Bank", 75, 82.50),
            StockHolding("BNS.TO", "Bank of Nova Scotia", 40, 70.25),
            StockHolding("CNQ.TO", "Canadian Natural Resources", 30, 85.00),
            StockHolding("SHOP.TO", "Shopify Inc.", 15, 95.50),
            StockHolding("ENB.TO", "Enbridge Inc.", 60, 52.00),
            StockHolding("BMO.TO", "Bank of Montreal", 35, 128.00),
            StockHolding("CP.TO", "Canadian Pacific Kansas City", 20, 110.00),
        ]

        portfolio = Portfolio(
            stocks=stocks,
            cash=5000.00,
            investor="Jahirul Islam",
            currency="CAD",
        )

        logger.info(f"✓ পোর্টফোলিও তৈরি: {len(stocks)} টি স্টক, "
                    f"মোট বিনিয়োগ: {format_currency(portfolio.total_invested)}")
        return portfolio

    @staticmethod
    def save_csv(portfolio: Portfolio, filepath: Path) -> Path:
        """
        পোর্টফোলিও CSV ফাইলে সেভ করে।

        Parameters
        ----------
        portfolio : Portfolio
            সেভ করার পোর্টফোলিও
        filepath : Path
            CSV ফাইলের পাথ

        Returns
        -------
        Path
            সেভ করা ফাইলের পাথ
        """
        try:
            filepath.parent.mkdir(exist_ok=True)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "ticker", "name", "shares", "buy_price"
                ])
                writer.writeheader()
                for stock in portfolio.stocks:
                    writer.writerow({
                        "ticker": stock.ticker,
                        "name": stock.name,
                        "shares": stock.shares,
                        "buy_price": stock.buy_price,
                    })
            logger.info(f"✓ CSV সেভ করা হয়েছে: {filepath}")
            return filepath
        except (OSError, IOError) as e:
            raise PortfolioLoadError(f"CSV সেভ করতে ব্যর্থ: {e}")

    @staticmethod
    def save_json(portfolio: Portfolio, filepath: Path) -> Path:
        """
        পোর্টফোলিও JSON ফাইলে সেভ করে।

        Parameters
        ----------
        portfolio : Portfolio
            সেভ করার পোর্টফোলিও
        filepath : Path
            JSON ফাইলের পাথ

        Returns
        -------
        Path
            সেভ করা ফাইলের পাথ
        """
        try:
            filepath.parent.mkdir(exist_ok=True)
            data = {
                "stocks": [asdict(s) for s in portfolio.stocks],
                "cash": portfolio.cash,
                "investor": portfolio.investor,
                "currency": portfolio.currency,
                "created": portfolio.created,
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ JSON সেভ করা হয়েছে: {filepath}")
            return filepath
        except (OSError, IOError) as e:
            raise PortfolioLoadError(f"JSON সেভ করতে ব্যর্থ: {e}")

    @staticmethod
    def load_csv(filepath: Path) -> Portfolio:
        """
        CSV ফাইল থেকে পোর্টফোলিও লোড করে।

        Parameters
        ----------
        filepath : Path
            CSV ফাইলের পাথ

        Returns
        -------
        Portfolio
            লোডকৃত পোর্টফোলিও

        Raises
        ------
        PortfolioLoadError
            ফাইল না থাকলে বা পড়তে ব্যর্থ হলে
        """
        if not filepath.exists():
            raise PortfolioLoadError(f"ফাইল পাওয়া যায়নি: {filepath}")

        try:
            stocks = []
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        stock = StockHolding(
                            ticker=row["ticker"].strip(),
                            name=row["name"].strip(),
                            shares=int(row["shares"]),
                            buy_price=float(row["buy_price"]),
                        )
                        stocks.append(stock)
                    except (KeyError, ValueError) as e:
                        logger.warning(f"⚠ একটি সারি পড়তে ব্যর্থ: {row} — {e}")

            if not stocks:
                raise PortfolioLoadError("CSV ফাইলে কোনো বৈধ স্টক নেই")

            logger.info(f"✓ CSV থেকে লোড করা হয়েছে: {len(stocks)} টি স্টক")
            return Portfolio(stocks=stocks)

        except (OSError, IOError) as e:
            raise PortfolioLoadError(f"CSV পড়তে ব্যর্থ: {e}")

    @staticmethod
    def display_summary(portfolio: Portfolio) -> None:
        """
        পোর্টফোলিওর সারাংশ কনসোলে দেখায়।

        Parameters
        ----------
        portfolio : Portfolio
            প্রদর্শনের পোর্টফোলিও
        """
        print(f"\n   {'টিকার':<10} {'নাম':<35} {'শেয়ার':<8} {'ক্রয় মূল্য':<12} {'মোট খরচ':<12}")
        print(f"   {'-'*10} {'-'*35} {'-'*8} {'-'*12} {'-'*12}")
        for s in portfolio.stocks:
            print(f"   {s.ticker:<10} {s.name:<35} {s.shares:<8} ${s.buy_price:<10.2f} ${s.cost_basis:<10.2f}")
        print(f"   {'নগদ':<67} ${portfolio.cash:<10.2f}")
        print(f"   {'মোট':<67} ${portfolio.total_invested:<10.2f}")


# ============================================================
# প্রাইস ফেচার — স্টক প্রাইস সংগ্রহের জন্য
# ============================================================
class PriceFetcher(ABC):
    """
    স্টক প্রাইস ফেচিংয়ের জন্য অ্যাবস্ট্র্যাক্ট বেস ক্লাস।
    """

    @abstractmethod
    def fetch(self, tickers: List[str], period: str) -> Dict[str, pd.DataFrame]:
        """স্টক প্রাইস ফেচ করে — সাবক্লাসে ইমপ্লিমেন্ট করতে হবে"""
        pass


class YFinanceFetcher(PriceFetcher):
    """
    Yahoo Finance (yfinance) থেকে স্টক প্রাইস ফেচ করে।

    yfinance ইন্সটল না থাকলে SimulatedFetcher-এ ফলব্যাক করে।
    """

    def __init__(self):
        if not YFINANCE_AVAILABLE:
            logger.warning("yfinance পাওয়া যায়নি — SimulatedFetcher ব্যবহার করুন")

    def fetch(self, tickers: List[str], period: str = "6mo") -> Dict[str, pd.DataFrame]:
        """
        yfinance API থেকে স্টক ডেটা ডাউনলোড করে।

        Parameters
        ----------
        tickers : List[str]
            স্টক টিকার তালিকা
        period : str
            সময়সীমা (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)

        Returns
        -------
        Dict[str, pd.DataFrame]
            {ticker: DataFrame} ফরম্যাটে প্রাইস ডেটা

        Raises
        ------
        PriceFetchError
            API কল ব্যর্থ হলে
        """
        if not YFINANCE_AVAILABLE:
            raise PriceFetchError("yfinance ইন্সটল নেই")

        if not tickers:
            raise PriceFetchError("টিকার তালিকা খালি")

        logger.info(f"yfinance দিয়ে {len(tickers)} টি স্টকের ডেটা ডাউনলোড করা হচ্ছে...")

        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=180)

            data = yf.download(
                tickers,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                group_by="ticker",
                auto_adjust=True,
                progress=False,
            )

            # yfinance একাধিক টিকারের জন্য MultiIndex DataFrame দেয়
            # একে {ticker: DataFrame} ফরম্যাটে রূপান্তর
            result = {}
            if len(tickers) == 1:
                ticker = tickers[0]
                if isinstance(data, pd.DataFrame) and not data.empty:
                    result[ticker] = data
            else:
                for ticker in tickers:
                    if ticker in data.columns.levels[1]:
                        ticker_data = data.xs(ticker, level=1, axis=1)
                        result[ticker] = ticker_data

            if not result:
                raise PriceFetchError("কোনো ডেটা পাওয়া যায়নি")

            logger.info(f"✓ ডেটা ডাউনলোড সফল: {len(result)} টি স্টক")
            return result

        except Exception as e:
            raise PriceFetchError(f"yfinance ত্রুটি: {e}")


class SimulatedFetcher(PriceFetcher):
    """
    সিমুলেটেড স্টক প্রাইস জেনারেটর।

    yfinance না থাকলে বা API ব্যর্থ হলে এই ফলব্যাক ব্যবহার করা হয়।
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        if NUMPY_AVAILABLE:
            np.random.seed(self.seed)

    def fetch(self, tickers: List[str], period: str = "6mo") -> Dict[str, pd.DataFrame]:
        """
        সিমুলেটেড স্টক প্রাইস ডেটা তৈরি করে।

        Parameters
        ----------
        tickers : List[str]
            স্টক টিকার তালিকা
        period : str
            সময়সীমা (বর্তমানে শুধু '6mo' সাপোর্টেড)

        Returns
        -------
        Dict[str, pd.DataFrame]
            {ticker: DataFrame} ফরম্যাটে সিমুলেটেড ডেটা
        """
        logger.info(f"সিমুলেটেড প্রাইস তৈরি করা হচ্ছে ({len(tickers)} টি স্টক)...")

        if not PANDAS_AVAILABLE:
            raise PriceFetchError("pandas প্রয়োজন — pip install pandas")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        dates = list(pd.bdate_range(start_date, end_date))
        n_days = len(dates)

        # প্রতিটি স্টকের জন্য বাস্তবসম্মত প্যারামিটার
        stock_params = {
            "RY.TO": {"base": 165.00, "vol": 0.008, "drift": 0.0003},
            "TD.TO": {"base": 85.00, "vol": 0.009, "drift": 0.0002},
            "BNS.TO": {"base": 72.50, "vol": 0.010, "drift": 0.0001},
            "CNQ.TO": {"base": 98.00, "vol": 0.015, "drift": 0.0004},
            "SHOP.TO": {"base": 110.00, "vol": 0.025, "drift": 0.0005},
            "ENB.TO": {"base": 53.00, "vol": 0.007, "drift": 0.0002},
            "BMO.TO": {"base": 130.00, "vol": 0.009, "drift": 0.0003},
            "CP.TO": {"base": 115.00, "vol": 0.012, "drift": 0.00035},
        }

        data = {}
        for ticker in tickers:
            params = stock_params.get(ticker, {"base": 100.00, "vol": 0.01, "drift": 0.0002})
            prices = []
            price = params["base"]

            if NUMPY_AVAILABLE:
                returns = np.random.normal(params["drift"], params["vol"], n_days)
                prices = [price * np.prod(1 + returns[:i+1]) for i in range(n_days)]
            else:
                # numpy ছাড়া সরল সিমুলেশন
                import random
                price = params["base"]
                for _ in range(n_days):
                    change = random.uniform(-0.02, 0.02)
                    price *= (1 + change)
                    prices.append(price)

            data[ticker] = pd.DataFrame({"Close": prices}, index=dates)

        logger.info(f"✓ সিমুলেটেড ডেটা তৈরি: {len(data)} টি স্টক, {n_days} দিন")
        return data


def get_price_fetcher(prefer_real: bool = True) -> PriceFetcher:
    """
    উপযুক্ত PriceFetcher সিলেক্ট করে (স্ট্র্যাটেজি প্যাটার্ন)।

    Parameters
    ----------
    prefer_real : bool
        True হলে yfinance ব্যবহারের চেষ্টা করবে

    Returns
    -------
    PriceFetcher
        YFinanceFetcher বা SimulatedFetcher
    """
    if prefer_real and YFINANCE_AVAILABLE:
        logger.debug("YFinanceFetcher সিলেক্ট করা হয়েছে")
        return YFinanceFetcher()
    logger.debug("SimulatedFetcher সিলেক্ট করা হয়েছে (yfinance উপলব্ধ নয়)")
    return SimulatedFetcher(seed=Config.RANDOM_SEED)


# ============================================================
# পারফরম্যান্স অ্যানালাইজার — পোর্টফোলিও পারফরম্যান্স বিশ্লেষণ
# ============================================================
class PerformanceAnalyzer:
    """
    পোর্টফোলিও পারফরম্যান্স বিশ্লেষণ ইঞ্জিন।

    Methods
    -------
    analyze(portfolio, price_data) -> Tuple[List[StockPerformance], dict]
        সম্পূর্ণ পারফরম্যান্স বিশ্লেষণ
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceAnalyzer")

    def analyze(
        self,
        portfolio: Portfolio,
        price_data: Dict[str, pd.DataFrame]
    ) -> Tuple[List[StockPerformance], Dict[str, Any]]:
        """
        পোর্টফোলিওর সম্পূর্ণ পারফরম্যান্স বিশ্লেষণ করে।

        Parameters
        ----------
        portfolio : Portfolio
            বিশ্লেষণের পোর্টফোলিও
        price_data : Dict[str, pd.DataFrame]
            {ticker: DataFrame} ফরম্যাটে প্রাইস ডেটা

        Returns
        -------
        Tuple[List[StockPerformance], Dict[str, Any]]
            - প্রতিটি স্টকের পারফরম্যান্স
            - সামগ্রিক পরিসংখ্যান (মোট রিটার্ন, রিস্ক ইত্যাদি)
        """
        self.logger.info("পারফরম্যান্স বিশ্লেষণ শুরু...")

        stock_performances = []
        total_value = portfolio.cash
        total_cost = portfolio.cash

        for stock in portfolio.stocks:
            perf = self._analyze_stock(stock, price_data)
            stock_performances.append(perf)
            total_cost += perf.cost
            total_value += perf.value

        # সামগ্রিক পরিসংখ্যান
        total_return = total_value - total_cost
        total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0

        stats = {
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "total_return": round(total_return, 2),
            "total_return_pct": round(total_return_pct, 2),
            "best_performer": max(stock_performances, key=lambda x: x.return_pct),
            "worst_performer": min(stock_performances, key=lambda x: x.return_pct),
            "positive_count": sum(1 for s in stock_performances if s.return_pct >= 0),
            "negative_count": sum(1 for s in stock_performances if s.return_pct < 0),
        }

        # সময় সিরিজ বিশ্লেষণ (যদি pandas থাকে)
        if PANDAS_AVAILABLE:
            try:
                stats["daily_stats"] = self._analyze_time_series(portfolio, price_data)
            except Exception as e:
                self.logger.warning(f"টাইম সিরিজ বিশ্লেষণ ব্যর্থ: {e}")
                stats["daily_stats"] = None

        self.logger.info(
            f"✓ বিশ্লেষণ সম্পন্ন: রিটার্ন {stats['total_return_pct']:+.2f}%, "
            f"{stats['positive_count']} টি লাভ, {stats['negative_count']} টি ক্ষতি"
        )

        return stock_performances, stats

    def _analyze_stock(
        self,
        stock: StockHolding,
        price_data: Dict[str, pd.DataFrame]
    ) -> StockPerformance:
        """
        একটি স্টকের পারফরম্যান্স বিশ্লেষণ করে।

        Parameters
        ----------
        stock : StockHolding
            বিশ্লেষণের স্টক
        price_data : Dict[str, pd.DataFrame]
            প্রাইস ডেটা

        Returns
        -------
        StockPerformance
            স্টকের পারফরম্যান্স ডেটা
        """
        try:
            current_price = self._get_current_price(stock.ticker, price_data)
            validate_price(current_price, stock.ticker)
        except DataValidationError as e:
            self.logger.warning(str(e))
            current_price = stock.buy_price
        except Exception as e:
            self.logger.error(f"{stock.ticker} প্রাইস পেতে ব্যর্থ: {e}")
            current_price = stock.buy_price

        cost = stock.shares * stock.buy_price
        value = stock.shares * current_price
        return_pct = ((current_price - stock.buy_price) / stock.buy_price) * 100
        return_dollar = value - cost

        return StockPerformance(
            ticker=stock.ticker,
            shares=stock.shares,
            buy_price=stock.buy_price,
            current_price=round(current_price, 2),
            cost=round(cost, 2),
            value=round(value, 2),
            return_pct=round(return_pct, 2),
            return_dollar=round(return_dollar, 2),
        )

    @staticmethod
    def _get_current_price(
        ticker: str,
        price_data: Dict[str, pd.DataFrame]
    ) -> float:
        """
        সর্বশেষ উপলব্ধ ক্লোজিং প্রাইস বের করে।

        Parameters
        ----------
        ticker : str
            স্টক টিকার
        price_data : Dict[str, pd.DataFrame]
            প্রাইস ডেটা

        Returns
        -------
        float
            বর্তমান প্রাইস (সর্বশেষ Close)
        """
        if ticker not in price_data:
            raise PriceFetchError(f"{ticker} প্রাইস ডেটায় পাওয়া যায়নি")

        df = price_data[ticker]
        if df.empty or "Close" not in df.columns:
            raise PriceFetchError(f"{ticker} ডেটা খালি বা Close কলাম নেই")

        return float(df["Close"].iloc[-1])

    @staticmethod
    def _analyze_time_series(
        portfolio: Portfolio,
        price_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, float]:
        """
        পোর্টফোলিওর টাইম সিরিজ বিশ্লেষণ (ডেইলি রিটার্ন, ভোলাটিলিটি)।

        Parameters
        ----------
        portfolio : Portfolio
            পোর্টফোলিও
        price_data : Dict[str, pd.DataFrame]
            প্রাইস ডেটা

        Returns
        -------
        Dict[str, float]
            পরিসংখ্যানিক মেট্রিক্স
        """
        if not PANDAS_AVAILABLE:
            return {}

        # পোর্টফোলিও ভ্যালুর টাইম সিরিজ
        first_key = next(iter(price_data.keys()))
        n_days = len(price_data[first_key])
        portfolio_values = []

        for i in range(n_days):
            daily_value = portfolio.cash
            for stock in portfolio.stocks:
                if stock.ticker in price_data:
                    df = price_data[stock.ticker]
                    if i < len(df):
                        daily_value += stock.shares * df["Close"].iloc[i]
            portfolio_values.append(daily_value)

        dates = price_data[first_key].index
        series = pd.Series(portfolio_values, index=dates)
        daily_returns = series.pct_change().dropna()

        return {
            "avg_daily_return": round(float(daily_returns.mean() * 100), 4),
            "volatility": round(float(daily_returns.std() * 100), 4),
            "max_daily_return": round(float(daily_returns.max() * 100), 4),
            "min_daily_return": round(float(daily_returns.min() * 100), 4),
            "cumulative_return": round(float((series.iloc[-1] / series.iloc[0] - 1) * 100), 2),
            "sharpe_ratio": round(float(daily_returns.mean() / daily_returns.std() * (252 ** 0.5)), 4),
        }


# ============================================================
# রিপোর্ট জেনারেটর — CSV, TXT, PLOT আউটপুট
# ============================================================
class ReportGenerator:
    """
    রিপোর্ট জেনারেশন — CSV, TXT, এবং প্লট ফাইল তৈরি করে।

    Methods
    -------
    to_csv(performances, stats, filepath) -> Path
        CSV ফাইলে রিপোর্ট সেভ
    to_txt(portfolio, performances, stats, filepath) -> Path
        টেক্সট ফাইলে রিপোর্ট সেভ
    plot(performances, stats, price_data, filepath) -> Path
        গ্রাফ ফাইল তৈরি
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ReportGenerator")

    def to_csv(
        self,
        performances: List[StockPerformance],
        stats: Dict[str, Any],
        filepath: Path
    ) -> Path:
        """
        পারফরম্যান্স ডেটা CSV ফাইলে সেভ করে।

        Parameters
        ----------
        performances : List[StockPerformance]
            স্টক পারফরম্যান্সের তালিকা
        stats : Dict[str, Any]
            সামগ্রিক পরিসংখ্যান
        filepath : Path
            CSV ফাইলের পাথ

        Returns
        -------
        Path
            সেভ করা ফাইলের পাথ
        """
        try:
            filepath.parent.mkdir(exist_ok=True)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                writer.writerow(["স্টক পারফরম্যান্স রিপোর্ট"])
                writer.writerow(["জেনারেটেড:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                writer.writerow([])

                # হেডার
                writer.writerow([
                    "টিকার", "নাম", "শেয়ার", "ক্রয় মূল্য", "বর্তমান মূল্য",
                    "মোট খরচ", "বর্তমান মূল্য (মোট)", "রিটার্ন ($)", "রিটার্ন (%)"
                ])

                # ডেটা
                for perf in performances:
                    writer.writerow([
                        perf.ticker, perf.ticker, perf.shares, perf.buy_price,
                        perf.current_price, perf.cost, perf.value,
                        perf.return_dollar, perf.return_pct
                    ])

                writer.writerow([])
                writer.writerow(["মোট রিটার্ন:", f"{stats['total_return']:+.2f}"])
                writer.writerow(["মোট রিটার্ন (%):", f"{stats['total_return_pct']:+.2f}%"])
                writer.writerow(["সেরা স্টক:", stats["best_performer"].ticker])
                writer.writerow(["সবচেয়ে খারাপ:", stats["worst_performer"].ticker])

            self.logger.info(f"✓ CSV রিপোর্ট সেভ করা হয়েছে: {filepath}")
            return filepath

        except (OSError, IOError) as e:
            raise PortfolioError(f"CSV রিপোর্ট সেভ করতে ব্যর্থ: {e}")

    def to_txt(
        self,
        portfolio: Portfolio,
        performances: List[StockPerformance],
        stats: Dict[str, Any],
        filepath: Path
    ) -> Path:
        """
        টেক্সট ফাইলে বিস্তারিত রিপোর্ট জেনারেট করে।

        Parameters
        ----------
        portfolio : Portfolio
            পোর্টফোলিও
        performances : List[StockPerformance]
            স্টক পারফরম্যান্স
        stats : Dict[str, Any]
            সামগ্রিক পরিসংখ্যান
        filepath : Path
            TXT ফাইলের পাথ

        Returns
        -------
        Path
            সেভ করা ফাইলের পাথ
        """
        try:
            filepath.parent.mkdir(exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"   📊 পোর্টফোলিও অ্যানালাইসিস রিপোর্ট\n")
                f.write(f"   Investor: {portfolio.investor}\n")
                f.write(f"   Currency: {portfolio.currency}\n")
                f.write(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                # সারাংশ
                f.write("📋 পোর্টফোলিও সারাংশ\n")
                f.write("-" * 60 + "\n")
                f.write(f"   মোট স্টক:        {portfolio.stock_count} টি\n")
                f.write(f"   নগদ ব্যালেন্স:    {format_currency(portfolio.cash)}\n")
                f.write(f"   মোট বিনিয়োগ:     {format_currency(portfolio.total_invested)}\n")
                f.write(f"   বর্তমান মূল্য:    {format_currency(stats['total_value'])}\n")
                f.write(f"   মোট রিটার্ন:      {format_currency(stats['total_return'])} "
                        f"({stats['total_return_pct']:+.2f}%)\n\n")

                # বিস্তারিত
                f.write("📈 প্রতি স্টকের বিস্তারিত\n")
                f.write("-" * 80 + "\n")
                header = (
                    f"  {'টিকার':<8} {'শেয়ার':<8} {'ক্রয়':<10} "
                    f"{'বর্তমান':<10} {'মোট খরচ':<12} {'বর্তমান মূল্য':<14} {'রিটার্ন%':<10}"
                )
                f.write(header + "\n")
                f.write("  " + "-" * 72 + "\n")

                for p in performances:
                    arrow = "▲" if p.return_pct >= 0 else "▼"
                    f.write(
                        f"  {p.ticker:<8} {p.shares:<8} ${p.buy_price:<8.2f} "
                        f"${p.current_price:<8.2f} ${p.cost:<10.2f} "
                        f"${p.value:<12.2f} {arrow}{p.return_pct:<+8.2f}%\n"
                    )

                f.write("\n")

                # পরিসংখ্যান
                f.write("📊 পরিসংখ্যান\n")
                f.write("-" * 60 + "\n")
                f.write(f"   🏆 সেরা:     {stats['best_performer'].ticker} "
                        f"({stats['best_performer'].return_pct:+.2f}%)\n")
                f.write(f"   ⚠️ সবচেয়ে খারাপ: {stats['worst_performer'].ticker} "
                        f"({stats['worst_performer'].return_pct:+.2f}%)\n")
                f.write(f"   ✅ লাভের স্টক: {stats['positive_count']} টি\n")
                f.write(f"   ❌ ক্ষতির স্টক: {stats['negative_count']} টি\n")

                if stats.get("daily_stats"):
                    ds = stats["daily_stats"]
                    f.write(f"\n   📉 রিস্ক অ্যানালাইসিস\n")
                    f.write(f"       গড় ডেইলি রিটার্ন:   {ds['avg_daily_return']:+.4f}%\n")
                    f.write(f"       ভোলাটিলিটি (ঝুঁকি):  {ds['volatility']:.4f}%\n")
                    f.write(f"       কিউমুলেটিভ রিটার্ন:  {ds['cumulative_return']:+.2f}%\n")
                    f.write(f"       Sharpe Ratio:         {ds['sharpe_ratio']:.4f}\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("   রিপোর্ট জেনারেটেড বাই Python Portfolio Analyzer v2.0\n")
                f.write("   Day 19 — পেশাদার কোড স্ট্রাকচার\n")
                f.write("=" * 80 + "\n")

            self.logger.info(f"✓ TXT রিপোর্ট সেভ করা হয়েছে: {filepath}")
            return filepath

        except (OSError, IOError) as e:
            raise PortfolioError(f"TXT রিপোর্ট সেভ করতে ব্যর্থ: {e}")

    def plot(
        self,
        performances: List[StockPerformance],
        stats: Dict[str, Any],
        price_data: Dict[str, pd.DataFrame],
        filepath: Path
    ) -> Optional[Path]:
        """
        পোর্টফোলিও পারফরম্যান্সের গ্রাফ তৈরি করে।

        Parameters
        ----------
        performances : List[StockPerformance]
            স্টক পারফরম্যান্স
        stats : Dict[str, Any]
            সামগ্রিক পরিসংখ্যান
        price_data : Dict[str, pd.DataFrame]
            প্রাইস ডেটা
        filepath : Path
            ইমেজ ফাইলের পাথ

        Returns
        -------
        Optional[Path]
            সেভ করা ইমেজের পাথ, ব্যর্থ হলে None
        """
        if not MPL_AVAILABLE:
            self.logger.warning("matplotlib না থাকায় গ্রাফ তৈরি করা যায়নি")
            return None

        if not PANDAS_AVAILABLE:
            self.logger.warning("pandas না থাকায় গ্রাফ তৈরি করা যায়নি")
            return None

        try:
            fig, axes = plt.subplots(2, 2, figsize=Config.PLOT_FIGSIZE)
            fig.suptitle(
                "📈 স্টক পোর্টফোলিও অ্যানালাইজার — পারফরম্যান্স রিপোর্ট",
                fontsize=16, fontweight="bold"
            )

            self._plot_cumulative_returns(axes[0, 0], performances, price_data)
            self._plot_stock_returns(axes[0, 1], performances)
            self._plot_allocation(axes[1, 0], performances)
            self._plot_price_trends(axes[1, 1], performances, price_data)

            plt.tight_layout()
            filepath.parent.mkdir(exist_ok=True)
            plt.savefig(filepath, dpi=Config.PLOT_DPI, bbox_inches="tight")
            plt.close()

            self.logger.info(f"✓ গ্রাফ সেভ করা হয়েছে: {filepath}")
            return filepath

        except Exception as e:
            raise PlottingError(f"গ্রাফ তৈরি করতে ব্যর্থ: {e}")

    @staticmethod
    def _plot_cumulative_returns(ax, performances, price_data):
        """কিউমুলেটিভ রিটার্ন গ্রাফ"""
        first_key = next(iter(price_data.keys()))
        dates = price_data[first_key].index
        total_invested = sum(p.cost for p in performances)

        portfolio_values = []
        for i in range(len(dates)):
            value = 0
            for p in performances:
                if p.ticker in price_data:
                    df = price_data[p.ticker]
                    if i < len(df):
                        value += p.shares * df["Close"].iloc[i]
            portfolio_values.append(value)

        cum_return = [(v / total_invested - 1) * 100 for v in portfolio_values]
        ax.plot(dates, cum_return, color="#2E86AB", linewidth=2)
        ax.fill_between(dates, 0, cum_return, alpha=0.2, color="#2E86AB")
        ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
        ax.set_title("কিউমুলেটিভ রিটার্ন (%)", fontsize=12)
        ax.set_ylabel("রিটার্ন (%)")
        ax.grid(True, alpha=0.3)

    @staticmethod
    def _plot_stock_returns(ax, performances):
        """প্রতি স্টকের রিটার্ন বার চার্ট"""
        tickers = [p.ticker for p in performances]
        returns = [p.return_pct for p in performances]
        colors = ["#2ECC71" if r >= 0 else "#E74C3C" for r in returns]
        bars = ax.bar(tickers, returns, color=colors, alpha=0.8)
        ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
        ax.set_title("প্রতি স্টকের রিটার্ন (%)", fontsize=12)
        ax.set_ylabel("রিটার্ন (%)")
        ax.tick_params(axis="x", rotation=45)
        for bar, ret in zip(bars, returns):
            y_pos = bar.get_height() + (0.5 if ret >= 0 else -1.5)
            ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                    f"{ret:+.1f}%", ha="center", fontsize=8)

    @staticmethod
    def _plot_allocation(ax, performances):
        """পোর্টফোলিও অ্যালোকেশন পাই চার্ট"""
        values = [p.value for p in performances]
        labels = [p.ticker for p in performances]
        total = sum(values)
        threshold = total * 0.05
        other = sum(v for v in values if v / total < threshold)
        main_labels = [l for l, v in zip(labels, values) if v / total >= threshold]
        main_values = [v for v in values if v / total >= threshold]
        if other > 0:
            main_labels.append("অন্যান্য")
            main_values.append(other)
        ax.pie(main_values, labels=main_labels, autopct="%1.1f%%",
               startangle=90, colors=plt.cm.Set2.colors, textprops={"fontsize": 9})
        ax.set_title("পোর্টফোলিও অ্যালোকেশন", fontsize=12)

    @staticmethod
    def _plot_price_trends(ax, performances, price_data):
        """স্টক প্রাইস ট্রেন্ড (নরমালাইজড)"""
        for p in performances:
            if p.ticker in price_data:
                df = price_data[p.ticker]
                normalized = (df["Close"] / df["Close"].iloc[0]) * 100
                normalized.plot(ax=ax, linewidth=1.5, alpha=0.8, label=p.ticker)
        ax.set_title("স্টক প্রাইস ট্রেন্ড (বেস=100)", fontsize=12)
        ax.set_ylabel("প্রাইস ইনডেক্স")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=7)


# ============================================================
# মেইন অ্যাপ্লিকেশন ক্লাস
# ============================================================
class PortfolioApp:
    """
    পোর্টফোলিও অ্যানালাইজার অ্যাপ্লিকেশন।
    পুরো ওয়ার্কফ্লো orchestrate করে।

    Usage
    -----
    >>> app = PortfolioApp()
    >>> app.run()
    """

    def __init__(self, log_level: str = "INFO"):
        global logger
        logger = setup_logging(log_level)
        self.logger = logger

        Config.ensure_dirs()

        self.portfolio_manager = PortfolioManager()
        self.price_fetcher = get_price_fetcher(prefer_real=False)
        self.analyzer = PerformanceAnalyzer()
        self.reporter = ReportGenerator()

        self.portfolio: Optional[Portfolio] = None
        self.price_data: Optional[Dict[str, pd.DataFrame]] = None
        self.performances: Optional[List[StockPerformance]] = None
        self.stats: Optional[Dict[str, Any]] = None

    def run(self) -> None:
        """পুরো পোর্টফোলিও অ্যানালাইসিস পাইপলাইন চালায়।"""
        start_time = time.time()

        print("\n" + "=" * 70)
        print("   📊 স্টক পোর্টফোলিও অ্যানালাইজার v2.0 (পলিশড)")
        print("   Python ফাইন্যান্স প্রজেক্ট — Day 19")
        print("=" * 70 + "\n")

        try:
            # Step 1: পোর্টফোলিও তৈরি
            self.portfolio = self.portfolio_manager.create_default()
            self.portfolio_manager.save_csv(self.portfolio, Config.PORTFOLIO_CSV)
            self.portfolio_manager.save_json(self.portfolio, Config.PORTFOLIO_JSON)
            self.portfolio_manager.display_summary(self.portfolio)

            # Step 2: প্রাইস ফেচ
            tickers = [s.ticker for s in self.portfolio.stocks]
            self.price_data = self.price_fetcher.fetch(tickers, Config.PRICE_PERIOD)

            # Step 3: বিশ্লেষণ
            self.performances, self.stats = self.analyzer.analyze(
                self.portfolio, self.price_data
            )
            self._display_performances()

            # Step 4: রিপোর্ট জেনারেট
            self.reporter.to_csv(self.performances, self.stats, Config.PERFORMANCE_CSV)
            self.reporter.to_txt(
                self.portfolio, self.performances, self.stats, Config.REPORT_TXT
            )
            self.reporter.plot(
                self.performances, self.stats, self.price_data, Config.PERFORMANCE_PLOT
            )

            # সমাপ্তি
            elapsed = time.time() - start_time
            print(f"\n{'='*70}")
            print(f"   ✅ অ্যানালাইসিস সম্পন্ন! সময়: {elapsed:.2f} সেকেন্ড")
            print(f"   📁 আউটপুট ডিরেক্টরি: {Config.OUTPUT_DIR}")
            print(f"   📊 CSV: {Config.PERFORMANCE_CSV.name}")
            print(f"   📝 রিপোর্ট: {Config.REPORT_TXT.name}")
            print(f"   📈 গ্রাফ: {Config.PERFORMANCE_PLOT.name}")
            print(f"{'='*70}\n")

        except PortfolioError as e:
            self.logger.error(f"❌ পোর্টফোলিও ত্রুটি: {e}")
        except Exception as e:
            self.logger.error(f"❌ অপ্রত্যাশিত ত্রুটি: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())

    def _display_performances(self) -> None:
        """পারফরম্যান্স ডেটা কনসোলে দেখায়।"""
        if not self.performances or not self.stats:
            return

        print(f"\n   {'টিকার':<10} {'শেয়ার':<8} {'ক্রয়':<10} {'বর্তমান':<10} "
              f"{'মোট':<12} {'মূল্য':<12} {'রিটার্ন%':<10}")
        print(f"   {'-'*10} {'-'*8} {'-'*10} {'-'*10} {'-'*12} {'-'*12} {'-'*10}")

        for p in self.performances:
            arrow = "▲" if p.return_pct >= 0 else "▼"
            print(f"   {p.ticker:<10} {p.shares:<8} ${p.buy_price:<8.2f} "
                  f"${p.current_price:<8.2f} ${p.cost:<10.2f} "
                  f"${p.value:<10.2f} {arrow}{p.return_pct:<+8.2f}")

        print(f"\n   {'মোট':<63} ${self.stats['total_return']:<+10.2f} "
              f"({self.stats['total_return_pct']:<+.2f}%)")
        print(f"   🏆 সেরা: {self.stats['best_performer'].ticker} "
              f"({self.stats['best_performer'].return_pct:+.2f}%)")
        print(f"   ⚠️ খারাপ: {self.stats['worst_performer'].ticker} "
              f"({self.stats['worst_performer'].return_pct:+.2f}%)")


# ============================================================
# এন্ট্রি পয়েন্ট
# ============================================================
def main():
    """
    অ্যাপ্লিকেশনের এন্ট্রি পয়েন্ট।

    উদাহরণ:
        python day19_portfolio_polish.py
        python day19_portfolio_polish.py --log-level DEBUG
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="পোর্টফোলিও অ্যানালাইজার — পেশাদার কোড স্ট্রাকচার"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="লগিং লেভেল (ডিফল্ট: INFO)"
    )
    parser.add_argument(
        "--load-csv",
        type=str,
        default=None,
        help="CSV ফাইল থেকে পোর্টফোলিও লোড করুন"
    )

    args = parser.parse_args()

    app = PortfolioApp(log_level=args.log_level)

    if args.load_csv:
        csv_path = Path(args.load_csv)
        if csv_path.exists():
            app.portfolio = PortfolioManager.load_csv(csv_path)
            app.portfolio_manager.display_summary(app.portfolio)
            app.price_data = app.price_fetcher.fetch(
                [s.ticker for s in app.portfolio.stocks],
                Config.PRICE_PERIOD
            )
            app.performances, app.stats = app.analyzer.analyze(
                app.portfolio, app.price_data
            )
            app.reporter.to_csv(app.performances, app.stats, Config.PERFORMANCE_CSV)
        else:
            logger.error(f"CSV ফাইল পাওয়া যায়নি: {csv_path}")
    else:
        app.run()


if __name__ == "__main__":
    main()
