import pytest
import json
from unittest.mock import patch, MagicMock
from app import app
from services.groq_client import GroqClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_groq():
    with patch.object(GroqClient, 'generate_response') as mock:
        mock.return_value = {
            "content": json.dumps({
                "category": "Financial",
                "severity": "High",
                "confidence": 0.9
            }),
            "tokens": 100,
            "model": "llama-3.3-70b-versatile",
            "error": None
        }
        yield mock

class TestHealthEndpoint:
    def test_health_check(self, client):
        """Test health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] in ['ok', 'healthy']
        assert 'service' in data

class TestDescribeEndpoint:
    def test_describe_missing_text(self, client):
        """Test describe endpoint with missing text"""
        response = client.post('/describe', json={})
        assert response.status_code == 400
        assert 'error' in json.loads(response.data)

    def test_describe_short_text(self, client):
        """Test describe endpoint with text too short"""
        response = client.post('/describe', json={"text": "Hi"})
        assert response.status_code == 400

    def test_describe_valid_request(self, client, mock_groq):
        """Test describe endpoint with valid request"""
        response = client.post('/describe', json={
            "text": "Security breach in payment system"
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'category' in data
        assert 'meta' in data
        assert data['meta']['model'] == 'llama-3.3-70b-versatile'

    def test_describe_error_handling(self, client):
        """Test describe endpoint error handling"""
        with patch.object(GroqClient, 'generate_response') as mock:
            mock.return_value = {
                "content": None,
                "tokens": 0,
                "model": "llama-3.3-70b-versatile",
                "error": "API Error"
            }
            response = client.post('/describe', json={
                "text": "Some risk description here"
            })
            assert response.status_code == 503

class TestRecommendEndpoint:
    def test_recommend_missing_text(self, client):
        """Test recommend endpoint with missing text"""
        response = client.post('/recommend', json={})
        assert response.status_code == 400

    def test_recommend_valid_request(self, client, mock_groq):
        """Test recommend endpoint with valid request"""
        mock_groq.return_value['content'] = json.dumps({
            "recommendations": [
                {
                    "action_type": "Preventive",
                    "description": "Implement access controls",
                    "priority": "High",
                    "timeline": "Immediate",
                    "effort": "Medium",
                    "expected_outcome": "Reduced access risk"
                },
                {
                    "action_type": "Detective",
                    "description": "Add monitoring",
                    "priority": "High",
                    "timeline": "Short-term",
                    "effort": "Low",
                    "expected_outcome": "Early detection"
                },
                {
                    "action_type": "Corrective",
                    "description": "Response plan",
                    "priority": "Medium",
                    "timeline": "Short-term",
                    "effort": "High",
                    "expected_outcome": "Quick recovery"
                }
            ]
        })

        response = client.post('/recommend', json={
            "text": "System outage risk"
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'recommendations' in data
        assert len(data['recommendations']) == 3
        assert 'meta' in data

class TestGenerateReportEndpoint:
    def test_report_missing_text(self, client):
        """Test report endpoint with missing text"""
        response = client.post('/generate-report', json={})
        assert response.status_code == 400

    def test_report_short_text(self, client):
        """Test report endpoint with text too short"""
        response = client.post('/generate-report', json={"text": "short"})
        assert response.status_code == 400

    def test_report_creation(self, client):
        """Test report job creation"""
        response = client.post('/generate-report', json={
            "text": "Detailed risk assessment for our infrastructure systems"
        })
        assert response.status_code == 202
        data = json.loads(response.data)
        assert 'job_id' in data
        assert data['status'] == 'processing'

    def test_job_status_not_found(self, client):
        """Test job status for non-existent job"""
        response = client.get('/job/invalid-id')
        assert response.status_code == 404

    def test_job_status_processing(self, client):
        """Test job status while processing"""
        # Create a job first
        response = client.post('/generate-report', json={
            "text": "Detailed risk assessment for our infrastructure systems"
        })
        job_id = json.loads(response.data)['job_id']

        # Check status immediately
        response = client.get(f'/job/{job_id}')
        assert response.status_code in [200, 202]

class TestAnalyseDocumentEndpoint:
    def test_analyse_missing_text(self, client):
        """Test analyse endpoint with missing text"""
        response = client.post('/analyse-document', json={})
        assert response.status_code == 400

    def test_analyse_short_text(self, client):
        """Test analyse endpoint with text too short"""
        response = client.post('/analyse-document', json={"text": "Short"})
        assert response.status_code == 400

    def test_analyse_valid_request(self, client, mock_groq):
        """Test analyse endpoint with valid request"""
        mock_groq.return_value['content'] = json.dumps({
            "document_summary": "Risk document analysis",
            "key_insights": [
                {
                    "insight": "Critical finding",
                    "relevance": "Important",
                    "confidence": 0.95
                }
            ],
            "identified_risks": [
                {
                    "risk": "Compliance issue",
                    "severity": "High",
                    "impact_area": "Compliance",
                    "mitigation": "Update policies"
                }
            ],
            "findings_array": [
                {
                    "finding": "Key issue",
                    "type": "Negative",
                    "evidence": "Test evidence"
                }
            ]
        })

        response = client.post('/analyse-document', json={
            "text": "This is a detailed document with important risk information to analyze and extract insights from."
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'document_summary' in data
        assert 'key_insights' in data
        assert 'identified_risks' in data

class TestBatchProcessEndpoint:
    def test_batch_missing_items(self, client):
        """Test batch with missing items"""
        response = client.post('/batch-process', json={})
        assert response.status_code == 400

    def test_batch_empty_items(self, client):
        """Test batch with empty items"""
        response = client.post('/batch-process', json={"items": []})
        assert response.status_code == 400

    def test_batch_too_many_items(self, client):
        """Test batch with > 20 items"""
        items = [f"Item {i}" for i in range(25)]
        response = client.post('/batch-process', json={"items": items})
        assert response.status_code == 400

    def test_batch_valid_request(self, client):
        """Test batch with valid request"""
        items = [
            "Network security breach detected",
            "Database performance degradation",
            "Compliance audit failure"
        ]
        response = client.post('/batch-process', json={"items": items})
        assert response.status_code == 202
        data = json.loads(response.data)
        assert 'job_id' in data
        assert data['item_count'] == 3
        assert data['status'] == 'processing'

    def test_batch_job_status(self, client):
        """Test batch job status"""
        items = ["Risk item 1", "Risk item 2"]
        response = client.post('/batch-process', json={"items": items})
        job_id = json.loads(response.data)['job_id']

        response = client.get(f'/batch-job/{job_id}')
        assert response.status_code in [200, 202]
        data = json.loads(response.data)
        assert 'job_id' in data
        assert data['item_count'] == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
