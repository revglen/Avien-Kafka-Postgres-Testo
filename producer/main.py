from app.config import settings
from app.transactionProducer import TransactionProducer

if __name__ == "__main__":
    print(f"Generating transactions...")
    TransactionProducer().run()