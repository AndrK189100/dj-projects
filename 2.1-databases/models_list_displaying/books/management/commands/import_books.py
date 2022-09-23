from django.core.management.base import BaseCommand
from books.models import Book
from main.settings import BASE_DIR
import pathlib
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        path = pathlib.Path(BASE_DIR, 'fixtures', 'books.json')
        with open(path, encoding='UTF-8') as file:
            books = json.load(file)
            for book in books:
                Book.objects.create(name=book['fields']['name'],
                                    author=book['fields']['author'],
                                    pub_date=book['fields']['pub_date'])
