"""内置演示目标：一个零依赖的本地 JSON API（仅监听 127.0.0.1:8090）。

Locust 是压测工具，需要一个被压测的目标。为了让应用开箱即可演示，
容器内自带这个轻量演示服务（模拟一个电商 API，带随机响应延迟），
首次启动时 Locust 会默认压测它，从而让统计表/图表立刻有真实数据。

用户要压测自己的服务时，在 Locust 界面把 Host 改成自己的地址即可，
本演示服务与用户目标无关。
"""

import json
import random
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PRODUCTS = [
    {"id": i, "name": f"demo-product-{i}", "price": round(9.9 + i * 3.7, 2), "stock": 100 - i}
    for i in range(30)
]
USERS = [{"id": i, "name": f"user_{i}", "vip": i % 5 == 0} for i in range(20)]
KEYWORDS = ["phone", "laptop", "book", "shoe", "toy"]


class DemoHandler(BaseHTTPRequestHandler):
    server_version = "LocustDemo/1.0"

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?")[0]

        if path == "/api/health":
            time.sleep(random.uniform(0.005, 0.02))
            return self._json({"status": "ok", "service": "locust-demo-shop"})

        if path == "/api/products":
            time.sleep(random.uniform(0.02, 0.09))
            return self._json({"count": len(PRODUCTS), "products": PRODUCTS})

        m = re.match(r"^/api/products/(\d+)$", path)
        if m:
            time.sleep(random.uniform(0.01, 0.06))
            return self._json(PRODUCTS[int(m.group(1)) % len(PRODUCTS)])

        if path == "/api/users":
            time.sleep(random.uniform(0.06, 0.18))
            return self._json({"count": len(USERS), "users": USERS})

        if path == "/api/search":
            time.sleep(random.uniform(0.12, 0.35))
            q = ""
            if "q=" in self.path:
                q = self.path.split("q=", 1)[1].split("&")[0]
            return self._json(
                {
                    "query": q,
                    "results": [
                        {"title": f"result {i} for {q}", "score": round(1 - i * 0.1, 2)}
                        for i in range(5)
                    ],
                }
            )

        time.sleep(random.uniform(0.01, 0.05))
        return self._json({"path": path, "ok": True})

    def log_message(self, *args):  # silence per-request logging
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8090), DemoHandler).serve_forever()
