from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from .service import UserService
from tradify.db import session_factory
from .schema import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])

def get_user_service() -> UserService:
    return UserService(session_factory)

@router.get('/', response_model=list[UserRead])
def get_all_users(service: UserService = Depends(get_user_service)):
    users = service.get_all_users()
    return users

@router.get('/{user_id}', response_model=UserRead)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user, from_attributes=True)

@router.post('/', response_model=UserRead)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")
    return user

@router.put('/', response_model=UserRead)
def update_user(data: UserUpdate, service: UserService = Depends(get_user_service)):
    user = service.update_user(data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or update failed")
    return user

@router.delete('/{user_id}', response_model=dict)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or delete failed")
    return {"success": True}