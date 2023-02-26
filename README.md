# Learning_Advanced_Django
Repeating how to set up a Django server, deploying with mod_wsgi and attempting to create a rest api

## Setup Venv
1. To create a virtual enviroment: 
```bash
$ python3 -m venv .venv
```
2. To activate the virtual enviroment: 
```bash
$ source .venv/bin/activate
``` 

## Start django project
1. Download django in the venv: 
```bash
$ pip3 install django
```
2. Test it with django admin
```bash
$ django-admin --version
```
3. Create a project:
```bash
$ django-admin startproject my_project
```
4. Run the project:
```bash
$ cd my_project
$ python3 manage.py runserver
```

## Track dependencies
1. To see a list of dependencies:
```bash
$ pip3 freeze
```
2. To list all dependencies in the requirements.txt file:
```bash
$ pip3 freeze > requirements.txt
```
3. To get all dependencies from the file:
```bash
$ pip3 install -r /requirements.txt
```

## Prouction server on ubuntu
1. Download project to production server via github or whatever gets the job done.
2. Add ip or domain to allowed hosts, if testing runserver dont forget 0.0.0.0:8000 to run on ip and not localhost.
3. Download gcc 'compiler' and python3.10-dev.
```bash
$ sudo apt-get install python3.10-dev
$ sudo apt-get install gcc
```
4. Install uWSGI.
```bash
$ pip3 install uwsgi
```
5. Test out uwsgi with the wsgi file test.py.
```bash
$ uwsgi --http :8000 --wsgi-file test.py
```
6. Test it out on the wsgi module in the project.
```bash
$ uwsgi --http :8000 --module restasured.wsgi
```
7. Install nginx.
```bash
$ sudo apt-get install nginx
```
8. Create a configuration file.
```bash
$ cd /etc/nginx/sites-available
$ touch restasured.conf
```
9. Configure the file with whatever text editor at your disposal. Here is a basic configuration.
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
10. create the uwsgi_params file in the location specified. Here are the default params.
```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;


uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;
uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```
11. Sim link the configuration file to the sites enabled directory.
```bash
$ sudo ln -s /etc/nginx/sites-available/restasured.conf /etc/nginx/sites-enabled
```
12. Configure the static root in the settings.py file.
```py
STATIC_URL = '/static/'
STATIC_ROOT = PATH.joinpath(BASE_DIR, "static/")
```
13. Create static folders acording to configuration on server.
```bash
$ python3 manage.py collectstatic
```
14. Create a media directory as specified in the .conf file. Add an image to it to test it out.
```bash
$ mkdir /home/megatron/Projects/Learning_Advanced_Django/restasured/media
$ wget https://upload.wikimedia.org/wikipedia/commons/b/b9/First-google-logo.gif -O media/media.gif
```
15. Restart the nginx server:
```bash
$ sudo /etc/init.d/nginx restart
```
- Make sure that all the folders above static and media have an adequate premission level of 755 and the files have at least a premission level of 644. If you f.ex put your file in a user folder /home/user it might have a premission level of 750 wich does not allow nginx to even execute the files. To change a file or folders premsiion level.
```bash
$ chmod 755 folder/file
``` 
16. Create a socket to django.
```bash
$ uwsgi --socket restasured.sock --module restasured.wsgi --chmod-socket=664
```
17. Instead of passing arguments directly to uwsgi you can streamline the process in a file.
```bash
$ touch /home/megatron/Projects/Learn_Advanced_Django/restasured/restasured_uwsgi.ini
```
```ini
[uwsgi]

# full path to Django project's root directory
chdir            = /home/megatron/Projects/Learning_Advanced_Django/restasured
# Django's wsgi file
module           = restasured.wsgi
# full path to python virtual env
home             = /home/megatron/Projects/Learning_Advanced_Django/.venv

# enable uwsgi master process
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = /home/megatron/Projects/Learning_Advanced_Django/restasured/restasured.sock
# socket permissions
chmod-socket    = 666
# clear environment on exit
vacuum          = true
# daemonize uwsgi and write messages into given log
daemonize       = /home/megatron/uwsgi-emperor.log
```
### Set up emperor and vassals to auo restart server on crash and configure multiple servers from one.
1. Create a new vassals directory in .venv
```bash
$ cd .venv
$ mkdir vassals
```
2. Make a simlink from the .ini file to the vassals directory.
```bash
$ sudo ln -s /home/megatron/Projects/Learn_Advanced_Django/restasured/restasured_uwsgi.ini /home/megatron/Projects/Learn_Advanced_Django/.venv/vassals
```
3. Check if it succeeded.
```bash
$ ls ./vassals
```
4. Reboot the server.
```bash
$ sudo reboot
```
5. When ubuntu has rebooted run the server in emperor-mode.
```bash
$ source .venv/bin/activate
$ uwsgi --emperor /home/megatron/Projects/Learn_Advanced_Django/.venv/vassals --uid www-data --gid www-data
```
6. Create a service that starts the server on boot.
```bash
$ touch /etc/systemd/system/emperor.uwsgi.service
$ sudo nano /etc/systemd/system/emperor.uwsgi.service
```
```service
[Unit]
Description=uwsgi emperor for restasured website
After=network.target

[Service]
User=megatron
Restart=always
ExecStart=/home/megatron/Projects/Learn_Advanced_Django/.venv/bin/uwsgi --emperor /home/megatron/Projects/Learn_Advanced_Django/.venv/vassals --uid www-data --gid www-data

[Install]
WantedBy=multi-user.target
```
7. Enable it with systemctl
```bash
$ systemctl enable emperor.uwsgi.service
```
8. Test it out by rebooting or starting it manualy like this.
```bash
$ systemctl start emperor.uwsgi.service
```