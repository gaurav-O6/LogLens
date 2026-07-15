from pathlib import Path

from app.parser.apache_parser import ApacheLogParser
from app.detection.detector import ThreatDetector
from app.detection.brute_force import BruteForceDetector
from app.services.aggregation_service import AggregationService
from app.services.log_service import save_logs


class ProcessingService:
    """
    Coordinates the log processing pipeline.

    Pipeline:
    Log File
        ↓
    Parser
        ↓
    Save Logs
        ↓
    Regex Threat Detection
        ↓
    Brute Force Detection
        ↓
    Aggregation
        ↓
    Results
    """

    def __init__(self):
        self.parser = ApacheLogParser()
        self.threat_detector = ThreatDetector()
        self.brute_force_detector = BruteForceDetector()
        self.aggregation_service = AggregationService()

    def process_file(self, file_path: Path) -> dict:
        """
        Process a log file through the complete detection pipeline.
        """

        # Parse the uploaded log file
        parsed_logs = self.parser.parse_file(file_path)

        # Persist parsed logs to the database
        save_logs(parsed_logs)

        detections = []

        for log_entry in parsed_logs:
            # Regex-based threat detection
            threats = self.threat_detector.detect(log_entry)
            if threats:
                detections.extend(threats)

            # Brute force detection
            brute_force = self.brute_force_detector.process(log_entry)
            if brute_force:
                detections.append(brute_force)

        # Aggregate detection statistics
        summary = self.aggregation_service.aggregate(detections)

        return {
            "parsed_logs": parsed_logs,
            "detections": detections,
            "summary": summary,
        }