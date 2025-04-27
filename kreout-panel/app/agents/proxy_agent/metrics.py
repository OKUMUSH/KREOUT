# File: app/agents/proxy_agent/metrics.py
import random

def collect_metrics():
    return {
        "type": "proxy",
        "tps": round(random.uniform(18.0, 20.0), 2),
        "online_players": random.randint(50, 200),
        "max_players": 500
    }
