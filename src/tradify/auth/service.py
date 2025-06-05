from sqlmodel import Session, select
from sqlalchemy.orm import sessionmaker
from uuid import UUID




class AuthService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory=session_factory


    def login(self):
        pass

