from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

try:
    SQLALCHEMY_DATABASE_URI = f"postgres://postgres:admin@localhost/eo"

except Exception as e:
    print(e)
    print("Favor configurar as variaveis de ambiente: [USERDB, PASSWORDDB, HOST, DBNAME]")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URI,pool_size=20, max_overflow=0)

Base = declarative_base()

class Config():
    """ Represents an abstract class that will be used to another models."""

    def create_database(self):
        Session = scoped_session(sessionmaker(bind=engine,autocommit=True))
        session = Session()
        session.begin(subtransactions=True)
        Base.metadata.create_all(engine)
