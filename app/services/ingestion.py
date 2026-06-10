import pandas as pd
import logging
from app.db.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def bulk_load(csv_path: str, table_name: str):
    """
    Generic bulk loader for any CSV → PostgreSQL table
    """

    try:
        logger.info(f"Loading {table_name} from {csv_path}")

        df = pd.read_csv(csv_path)

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi"
        )

        logger.info(f"{table_name} loaded successfully ({len(df)} rows)")

    except Exception as e:
        logger.error(f"Failed to load {table_name}: {str(e)}")
        raise



# Specific  ingestion Functions


def ingest_customers():
    bulk_load("data/customers.csv", "customers")


def ingest_orders():
    bulk_load("data/orders.csv", "orders")


def ingest_refunds():
    bulk_load("data/refunds.csv", "refunds")