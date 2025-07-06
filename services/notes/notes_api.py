import allure
import responses
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

    @allure.step('Create note with specific data')
    def create_note_with_specific_data(self, token: str, field: str, value):
        payload = self.payloads.create_note()
        payload[field] = value
        response = MyRequests.post(
            url=self.endpoints.create_new_note,
            json=payload,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Create a note without auth header')
    def create_note_without_auth_header(self):
        response = MyRequests.post(
            url=self.endpoints.create_new_note,
            json=self.payloads.create_note(),
        )
        assert response.status_code == 401, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Returns 500 internal server error for "create note" request')
    @responses.activate
    def create_note_with_internal_server_error(self, token):
        responses.add(
            method=responses.POST,
            url=self.endpoints.create_new_note,
            json={
                "success": False,
                "status": 500,
                "message": "Internal Error Server"
            },
            status=500
        )
        response = MyRequests.post(
            url=self.endpoints.create_new_note,
            json=self.payloads.create_note(),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 500, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

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

    @allure.step('Get a note with non-existent note id')
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

    @allure.step('Update note by non-existent note id')
    def update_note_by_non_existent_id(self, token: str):
        note_id = '68684aaf7691270289f2bdcb'
        response = MyRequests.put(
            url=self.endpoints.update_note_by_id(note_id),
            json=self.payloads.update_note(),
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 404, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

    @allure.step('Update a note without filling in the required field')
    def update_note_with_empty_required_field(self, token: str, note_id: str, field: str):
        payload = self.payloads.update_note()
        payload[field] = ''
        response = MyRequests.put(
            url=self.endpoints.update_note_by_id(note_id),
            json=payload,
            headers=self.headers.auth_token(token)
        )
        assert response.status_code == 400, f'{response.status_code}, {response.content.decode("utf-8")}'
        self.attach_response(response)
        model = BaseResponseModel(**response.json())
        return model

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
