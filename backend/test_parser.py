from pathlib import Path

from app.parser.apache_parser import ApacheLogParser

parser = ApacheLogParser()

log_file = Path("../sample_logs/test.log")

parsed_logs = parser.parse_file(log_file)

for log in parsed_logs:
    print(log)