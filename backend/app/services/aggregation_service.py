from collections import Counter


class AggregationService:
    """
    Maintains attack summary statistics while processing logs.
    Designed for streaming/batch processing.
    """


    def __init__(self):

        self.attack_types = Counter()

        self.source_ips = Counter()

        self.severity = Counter()



    def add_detection(self, detection: dict):
        """
        Add a single detection to aggregation counters.
        """


        attack_type = detection.get(
            "attack_type"
        )


        source_ip = detection.get(
            "source_ip"
        )


        severity = detection.get(
            "severity"
        )



        if attack_type:

            self.attack_types[attack_type] += 1



        if source_ip:

            self.source_ips[source_ip] += 1



        if severity:

            self.severity[severity] += 1





    def get_summary(self) -> dict:
        """
        Return final aggregated statistics.
        """


        return {

            "attack_types":
                dict(self.attack_types),


            "source_ips":
                dict(self.source_ips),


            "severity":
                dict(self.severity),

        }