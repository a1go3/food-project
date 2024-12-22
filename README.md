### Сервис для публикаций и обмена рецептами.

### Возможности сервиса:
- делитесь своими рецептами
- смотрите рецепты других пользователей
- добавляйте рецепты в избранное
- быстро формируйте список покупок, добавляя рецепт в корзину
- следите за своими друзьями и коллегами

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в список покупок (с возможностью его скачать). 
Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

### Технологии:
- Django
- Python
- Docker
- Nginx

## Подготовка и запуск проекта.
### Для работы с локальным сервером.

* Склонируйте репозиторий: 

```
git clone https://github.com/tatarenkov-r-v/food-project.git
```
* Cоберите образы foodgram_frontend, foodgram_backend 
и foodgram_gateway (образ nginx с конфигом для управления проектом):
```
docker compose up   
```
* Соберите статику Django:
```
docker compose exec backend python manage.py collectstatic
```
* Скопируйте статику в /backend_static/static:
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
* Выполните миграции:
```
docker compose exec backend python manage.py migrate
``` 
* Загрузите в базу данных информацию об ингридиентах (по желанию):
```
docker compose exec backend python manage.py load_data
``` 
* Проект будет доступен по адресу:
```
http://localhost:8000/
```

## Для работы с удаленным сервером на Ubuntu:

* Выполните вход на свой удаленный сервер

*  Установите docker и docker-compose на сервере:
```
sudo apt install docker.io 
sudo apt install docker-compose
```

* Создайте папку для проекта на сервере:
```
mkdir foodgram
```

* Создайте .env файл в папке проекта указав:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    ALLOWED_HOSTS=<список хостов/доменов>
    ```
* Скопируйте из корня проекта файл docker-compose.production.yml в папку foodgram на сервере

* Находясь в папке foodgram последовательно выполните команды:
```
   sudo docker compose -f docker-compose.production.yml up -d
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
   sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/.
```
* Загрузите данные ингредиентов в базу данных (по желанию):
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_data
```
* Создайте superuser-a:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```
