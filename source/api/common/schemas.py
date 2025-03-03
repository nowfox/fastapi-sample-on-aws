from pydantic import BaseModel


class Error(BaseModel):
    code: int
    message: str


class Result(BaseModel):
    result: str
