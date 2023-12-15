from pydantic import BaseModel
from pydantic.fields import Field
from pydantic_extra_types.color import Color


class GetImageRequest(BaseModel):
    color: Color | None = Field(default=None, examples=["blue", "red", "green"])
    face_tokens: list[str] = Field(default_factory=list, examples=[[]])


class GetCompareRequest(BaseModel):
    face_token_1: str
    face_token_2: str
