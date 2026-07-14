from app.detection.detector import ThreatDetector

detector = ThreatDetector()

sample_logs = [
    {
        "ip": "192.168.1.10",
        "timestamp": "14/Jul/2026:17:30:15 +0530",
        "method": "GET",
        "path": "/login?id=1' OR 1=1--",
        "status_code": 200,
        "user_agent": "Mozilla/5.0",
    },
    {
        "ip": "192.168.1.20",
        "timestamp": "14/Jul/2026:17:35:00 +0530",
        "method": "GET",
        "path": "/search?q=<script>alert(1)</script>",
        "status_code": 200,
        "user_agent": "Mozilla/5.0",
    },
    {
        "ip": "192.168.1.30",
        "timestamp": "14/Jul/2026:17:40:00 +0530",
        "method": "GET",
        "path": "/../../etc/passwd",
        "status_code": 403,
        "user_agent": "curl/8.0",
    },
]

for log in sample_logs:
    print(f"\nTesting: {log['path']}")
    detections = detector.detect(log)

    if detections:
        for detection in detections:
            print(detection)
    else:
        print("No threats detected.")