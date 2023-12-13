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
![image](https://github.com/VasylTurok/train-station/assets/127683195/80421bf4-c5dd-4098-a8c3-ca090781d2f3)


>Create superuser with

```bash
$ python manage.py createsuperuser
```

## Site 
![image](https://github.com/VasylTurok/train-station/assets/127683195/48488a04-8c3f-45f2-98a6-4011ac2d12e7)
![image](https://github.com/VasylTurok/train-station/assets/127683195/371b91f0-9c7c-49a6-b96a-7b471e5395af)
![image](https://github.com/VasylTurok/train-station/assets/127683195/e571ef00-932d-4c71-a2ec-725b222758c7)
![image](https://github.com/VasylTurok/train-station/assets/127683195/7189ab61-a2cc-48e1-b39b-f986452b64cb)
![image](https://github.com/VasylTurok/train-station/assets/127683195/1fe06c80-1894-4b0e-91bd-4633397bfdb5)
![image](https://github.com/VasylTurok/train-station/assets/127683195/de87086a-2150-4ac1-b92e-3643428caaee)
![image](https://github.com/VasylTurok/train-station/assets/127683195/959fd573-b296-428f-8edb-5539a894648e)
![image](https://github.com/VasylTurok/train-station/assets/127683195/ae0ccba7-d551-4f59-aaaf-2672fdda7278)
![image](https://github.com/VasylTurok/train-station/assets/127683195/eee04bdb-d322-4aac-846a-07710fed8dcc)
![image](https://github.com/VasylTurok/train-station/assets/127683195/84b0ea8b-4da7-4264-a4a7-255c9c1b6d49)


## Test
Use `python manage.py test` to run tests.




