from faker import Faker
import random
from datetime import datetime
import mysql.connector
from src.config.db_config import DB_CONFIG

fake = Faker()

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

customers = []
payments = []
usage_metrics = []
support_tickets = []

# ------------------- Realistic location setup -------------------
# Big cities: ~50% of customers
big_cities = ['New York', 'Los Angeles', 'Chicago']
# Medium cities: ~30% of customers
medium_cities = ['Austin', 'Denver', 'Seattle']
# Rare cities: ~20% of customers
rare_cities = [fake.city() for _ in range(600)]  # Generate enough rare cities

# Create weighted location list for sampling
weighted_locations = big_cities * 1500 + medium_cities * 300 + rare_cities  # Adjust for 3000 rows
random.shuffle(weighted_locations)  # Shuffle for randomness

# ------------------- Generate data -------------------
for i in range(1, 3001):  # 3000 customers

    signup_date = fake.date_between(start_date='-2y', end_date='-6m')
    last_login_date = fake.date_between(start_date=signup_date, end_date='today')

    age = random.randint(18, 60)
    
    # Pick location from weighted list
    location = weighted_locations[i-1]

    subscription_type = random.choice(["Monthly", "Yearly"])

    customers.append((i, age, location, signup_date, subscription_type))

    
    last_payment_date = fake.date_between(start_date=signup_date, end_date='today')
    payment_delay_days = random.randint(0, 15)
    failed_payments_count = random.randint(0, 4)

    payments.append((i, last_payment_date, payment_delay_days, failed_payments_count))

    
    avg_weekly_usage_hours = round(random.uniform(0, 20), 2)
    days_since_last_login = (datetime.today().date() - last_login_date).days
    courses_completed = random.randint(0, 10)

    usage_metrics.append((i, avg_weekly_usage_hours, days_since_last_login, courses_completed))

    
    tickets_raised = random.randint(0, 5)
    last_ticket_days = random.randint(0, 365) if tickets_raised > 0 else None

    support_tickets.append((i, tickets_raised, last_ticket_days))

# ------------------- Insert into MySQL -------------------
cursor.executemany(
    "INSERT INTO customers (customer_id, age, location, signup_date, subscription_type) VALUES (%s,%s,%s,%s,%s)",
    customers
)

cursor.executemany(
    "INSERT INTO payments (customer_id, last_payment_date, payment_delay_days, failed_payments_count) VALUES (%s,%s,%s,%s)",
    payments
)

cursor.executemany(
    "INSERT INTO usage_metrics (customer_id, avg_weekly_usage_hours, days_since_last_login, courses_completed) VALUES (%s,%s,%s,%s)",
    usage_metrics
)

cursor.executemany(
    "INSERT INTO support_tickets (customer_id, tickets_raised, last_ticket_days) VALUES (%s,%s,%s)",
    support_tickets
)

conn.commit()
cursor.close()
conn.close()

print("Dummy data for 3000 customers generated and inserted successfully!")
