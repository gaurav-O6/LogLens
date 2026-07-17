import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "attack_test.log"

TOTAL_LINES = 5000

PUBLIC_IPS = [
    "8.8.8.8",
    "1.1.1.1",
    "45.33.32.156",
    "103.21.244.1",
    "151.101.1.69",
    "185.199.108.153",
    "104.26.10.78",
]

NORMAL_PATHS = [
    "/",
    "/index.html",
    "/about",
    "/products",
    "/contact",
    "/blog",
    "/images/logo.png",
]

USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/138.0",
    "Firefox/140.0",
]

SCANNER_AGENTS = [
    "curl/8.0",
    "wget/1.21",
    "python-requests/2.31",
    "Nikto/2.5",
]

start = datetime(2026, 7, 17, 0, 0, 0)

lines = []

for _ in range(TOTAL_LINES):

    ip = random.choice(PUBLIC_IPS)

    timestamp = (
        start +
        timedelta(
            minutes=random.randint(0, 1439),
            seconds=random.randint(0, 59)
        )
    )

    ts = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0530")

    roll = random.random()

    # --------------------------------------------------
    # 55% Normal traffic
    # --------------------------------------------------

    if roll < 0.55:

        method = random.choice(["GET", "POST"])

        path = random.choice(NORMAL_PATHS)

        status = random.choice([200, 200, 200, 301])

        ua = random.choice(USER_AGENTS)

    # --------------------------------------------------
    # 15% XSS (High)
    # --------------------------------------------------

    elif roll < 0.70:

        method = "GET"

        path = "/search?q=<script>alert(1)</script>"

        status = 200

        ua = random.choice(USER_AGENTS)

    # --------------------------------------------------
    # 15% Directory Traversal (Medium)
    # --------------------------------------------------

    elif roll < 0.85:

        method = "GET"

        path = "/../../etc/passwd"

        status = 403

        ua = "curl/8.0"

    # --------------------------------------------------
    # 10% Reconnaissance (Low)
    # --------------------------------------------------

    elif roll < 0.95:

        method = "GET"

        path = random.choice([
            "/robots.txt",
            "/sitemap.xml",
            "/phpinfo.php",
            "/.env",
            "/config.php",
        ])

        status = random.choice([200, 403, 404])

        ua = random.choice(SCANNER_AGENTS)

    # --------------------------------------------------
    # 5% Brute Force (High)
    # --------------------------------------------------

    else:

        method = "GET"

        path = "/login"

        status = 401

        ua = "Mozilla/5.0"

    line = (
        f'{ip} - - [{ts}] '
        f'"{method} {path} HTTP/1.1" '
        f'{status} 512 "-" "{ua}"'
    )

    lines.append(line)


# ------------------------------------------------------
# Guaranteed brute-force attacks from one IP
# ------------------------------------------------------

bf_ip = "103.21.244.1"

for i in range(7):

    ts = (
        start +
        timedelta(hours=23, minutes=i)
    ).strftime("%d/%b/%Y:%H:%M:%S +0530")

    lines.append(
        f'{bf_ip} - - [{ts}] '
        f'"GET /login HTTP/1.1" '
        f'401 512 "-" "Mozilla/5.0"'
    )

random.shuffle(lines)

OUTPUT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print(f"Generated {len(lines)} log entries")
print(f"Saved to {OUTPUT_FILE}")