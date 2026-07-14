import re
from typing import Optional


class ApacheLogParser:
    """
    Parser for Apache Common Log Format (CLF) access logs.
    """

    LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) '
    r'\S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) '
    r'(?P<path>\S+) '
    r'HTTP/\d\.\d" '
    r'(?P<status_code>\d{3}) '
    r'\S+ '
    r'"[^"]*" '
    r'"(?P<user_agent>[^"]*)"'
)

    def parse_line(self, line: str) -> Optional[dict]:
        """
        Parse a single Apache log line.
        """

        match = self.LOG_PATTERN.match(line)

        if not match:
            return None

        return {
    "ip": match.group("ip"),
    "timestamp": match.group("timestamp"),
    "method": match.group("method"),
    "path": match.group("path"),
    "status_code": int(match.group("status_code")),
    "user_agent": match.group("user_agent"),
}