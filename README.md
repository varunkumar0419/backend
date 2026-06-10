#Setup Instructions

# 1. Clone the repository
git clone <your-repo-url>
cd backend-assignment

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)

### 3. Install dependencies
pip install -r requirements.txt

## 4. Run database migrations / setup DB
Ensure PostgreSQL is running and update DATABASE_URL in .env

### 5. Start backend server
python -m uvicorn app.main:app --reload --port 8000

### 6. Open API docs
http://127.0.0.1:8000/docs

# 7. Run load test
cd load_test
python -m locust -f locustfile.py

## API Endpoints

### 1. GET /analytics/summary
Returns overall revenue metrics.

### 2. GET /analytics/top-customers
Returns top 10 customers by spend.

### 3. GET /analytics/revenue-trends
Returns monthly revenue aggregation.

### 4. GET /analytics/repeat-customer-revenue
Returns revenue from customers with more than one order.

### 5. GET /customers
Paginated customer listing.

## Architecture Overview

- FastAPI backend built with SQLAlchemy ORM
- PostgreSQL used as primary database
- Modular design using routers, services, and DB layers
- Locust used for performance testing

---

## Optimization Techniques Used

### 1. Indexing
Added indexes on:
- orders.customer_id
- orders.order_date
- orders.amount

### 2. Caching (Critical Improvement)
Implemented in-memory cache layer for analytics endpoints:
- Reduces repeated database queries
- TTL-based expiration (up to 1–3 hours)

### 3. Query Optimization
- Used aggregation functions (SUM, COUNT)
- Reduced redundant queries
- Optimized GROUP BY operations

### 4. Reduced DB Load
- Heavy analytics endpoints cached
- Repeat queries avoided during load testing
## Result

- No failed requests under load
- Significant reduction in P95 latency
- Stable performance under concurrent users

- Host

http://localhost:8000

Status

running
Users

20
RPS

11.33
Failures

0%

<2 and 0 percentage of failure 




