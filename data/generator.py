"""
Synthetic data generator for customers and orders using Faker.
Creates deterministic, realistic business data for BI analysis.
"""
import random
from datetime import date, timedelta
from typing import List, Tuple
import pandas as pd
from faker import Faker

import config
from data.schema import Customer, Order


def generate_synthetic_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate synthetic customer and order data.
    
    Returns:
        Tuple of (customers_df, orders_df)
    """
    # Set random seed for reproducibility
    random.seed(config.RANDOM_SEED)
    fake = Faker()
    Faker.seed(config.RANDOM_SEED)
    
    customers = []
    orders = []
    order_counter = 1
    
    # Calculate segment counts
    segment_counts = {
        segment: int(config.NUM_CUSTOMERS * dist)
        for segment, dist in config.SEGMENT_DISTRIBUTION.items()
    }
    # Adjust for rounding
    diff = config.NUM_CUSTOMERS - sum(segment_counts.values())
    if diff > 0:
        segment_counts["returning"] += diff
    
    # Generate customers by segment
    customer_id = 1
    for segment, count in segment_counts.items():
        for _ in range(count):
            cust_id = f"CUST{customer_id:04d}"
            
            # Generate customer data
            created_days_ago = random.randint(90, 365)
            created_at = date.today() - timedelta(days=created_days_ago)
            last_contact_days_ago = random.randint(0, 30)
            last_contact = date.today() - timedelta(days=last_contact_days_ago)
            
            # Random interests (2-4 from pool)
            num_interests = random.randint(2, 4)
            interests = random.sample(config.INTEREST_POOL, num_interests)
            
            customer = Customer(
                customer_id=cust_id,
                name=fake.name(),
                email=fake.email(),
                segment=segment,
                interests=interests,
                last_contact_date=last_contact,
                created_at=created_at
            )
            customers.append(customer.model_dump())
            
            # Generate orders for this customer
            num_orders = random.randint(
                config.ORDERS_PER_CUSTOMER_MIN,
                config.ORDERS_PER_CUSTOMER_MAX
            )
            
            for _ in range(num_orders):
                order_id = f"ORD{order_counter:08d}"
                order_counter += 1
                
                # Order date within last DATA_DAYS_BACK days
                days_ago = random.randint(0, config.DATA_DAYS_BACK)
                order_date = date.today() - timedelta(days=days_ago)
                
                # Amount varies by segment
                if segment == "vip":
                    amount = random.uniform(5000, 20000)
                elif segment == "returning":
                    amount = random.uniform(2000, 8000)
                elif segment == "new":
                    amount = random.uniform(500, 3000)
                else:  # at_risk
                    amount = random.uniform(300, 2000)
                
                # Category based on interests
                if interests:
                    category = random.choice(interests)
                else:
                    category = random.choice(config.PRODUCT_CATEGORIES)
                
                channel = random.choice(config.ORDER_CHANNELS)
                
                order = Order(
                    order_id=order_id,
                    customer_id=cust_id,
                    order_date=order_date,
                    amount=round(amount, 2),
                    product_category=category,
                    channel=channel
                )
                orders.append(order.model_dump())
            
            customer_id += 1
    
    # Convert to DataFrames
    customers_df = pd.DataFrame(customers)
    orders_df = pd.DataFrame(orders)
    
    return customers_df, orders_df


def save_data(customers_df: pd.DataFrame, orders_df: pd.DataFrame) -> None:
    """
    Save dataframes to CSV files.
    
    Args:
        customers_df: Customer dataframe
        orders_df: Orders dataframe
    """
    customers_path = config.DATA_DIR / "customers.csv"
    orders_path = config.DATA_DIR / "orders.csv"
    
    customers_df.to_csv(customers_path, index=False)
    orders_df.to_csv(orders_path, index=False)
    
    print(f"✓ Saved {len(customers_df)} customers to {customers_path}")
    print(f"✓ Saved {len(orders_df)} orders to {orders_path}")


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load customer and order data from CSV files.
    
    Returns:
        Tuple of (customers_df, orders_df)
    """
    customers_path = config.DATA_DIR / "customers.csv"
    orders_path = config.DATA_DIR / "orders.csv"
    
    if not customers_path.exists() or not orders_path.exists():
        raise FileNotFoundError(
            "Data files not found. Please generate data first."
        )
    
    customers_df = pd.read_csv(customers_path)
    orders_df = pd.read_csv(orders_path)
    
    # Convert date strings to date objects
    customers_df['last_contact_date'] = pd.to_datetime(
        customers_df['last_contact_date']
    ).dt.date
    customers_df['created_at'] = pd.to_datetime(
        customers_df['created_at']
    ).dt.date
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date']).dt.date
    
    # Parse interests from string representation
    import ast
    customers_df['interests'] = customers_df['interests'].apply(ast.literal_eval)
    
    return customers_df, orders_df


def ensure_data_exists() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ensure data exists, generate if needed, then return it.
    
    Returns:
        Tuple of (customers_df, orders_df)
    """
    try:
        return load_data()
    except FileNotFoundError:
        print("Generating synthetic data...")
        customers_df, orders_df = generate_synthetic_data()
        save_data(customers_df, orders_df)
        return customers_df, orders_df


if __name__ == "__main__":
    # Generate and save data
    customers_df, orders_df = generate_synthetic_data()
    save_data(customers_df, orders_df)
    
    print("\nSample Customers:")
    print(customers_df.head())
    print("\nSample Orders:")
    print(orders_df.head())
