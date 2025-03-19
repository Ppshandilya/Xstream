from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote


# MySQL Database URL with custom port
user='root'
password='Mrin@0108'
encoded_password = quote(password, safe='')
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password }@localhost:3306/mysql"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
