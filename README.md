# Avien-Kafka-Postgres-Testo

This is a sample which tests Avien Kafka and Postgres Managed Cloud solutions.
Kafka and Postgres were created with the help of the Avian Commands.
This example is a classic example of an e-commerce payment fraud detection system.
Transactions are generated at the Producer app, which is then fed into the Kafka topic. The Consumer app tests for anomalies. 
The original transaction is saved to the Postgres transactions table, and if fraud is detected, then a fraud table is updated with the latest details.
Note: In the consumer app, the database password needs to be updated. 

**Commands to create Kafka Service in Aiven**
- pip3 install aiven-client`
- avn service create --service-type kafka --cloud aws-eu-west-1 kafka-demo`
- avn service update -c kafka_rest=true -c schema_registry=true -c backup_hour=02 -c backup_minute=30 kafka-demo`
- avn service topic-create kafka-demo transactions --partitions 3 --replication 2`
- avn service topic-get kafka-demo transactions`

**Commands to create Aiven Postgres Service in Aiven**
- sudo apt install postgresql-client`
- avn service create fraud-db-service --service-type pg --plan startup-4 --cloud aws-eu-west-1`


