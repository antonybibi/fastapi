from auth.auth_database import engine, Base
from auth import model

Base.metadata.create_all(bind=engine)