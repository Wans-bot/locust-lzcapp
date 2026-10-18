#!/bin/sh
set -e

# ---------------------------------------------------------------
# Locust 性能/压力测试平台
# 1) 启动内置演示目标（本地 JSON API，仅监听 127.0.0.1:8090）
# 2) 启动 Locust Web UI（0.0.0.0:8089），并把演示目标设为默认压测地址
#    首次启动自动跑一段 3 分钟演示压测，让统计表/图表开箱即有真实数据
# ---------------------------------------------------------------

python3 /lzcapp/pkg/content/demo_server.py &

sleep 1

exec locust \
  -f /lzcapp/pkg/content/locustfile.py \
  --host http://127.0.0.1:8090 \
  --web-host 0.0.0.0 \
  --web-port 8089 \
  --autostart -u 25 -r 5 -t 180s
