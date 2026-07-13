# LogLens - Project Context

## Project Overview

LogLens is a SIEM-lite (Security Information and Event Management) web application that analyzes Apache and Nginx web server logs to detect common cyber attacks and present the findings through an interactive dashboard.

This project is being developed as a portfolio-quality application using production-inspired software engineering practices.

---

## Primary Goal

Build a scalable, maintainable, and well-structured application that demonstrates:

- Backend development
- Cybersecurity fundamentals
- Large file processing
- REST API design
- Database design
- Asynchronous task processing
- Clean software architecture

---

## Technology Stack

### Backend
- Python 3.10+
- Flask
- SQLAlchemy
- PostgreSQL
- Redis
- Celery

### Frontend
- React
- Tailwind CSS
- Recharts

### DevOps
- Docker
- Docker Compose
- Git

---

## Core Features

- User authentication using JWT
- Apache/Nginx Common Log Format parser
- Streaming large log files
- Regex-based attack detection
- SQL Injection detection
- Cross Site Scripting (XSS) detection
- Directory Traversal detection
- Brute Force detection
- Severity scoring
- Dashboard analytics
- Timeline visualization
- Top attacker IPs
- GeoIP visualization
- Report generation
- Background processing using Celery

---

## Architecture Decisions

- Flask is used only as a REST API.
- Flask does NOT render HTML templates.
- React is a completely separate frontend application.
- Backend and frontend remain independent.
- Business logic belongs inside services.
- API routes should remain thin.
- Parsing logic belongs inside the parser module.
- Threat detection belongs inside the detection module.
- Database logic should remain isolated from business logic.
- Large log files must be processed using streaming instead of loading the whole file into memory.

---

## Coding Standards

Always:

- Follow PEP 8.
- Use type hints.
- Write docstrings.
- Prefer readable code over clever code.
- Keep functions small.
- Avoid duplicated code.
- Use descriptive variable names.
- Keep modules focused on one responsibility.
- Write modular and maintainable code.

---

## Important Rules

- Do not redesign the project architecture.
- Do not introduce unnecessary frameworks.
- Do not generate HTML templates.
- Do not use Flask templates.
- React handles the UI.
- Generate only the files requested.
- Explain important assumptions before generating code.
- Prefer production-quality patterns over tutorial shortcuts.

---

## Development Philosophy

The goal is not simply to make the application work.

The goal is to build software that is:

- Clean
- Modular
- Secure
- Easy to maintain
- Easy to explain during interviews