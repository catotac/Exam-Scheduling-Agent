# Exam Scheduling Application

## Introduction

This application is developed for COM S 572 Artificial Intelligence course offered in Fall 2017 semester at Iowa State University.

The application runs on the web browser and implements latest web technologies via combining [Bootstrap](https://getbootstrap.com/) and [Django](https://www.djangoproject.com/) frameworks with [Python programming language](https://www.python.org/). It consists of 2 algorithms, a greedy algorithm and simulated annealing, to solve for exam scheduling and proctor assignment problems at the same time.

## Requirements

Python 2.7.14 w/ Django 1.11.8 OR Python 3.6.3 w/ Django 2.0

### Installation Instructions

Please download the official Python distribution from [python.org](https://www.python.org/). For [Django](https://www.djangoproject.com/) installation, please see the following since it depends on the Python version used:

#### For Python v2.7.14

`pip2 install Django==1.11.8`

#### For Python v3.6.3

`pip3 install Django`

## Running the Application

The application depends on [Django Framework](https://www.djangoproject.com/), so please make sure that you have installed it correctly.

### How-to check if Django is installed correctly

Run `python` interpreter and execute the following commands:

```python
import django
django.get_version()  # it will show something like '1.11.8'
exit()  # to quit python shell
```

Before running the application, there are some steps to for initialization:

### Create Database and Tables

`python manage.py migrate`

Defaults to SQLite which comes with all Python distributions by default so,  no need to install anything extra, even you don’t need to download SQLite3 from its website.

### Create Admin User

`python manage.py createsuperuser`

Please follow the instructions on the command window, then access the admin page using [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Run Web Server

`python manage.py runserver`

Please follow the instructions on the command window to access the website

## Additional Information

### Dumping & Reloading the Database

1. Assuming that you have some data in your database, use the command to dump database to a file named data.json: `python manage.py dumpdata > data.json`
2. Clear the existing contents of the database: `python manage.py flush --no-input`
3. Import the previous database contents to the empty database: `python manage.py loaddata data.json`

### Entering Django Shell

`python manage.py shell`

Django shell is simply the Django Framework environment loaded on a Python interpreter instance so that, you can access all features of the Django application from the command line. It is like running the web server without the GUI access.

## Authors

* __Onur Bingol:__ GUI and integration
* __Rahul Singh:__ Greedy algorithm
* __Lei Liu:__: Simulated annealing algorithm
