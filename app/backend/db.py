from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('sqlite:///taskmanager.db')


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


Base = declarative_base()