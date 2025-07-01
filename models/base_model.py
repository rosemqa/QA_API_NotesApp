from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    success: bool
    status: int
    message: str
