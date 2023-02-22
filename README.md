# Learning_Advanced_Django
Repeating how to set up a Django server, deploying with mod_wsgi and attempting to create a rest api

## Setup Venv
* To create a virtual enviroment: 
```bash
$ python3 -m venv .venv
```
* To activate the virtual enviroment: 
```bash
$ source .venv/bin/activate
``` 

## Start django project
* Download django in the venv: 
```bash
$ pip3 install django
```
* Test it with django admin
```bash
$ django-admin --version
```
* Create a project:
```bash
$ django-admin startproject my_project
```
* Run the project:
```bash
$ cd my_project
$ python3 manage.py runserver
```

## Track dependencies
* To see a list of dependencies:
```bash
$ pip3 freeze
```
* To list all dependencies in the requirements.txt file:
```bash
$ pip3 freeze > requirements.txt
```
* To get all dependencies from the file:
```bash
$ pip3 install -r /requirements.txt
```

## Prouction server on ubuntu
* Download project to production server via github or whatever gets the job done.
* Add ip or domain to allowed hosts, if testing runserver dont forget 0.0.0.0:8000 to run on ip and not localhost.
* Download gcc 'compiler' and python3.10-dev.
```bash
$ sudo apt-get install python3.10-dev
$ sudo apt-get install gcc
```
* Install uWSGI
```bash
$ pip3 install uwsgi
```