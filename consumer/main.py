from app.config import settings
from app.fraudConsumer import FraudConsumer
from app.config import settings

if __name__ == "__main__":
    print(f"Generating transactions with {settings.FRAUD_RATE*100}% fraud rate...")
    FraudConsumer().run()