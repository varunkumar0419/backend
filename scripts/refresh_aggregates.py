from app.db.database import SessionLocal
from app.services.aggregation import build_aggregates

db = SessionLocal()

try:
    result = build_aggregates(db)

    print("\nAggregation Refreshed")
    print("---------")
    print(result)

finally:
    db.close()