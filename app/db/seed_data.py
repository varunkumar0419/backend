from app.services.generator import (
    generate_customers,
    generate_orders,
    generate_refunds
)

generate_customers()
generate_orders()
generate_refunds()

print("Seed Data Generated")