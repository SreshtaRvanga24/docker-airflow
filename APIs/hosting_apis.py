from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Retail Data API",
    description="API for accessing retail database tables",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "your_database"),
    "user": os.getenv("DB_USER", "your_user"),
    "password": os.getenv("DB_PASSWORD", "your_password")
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """Execute a query and return results as list of dictionaries"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return [dict(row) for row in cur.fetchall()]

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Retail Data API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/products",
            "customers": "/customers",
            "stores": "/stores",
            "suppliers": "/suppliers",
            "inventory": "/inventory",
            "transactions": "/transactions",
            "returns": "/returns",
            "promotions": "/promotions"
        }
    }

# Products endpoints
@app.get("/products")
def get_products(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None
):
    """Get all products with optional filtering"""
    query = "SELECT * FROM public.products WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    query += " ORDER BY product_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    results = execute_query(query, tuple(params))
    return {"count": len(results), "data": results}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Get a specific product by ID"""
    query = "SELECT * FROM public.products WHERE product_id = %s"
    results = execute_query(query, (product_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return results[0]

# Customers endpoints
@app.get("/customers")
def get_customers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all customers"""
    query = "SELECT * FROM public.customers ORDER BY customer_id LIMIT %s OFFSET %s"
    results = execute_query(query, (limit, offset))
    return {"count": len(results), "data": results}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    query = "SELECT * FROM public.customers WHERE customer_id = %s"
    results = execute_query(query, (customer_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return results[0]

# Stores endpoints
@app.get("/stores")
def get_stores(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all stores"""
    query = "SELECT * FROM public.stores ORDER BY store_id LIMIT %s OFFSET %s"
    results = execute_query(query, (limit, offset))
    return {"count": len(results), "data": results}

@app.get("/stores/{store_id}")
def get_store(store_id: int):
    """Get a specific store by ID"""
    query = "SELECT * FROM public.stores WHERE store_id = %s"
    results = execute_query(query, (store_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Store not found")
    
    return results[0]

# Suppliers endpoints
@app.get("/suppliers")
def get_suppliers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all suppliers"""
    query = "SELECT * FROM public.suppliers ORDER BY supplier_id LIMIT %s OFFSET %s"
    results = execute_query(query, (limit, offset))
    return {"count": len(results), "data": results}

@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int):
    """Get a specific supplier by ID"""
    query = "SELECT * FROM public.suppliers WHERE supplier_id = %s"
    results = execute_query(query, (supplier_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return results[0]

# Inventory endpoints
@app.get("/inventory")
def get_inventory(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    store_id: Optional[int] = None,
    product_id: Optional[int] = None
):
    """Get inventory with optional filtering"""
    query = "SELECT * FROM public.inventory WHERE 1=1"
    params = []
    
    if store_id:
        query += " AND store_id = %s"
        params.append(store_id)
    
    if product_id:
        query += " AND product_id = %s"
        params.append(product_id)
    
    query += " ORDER BY inventory_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    results = execute_query(query, tuple(params))
    return {"count": len(results), "data": results}

# Transactions endpoints
@app.get("/transactions")
def get_transactions(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    customer_id: Optional[int] = None,
    store_id: Optional[int] = None
):
    """Get transactions with optional filtering"""
    query = "SELECT * FROM public.transactions WHERE 1=1"
    params = []
    
    if customer_id:
        query += " AND customer_id = %s"
        params.append(customer_id)
    
    if store_id:
        query += " AND store_id = %s"
        params.append(store_id)
    
    query += " ORDER BY transaction_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    results = execute_query(query, tuple(params))
    return {"count": len(results), "data": results}

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    """Get a specific transaction by ID"""
    query = "SELECT * FROM public.transactions WHERE transaction_id = %s"
    results = execute_query(query, (transaction_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return results[0]

# Returns endpoints
@app.get("/returns")
def get_returns(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all returns"""
    query = "SELECT * FROM public.returns ORDER BY return_id LIMIT %s OFFSET %s"
    results = execute_query(query, (limit, offset))
    return {"count": len(results), "data": results}

# Promotions endpoints
@app.get("/promotions")
def get_promotions(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all promotions"""
    query = "SELECT * FROM public.promotions ORDER BY promotion_id LIMIT %s OFFSET %s"
    results = execute_query(query, (limit, offset))
    return {"count": len(results), "data": results}

# Analytics endpoints
@app.get("/analytics/sales-by-store")
def get_sales_by_store():
    """Get total sales grouped by store"""
    query = """
        SELECT 
            s.store_id,
            s.store_name,
            COUNT(t.transaction_id) as transaction_count,
            SUM(t.total_amount) as total_sales
        FROM public.stores s
        LEFT JOIN public.transactions t ON s.store_id = t.store_id
        GROUP BY s.store_id, s.store_name
        ORDER BY total_sales DESC
    """
    results = execute_query(query)
    return {"data": results}

@app.get("/analytics/top-products")
def get_top_products(limit: int = Query(10, ge=1, le=100)):
    """Get top selling products"""
    query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            COUNT(t.transaction_id) as sales_count,
            SUM(t.total_amount) as total_revenue
        FROM public.products p
        LEFT JOIN public.transactions t ON p.product_id = t.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY sales_count DESC
        LIMIT %s
    """
    results = execute_query(query, (limit,))
    return {"data": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)