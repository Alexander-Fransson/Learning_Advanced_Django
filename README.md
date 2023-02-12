# Learning_Advanced_Django
Repeating how to set up a Django server, deploying with mod_wsgi and attempting to create a rest api

## Setup Venv
* To create a virtual enviroment: 
```bash
$ python3 -m venv .venv
```
* To activate the virtual enviroment: $ source .venv/bin/activate 

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
