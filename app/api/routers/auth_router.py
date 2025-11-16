from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DBSession
from app.models.user import UserCreate, UserRead
from app.repositories.user_repository import UserRepository
from app.services.auth_services import AuthServices


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate, db: DBSession
):  # 👉 en lugar de db:Session = Deps(get_db)
    service = AuthServices(
        UserRepository(db)
    )  # 👉 tenemos que enviar una instancia de UserRepository
    return service.register(payload)


@router.post("/login")
def login(
    email: str, password: str, db: DBSession
):  # 👉 en lugar de db:Session = Deps(get_db)
    service = AuthServices(
        UserRepository(db)
    )  # 👉 tenemos que enviar una instancia de UserRepository
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}


#! ruta para usar el formulario en swagger


@router.post("/token")
def login_form(
    db: DBSession, form: OAuth2PasswordRequestForm = Depends()
):  # 👉 en lugar de db:Session = Deps(get_db)
    service = AuthServices(
        UserRepository(db)
    )  # 👉 tenemos que enviar una instancia de UserRepository
    email = form.username
    password = form.password
    service = AuthServices(UserRepository(db))
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}
