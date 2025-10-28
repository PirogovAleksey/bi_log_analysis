#!/usr/bin/env python3
"""
Banking System Log Generator
Generates realistic banking system logs for ELK Stack analysis
"""

import json
import random
import datetime
import ipaddress
from typing import Dict, List
import time

# Sample data
TRANSACTION_TYPES = ['transaction', 'authentication', 'atm', 'transfer', 'balance_inquiry']
TRANSACTION_STATUSES = ['success', 'failed', 'pending', 'cancelled']
CURRENCIES = ['USD', 'EUR', 'GBP', 'UAH', 'PLN']
COUNTRIES = ['US', 'UK', 'UA', 'PL', 'DE', 'FR', 'IT', 'ES']
CARD_TYPES = ['VISA', 'MASTERCARD', 'MAESTRO', 'AMERICAN_EXPRESS']
ATM_LOCATIONS = [
    'Kyiv Central', 'Lviv Downtown', 'Kharkiv Plaza', 'Odesa Beach',
    'Dnipro Station', 'Warsaw Center', 'Krakow Mall', 'London City'
]
SERVICES = ['mobile_banking', 'web_banking', 'atm', 'pos_terminal', 'api']
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
    'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
    'BankingApp/3.2.1 (iOS 14.0)',
    'BankingApp/3.2.1 (Android 10)'
]

# User pool for realistic patterns
USERS = [f'user_{i:04d}' for i in range(1, 501)]

# Fraud patterns
FRAUD_IPS = ['185.220.101.{}'.format(i) for i in range(1, 20)]
FRAUD_USERS = random.sample(USERS, 10)


def random_ip() -> str:
    """Generate random IP address"""
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))


def random_timestamp(days_back: int = 7) -> str:
    """Generate random timestamp within last N days"""
    now = datetime.datetime.now()
    random_days = random.uniform(0, days_back)
    random_time = now - datetime.timedelta(days=random_days)
    return random_time.strftime('%Y-%m-%d %H:%M:%S')


def generate_transaction_log() -> Dict:
    """Generate a transaction log entry"""
    amount = round(random.lognormvariate(5, 2), 2)
    user = random.choice(USERS)
    status = random.choices(
        TRANSACTION_STATUSES,
        weights=[85, 10, 3, 2],
        k=1
    )[0]

    # Simulate fraud patterns
    is_fraud = random.random() < 0.05
    if is_fraud:
        amount = random.uniform(5000, 50000)
        user = random.choice(FRAUD_USERS)
        ip = random.choice(FRAUD_IPS)
    else:
        ip = random_ip()

    return {
        'timestamp': random_timestamp(),
        'transaction_type': 'transaction',
        'transaction_id': f'TXN{random.randint(1000000, 9999999)}',
        'user_id': user,
        'account_number': f'{random.randint(1000000000, 9999999999)}',
        'amount': amount,
        'currency': random.choice(CURRENCIES),
        'status': status,
        'merchant': f'Merchant_{random.randint(1, 100)}',
        'merchant_category': random.choice(['retail', 'food', 'travel', 'entertainment', 'utilities']),
        'card_type': random.choice(CARD_TYPES),
        'card_last4': f'{random.randint(1000, 9999)}',
        'client_ip': ip,
        'country': random.choice(COUNTRIES),
        'service': random.choice(SERVICES),
        'response_time_ms': random.randint(50, 2000),
        'is_fraud': is_fraud
    }


def generate_authentication_log() -> Dict:
    """Generate an authentication log entry"""
    user = random.choice(USERS)
    status = random.choices(['success', 'failed'], weights=[90, 10], k=1)[0]

    # Simulate brute force attacks
    is_brute_force = random.random() < 0.03
    if is_brute_force:
        status = 'failed'
        ip = random.choice(FRAUD_IPS)
    else:
        ip = random_ip()

    auth_method = random.choice(['password', '2fa', 'biometric', 'sms_otp', 'email_otp'])

    return {
        'timestamp': random_timestamp(),
        'transaction_type': 'authentication',
        'event_id': f'AUTH{random.randint(1000000, 9999999)}',
        'user_id': user,
        'status': status,
        'auth_method': auth_method,
        'client_ip': ip,
        'country': random.choice(COUNTRIES),
        'service': random.choice(['mobile_banking', 'web_banking', 'api']),
        'user_agent': random.choice(USER_AGENTS),
        'session_id': f'SES{random.randint(1000000, 9999999)}',
        'response_time_ms': random.randint(100, 500),
        'is_brute_force': is_brute_force
    }


