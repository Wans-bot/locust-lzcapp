"""Locust 压测脚本（Python 定义负载）。

Locust 用普通 Python 代码描述压测场景：每个 @task 就是一个请求动作，
weight 决定权重，wait_time 决定每个虚拟用户两次请求之间的思考时间。

默认目标 Host 是容器内置的演示 API（http://127.0.0.1:8090）。
要压测自己的服务，直接在 Locust 网页界面把 Host 改成目标地址
（例如 http://your-service:8080 或 https://example.com）再点 Start 即可，
无需修改本文件。

想自定义更复杂的场景（登录、参数化、断言等），可参考
https://docs.locust.io/en/stable/quickstart.html
"""

import random

from locust import HttpUser, between, task

KEYWORDS = ["phone", "laptop", "book", "shoe", "toy"]


class DemoShopUser(HttpUser):
    """模拟一个浏览电商 API 的普通用户。"""

    wait_time = between(1, 3)

    @task(5)
    def list_products(self):
        self.client.get("/api/products", name="/api/products")

    @task(3)
    def product_detail(self):
        pid = random.randint(0, 29)
        self.client.get(f"/api/products/{pid}", name="/api/products/[id]")

    @task(2)
    def list_users(self):
        self.client.get("/api/users", name="/api/users")

    @task(2)
    def search(self):
        kw = random.choice(KEYWORDS)
        self.client.get(f"/api/search?q={kw}", name="/api/search?q=[kw]")

    @task(1)
    def health(self):
        self.client.get("/api/health", name="/api/health")
