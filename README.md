# LogLens - Simplified Security Log Analysis

![LogLens Banner](docs/banner.png)

## Overview

LogLens is a lightweight Security Information and Event Management (SIEM) platform designed to analyze Apache/Nginx web server logs.

Traditional server logs contain millions of requests, making manual investigation difficult. LogLens automates log parsing, threat detection, geographic enrichment, and security visualization through an interactive dashboard.

The system helps security analysts answer:

- Who attacked the system?
- What attack technique was used?
- When did the attack happen?
- Where did the attacker originate?

---

# Features

## Log Processing

- Apache/Nginx Common Log Format support
- Streaming file processing
- Large log file handling
- Background processing using Redis Queue

---

## Threat Detection

### Signature Based Detection

Detects common web attacks:

- Cross-Site Scripting (XSS)
- Directory Traversal
- Sensitive File Access
- Other malicious patterns

Detection uses configurable regex-based signatures.

---

## Brute Force Detection

Identifies repeated failed authentication attempts.

Example:


Multiple POST /login requests returning 401


Automatically generates high severity alerts.

---

## Threat Intelligence

Each detected event includes:

- Source IP
- Attack type
- Severity
- Timestamp
- Request path
- HTTP method
- Matched pattern
- Raw log entry

---

## GeoIP Intelligence

Provides geographic information:

- Country
- City
- Coordinates
- Private/Public IP classification

Threats are visualized on a global attack map.

---

# Dashboard

The SOC dashboard provides:

- Total attack statistics
- Severity distribution
- Attack classification
- Top attacking IPs
- Attack timeline
- Geographic visualization
- Threat investigation panel

---

# Architecture


             React Dashboard
                   |
                   |
             Flask REST API
                   |
    --------------------------------
    |              |               |

Log Parser Detection Engine GeoIP Service
| |
| ----------------
| | |
| Signature Rules Brute Force
|
|
PostgreSQL Database

    |
    |

Redis Queue + RQ Workers


---

# Tech Stack

## Frontend

- React
- Vite
- React Router
- Recharts
- Leaflet Maps
- Lucide Icons

## Backend

- Python
- Flask
- SQLAlchemy
- PostgreSQL

## Background Processing

- Redis
- RQ

## Infrastructure

- Docker
- Docker Compose

---

# Project Structure


LogLens/

├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── detection/
│ │ ├── models/
│ │ ├── parser/
│ │ ├── services/
│ │ └── workers/
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ └── api/
│
├── sample_logs/
│
├── docker-compose.yml
└── README.md


---

# Running Locally

## Clone Repository

```bash
git clone <repository-url>

cd LogLens
Backend Setup

Create environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run Flask:

python run.py
Worker Setup

Start Redis:

docker compose up redis

Start worker:

rq worker --worker-class rq.worker.SimpleWorker log_processing
Frontend Setup
cd frontend

Install:

npm install

Run:

npm run dev
API Endpoints
Health
GET /api/v1/health
Upload Log
POST /api/v1/upload
Detection Results
GET /api/v1/analysis/detections
Dashboard Summary
GET /api/v1/analysis/summary
Export
GET /api/v1/analysis/export/json

GET /api/v1/analysis/export/csv
Security Detection Examples

Example attacks detected:

XSS
GET /search?q=<script>alert(1)</script>
Directory Traversal
GET /../../etc/passwd
Brute Force
POST /login 401
POST /login 401
POST /login 401
Future Improvements

Possible enhancements:

Authentication system
Real-time WebSocket alerts
More attack signatures
Machine learning anomaly detection
Email notifications
Cloud deployment
Author

Gaurav Thakare

Computer Engineering

License

This project is developed for educational and cybersecurity learning purposes.