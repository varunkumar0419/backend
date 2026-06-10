from app.services.generator import (
    generate_customers,
    generate_orders,
    generate_refunds
)

def main():

    print("Generating Customers...")
    generate_customers("data/customers.csv", 100000)

    print("Generating Orders...")
    generate_orders("data/orders.csv", 1000000)

    print("Generating Refunds...")
    generate_refunds("data/refunds.csv", 200000)

    print("Data generation completed 🚀")


if __name__ == "__main__":
    main()