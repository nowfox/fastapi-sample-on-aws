from typing import Optional
from pydantic import BaseModel, Field

class PetBase(BaseModel):
    name: str = Field(title="MyTitle",description="MyDescription")
    description: Optional[str] = ""


class Pet(PetBase):
    id: int
