# LogLens – Simplified Security Log Analysis (SIEM-lite)

LogLens is a lightweight Security Information and Event Management (SIEM-lite) platform that analyzes Apache and Nginx web server logs to identify common web attacks. The system processes uploaded log files asynchronously, detects malicious activity using rule-based signatures, enriches results with GeoIP information, and presents them through an interactive security dashboard.

---

# Features

- Upload Apache/Nginx log files
- Direct browser uploads to Cloudflare R2
- Asynchronous log processing using Redis Queue (RQ)
- Streaming parser for efficient large file handling
- Signature-based threat detection
- Brute-force attack detection
- GeoIP enrichment
- Interactive SOC dashboard
- Threat investigation interface
- Analytics and visualization
- Job progress tracking
- CSV and JSON export support

---

# Supported Attack Detection

LogLens currently detects:

- Cross-Site Scripting (XSS)
- Directory Traversal
- Sensitive File Access
- Brute Force Login Attempts

Detection rules are configurable and can be extended by adding additional signatures.

---

# Technology Stack

## Frontend

- React
- Vite
- Axios
- Recharts
- Leaflet

## Backend

- Flask
- SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Redis
- RQ (Redis Queue)

## Storage

- Cloudflare R2 Object Storage

## Deployment

- Render
- Northflank
- Upstash Redis

---

# System Architecture

```
                 React Frontend
                        │
                        ▼
                  Flask REST API
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
 Cloudflare R2                  PostgreSQL
         │
         ▼
      Redis Queue
         │
         ▼
      RQ Worker
         │
         ▼
  Log Processing Engine
         │
         ├── Streaming Parser
         ├── Threat Detection
         ├── Brute Force Detection
         ├── GeoIP Enrichment
         └── Database Storage
```

---

# Processing Pipeline

```
Upload Log File
        │
        ▼
Cloudflare R2 Storage
        │
        ▼
Create Processing Job
        │
        ▼
Redis Queue
        │
        ▼
RQ Worker
        │
        ▼
Streaming Parser
        │
        ▼
Threat Detection
        │
        ▼
GeoIP Enrichment
        │
        ▼
Database Storage
        │
        ▼
Dashboard Analytics
```

---

# Screenshots

## Dashboard

![Dashboard](docs/dashboard.png)

---

## Threat Center

![Threat Center](docs/threat-center.png)

---

## Analytics

![Analytics](docs/analytics.png)

---

## Investigation Panel

![Investigation](docs/investigation.png)

---

# Project Structure

```
LogLens/
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── sample_logs/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

# Installation

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt

flask db upgrade

python run.py
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
SECRET_KEY=your_secret_key

DATABASE_URL=your_database_url

REDIS_URL=your_redis_url

R2_ACCESS_KEY=your_access_key

R2_SECRET_KEY=your_secret_key

R2_BUCKET=your_bucket_name

R2_ENDPOINT=your_endpoint
```

---

# Performance

The application uses:

- Streaming log parsing
- Batch database inserts
- PostgreSQL COPY optimization
- Redis Queue background processing
- Asynchronous workers

These optimizations allow LogLens to efficiently process large log files while keeping the web interface responsive.

---

# Future Improvements

- Additional attack signatures
- Machine learning anomaly detection
- Real-time log ingestion
- Email alerting
- User authentication
- Multi-user support
- Elasticsearch integration
- Kibana-style dashboards

---

# Author

**Gaurav Thakare**

Bachelor of Engineering (Computer Science)

Cybersecurity Internship Project

2026