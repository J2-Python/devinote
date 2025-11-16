from typing import List, Sequence
from sqlmodel import Session,select,delete
from app.models.label import NoteLabelLink
from app.models.note import Note

class NoteRepository:
    def __init__(self,db:Session):
        self.db=db
    
    def list_owned(self, owner_id: int) -> Sequence[Note]:
        query = select(Note).where(Note.owner_id ==
                                   owner_id).order_by(Note.id.desc()) # type: ignore
        return self.db.exec(query).all()
    
    def get(self,note_id)->Note|None:
        return self.db.get(Note,note_id)
    
    def create(self,note:Note)->Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def update(self,note:Note)->Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def delete(self,note:Note)->None:
        #!primero borramos los enlaces
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id==note.id)) # type: ignore
        self.db.delete(note)
        self.db.commit()
    
    def replace_labels(self,owner_id:int,note_id:int,label_ids:List[int])->None:
        #! primero borramos todos los enlaces
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id==note_id)) # type: ignore
        #! Luego agregamos los nuebos label_ids
        for label_id in set(label_ids or []):#list sin duplicados
            self.db.add(NoteLabelLink(note_id=note_id,label_id=label_id))
            self.db.commit()
    
    def list_by_ids(self,ids:list[int])->Sequence[Note]:
        print(f"list_by_ids {ids}")
        if not ids:
            return[]
        return self.db.exec(select(Note).where(Note.id.in_(set(ids)))).all()# type: ignore
        #return self.db.exec(select(Note).where(getattr(Note,"id").in_(set(ids)))).all()
        