# Risk Heatmap Visualiser
# AI Risk Analysis Service

An AI-powered backend service that analyzes user input, categorizes risks, generates reports, and provides intelligent insights using LLMs.

Built as part of a structured 4-week MVP sprint.

---

##  Features

###  Core AI Features
-  Risk Categorisation (`/categorise`)
-  AI Report Generation (`/generate-report`)
-  Structured JSON responses
-  Async job processing for long tasks

###  Performance & Optimization
-  In-memory caching (SHA256 keys)
-  Reduced latency using cache hits
-  Benchmarking (p50, p95, p99)

###  Reliability
-  Retry logic for API calls
-  Fallback (rule-based classification if AI fails)
-  Robust JSON cleaning

###  Security
-  Prompt injection detection
-  Input sanitisation (HTML stripping, length checks)
-  OWASP considerations (documented)

###  Observability
-  `/health` endpoint
-  Cache hit/miss stats
-  Uptime tracking

---

##  Tech Stack

- **Backend:** Flask
- **AI Model:** Groq (LLaMA 3.3 70B)
- **Vector DB:** ChromaDB
- **Caching:** In-memory (Day 8 fallback for Redis)
- **Language:** Python 3.12

---

## Project Structure
   |
   |---routes/
   | |---categorize.py
   | |---generate_report.py
   | |---health.py
   |
   |---services/
   | |---groq_client.py
   | |---cache.py
   | |---job_store.py
   | |---vector_store.py
   |
   |app.py
   |benchmark.py
   |requirements.txt
   |README.md

---

##  Setup Instructions

### 1. Clone the repo
git clone <https://github.com/camcode17/ayushi-ai-dev2>
cd ai-service 

### 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate 

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Setup environment variables
GROQ_API_KEY=your_api_key_here

### 5. Running the server
python app.py

---

## API Endpoints

### 1. Categorise Risk

- POST /categorise

{
  "text": "Company may face financial loss due to market volatility"
}

- Response:

{
  "category": "Financial",
  "confidence": 0.8,
  "severity": "Medium",
  "impact": 3,
  "reasoning": "...",
  "meta": {
    "cached": false,
    "response_time_ms": 1200
  }
}
### 2. Generate Report (Async)

- POST /generate-report

{
  "text": "System has weak security and financial risks"
}

- Response:

{
  "job_id": "uuid",
  "status": "processing"
}
### 3. Get Report Result

- GET /job/<job_id>

### 4. Health Check

- GET /health

{
  "status": "OK",
  "cache": {
    "hits": 5,
    "misses": 3
  },
  "uptime_seconds": 120.5
}

---

## Benchmarking

- Run performance test:
python benchmark.py

- Outputs:

p50: ~2000 ms
p95: ~2300 ms
p99: ~2400 ms

---

## AI Quality

Tested with 10+ inputs per endpoint
Average accuracy ≥ 4/5
Prompt tuning applied for consistency

---

## Fallback Strategy

- If AI fails:
Rule-based classification is used
Default response returned with low confidence

---

## Security Measures
Input sanitisation
Prompt injection detection
Length validation
Safe JSON parsing

---

## Future Improvements
Redis caching (production-ready)
Streaming responses
Advanced RAG pipeline
Authentication & rate limiting

---

## Author

Ayushi M Vasanad
AI Developer

---