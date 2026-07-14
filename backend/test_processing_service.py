from pathlib import Path

from app.services.processing_service import ProcessingService

service = ProcessingService()

result = service.process_file(Path("../sample_logs/test.log"))

print(f"Parsed Logs: {len(result['parsed_logs'])}")
print(f"Detections: {len(result['detections'])}")

for detection in result["detections"]:
    print(detection)