import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# Configuration
ROWS = 150
MIN_COST, MAX_COST = 3, 300
MIN_MARKUP, MAX_MARKUP = 1.2, 2.5  # 20% to 150% markup
CATEGORIES = ["Apparel", "Footwear", "Electronics", "Grocery", "Fitness"]
LOYALTY_TIERS = ["Silver", "Gold", "Platinum"]
STORE_TYPES = ["Mall", "Standalone", "Online"]
RETURN_REASONS = ["Damaged", "Wrong Item", "No Longer Needed"]
DISCOUNT_PERCENTAGES = [5, 10, 15, 20, 30]

# ---------------- PRODUCTS ----------------
costs = [round(random.uniform(MIN_COST, MAX_COST), 2) for _ in range(ROWS)]
products = pd.DataFrame({
    "product_id": range(1, ROWS + 1),
    "sku": [f"SKU{random.randint(100000, 999999)}" for _ in range(ROWS)],
    "product_name": [fake.word().capitalize() for _ in range(ROWS)],
    "category": [random.choice(CATEGORIES) for _ in range(ROWS)],
    "cost": costs,
    "price": [round(c * random.uniform(MIN_MARKUP, MAX_MARKUP), 2) for c in costs]
})

# Ensure SKUs are unique
seen_skus = set()
unique_skus = []
for sku in products['sku']:
    while sku in seen_skus:
        sku = f"SKU{random.randint(100000, 999999)}"
    seen_skus.add(sku)
    unique_skus.append(sku)
products['sku'] = unique_skus
# ---------------- CUSTOMERS ----------------
customers = pd.DataFrame({
    "customer_id": range(1, ROWS + 1),
    "name": [fake.name() for _ in range(ROWS)],
    "email": [fake.email() for _ in range(ROWS)],
    "city": [fake.city() for _ in range(ROWS)],
    "loyalty_tier": [random.choice(LOYALTY_TIERS) for _ in range(ROWS)]
})

# ---------------- STORES ----------------
stores = pd.DataFrame({
    "store_id": range(1, ROWS + 1),
    "store_name": [fake.company() for _ in range(ROWS)],
    "city": [fake.city() for _ in range(ROWS)],
    "store_type": [random.choice(STORE_TYPES) for _ in range(ROWS)]
})

# ---------------- SUPPLIERS ----------------
suppliers = pd.DataFrame({
    "supplier_id": range(1, ROWS + 1),
    "supplier_name": [fake.company() for _ in range(ROWS)],
    "country": [fake.country() for _ in range(ROWS)],
    "lead_time_days": [random.randint(3, 30) for _ in range(ROWS)]
})

# ---------------- INVENTORY ----------------
# Allow realistic inventory where multiple stores can stock the same product
inventory = pd.DataFrame({
    "inventory_id": range(1, ROWS + 1),
    "product_id": random.choices(products.product_id.tolist(), k=ROWS),
    "store_id": random.choices(stores.store_id.tolist(), k=ROWS),
    "stock_on_hand": [random.randint(0, 500) for _ in range(ROWS)],
    "reorder_level": [random.randint(20, 100) for _ in range(ROWS)]
})

# Ensure reorder level doesn't exceed realistic bounds
inventory['reorder_level'] = inventory.apply(
    lambda row: min(row['reorder_level'], row['stock_on_hand'] + 50) if row['stock_on_hand'] > 0 else row['reorder_level'],
    axis=1
)

# ---------------- TRANSACTIONS ----------------
transactions = pd.DataFrame({
    "transaction_id": range(1, ROWS + 1),
    "customer_id": random.choices(customers.customer_id.tolist(), k=ROWS),
    "product_id": random.choices(products.product_id.tolist(), k=ROWS),
    "store_id": random.choices(stores.store_id.tolist(), k=ROWS),
    "quantity": [random.randint(1, 5) for _ in range(ROWS)],
    "transaction_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(ROWS)]
})

# Calculate total_amount based on actual product price × quantity
transactions = transactions.merge(products[['product_id', 'price']], on='product_id')
transactions['total_amount'] = round(transactions['quantity'] * transactions['price'], 2)
transactions = transactions.drop('price', axis=1)

# ---------------- RETURNS ----------------
# Only create returns for actual transactions, and ensure refund doesn't exceed transaction amount
num_returns = int(ROWS * 0.3)  # Only 30% of transactions result in returns
return_transaction_ids = random.sample(transactions.transaction_id.tolist(), num_returns)

returns_list = []
for i, trans_id in enumerate(return_transaction_ids, 1):
    trans_amount = transactions[transactions.transaction_id == trans_id]['total_amount'].values[0]
    refund = round(random.uniform(min(5, trans_amount * 0.5), trans_amount), 2)
    
    returns_list.append({
        "return_id": i,
        "transaction_id": trans_id,
        "reason": random.choice(RETURN_REASONS),
        "refund_amount": refund
    })

returns = pd.DataFrame(returns_list)

# ---------------- PROMOTIONS ----------------
promotions = pd.DataFrame({
    "promotion_id": range(1, ROWS + 1),
    "promo_name": [fake.catch_phrase() for _ in range(ROWS)],
    "discount_pct": [random.choice(DISCOUNT_PERCENTAGES) for _ in range(ROWS)],
    "start_date": [fake.date_between("-6m", "today") for _ in range(ROWS)],
})

# Ensure end_date is after start_date
promotions['end_date'] = promotions['start_date'].apply(
    lambda x: x + timedelta(days=random.randint(7, 90))
)

# ---------------- SAVE ----------------
import os
os.makedirs("./data", exist_ok=True)

products.to_csv("./data/products.csv", index=False)
customers.to_csv("./data/customers.csv", index=False)
stores.to_csv("./data/stores.csv", index=False)
suppliers.to_csv("./data/suppliers.csv", index=False)
inventory.to_csv("./data/inventory.csv", index=False)
transactions.to_csv("./data/transactions.csv", index=False)
returns.to_csv("./data/returns.csv", index=False)
promotions.to_csv("./data/promotions.csv", index=False)

print("✓ Dataset generated successfully!")
print(f"  - {len(products)} products")
print(f"  - {len(customers)} customers")
print(f"  - {len(stores)} stores")
print(f"  - {len(suppliers)} suppliers")
print(f"  - {len(inventory)} inventory records")
print(f"  - {len(transactions)} transactions")
print(f"  - {len(returns)} returns")
print(f"  - {len(promotions)} promotions")