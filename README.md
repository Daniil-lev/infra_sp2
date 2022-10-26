# API_YAMDB
REST API проект для сервиса YaMDb — сбор отзывов о фильмах, книгах или музыке.
## Краткое описание
Групповой проект по разработке сервиса отзывов пользователя

### Стек
REST API, Docker, PostgreSQL


### Как запустить проект:

```
git clone https://github.com/daniilev/infra_sp2
cd infra_sp2
cd api_yamdb
```

Поднимаем контейнеры :
```
docker-compose up -d --build
```

Выполняем миграции:

```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

Србираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

Создаем дамп базы данных (нет в текущем репозитории):
```
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

Останавливаем контейнеры:
```
docker-compose down -v
```

### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
