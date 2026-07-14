import json
import re
from pathlib import Path


class ThreatDetector:
    """
    Detect known attacks using regex-based signatures.
    """

    def __init__(self):
        signatures_path = Path(__file__).parent / "signatures.json"

        with signatures_path.open("r", encoding="utf-8") as file:
            self.signatures = json.load(file)

        # Compile regex patterns once for better performance
        for signature in self.signatures:
            signature["compiled_patterns"] = [
                re.compile(pattern, re.IGNORECASE)
                for pattern in signature["patterns"]
            ]

    def detect(self, log_entry: dict) -> list[dict]:
        """
        Detect attacks in a parsed log entry.

        Args:
            log_entry: Parsed log dictionary.

        Returns:
            List of detected attacks.
        """

        detections = []

        path = log_entry.get("path", "")

        for signature in self.signatures:
            for regex in signature["compiled_patterns"]:

                if regex.search(path):

                    detections.append(
                        {
                            "attack_type": signature["type"],
                            "severity": signature["severity"],
                            "source_ip": log_entry["ip"],
                            "timestamp": log_entry["timestamp"],
                            "matched_pattern": regex.pattern,
                        }
                    )

                    break

        return detections