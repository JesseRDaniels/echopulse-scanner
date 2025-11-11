# ECHOPULSE v3.0 - Personal Rumor Trading Scanner

Railway-deployed stock scanner for short-term rumor trading opportunities.

## Phase 1: Manual MVP ✅

**What's Working**:
- ✅ FastAPI web application
- ✅ ECHOPULSE v3.0 analysis logic
- ✅ Web UI for uploading data and viewing briefs
- ✅ Railway-ready configuration
- ✅ Sample data template

**What's Next (Phase 2)**:
- Automated data collection from APIs
- Scheduled 8 AM EST daily runs
- Real-time API integrations (yfinance, ApeWisdom, etc.)

---

## Quick Start (Local Testing)

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Locally

```bash
uvicorn app:app --reload --port 8000
```

Visit: http://localhost:8000

### 3. Test with Sample Data

1. Click "Get Sample" to download `sample_data.json`
2. Upload the file
3. View generated brief

---

## Deploy to Railway

### Prerequisites
- Railway account (https://railway.app)
- Railway CLI installed (optional, or use web interface)

### Deployment Steps

#### Option A: Railway Web UI (Easiest)

1. **Create New Project**
   - Go to https://railway.app/new
   - Select "Deploy from GitHub repo" or "Empty Project"

2. **Connect Repository**
   - Push this code to GitHub
   - Connect the repository to Railway
   - Railway will auto-detect the configuration

3. **Configure Volume** (for persistent storage)
   - In Railway dashboard → Variables
   - Add volume mount: `/data`, `/briefs`, `/trades`

4. **Deploy**
   - Railway will automatically build and deploy
   - Visit the generated URL

#### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open in browser
railway open
```

---

## Usage

### Manual Workflow (Phase 1)

1. **Get Sample Data**
   - Click "Get Sample" button
   - This downloads a template JSON file

2. **Customize Data** (optional)
   - Edit the JSON with real tickers and data
   - Or use as-is for testing

3. **Upload & Analyze**
   - Upload JSON file
   - ECHOPULSE analyzes and generates brief
   - View morning brief on screen

4. **Review Brief**
   - Read Kevin Xu pick of the day
   - Check alternates and watching list
   - Verify links and catalysts
   - Make trading decision

---

## Data Format

Expected JSON structure:

```json
{
  "date": "2025-11-11",
  "candidates": [
    {
      "ticker": "RDDT",
      "name": "Reddit Inc",
      "price": 45.20,
      "market_cap": 7500000000,
      "volume": 15000000,
      "mentions_24h": 450,
      "buzz_ratio": 3.2,
      "velocity_1h": 85,
      "platforms": ["reddit", "twitter", "stocktwits"],
      "catalyst": "Earnings Report",
      "catalyst_date": "2025-11-18",
      "rumor": "Beat expectations expected, new AI features announcement",
      "rumor_confidence": 2,
      "sources": [
        "https://www.reddit.com/r/stocks/...",
        "https://twitter.com/trader123/..."
      ],
      "fundamentals": {
        "revenue_growing": true,
        "profitable": false,
        "path_to_profit": true,
        "red_flags": false,
        "debt_manageable": true,
        "dilution_ok": true
      },
      "health_score": 4
    }
  ]
}
```

---

## API Endpoints

- `GET /` - Web UI
- `GET /health` - Health check
- `POST /api/upload` - Upload JSON file for analysis
- `POST /api/analyze` - Analyze data (JSON body)
- `GET /api/sample-data` - Get sample data template
- `GET /api/briefs` - List all briefs
- `GET /api/briefs/{date}` - Get specific brief

---

## Project Structure

```
echopulse-scanner/
├── app.py                    # FastAPI web application
├── analyzer.py               # ECHOPULSE v3.0 analysis logic
├── requirements.txt          # Python dependencies
├── railway.json              # Railway configuration
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── data/                    # Uploaded data files
├── briefs/                  # Generated briefs
├── trades/                  # Trade log (Phase 2)
├── templates/               # HTML templates
│   └── index.html          # Web UI
└── static/                 # Static files (CSS/JS)
```

---

## Environment Variables (Phase 2)

For automated data collection:

```bash
ALPHA_VANTAGE_API_KEY=your_key_here
TZ=America/New_York
```

Set in Railway dashboard → Variables

---

## Roadmap

### ✅ Phase 1: Manual MVP (COMPLETE)
- Web app deployment
- Manual data upload
- ECHOPULSE analysis
- Brief generation

### ✅ Phase 2: Automation (COMPLETE)
- Automated data collection (yfinance, Reddit/PRAW)
- Scheduled 8 AM EST runs (GitHub Actions)
- Real API integrations with fundamentals
- Trade tracking system with P&L

### ✅ Phase 3: MCP Intelligence Layer (COMPLETE)
- Tavily MCP integration for rumor verification with historical data
- Sequential Thinking MCP for multi-step quality analysis
- Memory MCP for pattern tracking across scans
- Evidence-based scoring with confidence levels

### 🔄 Phase 4: Optimization (ONGOING)
- Performance tracking
- Algorithm refinement
- Sector-specific logic
- Historical analysis

---

## Phase 3: MCP Intelligence Layer

### What's Enhanced

**Tavily MCP - Real Catalyst Verification**
- Searches the web for actual earnings dates and news
- Provides historical pre-earnings patterns and win rates
- Verifies rumors with credible sources
- Example: "NVDA earnings Nov 19 @ 4PM, 75% historical win rate, 3.9% avg gain"

**Sequential Thinking MCP - Deep Analysis**
- Multi-step reasoning about trade quality
- Risk assessment with evidence
- Entry/exit strategy optimization
- Quality scoring (0-100) with confidence levels (1-3 stars)

**Memory MCP - Pattern Tracking**
- Stores winning setups and patterns across scans
- Tracks what characteristics lead to successful trades
- Learns from historical performance
- Example: "Pre-earnings momentum pattern: 75% win rate for high-quality tech"

### How to Use

Phase 3 enhancements run automatically when Claude Code executes the scanner with MCP access.

**Demo Script**:
```bash
python demo_mcp_scan.py
```

Shows the difference between Phase 2 (automated data) and Phase 3 (intelligent analysis).

**Value Add**:
- Phase 2: Generic catalyst data
- Phase 3: Real verification with historical win rates

- Phase 2: Basic scoring
- Phase 3: Multi-step reasoning with confidence levels

- Phase 2: No memory
- Phase 3: Learns patterns across scans

---

## Legal Disclaimer

⚠️ **FOR PERSONAL USE ONLY**

This tool is for research and analysis purposes only. It is NOT investment advice.

- You are responsible for all trading decisions and losses
- Always verify rumors and catalysts independently
- Use proper position sizing (2-5% max per trade)
- Rumor trading carries significant risk
- Expected win rate: 40-50%

---

## Support

For issues or questions:
1. Check Railway logs for errors
2. Test locally first before debugging Railway
3. Verify data format matches expected structure

---

**ECHOPULSE v3.0** - Built for Railway
*Personal Rumor Trading Edition*
