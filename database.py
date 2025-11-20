from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_URL = (
    "mysql+pymysql://hrd_user:"
    "Nb%40ab10f222f4d824a27e76ac4aff8978d70f631cfce552c5c80ee04903d2db1f07"
    "@72.61.174.26:3306/hrd"
)

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

