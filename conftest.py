import pytest
from pydantic import BaseModel
from services.notes.notes_api import NotesAPI
from services.users.users_api import UserAPI

api_user = UserAPI()
api_note = NotesAPI()


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


@pytest.fixture()
def create_note(request, auth_user):
    note, note_data = api_note.create_new_note(token=request.cls.token)
    return note
