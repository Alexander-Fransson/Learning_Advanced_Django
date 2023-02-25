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
* Install uWSGI.
```bash
$ pip3 install uwsgi
```
* Test out uwsgi with the wsgi file test.py.
```bash
$ uwsgi --http :8000 --wsgi-file test.py
```
* Test it out on the wsgi module in the project.
```bash
$ uwsgi --http :8000 --module restasured.wsgi
```
* Install nginx.
```bash
$ sudo apt-get install nginx
```
* Create a configuration file.
```bash
$ cd /etc/nginx/sites-available
$ touch restasured.conf
```
* Configure the file with whatever text editor at your disposal. Here is a basic configuration.
```conf
# the upstream component nginx needs to connect to
upstream django {
    server unix:///home/megatron/Projects/Learning_Advanced_Django/restasured/restasured.sock;
}

# configuration of the server
server {
    listen      80;
    server_name 192.168.64.3 www.192.168.64.3;
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;

    # Django media and static files
    location /media  {
        alias /home/megatron/Projects/Learning_Advanced_Django/restasured/media;
    }
    location /static {
        alias /home/megatron/Projects/Learning_Advanced_Django/restasured/static;
    }

    # Send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/megatron/Projects/Learning_Advanced_Django/restasured/uwsgi_params;
    }
}
```
* create the uwsgi params file in the location specified
