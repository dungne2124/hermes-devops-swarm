"""Monitoring Agent — ingests CI/CD logs, error stacks, and community updates."""

import logging
import random
from datetime import datetime

logger = logging.getLogger("MonitoringAgent")

MOCK_ALERTS = [
    {
        "severity": "CRITICAL",
        "service": "payment-service",
        "message": "Build failure rate rose to 34%, suspected dependency conflict.",
        "tokens_ingested": 108450,
    },
    {
        "severity": "WARNING",
        "service": "auth-module",
        "message": "P95 response latency increased by 220ms, possible slow query.",
        "tokens_ingested": 12300,
    },
]


class MonitoringAgent:
    def __init__(self, config: dict):
        self.config = config
        self.name = "MonitoringAgent"

    def _fetch_jenkins_logs(self) -> int:
        logger.info("Fetching Jenkins pipeline logs (last 60 minutes)... done.")
        return 3200

    def _fetch_github_actions(self) -> int:
        logger.info("Fetching GitHub Actions build logs (18 workflows)... done.")
        return 1800

    def _fetch_sentry_traces(self) -> int:
        logger.info("Fetching Sentry error stack traces (247 new)... done.")
        return 247

    def _fetch_community_updates(self) -> int:
        logger.info("Fetching community tech updates (14 Telegram channels, 3,128 new messages)... done.")
        return 3128

    def run(self) -> list:
        logger.info("Starting CI/CD real-time data ingestion...")
        msgs = self._fetch_jenkins_logs()
        msgs += self._fetch_github_actions()
        msgs += self._fetch_sentry_traces()
        msgs += self._fetch_community_updates()

        total_tokens = 108450
        logger.info(f"Pre-processing complete. Raw token count: {total_tokens:,}")
        logger.info(f"Pushing {total_tokens // 1000}k token payload to long-context LLM for noise filtering...")

        # Simulate LLM inference
        elapsed = 8.9
        logger.info(f"Inference complete (elapsed: {elapsed}s).")

        alerts = [a for a in MOCK_ALERTS if random.random() > 0.1]
        for a in alerts:
            tag = f"[{a['severity']}]"
            logger.info(f"  → {tag} {a['service']}: {a['message']}")

        return alerts
