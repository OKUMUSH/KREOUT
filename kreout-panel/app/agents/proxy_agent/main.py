# File: app/agents/proxy_agent/main.py
import asyncio
import os
from agents.proxy_agent.metrics import collect_metrics
from agents.proxy_agent.reporter import send_metrics

async def background_loop():
    while True:
        metrics = collect_metrics()
        token = os.getenv("PROXY_AGENT_TOKEN")
        await send_metrics(metrics, token)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(background_loop())

