# SIEM Dashboard using ELK Stack

A Security Information and Event Management (SIEM) system built with Elasticsearch, Logstash, and Kibana for real-time security monitoring and threat detection.

![Project Status](https://img.shields.io/badge/status-completed-success)
![ELK Version](https://img.shields.io/badge/ELK-8.11.0-blue)
![Docker](https://img.shields.io/badge/docker-compose-blue)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Security Detection Rules](#security-detection-rules)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project demonstrates a functional SIEM system capable of:
- Collecting logs from multiple sources (SSH, web servers, firewalls)
- Parsing and enriching security events in real-time
- Detecting common attack patterns (SQL injection, brute force, path traversal)
- Visualizing security events through interactive dashboards
- Classifying threats by severity level

**Project Context:** Educational/demonstration project built for IBM internship application.

## ✨ Features

### Security Monitoring
- **Real-time log ingestion** from multiple sources
- **Attack pattern detection** using Logstash filters
- **Threat classification** (Critical, High, Medium, Low severity)
- **GeoIP enrichment** for attacker location tracking

### Supported Attack Detection
- Failed SSH authentication attempts (brute force)
- SQL injection patterns in web requests
- Path traversal attempts
- Suspicious HTTP response codes
- Blocked firewall connections

### Visualization
- Failed login timeline showing attack frequency
- Attack severity distribution pie chart
- Top attack sources IP table
- Event type breakdown bar chart
- Real-time log stream

## 🏗️ Architecture

```
┌─────────────────┐
│   Log Sources   │
│  (auth, apache, │
│   firewall)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Logstash     │
│  (Parse & Tag)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Elasticsearch   │
│ (Store & Index) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Kibana      │
│  (Visualize)    │
└─────────────────┘
```

## 📦 Prerequisites

### System Requirements
- **RAM:** 8GB minimum (16GB recommended)
- **CPU:** 4 cores recommended
- **Storage:** 50GB free space
- **OS:** Ubuntu 20.04/22.04 or similar Linux distribution

### Software Requirements
- Docker Engine 20.10+
- Docker Compose 1.29+
- Python 3.8+
- curl (for testing)

## 🚀 Installation

### 1. Clone or Create Project Directory

```bash
mkdir ~/elk-siem-project
cd ~/elk-siem-project
```

### 2. Configure System Settings

```bash
# Increase virtual memory for Elasticsearch
sudo sysctl -w vm.max_map_count=262144

# Make it permanent
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

Make it executable:

```bash
chmod +x log-generator.py
```

### 6. Start the ELK Stack

```bash
# Start all containers
docker-compose up -d

# Wait 30-60 seconds for initialization
sleep 60

# Verify all containers are running
docker ps
```

You should see three containers: elasticsearch, logstash, and kibana.

## 💻 Usage

### 1. Generate Security Logs

```bash
# Start log generator
python3 log-generator.py

# Let it run for 5-10 minutes to generate sufficient data
# Press Ctrl+C to stop
```

### 2. Verify Data Ingestion

```bash
# Check if logs are being created
ls -lh logs/

# Verify Elasticsearch has data (wait 1-2 minutes after generating logs)
curl http://localhost:9200/siem-logs-*/_count?pretty
```

Expected output:
```json
{
  "count" : 5000,
  "_shards" : {
    "total" : 1,
    "successful" : 1
  }
}
```

### 3. Access Kibana Dashboard

Open your browser and navigate to: `http://localhost:5601`

Wait 1-2 minutes for Kibana to fully initialize.

### 4. Create Data View

1. Click hamburger menu → **Management** → **Stack Management**
2. Go to **Kibana** → **Data Views**
3. Click **Create data view**
4. Configure:
   - **Name:** SIEM Logs
   - **Index pattern:** `siem-logs-*`
   - **Timestamp field:** `@timestamp`
5. Click **Save data view to Kibana**

### 5. View Logs in Discover

1. Click hamburger menu → **Analytics** → **Discover**
2. Select "SIEM Logs" from the dropdown
3. You should see your security events with parsed fields

### 6. Create Visualizations

Create a new dashboard and add these visualizations:

**Failed Login Timeline:**
- Type: Line or Area chart
- Vertical axis: Count
- Horizontal axis: @timestamp
- Filter: `event_type : "failed_login"`

**Attack Severity Pie Chart:**
- Type: Pie
- Metric: Count
- Slice by: `severity.keyword`

**Top Attack Sources:**
- Type: Table
- Rows: `client_ip.keyword`
- Metrics: Count

**Event Types Bar Chart:**
- Type: Bar vertical
- Horizontal axis: `event_type.keyword`
- Vertical axis: Count

## 📊 Dashboard

The SIEM dashboard provides:

- **7,414 events** processed (example from test run)
- **Real-time monitoring** with auto-refresh
- **Attack pattern visualization** showing threat trends
- **Severity distribution** for threat prioritization
- **Source IP tracking** for attacker identification

### Key Metrics
- **Low Severity:** ~60% (successful authentications, normal traffic)
- **High Severity:** ~33% (failed logins, blocked requests)
- **Critical Severity:** ~6% (SQL injection attempts)

## 🛡️ Security Detection Rules

### Brute Force Detection
```ruby
if "Failed password" in [message] {
  mutate { add_field => { "event_type" => "failed_login" } }
}
```

### SQL Injection Detection
```ruby
if "OR" in [request] {
  mutate { add_field => { "attack_type" => "sql_injection" } }
}
```

### Suspicious Response Codes
```ruby
if [response_code] == "403" {
  mutate { add_field => { "event_type" => "blocked_request" } }
}
```

## 📁 Project Structure

```
elk-siem-project/
├── docker-compose.yml          # Container orchestration
├── logstash/
│   └── pipeline/
│       └── logstash.conf       # Log parsing configuration
├── logs/                       # Generated log files
│   ├── auth.log               # SSH authentication logs
│   └── access.log             # Apache access logs
├── log-generator.py            # Security event simulator
└── README.md                   # This file
```

## 🔧 Troubleshooting

### Containers Not Starting

```bash
# Check container status
docker ps -a

# View logs for specific container
docker logs elasticsearch
docker logs logstash
docker logs kibana
```

### Elasticsearch Won't Start (Memory Issue)

```bash
# Reduce heap size in docker-compose.yml
ES_JAVA_OPTS=-Xms1g -Xmx1g

# Restart
docker-compose restart elasticsearch
```

### Kibana Shows "No Data"

```bash
# Check if data exists in Elasticsearch
curl http://localhost:9200/siem-logs-*/_count?pretty

# Adjust time range in Kibana to match your data
# Check time picker in top-right corner
```

### Logstash Not Processing Logs

```bash
# Check Logstash logs
docker logs logstash | tail -50

# Verify log files exist and have content
cat logs/auth.log | head -20

# Restart Logstash
docker-compose restart logstash
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R $USER:$USER logstash/ logs/

# Set proper permissions
chmod -R 755 logstash/
chmod -R 777 logs/
```

## 🚀 Future Enhancements

- [ ] Add Windows Event Log collection
- [ ] Integrate threat intelligence feeds (AbuseIPDB, VirusTotal)
- [ ] Implement machine learning for anomaly detection
- [ ] Create automated alerting (email, Slack)
- [ ] Add firewall log parsing
- [ ] Implement index lifecycle management
- [ ] Deploy multi-node Elasticsearch cluster
- [ ] Add authentication and encryption
- [ ] Create automated incident response playbooks

## 🤝 Contributing

This is an educational project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🙏 Acknowledgments

- Elastic Stack documentation
- Docker community
- Security community for attack pattern references

---

**Note:** This is a demonstration project for learning purposes. For production use, implement proper security measures including authentication, encryption, access controls, and regular security updates.
