from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#password = quote_plus("U5zQNbprFL2ViWh2")

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:U5zQNbprFL2ViWh2"
    "@db.abcd1234.supabase.co:5432/postgres"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_size=5,
    max_overflow=5
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


