from sqlalchemy.orm import sessionmaker
from sqlmodel import Session ,select
from uuid import UUID
from .models import User 
from .schema import UserCreate, UserRead, UserDelete, UserUpdate

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

class UserService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory = session_factory
        self.hash = pwd_context.hash

        


    def get_user(self, user_id:UUID)->User | None:
        with self.session_factory() as session:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()

            return user
        
    def get_all_users(self)->list[User]| None:
        with self.session_factory() as session:
            statement = select(User)
            users = session.exec(statement).all()

            return list(users)


    def create_user(self, data: UserCreate) -> UserRead | None:
        from tradify.wallet.models.wallet import Wallet  # Import here to avoid circular import
        with self.session_factory() as session:
            try:
                # Create the user instance
                user = User(**data.model_dump())
                user.hashed_password = self.hash(data.password)
                # Create a wallet for the user
                wallet = Wallet()
                session.add(wallet)
                session.commit()
                session.refresh(wallet)
                # Link wallet to user
                user.wallet_id = wallet.id
                session.add(user)
                session.commit()
                session.refresh(user)
                return UserRead.model_validate(user, from_attributes=True)
            except Exception as e:
                print('-----------------------------------------------')
                print(e)
                print('-----------------------------------------------')
                return None


    def update_user(self, data: UserUpdate)->UserRead | None:
        with self.session_factory() as session:
            try:
                user =session.exec(select(User).where(User.id==data.id)).first()
                if not user:
                    return None
                update_data = data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(user, key, value)
                session.add(user)
                session.commit()
                session.refresh(user)
                return UserRead.model_validate(user, from_attributes=True)
            except Exception as e:
                print('-----------------------------------------------')
                print(e)
                print('-----------------------------------------------')
                return None

    def delete_user(self, user_id: UUID) -> bool:
        with self.session_factory() as session:
            try:
                user = session.exec(select(User).where(User.id == user_id)).first()
                if not user:
                    return False
                session.delete(user)
                session.commit()
                return True
            except:
                return False


