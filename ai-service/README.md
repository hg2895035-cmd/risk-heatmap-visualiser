# Risk Heatmap Visualiser - AI Service

Flask-based AI microservice for the Risk Heatmap Visualiser tool. Provides LLM-powered risk analysis, recommendations, and reporting capabilities.

**Port:** 5000  
**Health Check:** `http://localhost:5000/health`

---

## Prerequisites

- Python 3.11+
- Redis 7+ (optional, for caching)
- Groq API key (free tier available at console.groq.com)
- 4GB+ RAM recommended

---

## Setup Steps

### 1. Environment Variables

Create `.env` file:

```bash
GROQ_API_KEY=your_api_key_here
REDIS_URL=redis://localhost:6379/0
CHROMADB_PATH=./chroma_data
FLASK_ENV=production
```

Get Groq API key from: https://console.groq.com

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Service

```bash
python app.py
```

Service starts on `http://localhost:5000`

---

## API Endpoints Reference

### 1. Health Check
**GET** `/health`

Check service status.

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "ai-service",
  "timestamp": "2026-05-10T10:30:00.000000",
  "cache": {"hits": 0, "misses": 0, "keys": 0}
}
```

---

### 2. Describe Risk
**POST** `/describe`

Analyze and describe a risk in detail.

**Request:**
```json
{
  "text": "Security breach in payment system affecting customer data"
}
```

**Response:**
```json
{
  "title": "Payment System Security Breach",
  "category": "Cybersecurity",
  "severity": "Critical",
  "confidence": 0.95,
  "description": "Detailed analysis of the security breach...",
  "impact": {
    "business": "Customer trust erosion, potential business disruption",
    "financial": "Potential fines up to $X per customer",
    "stakeholders": "Customers, regulators, employees"
  },
  "root_causes": ["Unpatched vulnerability", "Insufficient access controls"],
  "mitigation": "Immediate patching and incident response",
  "meta": {
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 245,
    "response_time_ms": 1234,
    "cached": false,
    "generated_at": "2026-05-10T10:30:00.000000"
  }
}
```

---

### 3. Get Recommendations
**POST** `/recommend`

Generate 3 actionable recommendations for a risk.

**Request:**
```json
{
  "text": "Database performance degradation"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "action_type": "Preventive",
      "description": "Implement query optimization and indexing strategy",
      "priority": "High",
      "timeline": "Immediate",
      "effort": "Medium",
      "expected_outcome": "Performance improvement by 40-60%"
    },
    {
      "action_type": "Detective",
      "description": "Deploy database monitoring and alerting",
      "priority": "High",
      "timeline": "Short-term",
      "effort": "Low",
      "expected_outcome": "Early detection of performance issues"
    },
    {
      "action_type": "Corrective",
      "description": "Develop incident response runbook",
      "priority": "Medium",
      "timeline": "Short-term",
      "effort": "High",
      "expected_outcome": "Faster recovery from similar incidents"
    }
  ],
  "meta": {
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 512,
    "response_time_ms": 2100,
    "cached": false,
    "generated_at": "2026-05-10T10:30:00.000000"
  }
}
```

---

### 4. Generate Report (Async)
**POST** `/generate-report`

Create async job to generate comprehensive risk report.

**Request:**
```json
{
  "text": "We experienced a 4-hour outage in our primary data center affecting all services..."
}
```

**Response:** (Async - returns 202)
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "status_url": "/job/550e8400-e29b-41d4-a716-446655440000"
}
```

**Check Status:** `GET /job/{job_id}`

```json
{
  "title": "Data Center Outage Report",
  "executive_summary": "4-hour outage caused by hardware failure...",
  "overview": "Complete incident analysis and timeline...",
  "top_items": [
    {"item": "Root cause identified", "impact": "High", "description": "..."},
    {"item": "Customer impact quantified", "impact": "High", "description": "..."}
  ],
  "recommendations": [
    {"recommendation": "Add redundancy", "priority": "High", "timeline": "Immediate"}
  ],
  "meta": {
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 2048,
    "generated_at": "2026-05-10T10:30:00.000000"
  }
}
```

---

### 5. Analyse Document
**POST** `/analyse-document`

Extract insights and risks from a document.

**Request:**
```json
{
  "text": "Annual security audit report showing multiple findings in infrastructure..."
}
```

