from config.config import BASE_URL


class UsersEndpoints:
    create_user = f'{BASE_URL}/users/register'
    login_user = f'{BASE_URL}/users/login'
    get_user_profile = f'{BASE_URL}/users/profile'
    update_user_profile = f'{BASE_URL}/users/profile'
    send_password_reset_link = f'{BASE_URL}/users/forgot-password'
    reset_password = f'{BASE_URL}/users/reset-password'
    change_password = f'{BASE_URL}/users/change-password'
    logout_user = f'{BASE_URL}/users/logout'
    delete_user = f'{BASE_URL}/users/delete-account'
