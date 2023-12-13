# train-station

## Introduction
The Train Station Project is a web application built using Django and Django REST Framework to manage and provide information about train stations. This project aims to offer a convenient platform for users to access details about train stations, including schedules, arrivals, departures, and other relevant information.

## Features
- JWT authenticated

- Admin panel /admin/

- Documentation is located at api/doc/swagger/ or api/doc/redoc/

- Managing orders and tickets

- Creating train with train_type

- Creating trip with train, route, crews

- Filtering for crews, train_types, routes, stations, trains, trips, tickets


## Installation with GitHub

 Clone the repository:
```bash
$ https://github.com/VasylTurok/train-station.git
$ cd train_station
```
> 👉 Install modules via `VENV`  

On Linux and Mac:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

On Windows:

```bash
$ python -m venv venv
$ .\venv\Scripts\activate
```

## Run project
```bash
$ pip install -r requirements.txt
$ set POSTGRES_HOST=<your db hostname>
$ set POSTGRES_NAME=<your db name>
$ set POSTGRES_USER=<your db username>
$ set POSTGRES_PASSWORD=<your db user password>
$ set SECRET_KEY=<your secret key>
$ python manage.py migrate
$ python manage.py runserver
```
At this point, the app runs at `http://127.0.0.1:8000/`. 

## Run with Docker
Docker should be installed
```bash
$ docker-compose build
$ docker-compose up
```

## Getting access

- create user via api/user/register/
- get access token api/user/token/



## Model DB


>Create superuser with

```bash
$ python manage.py createsuperuser
```

## Site 


## Test
Use `python manage.py test` to run tests.




