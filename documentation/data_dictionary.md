\# Data Dictionary

\## YottaFlex AI – Customer Support Ticket Routing \& SLA Management System



\## 1. Introduction



This document describes the database entities, their purpose, relationships, and important business rules used in the Customer Support Ticket Routing and SLA Management System.



The database is implemented using SQLite.



\## 2. Database Entities



| Table Name | Purpose |

|---|---|

| customers | Stores customer information |

| channels | Stores support channels such as Email, Chat, and Phone |

| tickets | Stores customer support tickets |

| messages | Stores conversations related to tickets |

| intents | Stores customer request categories |

| languages | Stores supported languages |

| agents | Stores support agent information |

| skills | Stores agent skill categories |

| agent\_skills | Maps agents to their skills |

| agent\_languages | Maps agents to supported languages |

| queues | Stores ticket queues |

| priority\_rules | Defines ticket priority and SLA targets |

| assignment\_events | Maintains ticket assignment history |

| sla\_events | Tracks SLA activities and outcomes |

| resolutions | Stores ticket resolution details |

| overflow\_queue | Stores tickets waiting for routing |

| simulation\_assignments | Stores routing simulation results |



\## 3. Important Entity Descriptions



\### Customers

Stores customer details used to identify the person who raised a support ticket.



\### Agents

Stores support agent details, including status, shift information, and maximum concurrent ticket capacity.



\### Tickets

Stores support requests, including ticket status, priority, customer, channel, intent, and creation time.



\### Messages

Stores customer, agent, and system messages associated with tickets.



\### Intents

Defines the category of a customer request and helps determine routing requirements.



\### Skills

Defines the skills required to handle different types of support requests.



\### Agent Skills

A bridge table that connects agents with their skills. One agent can have multiple skills.



\### Agent Languages

A bridge table that connects agents with supported languages.



\### Assignment Events

Maintains a history of ticket assignment, transfer, unassignment, and escalation activities.



\### SLA Events

Tracks SLA start, first response, at-risk, breached, met, and escalation events.



\### Resolutions

Stores ticket resolution status, resolution details, and customer satisfaction scores.



\### Overflow Queue

Stores tickets that are waiting for an eligible agent or available capacity.



\### Simulation Assignments

Stores the results of the routing simulation, including assigned agent and routing reason.



\## 4. Database Relationships



\- One customer can create multiple tickets.

\- One ticket can contain multiple messages.

\- One ticket can have multiple assignment events.

\- One ticket can have multiple SLA events.

\- One agent can handle multiple tickets.

\- One agent can have multiple skills.

\- One skill can belong

