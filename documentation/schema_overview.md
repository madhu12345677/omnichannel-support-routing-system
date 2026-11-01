\# Database Schema Overview

\## YottaFlex AI – Customer Support Ticket Routing \& SLA Management System



\## 1. Introduction



The database schema defines how customer support information is stored, connected, and managed.



The system uses SQLite as its database.



It contains master data tables, transaction tables, event history tables, and routing simulation tables.



\## 2. Database Architecture



The database is organized into four main groups.



\### A. Master Data Tables



These tables store reference information used by the system.



\- customers

\- channels

\- agents

\- intents

\- languages

\- skills

\- queues

\- priority\_rules



\### B. Transaction Tables



These tables store customer support activities.



\- tickets

\- messages

\- resolutions



\### C. Event History Tables



These tables preserve important changes and SLA activities.



\- assignment\_events

\- sla\_events



\### D. Routing Support Tables



These tables support agent matching and routing simulation.



\- agent\_skills

\- agent\_languages

\- overflow\_queue

\- simulation\_assignments



\## 3. Primary Keys and Foreign Keys



\### Primary Keys



A Primary Key (PK) uniquely identifies each record in a table.



Examples:

\- Customer ID identifies a customer.

\- Ticket ID identifies a ticket.

\- Agent ID identifies an agent.

\- Message ID identifies a message.



\### Foreign Keys



A Foreign Key (FK) connects records between related tables.



Examples:

\- tickets.customer\_id references customers.

\- messages.ticket\_id references tickets.

\- assignment\_events.ticket\_id references tickets.

\- assignment\_events.agent\_id references agents.

\- sla\_events.ticket\_id references tickets.



Foreign key relationships help maintain data consistency.



\## 4. Relationship Overview



| Parent Table | Child Table | Relationship |

|---|---|---|

| customers | tickets | One-to-Many |

| tickets | messages | One-to-Many |

| tickets | assignment\_events | One-to-Many |

| tickets | sla\_events | One-to-Many |

| agents | assignment\_events | One-to-Many |

| agents | agent\_skills | One-to-Many |

| skills | agent\_skills | One-to-Many |

| agents | agent\_languages | One-to-Many |

| languages | agent\_languages | One-to-Many |

| tickets | resolutions | One-to-One in current data |



\## 5. Many-to-Many Relationships



Some entities have Many-to-Many relationships.



\### Agents and Skills



\- One agent can have multiple skills.

\- One skill can be assigned to multiple agents.

\- The `agent\_skills` bridge table connects them.



\### Agents and Languages



\- One agent can support multiple languages.

\- One language can be supported by multiple agents.

\- The `agent\_languages` bridge table connects them.



\## 6. Ticket Routing Workflow



1\. A customer creates a support ticket.

2\. The ticket is associated with a channel and intent.

3\. The system identifies the required skill and language.

4\. Eligible agents are checked based on status and capacity.

5\. The routing simulation selects a suitable available agent.

6\. Assignment details are stored in simulation assignments.

7\. Tickets without an eligible available agent remain in the overflow queue.

8\. SLA events are used to track response performance.

9\. Resolution details are stored when a ticket is resolved.



\## 7. Data Integrity Rules



\- Primary keys must be unique.

\- Foreign keys must reference valid parent records.

\- Ticket statuses must follow allowed values.

\- Agent capacity must not be exceeded during routing.

\- Event history should be preserved.

\-

