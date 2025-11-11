#!/usr/bin/env python3
"""
ECHOPULSE v3.0 Scanner Script
Automated daily scan of watchlist stocks
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collectors import DataAggregator
from analyzer import EchoPulseAnalyzer


# Default watchlist - can be customized
DEFAULT_WATCHLIST = [
    # Tech / Growth
    "NVDA", "AMD", "TSLA", "PLTR", "SNOW", "DDOG",
    # Meme / High Buzz
    "GME", "AMC", "BBBY", "RDDT",
    # Small Cap / Volatile
    "SOFI", "HOOD", "COIN", "RBLX",
    # Recent IPOs
    "ARM", "INSTACART"
]


def load_watchlist(filepath: str = None) -> list:
    """Load watchlist from file or use default"""
    if filepath and Path(filepath).exists():
        with open(filepath, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
            return tickers
    return DEFAULT_WATCHLIST


def save_scan_results(data: dict, output_dir: Path = Path("data")):
    """Save raw scan data to file"""
    output_dir.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = output_dir / f"scan_{today}.json"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved scan data to {filename}")
    return filename


def generate_brief(data: dict, output_dir: Path = Path("briefs")):
    """Generate ECHOPULSE brief from scan data"""
    output_dir.mkdir(exist_ok=True)

    analyzer = EchoPulseAnalyzer()
    brief = analyzer.analyze(data)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = output_dir / f"morning_brief_{today}.md"

    with open(filename, 'w') as f:
        f.write(brief)

    print(f"✅ Generated brief at {filename}")
    return filename, brief


def main():
    """Main scanner execution"""
    print("=" * 60)
    print("ECHOPULSE v3.0 - Automated Scanner")
    print("=" * 60)
    print()

    # Load watchlist
    watchlist_file = sys.argv[1] if len(sys.argv) > 1 else None
    watchlist = load_watchlist(watchlist_file)

    print(f"📋 Watchlist: {len(watchlist)} tickers")
    print(f"   {', '.join(watchlist)}")
    print()

    # Collect data
    print("🔍 Collecting data...")
    aggregator = DataAggregator()
    data = aggregator.scan_watchlist(watchlist)

    print(f"✅ Collected data for {len(data['candidates'])} candidates")
    print()

    # Save raw data
    save_scan_results(data)

    # Generate brief
    print("📊 Generating ECHOPULSE brief...")
    brief_file, brief_content = generate_brief(data)

    # Print summary
    print()
    print("=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)
    print()
    print(brief_content[:500] + "...")
    print()
    print(f"📄 Full brief: {brief_file}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
