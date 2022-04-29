# Foodgram

[![CI](https://github.com/8ubble8uddy/foodgram-project-react/workflows/foodgram-project-react/badge.svg
)](https://github.com/8ubble8uddy/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

### **Адрес**

**https://foodgram.ddnsking.com/** _(сайт временно недоступен)_

### **Описание**

_[foodgram-project-react](https://github.com/8ubble8uddy/foodgram-project-react) - это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд._

### **Технологии**

```Python``` ```Django```  ```React``` ```PostgreSQL``` ```Docker``` ```Gunicorn``` ```nginx```

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него в директорию ```infra/local/```:
```
git clone https://github.com/8ubble8uddy/foodgram-project-react.git
```
```sh
cd foodgram-project-react/infra/local/
```

Создать файл .env и добавить настройки подключения к базе данных:
```sh
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Развернуть и запустить проект в контейнерах:
```
docker-compose up -d --build
```

Внутри контейнера ```backend```:

- _Выполнить миграции_
  ```
  docker-compose exec backend python manage.py migrate
  ```
- _Создать суперпользователя_
  ```
  docker-compose exec backend python manage.py createsuperuser
  ```
- _Собрать статику_
  ```
  docker-compose exec backend python manage.py collectstatic --no-input
  ```
- _Заполнить базу данных_
  ```
  docker-compose exec backend python manage.py loaddata static/fixtures.json
  ```

**Проект будет доступен по адресу http://127.0.0.1/**

### Автор: Герман Сизов