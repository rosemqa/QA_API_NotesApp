

BASE_URL = 'https://practice.expandtesting.com/notes/api'


class Headers:
    auth_token = lambda token: {'x-auth-token': token}
