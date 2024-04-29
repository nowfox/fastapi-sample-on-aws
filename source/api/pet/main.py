from fastapi import APIRouter
from . import schemas, service

router = APIRouter(prefix="/pets", tags=["pets"])


@router.get("", response_model=list[schemas.Pet])
def list():
    return service.list();


@router.get("/{id}", response_model=schemas.Pet)
def get(id: int):
    return service.get(id);
