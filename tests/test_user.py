import allure
import pytest
from faker import Faker
from config.base_test import BaseTest
from services.users.users_constants import UsersMessages

fake = Faker()


@allure.epic('Users')
class TestUser:
    @allure.feature('Create user')
    class TestCreateUser(BaseTest):
        @allure.description('Can register a new user')
        def test_create_new_user(self, check):
            user, register_data = self.api_user.create_new_user()

            with check:
                assert user.success is True, 'Check the Success'
                assert user.status == 201, 'Check the Status'
                assert user.message == UsersMessages.ACCOUNT_CREATED, 'Check the Message text'
            with check:
                assert user.data.name == register_data.name, 'Check the Name'
            with check:
                assert user.data.email == register_data.email, 'Check Email'

        @allure.description('Can not register a user with existing email')
        @allure.tag('negative')
        def test_create_same_user_twice(self):
            user = self.api_user.create_same_user_twice()

            assert user.success is False, 'Check the Success'
            assert user.status == 409, 'Check the Status'
            assert user.message == UsersMessages.ACCOUNT_ALREADY_EXISTS, 'Check the Message text'

        @allure.description('Unable to create user if any of the required fields are empty')
        @allure.tag('negative')
        @pytest.mark.parametrize('empty_field, error_message', [
            ('name', UsersMessages.NAME_ERROR),
            ('email', UsersMessages.EMPTY_EMAIL),
            ('password', UsersMessages.PASSWORD_ERROR)
        ])
        def test_create_user_with_empty_required_field(self, empty_field, error_message):
            user = self.api_user.create_user_with_empty_required_field(empty_field)

            assert user.success is False, 'Check the Success'
            assert user.status == 400, 'Check the Status'
            assert user.message == error_message, 'Check the Message text'

        @allure.description('Unable to create user with name that is less than 4 symbols and greater than 30 symbols')
        @allure.tag('negative')
        @pytest.mark.parametrize('value', ['qwe', 'qwertyuiopasdfghjklzxcvbnmqwerv'])
        def test_create_user_with_too_short_or_long_name(self, value):
            user = self.api_user.create_user_with_specific_data('name', value)

            assert user.message == UsersMessages.NAME_ERROR

        @allure.description('Can not create user with password that is less than 6 symbols and greater than 30 symbols')
        @allure.tag('negative')
        @pytest.mark.parametrize('value', ['12345', '1234567890123456789012345678900'])
        def test_create_user_with_too_short_or_long_password(self, value):
            user = self.api_user.create_user_with_specific_data('password', value)

            assert user.message == UsersMessages.PASSWORD_ERROR

        @allure.description('Check for 500 internal server error for "create user" request')
        def test_create_user_returns_500(self):
            error = self.api_user.create_user_internal_server_error()

            assert error.success is False, 'Check the Success'
            assert error.status == 500, 'Check the Status'
            assert error.message == UsersMessages.INTERNAL_SERVER_ERROR, 'Check the Message text'

    @allure.feature('Login/logout user')
    class TestAuthUser(BaseTest):
        @allure.description('Can login with valid credentials')
        def test_auth_user(self, check, register_user, delete_new_user):
            login = self.api_user.login_user(email=register_user.email, password=register_user.password)

            with check:
                assert login.success is True, 'Check the Success'
                assert login.status == 200, 'Check the Status'
                assert login.message == UsersMessages.LOGIN_SUCCESSFUL, 'Check the Message text'
            with check:
                assert login.data.id == register_user.user_id, 'Check the user ID'
            with check:
                assert login.data.name == register_user.user_name, 'Check the user name'
            with check:
                assert login.data.email == register_user.email, 'Check Email'

        @allure.description('Can not login with empty required fields')
        @allure.tag('negative')
        @pytest.mark.parametrize('empty_field, error_message', [
            ('email', UsersMessages.EMPTY_EMAIL),
            ('password', UsersMessages.PASSWORD_ERROR)
        ])
        def test_login_with_empty_credentials(self, register_user, delete_new_user, empty_field, error_message):
            if empty_field == 'email':
                login = self.api_user.login_with_empty_credentials(password=register_user.password)
            else:
                login = self.api_user.login_with_empty_credentials(email=register_user.email)

            assert login.success is False, 'Check the Success'
            assert login.status == 400, 'Check the Status'
            assert login.message == error_message, f'Check the Message text for empty {empty_field} field'

        @allure.description('Can not login with wrong email or password')
        @allure.tag('negative')
        @pytest.mark.parametrize('wrong_value', ['email', 'password'])
        def test_login_with_wrong_credentials(self, register_user, delete_new_user, wrong_value):
            wrong_email = fake.email()
            wrong_password = fake.password()

            if wrong_value == 'email':
                login = self.api_user.login_with_wrong_credentials(email=wrong_email, password=register_user.password)
            else:
                login = self.api_user.login_with_wrong_credentials(email=register_user.email, password=wrong_password)

            assert login.success is False, 'Check the Success'
            assert login.status == 401, 'Check the Status'
            assert login.message == UsersMessages.WRONG_CREDENTIALS, f'Check the Message text for wrong {wrong_value}'

        @allure.description('Can logout user')
        def test_logout_user(self, auth_user):
            logout_response = self.api_user.logout_user(self.token)

            assert logout_response.success is True, 'Check the Success in response for DELETE method'
            assert logout_response.status == 200, 'Check the Status in response for DELETE method'
            assert logout_response.message == UsersMessages.LOGOUT_SUCCESSFUL, 'Check Message text for DELETE method'

            get_response = self.api_user.get_user_with_expired_token(self.token)

            assert get_response.success is False, 'Check the Success in response for GET method'
            assert get_response.status == 401, 'Check the Status in response for GET method'
            assert get_response.message == UsersMessages.TOKEN_NOT_VALID, 'Check the Message text for GET method'

    @allure.feature('Get user account')
    class TestGetUser(BaseTest):
        @allure.description('Can get user info for authed user')
        def test_get_user_info(self, check, register_user, auth_user, delete_new_user):
            profile = self.api_user.get_user(token=self.token)

            with check:
                assert profile.success is True, 'Check the Success'
                assert profile.status == 200, 'Check the Status'
                assert profile.message == UsersMessages.GET_PROFILE_SUCCESSFUL, 'Check the Message text'
            with check:
                assert profile.data.id == register_user.user_id, 'Check the user ID'
            with check:
                assert profile.data.name == register_user.user_name, 'Check the user name'
            with check:
                assert profile.data.email == register_user.email, 'Check Email'

        @allure.description('Unauthorized user can not get a user info')
        def test_get_user_info_without_auth_header(self):
            user = self.api_user.get_not_authed_user()

            assert user.success is False, 'Check the Success'
            assert user.status == 401, 'Check the Status'
            assert user.message == UsersMessages.NO_TOKEN, 'Check the Message text'

        @allure.description('Check for 500 internal server error for "get user profile" request')
        def test_user_profile_returns_500(self, auth_user, delete_new_user):
            error = self.api_user.get_user_profile_internal_server_error(self.token)

            assert error.success is False, 'Check the Success'
            assert error.status == 500, 'Check the Status'
            assert error.message == UsersMessages.INTERNAL_SERVER_ERROR, 'Check the Message text'

    @allure.feature('Update user account')
    class TestUpdateUser(BaseTest):
        @allure.description('Can update user info for authed user')
        def test_update_user(self, check, register_user, auth_user, delete_new_user):
            user, updated_data = self.api_user.update_user(token=self.token)

            with check:
                assert user.success is True, 'Check the Success'
                assert user.status == 200, 'Check the Status'
                assert user.message == UsersMessages.PROFILE_UPDATED, 'Check the Message text'
            with check:
                assert user.data.id == register_user.user_id, 'Check the user ID'
            with check:
                assert user.data.name == updated_data.name, 'Check the Name'
            with check:
                assert user.data.email == user.data.email, 'Check Email'
            with check:
                assert user.data.phone == updated_data.phone, 'Check the phone number'
            with check:
                assert user.data.company == updated_data.company, 'Check the company name'

        @allure.description('Unable to update user without filling required field')
        @allure.tag('negative')
        def test_update_with_empty_required_field(self, auth_user, delete_new_user):
            user = self.api_user.update_user_with_empty_required_field(token=self.token, field='name')

            assert user.success is False, 'Check the Success'
            assert user.status == 400, 'Check the Status'
            assert user.message == UsersMessages.NAME_ERROR, 'Check the Message text'

    @allure.feature('Delete user account')
    class TestDeleteUser(BaseTest):
        @allure.description('Can delete authed user')
        def test_delete_user(self, register_user, auth_user):
            del_response = self.api_user.delete_user(self.token)

            assert del_response.success is True, 'Check the Success'
            assert del_response.status == 200, 'Check the Status'
            assert del_response.message == UsersMessages.ACCOUNT_DELETED, 'Check the Message text'

    @allure.feature('Change/reset password')
    class TestChangePassword(BaseTest):
        @allure.description('Can send the link to reset the password')
        def test_send_password_reset_link(self, register_user, delete_new_user):
            email = register_user.email
            link = self.api_user.send_password_reset_link(email)

            assert link.success is True, 'Check the Success'
            assert link.status == 200, 'Check the Status'
            assert link.message == UsersMessages.PASSWORD_RESET_LINK_SENT(email), 'Check the Message text'

        @allure.description('Can change the password')
        def test_change_password(self, register_user, auth_user):
            # CHANGE PASSWORD
            post_response, new_password = self.api_user.change_password(
                self.token, current_password=register_user.password
            )
            assert post_response.success is True, 'Check the Success'
            assert post_response.status == 200, 'Check the Status'
            assert post_response.message == UsersMessages.PASSWORD_UPDATED, 'Check the Message text'
            # LOGOUT
            self.api_user.logout_user(self.token)
            # CHECK IF USER CAN LOG IN WITH NEW PASSWORD
            self.api_user.login_user(email=register_user.email, password=new_password)
