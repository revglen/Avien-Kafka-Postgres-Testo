class Fraud_Rules:
    def __init__(self):
        self.fraud_rules = {
            'high_value': {
                'threshold': 1000.00,
                'probability': 0.3
            },
            'geo_mismatch': {
                'threshold': 0.7,
                'high_risk_countries': ['CN', 'NG', 'CU', 'VE', 'IR', 'SY', 'NK']
            },
            'velocity': {
                'txn_count_threshold': 5,
                'time_window_hours': 1
            }
        }

        self.user_states = {}

rules = Fraud_Rules()