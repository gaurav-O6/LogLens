from pathlib import Path

from app import create_app
from app.services.processing_service import ProcessingService


app = create_app()

with app.app_context():
    service = ProcessingService()

    result = service.process_file(Path("../sample_logs/test.log"))

    print(f"Parsed Logs: {len(result['parsed_logs'])}")
    print(f"Detections: {len(result['detections'])}")

    print("\nDetections:")
    for detection in result["detections"]:
        print(detection)

    print("\nSummary:")
    print(result["summary"])