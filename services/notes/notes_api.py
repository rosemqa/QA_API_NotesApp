import allure

from config.config import Headers
from models.base_model import BaseResponseModel
from models.notes_model import NoteModel, NoteListModel
from services.notes.notes_endpoints import NotesEndpoints
from services.notes.notes_payloads import NotesPayloads
from utils.helper import Helper
from utils.my_requests import MyRequests


class NotesAPI(Helper):
    def __init__(self):
        self.endpoints = NotesEndpoints
        self.payloads = NotesPayloads()
        self.headers = Headers

    @allure.step('Create a new note')
    def create_new_note(self, token: str):
        payload = self.payloads.create_note()
        response = MyRequests.post(
            url=self.endpoints.create_new_note,
            json=payload,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = NoteModel(**response.json())
        return model, payload

    @allure.step('Get note by note ID')
    def get_note_by_id(self, token: str, note_id: str):
        response = MyRequests.get(
            url=self.endpoints.get_note_by_id(note_id),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = NoteModel(**response.json())
        return model

    @allure.step('Get a list of all user notes')
    def get_all_notes(self, token: str):
        response = MyRequests.get(
            url=self.endpoints.get_all_notes,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = NoteListModel(**response.json())
        return model

    def get_not_existed_note(self, token: str, note_id: str):
        response = MyRequests.get(
            url=self.endpoints.get_note_by_id(note_id),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 404, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Update note by its ID')
    def update_note_by_id(self, token: str, note_id: str):
        payload = self.payloads.update_note()
        response = MyRequests.put(
            url=self.endpoints.update_note_by_id(note_id),
            json=payload,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = NoteModel(**response.json())
        return model, payload

    @allure.step('Edit the completed status of a note with the specified id')
    def update_note_status(self, token: str, note_id: str, status: bool):
        response = MyRequests.patch(
            url=self.endpoints.update_note_status(note_id),
            json={'completed': status},
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = NoteModel(**response.json())
        return model

    @allure.step('Delete note by id')
    def delete_note_by_id(self, token: str, note_id: str):
        response = MyRequests.delete(
            url=self.endpoints.delete_note_by_id(note_id),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 200, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model


