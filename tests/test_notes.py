import random
import allure
from config.base_test import BaseTest
from services.notes.notes_constants import NotesMessages


class TestNotes(BaseTest):
    @allure.description('Can create a new note')
    def test_create_new_note(self, check, register_user, auth_user, delete_new_user):
        note, note_data = self.api_notes.create_new_note(token=self.token)

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
            assert note.data.category == note_data['category'], 'Check the note category'
        with check:
            assert note.data.user_id == register_user.user_id, 'Check the user ID'

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
