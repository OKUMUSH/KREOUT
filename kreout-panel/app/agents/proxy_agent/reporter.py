# File: app/agents/proxy_agent/reporter.py
import aiohttp
import os

async def send_metrics(metrics: dict):
    async with aiohttp.ClientSession() as session:
        token = os.getenv("AGENT_TOKEN", "Kreout!225900")
        headers = {"Authorization": f"Bearer {token}"}
        async with session.post("http://localhost:8000/proxy/update", json=metrics, headers=headers) as resp:
            print(f"[ProxyAgent] Sent metrics: {metrics} — Status {resp.status}")