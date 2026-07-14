from pathlib import Path
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

        Args:
            line: Raw Apache log line.

        Returns:
            Dictionary containing parsed fields,
            or None if the line cannot be parsed.
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

    def parse_file(self, file_path: Path) -> list[dict]:
        """
        Parse an entire Apache log file.

        Args:
            file_path: Path to the log file.

        Returns:
            List of successfully parsed log entries.
        """

        parsed_logs = []

        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                parsed = self.parse_line(line.strip())

                if parsed is not None:
                    parsed_logs.append(parsed)

        return parsed_logs