from pathlib import Path
import re
from typing import Optional, Iterator


class ApacheLogParser:
    """
    Parser for Apache Common Log Format (CLF) access logs.

    Uses streaming parsing so the entire file is not loaded into memory.
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

            "raw_log": line,

        }


    def parse_file(
        self,
        file_path: Path
    ) -> Iterator[dict]:

        matched = 0
        skipped = 0

        with file_path.open(
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            for line in file:

                raw_line = line.rstrip("\n")

                parsed = self.parse_line(raw_line)

                if parsed is None:
                    skipped += 1
                    continue

                matched += 1
                yield parsed

        print(f"[PARSER] Matched: {matched:,}")
        print(f"[PARSER] Skipped: {skipped:,}")