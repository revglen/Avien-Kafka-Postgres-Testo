import json
from math import erf
import random
import time
from dotenv import load_dotenv
from confluent_kafka import Producer
from app.custom_logging import logger

from app.config import settings
from app.fraudPatternGenerator import FraudPatternGenerator

load_dotenv()

class TransactionProducer:    

    def __init__(self):
        self.producer = Producer(settings.KAFKA_CONFIG)
        self.producer.init_transactions()
        self.fraud_producer = FraudPatternGenerator()
        
    def delivery_report(self, err, msg):
        if err:
            print(f"Delivery failed: {err}")
        else:
            txn = json.loads(msg.value())
            status = "🚨 FRAUD" if txn.get('is_fraud') else "✅ LEGIT"
            print(f"{status} {txn['transaction_id']}: ${txn['amount']} {txn['merchant']}")

    def run(self):        
        try:        
            self.producer.begin_transaction()
            #for i in range(random.randint(1, settings.NUMBER_OF_MESSAGES)):  
            for i in range(1, settings.NUMBER_OF_MESSAGES):  
                txn = self.fraud_producer.generate_transaction()
                self.producer.produce(
                    settings.TOPIC_NAME,
                    value=json.dumps(txn),
                    callback=self.delivery_report
                )
                print("Proceed Message: " + str(i))
                
            self.producer.commit_transaction()                
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            logger.error(f"Failed to configure producer: {str(e)}")
        finally:
            self.producer.flush()
   