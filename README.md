# FOODGRAM
_Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд_

## Технологии
- Python 3.9.13
- Django 4.1.7
- Django REST framework 3.14
- Nginx 1.19.3
- Postgres 13.0

## Инструкции по запуску
- склонировать репозиторий
```
git clone git@github.com:tsurik1/foodgram-project-react.git
```
- подключиться к серверу
- установить docker, docker-compose на сервере
```
sudo apt install docker.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- скопировать файлы docker-compose.yml и nginx.conf на сервер
```
cp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml

cp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

- создать .env файл на сервере и добавить в него настройки:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- запустить сборку контейнеров
```
sudo docker-compose up -d
```

- создать миграции, суперюзера, собрать статику, заполнить бд ингредиентами и тегами
```
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py createsuperuser

docker-compose exec backend python manage.py collectstatic --no-input 

docker-compose exec backend python manage.py import_json
```

### Публичный IP
http://158.160.52.188

### админка
- login: admin3@mail.ru
- password: admin12345434

# Автор
https://github.com/tsurik1