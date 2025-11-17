import os
from typing import Iterator
from sqlmodel import SQLModel, Session, create_engine
from app.core.conf import settings


raw_url = os.environ["DATABASE_URL"]
url = raw_url

if url.startswith("postgres://"):
    url = "postgresql+psycopg://" + url[len("postgres://")]
    print(f"url {url}")
elif url.startswith("postgresql://") and "+psycopg" not in url:
    url = "postgresql+psycopg://" + url[len("postgresql://")]

# engine=create_engine(settings.DATABASE_URL,echo=False,connect_args={"check_same_thread":False} if "sqlite" in settings.DATABASE_URL else {})
engine = create_engine(url, pool_pre_ping=True)


def init_db() -> None:

    if settings.ENVIRONMENT == "DEV":
        #! si no esta la base de datos es creada
        SQLModel.metadata.create_all(engine)  # dev


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
