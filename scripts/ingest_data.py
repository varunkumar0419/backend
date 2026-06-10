
from app.services.ingestion import (
    ingest_customers,
    ingest_orders,
    ingest_refunds
)

print("Loading Customers...")
ingest_customers()

print("Loading Orders...")
ingest_orders()

print("Loading Refunds...")
ingest_refunds()

print("Database ingestion completed.")