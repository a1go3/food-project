# Учебный проект FoodGram.
### Сервис для публикаций и обмена рецептами.
#### Сервис доступен по адресу:
```
https://foodgrammproject.hopto.org/
```

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

## Подготовка и запуск проекта
### Склонировать репозиторий: 
```
git clone https://github.com/tatarenkov-r-v/foodgram-project-react.git
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
    ```
  
* Скопируйте из корня проекта файл docker-compose.production.yml в папку foodgram на сервере


* Находясь в папке foodgram последовательно выполните комманды:
```
   sudo docker compose -f docker-compose.production.yml up -d
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_data
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
   sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/.
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

