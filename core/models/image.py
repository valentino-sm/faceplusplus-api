from pydantic import BaseModel


class Face(BaseModel):
    id: str
    x: int
    y: int
    width: int
    height: int


class Image(BaseModel):
    id: str
    data: bytes
    faces: list[Face]
