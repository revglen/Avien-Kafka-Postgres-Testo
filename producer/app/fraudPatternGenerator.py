import datetime
import random
import time
from dotenv import load_dotenv
import hashlib
from faker import Faker

from app.config import settings
from app.fraud_rules import rules

import logging

load_dotenv()

class FraudPatternGenerator:
    def __init__(self):
        self.faker = Faker()
        self.user_profiles = {}
        self.device_profiles = {}

    
    def _generate_user_profile(self, user_id):
       
        if user_id not in self.user_profiles:
            seed = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
            random.seed(seed)
            
            self.user_profiles[user_id] = {
                'home_country': random.choice(['US', 'GB', 'DE', 'FR', 'IR', 'SG']),
                'avg_amount': random.uniform(50, 200),
                'txn_frequency': random.uniform(0.5, 3)  # txns/hour
            }

        return self.user_profiles[user_id]
    
    #Simulate the fraud detection
    def _is_fraud_transaction(self, transaction):
        
        # Rule 1: High value
        if transaction['amount'] > rules.fraud_rules['high_value']['threshold']:
            return True, 'high_value'
        
        # Rule 2: Geo mismatch
        user_profile = self._generate_user_profile(transaction['user_id'])
        if (transaction['country'] != user_profile['home_country'] and 
            transaction['country'] in rules.fraud_rules['geo_mismatch']['high_risk_countries']):
            return True, 'geo_mismatch'
        
        # Rule 3: Velocity
        txn_count = sum(1 for t in self.user_profiles[transaction['user_id']].get('recent_txns', []) 
                     if t > datetime.now() - datetime.timedelta(hours=rules.fraud_rules['velocity']['time_window_hours']))
        if txn_count > rules.fraud_rules['velocity']['txn_count_threshold']:
            return True, 'velocity'
        
        return False, None

    def generate_transaction(self):
        user_id = f"user_{random.randint(1000, 9999)}"
        profile = self._generate_user_profile(user_id)
        
        transaction = {
            'transaction_id': f"txn_{int(time.time() * 1000)}",
            'user_id': user_id,
            #'amount': max(1, round(random.gauss(profile['avg_amount'], profile['avg_amount']/3), 2)),
            'amount': random.randint(1, 10000),
            'currency': 'EUR',
            'merchant': self.faker.company(),
            'timestamp': datetime.datetime.now().isoformat(),
            'ip': self.faker.ipv4(),
            'user_agent': self.faker.user_agent(),
            'country': profile['home_country'] if random.random() > 0.1 else random.choice(rules.fraud_rules['geo_mismatch']['high_risk_countries']),
            'device_id': f"device_{hashlib.md5(user_id.encode()).hexdigest()[:6]}"
        }
        
        # Embed fraud markers
        is_fraud, fraud_type = self._is_fraud_transaction(transaction)
        if is_fraud:
            transaction.update({
                'is_fraud': True,
                'fraud_type': fraud_type,
                'fraud_rule_triggered': rules.fraud_rules[fraud_type]
            })
        
        return transaction