from dataclasses import dataclass
from statistics import mean


@dataclass
class RiskResult:
    score: float
    level: str
    indicators: list[str]


class RiskEngine:
    def evaluate(self, transactions: list[dict], customer_risk: str) -> RiskResult:
        if not transactions:
            return RiskResult(0.0, "LOW", ["No transactions available"])

        score = 0.0
        indicators: list[str] = []
        amounts = [float(t["amount"]) for t in transactions]
        total = sum(amounts)
        new_bens = sum(1 for t in transactions if t.get("is_new_beneficiary"))
        countries = {t.get("beneficiary_country") for t in transactions}

        if total >= 25000:
            score += 30
            indicators.append(f"Elevated aggregate transaction value: ${total:,.2f}")
        if new_bens >= 2:
            score += 25
            indicators.append(f"Concentration of activity to {new_bens} new beneficiaries")
        if len(countries) >= 3:
            score += 20
            indicators.append(f"Geographic dispersion across {len(countries)} beneficiary countries")
        if max(amounts) > mean(amounts) * 1.5 and len(amounts) > 2:
            score += 15
            indicators.append("Material transaction-size deviation within the review window")
        if customer_risk.upper() in {"HIGH", "MEDIUM"}:
            score += 10 if customer_risk.upper() == "MEDIUM" else 20
            indicators.append(f"Existing customer risk rating: {customer_risk.upper()}")

        score = min(score, 100.0)
        level = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
        return RiskResult(score, level, indicators or ["No material configured indicators detected"])
