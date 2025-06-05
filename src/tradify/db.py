from sqlmodel import  create_engine, Session
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL') or ''
engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
