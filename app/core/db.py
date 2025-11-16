from typing import Iterator
from sqlmodel import SQLModel, Session, create_engine

from app.core.conf import settings


engine=create_engine(settings.DATABASE_URL,echo=False,connect_args={"check_same_thread":False} if "sqlite" in settings.DATABASE_URL else {})

def init_db()->None:
    
    if settings.ENVIRONMENT=="DEV":
        #! si no esta la base de datos es creada
        SQLModel.metadata.create_all(engine) # dev
    




def get_session()->Iterator[Session]:
    with Session(engine) as session:
        yield session