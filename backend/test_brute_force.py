from app.detection.brute_force import BruteForceDetector

detector = BruteForceDetector(threshold=5)

log_entry = {
    "ip": "192.168.1.10",
    "path": "/login",
    "status_code": 401,
}

for i in range(7):
    result = detector.process(log_entry)
    print(f"Attempt {i + 1}: {result}")