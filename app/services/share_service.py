from fastapi import HTTPException
from sqlmodel import Session

from app.models.share import LabelShare, NoteShare, ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class ShareService:
    def __init__(self,db:Session):
        self.db=db
        self.shares=ShareRepository(db)
        self.notes=NoteRepository(db)
        self.labels=LabelRepository(db)
        
    def share_note(self,owner_id:int,note_id:int,target_user_id:int,role:ShareRole)->NoteShare:
        #target_user_id es el id del usuario a quien se le va a compartir la nota
        note=self.notes.get(note_id)
        if note is None or owner_id!=note.owner_id:
            raise HTTPException(status_code=404,detail="Nota no encontrada")
        share=self.shares.upsert_note_share(note_id,target_user_id,role.value if hasattr(role,"value") else role)
        return share
    
    def unshare_note(self,owner_id:int,note_id:int,target_user_id:int)->None:
        #target_user_id es el id del usuario a quien se le va a compartir la nota
        note=self.notes.get(note_id)
        if note is None or owner_id!=note.owner_id:
            raise HTTPException(status_code=404,detail="Nota no encontrada")
        self.shares.remove_note_share(note_id,target_user_id)
    
    def share_label(self,owner_id:int,label_id:int,target_user_id:int,role:ShareRole)->LabelShare:
        label=self.labels.get_by_id(label_id)
        if label is None or label.owner_id!=owner_id:
            raise HTTPException(status_code=404,detail="Etiqueta no encontrada o no autorizada")
        share=self.shares.upsert_label_share(label_id,target_user_id,role.value if hasattr(role,"value") else role)
        return share
    def unshare_label(self,owner_id:int,label_id:int,target_user_id:int):
        label=self.labels.get_by_id(label_id)
        if label is None or label.owner_id!=owner_id:
            raise HTTPException(status_code=404,detail="Etiqueta no encontrada o no autorizada")
        self.shares.remove_label_share(label_id,target_user_id)