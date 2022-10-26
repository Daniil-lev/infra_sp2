from csv import DictReader

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Load data from static/data/*.csv files into database'

    # Категории
    def load_categories(self):
        with open(
            './static/data/category.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            try:
                i = 0
                for row in DictReader(csv_file):
                    category = Category(
                        pk=row['id'],
                        name=row['name'],
                        slug=row['slug'])
                    category.save()
                    i += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Загружено {i} строк объектов категории'))
            except Exception:
                raise CommandError('Невозможно загрузить данные категорий')

        # Жанры
    def load_genres(self):
        with open(
            './static/data/genre.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            try:
                i = 0
                for row in DictReader(csv_file):
                    genre = Genre(
                        pk=row['id'],
                        name=row['name'],
                        slug=row['slug'])
                    genre.save()
                    i += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Загружено {i} строк объектов жанры'))
            except Exception:
                raise CommandError('Невозможно загрузить данные жанров')

        # Произведения
    def load_titles(self):
        with open(
            './static/data/titles.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            try:
                i = 0
                for row in DictReader(csv_file):
                    title = Title(
                        pk=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category']
                    )
                    title.save()
                    i += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Загружено {i} произведений'))
            except Exception:
                raise CommandError('Невозможно загрузить произведения')

        # Произведения и жанры -- многие ко многим.
    def load_genre_titles(self):
        with open(
            './static/data/genre_title.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            i = 0
            for row in DictReader(csv_file):
                title = Title.objects.get(
                    pk=row['title_id']
                )
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)
                title.save()
                i += 1
            self.stdout.write(self.style.SUCCESS(
                f'Загружено {i} жанров произведений'))

        # Пользователи

    def load_users(self):
        with open(
            './static/data/users.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            i = 0
            for row in DictReader(csv_file):
                user = User(
                    pk=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']

                )
                user.save()
                i += 1
            self.stdout.write(self.style.SUCCESS(
                f'Загружено {i} пользователей'))

        # Обзоры

    def load_reviews(self):
        with open(
            './static/data/review.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            i = 0
            try:
                for row in DictReader(csv_file):
                    title = Review(
                        pk=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                    title.save()
                    i += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Загружено {i} обзоров'))
            except Exception:
                raise CommandError('Невозможно загрузить обзоры')

        # Комментарии
    def load_comments(self):
        with open(
            './static/data/comments.csv', mode="r", encoding="utf-8"
        ) as csv_file:
            i = 0
            try:
                for row in DictReader(csv_file):
                    comment = Comment(
                        pk=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author_id=row['author'],
                        pub_date=row['pub_date'],
                    )
                    comment.save()
                    i += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Загружено {i} комментариев'))
            except Exception:
                raise CommandError('Невозможно загрузить комментарии')

    def handle(self, *args, **options):
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_genre_titles()
        self.load_users()
        self.load_reviews()
        self.load_comments()
