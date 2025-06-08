from faker import Faker
from pydantic import BaseModel

fake = Faker()


class RegisterData(BaseModel):
    name: str | int
    email: str
    password: str


class UpdateData(BaseModel):
    name: str
    phone: str = ''
    company: str = ''


class UserPayloads:
    @staticmethod
    def create_user():
        return RegisterData(name=fake.first_name(), email=fake.email(), password=fake.password())

    @staticmethod
    def update_user():
        return UpdateData(name=fake.first_name(), phone=str(fake.random_number(10)), company=fake.company())

    new_password = fake.password()


print(UserPayloads.create_user().email)
