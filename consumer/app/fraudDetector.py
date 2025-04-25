from datetime import datetime, timedelta
import random
import hashlib
from app.fraud_rules import rules

class FraudDetector:
    def detect_fraud(self, transaction):
        
        # Rule 1: High value
        if transaction['amount'] > rules.fraud_rules['high_value']['threshold']:
            return True, 'high_value'
        
        # Rule 2: Geo mismatch
        user_country = self._get_user_home_country(transaction['user_id'])
        if (transaction['country'] != user_country and 
            transaction['country'] in rules.fraud_rules['geo_mismatch']['high_risk_countries']):
            if random.random() < rules.fraud_rules['geo_mismatch']['threshold']:
                return True, 'geo_mismatch'
        
        # Rule 3: Velocity
        if self._check_velocity(transaction):
            return True, 'velocity'
        
        return False, None

    def _get_user_home_country(self, user_id):
        seed = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        return random.choice(['US', 'GB', 'DE', 'FR'])

    def _check_velocity(self, transaction):
        if transaction['user_id'] not in rules.user_states:
            rules.user_states[transaction['user_id']] = {
                'txn_history': [],
                'last_country': None
            }
        
        now = datetime.now()
        rules.user_states[transaction['user_id']]['txn_history'] = [
            t for t in rules.user_states[transaction['user_id']]['txn_history']
            if t > now - timedelta(hours=rules.fraud_rules['velocity']['time_window_hours'])
        ]
        
        if len(rules.user_states[transaction['user_id']]['txn_history']) >= rules.fraud_rules['velocity']['txn_count_threshold']:
            return True
        
        rules.user_states[transaction['user_id']]['txn_history'].append(now)
        return False