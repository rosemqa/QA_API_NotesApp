import random
import allure
import pytest
from config.base_test import BaseTest
from services.notes.notes_constants import NotesMessages
from services.users.users_constants import UsersMessages
from utils.fakers import fake
from datetime import datetime, timedelta
from datetime import timezone


@allure.epic('Notes')
class TestNotes:
    @allure.feature('Create note')
    class TestCreateNote(BaseTest):
        @allure.description('Can create a new note')
        def test_create_new_note(self, check, register_user, auth_user, delete_new_user):
            note, note_data = self.api_notes.create_new_note(token=self.token)

            now = datetime.now(timezone.utc)
            created_at = note.data.created_at
            delta = abs(now - created_at)

            with check:
                assert note.success is True, 'Check the Success'
                assert note.status == 200, 'Check the Status'
                assert note.message == NotesMessages.NOTE_CREATED, 'Check the Message text'
            with check:
                assert note.data.title == note_data['title'], 'Check the note title'
            with check:
                assert note.data.description == note_data['description'], 'Check the note description'
            with check:
                assert note.data.completed is False, 'Check the Completed'
            with check:
                assert delta < timedelta(seconds=5), 'Created_at is very different from the current time'
            with check:
                assert note.data.category == note_data['category'], 'Check the note category'
            with check:
                assert note.data.user_id == register_user.user_id, 'Check the user ID'

        @allure.description('Unable to create note if any of the required fields are empty')
        @allure.tag('negative')
        @pytest.mark.parametrize('empty_field, error_message', [
            ('title', NotesMessages.TITLE_ERROR),
            ('description', NotesMessages.DESCRIPTION_ERROR),
            ('category', NotesMessages.CATEGORY_ERROR)
        ])
        def test_create_note_with_empty_required_field(self, auth_user, delete_new_user, empty_field, error_message):
            note = self.api_notes.create_note_with_specific_data(token=self.token, field=empty_field, value='')

            assert note.success is False, 'Check the Success'
            assert note.status == 400, 'Check the Status'
            assert note.message == error_message, 'Check the Message text'
            print(note.json())

        @allure.description('Unable to create note with a title shorter than 4 symbols or longer than 100 symbols')
        @allure.tag('negative')
        @pytest.mark.parametrize('title_text', ['long_title', 'short_title'])
        def test_create_note_with_too_short_or_long_title(self, auth_user, delete_new_user, title_text):
            if title_text == 'long_title':
                note = self.api_notes.create_note_with_specific_data(
                    token=self.token, field='title',
                    value=fake.long_note_title()
                )
            else:
                note = self.api_notes.create_note_with_specific_data(
                    token=self.token,
                    field='title',
                    value=fake.short_note_title()
                )
            assert note.message == NotesMessages.TITLE_ERROR, 'Check the Message text'

        @allure.description('Unable to create a note as unauthorized user')
        def test_create_note_without_auth_header(self):
            note = self.api_notes.create_note_without_auth_header()

            assert note.success is False, 'Check the Success'
            assert note.status == 401, 'Check the Status'
            assert note.message == UsersMessages.NO_TOKEN, 'Check the Message text'

        @allure.description('Check for 500 internal server error for "create note" request')
        def test_create_note_returns_500(self, auth_user, delete_new_user):
            error = self.api_notes.create_note_with_internal_server_error(token=self.token)

            assert error.success is False, 'Check the Success'
            assert error.status == 500, 'Check the Status'
            assert error.message == UsersMessages.INTERNAL_SERVER_ERROR, 'Check the Message text'

    @allure.feature('Get note/notes')
    class TestGetNote(BaseTest):
        @allure.description('Can get the note by note ID for authed user')
        def test_get_note_by_id(self, check, register_user, auth_user, create_note, delete_new_user):
            get_note = self.api_notes.get_note_by_id(token=self.token, note_id=create_note.data.id)

            with check:
                assert get_note.success is True, 'Check the Success'
                assert get_note.status == 200, 'Check the Status'
                assert get_note.message == NotesMessages.NOTE_RETRIEVED, 'Check the Message text'
            with check:
                assert get_note.data.id == create_note.data.id, 'Check the note ID'
            with check:
                assert get_note.data.title == create_note.data.title, 'Check the note title'
            with check:
                assert get_note.data.description == create_note.data.description, 'Check the note description'
            with check:
                assert get_note.data.completed == create_note.data.completed, 'Check the Completed'
            with check:
                assert get_note.data.created_at == create_note.data.created_at, 'Check the Created_at'
                assert get_note.data.updated_at == create_note.data.updated_at, 'Check the Updated_at'
            with check:
                assert get_note.data.category == create_note.data.category, 'Check the note category'
            with check:
                assert get_note.data.user_id == create_note.data.user_id, 'Check the user ID'

        @allure.description('Can get the list of all notes of the authed user')
        def test_get_all_notes(self, auth_user, delete_new_user):
            # CREATE A FEW NOTES AND GET THEIR IDS
            notes_quantity = random.randint(2, 2)
            notes_ids = []
            for _ in range(notes_quantity):
                note = self.api_notes.create_new_note(token=self.token)[0]
                notes_ids.append(note.data.id)

            # GET THE NOTE LIST
            note_list = self.api_notes.get_all_notes(token=self.token)

            assert len(note_list.data) == notes_quantity, 'Check the number of notes in the list'
            assert sorted(notes_ids, reverse=True) == [note.id for note in note_list.data], \
                'Created notes are not in the list'

    @allure.feature('Update note')
    class TestUpdateNote(BaseTest):
        @allure.description('Can edit note for authed user')
        def test_update_note(self, check, auth_user, create_note, delete_new_user):
            note, updated_data = self.api_notes.update_note_by_id(token=self.token, note_id=create_note.data.id)

            with check:
                assert note.success is True, 'Check the Success'
                assert note.status == 200, 'Check the Status'
                assert note.message == NotesMessages.NOTE_UPDATED, 'Check the Message text'
            with check:
                assert note.data.title == updated_data['title'], 'Check the note title'
            with check:
                assert note.data.description == updated_data['description'], 'Check the note description'
            with check:
                assert note.data.completed == updated_data['completed'], 'Check the Completed'
            with check:
                assert note.data.category == updated_data['category'], 'Check the note category'

        @allure.description('Unable to create a note by non-existent note id')
        @allure.tag('negative')
        def test_update_note_by_non_existent_id(self, auth_user, delete_new_user):
            note = self.api_notes.update_note_by_non_existent_id(token=self.token)

            assert note.message == NotesMessages.NO_NOTE_WITH_PROVIDED_ID, 'Check the Message text'

        @allure.description('Unable to update note if any of the required fields are empty')
        @pytest.mark.parametrize('empty_field, error', [
            ('title', NotesMessages.TITLE_ERROR),
            ('description', NotesMessages.DESCRIPTION_ERROR),
        ])
        def test_edit_note_with_empty_required_field(self, auth_user, create_note, delete_new_user, empty_field, error):
            note_id = create_note.data.id
            note = self.api_notes.update_note_with_empty_required_field(
                token=self.token,
                note_id=note_id,
                field=empty_field
            )
            assert note.message == error, 'Check the Message text'

        @allure.description('Can change the completed status of a note between True/False')
        def test_update_note_status(self, auth_user, create_note, delete_new_user):
            status_true = self.api_notes.update_note_status(
                token=self.token,
                note_id=create_note.data.id,
                status=True
            )
            assert status_true.data.completed is True, 'Status is not changed to True'

            status_false = self.api_notes.update_note_status(
                token=self.token,
                note_id=create_note.data.id,
                status=False
            )
            assert status_false.data.completed is False, 'Status is not changed to False'

    @allure.feature('Delete note')
    class TestDeleteNote(BaseTest):
        @allure.description('Can delete note by its ID for authed user')
        def test_delete_note_by_id(self, auth_user, create_note, delete_new_user):
            note_id = create_note.data.id
            # DELETE NOTE
            note = self.api_notes.delete_note_by_id(token=self.token, note_id=note_id)

            assert note.success is True, 'Check the Success for Deleted method'
            assert note.status == 200, 'Check the Status for Deleted method'
            assert note.message == NotesMessages.NOTE_DELETED, 'Check the Message text for Deleted method'

            # VALIDATE THAT THE NOTE WAS DELETED FROM THE NOTE LIST
            note_list = self.api_notes.get_all_notes(token=self.token)
            assert note_list.message == NotesMessages.NO_NOTES_FOUND, 'Check the Message text for GET all notes method'
            assert note_list.data == [], 'Note list is not empty'

            # VERIFY THAT NOTE INFORMATION DOESN'T RETURN
            get_note = self.api_notes.get_not_existed_note(token=self.token, note_id=note_id)

            assert get_note.success is False, 'Check the Success for GET note by ID method'
            assert get_note.status == 404, 'Check the Status for GET note by ID method'
            assert get_note.message == NotesMessages.NO_NOTE_WITH_PROVIDED_ID, \
                'Check the Message text for GET note by ID method'
