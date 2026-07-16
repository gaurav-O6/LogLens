class BruteForceDetector:

    def __init__(self, threshold=5):
        self.threshold = threshold
        self.failed_attempts = {}
        self.alerted_ips = set()


    def process(self, log_entry):

        ip = log_entry.get("ip")
        path = log_entry.get("path")
        status_code = log_entry.get("status_code")


        # Only track failed login attempts
        if path == "/login" and status_code == 401:

            self.failed_attempts[ip] = (
                self.failed_attempts.get(ip, 0) + 1
            )


            if (
                self.failed_attempts[ip] >= self.threshold
                and ip not in self.alerted_ips
            ):

                self.alerted_ips.add(ip)


                return {
                    "attack_type": "Brute Force",
                    "severity": "High",

                    "source_ip": ip,
                    "timestamp": log_entry.get("timestamp"),

                    "matched_pattern": None,

                    "http_method": log_entry.get("method"),
                    "request_path": log_entry.get("path"),
                    "status_code": log_entry.get("status_code"),
                    "raw_log": log_entry.get("raw_log"),

                    "attempts": self.failed_attempts[ip],
                }


        return None