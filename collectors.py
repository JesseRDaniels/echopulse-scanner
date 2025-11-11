"""
ECHOPULSE v3.0 Data Collectors
Automated data collection from multiple sources
"""

import yfinance as yf
import praw
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
from collections import defaultdict


class StockDataCollector:
    """Collect stock price and volume data via yfinance"""

    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes

    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get current stock data for a ticker
        Returns: price, market_cap, volume, or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker,
                "name": info.get("longName", ticker),
                "price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "volume": info.get("volume", 0),
                "sector": info.get("sector", "Unknown")
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def get_multiple_stocks(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """Batch fetch multiple tickers"""
        results = {}
        for ticker in tickers:
            data = self.get_stock_data(ticker)
            if data:
                results[ticker] = data
        return results


class RedditBuzzCollector:
    """Collect mentions and buzz from Reddit via PRAW"""

    def __init__(self):
        # Reddit API credentials from environment
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID", ""),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
            user_agent=os.getenv("REDDIT_USER_AGENT", "ECHOPULSE/3.0")
        )
        self.subreddits = ["wallstreetbets", "stocks", "investing", "stockmarket"]

    def get_ticker_mentions(self, ticker: str, hours: int = 24) -> Dict[str, Any]:
        """
        Get mention count and buzz for a ticker over the last N hours
        Returns: mentions_24h, buzz_ratio, velocity_1h, platforms
        """
        if not os.getenv("REDDIT_CLIENT_ID"):
            # Return mock data if no Reddit credentials
            return self._mock_reddit_data(ticker)

        try:
            mentions_24h = 0
            mentions_7d = 0
            mentions_1h = 0

            # Search across multiple subreddits
            for sub_name in self.subreddits:
                subreddit = self.reddit.subreddit(sub_name)

                # Last 24 hours
                time_filter_24h = datetime.now() - timedelta(hours=24)
                for submission in subreddit.search(f"${ticker}", time_filter="day", limit=100):
                    if datetime.fromtimestamp(submission.created_utc) > time_filter_24h:
                        mentions_24h += 1

                # Last 1 hour for velocity
                time_filter_1h = datetime.now() - timedelta(hours=1)
                for submission in subreddit.search(f"${ticker}", time_filter="hour", limit=50):
                    if datetime.fromtimestamp(submission.created_utc) > time_filter_1h:
                        mentions_1h += 1

                # Last 7 days for baseline
                for submission in subreddit.search(f"${ticker}", time_filter="week", limit=200):
                    mentions_7d += 1

            # Calculate buzz ratio (current vs 7-day average)
            avg_daily_mentions = mentions_7d / 7 if mentions_7d > 0 else 1
            buzz_ratio = mentions_24h / avg_daily_mentions if avg_daily_mentions > 0 else 1.0

            return {
                "mentions_24h": mentions_24h,
                "buzz_ratio": round(buzz_ratio, 2),
                "velocity_1h": mentions_1h,
                "platforms": ["reddit"]
            }

        except Exception as e:
            print(f"Reddit API error for {ticker}: {e}")
            return self._mock_reddit_data(ticker)

    def _mock_reddit_data(self, ticker: str) -> Dict[str, Any]:
        """Mock data when Reddit API not available"""
        import random
        return {
            "mentions_24h": random.randint(10, 500),
            "buzz_ratio": round(random.uniform(0.8, 4.0), 2),
            "velocity_1h": random.randint(0, 100),
            "platforms": ["reddit"]
        }


