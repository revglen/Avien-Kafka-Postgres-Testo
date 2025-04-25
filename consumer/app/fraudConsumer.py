import json
from confluent_kafka import Consumer, KafkaException
from app.fraudDetector import FraudDetector
from app.postgresSink import PostgresSink
from app.config import settings

class FraudConsumer:
    def __init__(self):
        self.consumer = Consumer(settings.KAFKA_CONFIG)
        self.detector = FraudDetector()
        self.db_sink = PostgresSink()

    def process_message(self, msg):
        try:
            transaction = json.loads(msg.value())
            
            # Re-detect fraud
            is_fraud, fraud_type = self.detector.detect_fraud(transaction)
            transaction['is_fraud'] = is_fraud
            transaction['fraud_type'] = fraud_type if is_fraud else None
            
            self.db_sink.save_transaction(transaction)
            
            if is_fraud:
                print(f"🚨 Detected fraud: {transaction['transaction_id']} ({fraud_type})")
            else:
                print(f"✅ Processed: {transaction['transaction_id']}")

        except json.JSONDecodeError as e:
            print(f"Invalid message: {e}")
        except Exception as e:
            print(f"Processing error: {e}")

    def run(self):
        self.consumer.subscribe([settings.TOPIC_NAME])
        print("Listening for transactions to analyse for fraud...")
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                self.process_message(msg)
                self.consumer.commit(asynchronous=False)
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.consumer.close()
            self.db_sink.conn.close()