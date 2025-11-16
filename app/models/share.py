from enum import Enum
#from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field,UniqueConstraint


class ShareRole(str, Enum):
    READ = "read"
    EDIT = "edit"


class NoteShare(SQLModel, table=True):
    __tablename__="note_share"  # type: ignore
    # uniqueconstraint: no puede haber 2 o mas registros con la misma combinacion note_id+user_id 
    __table_args__=(UniqueConstraint("note_id","user_id",name="uq_note_user"),)
    
    id: int = Field(default=None,primary_key=True)
    note_id:int =Field(foreign_key="note.id",index=True)
    user_id:int =Field(foreign_key="user.id",index=True)
    role:ShareRole=Field(default=ShareRole.READ)

class LabelShare(SQLModel,table=True):
    __tablename__="label_share" # type: ignore
    # uniqueconstraint: no puede haber 2 o mas registros con la misma combinacion user_id+label_id 
    __table_args__=(UniqueConstraint("user_id","label_id",name="uq_user_label"),)
    
    id: int = Field(primary_key=True,index=True)
    label_id:int =Field(foreign_key="label.id",index=True)
    user_id:int =Field(foreign_key="user.id",index=True)
    role:ShareRole=Field(default=ShareRole.READ)

class ShareRequest(SQLModel):
    target_user_id:int =Field(gt=0)
    role:ShareRole=ShareRole.READ
    