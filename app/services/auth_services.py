from fastapi import HTTPException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthServices:
    def __init__(self,repository:UserRepository):
        self.repository=repository
    def register(self,payload:UserCreate)->User:
        if self.repository.get_by_email(payload.email):
            raise HTTPException(status_code=400,detail="Email ya registrado")
        
        user=User(email=payload.email,full_name=payload.full_name,hashed_password=hash_password(payload.password[:72]))
        return self.repository.create(user)

    def login(self,email:str,password:str)->str:
        user=self.repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404,detail="Usuario no existe")
        
        if not verify_password(password,user.hashed_password):
            raise HTTPException(status_code=401,detail="Credenciales invalidas")
        
        return create_access_token({"sub":str(user.id)})