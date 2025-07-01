from config.config import BASE_URL


class NotesEndpoints:
    create_new_note = f'{BASE_URL}/notes'
    get_all_notes = f'{BASE_URL}/notes'
    get_note_by_id = lambda note_id: f'{BASE_URL}/notes/{note_id}'
    update_note_by_id = lambda note_id: f'{BASE_URL}/notes/{note_id}'
    update_note_status = lambda note_id: f'{BASE_URL}/notes/{note_id}'
    delete_note_by_id = lambda note_id: f'{BASE_URL}/notes/{note_id}'

