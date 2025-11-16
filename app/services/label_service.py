from fastapi import HTTPException
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self,db:Session):
        self.db=db
        self.label=LabelRepository(db)
    
    def list(self,owner_id:int)->list[Label]:
        return list(self.label.list_by_user(owner_id))
    
    def create(self,owner_id:int,payload:LabelCreate)->Label:
        #! Verificamos si existe
        if self.label.get_by_name(owner_id,payload.name):
            raise HTTPException(status_code=400,detail="Label ya existe")
        return self.label.create(owner_id,payload.name)
    
    def delete(self,owner_id:int,label_id:int)->None:
        #! Verificamos si existe
        label=self.label.get_by_id(label_id)
        if  label is None or owner_id!=label.owner_id:
            raise HTTPException(status_code=404,detail="Label no existe o no autorizado")
        self.label.delete(label)