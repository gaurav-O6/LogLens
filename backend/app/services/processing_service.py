from pathlib import Path

from app.parser.apache_parser import ApacheLogParser
from app.detection.detector import ThreatDetector
from app.detection.brute_force import BruteForceDetector


class ProcessingService:
    """
    Coordinates the log processing pipeline.

    Pipeline:
    Log File
        ↓
    Parser
        ↓
    Regex Threat Detection
        ↓
    Brute Force Detection
        ↓
    Results
    """

    def __init__(self):
        self.parser = ApacheLogParser()
        self.threat_detector = ThreatDetector()
        self.brute_force_detector = BruteForceDetector()

    def process_file(self, file_path: Path):
        parsed_logs = self.parser.parse_file(file_path)

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

        return {
            "parsed_logs": parsed_logs,
            "detections": detections,
        }