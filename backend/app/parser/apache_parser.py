from pathlib import Path
import re
from typing import Optional, Iterator


class ApacheLogParser:
    """
    Streaming Apache Common Log Format parser.

    The file is never loaded entirely into memory.
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

    def parse_line(
        self,
        line: str,
    ) -> Optional[dict]:

        match = self.LOG_PATTERN.match(
            line
        )

        if not match:
            return None

        return {
            "ip": match.group("ip"),
            "timestamp": match.group("timestamp"),
            "method": match.group("method"),
            "path": match.group("path"),
            "status_code": int(
                match.group("status_code")
            ),
            "user_agent": match.group("user_agent"),
            "raw_log": line,
        }

    def iter_lines(
        self,
        file_path: Path,
    ) -> Iterator[str]:
        """
        Stream raw lines from the log file.

        This separates file I/O from parsing so the processing
        pipeline can profile the actual parser independently.
        """

        with file_path.open(
            "r",
            encoding="utf-8",
            errors="ignore",
            buffering=1024 * 1024,
        ) as file:

            for line in file:

                yield line.rstrip("\n")

    def parse_file(
        self,
        file_path: Path,
    ) -> Iterator[dict]:

        matched = 0
        skipped = 0

        for raw_line in self.iter_lines(
            file_path
        ):

            parsed = self.parse_line(
                raw_line
            )

            if parsed is None:

                skipped += 1

                continue

            matched += 1

            yield parsed

        print(
            f"[PARSER] Matched: {matched:,}",
            flush=True,
        )

        print(
            f"[PARSER] Skipped: {skipped:,}",
            flush=True,
        )
