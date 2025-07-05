from faker import Faker


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def long_note_title(self):
        """Returns a title longer than 100 characters."""
        return ''.join(self.faker.random_letters(length=101)).title()

    def short_note_title(self):
        """Returns a title shorter than 4 characters."""
        return ''.join(self.faker.random_letters(length=3)).title()


fake = Fake(faker=Faker())
