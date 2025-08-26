from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

#load_dotenv()
#DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URL = "postgresql://postgres:postgrespassword@postgres-db:5432/fastapi_clients_orders"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()