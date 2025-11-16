from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_db() -> Session:
    # toma el primer valor devuelto por el yeld por la funcion generadora get_db
    return next(get_session())


# antes en el def de la ruta db:Session=Depends(get_db)
DBSession = Annotated[
    Session, Depends(get_db)
]  # Annotated incluye: el tipo de datos y los metadatos
# ahora en el def de la ruta db:DBSession


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DBSession) -> User:
    
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No authorizado",
        headers={"www-Authenticate": "Bearer"},
    )
    try:
        print(f"Entro get_current_user:{token}")
        payload = decode_token(token)
        print(f"type {payload}")
        user_id = payload.get("sub")
    except Exception :
        raise credentials_exc
        
    repo = UserRepository(db)
    user = repo.get_by_id(user_id or 0)
    if not user:
        raise credentials_exc
    print(f"User {user}")
    return user

CurrentUser=Annotated[User,Depends(get_current_user)]