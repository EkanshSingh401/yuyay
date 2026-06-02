"""Prometheus metrics configuration for the YUYAY Intelligence API."""

from __future__ import annotations

from prometheus_client import Counter, Histogram, Info

# API info
api_info = Info(
    "yuyay_api",
    "YUYAY Intelligence API information",
)
api_info.info({"version": "0.1.0", "environment": "production"})

# Request counter — tracks total requests by endpoint and method
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

# Request duration — tracks latency distribution
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# Evaluation counter — tracks YUYAY evaluations
evaluations_total = Counter(
    "evaluations_total",
    "Total YUYAY evaluations submitted",
)

# YES/NO/PO counters
yes_responses_total = Counter(
    "yes_responses_total",
    "Total YES responses across all evaluations",
)

no_responses_total = Counter(
    "no_responses_total",
    "Total NO responses across all evaluations",
)

po_responses_total = Counter(
    "po_responses_total",
    "Total PO responses across all evaluations",
)

# LLM query counter — tracks FIOS queries by provider
llm_queries_total = Counter(
    "llm_queries_total",
    "Total LLM queries through FIOS",
    ["provider"],
)

# LLM latency — tracks response time by provider
llm_query_duration_seconds = Histogram(
    "llm_query_duration_seconds",
    "LLM query duration in seconds",
    ["provider"],
    buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
)

# LLM cost tracker
llm_cost_usd_total = Counter(
    "llm_cost_usd_total",
    "Total estimated LLM cost in USD",
    ["provider"],
)
