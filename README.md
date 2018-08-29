__
# Python Flask microservice.

* Backend: Flask,  Sqlalchemy
* Frontend: Bootstrap 4, JQuery 3

### demo user and password ("admin", "password")

git clone https://github.com/struy/halo.git

_USE VENV:_

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt 

python3 models.py

python3 seeds.py

python3 app.py

_OR USE DOCKER:_

docker build -t flask-halo-api  .

docker-compose up -d

_RESULT:_

### http://127.0.0.1:2020/
