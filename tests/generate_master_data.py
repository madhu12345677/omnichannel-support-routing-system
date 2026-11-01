
import random
import pandas as pd
from faker import Faker

fake = Faker("en_IN")

# Master data configuration
CHANNELS = ["Email", "Chat", "Phone"]

LANGUAGES = [
    "English",
    "Telugu",
    "Hindi",
    "Tamil",
    "Kannada"
]

INTENTS = [
    "Order Status",
    "Refund",
    "Payment Issue",
    "Account Access",
    "Product Information",
    "Technical Support",
    "Cancellation",
    "Complaint"
]

SKILLS = [
    "Billing", "Technical", "Refund",
    "Sales", "Account Support",
    "Order Management", "Delivery",
    "Product Support", "Complaints",
    "General Support"
]

QUEUES = [
    "Billing Queue", "Technical Queue",
    "Refund Queue", "Sales Queue",
    "Account Queue", "General Queue"
]

# Generate 10,000 customers
customers = []

for i in range(1, 10001):
    customers.append({
        "customer_id": i,
        "customer_name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "language": random.choice(LANGUAGES)
    })

customers_df = pd.DataFrame(customers)

# Save customer data
customers_df.to_csv("customers.csv", index=False)

# Generate master data
master_data = {
    "channels": CHANNELS,
    "languages": LANGUAGES,
    "intents": INTENTS,
    "skills": SKILLS,
    "queues": QUEUES
}

for name, values in master_data.items():
    pd.DataFrame({
        f"{name[:-1] if name.endswith('s') else name}_name": values
    }).to_csv(f"{name}.csv", index=False)

print("Master data generated successfully!")
print("Customers:", len(customers_df))
print("Channels:", len(CHANNELS))
print("Languages:", len(LANGUAGES))
print("Intents:", len(INTENTS))
print("Skills:", len(SKILLS))
print("Queues:", len(QUEUES))
# Generate 100 agents
agents = []

for i in range(1, 101):
    agents.append({
        "agent_id": i,
        "agent_name": fake.name(),
        "email": f"agent{i}@yottaflex.com",
        "language": random.choice(LANGUAGES),
        "skill": random.choice(SKILLS),
        "queue": random.choice(QUEUES),
        "status": random.choice(["Available", "Busy", "Offline"])
    })

agents_df = pd.DataFrame(agents)

agents_df.to_csv("agents.csv", index=False)

print("Agents generated:", len(agents_df))