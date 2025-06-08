

class UsersMessages:
    ACCOUNT_CREATED = 'User account created successfully'
    ACCOUNT_ALREADY_EXISTS = 'An account already exists with the same email address'
    ACCOUNT_DELETED = 'Account successfully deleted'
    LOGIN_SUCCESSFUL = 'Login successful'
    GET_PROFILE_SUCCESSFUL = 'Profile successful'
    PROFILE_UPDATED = 'Profile updated successful'
    NO_TOKEN = 'No authentication token specified in x-auth-token header'
    TOKEN_NOT_VALID = 'Access token is not valid or has expired, you will need to login'
    LOGOUT_SUCCESSFUL = 'User has been successfully logged out'
    PASSWORD_RESET_LINK_SENT = lambda email: (f'Password reset link successfully sent to {email}. '
                                              f'Please verify by clicking on the given link')
    PASSWORD_UPDATED = 'The password was successfully updated'
    NAME_ERROR = 'User name must be between 4 and 30 characters'
    EMPTY_EMAIL = 'A valid email address is required'
    PASSWORD_ERROR = 'Password must be between 6 and 30 characters'
    WRONG_CREDENTIALS = 'Incorrect email address or password'
    INTERNAL_SERVER_ERROR = 'Internal Error Server'
