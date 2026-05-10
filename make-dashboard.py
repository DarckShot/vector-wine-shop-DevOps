import json

DS = {"type": "prometheus", "uid": "prometheus"}

def target(expr, ref="A", instant=False, fmt="time_series"):
    return {
        "refId": ref,
        "datasource": DS,
        "expr": expr,
        "instant": instant,
        "format": fmt
    }

def stat(i, title, expr, x, y, w=6, h=4):
    return {
        "id": i,
        "title": title,
        "type": "stat",
        "datasource": DS,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "targets": [target(expr, instant=True)],
        "options": {"reduceOptions": {"calcs": ["lastNotNull"]}}
    }

def timeseries(i, title, expr, legend, x, y, w=12, h=8):
    return {
        "id": i,
        "title": title,
        "type": "timeseries",
        "datasource": DS,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "targets": [{
            **target(expr),
            "legendFormat": legend
        }]
    }

def table(i, title, expr, x, y, w=24, h=8):
    return {
        "id": i,
        "title": title,
        "type": "table",
        "datasource": DS,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "targets": [target(expr, instant=True, fmt="table")]
    }

dashboard = {
    "uid": "wine-shop-pods",
    "title": "Wine Shop - Monitoring",
    "tags": ["wine-app", "prometheus", "cloud"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 0,
    "refresh": "10s",
    "panels": [
        stat(1, "Running pods", 'count(kube_pod_status_phase{namespace="wine-app",phase="Running"} == 1)', 0, 0),
        stat(2, "Problem pods", 'count(kube_pod_status_phase{namespace="wine-app",phase=~"Pending|Failed|Unknown"} == 1)', 6, 0),
        stat(3, "Backend RPS", 'sum(rate(backend_requests_total[1m]))', 12, 0),
        stat(4, "HTTP errors RPS", 'sum(rate(backend_requests_total{status=~"4..|5.."}[1m]))', 18, 0),

        table(5, "Pods status - wine-app namespace", 'kube_pod_status_phase{namespace="wine-app"} == 1', 0, 4),

        timeseries(
            6,
            "HTTP requests by pod / endpoint / status",
            'sum by (pod, method, path, status) (rate(backend_requests_total[1m]))',
            "{{pod}} {{method}} {{path}} {{status}}",
            0, 12, 24, 9
        ),

        timeseries(
            7,
            "HTTP errors by pod",
            'sum by (pod, status) (rate(backend_requests_total{status=~"4..|5.."}[1m]))',
            "{{pod}} {{status}}",
            0, 21, 12, 8
        ),

        timeseries(
            8,
            "CPU usage by pod",
            'sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="wine-app",container!="",image!=""}[5m]))',
            "{{pod}}",
            12, 21, 12, 8
        ),

        timeseries(
            9,
            "Memory usage by pod",
            'sum by (pod) (container_memory_working_set_bytes{namespace="wine-app",container!="",image!=""})',
            "{{pod}}",
            0, 29, 12, 8
        ),

        timeseries(
            10,
            "Container restarts by pod",
            'sum by (pod) (increase(kube_pod_container_status_restarts_total{namespace="wine-app"}[6h]))',
            "{{pod}}",
            12, 29, 12, 8
        )
    ]
}

payload = {
    "dashboard": dashboard,
    "folderId": 0,
    "overwrite": True
}

with open("wine-shop-monitoring.json", "w") as f:
    json.dump(payload, f, indent=2)
