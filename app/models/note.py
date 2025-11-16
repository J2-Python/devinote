from typing import Optional
from sqlmodel import SQLModel,Field


class Note(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    title:str
    content:str=""
    color:Optional[str]=None
    owner_id:int=Field(foreign_key="user.id",index=True)

#!Clases de validacion
class NoteCreate(SQLModel):
    title:str
    content:str=""
    color:Optional[str]=None
    label_ids:Optional[list[int]]=None
    
#!Clases de validacion
class NoteUpdate(SQLModel):
    title:Optional[str]=None
    content:Optional[str]=None
    color:Optional[str]=None
    label_ids:Optional[list[int]]=None

#!Clases de validacion
class NoteRead(SQLModel):
    id:int
    title:str
    content:str
    color:str
    #! para poder leer objetos orm o de slqmodel
    model_config={"from_attributes":True}  #type: ignore