from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseURL = "mysql://tesista:12345@localhost:3307/proto_db"

engine = create_engine(databaseURL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base