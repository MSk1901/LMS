## API LMS (Learning Management System)
**Backend part of the e-learning web application.**
- Course subscription
- Viewing, adding own, and editing courses and lessons
- Payment via Stripe
### Technology Stack:
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

## Table of Contents

<details>
<summary>Deployment Guide</summary>

#### 1. Clone the project:
```
git clone https://github.com/MSk1901/LMS.git
```
#### 2. Navigate to the project root directory
#### 3. Set up environment variables:

   1. Create a file named `.env` in the root directory
   2. Copy the contents of the `.env.sample` file into it and replace the values with your own
   3. For the project to work correctly in the local development environment, set the value of `DEBUG=True` to automatically handle static files and provide detailed error messages.


#### 4. Run the command to build and start Docker containers:
```
docker-compose up -d --build
```
</details>

<details>
<summary>Usage</summary>

#### 1. Admin Panel:
To access the admin panel, create a superuser

1. You will need to view the list of running containers and copy the container id of the app container
    ```
    docker ps
    ```
    Example output:
    ```
    CONTAINER ID   IMAGE                                                         
    e5e38dccec3d   drf-lms-app                
    ```
2. Then execute the command to enter the container and execute commands available in its environment
    ```
    docker exec -it <container id> bash
    ```
3. To create a superuser (admin), execute the command
    ```
    python3 manage.py createsuperuser
    ```
   You can view the superuser's email and password for logging into the admin panel in the `/users/management/commands/csu.py` file. If desired, you can set your own email and password.


4. Open the administrative panel at http://localhost:8000/admin/ and enter the email and password of the superuser

    
#### 2. User Registration:
1. User registration is available at the endpoint http://localhost:8000/users/
2. Send a POST request with an email and password in the request body, for example
    ```
    {
        "email": "user@example.com",
        "password": "Somepassword"
    }
    ```
#### 3. User Authentication:
1. User authentication is available at the endpoint http://localhost:8000/users/login/
2. Send a POST request with the email and password of the previously created user in the request body
3. In the response body, you will receive a Bearer token for further authentication
    ```
    {
        "refresh": "eyJhbGciOiJIUzI",
        "access": "eyJhbGciOiJIUzI1"
    }
    ```
   Copy the access token
#### 4. Entity Creation:
! Note. Entity management is available only to authenticated users.

The Bearer token is passed in the request header. To specify it, you can:
- use a third-party application to interact with the API, such as `Postman`
- authenticate through `swagger` by clicking the `Authorize` button

The token value is specified in the format `Bearer <token value>`
1. Course with lessons creation  
Available at the endpoint http://localhost:8000/courses/ (POST method)  
Example request body:
    ```
    {
        "title": "Django",
        "description": "Django Course",
        "lessons": [
                     {
                       "title": "Lesson 1. Introduction",
                       "description": "What is Django",
                       "video_url": "https://www.youtube.com/watch?v=L-FyeHQwo4U&",
                     }
                   ]
   }
    ```
   Link validation is configured for `video_url` within this project. Only links to YouTube can be provided


2. Stripe Payment Creation  
Available at the endpoint http://localhost:8000/users/payment/ (POST method)  
Example request body:
    ```
    {
        "amount": 10000, # specify an integer value (in rubles)
        "method": "card",
        "course_subject": 1 # id of the course for payment
    }
    ```
    You can create a payment for a course or a separate lesson by specifying either `course_subject` or `lesson_subject`  
In the response body, you will receive a link to Stripe payment, where you can enter your card details
     
#### 5. Other Interaction Methods:
You can find all interaction methods in the documentation
</details>

## Documentation
API documentation is available at:
- Swagger - http://localhost:8000/swagger/
- Redoc - http://localhost:8000/redoc/



Project Author: Maria Kuznetsova - [kuznetsova19.m@gmail.com](mailto:kuznetsova19.m@gmail.com)
                   