from typing import Sequence
from fastapi import APIRouter,status

from app.api.deps import CurrentUser, DBSession
from app.models.label import Label, LabelCreate, LabelRead
from app.services.label_service import LabelService


router = APIRouter(prefix="/labels", tags=["Labels"])
# get / listar labels
@router.get("/",response_model=list[LabelRead])
def listar_labels(db:DBSession,user:CurrentUser)->Sequence[Label]:
    service=LabelService(db)
    return service.list(user.id)

# post / crear
@router.post("/",response_model=LabelRead,status_code=status.HTTP_201_CREATED)
def create(db:DBSession,payload:LabelCreate,user:CurrentUser)->Label:
    service=LabelService(db)
    return service.create(user.id,payload)

# delete /{label_id}
@router.delete("/{label}",status_code=status.HTTP_204_NO_CONTENT)
def delete(db:DBSession,label_id:int,user:CurrentUser):
    service=LabelService(db)
    service.delete(user.id,label_id)
    return None