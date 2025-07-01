import allure
import responses
from config.config import Headers
from models.base_model import BaseResponseModel
from models.user_model import UserModel, LoginUserModel
from services.users.users_endpoints import UsersEndpoints
from services.users.users_payloads import UserPayloads
from utils.helper import Helper
from utils.my_requests import MyRequests


class UserAPI(Helper):
    def __init__(self):
        self.endpoints = UsersEndpoints()
        self.payloads = UserPayloads()
        self.headers = Headers

    @allure.step('Register a new user')
    def create_new_user(self):
        payload = self.payloads.create_user()
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload.model_dump()
        )
        assert response.status_code == 201, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = UserModel(**response.json())
        return model, payload

    @allure.step('Register two users with the same email')
    def create_same_user_twice(self):
        payload = self.payloads.create_user().model_dump()
        MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        assert response.status_code == 409, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Register a user with empty required field')
    def create_user_with_empty_required_field(self, empty_field):
        payload = self.payloads.create_user().model_dump()
        payload[empty_field] = ''
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Register a user with with specific data')
    def create_user_with_specific_data(self, field, value):
        payload = self.payloads.create_user().model_dump()
        payload[field] = value
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=payload
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Login with valid email and password')
    def login_user(self, email, password):
        response = MyRequests.post(
            url=self.endpoints.login_user,
            json={'email': email, 'password': password}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = LoginUserModel(**response.json())
        return model

    @allure.step('Login with empty credentials')
    def login_with_empty_credentials(self, email='', password=''):
        response = MyRequests.post(
            url=self.endpoints.login_user,
            json={'email': email, 'password': password}
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Login with wrong credentials')
    def login_with_wrong_credentials(self, email, password):
        response = MyRequests.post(
            url=self.endpoints.login_user,
            json={'email': email, 'password': password}
        )
        assert response.status_code == 401, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Get profile info for authed user')
    def get_user(self, token):
        response = MyRequests.get(
            url=self.endpoints.get_user_profile,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = UserModel(**response.json())
        return model

    @allure.step('Get profile info without auth header')
    def get_not_authed_user(self):
        response = MyRequests.get(
            url=self.endpoints.get_user_profile,
        )
        assert response.status_code == 401, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Get profile info with not valid or expired token')
    def get_user_with_expired_token(self, token):
        response = MyRequests.get(
            url=self.endpoints.get_user_profile,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 401, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Update profile info for authed user')
    def update_user(self, token):
        payload = self.payloads.update_user()
        response = MyRequests.patch(
            url=self.endpoints.update_user_profile,
            json=payload.model_dump(),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = UserModel(**response.json())
        return model, payload

    @allure.step('Update user with empty required field')
    def update_user_with_empty_required_field(self, token, field):
        payload = self.payloads.update_user().model_dump()
        payload[field] = ''
        response = MyRequests.patch(
            url=self.endpoints.update_user_profile,
            json=payload,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Logout authed user')
    def logout_user(self, token):
        response = MyRequests.delete(
            url=self.endpoints.logout_user,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Delete authed user')
    def delete_user(self, token):
        response = MyRequests.delete(
            url=self.endpoints.delete_user,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step("Send the password reset link to the user's email")
    def send_password_reset_link(self, email):
        response = MyRequests.post(
            url=self.endpoints.send_password_reset_link,
            json={'email': email}
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    def reset_password(self, token, new_password):
        response = MyRequests.post(
            url=self.endpoints.reset_password,
            json={'token': token, 'newPassword': new_password},
            headers=self.headers.auth_token(token)
        )
        return response

    @allure.description("Change a user's password")
    def change_password(self, token, current_password):
        new_password = self.payloads.new_password
        response = MyRequests.post(
            url=self.endpoints.change_password,
            json={'currentPassword': current_password, 'newPassword': new_password},
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model, new_password

    @allure.step('Returns 500 internal server error for "get user profile" request')
    @responses.activate
    def get_user_profile_internal_server_error(self, token=None):
        responses.add(
            responses.GET,
            self.endpoints.get_user_profile,
            json={
                "success": False,
                "status": 500,
                "message": "Internal Error Server"
            },
            status=500
        )
        response = MyRequests.get(
            url=self.endpoints.get_user_profile,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 500, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Returns 500 internal server error for "create user" request')
    @responses.activate
    def create_user_internal_server_error(self):
        responses.add(
            responses.POST,
            self.endpoints.create_user,
            json={
                "success": False,
                "status": 500,
                "message": "Internal Error Server"
            },
            status=500
        )
        response = MyRequests.post(
            url=self.endpoints.create_user,
            json=self.payloads.create_user().model_dump()
        )
        assert response.status_code == 500, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model
