# 🛡️ Sentinel Access

Enterprise Operational Intelligence Platform for Access Control Analytics.

Developed by Yago Marinho.

---

# Overview

Sentinel Access is an enterprise analytics platform designed for operational analysis of physical access control events exported from Genetec Security Desk.

The platform enables:

- Operational analytics
- Access flow investigation
- Department movement analysis
- Shift behavior monitoring
- Security compliance insights
- Historical event research
- Corporate access intelligence

---

# Main Features

## 📥 CSV Import

Import CSV files exported directly from:

- Genetec Security Desk 5.6

Uploaded files are automatically stored in:

```text
data/uploads
```

---

## 🔍 Intelligent Search

Search by:

- Employee Name
- Badge ID
- Door
- Department
- Company
- Credential
- Supervisor

---

## 📊 Operational Dashboard

Real-time analytical visualization from imported datasets:

- Total Access Events
- Active Employees
- Monitored Doors
- Operational Indicators

---

## 🏢 Designed For

- Industrial Facilities
- Corporate Security Operations
- Access Control Management
- Multinational Companies
- Compliance Teams
- Operational Intelligence Centers

---

# Current Architecture

```text
Sentinel-Access/

├── app.py
├── README.md
│
├── assets/
│   ├── logo.png
│   └── styles.css
│
├── data/
│   └── uploads/
│
├── processed/
│
└── venv/
```

---

# Technologies

- Python
- Streamlit
- Pandas
- PySpark (Upcoming)
- Plotly (Upcoming)

---

# Upcoming Features

## Analytics Engine

- Shift analysis
- 12x36 scale detection
- Duplicate access filtering
- Early access detection
- Security anomalies
- Operational heatmaps

---

## Enterprise Features

- User authentication
- Administrative panel
- PDF export
- Executive reports
- KPI dashboards
- Historical analytics

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Sentinel-Access.git
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\\Scripts\\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
streamlit run app.py
```

---

# Data Structure

Expected CSV structure:

| Field | Description |
|---|---|
| Evento | Access Event |
| Porta | Door |
| Lado | Reader Direction |
| Matricula | Employee ID |
| Nome | Employee Name |
| Sobrenome | Last Name |
| Empresa | Company |
| Credencial | Credential |
| DataHora | Event Timestamp |
| Departamento | Department |
| Gestor | Supervisor |

---

# Copyright

© 2026 Sentinel Access

Developed by Yago Marinho.

All rights reserved.