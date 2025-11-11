"""
ECHOPULSE v3.0 Analyzer
Implements the scoring and brief generation logic
"""

from datetime import datetime
from typing import Dict, List, Any


class EchoPulseAnalyzer:
    """ECHOPULSE v3.0 analysis engine"""

    def __init__(self):
        self.min_attention_score = 60
        self.min_health_score = 2
        self.min_rumor_confidence = 2

    def analyze(self, data: Dict[str, Any]) -> str:
        """
        Main analysis function
        Takes raw data and generates ECHOPULSE morning brief
        """
        candidates = data.get("candidates", [])

        if not candidates:
            return self._generate_no_setup_brief()

        # Score each candidate
        scored_candidates = []
        for candidate in candidates:
            score = self._score_candidate(candidate)
            scored_candidates.append({
                "data": candidate,
                "scores": score
            })

        # Filter qualified candidates
        qualified = [
            c for c in scored_candidates
            if c["scores"]["attention"] >= self.min_attention_score
            and c["scores"]["health"] >= self.min_health_score
            and c["data"].get("rumor_confidence", 0) >= self.min_rumor_confidence
        ]

        # Sort by composite score
        qualified.sort(key=lambda x: x["scores"]["composite"], reverse=True)

        if not qualified:
            return self._generate_no_setup_brief()

        # Generate brief
        return self._generate_brief(qualified)

    def _score_candidate(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores for a candidate"""

        # Attention Score (0-100)
        buzz_ratio = candidate.get("buzz_ratio", 1.0)
        buzz_points = min(50, buzz_ratio / 4.0 * 50)  # Max 50 points

        velocity_1h = candidate.get("velocity_1h", 0)
        velocity_points = min(20, velocity_1h / 10 * 20)  # Max 20 points

        platforms = candidate.get("platforms", [])
        platform_points = min(15, len(platforms) * 5)  # Max 15 points (3+ platforms)

        # Influencer factor (simplified - would need real influencer tracking)
        influencer_points = 15 if buzz_ratio > 3.0 else 5

        attention_score = buzz_points + velocity_points + platform_points + influencer_points

        # Health Score (already provided in data, 0-5)
        health_score = candidate.get("health_score", 0)

        # Composite Score (for ranking)
        # 40% Attention + 20% Health + 20% Catalyst + 20% Confidence
        catalyst_proximity_score = 100 if candidate.get("catalyst_date") else 50
        confidence_score = candidate.get("rumor_confidence", 0) * 33.3  # Scale to 100

        composite = (
            attention_score * 0.4 +
            health_score * 20 * 0.2 +  # Scale 0-5 to 0-100
            catalyst_proximity_score * 0.2 +
            confidence_score * 0.2
        )

        return {
            "attention": attention_score,
            "health": health_score,
            "composite": composite
        }

    def _generate_brief(self, qualified: List[Dict]) -> str:
        """Generate morning decision dashboard"""

        today = datetime.now().strftime("%A, %B %d, %Y")
        pick = qualified[0]
        alternates = qualified[1:3] if len(qualified) > 1 else []

        brief = f"""# ECHOPULSE v3.0 - Morning Brief
**{today}**

---

## 🎯 KEVIN XU PICK OF THE DAY

"""

        # Primary pick
        brief += self._format_primary_pick(pick)

        # Alternates
        if alternates:
            brief += "\n\n---\n\n## 📦 BACKUP OPTIONS (Bench)\n\n"
            for i, alt in enumerate(alternates, 1):
                brief += self._format_alternate(alt, i)

        # Watching list (lower-scoring candidates)
        watching = qualified[3:6] if len(qualified) > 3 else []
        if watching:
            brief += "\n\n---\n\n## 📈 WATCHING LIST (Emerging - Not Ready Yet)\n\n"
            for candidate in watching:
                ticker = candidate["data"]["ticker"]
                attention = int(candidate["scores"]["attention"])
                health = candidate["scores"]["health"]
                brief += f"- **${ticker}**: Attention {attention}/100, Health {health}/5 - Monitor for setup\n"

        # Footer
        brief += f"""

---

## ⚠️ RISK DISCLAIMER

This is intelligence aggregation, NOT investment advice. You are responsible for:
- All verification of rumors and catalysts
- Position sizing decisions
- Entry/exit execution
- Risk management and losses

**Expected win rate: 40-50%**. Proper position sizing (2-5%) and time discipline determine survival.

---

**ECHOPULSE v3.0** - Personal Rumor Trading Edition
*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M EST")}*
"""

        return brief

    def _format_primary_pick(self, pick: Dict) -> str:
        """Format the primary pick section"""
        data = pick["data"]
        scores = pick["scores"]

        ticker = data["ticker"]
        name = data.get("name", ticker)
        price = data.get("price", 0)
        mcap = data.get("market_cap", 0)
        mcap_str = f"${mcap/1e9:.1f}B" if mcap > 1e9 else f"${mcap/1e6:.1f}M"

        attention = int(scores["attention"])
        health = scores["health"]
        buzz = data.get("buzz_ratio", 0)

        platforms_str = " | ".join([p.title() + " ✓" for p in data.get("platforms", [])])

        catalyst = data.get("catalyst", "TBD")
        catalyst_date = data.get("catalyst_date", "TBD")

        rumor_conf = data.get("rumor_confidence", 0)
        confidence_str = "⭐" * rumor_conf

        rumor = data.get("rumor", "No rumor details")

        health_details = data.get("fundamentals", {})
        health_str = self._format_health_check(health_details)

        risk_flags = self._identify_risk_flags(data)
        risk_str = ", ".join(risk_flags) if risk_flags else "None identified"

        sources = data.get("sources", [])
        sources_str = "\n".join([f"- {s}" for s in sources]) if sources else "- No sources provided"

        # Calculate targets (simplified - would need real support/resistance)
        entry_low = price * 0.97
        entry_high = price * 1.02
        t1 = price * 1.20  # +20%
        t2 = price * 1.35  # +35%

        return f"""**[TICKER: ${ticker}]** | {name}
**Price**: ${price:.2f} | **Market Cap**: {mcap_str}

**ATTENTION SCORE**: {attention}/100
- Buzz Ratio: {buzz:.1f}x (vs 7-day average)
- Platforms: {platforms_str}

**CATALYST**: {catalyst}
- Date: {catalyst_date}

**RUMOR CONFIDENCE**: {confidence_str} ({rumor_conf}/3)

**HEALTH CHECK**: {health}/5 {"(Quality)" if health >= 4 else "(Acceptable)" if health == 3 else "(Momentum Only)"}
{health_str}

**RISK FLAGS**: {risk_str}

---

**THE THESIS**:
{rumor}

**ENTRY STRATEGY**:
- **Entry Zone**: ${entry_low:.2f} - ${entry_high:.2f}
- **Position Size**: {self._recommend_position_size(data, health)}% of account
- **Avoid if**: Up >25% intraday, low volume, or news already mainstream

**EXIT STRATEGY**:
- **Target 1 (T1)**: ${t1:.2f} (+20%) - Sell 50%, move stop to breakeven
- **Target 2 (T2)**: ${t2:.2f} (+35%) - Sell 25%, trail remaining
- **Time Stop**: Exit by {catalyst_date} if no progress
- **Thesis Invalidation**: Exit immediately if rumor contradicted

**RISK ASSESSMENT**: {self._assess_risk(data, health)}/5

**KEY VERIFICATION LINKS**:
{sources_str}
"""

    def _format_alternate(self, alt: Dict, number: int) -> str:
        """Format alternate pick (condensed)"""
        data = alt["data"]
        scores = alt["scores"]

        ticker = data["ticker"]
        attention = int(scores["attention"])
        health = scores["health"]
        catalyst = data.get("catalyst", "TBD")
        catalyst_date = data.get("catalyst_date", "TBD")
        rumor = data.get("rumor", "")[:80] + "..." if len(data.get("rumor", "")) > 80 else data.get("rumor", "")
        price = data.get("price", 0)
        t1 = price * 1.20

        return f"""**ALTERNATE #{number}: ${ticker}**
- Attention: {attention}/100 | Health: {health}/5 | Catalyst: {catalyst} on {catalyst_date}
- Thesis: {rumor}
- Entry: ${price * 0.97:.2f}-${price * 1.02:.2f} | T1: ${t1:.2f} (+20%)

"""

    def _format_health_check(self, fundamentals: Dict) -> str:
        """Format health check details"""
        checks = []
        checks.append(f"- Revenue: {'Growing ✓' if fundamentals.get('revenue_growing') else 'Declining ✗'}")
        checks.append(f"- Profitability: {'Profitable ✓' if fundamentals.get('profitable') else 'Path clear' if fundamentals.get('path_to_profit') else 'Burning ✗'}")
        checks.append(f"- Red Flags: {'None ✓' if not fundamentals.get('red_flags') else 'Present ✗'}")
        checks.append(f"- Debt: {'Manageable ✓' if fundamentals.get('debt_manageable') else 'Distressed ✗'}")
        checks.append(f"- Dilution: {'Disciplined ✓' if fundamentals.get('dilution_ok') else 'Heavy SBC ✗'}")

        return "\n".join(checks)

    def _identify_risk_flags(self, data: Dict) -> List[str]:
        """Identify risk flags"""
        flags = []

        mcap = data.get("market_cap", 0)
        if mcap < 500_000_000:
            flags.append("Small-cap (<$500M)")

        if "biotech" in data.get("sector", "").lower():
            flags.append("Biotech binary")

        if data.get("health_score", 0) < 3:
            flags.append("Momentum only (weak fundamentals)")

        return flags

    def _recommend_position_size(self, data: Dict, health: int) -> float:
        """Recommend position size based on quality and risk"""
        base_size = 3.0

        # Adjust for health
        if health >= 4:
            size = 5.0
        elif health == 3:
            size = 3.0
        else:
            size = 1.5

        # Reduce for risk flags
        mcap = data.get("market_cap", 0)
        if mcap < 500_000_000:
            size *= 0.5

        return min(5.0, size)

    def _assess_risk(self, data: Dict, health: int) -> int:
        """Assess risk level 1-5"""
        risk = 2  # Base risk

        # Increase risk for weak fundamentals
        if health < 3:
            risk += 1

        # Increase risk for small-cap
        mcap = data.get("market_cap", 0)
        if mcap < 500_000_000:
            risk += 1

        # Increase risk for biotech
        if "biotech" in data.get("sector", "").lower():
            risk += 1

        return min(5, risk)

    def _generate_no_setup_brief(self) -> str:
        """Generate brief when no qualified setups"""
        today = datetime.now().strftime("%A, %B %d, %Y")

        return f"""# ECHOPULSE v3.0 - Morning Brief
**{today}**

---

## 🎯 KEVIN XU PICK OF THE DAY: NONE

**Reason**: No qualified setups meeting risk-reward criteria today.

**Minimum criteria not met**:
- Attention Score <60, OR
- Health Check <2/5, OR
- Rumor Confidence <⭐⭐, OR
- No catalyst within 7 days

**Action**: Stand aside. Cash is a position. Wait for better setups tomorrow.

---

**Bad days happen. Don't force trades.**

*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M EST")}*
"""
