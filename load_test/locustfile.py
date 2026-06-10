
from locust import HttpUser, task, between


class AnalyticsUser(HttpUser):

    wait_time = between(1, 2)

    @task(5)
    def analytics(self):
        self.client.get("/analytics/summary")

    @task(2)
    def customers(self):
        self.client.get("/customers?page=1&size=100")

    @task(1)
    def top_customers(self):
        self.client.get("/analytics/top-customers")

    @task(1)
    def revenue_trends(self):
        self.client.get("/analytics/revenue-trends")

    @task(1)
    def repeat_customer_revenue(self):
        self.client.get("/analytics/repeat-customer-revenue")