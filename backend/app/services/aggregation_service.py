from collections import Counter


class AggregationService:
    """
    Aggregates detected attacks into summary statistics.
    """

    def aggregate(self, detections: list[dict]) -> dict:
        attack_types = Counter()
        source_ips = Counter()
        severity = Counter()

        for detection in detections:
            attack_types[detection["attack_type"]] += 1
            source_ips[detection["source_ip"]] += 1
            severity[detection["severity"]] += 1

        return {
            "attack_types": dict(attack_types),
            "source_ips": dict(source_ips),
            "severity": dict(severity),
        }
