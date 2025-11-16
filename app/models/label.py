from operator import index
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Label(SQLModel,table=True):
    #!Caracteristicas avanzadas
    #nombre de la tabla personalizada
    #__tablename__="label"
    # uniqueconstraint: no puede haber 2 o mas registros con la misma combinacion owner_id+name 
    __table_args__=(UniqueConstraint("owner_id","name",name="uq_label_owner_name"),)
    
    id: int=Field(default=None,primary_key=True)
    name:str=Field(index=True,min_length=1)
    owner_id:int=Field(foreign_key="user.id",index=True)

#!Tabla Intermedia
class NoteLabelLink(SQLModel,table=True):
    __tablename__="note_label_link" # type: ignore
    # uniqueconstraint: no puede haber 2 o mas registros con la misma combinacion note_id+label_id 
    __table_args__=(UniqueConstraint("note_id","label_id",name="uq_note_label_name"),)
    id:int=Field(default=None,primary_key=True)
    note_id:int=Field(foreign_key="note.id",index=True)
    label_id:int=Field(foreign_key="label.id",index=True)

class LabelCreate(SQLModel):
    #!solo enviamos el nombre
    name:str

class LabelRead(SQLModel):
    id:int
    name:str
    model_config={"from_attributes":True} # type: ignore