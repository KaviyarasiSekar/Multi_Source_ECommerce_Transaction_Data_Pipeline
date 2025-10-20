from faker import Faker
import random
from datetime import datetime, timedelta
import json

fake = Faker()

def generate_transactions(num_records):
    """
    Generate realistic transaction data
    """

    transactions = []
    for i in range(num_records):
        transaction = {
            'transaction_id': f'TXN_{i:08d}',
            'user_id': random.randint(1000, 9999),
            'product_id': random.randint(100, 999),
            'amount': round(random.uniform(10.0, 500.0), 2),
            'quantity': random.randint(1, 5),
            'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'crypto']),
            'status': random.choice(['completed', 'pending', 'failed']),
            'transaction_date': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            'country': fake.country_code(),
            'city': fake.city(),
        }
        transactions.append(transaction)

    # Save Results to local Json File
    with open(
        'simulated_transactions.json', "w", encoding='utf-8') as f:
        json.dump(transactions, f, ensure_ascii=False, indent=4)

    print(f"completed items to simulated_transactions.json ")

    return transactions

if __name__ == "__main__":
    generate_transactions(1000)