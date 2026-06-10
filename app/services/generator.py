
import csv
from faker import Faker
import random
from datetime import datetime

fake = Faker()
random.seed(42)


# -------------------------
# WRITE CSV HELPER
# -------------------------
def write_csv(filename, data):
    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


# -------------------------
# CUSTOMERS
# -------------------------
def generate_customers(filename, count=100000):

    customers = [
        {
            "id": i,
            "name": fake.name(),
            "email": fake.email(),
            "created_at": datetime.now().isoformat()
        }
        for i in range(1, count + 1)
    ]

    write_csv(filename, customers)
    print(f"Customers saved → {filename}")


# -------------------------
# ORDERS
# -------------------------
def generate_orders(filename, count=1000000):

    orders = [
        {
            "id": i,
            "customer_id": random.randint(1, 100000),
            "amount": round(random.uniform(10, 1000), 2),
            "order_date": datetime.now().isoformat()
        }
        for i in range(1, count + 1)
    ]

    write_csv(filename, orders)
    print(f"Orders saved → {filename}")


# -------------------------
# REFUNDS
# -------------------------
def generate_refunds(filename, count=200000):

    refunds = [
        {
            "id": i,
            "order_id": random.randint(1, 1000000),
            "refund_amount": round(random.uniform(5, 200), 2),
            "refund_date": datetime.now().isoformat()
        }
        for i in range(1, count + 1)
    ]

    write_csv(filename, refunds)
    print(f"Refunds saved → {filename}")