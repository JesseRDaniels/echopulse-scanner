"""
ECHOPULSE v3.0 Trade Tracker
Log and track trading performance
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TradeTracker:
    """Track trades and calculate performance metrics"""

    def __init__(self, trades_file: str = "trades/trades.csv"):
        self.trades_file = Path(trades_file)
        self.trades_file.parent.mkdir(exist_ok=True)

        # Initialize CSV if doesn't exist
        if not self.trades_file.exists():
            self._init_csv()

    def _init_csv(self):
        """Create CSV with headers"""
        with open(self.trades_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "date",
                "ticker",
                "action",  # BUY or SELL
                "shares",
                "price",
                "total_cost",
                "notes"
            ])

    def log_trade(
        self,
        ticker: str,
        action: str,
        shares: int,
        price: float,
        notes: str = ""
    ):
        """
        Log a trade
        action: 'BUY' or 'SELL'
        """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_cost = shares * price

        with open(self.trades_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                date,
                ticker,
                action.upper(),
                shares,
                f"{price:.2f}",
                f"{total_cost:.2f}",
                notes
            ])

        print(f"✅ Logged: {action} {shares} {ticker} @ ${price:.2f}")

    def get_trades(self, ticker: Optional[str] = None) -> List[Dict]:
        """Get all trades or trades for a specific ticker"""
        if not self.trades_file.exists():
            return []

        trades = []
        with open(self.trades_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if ticker is None or row['ticker'] == ticker:
                    trades.append(row)

        return trades

    def calculate_pnl(self, ticker: Optional[str] = None) -> Dict:
        """
        Calculate P&L
        Simple FIFO (First In First Out) accounting
        """
        trades = self.get_trades(ticker)

        if not trades:
            return {
                "total_invested": 0,
                "total_proceeds": 0,
                "realized_pnl": 0,
                "open_positions": {}
            }

        # Track positions using FIFO
        positions = {}  # ticker -> list of (shares, price)
        total_invested = 0
        total_proceeds = 0
        realized_pnl = 0

        for trade in trades:
            t = trade['ticker']
            action = trade['action']
            shares = int(trade['shares'])
            price = float(trade['price'])

            if action == 'BUY':
                if t not in positions:
                    positions[t] = []
                positions[t].append((shares, price))
                total_invested += shares * price

            elif action == 'SELL':
                if t not in positions or not positions[t]:
                    print(f"⚠️  Warning: SELL without BUY for {t}")
                    continue

                remaining_to_sell = shares
                sell_proceeds = shares * price
                total_proceeds += sell_proceeds

                # FIFO: sell oldest lots first
                while remaining_to_sell > 0 and positions[t]:
                    lot_shares, lot_price = positions[t][0]

                    if lot_shares <= remaining_to_sell:
                        # Sell entire lot
                        cost_basis = lot_shares * lot_price
                        proceeds = lot_shares * price
                        realized_pnl += (proceeds - cost_basis)

                        remaining_to_sell -= lot_shares
                        positions[t].pop(0)
                    else:
                        # Partial sell
                        cost_basis = remaining_to_sell * lot_price
                        proceeds = remaining_to_sell * price
                        realized_pnl += (proceeds - cost_basis)

                        # Update lot
                        positions[t][0] = (lot_shares - remaining_to_sell, lot_price)
                        remaining_to_sell = 0

        # Calculate open positions
        open_positions = {}
        for ticker, lots in positions.items():
            if lots:
                total_shares = sum(shares for shares, _ in lots)
                avg_price = sum(shares * price for shares, price in lots) / total_shares
                open_positions[ticker] = {
                    "shares": total_shares,
                    "avg_price": round(avg_price, 2),
                    "cost_basis": round(sum(shares * price for shares, price in lots), 2)
                }

        return {
            "total_invested": round(total_invested, 2),
            "total_proceeds": round(total_proceeds, 2),
            "realized_pnl": round(realized_pnl, 2),
            "realized_pnl_pct": round((realized_pnl / total_invested * 100) if total_invested > 0 else 0, 2),
            "open_positions": open_positions
        }

    def generate_report(self) -> str:
        """Generate performance report"""
        pnl = self.calculate_pnl()

        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ECHOPULSE TRADE TRACKER - Performance Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 REALIZED P&L
   Total Invested:  ${pnl['total_invested']:,.2f}
   Total Proceeds:  ${pnl['total_proceeds']:,.2f}
   Realized P&L:    ${pnl['realized_pnl']:,.2f} ({pnl['realized_pnl_pct']:+.2f}%)

📦 OPEN POSITIONS
"""

        if pnl['open_positions']:
            for ticker, pos in pnl['open_positions'].items():
                report += f"   ${ticker}: {pos['shares']} shares @ ${pos['avg_price']:.2f} avg (Cost: ${pos['cost_basis']:,.2f})\n"
        else:
            report += "   None\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        return report


# CLI interface
if __name__ == "__main__":
    import sys

    tracker = TradeTracker()

    if len(sys.argv) < 2:
        print("ECHOPULSE Trade Tracker")
        print()
        print("Usage:")
        print("  python trade_tracker.py buy TICKER SHARES PRICE [NOTES]")
        print("  python trade_tracker.py sell TICKER SHARES PRICE [NOTES]")
        print("  python trade_tracker.py report")
        print("  python trade_tracker.py pnl [TICKER]")
        print()
        print("Examples:")
        print("  python trade_tracker.py buy NVDA 10 193.50 'Kevin Xu pick'")
        print("  python trade_tracker.py sell NVDA 5 232.75 'T1 target hit'")
        print("  python trade_tracker.py report")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command in ['buy', 'sell']:
        if len(sys.argv) < 5:
            print("❌ Error: Missing arguments")
            print(f"Usage: python trade_tracker.py {command} TICKER SHARES PRICE [NOTES]")
            sys.exit(1)

        ticker = sys.argv[2].upper()
        shares = int(sys.argv[3])
        price = float(sys.argv[4])
        notes = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ""

        tracker.log_trade(ticker, command, shares, price, notes)

    elif command == 'report':
        print(tracker.generate_report())

    elif command == 'pnl':
        ticker = sys.argv[2].upper() if len(sys.argv) > 2 else None
        pnl = tracker.calculate_pnl(ticker)

        if ticker:
            print(f"\n📊 P&L for ${ticker}")
        else:
            print("\n📊 Overall P&L")

        print(f"   Total Invested: ${pnl['total_invested']:,.2f}")
        print(f"   Total Proceeds: ${pnl['total_proceeds']:,.2f}")
        print(f"   Realized P&L:   ${pnl['realized_pnl']:,.2f} ({pnl['realized_pnl_pct']:+.2f}%)")
        print()

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
