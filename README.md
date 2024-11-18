# Foodgram - Продуктовый помощник!!!

## Описание проекта
Приложение в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов,
необходимых для приготовления выбранных блюд!

Проект доступен по адресу - <a href="http://51.250.23.36">51.250.23.36</a>

### Для реализации проекта используются:

- __Python__
- __Django__
- __Django Rest Framework__
- __Gunicorn__
- __NGINX__
- __PostgreSQL__
- __Docker__

### Запуск проекта:

Клонировать репозиторий:
```
https://github.com/AndrejGurtovoj/foodgram-project-react.git
```
__Запустить проект в контейнерах Docker:__

перейти в каталог **`infra`** и создать файл **`.env`**:
```
cd infra
touch .env
```
запонить его данными:
```
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs

```
Выполнить команду:
```
sudo docker-compose up -d --build
```
Сделать миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
sudo compose exec backend python manage.py createsuperuser
```
Собрать статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Заполненить базу данными:
```
sudo docker compose exec backend python manage.py load_ingredients
```
```
sudo docker compose exec backend python manage.py load_tags
```
```
sudo docker compose exec backend python manage.py dumpdata > dump.json
```
После запуска проект будет доступен по адресу:  <a href="http://51.250.23.36">51.250.23.36</a>

#### Автор проекта:  <a href= "https://github.com/AndrejGurtovoj">__Андрей Гуртовой__<a>
