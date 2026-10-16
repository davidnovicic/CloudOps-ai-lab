from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_agent_analyze_endpoint():
    response = client.post(
        "/agent/analyze",
        json={
            "server_name": "web-01",
            "cpu_percent": 92,
            "memory_percent": 78,
            "disk_percent": 65,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["agent"] == "CloudOps Health Agent"
    assert data["mode"] == "deterministic_demo"
    assert "CRITICAL CPU usage" in data["analysis"]


def test_agent_rejects_invalid_cpu():
    response = client.post(
        "/agent/analyze",
        json={
            "server_name": "web-01",
            "cpu_percent": 150,
            "memory_percent": 78,
            "disk_percent": 65,
        },
    )

    assert response.status_code == 422


def test_agent_rejects_empty_server_name():
    response = client.post(
        "/agent/analyze",
        json={
            "server_name": "",
            "cpu_percent": 50,
            "memory_percent": 50,
            "disk_percent": 50,
        },
    )

    assert response.status_code == 422

    
def test_ai_endpoint_returns_hosted_agent_result(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODEL_ID", "test-model")

    def fake_ai_agent(**kwargs):
        assert kwargs["server_name"] == "web-01"
        assert kwargs["cpu_percent"] == 92
        return {
            "agent": "CloudOps Health Agent",
            "mode": "hosted_llm",
            "model": "test-model",
            "analysis": "CRITICAL CPU usage",
        }

    monkeypatch.setattr(
        "app.main.run_llm_health_agent",
        fake_ai_agent,
    )

    response = client.post(
        "/agent/analyze-ai",
        json={
            "server_name": "web-01",
            "cpu_percent": 92,
            "memory_percent": 78,
            "disk_percent": 65,
        },
    )

    assert response.status_code == 200
    assert response.json()["mode"] == "hosted_llm"
    assert response.json()["analysis"] == "CRITICAL CPU usage"


def test_ai_endpoint_returns_503_when_unconfigured(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_MODEL_ID", raising=False)

    response = client.post(
        "/agent/analyze-ai",
        json={
            "server_name": "web-01",
            "cpu_percent": 50,
            "memory_percent": 50,
            "disk_percent": 50,
        },
    )

    assert response.status_code == 503


def test_ai_endpoint_handles_provider_failure(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODEL_ID", "test-model")

    def fake_ai_agent(**kwargs):
        raise RuntimeError("Simulated provider failure")

    monkeypatch.setattr(
        "app.main.run_llm_health_agent",
        fake_ai_agent,
    )

    response = client.post(
        "/agent/analyze-ai",
        json={
            "server_name": "web-01",
            "cpu_percent": 50,
            "memory_percent": 50,
            "disk_percent": 50,
        },
    )

    assert response.status_code == 502
    assert "hosted AI request failed" in response.json()["detail"]
