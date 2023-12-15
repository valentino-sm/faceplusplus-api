from pydantic import BaseModel


class DetectResponse(BaseModel):
    id: str
    face_tokens: list[str]


class CompareResponse(BaseModel):
    score: float
