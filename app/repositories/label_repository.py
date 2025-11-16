from typing import Sequence
from sqlmodel import Session, delete, select, asc

from app.models.label import Label, NoteLabelLink
from app.models.share import LabelShare

class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, label_id: int) -> Label | None:
        return self.db.get(Label, label_id)

    def list_by_user(self, owner_id: int) -> Sequence[Label]:
        query = select(Label).where(Label.owner_id == owner_id).order_by(Label.name.asc()) # type: ignore
        return self.db.exec(
            query
        ).all()  # el resultado es de tipo sequence se puede convertir a list

    def get_by_name(self, owner_id:int,name:str) -> Label | None:
        #! se tiene que cumplir 2 condiciones que sea nuestros label y el nombre del label
        return self.db.exec(select(Label).where(Label.id==owner_id,Label.name == name)).first()

    def create(self, owner_id:int,name:str) -> Label:
        # Creamos la instancia de label para crearlo
        label=Label(name=name,owner_id=owner_id)
        self.db.add(label)
        self.db.flush()
        self.db.commit()
        self.db.refresh(label)
        return label
    def delete(self,label:Label)->None:
        #!eliminamos las relaciones
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.label_id == label.id))  # type: ignore
        self.db.exec(delete(LabelShare).where(LabelShare.label_id == label.id)) # type: ignore
        #!Eliminamos el label
        # delete the Label instance via the Session API to avoid constructing a where-clause expression
        self.db.delete(label)
        self.db.commit()
    
    def list_ids_for_owner_subset(self,owner_id:int,ids:list[int])->Sequence[int]:
        if not ids:
            return []
        rows=self.db.exec(select(Label.id).where(Label.owner_id==owner_id,Label.id.in_(set(ids)))).all() # type: ignore
        #rows = self.db.exec(select(Label.id).where(Label.owner_id == owner_id, getattr(Label, "id").in_(set(ids)))).all()
        return rows
    
    def list_label_ids_for_note(self,note_id:int)->Sequence[int]:
        return self.db.exec(select(NoteLabelLink.label_id).where(NoteLabelLink.note_id==note_id)).all()
    
    def list_note_ids_by_label_ids(self,label_ids:list[int])->Sequence[int]:
        if not label_ids:
            return []
        
        
        return self.db.exec(select(NoteLabelLink.note_id).where(NoteLabelLink.label_id.in_(set(label_ids)))).all() # type: ignore
        #return self.db.exec(select(NoteLabelLink.note_id).where(getattr(NoteLabelLink,"label_id").in_(set(label_ids)))).all()