import pytest
from pydantic import BaseModel
from services.users.users_api import UserAPI

api_user = UserAPI()


class RegisterUser(BaseModel):
    user_id: str
    user_name: str
    email: str
    password: str


@pytest.fixture()
def register_user(request):
    user, register_data = api_user.create_new_user()

    request.cls.email = register_data.email
    request.cls.password = register_data.password

    return RegisterUser(
        user_id=user.data.id,
        user_name=register_data.name,
        email=register_data.email,
        password=register_data.password
    )


@pytest.fixture()
def auth_user(request, register_user):
    login = api_user.login_user(email=request.cls.email, password=request.cls.password)

    request.cls.token = login.data.token


@pytest.fixture()
def delete_new_user(request, auth_user):
    yield
    api_user.delete_user(token=request.cls.token)
