import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

# import models here so sqlmodel discovers table definitions
from database.models import Shipment, User, RevokedToken  # noqa: F401

load_dotenv()

# defaults to local sqlite so students can test immediately without installing postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# sqlite needs this flag so fastapi background threads can access the same connection
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    url=DATABASE_URL,
    echo=False,
    connect_args=connect_args,
)


def create_db_and_table():
    SQLModel.metadata.create_all(bind=engine)


# dependency to inject db session into route handlers
def get_session():
    with Session(engine) as db:
        yield db
