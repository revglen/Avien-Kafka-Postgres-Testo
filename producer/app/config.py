from dotenv import load_dotenv
import os

load_dotenv()
print(os.getcwd())

class Settings:
        
    TOPIC_NAME:str='transactions'
    #FRAUD_RATE:float=0.50

    SERVER="kafka-demo-testo1.d.aivencloud.com"
    PORT=16971
    BOOTSTRAP_SERVERS:str="kafka-demo-testo1.d.aivencloud.com:16971"

    SECURITY_PROTOCOLS:str="ssl"
    CA_LOCATION:str= os.getcwd() + "/app/ssl/ca.pem"
    SSL_CERTIFICATE_LOCATION:str= os.getcwd() + "/app/ssl/service.cert"
    SERVICE_KEY_LOCATION:str= os.getcwd() + "/app/ssl/service.key"

    KAFKA_CONFIG = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "security.protocol": SECURITY_PROTOCOLS,
        "ssl.ca.location": CA_LOCATION,
        "ssl.certificate.location":SSL_CERTIFICATE_LOCATION,
        'ssl.key.location': SERVICE_KEY_LOCATION,
        "ssl.endpoint.identification.algorithm": "none",
        "transactional.id": "fraud-management",
        "queue.buffering.max.messages": 100000,
        'retries': 5,
        'retry.backoff.ms': 1000,
        'transaction.timeout.ms': 60000,
        'request.timeout.ms': 30000,
        "default.topic.config": {"acks": "all"}
    }

    NUMBER_OF_MESSAGES=5

settings = Settings()

   