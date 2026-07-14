from app.parser.apache_parser import ApacheLogParser

sample_log = (
    '192.168.1.10 - - [14/Jul/2026:17:30:15 +0530] '
    '"GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"'
)

parser = ApacheLogParser()

result = parser.parse_line(sample_log)

print(result)