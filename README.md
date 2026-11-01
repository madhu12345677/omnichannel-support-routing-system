
# AI-Powered Customer Support Ticket Routing & SLA Management System

## Project Overview

The AI-Powered Customer Support Ticket Routing & SLA Management System is designed to organize customer support tickets and assign them to suitable agents based on ticket intent, priority, language, agent skills, and available capacity.

The system also tracks Service Level Agreement (SLA) events, monitors ticket status, and provides dashboards for analyzing routing and support performance.

## Problem Statement

Customer support teams receive tickets through multiple channels such as email, chat, and phone. Manually assigning tickets can cause delays, incorrect routing, agent overload, and SLA violations.

## Proposed Solution

This project provides a structured ticket routing and monitoring system that:

- Categorizes customer support tickets by intent.
- Considers ticket priority and language.
- Matches tickets with agents based on skills.
- Checks agent workload and capacity.
- Places tickets in an overflow queue when suitable agents are unavailable.
- Tracks SLA events and ticket resolutions.
- Displays operational insights through dashboards.

## Key Features

- Ticket and customer data management
- Multi-channel support
- Intent and priority-based routing
- Agent skill and language matching
- Agent workload and capacity monitoring
- Overflow queue management
- SLA tracking and monitoring
- Routing simulation
- Dashboard and performance reporting

## Technology Stack

- **Programming:** Python
- **Frontend / Dashboard:** Streamlit
- **Database:** SQLite
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Version Control:** Git and GitHub

## Project Structure

```text
YottaFlex_Customer_Support_AI/
│
├── app.py
├── simulation_router.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── support_system.db
│   └── schema.sql
│
├── data/
│   ├── csv/
│   └── json/
│
├── dashboards/
├── documentation/
├── src/
├── tests/
│
├── generate_master_data.py
├── generate_tickets.py
├── generate_messages.py
├── generate_assignments.py
├── generate_sla_events.py
└── validate_database.py
```

## Database

The project uses SQLite and includes structured tables for:

- Customers
- Agents
- Tickets
- Messages
- Channels
- Languages
- Skills
- Queues
- Assignment events
- SLA events
- Resolutions
- Overflow queue
- Simulation assignments

## Routing Logic

The routing simulation follows these steps:

1. Read tickets waiting for assignment.
2. Identify ticket intent and required skill.
3. Check the ticket language.
4. Find active agents with matching skills and languages.
5. Check agent workload and available capacity.
6. Assign the ticket to an eligible agent with available capacity.
7. Keep tickets in the waiting queue when no suitable agent is available.

## Sample Simulation Results

The current sample project contains:

- 5,000 tickets
- 20,000 messages
- 100 agents
- 5,000 initial SLA records

Sample SLA results:

| Metric | Result |
|---|---:|
| SLA Met | 4,376 |
| SLA Breached | 624 |
| SLA Compliance | 87.52% |

These are results from the current generated dataset and simulation, not live production metrics.

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/madhu12345677/omnichannel-support-routing-system.git
```

### 2. Open the project folder

```bash
cd omnichannel-support-routing-system
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
python -m streamlit run app.py
```

## Validation

The project includes scripts for checking:

- Database tables and relationships
- Primary and foreign keys
- Ticket and assignment schemas
- Agent capacity
- Overflow queue
- SLA events
- Database consistency

Run the database validation script:

```bash
python validate_database.py
```

## Future Enhancements

- AI/LLM-based ticket intent classification
- Advanced priority prediction
- Real-time email, chat, and phone integrations
- Dynamic agent workload balancing
- Improved SLA breach prediction
- Agent performance analytics
- Automated ticket resolution suggestions

## Author

**Madhu Chandana Singareddy**

GitHub: https://github.com/madhu12345677