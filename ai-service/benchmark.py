import requests
import time
import statistics

URL = "http://localhost:5000/categorise"

payload = {
    "text": "Risk of data breach due to weak authentication"
}

times = []

for i in range(50):
    start = time.time()

    response = requests.post(URL, json=payload)

    end = time.time()

    duration = (end - start) * 1000  # ms
    times.append(duration)

    print(f"Request {i+1}: {duration:.2f} ms")

# 📊 Calculate metrics
times.sort()

p50 = statistics.median(times)
p95 = times[int(0.95 * len(times)) - 1]
p99 = times[int(0.99 * len(times)) - 1]

print("\n📊 RESULTS:")
print(f"p50: {p50:.2f} ms")
print(f"p95: {p95:.2f} ms")
print(f"p99: {p99:.2f} ms")