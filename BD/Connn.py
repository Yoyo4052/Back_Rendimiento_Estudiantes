from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseURL = "mysql://root:AxunnCqyVcNXuYrYmbernOvicOPIsOzu@autorack.proxy.rlwy.net:45891/railway"

engine = create_engine(databaseURL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base