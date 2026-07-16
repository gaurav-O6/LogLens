from app.detection.detector import ThreatDetector


detector = ThreatDetector()


test_log = {
    "ip": "192.168.1.30",
    "timestamp": "17/Jul/2026:01:01:00 +0530",
    "method": "GET",
    "path": "/../../etc/passwd",
    "status_code": 403,
    "raw_log": "test"
}


result = detector.detect(test_log)


print("RESULT:")
print(result)