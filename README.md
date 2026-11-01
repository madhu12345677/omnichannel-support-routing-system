\# YottaFlex AI – Customer Support Ticket Routing \& SLA Management System



\## 1. Project Overview



This project is an AI-assisted customer support ticket routing and SLA management system.



It helps support teams organize customer tickets, identify routing requirements, monitor agent workload, and track SLA performance.



\## 2. Business Problem



Customer support teams receive requests through multiple channels such as Email, Chat, and Phone.



Manual ticket assignment can cause:

\- Delayed responses

\- Incorrect agent assignments

\- Agent workload imbalance

\- SLA breaches

\- Difficulty tracking ticket history



\## 3. Proposed Solution



The system maintains customer tickets, messages, agent information, assignment events, SLA events, and resolution records.



The routing simulation considers:

\- Ticket intent and required skill

\- Customer language

\- Agent availability

\- Agent concurrent ticket capacity



\## 4. Main Modules



\- Customer and agent master data

\- Ticket and message management

\- Intent and priority rules

\- Agent skills and language mapping

\- Ticket routing simulation

\- Overflow queue management

\- SLA event tracking

\- Resolution and customer satisfaction tracking

\- Routing dashboard



\## 5. Technology Stack



\- Python

\- Streamlit

\- SQLite

\- Pandas

\- SQL

\- VS Code



\## 6. Database



Database file: `database/support\_system.db`



Schema file: `database/schema.sql`



The database contains 18 tables covering master data, tickets, messages, assignments, SLA events, resolutions, and routing simulation.



\## 7. Current Dataset



\- Customers: 10,000

\- Agents: 100

\- Tickets: 5,000

\- Messages: 20,000

\- Assignment events: 5,000

\- SLA events: 15,000

\- Resolutions: 1,116



These are the current database counts and not the final target dataset sizes.



\## 8. Run the Application



Install dependencies:



```bash

pip install streamlit pandas faker

