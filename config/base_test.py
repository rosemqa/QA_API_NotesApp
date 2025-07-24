from services.notes.notes_api import NotesAPI
from services.users.users_api import UserAPI


class BaseTest:
    def setup_method(self):
        self.api_user = UserAPI()
        self.api_notes = NotesAPI()
