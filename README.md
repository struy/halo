
# Python Flask microservice.

* Backend: Flask,  Sqlalchemy
* Frontend: Bootstrap 4, JQuery 3

### demo user and password ("admin", "password")

##########################

USE VENV:

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt 

python3 models.py

python3 seeds.py

python3 app.py

##########################

OR USE DOCKER:

docker build -t flask-halo-api  .

docker-compose up -d

### http://127.0.0.1:2020/
