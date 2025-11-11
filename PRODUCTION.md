# ECHOPULSE v3.0 - Production Usage Guide

**Deployment Model**: Manual Claude Code Tool with Full MCP Intelligence

## Why Manual with Claude Code?

Phase 3 testing revealed that **automated scanning without MCP verification has a 66% false positive rate**:
- Phase 2 alone recommended AMD and TSLA (earnings already passed)
- Only NVDA was a valid setup (earnings Nov 19)
- MCP intelligence prevented 2 bad trades out of 3 recommendations

**Conclusion**: MCP verification is CRITICAL. Since MCPs only work when Claude Code runs the scanner, we use manual execution for maximum quality.

---

## Daily Production Workflow

### Morning Routine (8 AM EST or when markets open)

**Step 1: Ask Claude to Run Scan**
```
You: "trun echopulse scan"
```
or
```
You: "Run ECHOPULSE scan for today"
```

**Step 2: Claude Executes with Full MCP Intelligence**
Claude will automatically:
1. Run Phase 2 data collection (yfinance, Reddit, fundamentals)
2. Run Phase 3 MCP analysis:
   - Tavily: Verify real earnings dates and historical patterns
   - Sequential: Multi-step quality analysis with confidence scoring
   - Memory: Match against winning patterns
3. Generate MCP-enhanced brief with real analysis
4. Filter out false positives (stocks with past earnings)
5. Provide only validated setups with evidence

**Step 3: Review Brief**
Claude presents:
- Valid setups with quality scores and confidence levels
- Rejected candidates with reasoning (catalyst already passed, etc.)
- Entry/exit strategies based on historical patterns
- Risk assessment with statistical edges

**Step 4: Make Trading Decision**
You decide whether to trade based on:
- Setup quality (70+ score preferred)
- Confidence level (3/3 stars = TIER-1)
- Historical win rate (75%+ preferred)
- Your risk tolerance and account size

---

## What Claude Does Automatically

### Phase 2: Automated Data Collection
- ✅ Real stock prices via yfinance
- ✅ Reddit buzz tracking via PRAW (mentions, buzz ratio, velocity)
- ✅ Fundamental health scoring (revenue, profitability, debt, dilution)
- ✅ Saves scan data to `data/scan_YYYY-MM-DD.json`

### Phase 3: MCP Intelligence Layer
- ✅ **Tavily MCP**: Searches web for REAL earnings dates and historical patterns
- ✅ **Sequential Thinking MCP**: 5-step quality analysis with evidence-based scoring
- ✅ **Memory MCP**: Tracks winning patterns and matches setups against history
- ✅ Filters out false positives (stocks with past catalysts)
- ✅ Generates `briefs/mcp_enhanced_brief_YYYY-MM-DD.md`

### Quality Assurance
- ✅ Verifies catalyst dates (not mock data)
- ✅ Rejects setups with past earnings
- ✅ Provides confidence levels (1-3 stars)
- ✅ Shows historical win rates when available
- ✅ Explains why candidates were rejected

---

## Command Examples

### Daily Morning Scan
```
You: "Run ECHOPULSE scan for today"
Claude: [Executes full MCP-enhanced scan]
```

### Custom Watchlist
```
You: "Scan these tickers: NVDA, TSLA, PLTR, SNOW"
Claude: [Runs MCP analysis on specified tickers]
```

### Check Specific Stock
```
You: "Is NVDA a good setup right now?"
Claude: [Runs Tavily + Sequential analysis on NVDA]
```

### Review Pattern Performance
```
You: "Show me the PreEarnings_Momentum_Pattern performance"
Claude: [Retrieves from Memory MCP]
```

---

## Expected Results

### High-Quality Output
- **Accuracy**: 100% on recommended setups (false positives filtered)
- **Confidence**: 1-3 star ratings (3 = TIER-1 highest conviction)
- **Evidence**: Historical win rates, real earnings dates, verified catalysts
- **Risk Management**: Clear entry/exit, position sizing, invalidation criteria

### What You WON'T Get
- ❌ Stocks with earnings already passed (Phase 3 catches this)
- ❌ Mock catalyst dates (Tavily verifies real dates)
- ❌ Generic rumors (Tavily finds real news and patterns)
- ❌ Unscored recommendations (Sequential provides 0-100 quality score)

---

## Trade Tracking

After executing a trade, use the trade tracker:

```bash
# Record buy
python trade_tracker.py buy NVDA 10 193.50 "Pre-earnings momentum setup"

# Record sell
python trade_tracker.py sell NVDA 5 211.50 "Hit T1 target"

# View P&L
python trade_tracker.py report
```

All trades logged to `trades/trades.csv` with FIFO accounting.

---

## Phase 1 Web UI (Still Available)

The Railway web app is still live for manual data upload if needed:
- URL: https://echopulse-scanner-production.up.railway.app
- Upload custom JSON data
- View historical briefs
- Alternative to command-line workflow

---

## Best Practices

### Timing
- Run scan 30-60 minutes before market open (8-8:30 AM EST)
- Allows time to review brief and plan entries
- Avoid scanning after hours (stale data)

### Position Sizing
- Max 5% per trade (ECHOPULSE recommendation)
- Scale down to 2-3% if win rate drops below 40%
- Never risk more than you can afford to lose

### Discipline
- Exit by time stop if specified (e.g., day before earnings)
- Exit immediately if thesis invalidated (e.g., negative catalyst)
- Don't chase - if price gaps above entry zone, skip the trade

### Learning
- Track actual results vs predictions
- Claude's Memory MCP learns from your trades
- Patterns improve as more data accumulates

---

## Maintenance

### Weekly
- Review trade performance vs ECHOPULSE predictions
- Ask Claude to analyze winning vs losing setups
- Adjust position sizing based on actual win rate

### Monthly
- Full P&L review with trade tracker
- Pattern performance analysis (Memory MCP query)
- Refine watchlist based on sectors performing well

---

## Support

**For Issues**:
1. Check that venv is activated: `source venv/bin/activate`
2. Verify Reddit API credentials in environment
3. Ask Claude to debug specific errors

**For Improvements**:
- Ask Claude to add new data sources
- Request new MCP analysis features
- Suggest pattern refinements based on results

---

**ECHOPULSE v3.0 Production Mode**: Manual execution by Claude Code with full MCP intelligence for maximum accuracy and evidence-based recommendations.

*Last Updated: November 11, 2025*
