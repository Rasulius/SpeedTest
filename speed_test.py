#!/usr/bin/env python3
"""
Download Speed Test — измерение скорости скачивания по URL.
Выполняет заданное количество последовательных запросов,
считает среднее время, общий объём и скорость.
"""

import argparse
import time
import urllib.request
import urllib.error
import sys

def download_speed_test(url: str, num_requests: int = 10, chunk_size: int = 64 * 1024, timeout: int = 30) -> None:
    total_bytes = 0
    total_time = 0.0
    successful_requests = 0
    request_times = []

    for i in range(1, num_requests + 1):
        try:
            start = time.perf_counter()
            req = urllib.request.Request(url, headers={"User-Agent": "SpeedTest/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    total_bytes += len(chunk)
            elapsed = time.perf_counter() - start
            total_time += elapsed
            request_times.append(elapsed)
            successful_requests += 1
            print(f"Запрос {i}/{num_requests}: {elapsed:.3f} с", file=sys.stderr)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"Запрос {i}/{num_requests} не удался: {e}", file=sys.stderr)

    if successful_requests == 0:
        print("Не удалось выполнить ни одного запроса.", file=sys.stderr)
        return

    avg_time = total_time / successful_requests
    speed_mb_per_sec = total_bytes / (total_time * 1_000_000) if total_time > 0 else 0.0
    speed_mbps = (total_bytes * 8) / (total_time * 1_000_000) if total_time > 0 else 0.0

    print("\n--- Результаты ---")
    print(f"Успешных запросов: {successful_requests} из {num_requests}")
    print(f"Среднее время запроса: {avg_time:.3f} с")
    print(f"Общий объём скачанных данных: {total_bytes} байт ({total_bytes / 1_000_000:.2f} МБ)")
    print(f"Общее время: {total_time:.3f} с")
    print(f"Скорость скачивания: {speed_mb_per_sec:.2f} МБ/с ({speed_mbps:.2f} Мбит/с)")
    if request_times:
        print(f"Времена запросов: {', '.join(f'{t:.3f}' for t in request_times)} с")

def main() -> None:
    parser = argparse.ArgumentParser(description="Измерение скорости скачивания по URL")
    parser.add_argument("url", help="URL файла для скачивания")
    parser.add_argument("-n", "--num-requests", type=int, default=10,
                        help="Количество последовательных запросов (по умолчанию 10)")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Таймаут одного запроса в секундах (по умолчанию 30)")
    args = parser.parse_args()
    download_speed_test(args.url, args.num_requests, timeout=args.timeout)

if __name__ == "__main__":
    main()