def generate_atm_log() -> Dict:
    """Generate an ATM transaction log"""
    operation = random.choice(['withdrawal', 'deposit', 'balance_check', 'pin_change'])
    status = random.choices(TRANSACTION_STATUSES, weights=[85, 10, 3, 2], k=1)[0]

    amount = None
    if operation in ['withdrawal', 'deposit']:
        amount = random.choice([20, 50, 100, 200, 500, 1000])

    return {
        'timestamp': random_timestamp(),
        'transaction_type': 'atm',
        'transaction_id': f'ATM{random.randint(1000000, 9999999)}',
        'user_id': random.choice(USERS),
        'account_number': f'{random.randint(1000000000, 9999999999)}',
        'operation': operation,
        'amount': amount,
        'currency': random.choice(CURRENCIES) if amount else None,
        'status': status,
        'atm_id': f'ATM{random.randint(1000, 5000)}',
        'atm_location': random.choice(ATM_LOCATIONS),
        'card_type': random.choice(CARD_TYPES),
        'card_last4': f'{random.randint(1000, 9999)}',
        'country': random.choice(COUNTRIES),
        'response_time_ms': random.randint(1000, 5000)
    }


def generate_transfer_log() -> Dict:
    """Generate a transfer log entry"""
    amount = round(random.lognormvariate(6, 1.5), 2)
    status = random.choices(TRANSACTION_STATUSES, weights=[80, 12, 5, 3], k=1)[0]

    transfer_type = random.choice(['internal', 'external', 'international'])

    return {
        'timestamp': random_timestamp(),
        'transaction_type': 'transfer',
        'transaction_id': f'TRF{random.randint(1000000, 9999999)}',
        'user_id': random.choice(USERS),
        'from_account': f'{random.randint(1000000000, 9999999999)}',
        'to_account': f'{random.randint(1000000000, 9999999999)}',
        'amount': amount,
        'currency': random.choice(CURRENCIES),
        'status': status,
        'transfer_type': transfer_type,
        'client_ip': random_ip(),
        'country': random.choice(COUNTRIES),
        'service': random.choice(['mobile_banking', 'web_banking']),
        'response_time_ms': random.randint(200, 3000)
    }


def generate_balance_inquiry_log() -> Dict:
    """Generate a balance inquiry log"""
    return {
        'timestamp': random_timestamp(),
        'transaction_type': 'balance_inquiry',
        'event_id': f'BAL{random.randint(1000000, 9999999)}',
        'user_id': random.choice(USERS),
        'account_number': f'{random.randint(1000000000, 9999999999)}',
        'status': random.choices(['success', 'failed'], weights=[95, 5], k=1)[0],
        'client_ip': random_ip(),
        'country': random.choice(COUNTRIES),
        'service': random.choice(SERVICES),
        'response_time_ms': random.randint(50, 300)
    }


def generate_logs(num_logs: int = 10000, output_file: str = 'logs/banking_transactions.log'):
    """Generate banking logs"""
    generators = [
        (generate_transaction_log, 40),
        (generate_authentication_log, 25),
        (generate_atm_log, 20),
        (generate_transfer_log, 10),
        (generate_balance_inquiry_log, 5)
    ]

    # Normalize weights
    total_weight = sum(weight for _, weight in generators)
    weights = [weight / total_weight for _, weight in generators]

    print(f"Generating {num_logs} banking log entries...")

    with open(output_file, 'w') as f:
        for i in range(num_logs):
            # Select generator based on weights
            generator_func = random.choices(
                [gen for gen, _ in generators],
                weights=weights,
                k=1
            )[0]

            log_entry = generator_func()
            f.write(json.dumps(log_entry) + '\n')

            if (i + 1) % 1000 == 0:
                print(f"Generated {i + 1} logs...")

    print(f"Successfully generated {num_logs} logs to {output_file}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate banking system logs')
    parser.add_argument('-n', '--num-logs', type=int, default=10000,
                        help='Number of log entries to generate (default: 10000)')
    parser.add_argument('-o', '--output', type=str, default='logs/banking_transactions.log',
                        help='Output file path (default: logs/banking_transactions.log)')

    args = parser.parse_args()

    generate_logs(args.num_logs, args.output)
