from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class User(SQLModel,table=True):
    id: int =Field(default=None,primary_key=True)
    email:str =Field(index=True,unique=True)
    full_name: str=Field(default="")
    hashed_password: str # Se va a llenar solo
    #! para probar upgrade y downgrade de alembic
    #active:bool = Field(default=True) 

#! Esta clase sera tratada como un validador de pydantic sin el table=True
class UserCreate(SQLModel):
    email:str
    full_name:str=""
    password:str

#! Esta clase sera tratada como un validador de pydantic sin el table=True    
class UserRead(SQLModel):
    id: int
    email: str
    #! para poder leer objetos orm o de slqmodel
    model_config = {"from_attributes": True} # type: ignore