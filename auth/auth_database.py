from sqlalchemy import create_engine # to connect the enginer to the db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the DATABASE_URL with your MySQL credentials
# format: "mysql+pymysql://<username>:<password>@<host>:<port>/<db_name>"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:my-secret-pw@127.0.0.1:3307/fastapi_db"


# Connection
engine = create_engine(SQLALCHEMY_DATABASE_URL) #  Connection is ready
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine) # session

Base = declarative_base() # all the sql achemy model is inheritted

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
