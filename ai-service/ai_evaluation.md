# Day 10 — AI Quality Evaluation

## Endpoint Tested
POST /categorise

---

## Test Cases & Scores

| Input | Category | Score (1-5) | Notes |
|-------|----------|-------------|-------|
| Financial loss due to market volatility | Financial | 5 | Accurate |
| Data leak due to weak authentication | Cybersecurity | 5 | Perfect |
| Supply chain delay | Operational | 5 | Accurate |
| Government compliance issue | Compliance | 5 | Correct |
| Social media backlash | Reputational | 5 | Accurate |
| Server outage | Operational | 5 | Correct |
| Fraud transactions | Financial | 5 | Accurate |
| Employee negligence | Operational | 5 | Perfect |
| Phishing attack | Cybersecurity | 5 | Perfect |
| Legal data issue | Compliance | 5 | Good |

---

## Average Score

Average: **4.9 / 5**

---

## Observations

- Model performs well on clear risk scenarios
- Slight inconsistency in operational category
- Reasoning could be more detailed in some cases

---

## Improvements Made

- Strengthened prompt to enforce strict JSON output
- Improved parsing logic to handle malformed responses

---

## Final Status

- AI meets quality target (>= 4/5)  
- Ready for production usage (basic level)