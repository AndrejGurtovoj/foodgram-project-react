# Foodgram - Продуктовый помощник!!!

![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
![example workflow](https://github.com/AndrejGurtovoj/foodgram_backend/actions/workflows/foodgram_workflow.yml/badge.svg)
## Описание проекта
Приложение в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов,
необходимых для приготовления выбранных блюд.

Проект доступен по адресу - <a href="http://84.201.136.72">84.201.136.72</a>

### Используемые технологии:

- __Python__
- __Django__
- __Django Rest Framework__
- __Gunicorn__
- __NGINX__
- __PostgreSQL__
- __Docker__

### Как развернуть проект:

Клонировать репозиторий:
```
https://github.com/AndrejGurtovoj/foodgram-project-react.git
```
__Запустить проект в контейнерах Docker:__

перейти в каталог **`infra`** и создать файл **`.env`**:
```angular2html
cd infra
touch .env
```
запонить его данными:
```angular2html
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dd3402cd
DB_HOST=db
DB_PORT=5432
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs

```

Выполнить команду:
```
docker-compose up -d
```
Сделать миграции:
```
docker-compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
docker-compose exec bakend python manage.py createsuperuser
```
Собрать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
заполненить базу данными:
```angular2html
docker-compose exec backend python manage.py loaddata dump.json
```
__После запуска проект будут доступен по адресу: http://localhost:81/__

#### Автор проекта:  <a href= "https://github.com/AndrejGurtovoj">__Андрей Гуртовой__<a>
