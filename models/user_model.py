from pydantic import BaseModel


class Data(BaseModel):
    id: str
    name: str
    email: str
    phone: str = ''
    company: str = ''


class LoginData(BaseModel):
    id: str
    name: str
    email: str
    token: str


class UserModel(BaseModel):
    success: bool
    status: int
    message: str
    data: Data


class LoginUserModel(BaseModel):
    success: bool
    status: int
    message: str
    data: LoginData


class BaseResponseModel(BaseModel):
    success: bool
    status: int
    message: str
