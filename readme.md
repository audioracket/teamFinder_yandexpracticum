# TeamFinder: Платформа для поиска единомышленников в pet-проекты. 
TeamFinder помогает разработчикам находить единомышленников для совместной работы над проектами. Пользователи могут создавать проекты, указывать необходимые навыки, находить подходящих участников и присоединяться к чужим проектам.
## Функциональность

- Регистрация и авторизация по email
- Создание, редактирование и завершение проектов
- Фильтрация проектов по навыкам
- Присоединение к проектам
- Профили пользователей с аватаром, контактами и GitHub
- Автодополнение при добавлении навыков к проекту
- Поделиться ссылкой на проект или профиль
## Технологии
- Python 3.10, Django 4.2
- PostgreSQL
- Docker, Docker Compose
- Gunicorn, Pytest, Flake8
## Запуск проекта
### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/audioracket/teamFinder_yandexpracticum.git
cd teamFinder_yandexpracticum
```
### 2. Создайте файл .env
Скопируйте пример и заполните значения:

```bash
cp .env_example .env
```
Содержимое .env:
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=teamfinder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш-пароль
DB_HOST=db
DB_PORT=5432

### 3. Запустите через Docker Compose

```bash
docker compose up -d --build
```

Проект будет доступен по адресу: http://localhost:8000

### 4. Создайте суперпользователя (опционально)

```bash
docker compose exec backend python manage.py createsuperuser
```

#### Автор
Сергей — [GitHub](https://github.com/audioracket)