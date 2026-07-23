# LogLens - Simplified Security Log Analysis

![LogLens Banner](docs/banner.png)


# Overview

LogLens is a lightweight Security Information and Event Management (SIEM-lite) platform designed to analyze Apache/Nginx web server logs.

Traditional server logs contain millions of requests, making manual investigation extremely difficult. LogLens automates log ingestion, parsing, threat detection, geographic enrichment, and security visualization through an interactive SOC dashboard.

The system helps security analysts answer:

- Who attacked the system?
- What attack technique was used?
- When did the attack happen?
- Where did the attacker originate?


---

# Screenshots


## SOC Dashboard

![SOC Dashboard](docs/dashboard.png)


The SOC dashboard provides:

- Real-time security overview
- Attack statistics
- Severity analysis
- Threat intelligence
- Geographic attack visualization
- Timeline monitoring



## Threat Center

![Threat Center](docs/threat-center.png)


The Threat Center allows analysts to:

- Search security incidents
- Filter threats by severity
- Filter by attack type
- Investigate individual detections
- View matched attack signatures



## Analytics Dashboard

![Analytics](docs/analytics.png)


Analytics provides:

- Attack trends
- Source IP analysis
- Attack distribution
- Detection timelines



## Investigation Panel

![Investigation Panel](docs/investigation.png)


Security analysts can inspect:

- Source information
- Attack classification
- Request details
- Matched patterns
- Raw log evidence



---

# Features


# Log Processing


LogLens supports efficient processing of large Apache/Nginx log files.


Features:

- Apache/Nginx Common Log Format support
- Streaming file processing
- Large log file handling
- Batch database insertion
- Background processing using Redis Queue
- Asynchronous worker architecture


Large files are processed without loading the complete file into memory.


---

# Threat Detection


## Signature Based Detection


LogLens uses configurable regex-based detection signatures to identify malicious requests.


Currently detected attacks:


### Cross-Site Scripting (XSS)

Detects malicious script injection attempts.


Example:


GET /search?q=<script>alert(1)</script>




### Directory Traversal

Detects attempts to access restricted files.


Example:


GET /../../etc/passwd




### Sensitive File Access

Detects attempts to access sensitive resources.


Examples:


.env

phpinfo.php

robots.txt

sitemap.xml




Detection rules are stored separately and can be extended with additional signatures.



---

# Brute Force Detection


LogLens detects repeated authentication failures.


Example:


POST /login 401
POST /login 401
POST /login 401
POST /login 401



Repeated failed login attempts are automatically classified as high severity security events.



---

# Threat Intelligence


Each detected security event contains:


- Source IP
- Attack type
- Severity
- Timestamp
- HTTP method
- Request path
- Status code
- Matched signature pattern
- Raw log entry


This information allows analysts to investigate the complete attack context.



---

# GeoIP Intelligence


LogLens enriches detected threats with geographic information.


Provides:

- Country
- City
- Latitude
- Longitude
- Public/private IP classification


Threat locations are displayed using an interactive global attack map.



---

# SOC Dashboard


The security dashboard provides:


## Security Overview

- Total detected attacks
- Critical threats
- Attack categories
- Threat signatures



## Threat Intelligence

Displays:

- Most active attacker IP
- Top attack origin country
- Most targeted endpoint
- Highest risk attack type
- Latest security event
- Network exposure analysis



## Visualization

Includes:

- Severity distribution
- Attack classification charts
- Detection timeline
- Top attacker ranking
- Global attack map



## Investigation Workflow

Security analysts can:

- Select incidents
- Review detailed evidence
- Analyze attack patterns
- Investigate suspicious activity



---

# Architecture


                     React Dashboard
                           |
                           |
                     Flask REST API
                           |
    ------------------------------------------------
    |                      |                       |

Log Parser Detection Engine GeoIP Service
| |
| -----------------
| | |
| Signature Rules Brute Force Detection
|
|
PostgreSQL Database

                           |
                           |
                 Redis Queue + RQ Workers


---

# Processing Pipeline


LogLens follows this processing workflow:



Upload Log File

   |

Background Job Created

   |

Redis Queue

   |

RQ Worker

   |

Streaming Parser

   |

Threat Detection

   |

GeoIP Enrichment

   |

Database Storage

   |

Dashboard Analytics



The asynchronous architecture prevents large log uploads from blocking API requests.



---

# Production Deployment Architecture


                 Users

                   |

            React Frontend

                   |

             Flask Backend

                   |

    --------------------------------

    |                              |

PostgreSQL Database Upstash Redis

                                  |

                              RQ Worker


Production components:


Frontend:

- React/Vite application


Backend:

- Flask API service


Database:

- PostgreSQL


Queue:

- Upstash Redis


Background Processing:

- RQ worker service
