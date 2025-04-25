import psycopg2
from app.config import settings

class PostgresSink:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            sslmode="require"
        )
        self._init_db()
        self._create_view()

    def _init_db(self):
        with self.conn.cursor() as cur:
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    amount DECIMAL(10,2),
                    currency TEXT,
                    merchant TEXT,
                    ip TEXT,
	                user_aqent TEXT,
                    timestamp TIMESTAMPTZ,
                    is_fraud BOOLEAN,
                    fraud_type TEXT,
                    processed_at TIMESTAMPTZ DEFAULT NOW()
                );
                        
                CREATE TABLE if not exists fraud_alerts (
                    alert_id SERIAL PRIMARY KEY,
                    transaction_id VARCHAR REFERENCES transactions(transaction_id),
                    reason VARCHAR,
                    detected_at TIMESTAMP DEFAULT NOW()
                );
            """)
            self.conn.commit()

    def _create_view(self):

        with self.conn.cursor() as cur:       
            create_view_sql:str = """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_views 
                        WHERE viewname = 'high_risk_transactions'
                            AND schemaname = 'public'
                    ) THEN
                        EXECUTE '
                            CREATE VIEW high_risk_transactions AS
                            SELECT t.*, f.reason 
                            FROM transactions t
                            JOIN fraud_alerts f ON t.transaction_id = f.transaction_id
                        ';
                    END IF;
                END
                $$;
            """

            try:
                cur.execute(create_view_sql)
                self.conn.commit()
                print("View created or already exists.")
            except Exception as e:
                self.conn.rollback()
                print("Error creating view:", e)

    def save_transaction(self, transaction):
        user_agent:str = ""
        try:
            if transaction['user_agent'] is not None:
                user_agent = transaction['user_agent']
        except:
            pass

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transactions (
                    transaction_id, user_id, amount, currency,
                    merchant,ip, user_aqent, timestamp, is_fraud, fraud_type
                ) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                transaction['transaction_id'],
                transaction['user_id'],
                transaction['amount'],
                transaction['currency'],
                transaction['merchant'],
                transaction['ip'],
                user_agent,
                transaction['timestamp'],
                transaction.get('is_fraud', False),
                transaction.get('fraud_type')
            ))

            if transaction.get('is_fraud') is not None and  transaction['is_fraud'] == True:
                cur.execute("""
                    INSERT INTO fraud_alerts (
                        transaction_id, reason
                    ) VALUES (%s, %s)
                """, (
                    transaction["transaction_id"],
                    transaction.get('fraud_type')
                ))

            self.conn.commit()