from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

class Settings:
        
    TOPIC_NAME:str="transactions"
   
    KAFKA_SERVER="kafka-demo-testo1.d.aivencloud.com"
    KAFKA_PORT=16971
    BOOTSTRAP_SERVERs:str="kafka-demo-testo1.d.aivencloud.com:16971"

    SECURITY_PROTOCOLS:str="ssl"
    CA_LOCATION:str= os.getcwd() + "/app/ssl/ca.pem"
    SSL_CERTIFICATE_LOCATION:str= os.getcwd() + "/app/ssl/service.cert"
    SERVICE_KEY_LOCATION:str= os.getcwd() + "/app/ssl/service.key"

    KAFKA_CONFIG = {
        "bootstrap.servers": BOOTSTRAP_SERVERs,
        "security.protocol": SECURITY_PROTOCOLS,
        "ssl.ca.location": CA_LOCATION,
        "ssl.certificate.location":SSL_CERTIFICATE_LOCATION,
        "ssl.key.location": SERVICE_KEY_LOCATION,
        "group.id": "fraud-detection-group",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "isolation.level": "read_committed"
    }

    DB_NAME:str="defaultdb"
    DB_USER:str="avnadmin"
    DB_PASSWORD:str="" # Update this password 
    DB_HOST:str="fraud-db-service-testo1.i.aivencloud.com"
    DB_PORT:int=16969
    SSL_MODE:str="require"

    FRAUD_RATE:float=0.05

settings = Settings()

   