from app.tools import analyze_server_health


def test_high_cpu_is_detected():
    result = analyze_server_health(
        "web-01", 92, 60, 50
    )
    assert "CRITICAL CPU usage" in result


def test_healthy_server():
    result = analyze_server_health(
        "web-02", 30, 45, 50
    )
    assert "No configured resource thresholds exceeded" in result


def test_invalid_metric_is_rejected():
    result = analyze_server_health(
        "web-03", 120, 45, 50
    )
    assert "Invalid input" in result