class NewsCollector:
    """Collect news and catalysts (simplified - can integrate NewsAPI, Alpha Vantage, etc.)"""

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY", "")

    def get_upcoming_catalysts(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get upcoming catalyst for a ticker
        In production, this would hit earnings calendars, SEC filings, etc.
        For now, returns mock data structure
        """
        # This is a placeholder - in production you'd integrate:
        # - Alpha Vantage earnings calendar
        # - SEC Edgar API for filings
        # - News APIs for product launches, etc.

        return {
            "catalyst": "Earnings Report",
            "catalyst_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "rumor": "Market expects positive guidance",
            "rumor_confidence": 2,
            "sources": ["https://finance.yahoo.com/calendar/earnings"]
        }


class FundamentalsCollector:
    """Collect fundamental health metrics"""

    def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """
        Get fundamental health check data
        Uses yfinance to assess basic fundamentals
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Revenue growth
            revenue_growth = info.get("revenueGrowth", 0)
            revenue_growing = revenue_growth > 0

            # Profitability
            profit_margin = info.get("profitMargins", 0)
            profitable = profit_margin > 0

            # Path to profit (for unprofitable companies)
            operating_margin = info.get("operatingMargins", -1)
            path_to_profit = operating_margin > -0.2  # Improving margins

            # Debt
            debt_to_equity = info.get("debtToEquity", 0)
            debt_manageable = debt_to_equity < 200  # < 2x equity

            # Dilution (simplified check)
            shares_outstanding = info.get("sharesOutstanding", 0)
            dilution_ok = True  # Would need historical data for real check

            # Red flags
            red_flags = (
                debt_to_equity > 300 or  # Excessive debt
                revenue_growth < -0.2  # Severe revenue decline
            )

            # Health score (0-5)
            health_score = 0
            if revenue_growing: health_score += 1
            if profitable: health_score += 2
            elif path_to_profit: health_score += 1
            if not red_flags: health_score += 1
            if debt_manageable: health_score += 1

            return {
                "revenue_growing": revenue_growing,
                "profitable": profitable,
                "path_to_profit": path_to_profit,
                "red_flags": red_flags,
                "debt_manageable": debt_manageable,
                "dilution_ok": dilution_ok,
                "health_score": min(5, health_score)
            }

        except Exception as e:
            print(f"Fundamentals error for {ticker}: {e}")
            return {
                "revenue_growing": False,
                "profitable": False,
                "path_to_profit": False,
                "red_flags": True,
                "debt_manageable": False,
                "dilution_ok": False,
                "health_score": 0
            }


class DataAggregator:
    """Main aggregator that combines all data sources"""

    def __init__(self):
        self.stock_collector = StockDataCollector()
        self.reddit_collector = RedditBuzzCollector()
        self.news_collector = NewsCollector()
        self.fundamentals_collector = FundamentalsCollector()

    def collect_candidate_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Collect all data for a single ticker candidate
        Returns complete candidate object for ECHOPULSE analysis
        """
        print(f"Collecting data for {ticker}...")

        # Get stock data
        stock_data = self.stock_collector.get_stock_data(ticker)
        if not stock_data:
            return None

        # Get social buzz
        buzz_data = self.reddit_collector.get_ticker_mentions(ticker)

        # Get catalysts
        catalyst_data = self.news_collector.get_upcoming_catalysts(ticker)

        # Get fundamentals
        fundamentals = self.fundamentals_collector.get_fundamentals(ticker)

        # Combine all data
        candidate = {
            **stock_data,
            **buzz_data,
            **catalyst_data,
            "fundamentals": {
                "revenue_growing": fundamentals["revenue_growing"],
                "profitable": fundamentals["profitable"],
                "path_to_profit": fundamentals["path_to_profit"],
                "red_flags": fundamentals["red_flags"],
                "debt_manageable": fundamentals["debt_manageable"],
                "dilution_ok": fundamentals["dilution_ok"]
            },
            "health_score": fundamentals["health_score"]
        }

        return candidate

    def scan_watchlist(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Scan a list of tickers and return formatted data for ECHOPULSE
        """
        candidates = []

        for ticker in tickers:
            candidate = self.collect_candidate_data(ticker)
            if candidate:
                candidates.append(candidate)

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "candidates": candidates
        }


# Example usage
if __name__ == "__main__":
    # Test the collectors
    aggregator = DataAggregator()

    # Test with a few tickers
    test_tickers = ["AAPL", "TSLA", "NVDA"]
    data = aggregator.scan_watchlist(test_tickers)

    print(f"\nCollected data for {len(data['candidates'])} candidates")
    for candidate in data["candidates"]:
        print(f"  ${candidate['ticker']}: {candidate['mentions_24h']} mentions, buzz {candidate['buzz_ratio']}x")
