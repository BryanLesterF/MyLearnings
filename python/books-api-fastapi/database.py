from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
from sqlalchemy.engine import URL

# In real system, values in URL_DATABASE should be retrieved from a config file or url. 
URL_DATABASE = URL.create(
    drivername="mysql+pymysql",
    username="my_user",
    password="my_pass",
    host="localhost",
    port=3306,
    database="fastapi_schema"
)

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()