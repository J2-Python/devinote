from fastapi import HTTPException
from sqlmodel import Session

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.note_repository import NoteRepository
from app.repositories.label_repository import LabelRepository
from app.repositories.share_repository import ShareRepository

class NoteService:
    def __init__(self,db:Session):
        self.db=db
        self.notes=NoteRepository(db)
        self.labels=LabelRepository(db)
        self.shares=ShareRepository(db)
    
    #!Permisos:
    def user_can_read(self,user_id:int,note:Note)->bool:
        #si el owner de la nota es igual al user_id que se envia
        if note.owner_id==user_id:
            return True
        #si la nota le ha sido compartido al usuario enviado
        if self.shares.has_note_share(note_id=note.id,user_id=user_id):
            return True
        #nos traemos las labels de la nota
        label_ids=self.labels.list_label_ids_for_note(note.id)
        
        return self.shares.has_any_label_share(list(label_ids),user_id)
    
    def user_can_edit(self,user_id:int,note:Note)->bool:
        #si el owner de la nota es igual al user_id que se envia
        if note.owner_id==user_id:
            return True
        #si la nota le ha sido compartido al usuario enviado y si tiene permisos de edicion
        if self.shares.has_note_share(note_id=note.id,user_id=user_id,role=ShareRole.EDIT):
            return True
        #nos traemos las labels de la nota
        label_ids=self.labels.list_label_ids_for_note(note.id)
        
        return self.shares.has_any_label_share(list(label_ids),user_id,role=ShareRole.EDIT)
        
    def list_visible(self,user_id:int)->list[Note]:
        #recupero las notas que le pertenecen al usuario
        owned=self.notes.list_owned(user_id) # [Note(id=10), Note(id=12)]
        print(f"owned {len(owned)}")
        for item in owned:
            print(item)
        notes_direct_ids=self.shares.list_note_ids_shared_directly(user_id)
        print(f"notes_direct_ids {len(notes_direct_ids)}")
        for item in notes_direct_ids:
            print(item)
        
        
        shared_label_ids=self.shares.list_label_ids_shared_with_user(user_id)
        print(f"list_label_ids_shared_with_user {len(shared_label_ids)}")
        for item in shared_label_ids:
            print(item)
        
        ids_by_label=self.labels.list_note_ids_by_label_ids(list(shared_label_ids))
        print(f"ids_by_label {len(ids_by_label)}")
        for item in ids_by_label:
            print(item)
        
        
        ids=list({*notes_direct_ids,*ids_by_label})#dentro de la lista hay un set
        print(f"len ids {len(ids)}")
        print(ids)
        for item in ids:
            print(item)
        
        shared=self.notes.list_by_ids(ids)
        
        #! para cada nota dentro de las notas que son mias
        # creamos un diccionario dinamico con las notas propias del usuario
        # {10: Note(10), 12: Note(12)}
        combined={note.id: note for note in owned}
        
        for note in shared:# 👉 Las notas compartidas
            # 👉 "Si la clave NO existe en el diccionario, la agrego con ese valor.Si YA existe, no la toco."
            combined.setdefault(note.id,note)
        print(f"Combined: {combined}")
        return sorted(combined.values(),key=lambda note:note.id, reverse=True )
    
    
    
    def create(self,owner_id:int, payload:NoteCreate)->Note:
        #Como payload es un objeto de timpo NoteCreate hacemos un model_dump para crear un diccionario sin el atributo label_ids
        note=self.notes.create(Note(owner_id=owner_id,**payload.model_dump(exclude={"label_ids"})))
        
        if payload.label_ids: #si vienen los label_ids, llamamos al helper
            self._set_labels(owner_id,note.id,payload.label_ids)
        return note
        
    def update(self,user_id:int,note_id:int,payload:NoteUpdate)->Note:
        note=self.notes.get(note_id)
        if note is None:
            raise HTTPException(status_code=404,detail="Nota n existe")
        if self.user_can_edit(user_id,note) is None:
            raise HTTPException(status_code=403,detail="No autorizado")
        updates=payload.model_dump(exclude_none=True)
        label_ids=updates.pop("label_ids",None)#👉 quitamos del dict el key label_ids, si no se encuentra se devuelve None, para manejarlo por separado
        
        for key,value in updates.items():
            setattr(note,key,value)
        self.notes.update(note)
        
        if label_ids is not None:
            if note.owner_id!=user_id:
                raise HTTPException(status_code=404,detail="No Autorizado")
        self._set_labels(user_id,note.id,label_ids)
        return note
    
    def delete(self,user_id,note_id)->None:
        note=self.notes.get(note_id)
        if note is None or user_id!=note.owner_id:
            raise HTTPException(status_code=404,detail="Nota no existe o No autorizado")
        self.notes.delete(note)
    
    #!Helper
    def _set_labels(self,owner_id:int,note_id:int,label_ids:list[int])->None:
        valid_ids=self.labels.list_ids_for_owner_subset(owner_id,label_ids or [])
        self.notes.replace_labels(owner_id,note_id,list(valid_ids))
