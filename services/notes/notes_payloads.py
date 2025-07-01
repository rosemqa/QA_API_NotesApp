import random

from faker import Faker

fake = Faker()


class NotesPayloads:
    @staticmethod
    def create_note():
        return {
            'title': fake.word() + 'c',
            'description': fake.sentence(),
            'category': random.choice(['Home', 'Work', 'Personal'])
        }

    @staticmethod
    def update_note():
        return {
            'title': fake.word() + 'v',
            'description': fake.sentence(),
            'category': random.choice(['Home', 'Work', 'Personal']),
            'completed': random.choice([True, False])
        }
