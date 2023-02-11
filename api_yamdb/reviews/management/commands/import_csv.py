import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import (Category, Comment,
                            Genre, GenreTitle,
                            Review, Title, User)


class Command(BaseCommand):
    """Команда для заполнения базы данных путем импорта из csv-файла."""
    CSV_FILES = (
        (User, 'users.csv'),
        (Category, 'category.csv'),
        (Genre, 'genre.csv'),
        (Title, 'titles.csv'),
        (GenreTitle, 'genre_title.csv'),
        (Review, 'review.csv'),
        (Comment, 'comments.csv'),
    )

    def handle(self, *args, **options):
        for model, file_name in self.CSV_FILES:
            print(f'Loading data for {model}')
            csv_reader = csv.DictReader(
                open(f'static/data/{file_name}', encoding='utf-8')
            )
            for row in csv_reader:
                row_copy = row.copy()
                for field_name in row_copy.keys():
                    if field_name == 'author':
                        row['author_id'] = row.pop('author')
                    elif field_name == 'category':
                        row['category_id'] = row.pop('category')
                try:
                    model.objects.create(**row)
                except Exception as error:
                    raise CommandError(
                        f'Ошибка: {error}, файл {file_name}, строка {row}'
                    )
            print(f'Loaded data for {model}')
