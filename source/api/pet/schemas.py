from pydantic import BaseModel, Field
from common.enum import Sex


class PetCreate(BaseModel):
    name: str = Field(description="Pet name")
    sex: Sex = Sex.FEMALE
    description: str | None = None


class Pet(PetCreate):
    id: str


class PetUpdate(BaseModel):
    name: str = None
    sex: Sex = None
    description: str = None
