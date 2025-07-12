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
        first_name = fake.first_name()
        if len(first_name) < 4:
            first_name += 'ab'
        return RegisterData(name=first_name, email=fake.email(), password=fake.password())

    @staticmethod
    def update_user():
        first_name = fake.first_name()
        company = fake.company()
        if len(first_name) < 4:
            first_name += 'ab'
        if len(company) < 4:
            company += 'ab'
        return UpdateData(name=first_name, phone=str(fake.random_number(10)), company=company)

    new_password = fake.password()
