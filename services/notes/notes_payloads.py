import random

from faker import Faker

fake = Faker()


class NotesPayloads:
    @staticmethod
    def create_note():
        title = fake.word()
        if len(title) < 4:
            title += 'ab'
        return {
            'title': title,
            'description': fake.sentence(),
            'category': random.choice(['Home', 'Work', 'Personal'])
        }

    @staticmethod
    def update_note():
        title = fake.word()
        if len(title) < 4:
            title += 'ab'
        return {
            'title': title,
            'description': fake.sentence(),
            'category': random.choice(['Home', 'Work', 'Personal']),
            'completed': random.choice([True, False])
        }
