#!/usr/bin/env python3
"""
监控客户端 - 采集本机指标并上报到博客后端
用法: python scripts/monitor_agent.py --token YOUR_TOKEN --url http://127.0.0.1:8000
"""
import argparse
import json
import os
import socket
import time
import urllib.request


def collect_metrics():
    import psutil
    disk_path = 'C:\\' if os.name == 'nt' else '/'
    net = psutil.net_io_counters()
    return {
        'hostname': socket.gethostname(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage(disk_path).percent,
        'load_avg': (psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0),
        'network_in': net.bytes_recv,
        'network_out': net.bytes_sent,
        'uptime': int(time.time() - psutil.boot_time()),
    }


def report(url, token, data):
    payload = json.dumps({**data, 'token': token}).encode()
    req = urllib.request.Request(
        f'{url.rstrip("/")}/api/monitoring/report/',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def main():
    parser = argparse.ArgumentParser(description='Blog monitor agent')
    parser.add_argument('--token', required=True, help='MonitorServer token from Django admin')
    parser.add_argument('--url', default='http://127.0.0.1:8000', help='Blog API base URL')
    parser.add_argument('--interval', type=int, default=30, help='Report interval in seconds')
    args = parser.parse_args()

    print(f'Agent started, reporting every {args.interval}s to {args.url}')
    while True:
        try:
            data = collect_metrics()
            result = report(args.url, args.token, data)
            print(f'Reported OK: CPU={data["cpu_percent"]:.1f}% MEM={data["memory_percent"]:.1f}%')
        except Exception as e:
            print(f'Report failed: {e}')
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
