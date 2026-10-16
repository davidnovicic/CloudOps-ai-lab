from smolagents import tool


@tool
def analyze_server_health(
    server_name: str,
    cpu_percent: float,
    memory_percent: float,
    disk_percent: float,
) -> str:
    """Analyze synthetic server metrics and return health findings.

    Args:
        server_name: Name of the server being analyzed.
        cpu_percent: CPU usage percentage, from 0 to 100.
        memory_percent: Memory usage percentage, from 0 to 100.
        disk_percent: Disk usage percentage, from 0 to 100.
    """
    metrics = {
        "cpu": cpu_percent,
        "memory": memory_percent,
        "disk": disk_percent,
    }

    if not server_name.strip():
        return "Invalid input: server name is required."

    if any(value < 0 or value > 100 for value in metrics.values()):
        return "Invalid input: metrics must be between 0 and 100."

    findings = []

    if cpu_percent >= 90:
        findings.append("CRITICAL CPU usage")
    elif cpu_percent >= 75:
        findings.append("HIGH CPU usage")

    if memory_percent >= 90:
        findings.append("CRITICAL memory usage")
    elif memory_percent >= 80:
        findings.append("HIGH memory usage")

    if disk_percent >= 90:
        findings.append("CRITICAL disk usage")
    elif disk_percent >= 80:
        findings.append("HIGH disk usage")

    if not findings:
        findings.append("No configured resource thresholds exceeded")

    return (
        f"Server: {server_name}\n"
        f"CPU: {cpu_percent}%\n"
        f"Memory: {memory_percent}%\n"
        f"Disk: {disk_percent}%\n"
        f"Findings: {'; '.join(findings)}"
    )