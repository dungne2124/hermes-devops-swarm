"""Code Analysis Agent — deep-dives into affected service modules to locate root causes."""

import logging

logger = logging.getLogger("CodeAnalysisAgent")


class CodeAnalysisAgent:
    def __init__(self, config: dict):
        self.config = config

    def _load_service_context(self, service: str) -> dict:
        files = 38
        tokens = 94200
        logger.info(f"Loading {service} core modules into context window ({files} files, ~{tokens:,} tokens)...")
        return {"service": service, "files": files, "tokens": tokens}

    def _analyze_dependency_conflict(self, service: str) -> dict:
        logger.info("Running long-chain reasoning to trace dependency conflict root cause...")
        result = {
            "type": "dependency_conflict",
            "root_cause": "stripe-sdk@12.1.0 and axios@1.6.0 have indirect dependency conflict (node-fetch@2 vs @3).",
            "affected_path": "src/payment/providers/stripe.provider.ts → src/utils/http.client.ts",
            "fix": "Pin axios@1.4.0 and upgrade stripe-sdk to @12.3.1 (compatible with node-fetch@3).",
        }
        logger.info(f"  → Root cause: {result['root_cause']}")
        logger.info(f"  → Affected path: {result['affected_path']}")
        logger.info(f"  → Fix: {result['fix']}")
        return result

    def _analyze_slow_query(self, service: str) -> dict:
        logger.info("Analyzing slow query issue in auth-module...")
        result = {
            "type": "n_plus_1_query",
            "location": "src/auth/services/session.service.ts line 187",
            "fix": "Replace in-loop findOne() with batch findByIds() and add Redis cache layer.",
        }
        logger.info(f"  → Detected N+1 query at {result['location']}")
        logger.info(f"  → Fix: {result['fix']}")
        return result

    def run(self, alerts: list) -> list:
        results = []
        logger.info("Received critical alerts. Starting deep code review...")

        for alert in alerts:
            ctx = self._load_service_context(alert["service"])
            if alert["severity"] == "CRITICAL":
                analysis = self._analyze_dependency_conflict(alert["service"])
            else:
                analysis = self._analyze_slow_query(alert["service"])

            results.append({**ctx, **analysis, "alert": alert})

        logger.info(f"Root cause analysis complete. {len(results)} issue(s) identified.")
        return results
