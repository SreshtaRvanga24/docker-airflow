import pandas as pd
import random
from faker import Faker

fake = Faker()
ROWS = 150

# ---------------- PRODUCTS ----------------
products = pd.DataFrame({
    "product_id": range(1, ROWS + 1),
    "sku": [f"SKU{random.randint(100000,999999)}" for _ in range(ROWS)],
    "product_name": [fake.word().capitalize() for _ in range(ROWS)],
    "category": [random.choice(["Apparel","Footwear","Electronics","Grocery","Fitness"]) for _ in range(ROWS)],
    "price": [round(random.uniform(5, 500), 2) for _ in range(ROWS)],
    "cost": [round(random.uniform(3, 300), 2) for _ in range(ROWS)]
})

# ---------------- CUSTOMERS ----------------
customers = pd.DataFrame({
    "customer_id": range(1, ROWS + 1),
    "name": [fake.name() for _ in range(ROWS)],
    "email": [fake.email() for _ in range(ROWS)],
    "city": [fake.city() for _ in range(ROWS)],
    "loyalty_tier": [random.choice(["Silver","Gold","Platinum"]) for _ in range(ROWS)]
})

# ---------------- STORES ----------------
stores = pd.DataFrame({
    "store_id": range(1, ROWS + 1),
    "store_name": [fake.company() for _ in range(ROWS)],
    "city": [fake.city() for _ in range(ROWS)],
    "store_type": [random.choice(["Mall","Standalone","Online"]) for _ in range(ROWS)]
})

# ---------------- SUPPLIERS ----------------
suppliers = pd.DataFrame({
    "supplier_id": range(1, ROWS + 1),
    "supplier_name": [fake.company() for _ in range(ROWS)],
    "country": [fake.country() for _ in range(ROWS)],
    "lead_time_days": [random.randint(3, 30) for _ in range(ROWS)]
})

# ---------------- INVENTORY ----------------
inventory = pd.DataFrame({
    "inventory_id": range(1, ROWS + 1),
    "product_id": random.sample(list(products.product_id), ROWS),
    "store_id": random.sample(list(stores.store_id), ROWS),
    "stock_on_hand": [random.randint(0, 500) for _ in range(ROWS)],
    "reorder_level": [random.randint(20, 100) for _ in range(ROWS)]
})

# ---------------- TRANSACTIONS ----------------
transactions = pd.DataFrame({
    "transaction_id": range(1, ROWS + 1),
    "customer_id": random.choices(customers.customer_id, k=ROWS),
    "product_id": random.choices(products.product_id, k=ROWS),
    "store_id": random.choices(stores.store_id, k=ROWS),
    "quantity": [random.randint(1, 5) for _ in range(ROWS)],
    "total_amount": [round(random.uniform(10, 1000), 2) for _ in range(ROWS)],
    "transaction_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(ROWS)]
})

# ---------------- RETURNS ----------------
returns = pd.DataFrame({
    "return_id": range(1, ROWS + 1),
    "transaction_id": random.choices(transactions.transaction_id, k=ROWS),
    "reason": [random.choice(["Damaged","Wrong Item","No Longer Needed"]) for _ in range(ROWS)],
    "refund_amount": [round(random.uniform(5, 500), 2) for _ in range(ROWS)]
})

# ---------------- PROMOTIONS ----------------
promotions = pd.DataFrame({
    "promotion_id": range(1, ROWS + 1),
    "promo_name": [fake.catch_phrase() for _ in range(ROWS)],
    "discount_pct": [random.choice([5,10,15,20,30]) for _ in range(ROWS)],
    "start_date": [fake.date_between("-6m", "today") for _ in range(ROWS)],
    "end_date": [fake.date_between("today", "+3m") for _ in range(ROWS)]
})

# ---------------- SAVE ----------------
products.to_csv("products.csv", index=False)
customers.to_csv("customers.csv", index=False)
stores.to_csv("stores.csv", index=False)
suppliers.to_csv("suppliers.csv", index=False)
inventory.to_csv("inventory.csv", index=False)
transactions.to_csv("transactions.csv", index=False)
returns.to_csv("returns.csv", index=False)
promotions.to_csv("promotions.csv", index=False)
