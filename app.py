"""
ECHOPULSE v3.0 - Personal Rumor Trading Scanner
Railway-deployed FastAPI application
"""

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Any

from analyzer import EchoPulseAnalyzer

# Initialize FastAPI
app = FastAPI(title="ECHOPULSE Scanner", version="3.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize analyzer
analyzer = EchoPulseAnalyzer()

# Data directories
DATA_DIR = Path("data")
BRIEFS_DIR = Path("briefs")
TRADES_DIR = Path("trades")

# Ensure directories exist
for dir in [DATA_DIR, BRIEFS_DIR, TRADES_DIR]:
    dir.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - view latest brief or upload data"""

    # Get latest brief if exists
    briefs = sorted(BRIEFS_DIR.glob("morning_brief_*.md"), reverse=True)
    latest_brief = None
    brief_content = None

    if briefs:
        latest_brief = briefs[0]
        with open(latest_brief, "r") as f:
            brief_content = f.read()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "latest_brief": latest_brief.name if latest_brief else None,
        "brief_content": brief_content,
        "today": datetime.now().strftime("%Y-%m-%d")
    })


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "version": "3.0"}


@app.post("/api/analyze")
async def analyze_data(data: Dict[str, Any]):
    """
    Analyze stock data and generate ECHOPULSE brief

    Expected data format:
    {
        "candidates": [
            {
                "ticker": "AAPL",
                "mentions_24h": 150,
                "buzz_ratio": 2.5,
                "price": 180.50,
                "market_cap": 2800000000000,
                "volume": 50000000,
                "catalyst": "Earnings 2025-11-15",
                "rumor_text": "New product launch rumored",
                "sources": ["reddit", "twitter"]
            }
        ]
    }
    """
    try:
        # Run ECHOPULSE analysis
        brief = analyzer.analyze(data)

        # Save brief to file
        today = datetime.now().strftime("%Y-%m-%d")
        brief_file = BRIEFS_DIR / f"morning_brief_{today}.md"

        with open(brief_file, "w") as f:
            f.write(brief)

        return JSONResponse({
            "status": "success",
            "brief_file": str(brief_file),
            "brief_content": brief
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


@app.post("/api/upload")
async def upload_data(file: UploadFile = File(...)):
    """Upload JSON data file for analysis"""
    try:
        # Read uploaded file
        contents = await file.read()
        data = json.loads(contents)

        # Save to data directory
        today = datetime.now().strftime("%Y-%m-%d")
        data_file = DATA_DIR / f"scan_{today}.json"

        with open(data_file, "w") as f:
            json.dump(data, f, indent=2)

        # Run analysis
        brief = analyzer.analyze(data)

        # Save brief
        brief_file = BRIEFS_DIR / f"morning_brief_{today}.md"
        with open(brief_file, "w") as f:
            f.write(brief)

        return JSONResponse({
            "status": "success",
            "data_file": str(data_file),
            "brief_file": str(brief_file),
            "brief_content": brief
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


@app.get("/api/briefs")
async def list_briefs():
    """List all generated briefs"""
    briefs = sorted(BRIEFS_DIR.glob("morning_brief_*.md"), reverse=True)

    return JSONResponse({
        "briefs": [
            {
                "filename": b.name,
                "date": b.stem.replace("morning_brief_", ""),
                "size": b.stat().st_size
            }
            for b in briefs
        ]
    })


@app.get("/api/briefs/{date}")
async def get_brief(date: str):
    """Get specific brief by date (YYYY-MM-DD)"""
    brief_file = BRIEFS_DIR / f"morning_brief_{date}.md"

    if not brief_file.exists():
        return JSONResponse({
            "status": "error",
            "message": f"Brief for {date} not found"
        }, status_code=404)

    with open(brief_file, "r") as f:
        content = f.read()

    return JSONResponse({
        "date": date,
        "content": content
    })


@app.get("/api/sample-data")
async def get_sample_data():
    """Get sample data template for testing"""
    sample = {
        "date": datetime.now().strftime("%Y-%m-%d"),
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
                    "revenue_growing": True,
                    "profitable": False,
                    "path_to_profit": True,
                    "red_flags": False,
                    "debt_manageable": True,
                    "dilution_ok": True
                },
                "health_score": 4
            },
            {
                "ticker": "NVDA",
                "name": "NVIDIA Corporation",
                "price": 495.30,
                "market_cap": 1220000000000,
                "volume": 45000000,
                "mentions_24h": 320,
                "buzz_ratio": 2.8,
                "velocity_1h": 62,
                "platforms": ["reddit", "twitter"],
                "catalyst": "AI Partnership Rumor",
                "catalyst_date": "2025-11-20",
                "rumor": "Major cloud provider partnership announcement expected",
                "rumor_confidence": 2,
                "sources": [
                    "https://twitter.com/techanalyst/..."
                ],
                "fundamentals": {
                    "revenue_growing": True,
                    "profitable": True,
                    "path_to_profit": True,
                    "red_flags": False,
                    "debt_manageable": True,
                    "dilution_ok": True
                },
                "health_score": 5
            }
        ]
    }

    return JSONResponse(sample)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
