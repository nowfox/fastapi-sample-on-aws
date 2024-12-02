from fastapi import APIRouter
from common.schemas import Result
from . import schemas, service

router = APIRouter(prefix="/pets", tags=["Pets"])


@router.get("", response_model=list[schemas.Pet])
def list():
    return service.list()


@router.get("/{id}", response_model=schemas.Pet)
def get(id: str) -> schemas.Pet:
    return service.get(id)


@router.post("", response_model=schemas.Pet)
def create(pet: schemas.PetCreate) -> schemas.Pet:
    """
    Create a pet.
    """
    return service.create(pet)


@router.patch("/{id}", response_model=schemas.PetUpdate)
def update(id: str, pet: schemas.PetUpdate) -> schemas.PetUpdate:
    return service.update(id, pet)


@router.delete("/{id}", response_model=Result)
def delete(id: str) -> schemas.Pet:
    service.delete(id)
    return Result(result="OK")
