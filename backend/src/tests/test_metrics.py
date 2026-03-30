from wines_rag.metrics import MetricsRegistry, _esc


def test_escape_prometheus_label_values() -> None:
    raw = 'a\\b\n"c"'
    assert _esc(raw) == 'a\\\\b\\n\\"c\\"'


def test_render_prometheus_with_observations() -> None:
    registry = MetricsRegistry()

    registry.observe_request("GET", "/chat", 200, 0.12)
    registry.observe_request("GET", "/chat", 200, 0.30)
    registry.observe_request("POST", '/metrics"live', 500, 1.0)

    rendered = registry.render_prometheus()

    assert "# HELP backend_uptime_seconds" in rendered
    assert 'backend_requests_total{method="GET",path="/chat",status="200"} 2' in rendered
    assert 'backend_requests_total{method="POST",path="/metrics\\"live",status="500"} 1' in rendered
    assert 'backend_request_duration_seconds_sum{method="GET",path="/chat"} 0.420000' in rendered
    assert 'backend_request_duration_seconds_count{method="GET",path="/chat"} 2' in rendered


def test_render_prometheus_without_observations() -> None:
    registry = MetricsRegistry()

    rendered = registry.render_prometheus()

    assert "# TYPE backend_requests_total counter" in rendered
    assert "# TYPE backend_request_duration_seconds_count counter" in rendered