**Response:**
```json
{
  "document_summary": "Security audit highlighting critical vulnerabilities",
  "key_insights": [
    {
      "insight": "Multiple unpatched servers detected",
      "relevance": "Immediate security risk",
      "confidence": 0.98
    }
  ],
  "identified_risks": [
    {
      "risk": "Unpatched systems exploitable",
      "severity": "Critical",
      "impact_area": "Technical",
      "mitigation": "Apply patches immediately"
    }
  ],
  "findings_array": [
    {
      "finding": "10 servers pending security updates",
      "type": "Negative",
      "evidence": "Scan results from 2026-05-10"
    }
  ],
  "meta": {
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 1024,
    "response_time_ms": 1800,
    "cached": false,
    "generated_at": "2026-05-10T10:30:00.000000",
    "document_length": 2450
  }
}
```

---

### 6. Batch Process
**POST** `/batch-process`

Process up to 20 items asynchronously (100ms delay between each).

**Request:**
```json
{
  "items": [
    "Network intrusion detected",
    "Database backup failed",
    "Compliance deadline missed"
  ]
}
```

**Response:** (Async - returns 202)
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "item_count": 3,
  "status_url": "/batch-job/550e8400-e29b-41d4-a716-446655440000"
}
```

**Check Status:** `GET /batch-job/{job_id}`

```json
{
  "status": "processing",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "item_count": 3,
  "completed_count": 2,
  "progress_percent": 66
}
```

When completed:
```json
{
  "status": "completed",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "item_count": 3,
  "completed_count": 3,
  "results": [
    {
      "category": "Cybersecurity",
      "severity": "Critical",
      "confidence": 0.95,
      "summary": "Immediate response required",
      "status": "completed",
      "processing_time_ms": 1234
    },
    {
      "category": "Operational",
      "severity": "High",
      "confidence": 0.88,
      "summary": "Service recovery needed",
      "status": "completed",
      "processing_time_ms": 1156
    },
    {
      "category": "Compliance",
      "severity": "High",
      "confidence": 0.92,
      "summary": "Regulatory action required",
      "status": "completed",
      "processing_time_ms": 987
    }
  ],
  "meta": {
    "created_at": "2026-05-10T10:30:00.000000",
    "completed_at": "2026-05-10T10:30:05.000000"
  }
}
```

---

## Error Handling

All endpoints return standard error responses:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

**Common Status Codes:**
- `200` - Success
- `202` - Async job accepted (processing)
- `400` - Bad request (missing/invalid fields)
- `404` - Not found
- `429` - Rate limit exceeded
- `500` - Server error
- `503` - Service unavailable

---

## Rate Limiting

- **Default:** 30 requests per minute per IP
- **Response on limit exceeded:**

```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": "60 seconds"
}
```

---

## Caching

- **TTL:** 15 minutes by default
- **Storage:** Redis (fallback to in-memory)
- **Cache Key Format:** `endpoint:hash(input)`
- **Bypass:** Make fresh requests with different inputs

---

## Testing

Run unit tests:

```bash
pytest test_endpoints.py -v

# With coverage
pytest test_endpoints.py --cov=routes --cov=services
```

---

## Docker Deployment

Build and run:

```bash
docker build -t risk-heatmap-ai .
docker run -p 5000:5000 --env-file .env risk-heatmap-ai
```

---

## Performance Targets

| Endpoint | Target (p95) | Limit |
|----------|-------------|-------|
| /describe | < 2000ms | 1024 tokens |
| /recommend | < 2500ms | 2048 tokens |
| /generate-report | < 5000ms | 4096 tokens |
| /analyse-document | < 3000ms | 3000 tokens |
| /batch-process (per item) | < 1000ms | 500 tokens |

---

## Troubleshooting

### Groq API Error
```
Error: API key not valid
```
- Verify GROQ_API_KEY in .env
- Check API key at console.groq.com

### Redis Connection Error
```
Warning: Redis not available. Using in-memory cache.
```
- Optional - service continues without caching
- To enable: Start Redis on localhost:6379
- Or set REDIS_URL in .env

### ChromaDB Issues
```
Error: Vector store initialization failed
```
- Ensure write permissions in project directory
- Check CHROMADB_PATH setting

---

## Development

Enable debug mode:

```bash
FLASK_ENV=development python app.py
```

Watch for changes and reload automatically.

---

## Documentation

- **Groq API:** https://console.groq.com/docs
- **ChromaDB:** https://docs.trychroma.com
- **Flask:** https://flask.palletsprojects.com
- **sentence-transformers:** https://www.sbert.net

---

**Last Updated:** May 10, 2026  
**Status:** Production Ready
