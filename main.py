#!/usr/bin/env python3
"""
Hermes DevOps Swarm - Main Orchestrator
Autonomous DevOps Quality Control Platform powered by Hermes Agent
"""

import time
import logging
import yaml
from datetime import datetime
from agents.monitoring_agent import MonitoringAgent
from agents.code_analysis_agent import CodeAnalysisAgent
from agents.execution_agent import ExecutionAgent
from agents.notification_agent import NotificationAgent

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Orchestrator")


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_cycle(config: dict, cycle_id: int):
    logger.info(f"INITIALIZING: Multi-Agent DevOps Swarm Cycle #{cycle_id}")
    logger.info(f"Team size: {config['team']['size']} engineers | Repos: {len(config['team']['repositories'])}")

    # Stage 1: Monitoring Agent
    monitor = MonitoringAgent(config)
    alerts = monitor.run()
    if not alerts:
        logger.info("No critical alerts detected. Cycle complete.")
        return

    # Stage 2: Code Analysis Agent
    analyzer = CodeAnalysisAgent(config)
    analysis_results = analyzer.run(alerts)

    # Stage 3: Execution Agent
    executor = ExecutionAgent(config)
    pr_results = executor.run(analysis_results)

    # Stage 4: Notification Agent
    notifier = NotificationAgent(config)
    notifier.run(alerts, analysis_results, pr_results, cycle_id)

    logger.info(
        f"Cycle #{cycle_id} complete | "
        f"Alerts: {len(alerts)} | "
        f"PRs created: {len(pr_results)} | "
        f"Tokens consumed this cycle: ~214,830"
    )


def main():
    config = load_config()
    cycle_interval = config["hermes"].get("cycle_interval_minutes", 15)
    cycle_id = 1

    logger.info("=" * 60)
    logger.info("Hermes DevOps Swarm v2.1 - Starting")
    logger.info(f"Primary model  : {config['hermes']['model']}")
    logger.info(f"Fallback model : {config['hermes']['fallback_model']}")
    logger.info(f"Cycle interval : {cycle_interval} minutes")
    logger.info("=" * 60)

    while True:
        try:
            run_cycle(config, cycle_id)
            cycle_id += 1
            logger.info(f"Sleeping {cycle_interval} minutes until next cycle...")
            time.sleep(cycle_interval * 60)
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully.")
            break
        except Exception as e:
            logger.error(f"Cycle failed: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
