
PRAGMA foreign_keys = ON;

-- 1. CHANNEL
CREATE TABLE IF NOT EXISTS channels (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE,
    calendar_type TEXT NOT NULL
        CHECK(calendar_type IN ('24x7', 'BUSINESS_HOURS')),
    business_start TEXT,
    business_end TEXT,
    timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata'
);

-- 2. LANGUAGE
CREATE TABLE IF NOT EXISTS languages (
    language_id TEXT PRIMARY KEY,
    language_name TEXT NOT NULL UNIQUE,
    language_code TEXT NOT NULL UNIQUE
);

-- 3. INTENT
CREATE TABLE IF NOT EXISTS intents (
    intent_id TEXT PRIMARY KEY,
    intent_name TEXT NOT NULL UNIQUE,
    description TEXT,
    default_priority TEXT NOT NULL
        CHECK(default_priority IN ('Critical','High','Medium','Low')),
    active INTEGER NOT NULL DEFAULT 1
        CHECK(active IN (0,1))
);

-- 4. SKILL
CREATE TABLE IF NOT EXISTS skills (
    skill_id TEXT PRIMARY KEY,
    skill_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 5. QUEUE
CREATE TABLE IF NOT EXISTS queues (
    queue_id TEXT PRIMARY KEY,
    queue_name TEXT NOT NULL UNIQUE,
    description TEXT,
    active INTEGER NOT NULL DEFAULT 1
        CHECK(active IN (0,1))
);

-- 6. CUSTOMER
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT UNIQUE,
    preferred_language_id TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (preferred_language_id)
        REFERENCES languages(language_id)
);

-- 7. AGENT
CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL
        CHECK(status IN ('Active','Inactive','On Leave')),
    shift_start TEXT NOT NULL,
    shift_end TEXT NOT NULL,
    max_concurrent_tickets INTEGER NOT NULL
        CHECK(max_concurrent_tickets > 0)
);

-- 8. AGENT SKILLS (Bridge table)
CREATE TABLE IF NOT EXISTS agent_skills (
    agent_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    proficiency TEXT NOT NULL
        CHECK(proficiency IN ('Basic','Intermediate','Expert')),
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    PRIMARY KEY(agent_id, skill_id, effective_from),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
    CHECK(effective_to IS NULL OR effective_to >= effective_from)
);

-- 9. AGENT LANGUAGES (Bridge table)
CREATE TABLE IF NOT EXISTS agent_languages (
    agent_id TEXT NOT NULL,
    language_id TEXT NOT NULL,
    proficiency TEXT NOT NULL
        CHECK(proficiency IN ('Basic','Intermediate','Fluent')),
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    PRIMARY KEY(agent_id, language_id, effective_from),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY (language_id) REFERENCES languages(language_id),
    CHECK(effective_to IS NULL OR effective_to >= effective_from)
);

-- 10. PRIORITY RULE
CREATE TABLE IF NOT EXISTS priority_rules (
    rule_id TEXT PRIMARY KEY,
    intent_id TEXT NOT NULL,
    channel_id TEXT,
    priority TEXT NOT NULL
        CHECK(priority IN ('Critical','High','Medium','Low')),
    first_response_minutes INTEGER NOT NULL
        CHECK(first_response_minutes > 0),
    resolution_minutes INTEGER NOT NULL
        CHECK(resolution_minutes > 0),
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    FOREIGN KEY (intent_id) REFERENCES intents(intent_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    CHECK(effective_to IS NULL OR effective_to >= effective_from)
);

-- 11. TICKET
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    intent_id TEXT NOT NULL,
    language_id TEXT NOT NULL,
    queue_id TEXT,
    rule_id TEXT,
    subject TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL
        CHECK(priority IN ('Critical','High','Medium','Low')),
    status TEXT NOT NULL
        CHECK(status IN (
            'New','Open','Assigned','In Progress',
            'Pending','Resolved','Closed','Reopened','Unassigned'
        )),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (intent_id) REFERENCES intents(intent_id),
    FOREIGN KEY (language_id) REFERENCES languages(language_id),
    FOREIGN KEY (queue_id) REFERENCES queues(queue_id),
    FOREIGN KEY (rule_id) REFERENCES priority_rules(rule_id)
);

-- 12. MESSAGE
CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    sender_type TEXT NOT NULL
        CHECK(sender_type IN ('Customer','Agent','System')),
    sender_customer_id TEXT,
    sender_agent_id TEXT,
    message_text TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (sender_customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (sender_agent_id) REFERENCES agents(agent_id),
    UNIQUE(ticket_id, sequence_number),
    CHECK(
        (sender_type = 'Customer' AND sender_customer_id IS NOT NULL
            AND sender_agent_id IS NULL)
        OR
        (sender_type = 'Agent' AND sender_agent_id IS NOT NULL
            AND sender_customer_id IS NULL)
        OR
        (sender_type = 'System' AND sender_customer_id IS NULL
            AND sender_agent_id IS NULL)
    )
);

-- 13. ASSIGNMENT EVENT
CREATE TABLE IF NOT EXISTS assignment_events (
    assignment_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    agent_id TEXT,
    queue_id TEXT,
    action_type TEXT NOT NULL
        CHECK(action_type IN (
            'Assigned','Transferred','Unassigned','Escalated'
        )),
    routing_reason TEXT,
    event_time TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY (queue_id) REFERENCES queues(queue_id)
);

-- 14. SLA EVENT
CREATE TABLE IF NOT EXISTS sla_events (
    sla_event_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    event_type TEXT NOT NULL
        CHECK(event_type IN (
            'Started','First_Response','At_Risk',
            'Breached','Met','Escalated'
        )),
    target_at TEXT,
    actual_at TEXT,
    event_time TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

-- 15. RESOLUTION
CREATE TABLE IF NOT EXISTS resolutions (
    resolution_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    resolution_status TEXT NOT NULL
        CHECK(resolution_status IN ('Resolved','Rejected')),
    resolution_notes TEXT,
    resolved_at TEXT NOT NULL,
    customer_satisfaction INTEGER
        CHECK(customer_satisfaction BETWEEN 1 AND 5),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

-- INDEXES FOR FASTER QUERIES
CREATE INDEX IF NOT EXISTS idx_ticket_status
ON tickets(status);

CREATE INDEX IF NOT EXISTS idx_ticket_priority
ON tickets(priority);

CREATE INDEX IF NOT EXISTS idx_assignment_ticket
ON assignment_events(ticket_id);

CREATE INDEX IF NOT EXISTS idx_sla_ticket
ON sla_events(ticket_id);
