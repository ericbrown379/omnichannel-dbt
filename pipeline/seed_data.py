# Data Lineage
# Source: local generation (not a real source system)
# Pipeline: mysql-bq-pipeline seed v1
# Schedule: one-off, manual
# Owner: eric.brown@thelyst.com
"""
Seeds Omni_Management with referentially-consistent sample data so the
MySQL -> BigQuery pipeline has something real to move.
Run: python seed_data.py
"""
import os
import random
from datetime import datetime, timedelta

import mysql.connector as connection
from dotenv import load_dotenv

load_dotenv()

random.seed(42)

CHANNELS = ["Organic Search", "Paid Search", "Paid Social", "Email", "Direct"]

FIRST_NAMES = ["Ava", "Liam", "Maya", "Noah", "Sofia", "Ethan", "Zoe", "Mason",
               "Ivy", "Lucas", "Nora", "Elias", "Priya", "Omar", "Grace", "Kai",
               "Layla", "Diego", "Chloe", "Ravi", "Emma", "Yusuf", "Isla", "Theo",
               "Amara", "Felix", "Nadia", "Owen", "Sana", "Milo"]
LAST_NAMES = ["Reyes", "Nguyen", "Patel", "Okafor", "Kowalski", "Rossi", "Muller",
              "Kim", "Silva", "Haddad", "Fischer", "Chen", "Novak", "Alvarez",
              "Larsson", "Duarte", "Ibrahim", "Sato", "Weber", "Costa"]
COUNTRY_DIAL = [("United States", "1"), ("United Kingdom", "44"), ("Canada", "1"),
                 ("Germany", "49"), ("Australia", "61"), ("Brazil", "55"),
                 ("India", "91"), ("France", "33")]

PRODUCTS = [
    ("Starter Plan - Monthly", 29.00),
    ("Starter Plan - Annual", 290.00),
    ("Growth Plan - Monthly", 79.00),
    ("Growth Plan - Annual", 790.00),
    ("Pro Plan - Monthly", 149.00),
    ("Pro Plan - Annual", 1490.00),
    ("Onboarding Package", 499.00),
    ("Analytics Add-on", 39.00),
    ("Priority Support Add-on", 59.00),
    ("Custom Integration", 899.00),
    ("Brand Audit", 1200.00),
    ("Campaign Sprint", 2500.00),
    ("Creative Refresh", 950.00),
    ("SEO Audit", 650.00),
    ("Reporting Dashboard License", 199.00),
]


def random_phone(dial_code):
    if dial_code == "1":
        area = random.randint(200, 989)
        exch = random.randint(200, 989)
        line = random.randint(0, 9999)
        return f"+{dial_code}{area}{exch}{line:04d}"
    subscriber = random.randint(10**8, 10**9 - 1)
    return f"+{dial_code}{subscriber}"


def random_date_birth():
    start = datetime(1962, 1, 1)
    end = datetime(2004, 12, 31)
    delta_days = (end - start).days
    return (start + timedelta(days=random.randint(0, delta_days))).date()


def random_recent_datetime(days_back=365):
    now = datetime(2026, 8, 20, 12, 0, 0)
    delta_seconds = random.randint(0, days_back * 24 * 3600)
    return now - timedelta(seconds=delta_seconds)


def main():
    db = connection.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ.get("MYSQL_PORT", 3306)),
        user=os.environ["MYSQL_USER"],
        passwd=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )
    cur = db.cursor()

    for table in ("channels", "customers", "products", "purchaseHistory", "visitHistory"):
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        assert count == 0, f"{table} is not empty ({count} rows) — refusing to seed on top of existing data"

    channel_ids = []
    for name in CHANNELS:
        cur.execute("INSERT INTO channels (channel_name) VALUES (%s)", (name,))
        channel_ids.append(cur.lastrowid)
    db.commit()
    print(f"records_out channels: {len(channel_ids)}")

    customer_ids = []
    used_emails = set()
    for _ in range(60):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        country, dial = random.choice(COUNTRY_DIAL)
        base_email = f"{first.lower()}.{last.lower()}@example.com"
        email = base_email
        suffix = 1
        while email in used_emails:
            email = f"{first.lower()}.{last.lower()}{suffix}@example.com"
            suffix += 1
        used_emails.add(email)
        cur.execute(
            "INSERT INTO customers (name, date_birth, email_address, phone_number, country) "
            "VALUES (%s, %s, %s, %s, %s)",
            (name, random_date_birth(), email, random_phone(dial), country),
        )
        customer_ids.append(cur.lastrowid)
    db.commit()
    print(f"records_out customers: {len(customer_ids)}")
    assert len(used_emails) == len(customer_ids), "Duplicate emails detected"

    product_skus = []
    for pname, price in PRODUCTS:
        cur.execute(
            "INSERT INTO products (product_name, unit_price) VALUES (%s, %s)",
            (pname, price),
        )
        product_skus.append(cur.lastrowid)
    db.commit()
    print(f"records_out products: {len(product_skus)}")

    visit_rows = 400
    for _ in range(visit_rows):
        cust = random.choice(customer_ids)
        chan = random.choice(channel_ids)
        visit_ts = random_recent_datetime()
        bounced = random.random() < 0.35
        bounce_ts = visit_ts + timedelta(seconds=random.randint(3, 45)) if bounced else None
        cur.execute(
            "INSERT INTO visitHistory (customer_id, channel_id, visit_timestamp, bounce_timestamp) "
            "VALUES (%s, %s, %s, %s)",
            (cust, chan, visit_ts, bounce_ts),
        )
    db.commit()
    print(f"records_out visitHistory: {visit_rows}")

    purchase_rows = 250
    for _ in range(purchase_rows):
        cust = random.choice(customer_ids)
        sku = random.choice(product_skus)
        chan = random.choice(channel_ids)
        qty = random.randint(1, 5)
        discount = random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20])
        order_date = random_recent_datetime()
        cur.execute(
            "INSERT INTO purchaseHistory (customer_id, product_sku, channel_id, quantity, discount, order_date) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (cust, sku, chan, qty, discount, order_date),
        )
    db.commit()
    print(f"records_out purchaseHistory: {purchase_rows}")

    for table in ("channels", "customers", "products", "purchaseHistory", "visitHistory"):
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]} rows")

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
