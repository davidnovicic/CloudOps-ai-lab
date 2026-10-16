from app.agent import run_health_agent


def test_agent_reports_high_cpu():
    result = run_health_agent(
        "web-01", 92, 78, 65
    )

    assert result["agent"] == "CloudOps Health Agent"
    assert result["mode"] == "deterministic_demo"
    assert "CRITICAL CPU usage" in result["analysis"]


def test_agent_reports_healthy_server():
    result = run_health_agent(
        "web-02", 30, 45, 50
    )

    assert "No configured resource thresholds exceeded" in result["analysis"]