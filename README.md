## API LMS (Система управления обучением) [(Version in English)](README_EN.md)
**Backend-часть веб-приложения для обучения.**
- Подписка на курсы
- Просмотр, добавление своих и редактирование курсов и уроков
- Оплата через Stripe
### Стек технологий:
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.4-blue?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15.1-blue)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.4.0-blue?logo=Celery)](https://docs.celeryq.dev/en/stable/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-5.0.4-blue?logo=Redis)](https://redis.io/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![stripe](https://img.shields.io/badge/Stripe-9.3.0-blue?style=flat-square&logo=stripe)](https://stripe.com/)

- `python`
- `django`
- `djangorestframework`
- `celery`
- `celery-beat`
- `postgreSQL`
- `redis`
- `docker`
- `stripe`

## Содержание

<details>
<summary>Инструкция по развертыванию проекта</summary>

#### 1. Клонируйте проект:
```
git clone https://github.com/MSk1901/habits.git
```
#### 2. Перейдите в корневую директорию проекта 
#### 3. Настройте переменные окружения: 

   1. Создайте файл `.env` в корневой директории 
   2. Скопируйте в него содержимое файла `.env.sample` и подставьте свои значения
   3. Для корректной работы проекта в локальной среде разработки установите значение `DEBUG=True`, чтобы обеспечить автоматическую обработку статических файлов и подробные сообщения об ошибках.


#### 4. Запустите команду для сборки и запуска контейнеров Docker:
```
docker-compose up -d --build
```
</details>

<details>
<summary>Использование</summary>

#### 1. Административная панель:
Для доступа к админке создайте суперпользователя

1. Для этого нужно будет посмотреть список запущенных контейнеров и скопировать id контейнера app
    ```
    docker ps
    ```
    Пример вывода:
    ```
    CONTAINER ID   IMAGE                                                         
    e5e38dccec3d   drf-lms-app                
    ```
2. После этого выполните команду, чтобы попасть в контейнер и выполнять команды, доступные в его окружении
    ```
    docker exec -it <id контейнера> bash
    ```
3. Для создания суперпользователя (админа) выполните команду
    ```
    python3 manage.py csu
    ```
   E-mail и пароль суперпользоветеля для входа в админку вы можете посмотреть в файле `/users/management/commands/csu.py`. При желании, вы можете задать свои e-mail и пароль


4. Откройте администратичную панель по адресу http://localhost:8000/admin/ и введите e-mail и пароль суперпользоветеля

    
#### 2. Регистрация пользователя:
1. Регистрация пользователя доступна на эндпоинте http://localhost:8000/users/
2. Отправьте POST-запрос c e-mail и паролем в теле запроса, например
    ```
    {
        "email": "user@example.com",
        "password": "Somepassword"
    }
    ```
#### 3. Аутентификация пользователя:
1. Аутентификация пользователя доступна на эндпоинте http://localhost:8000/users/login/
2. Отправьте POST-запрос c e-mail и паролем созданного ранее пользователя в теле запроса
3. В теле ответа вы получите Bearer token для дальнейшей аутентификации
    ```
    {
        "refresh": "eyJhbGciOiJIUzI",
        "access": "eyJhbGciOiJIUzI1"
    }
    ```
   Скопируйте access токен
#### 4. Создание сущностей:
! Обратите внимание. Управление сущностями доступно только аутентифицированным пользователям. 

Bearer token передается в заголовке запроса. Чтобы его указать, можно:
- использовать сторонне приложение для взаимодействия с API, например `Postman`
- авторизоваться через `swagger` по кнопке `Authorize`

Значение токена указывается в формате `Bearer <значение токена>`
1. Создание курса с уроками  
Доступно по эндпоинту http://localhost:8000/course/ (Метод POST)  
Пример тела запроса:
    ```
    {
        "title": "Django",
        "description": "Курс по Django",
        "lessons": [
                       {
                           "title": "Урок 1. Введение",
                           "description": "Что такое Django",
                           "video_url": "https://www.youtube.com/watch?v=L-FyeHQwo4U&",
                       }
                   ]
    }
    ```
   В рамках этого проекта настроена валидация прикрепляемых ссылок в `video_url`. Можно указывать ссылки только на Youtube


2. Создание оплаты Stripe  
Доступно по эндпоинту http://localhost:8000/users/payment/ (Метод POST)  
Пример тела запроса:
    ```
    {
        "amount": 10000, # указывается целое значение (рубли)
        "method": "card",
        "course_subject": 1 # id курса для оплаты
    }
    ```
    Можно создать оплату на курс или отдельный урок, указав либо `course_subject`, либо `lesson_subject`  
В теле ответа придет ссылка на оплату через Stripe, где можно будет ввести данные карты
     
#### 5. Другие способы взаимодействия:
Все способы взаимодействия вы можете найти в документации
</details>

## Документация
Документация по API доступна по адресам:
- Swagger - http://localhost:8000/swagger/
- Redoc - http://localhost:8000/redoc/



Автор проекта Мария Кузнецова - [kuznetsova19.m@gmail.com](mailto:kuznetsova19.m@gmail.com)
