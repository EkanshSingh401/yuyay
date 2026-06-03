"""Locust load test for YUYAY Intelligence API.

Tests non-LLM endpoints only to measure API performance
without incurring LLM API costs.

Run with:
    locust -f locustfile.py --host https://yuyay-production-2e45.up.railway.app
"""

from locust import HttpUser, between, task


class YUYAYUser(HttpUser):
    """Simulates a user interacting with the YUYAY API."""

    wait_time = between(1, 3)

    @task(3)
    def health_check(self) -> None:
        """Hit the health endpoint."""
        self.client.get("/api/v1/health")

    @task(3)
    def get_archetypes(self) -> None:
        """Fetch all archetypes."""
        self.client.get("/api/v1/archetypes")

    @task(2)
    def get_prometheus_metrics(self) -> None:
        """Fetch Prometheus metrics."""
        self.client.get("/api/v1/prometheus")
