# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

# Datos de conexión
password = "hEqETD0V851JnBcB"
user = "postgres.qbpporkcnzredtedqwyx"
host = "aws-0-us-west-2.pooler.supabase.com"
port = 6543
database = "postgres"

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

# Engine usando NullPool para Transaction Pooler
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Test de conexión
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW();"))
            print("Conexión OK, hora del servidor:", result.fetchone()[0])
    except Exception as e:
        print("Error al conectar:", e)
