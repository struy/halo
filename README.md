
# Python Flask microservice.

* Backend: Flask,  Sqlalchemy
* Frontend: Bootstrap 4, JQuery 3

### demo user and password ("admin", "password")
##########################
### VENV
##########################
python3 -m venv env
source env/bin/activate
##########################
### Requirements
###############################
pip install -r requirements.txt 

################################
###Create db and seeds
python3 models.py

python3 seeds.py

################################
### Start aplication
python3 app.py

